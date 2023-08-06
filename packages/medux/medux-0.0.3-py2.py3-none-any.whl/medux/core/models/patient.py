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

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .common import BaseModel
from .datapacks import PackageDataModel
from .organizations import HealthServiceProvider, Person

__all__ = [
    "Patient",
    "Encounter",
    "Problem",
    "NarrativeType",
    "Narrative",
]


class RelationType(models.Model):
    """A relation between 2 identities.

    This could be father, mother, son, daughter, uncle, friend etc."""

    name = models.CharField(max_length=255)


class Patient(Person):
    # see https://www.hl7.org/fhir/valueset-marital-status.html#expansion
    MARITIAL_STATUS_CHOICES = (
        ("A", _("Annulled")),
        ("D", _("Divorced")),
        ("I", _("Interlocutory")),
        ("L", _("Legally Separated")),
        ("M", _("Married")),
        ("P", _("Polygamous")),
        ("S", _("Never Married")),
        ("T", _("Domestic partner")),
        ("U", _("Unmarried")),
        ("W", _("Widowed")),
        ("UNK", _("Unknown")),
    )
    # mandatory fields:
    # name(s), birth_date, gender
    person = models.OneToOneField(
        Person, parent_link=True, on_delete=models.PROTECT, related_name="+"
    )

    marital_status = models.CharField(
        max_length=3, null=True, blank=True, choices=MARITIAL_STATUS_CHOICES
    )

    general_practitioner = models.ForeignKey(
        "Physician",
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        help_text=_("The patient's general practitioner"),
        related_name="+",
    )
    physicians = models.ManyToManyField(
        "Physician",
        blank=True,
        help_text=_("Physicians the patient consults regularly"),
        related_name="+",
    )

    related_persons = models.ManyToManyField(
        "Patient", through="Relationship", related_name="+"
    )

    # Link to another Person to be used as emergency contact
    emergency_contact = models.ManyToManyField(
        Person,
        help_text=_("Persons who should be contacted in case of an emergency"),
        related_name="+",
        blank=True,
    )

    # Free text emergency contact information.
    emergency_contact_freetext = models.CharField(max_length=255, blank=True, null=True)

    comment = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text=_("Generic comment for this patient"),
    )

    # # TODO: implement generatePupic and set required=True
    # pupic = models.CharField(
    #     max_length=24,
    #     blank=True,
    #     null=True,
    #     editable=False,
    #     help_text=_(
    #         "Portable Unique Person "
    #         "Identification Code as per GNUmed "
    #         "white papers"
    #     ),
    # )
    #
    # def generate_pupic(self):
    #     """Generates a Portable Unique Person Identification according to
    #     GNUmed definition"""
    #     # TODO: implement PUPIC generation
    #     return ""


class Relationship(models.Model):
    """A related person model to be used as through= table."""

    from_patient_id = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name="+"
    )
    to_patient_id = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name="+"
    )
    relation_type = models.ForeignKey(RelationType, on_delete=models.PROTECT)


# TODO: use BaseModel?


class Encounter(BaseModel):
    """A clinical encounter between a person and the health care system."""

    date = models.DateTimeField(default=timezone.now)

    # FIXME: add a function to set this to "anonymous" in case of deletion of HSP
    provider = models.ForeignKey(HealthServiceProvider, on_delete=models.PROTECT)


class Problem(BaseModel):
    """Represents a clinical problem during a time.

    In other specifications, this could be named health issue, condition
    (FHIR), diagnosis etc.
    One or more (ICPC2/ICD10 coded) diagnoses could be a part of a problem,
    but there could be problems that have no clear diagnosis as well.
    """

    name = models.CharField(max_length=255)


class NarrativeType(models.Model):
    """The type of a narrative.

    This per default are the first 2 letters of narratives in the SOAP schema:
    S subjective, anamnesis
    O objective, findings
    A assessment, differential diagnoses
    P plan - what to do next
    """

    shortcut = models.CharField(primary_key=True, max_length=2)
    name = models.CharField(max_length=100)


class Narrative(BaseModel):
    type = models.ForeignKey(NarrativeType, on_delete=models.PROTECT)
    encounter = models.ForeignKey(Encounter, on_delete=models.CASCADE)

    problem = models.ForeignKey(Problem, on_delete=models.PROTECT)
    narrative = models.TextField()


class Firstname(PackageDataModel):
    """Model for saving packages with firstnames, matched with the correct gender.

    See https://github.com/MatthiasWinkelmann/firstname-database, under GNU Free Documentation License 1.2+
    """

    NAME_GENDER_CHOICES = (
        ("M", "Male"),
        ("1M", "male if first part of name, otherwise mostly female"),
        ("?M", "mostly male"),
        ("F", "Female"),
        ("1F", "female if first part of name, otherwise mostly male"),
        ("?F", "mostly female"),
        ("?", "unisex"),
    )
    name = models.CharField(max_length=50)
    sex = models.CharField(max_length=2, choices=NAME_GENDER_CHOICES)
