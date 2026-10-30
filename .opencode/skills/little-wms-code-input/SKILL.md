---
name: little-wms-code-input
description: Use when adding or reviewing a field that expects a code (article `a0…`, storage `s0…`, location `l0…`, or a target code) in little_WMS — ensures the reusable QR-scan (and code/name search) pattern is used instead of a bare text input.
---

# little_WMS Code Input (QR scan + search)

Any input that expects a **code** — a scan field, a "store target" field, a
packlist article, a form's `code`/`stored` field — MUST offer the QR scanner
(and, where useful, code/name search). Do not ship a bare text input for codes.

## Why

The app is built around scanning. A code field without a scanner forces manual
typing and is a recurring defect.

## The reusable template

`hub/modules/qrScanner.html` renders the QR button. Include it **inside** the
input-group and give it two variables:

```django
<input id="myCode" name="code" class="form-control" placeholder="Scan or enter code">
{% include "hub/modules/qrScanner.html" with input="myCode" scannerUrl="/my/scanner/myCode/toggle" %}
```

Two more rules:

1. Every scanner needs its **toggle URL** (a view that returns
   `hub/modules/toggleScanner.html`).
2. Add the container **outside** the input-group, using the same `input` id:

```django
<div id="scannerDivmyCode"></div>
```

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

## Code + name search (preferred)

For a field that should also accept a name, add live suggestions, like
`movement/inventory.html`:

```django
<input id="myCode" name="code" class="form-control"
       hx-get="{% url 'my search' %}" hx-target="#myResults"
       hx-trigger="input changed delay:300ms">
...
<div id="myResults" class="list-group mt-1"></div>
```

The search view returns a partial of clickable suggestions that post the scanned
code back to the parent form.

## Django forms

For a model form rendered by `itemForm.html` / `addForm.html`, the `code` and
`stored` fields already get a QR button automatically (`field.auto_id`); keep
that branch when adding new forms.

## Checklist

- [ ] The code field has the QR button (`qrScanner.html` include).
- [ ] The matching `scannerDiv<id>` container exists outside the input-group.
- [ ] A `.../scanner/<scannerId>/<state>` URL + view exist and return
      `toggleScanner.html`.
- [ ] Where names are useful, a live search endpoint is wired.
- [ ] The permission guard on the scanner view matches the field's action.
- [ ] Tested in Docker (`sg docker`) — see `little-wms-implementation`.

## Existing usages (copy from these)

- `movement/templates/movement/movement.html` (scan)
- `movement/templates/movement/inventory.html` (scan + search)
- `movement/templates/movement/where.html` (scan + search)
- `hub/modules/storeActions.html`, `hub/modules/storageContents.html` (target/article code)
- `occasion/templates/occasion/packlist.html` (packlist article)
