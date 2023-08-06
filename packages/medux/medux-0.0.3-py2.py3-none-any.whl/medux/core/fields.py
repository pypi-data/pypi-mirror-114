"""
MedUX - A Free/OpenSource Electronic Medical Record
Copyright (C) 2017-2021 Christian González

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
from typing import Union

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.core import exceptions
from django.utils.datetime_safe import datetime

import base64
from uuid import uuid4

from environ import ImproperlyConfigured

from medux.core.validators import (
    fhir_server_allowed_references,
    CodeValidator,
    IdValidator,
    OidValidator,
)

__author__ = "Christian González <christian.gonzalez@nerdocs.at>"

# TODO: Fields could be done better, see http://build.fhir.org/datatypes.html
# These types should be implemented very carefully, with all the validators
# and custom behaviours in place.
# Especially the ReferenceField is used very often and should be implemented
# very well.


from django import forms
from django.conf import settings


class OptionalTimeDateTimeField(models.DateTimeField):
    """Field that optionally uses the time format.

    Set MEDUX["BIRTHDAY_FORMAT"] in settings.py to either "Date" or "DateTime" to use the desired format.
    """

    def formfield(self, **kwargs):
        field = None
        try:
            if settings.MEDUX["BIRTHDAY_FORMAT"] == "Date":
                field = forms.DateField
            elif settings.MEDUX["BIRTHDAY_FORMAT"] == "DateTime":
                field = forms.DateTimeField
            else:
                raise ImproperlyConfigured(
                    f"MEDUX['BIRTHDAY_FORMAT'] settings variable contains wrong value '{settings.MEDUX['BIRTHDAY_FORMAT']}'. Please set it to 'Date' or 'DateTime'."
                )
        except AttributeError:
            raise ImproperlyConfigured(
                "MEDUX settings variable does not contain a 'BIRTHDAY_FORMAT'. Please set it to 'Date' or 'DateTime'."
            )
        # FIXME: DateField is ignored in Admin
        return super().formfield(
            **{
                "form_class": field,
                **kwargs,
            }
        )


# ===================== Primitive types =====================
# Primitive types are those with only a value,
# and no additional elements as children.
# see examples: http://build.fhir.org/datatypes-examples.html#primitives
# ===========================================================


class Base64TextField(models.TextField):
    """A stream of bytes, base64 encoded"""

    # TODO: +RegexValidator '(\s*([0-9a-zA-Z\+\=]){4}\s*)+'
    def from_db_value(value):
        """Returns a str from the database value,
        which is encoded as base64 string"""

        if value is None:
            return None
        else:
            return base64.b64decode(value).decode("utf-8")

    # TODO: read only yet


# StringFields are implemented either as Textfields, or as Charfields,
# depending on how many chars (>255) are possible. Some databases do not
# implement more than 255 chars in a string.


class StringListField(models.TextField):
    """Represents a list of strings.

    in FHIR resources, there is often a string[0..*] needed. As Django
    Doesn't provide a string list field, this is a simple implementation.
    Other implementations would be possible using JSONfield on PostGreSQL."""

    # TODO: implement this field completely.
    # TODO: Beware of strings >255 chars
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def to_python(self, value):
        """Normalize data to a list of strings."""
        # Return an empty list if no input was given.
        if not value:
            return []
        return value.split("\n")


class InstantField(models.DateTimeField):
    """An instant in time

    It must be known at least to the second and always includes a time zone.
    Note: This type is for system times, not human times."""

    def __init__(self, *args, **kwargs):
        kwargs["validators"] = [
            RegexValidator(
                r"([0-9]([0-9]([0-9][1-9]|[1-9]0)|"
                r"[1-9]00)|[1-9]000)-(0[1-9]|1[0-2])-"
                r"(0[1-9]|[1-2][0-9]|3[0-1])T([01][0-9]|2[0-3]):"
                r"[0-5][0-9]:"
                r"([0-5][0-9]|60)(\.[0-9]+)?(Z|(\+|-)"
                r"((0[0-9]|1[0-3]):[0-5][0-9]|14:00))"
            )
        ]
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()

        del kwargs["validators"]
        return name, path, args, kwargs


# ===================== Complex types =====================
# In XML, these types are represented as XML Elements with child elements
# with the name of the defined elements of the type.
# The name of the element is defined where the type is used.
# In JSON, the data type is represented by an object with properties named
# the same as the XML elements. Since the JSON representation is almost
# exactly the same, only the first example has an additional explicit
# JSON representation.
#
# Complex data types may be "profiled".
# A Structure Definition or type "constraint" makes a set of rules about
# which elements SHALL have values and what the possible values are.
# ===========================================================


class ManyReferenceField(models.ManyToManyField):
    def __init__(self, to: str, **kwargs):

        self.allowed_references = to.split("|")
        for ref in self.allowed_references:
            if ref not in fhir_server_allowed_references.split("|"):
                raise exceptions.FieldError(
                    _("'{}' is not allowed as reference in {}".format(ref, "<FIXME>"))
                )

        # No matter what this field should (dynamically) refer to,
        # always make sure the Foreign key is bound to a "Reference" object
        kwargs["to"] = "Reference"
        super().__init__(**kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs["to"] = "|".join(self.allowed_references)
        return name, path, args, kwargs


class CodeableConceptField(models.ForeignKey):
    def __init__(self, value_set: str, *args, **kwargs):
        assert type(value_set) == str

        self.allowed_codings = value_set.split("|")

        # always refer to the model "CodeableConcept", no matter what is given
        kwargs["to"] = "CodeableConcept"

        # FIXME: is SET_NULL ok everywhere?
        kwargs["null"] = True
        kwargs["on_delete"] = models.SET_NULL
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs["null"]
        kwargs["value_set"] = "|".join(self.allowed_codings)
        return name, path, args, kwargs


# url is represented by Django's URLField
class UriField(models.URLField):
    """A Uniform Resource Identifier Reference.

    This is a URI, as defined in RFC 3986: https://tools.ietf.org/html/rfc3986
    Note: URIs generally are case sensitive. For an UUID like
    (urn:uuid:ad1b1c1b-96b0-4c4d-a826-2b6e31f0512b) use all lowercase letters!
    """

    # TODO: implementation
    def __init__(self, *args, **kwargs):
        # FIXME: we set this to an arbitrary 255 char string as max. could be more specific
        kwargs["max_length"] = 255
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs["max_length"]
        return name, path, args, kwargs


class UrlField(UriField):
    """A Uniform Resource Locator (RFC 1738 ).

    Note: URLs are accessed directly using the specified protocol.
    Common URL protocols are http(s):, ftp:, mailto: and mllp:,
    though many others are defined.
    """


class CanonicalField(UriField):
    """A URI that refers to a canonical URI.

    The canonical type differs from a uri in that it has special meaning
    in this specification, and in that it may have a version appended,
    separated y a vertical bar (|).

    URIs can be absolute or relative, and may have an optional fragment
    identifier.
    This data type can be bound to a value set
    """


# class PositiveIntField(models.PositiveIntegerField):
#     description = _("Positive integer >= 1")
#
#     def formfield(self, **kwargs):
#         defaults = {"min_value": 1}
#         defaults.update(kwargs)
#         return super().formfield(**defaults)


# class UnsignedIntField(models.PositiveIntegerField):
#     description = _("Positive integer >= 0")
#
#     # this is the Django implementation of PositiveIntegerField


class CodeField(models.CharField):
    """Represents a field with a "code" that is defined elsewhere.

    This field must not contain arbitrary strings, but only the ones that are defined in the given
    terminology system.

    Technically, a code is restricted to a string which has at least one
    character and no leading or trailing whitespace, and where there is no
    whitespace other than single spaces in the contents"""

    # TODO: This could be a ForeignKey, pointing to a FHIR ValueSet class!
    description = _('A "code" that is defined elsewhere')
    default_validators = [CodeValidator]
    default_error_messages = {
        "not_multiple": _('There are no multiple values allowed in "{key}".'),
    }

    def __init__(
        self, terminology_binding: str = None, multi: bool = False, *args, **kwargs
    ):

        assert terminology_binding is None or type(terminology_binding) == str

        # The ValueSet this code is defined in
        self.terminology_binding = terminology_binding
        # are multiple values allowed?
        self.multi = multi

        # TODO: we set this to an arbitrary 64 char string as max.
        # Could be more specific
        kwargs["max_length"] = 64

        # value_set = "Patient"  # FIXME: this is just a demo
        # does not work: ValueSet.objects.name(name=terminology_binding).first() # etc

        # if not value_set:
        #     raise exceptions.ValidationError(
        #         "Terminology binding {} not found.".format(terminology_binding)
        #     )
        choices = {}
        kwargs["choices"] = choices
        super().__init__(*args, **kwargs)

    def validate(self, value, model_instance):
        super().validate(value, model_instance)
        # print(value)
        #        for key, val in value.items():
        #            if True:
        #                raise exceptions.ValidationError(
        #                    self.error_messages['not_multiple'],
        #                    code='not_multiple',
        #                    params={'key': key},
        #                )
        return

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs["max_length"]
        kwargs["terminology_binding"] = self.terminology_binding
        kwargs["multi"] = self.multi
        return name, path, args, kwargs


class OidField(UriField):
    """An OID represented as a URI"""

    def __init__(self, *args, **kwargs):
        kwargs["validators"] = [OidValidator]
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs["validators"]
        return name, path, args, kwargs


class IdField(models.CharField):
    """A field that can be used for an ID of an Object.

    Any combination of upper or lower case ASCII letters ('A'..'Z', and 'a'..'z',
    numerals ('0'..'9'), '-' and '.', with a length limit of 64 characters.
    This might be an integer, an un-prefixed OID, UUID or any other identifier
    pattern that meets these constraints."""

    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 64
        kwargs["default"] = uuid4()
        kwargs["validators"] = [IdValidator]
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs["max_length"]
        del kwargs["default"]
        del kwargs["validators"]
        return name, path, args, kwargs


class MarkdownField(models.TextField):
    """A string that *may* contain markdown syntax.

    This can be used for optional processing by a markdown presentation engine"""

    # TODO: implement Validator: \s*(\S|\s)*


# http://hl7.org/fhir/narrative-status
# FIXME: implement/import as ValueSet
NARRATIVE_STATUS = (
    ("generated", _("Generated")),
    ("extensions", _("Extensions")),
    ("additional", _("Additional")),
    ("empty", _("Empty")),
)


# ======================== Special data types ========================


# class ReferenceField(models.ForeignKey):
#     """A field that holds a Foreignkey to a Reference Object,
#     which points to another FHIR Resource
#
#     At least one of reference, identifier and display SHALL be present
#     (unless an extension is provided).
#     The Reference object should return the real object.
#     FIXME this has to be coded in Django, does not work yet.
#     """
#
#     # This regex is true if the reference to a resource is consistent with a FHIR API
#     fhir_server_abs_url_conformance = (
#         r"((http|https)://([A-Za-z0-9\\\.\:\%\$]\/)*)?("
#         + fhir_server_allowed_references
#         + ")\/[A-Za-z0-9\-\.]{1,64}(\/_history\/[A-Za-z0-9\-\.]{1,64})?"
#     )
#
#     description = _("A dynamic reference to another Resource")
#
#     def __init__(self, to: str, **kwargs):
#         """Creates a new Reference Field.
#
#         The 'to' parameter is always overwritten and set to "Reference",
#         as the Reference db table works as intermediate mapper to the "real"
#         reference where this field points to.
#
#         Note: the 'on_delete' parameter must be set manually, as it could
#         change according to the context.
#         :param str to: one or more possible FHIR resources where an object
#             could point to. If there are more than one, use '|' as separator.
#             Example: 'Patient|Practitioner|Organization'
#         :raises FieldError: if the 'to' parameter is a not allowed resource.
#         """MarkdownField
#
#         assert type(to) == str
#
#         self.allowed_references = to.split("|")
#         for ref in self.allowed_references:
#             if ref not in fhir_server_allowed_references.split("|"):
#                 raise exceptions.FieldError(
#                     _("'{}' is not allowed as reference in {}".format(ref, "<FIXME>"))
#                 )
#
#         # No matter what this field should (dynamically) refer to,
#         # always make sure the Foreign key is bound to a "Reference" object
#         kwargs["to"] = "Reference"
#         super().__init__(**kwargs)
#
#     def deconstruct(self):
#         name, path, args, kwargs = super().deconstruct()
#         kwargs["to"] = "|".join(self.allowed_references)
#         return name, path, args, kwargs


# class NarrativeField(models.TextField):
#
#     # http://hl7.org/fhir/ValueSet/narrative-status
#     # general, extensions, additional, empty
#     status = models.CharField(max_length=35, choices=NARRATIVE_STATUS)
#
#     # TODO: implement a XHTMLField
#     # The XHTML content SHALL NOT contain a head, a body element, external stylesheet references,
#     # deprecated elements, scripts, forms, base/link/xlink, frames, iframes, objects or event related attributes
#     # (e.g. onClick).This is to ensure that the content of the narrative is contained within the resource
#     # and that there is no active content. Such content would introduce security issues and potentially safety
#     # issues with regard to extracting text from the XHTML.
#     div = models.TextField(null=False, blank=False)


class Period:
    """A period of Time, with optional start/end"""

    def __init__(self, start: datetime = None, end: datetime = None):
        self.start = start
        self.end = end

    def __len__(self):
        return 2 * 25 + 1


class PeriodField(models.CharField):
    """A Field representing a period in time, with optional start or end.

    One of [start|end] must be given."""

    # TODO: make a date(time) widget

    description = "A period of Time, with optional start/end"

    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 2 * 25 + 1
        super().__init__(*args, **kwargs)

    def deconstruct(self) -> tuple:
        name, path, args, kwargs = super().deconstruct()
        del kwargs["max_length"]
        return name, path, args, kwargs

    def _parse(self, value: str) -> Period:
        start, end = value.split(";")
        if start:  # datetime
            start = datetime.fromisoformat(start)
        if end:
            end = datetime.fromisoformat(end)
        return Period(start, end)

    def to_python(self, value) -> Union[Period, None]:
        if isinstance(value, Period):
            return value

        if value is None:
            return value

        if isinstance(value, str):
            return self._parse(value)

        raise ValidationError(f"Could not parse Period value: {value}")

    def get_prep_value(self, value: Period) -> str:
        """serializes a Period value into a db saveable string"""
        if isinstance(value, Period):
            start = str(value.start.isoformat()) if value.start else ""
            end = str(value.end.isoformat()) if value.end else ""
            return ";".join([start, end])
