from django.db import models
import uuid

# TODO: Add `active`, `owner`, and `is_deleted` fields
class BaseModel(models.Model):
  uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
  created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
  updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

  class Meta:
    abstract = True
