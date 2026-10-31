from django.core.exceptions import ValidationError
from django.db import models
from softdelete.models import SoftDeleteObject
from codeSystem.models import UuidCode
from hub.fields import SelfForeignKey
from tag.models import Tag
from space.models import Space
from organisation.current import current_organisation_id
from organisation.managers import SoftDeleteOrganisationManager

# Create your models here.

ZUSTAND_CHOICES = [
    ("gut", "gut"),
    ("gebraucht", "gebraucht"),
    ("defekt", "defekt"),
    ("reparatur", "in Reparatur"),
]

SIZE_CLASS_CHOICES = [
    ("S", "S"),
    ("M", "M"),
    ("L", "L"),
    ("XL", "XL"),
]

"""
The Article model holds all articles and information about the Articles.

In der class Article is the unice Data is space 
"""

#---------------------------------------------------------------------------
# The Article model is were the unice value is space

class ArticleType(SoftDeleteObject, models.Model):

    objects = SoftDeleteOrganisationManager()

    organisation = models.ForeignKey("organisation.Organisation", on_delete=models.CASCADE, default=current_organisation_id)
    name = models.CharField(max_length=20)
    symbol = models.CharField(max_length=20)

    article_toggle_space = models.BooleanField(default=False)
    allow_merge_split = models.BooleanField(default=False)

    # Visibility/required of the global fields (§4a-c), e.g.
    # {"zustand": {"visible": true, "required": false}}
    field_config = models.JSONField(default=dict, blank=True)
    # Type-specific field definitions (§4a-c, §25), e.g.
    # {"fields": [{"name": "personenzahl", "type": "integer", "label": "Personenzahl",
    #              "required": true, "visible": true, "min": 1, "max": 20, "level": "base"}]}
    custom_fields_schema = models.JSONField(default=dict, blank=True)

    code = models.OneToOneField(UuidCode, on_delete = models.CASCADE, editable = False, blank = True, null = True)

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        if not self.code:
            uCode = UuidCode()
            uCode.prefix = "at" 
            self.code = uCode
            uCode.save()
        super().save(*args, **kwargs)

    def clean(self):
        # a container holds other articles; a merge/split article is a quantity
        # of one thing — the two are mutually exclusive (§4d)
        if self.article_toggle_space and self.allow_merge_split:
            raise ValidationError(
                "An article type cannot be a container and merge/split at the same time."
            )

    def fields_for_level(self, level):
        """Return the custom field definitions for a level ("base" or "article")."""
        return [
            field
            for field in self.custom_fields_schema.get("fields", [])
            if field.get("level", "base") == level
        ]

    def validate_attributes(self, attributes):
        """Validate custom field values against custom_fields_schema (§4a-c).

        Raises ValidationError with {field_name: [messages]} on failure.
        """
        attributes = attributes or {}
        errors = {}
        for field in self.custom_fields_schema.get("fields", []):
            name = field.get("name")
            value = attributes.get(name)
            if value in (None, ""):
                if field.get("required"):
                    errors.setdefault(name, []).append("This field is required.")
                continue
            message = self._validate_value(field, value)
            if message:
                errors.setdefault(name, []).append(message)
        if errors:
            raise ValidationError(errors)

    @staticmethod
    def _validate_value(field, value):
        ftype = field.get("type", "text")
        if ftype == "integer":
            if isinstance(value, bool) or not isinstance(value, int):
                return "Must be an integer."
        elif ftype in ("decimal", "number", "float"):
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                return "Must be a number."
        elif ftype == "boolean":
            if not isinstance(value, bool):
                return "Must be a boolean."
        elif ftype == "choice":
            if value not in field.get("options", []):
                return "Not a valid choice."
        elif ftype == "text":
            if not isinstance(value, str):
                return "Must be text."
        if ftype in ("integer", "decimal", "number", "float"):
            if "min" in field and value < field["min"]:
                return "Must be at least %s." % field["min"]
            if "max" in field and value > field["max"]:
                return "Must be at most %s." % field["max"]
        return None

    def __str__(self, *args, **kwargs):
        return self.name

class ArticleBase(SoftDeleteObject, models.Model):

    objects = SoftDeleteOrganisationManager()

    organisation = models.ForeignKey("organisation.Organisation", on_delete=models.CASCADE, default=current_organisation_id)
    name = models.CharField(max_length=20)

    pType = models.ForeignKey(ArticleType, on_delete=models.CASCADE, blank=True , null = False)

    # Catalog properties (shared by all instances of this model)
    outer_length_mm = models.IntegerField(null=True, blank=True)
    outer_width_mm = models.IntegerField(null=True, blank=True)
    outer_height_mm = models.IntegerField(null=True, blank=True)
    size_class = models.CharField(max_length=2, choices=SIZE_CLASS_CHOICES, null=True, blank=True)
    attributes = models.JSONField(default=dict, blank=True)

    # Global minimum for this kind of thing, independent of location (§4d).
    mindestbestand = models.IntegerField(null=True, blank=True)

    code = models.OneToOneField(UuidCode, on_delete = models.CASCADE, editable = False, blank = True, null = True)

    def save(self, *args, **kwargs):
        if not self.code:
            uCode = UuidCode()
            uCode.prefix = "ab" 
            self.code = uCode
            uCode.save()
        super().save(*args, **kwargs)

    def __str__(self, *args, **kwargs):
        return self.name

class Article(SoftDeleteObject, models.Model):

    objects = SoftDeleteOrganisationManager()

    organisation = models.ForeignKey("organisation.Organisation", on_delete=models.CASCADE, default=current_organisation_id)
    base = models.ForeignKey(ArticleBase, on_delete=models.CASCADE, blank=True, null=False)
    #the storage space where other articles can be stored in the Article
    space = models.OneToOneField(Space, on_delete = models.CASCADE, related_name = "itemArticle", null=True, blank=True)
    #the unique code for the article
    code = models.OneToOneField(UuidCode, on_delete = models.CASCADE, blank = True, null = True)

    # Global fields (every article has them)
    zustand = models.CharField(max_length=20, choices=ZUSTAND_CHOICES, default="gut")
    anschaffungswert = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    kaufdatum = models.DateField(null=True, blank=True)
    ablaufdatum = models.DateField(null=True, blank=True)
    gewicht_gramm = models.IntegerField(null=True, blank=True)
    notiz = models.TextField(blank=True)
    ist_verbrauchsartikel = models.BooleanField(default=False)
    mengeneinheit = models.CharField(max_length=20, blank=True)

    # Ownership (§20): owned by the organisation or borrowed from an external lender.
    OWNERSHIP_CHOICES = [
        ("owned", "Owned by organisation"),
        ("borrowed", "Borrowed from external"),
    ]
    ownership = models.CharField(max_length=10, choices=OWNERSHIP_CHOICES, default="owned")
    loan_requires_confirmation = models.BooleanField(default=True)

    # Custom field values for article-level fields (§25)
    attributes = models.JSONField(default=dict, blank=True)

    tags = models.ManyToManyField(Tag, blank=True, related_name="articles")

    # Users this article is assigned to (§3 assigned scope)
    assigned_to = models.ManyToManyField("auth.User", blank=True, related_name="assigned_articles")

    # here the code gets the prefix for the article
    def save(self, *args, **kwargs):
        if not self.code:
            uCode = UuidCode()
            uCode.prefix = "a0" 
            self.code = uCode
            uCode.save()
        super().save(*args, **kwargs)


    def __str__(self, *args, **kwargs):
        return self.base.name + " " + self.code.code


class Stock(models.Model):
    """A quantity of an ``Article`` at a location (docs/design/stock.md).

    An ``Article`` is the identity; a ``Stock`` is how much of it sits where.
    ``stored`` is ``None`` for the "not stored" pile. One line per location.
    """

    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="stocks")
    stored = models.ForeignKey(Space, on_delete=models.SET_NULL, null=True, blank=True, related_name="stocks")
    menge = models.DecimalField(max_digits=10, decimal_places=2, default=1)

    class Meta:
        unique_together = ("article", "stored")

    def __str__(self):
        return "%s @ %s x%s" % (self.article, self.stored or "—", self.menge)


class CompositionItem(models.Model):
    """What a storage location should contain (§4d, docs/design/composition.md).

    ``soll_menge`` blank means "any amount" (no check); ``mindestmenge`` blank
    means "no minimum" (never a refill hint).
    """

    space = models.ForeignKey(Space, on_delete=models.CASCADE, related_name="composition")
    base = models.ForeignKey(ArticleBase, on_delete=models.CASCADE, related_name="composition_items")
    soll_menge = models.IntegerField(null=True, blank=True)
    mindestmenge = models.IntegerField(null=True, blank=True)

    class Meta:
        unique_together = ("space", "base")

    def __str__(self):
        return "%s in %s" % (self.base.name, self.space)
