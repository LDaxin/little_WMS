from django.core.exceptions import ValidationError
from django.db import models


class SelfForeignKey(models.ForeignKey):
    def pre_save(self, instance, add):
        from space.services import max_storage_depth

        manager = instance.__class__.objects
        ancestor_id = getattr(instance, self.attname)
        depth = 0
        max_depth = max_storage_depth()
        while ancestor_id is not None:
            depth += 1
            if depth > max_depth:
                raise ValidationError("Maximum storage depth (%s) exceeded" % max_depth)
            if ancestor_id == instance.id:
                raise ValidationError("Cycle detected")
            ancestor = manager.get(id=ancestor_id)
            ancestor_id = getattr(ancestor, self.attname)
        return getattr(instance, self.attname)
