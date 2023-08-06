from django.db import models
from django.db.models import PositiveIntegerField
from django.utils.translation import gettext_lazy as _

from . import ongoing_period
from .common import BaseModel
from .datapacks import PackageDataModel
from ..fields import PeriodField


class UpperCodeMixin:
    def save(self, *args, **kwargs):
        self.code = self.code.upper()
        super().save(*args, **kwargs)


class Language(UpperCodeMixin, PackageDataModel):
    """A Language name like "German", "English", used all over the place in MedUX."""

    # see https://en.wikipedia.org/wiki/ISO_639-1
    code = models.CharField(
        max_length=2, primary_key=True, help_text=_("ISO 639-1 language code")
    )
    name = models.CharField(
        max_length=50, help_text=_("ISO 639-1 English language name")
    )

    def __str__(self):
        return f"{self.name} ({self.code})"


class ZipCode(PackageDataModel):
    # TODO add validator
    code = models.CharField(max_length=10)

    def __str__(self):
        return self.code


class City(PackageDataModel):
    name = models.CharField(max_length=100)
    # a city can have more than one zipcode
    zipcodes = models.ManyToManyField(ZipCode)

    class Meta:
        verbose_name_plural = _("Cities")

    def __str__(self):
        return self.name


class Country(UpperCodeMixin, PackageDataModel):
    """Countries coded per ISO 3166-1

    see https://en.wikipedia.org/wiki/ISO_3166-1"""

    code = models.CharField(max_length=2, primary_key=True, help_text="ISO 3166-1 code")
    name = models.CharField(max_length=255, help_text=_("Official English short name"))
    # the flag of the country, as Unicode char
    flag = models.CharField(max_length=5, blank=True)

    default_language = models.ForeignKey(
        Language, blank=True, null=True, on_delete=models.PROTECT
    )

    class Meta:
        verbose_name_plural = _("Countries")

    def __str__(self):
        return self.name


class AddressType(models.Model):
    """Type of an address, like home, work, parents, holidays etc."""

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Address(BaseModel):
    street = models.CharField(max_length=255, blank=True)

    # additional street-level information which formatters would usually
    # put on lines directly below the street line of an address, such as
    # postal box directions in CA, or c/o hints
    aux_street = models.CharField(
        max_length=255,
        blank=True,
        help_text=_("hints like postal box directions in CA, or c/o, etc."),
    )

    number = models.CharField(
        max_length=50,
        blank=True,
        help_text=_("Street number, evtl. with additions like stair number, etc."),
    )

    # directions *below* the unit (eg.number) level, such as apartment number,
    # room number, level, entrance or even verbal directions
    subunit = models.CharField(max_length=255, blank=True)

    postcode = models.CharField(max_length=10, blank=True)

    city = models.CharField(max_length=255, blank=True)

    state = models.ForeignKey(Country, blank=True, null=True, on_delete=models.PROTECT)

    addendum = models.CharField(
        max_length=255,
        blank=True,
        help_text=_("Any additional information that did not fit anywhere else"),
    )

    location = models.CharField(
        max_length=255,
        blank=True,
        help_text=_("The exact location of this address in latitude-longtitude"),
    )

    # TODO: make sure that period gets a default value - "now -> ongoing"
    period = PeriodField(default=ongoing_period)
    # period = models.ForeignKey(
    #     Period,
    #     on_delete=models.PROTECT,
    #     help_text=_("The time period this address is valid."),
    #     blank=True,
    #     null=True,
    # )

    weight = PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.street} {self.number}, {self.postcode} {self.city}"

    class Meta:
        verbose_name_plural = _("Addresses")
        unique_together = ("street", "number", "postcode", "city", "state")
        ordering = ["weight"]


class AddressMapper(models.Model):
    address_id = models.ForeignKey(Address, on_delete=models.PROTECT)
    person_id = models.ForeignKey("Person", on_delete=models.PROTECT)
    address_type = models.ForeignKey(AddressType, on_delete=models.PROTECT)
