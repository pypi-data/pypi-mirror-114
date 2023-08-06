from django.db import models
from django.utils import timezone


class SoftDeletionQuerySet(models.QuerySet):
    def delete(self):
        return super().update(deleted_at=timezone.now())

    def hard_delete(self):
        return super().delete()

    def alive(self):
        return self.filter(deleted_at=None)

    def dead(self):
        return self.exclude(deleted_at=None)


class SoftDeletionManager(models.Manager):
    """Custom Django Manager for soft-delete querys.

    This object manager transparently only fetches objects from the
    database that are not soft-deleted."""

    # https://medium.com/@adriennedomingus/soft-deletion-in-django-e4882581c340
    def __init__(self, *args, **kwargs):
        self.alive_only = kwargs.pop("alive_only", True)
        super().__init__(*args, **kwargs)

    def get_queryset(self):
        if self.alive_only:
            return SoftDeletionQuerySet(self.model).filter(deleted_at=None)
        return SoftDeletionQuerySet(self.model)

    def hard_delete(self):
        return self.get_queryset().hard_delete()


class CreatedModifiedMixin:
    """A simple mixin for model classes that need to have created/modified fields."""

    created = models.DateTimeField(editable=False, auto_now_add=True)
    modified = models.DateTimeField(editable=False, auto_now=True)


class BaseModel(CreatedModifiedMixin, models.Model):
    """An abstract base class with common used functions.

    Every relevant model in Medux should inherit BaseModel.

    It provides:
    * basic created/modified timestamps for auditing
    * a soft delete functionality: Deleted items are just marked as deleted.
    """

    deleted_at = models.DateTimeField(
        editable=False, blank=True, null=True, default=None
    )

    row_version = models.PositiveIntegerField(editable=False, default=0)

    # The standard manager only returns not-soft-deleted objects
    objects = SoftDeletionManager()

    # The all_objects Manager returns ALL objects, even soft-deleted ones
    all_objects = SoftDeletionManager(alive_only=False)

    class Meta:
        # this is necessary, as we don't want inheriting (=DB relations) here
        abstract = True

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = timezone.now()
        self.save()

    def hard_delete(self):
        super().delete()
