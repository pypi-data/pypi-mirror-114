# This file contains base models for master data used in MedUX. They can be provided using packages.

import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _

from .common import BaseModel
from ..fields import MarkdownField


class PackageDataModel(models.Model):
    """An abstract base model for everything that can be packaged.

    .. note:

        This is not inheriting :class:`BaseModel`, so no soft-delete is available here.
    """

    USER = 1  # User generated data
    LOCAL_ADMIN = 10
    VENDOR = 99
    MAINTAINER = (
        (USER, _("User")),
        (LOCAL_ADMIN, _("Admin")),
        (VENDOR, _("Vendor")),
    )
    # the uuid field is for uniquely identifying this item across practices, to simplify distribution
    uuid = models.UUIDField(default=uuid.uuid4)

    maintainer = models.SmallIntegerField(choices=MAINTAINER, default=VENDOR)

    # TODO: include a "dirty" field for indicating that the user, admin etc. has changed something
    # So it can be excluded from updating, depending on what the user wants.

    class Meta:
        abstract = True


class DataPack(BaseModel):
    """A data pack that can be downloaded from an update server.

    A data pack contains data in the form of :class:`PackageDataModel`s.
    This is basically what a ValueSet in FHIR means.

    A DataPack is intended to be downloaded from an update server as zip file.
    The metadata can be saved in this DataPack model, to keep a trace of it."""

    uuid = models.UUIDField(default=uuid.uuid4)
    name = models.CharField(
        max_length=100, help_text=_("Name for this data pack (computer friendly)")
    )
    title = models.CharField(
        max_length=255, help_text=_("Name for this data pack (human friendly)")
    )
    description = MarkdownField(
        max_length=255, help_text=_("Natural description, in MarkDown")
    )
    license = models.CharField(max_length=20)
    version = models.CharField(max_length=25)
    experimental = models.BooleanField(default=False)
    publisher = models.CharField(max_length=255, blank=True)
    language = models.ForeignKey("Language", on_delete=models.PROTECT)
    # TODO medux compatibility version

    #: the model in which the field should be saved
    model = models.CharField(max_length=255)
    downloaded = models.BooleanField(default=False)
    installed = models.BooleanField(default=False)
    data_file = models.FileField(upload_to="datapacks")
