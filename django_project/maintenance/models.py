from django.db import models
import uuid

# Create your models here.

class Checklist(models.Model):
    list = models.UUIDField()


class Plan(models.Model):
    maintenanceCycle = models.DurationField()

    checklist = models.UUIDField(default=uuid.uuid4,editable=False)


class Log(models.Model):
    date = models.DateTimeField(auto_now=True)

    checklist = models.ForeignKey()

