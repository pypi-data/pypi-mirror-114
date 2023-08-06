from django.db import models
from django.utils.translation import gettext as _

from medux.core.fields import CodeField
from .organizations import HealthServiceProvider
from .fhir import CodeValueSet, BaseModel, EpisodeOfCare
from .datapacks import PackageDataModel


class MedicationStatus(CodeValueSet):
    pass
    # comment = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name_plural = _("Medication Statuses")


class MedicationRoute(PackageDataModel):
    pass


class Dosage(models.Model):
    # sequence
    text = models.CharField(
        max_length=255, help_text=_("Free text dosage instructions e.g. '1x/day'")
    )
    additionalInstruction = models.CharField(
        max_length=255,
        help_text=_(
            "Supplemental instruction or warnings to the patient - e.g. 'with meals', 'may cause drowsiness'"
        ),
    )
    patientInstructions = models.CharField(
        max_length=255,
        help_text=_("Instructions in terms that are understood by the patient"),
    )
    route = models.ForeignKey(MedicationRoute, on_delete=models.PROTECT)
    # maxDosePerPeriod

    def __str__(self):
        return self.text


class MedicationForm(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Ingredient(models.Model):  # PackageDataModel
    pass


class MedicationTerminologySystem(PackageDataModel):
    """A Medication terminology system like SNOMED, Austrian PZN (Pharmazentralnummer), etc."""

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Medication(PackageDataModel):
    """Definition of a medication for the purposes of prescribing, dispensing, and administering."""

    code_system = models.ForeignKey(
        MedicationTerminologySystem,
        help_text=_("The defining coding system"),
        on_delete=models.PROTECT,
    )
    code = CodeField(
        terminology_binding="MedicationTerminologySystem",
        help_text=_("The medication code within this coding system"),
    )

    # active, inactive, entered-in-error
    status = models.ForeignKey(
        MedicationStatus, default=0, on_delete=models.PROTECT
    )  # default: "active"

    manufacturer = models.ForeignKey(
        HealthServiceProvider,
        on_delete=models.PROTECT,
        help_text=_("Manufacturer of the medication product. Not the distributor."),
    )

    # e.g. powder | tablets | capsule
    form = models.ForeignKey(MedicationForm, on_delete=models.PROTECT)

    # Amount
    # TODO: amount nominator/denominator for ratios?
    # see https://www.hl7.org/fhir/medication.html, https://www.hl7.org/fhir/datatypes.html#Ratio and
    # https://www.hl7.org/fhir/datatypes.html#Quantity
    amount_value = models.DecimalField(
        decimal_places=3, max_digits=10, help_text=_("Amount of drug in package")
    )
    amount_unit = models.CharField(max_length=25, help_text=_("Unit representation"))
    # TODO: use FK instead of code?
    amount_unit_code = CodeField()

    ingredients = models.ManyToManyField(Ingredient)

    # Batch / Package information (optional)
    batch_lot_number = models.CharField(
        max_length=255, blank=True, help_text=_("Identifier assigned to batch")
    )
    batch_expiration_date = models.DateField(
        blank=True, help_text=_("When batch will expire")
    )


class MedicationStatement(BaseModel):
    """Basically a line in a list of prescribed medications."""

    # active | completed | entered-in-error | intended | stopped | on-hold | unknown | not-taken
    status = models.ForeignKey(MedicationStatus, on_delete=models.PROTECT)
    patient = models.ForeignKey("Patient", on_delete=models.PROTECT)
    medication = models.ManyToManyField(Medication)
    encounter = models.ForeignKey(
        "Encounter",
        help_text=_("Encounter associated with MedicationStatement"),
        on_delete=models.PROTECT,
    )
    episode = models.ForeignKey(
        EpisodeOfCare,
        help_text=_("EpisodeOfCare associated with MedicationStatement"),
        on_delete=models.PROTECT,
    )
    note = models.TextField()
