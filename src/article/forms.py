from django import forms
from .models import *
from codeSystem.models import *
from space.models import *


def custom_form_field(definition):
    """Build a Django form field from a custom_fields_schema definition (§4a-c)."""
    ftype = definition.get("type", "text")
    kwargs = {
        "label": definition.get("label", definition["name"]),
        "required": definition.get("required", False),
    }
    if ftype == "choice":
        kwargs["choices"] = [(o, o) for o in definition.get("options", [])]
        return forms.ChoiceField(**kwargs)
    if ftype == "integer":
        kwargs["min_value"] = definition.get("min")
        kwargs["max_value"] = definition.get("max")
        return forms.IntegerField(**kwargs)
    if ftype in ("decimal", "number", "float"):
        kwargs["min_value"] = definition.get("min")
        kwargs["max_value"] = definition.get("max")
        return forms.FloatField(**kwargs)
    if ftype == "boolean":
        kwargs["required"] = False
        return forms.BooleanField(**kwargs)
    return forms.CharField(**kwargs)


class CustomFieldsMixin:
    """Applies ArticleType.field_config and custom_fields_schema to a form (§4a-c).

    ``level`` selects which custom fields are rendered: "base" for the
    ArticleBase form, "article" for the Article form (§25).
    """

    level = "article"

    def __init__(self, *args, article_type=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.article_type = article_type
        self.custom_field_names = []
        if article_type is None:
            return

        # merge/split: without it an article is always a single item (§4d)
        if not article_type.allow_merge_split:
            self.fields.pop("menge", None)

        # field_config: hide/require global fields for this article type
        for name, config in (article_type.field_config or {}).items():
            if name not in self.fields:
                continue
            if config.get("visible") is False:
                del self.fields[name]
            elif config.get("required"):
                self.fields[name].required = True

        # custom fields for this level, prefilled from the instance's attributes
        values = getattr(self.instance, "attributes", None) or {}
        for definition in article_type.fields_for_level(self.level):
            if definition.get("visible") is False:
                continue
            name = definition["name"]
            self.fields[name] = custom_form_field(definition)
            self.custom_field_names.append(name)
            if name in values:
                self.initial[name] = values[name]

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.custom_field_names:
            attributes = dict(instance.attributes or {})
            for name in self.custom_field_names:
                value = self.cleaned_data.get(name)
                if value in (None, ""):
                    attributes.pop(name, None)
                else:
                    attributes[name] = value
            instance.attributes = attributes
        if commit:
            instance.save()
        return instance


class FormArticle(CustomFieldsMixin, forms.ModelForm):
    level = "article"
    stored = forms.CharField(max_length=34, required=False)
    menge = forms.DecimalField(required=False, min_value=0, max_digits=10, decimal_places=2)
    code = forms.CharField(max_length=34, required=False)

    class Meta:
        model = Article
        exclude = ('organisation', 'pType', 'space', 'code', 'base', 'attributes', 'tags', 'ownership', 'loan_requires_confirmation', 'version')

    def __init__(self, *args, **kwargs):
        super(FormArticle, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"]= "form-control"
        self.fields['code'].queryset = UuidCode.objects.filter(prefix="a0", used=False)


class FormChangeArticle(CustomFieldsMixin, forms.ModelForm):
    level = "article"
    menge = forms.DecimalField(required=False, min_value=0, max_digits=10, decimal_places=2)

    class Meta:
        model = Article
        exclude = ('organisation', 'pType', 'space', 'code', 'base', 'attributes', 'tags', 'ownership', 'loan_requires_confirmation', 'version')

    def __init__(self, *args, **kwargs):
        super(FormChangeArticle, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"]= "form-control"
        #self.fields['Space'].widget.attrs['id'] = 'id_space_change'

class FormArticleBase(CustomFieldsMixin, forms.ModelForm):
    level = "base"

    class Meta:
        model = ArticleBase
        exclude = ('organisation', 'pType', 'code', 'attributes', 'version')

    def __init__(self, *args, **kwargs):
        super(FormArticleBase, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"]= "form-control"


class ArticleTypeForm(forms.ModelForm):
    """Admin form for ArticleType; disables the mutually exclusive flags (§4d)."""

    class Meta:
        model = ArticleType
        fields = "__all__"

    class Media:
        js = ("article/articletype.js",)
