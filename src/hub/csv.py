"""CSV download responses."""
import csv

from django.http import HttpResponse


def csv_response(filename, header, rows, encoding="utf-8"):
    """A CSV download response with ``header`` and ``rows``."""
    response = HttpResponse(content_type="text/csv; charset=%s" % encoding)
    response["Content-Disposition"] = 'attachment; filename="%s"' % filename
    writer = csv.writer(response, dialect="excel")
    writer.writerow(header)
    writer.writerows(rows)
    return response
