"""Per-organisation export/import (§17 level 2).

Exports one organisation's inventory as JSON and imports it into a new
organisation, assigning new primary keys and remapping foreign keys. Codes and
primary keys are regenerated on import.
"""
from django.apps import apps
from django.utils.text import slugify

# Topological order: dependencies first.
EXPORT_ORDER = [
    "article.ArticleType",
    "storage.StorageType",
    "location.Location",
    "tag.TagCategory",
    "tag.Tag",
    "space.Space",
    "storage.Storage",
    "article.ArticleBase",
    "article.Article",
    "article.Stock",
    "article.CompositionItem",
]

# Regenerated on import (new codes / primary keys / organisation).
SKIP_FIELDS = {"id", "pk", "code", "organisation"}


def _has_org(model):
    return any(f.name == "organisation" for f in model._meta.get_fields())


def _queryset(model, organisation):
    if _has_org(model):
        return model.objects.filter(organisation=organisation)
    label = model._meta.label_lower
    if label == "article.stock":
        return model.objects.filter(article__organisation=organisation)
    if label == "article.compositionitem":
        return model.objects.filter(space__organisation=organisation)
    return model.objects.none()


def export_organisation(organisation):
    """Return a JSON-serialisable dict of the organisation's inventory."""
    data = {
        "version": 1,
        "organisation": {"name": organisation.name, "slug": organisation.slug},
        "objects": [],
    }
    for label in EXPORT_ORDER:
        model = apps.get_model(label)
        for obj in _queryset(model, organisation):
            data["objects"].append(_serialize(obj))
    return data


def _serialize(obj):
    fields = {}
    for field in obj._meta.get_fields():
        if not field.concrete or field.name in SKIP_FIELDS:
            continue
        if field.is_relation:
            value = getattr(obj, field.name)
            if value is not None:
                fields[field.name] = {"__ref__": [value._meta.label_lower, value.pk]}
        else:
            fields[field.name] = getattr(obj, field.name)

    m2m = {}
    for field in obj._meta.many_to_many:
        if field.related_model._meta.label_lower == "auth.user":
            continue  # users are not exported
        m2m[field.name] = [
            {"__ref__": [v._meta.label_lower, v.pk]} for v in getattr(obj, field.name).all()
        ]
    return {"model": obj._meta.label_lower, "pk": obj.pk, "fields": fields, "m2m": m2m}


def import_organisation(data, name=None):
    """Create a new organisation from an export. Returns the organisation."""
    from organisation.models import Organisation

    name = name or data["organisation"]["name"]
    organisation = Organisation.objects.create(name=name, slug=_unique_slug(name))

    pk_map = {}
    deferred = []  # (obj, field_name, ref_label, ref_pk) for unresolved refs
    for entry in data["objects"]:
        model = apps.get_model(entry["model"])
        kwargs = {}
        local_deferred = []
        for field_name, value in entry["fields"].items():
            if field_name in SKIP_FIELDS:
                continue
            if isinstance(value, dict) and "__ref__" in value:
                ref_label, ref_pk = value["__ref__"]
                target = pk_map.get((ref_label, ref_pk))
                if target is None:
                    local_deferred.append((field_name, ref_label, ref_pk))
                    continue
                kwargs[field_name] = target
            else:
                kwargs[field_name] = value

        obj = model(**kwargs)
        if _has_org(model):
            obj.organisation = organisation
        obj.save()
        pk_map[(entry["model"], entry["pk"])] = obj

        for field_name, refs in entry.get("m2m", {}).items():
            related = [pk_map.get((r["__ref__"][0], r["__ref__"][1])) for r in refs]
            related = [r for r in related if r is not None]
            if related:
                getattr(obj, field_name).set(related)

        for field_name, ref_label, ref_pk in local_deferred:
            deferred.append((obj, field_name, ref_label, ref_pk))

    # Second pass: resolve references that were not available yet (self-refs).
    for obj, field_name, ref_label, ref_pk in deferred:
        target = pk_map.get((ref_label, ref_pk))
        if target is not None:
            setattr(obj, field_name, target)
            obj.save()

    return organisation


def _unique_slug(name):
    from organisation.models import Organisation

    base = slugify(name) or "org"
    slug = base
    n = 1
    while Organisation.objects.filter(slug=slug).exists():
        n += 1
        slug = "%s-%s" % (base, n)
    return slug
