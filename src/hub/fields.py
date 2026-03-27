from django.db import models

class SelfForeignKey(models.ForeignKey):
    def pre_save(self, instance, add):
        manager = instance.__class__.objects
        ancestor_id = getattr(instance, self.attname)
        while ancestor_id is not None:
            if ancestor_id == instance.id:
                return None
            ancestor = manager.get(id=ancestor_id)
            ancestor_id = getattr(ancestor, self.attname)
        return getattr(instance, self.attname)
