---
name: little-wms-code-input
description: Use when adding or reviewing a field that expects a code (article `a0…`, storage `s0…`, location `l0…`, or a target code) in little_WMS — ensures the field finds the object by code OR name AND offers the QR scanner, instead of a bare text input.
---

# little_WMS Code Input (code + search + scanner)

Any input that expects a **code** — a scan field, a "store target" field, a
packlist article, a form's `code`/`stored` field — MUST be user-friendly:

1. **Find by code OR name** (live search suggestions).
2. **Offer the QR scanner.**

Do not ship a bare text input for codes. A field that only accepts a code, or
only has a scanner without search, is a defect.

## Why

The app is built around scanning and quick lookup. Users should be able to type
a name, pick from suggestions, or scan — without knowing the code.

## The standard field

```django
<input id="myCode" name="code" class="form-control" placeholder="Scan or search …"
       autocomplete="off"
       hx-get="{% url 'my search' %}" hx-target="#myResults"
       hx-trigger="input changed delay:300ms">
{% include "hub/modules/qrScanner.html" with input="myCode" scannerUrl="/my/scanner/myCode/toggle" %}
...
<div id="scannerDivmyCode"></div>       {# outside the input-group #}
<div id="myResults" class="list-group mt-1"></div>
```

The search endpoint returns a partial of clickable suggestions that post the
object's code back to the parent form (like `movement/inventory.html` +
`movement/inventoryResults.html`).

## The scanner toggle view

Copy the existing pattern (`articleScanner`, `storageScanner`, `movementScanner`,
`occasionScanner`):

```python
@login_required(login_url='/accounts/login/')
@require_perm("...")   # the permission that matches the field
def myScanner(request, scannerId, state):
    if state == "toggle":
        active = request.POST.get("active_scanner", "")
        if active == scannerId:
            context = {"activeInput": "", "input": scannerId, "state": "off"}
        else:
            context = {"activeInput": active, "input": scannerId, "state": "on", "scan": True}
        return render(request, "hub/modules/toggleScanner.html", context=context)
    return HttpResponseNotFound('<h1>Page not found</h1>')
```

URL (register it in the app's `urls.py`; include the app in
`little_wms/urls.py` if it is new):

```python
path("my/scanner/<str:scannerId>/<str:state>", views.myScanner, name="my scanner"),
```

## The search view

```python
def mySearch(request):
    query = request.GET.get("code", "").strip()
    results = Model.objects.filter(
        Q(name__contains=query) | Q(code__code__contains=query)
    )[:20] if query else Model.objects.none()
    return render(request, "my/app/results.html", {"results": results})
```

## Django forms

For a model form rendered by `itemForm.html` / `addForm.html`, the `code` and
`stored` fields already get a QR button automatically (`field.auto_id`); keep
that branch when adding new forms.

## Checklist

- [ ] The field finds the object **by code OR name** (live search + suggestions).
- [ ] The QR button is present (`qrScanner.html` include) with a matching
      `scannerDiv<id>` outside the input-group.
- [ ] A `.../scanner/<scannerId>/<state>` URL + view exist and return
      `toggleScanner.html`.
- [ ] A search URL + view exist and return a clickable-suggestions partial.
- [ ] The permission guard on both views matches the field's action.
- [ ] Tested in Docker (`sg docker`) — see `little-wms-implementation`.

## Existing usages (copy from these)

- `movement/templates/movement/inventory.html` + `inventoryResults.html` (scan + search) — the reference.
- `movement/templates/movement/where.html` (scan + search)
- `movement/templates/movement/movement.html` (scan)
- `occasion/templates/occasion/packlist.html` + `packlistResults.html` (scan + search)
- `hub/modules/storeActions.html`, `hub/modules/storageContents.html` (target/article code)
