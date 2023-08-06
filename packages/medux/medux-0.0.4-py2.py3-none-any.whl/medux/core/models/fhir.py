from django.db import models
from django.db.models import PositiveIntegerField
from django.utils.timezone import now
from django.utils.translation import gettext as _, pgettext

from .datapacks import PackageDataModel
from .common import BaseModel
from ..fields import Period, PeriodField


def ongoing_period() -> str:
    return ";".join([now().isoformat(), ""])


class Element(BaseModel):
    """The base definition for all elements contained inside a resource.

    All elements, whether defined as a Data Type (including primitives) or as
    part of a resource structure, have this base content:

    * Extensions
    * an internal id
    """

    # This field originally is named "extension". This causes some problems
    # with name clashing. So, as it's a ManyToManyField anyway, we renamed
    # it to "extensions"
    # extensions = models.ManyToManyField("Extension", related_name="+", blank=True)

    class Meta:
        abstract = True

    def to_xml(self):
        raise NotImplementedError

    def to_json(self):
        raise NotImplementedError


# class Extension(Element):
#     # SHALL be a URL, not a URN (e.g. not an OID or a UUID),
#     url = UriField()
#
#     # FIXME: this field in reality should be more flexible.
#     # see http://build.fhir.org/extensibility.html#Extension
#     # value = models.CharField(max_length=255, blank=True)
#
#     class Meta:
#         abstract = True


#
# class Period(models.Model):
#     """A time period defined by a start and end date/time.
#
#     If the start element is missing, the start of the period is not known.
#     If the end element is missing, it means that the period is ongoing, or the
#     start may be in the past, and the end date in the future, which means that
#     period is expected/planned to end at the specified time.
#     """
#
#     start = OptionalTimeDateTimeField(blank=True, null=True)
#     end = OptionalTimeDateTimeField(blank=True, null=True)
#
#     def __str__(self):
#         # TODO: return date with local format
#         return f"{self.start or _('unknown')} - {self.end or _('ongoing')}"
#
#     class Meta:
#         pass
#         # constraints = [
#         #     # Check if either start or end is presents
#         #     models.CheckConstraint(
#         #         check=models.Q(start__isnull=False) | models.Q(end__isnull=False),
#         #         name="either_start_or_end_present",
#         #     )
#         # ]


class ContactPoint(Element):
    """Details for all kinds of technology-mediated contact points.

    These can be for a person or organization, and includes telephone, email, etc.
    """

    CONTACT_POINT_SYSTEM = (
        ("phone", _("Phone")),
        ("fax", _("Fax")),
        ("email", _("Email")),
        ("pager", _("Pager")),
        ("url", _("URL")),
        ("sms", _("SMS")),
        ("other", _("Other")),
    )

    CONTACT_POINT_USE = (
        (
            "home",
            pgettext("at home", "Home"),
        ),
        ("work", _("Work")),
        ("temp", _("Temporary")),
        ("old", _("Old")),  # not in use anymore, or was never correct
        ("mobile", _("Mobile")),
    )

    # links to ContactPointSystem
    # http://hl7.org/fhir/ValueSet/contact-point-system
    system = models.CharField(max_length=20, choices=CONTACT_POINT_SYSTEM)

    value = models.CharField(max_length=255, blank=True)

    # links to ContactPointUse
    # http://hl7.org/fhir/ValueSet/contact-point-use
    use = models.CharField(max_length=20, choices=CONTACT_POINT_USE, blank=True)

    # in FHIR, this is actually "rank" - but could be easily converted when exporting.
    # we stay with "weight" to be consistent with MedUX
    weight = PositiveIntegerField(blank=True, default=1)

    period = PeriodField(default=ongoing_period)
    # period = models.ForeignKey(
    #     Period,
    #     on_delete=models.SET_NULL,
    #     blank=True,
    #     null=True,
    #     help_text=_("The period in which this contact point is valid."),
    # )

    def __str__(self):
        return f"{[value for key, value in self.CONTACT_POINT_SYSTEM if key == self.system][0]}: {self.value}"


# https://fhir-ru.github.io/codesystem-administrative-gender.html
class AdministrativeGender(models.Model):
    #: the (mostly single char) gender, like "m", "f", etc.
    tag = models.CharField(primary_key=True, max_length=2)

    label = models.CharField(max_length=50)
    sort_weight = models.IntegerField(default=0)
    comment = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.label


# http://hl7.org/fhir/CodeSystem/medication-statement-status
class CodeValueSet(PackageDataModel):
    """Represents a ValueSet for Status items, like EpisodeStatus, MedicationStatus.

    You have to subclass this model to make use of it, as it is an abstract model.

    Each instance has the minimum fields:
    * code: the code that represents this item
    * display: the human readable code in short form
    * definition: a detailed description of the item
    """

    code = models.CharField(max_length=50)
    display = models.CharField(max_length=50)
    definition = models.CharField(max_length=255)

    class Meta:
        abstract = True

    def __str__(self):
        return self.code


# http://hl7.org/fhir/valueset-medication-status.html


# https://www.hl7.org/fhir/medication.html


# https://www.hl7.org/fhir/medication.html


# https://hl7.org/fhir/episode-of-care-status
class EpisodeStatus(CodeValueSet):
    pass

    class Meta:
        verbose_name_plural = _("Episode Statuses")


class EpisodeStatusHistory(models.Model):
    """ManyToMany "Through" model for EpisodeOfCare"""

    status = models.ForeignKey(EpisodeStatus, on_delete=models.CASCADE)
    episode = models.ForeignKey("EpisodeOfCare", on_delete=models.CASCADE)
    period = PeriodField(default=ongoing_period)
    # period = models.ForeignKey(Period, on_delete=models.PROTECT, related_name="+")

    class Meta:
        verbose_name_plural = _("Episode Status Histories")


class EpisodeOfCare(BaseModel):
    """An episode of problem(s) within a given period."""

    ##### TODO

    # code: planned | waitlist | active | onhold | finished | cancelled | entered-in-error
    status = models.ForeignKey(
        EpisodeStatus, on_delete=models.PROTECT, related_name="+"
    )
    status_history = models.ManyToManyField(EpisodeStatus, through=EpisodeStatusHistory)
