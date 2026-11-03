import io

import qrcode
import qrcode.image.svg
from django.contrib.auth.decorators import login_required
from organisation.decorators import require_perm
from django.http import HttpResponseNotFound
from django.shortcuts import render

from article.models import Article
from storage.models import Storage

# Create your views here.

# Label grid: columns x rows on A4
FORMATS = {
    "2x4": (2, 4),
    "3x7": (3, 7),
    "4x10": (4, 10),
}

# QR edge length in mm
SIZES = {
    "small": 20,
    "medium": 30,
    "large": 40,
}


def qr_svg(data):
    """Render ``data`` as an SVG QR code (no Pillow needed)."""
    img = qrcode.make(data, image_factory=qrcode.image.svg.SvgPathImage)
    buf = io.BytesIO()
    img.save(buf)
    return buf.getvalue().decode()


@login_required(login_url='/accounts/login/')
@require_perm("export.qr_sheet_all")
def qrPrint(request):
    """Printable QR sheet for the selected articles/storages (§5a)."""
    if request.method != "POST":
        return HttpResponseNotFound('<h1>Page not found</h1>')

    typ = request.POST.get("type", "article")

    if request.POST.get("all"):
        # "Select all matches": re-run the list filter server-side (§ list-views).
        list_typ = request.POST.get("typ", "")
        if typ == "storage":
            from storage.views import _storage_list

            objects = _storage_list(request, request.POST, list_typ)
        else:
            from article.views import _article_stocks

            ids = _article_stocks(request, request.POST).filter(
                article__base__pType__name__exact=list_typ
            ).values_list("article_id", flat=True)
            objects = Article.objects.filter(pk__in=list(ids))
    else:
        ids = [value for key, value in request.POST.items() if key.startswith("_")]
        objects = (Storage if typ == "storage" else Article).objects.filter(pk__in=ids)

    if typ == "storage":
        link_prefix = "s"
        items = [
            {"code": s.code.code, "name": s.name, "symbol": s.typ.symbol}
            for s in objects
        ]
    else:
        link_prefix = "a"
        items = [
            {"code": a.code.code, "name": a.base.name, "symbol": a.base.pType.symbol}
            for a in objects
        ]

    if request.POST.get("sort") == "code":
        items.sort(key=lambda i: i["code"])
    else:
        items.sort(key=lambda i: i["name"].lower())

    qr_content = request.POST.get("qr", "code")
    for item in items:
        if qr_content == "link":
            data = request.build_absolute_uri("/%s/%s" % (link_prefix, item["code"]))
        else:
            data = item["code"]
        item["qr"] = qr_svg(data)

    cols, rows = FORMATS.get(request.POST.get("format"), FORMATS["3x7"])
    context = {
        "items": items,
        "cols": cols,
        "rows": rows,
        "size": SIZES.get(request.POST.get("size"), SIZES["medium"]),
        "label": request.POST.get("label", "name"),
    }
    return render(request, "export/qrPrint.html", context=context)
