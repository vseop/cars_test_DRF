from django.http import HttpResponse
from import_export.formats.base_formats import CSV, HTML, JSON, ODS, TSV, XLS, XLSX, YAML
from import_export.resources import ModelResource
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from tablib import Dataset
from rest_framework import exceptions
from datetime import date


class ExportError(exceptions.APIException):
    status_code = 400
    default_detail = "Export error"
    default_code = "export_error"


class ImportError(exceptions.APIException):
    status_code = 500
    default_detail = "Import error"
    default_code = "import_error"


EXPORT_FORMATS_DICT = {
    "csv": CSV.CONTENT_TYPE,
    "xls": XLS.CONTENT_TYPE,
    "xlsx": XLSX.CONTENT_TYPE,
    "tsv": TSV.CONTENT_TYPE,
    "ods": ODS.CONTENT_TYPE,
    "yaml": YAML.CONTENT_TYPE,
    "json": JSON.CONTENT_TYPE,
    "html": HTML.CONTENT_TYPE,
}
IMPORT_FORMATS_DICT = EXPORT_FORMATS_DICT


class ExportMixin:
    """Export Mixin"""

    export_filename: str = "Default"
    export_resource: ModelResource = None

    @action(detail=False, methods=["get"])
    def export(self, request, *args, **kwargs):
        filename = self.export_filename
        eformat = request.query_params.get("eformat", "csv")
        print(eformat)

        queryset = self.filter_queryset(self.get_queryset())
        print(queryset)

        dataset = self.get_resource().export(queryset)
        print(dataset)
        if not hasattr(dataset, eformat):
            raise ExportError(
                detail="Unsupport export format", code="unsupport_export_format"
            )

        data, content_type = (
            getattr(dataset, eformat),
            EXPORT_FORMATS_DICT[eformat],
        )

        response = HttpResponse(data, content_type=content_type)
        response["Content-Disposition"] = f"attachment; filename={filename}{date.today()}.{eformat}"
        return response

    def get_resource(self):
        if not self.export_resource:
            raise ExportError(detail="Set export resource")
        return self.export_resource()


class ImportMixin:
    """Import Mixin"""

    import_resource: ModelResource = None

    @action(methods=["post"], detail=False)
    def import_data(self, request, *args, **kwargs):
        file = request.FILES["file"]
        extension = file.name.split(".")[-1].lower()
        import_resource = self.get_import_resource()
        dataset = Dataset()

        if extension in IMPORT_FORMATS_DICT:
            dataset.load(file.read(), format=extension)
        else:
            raise ImportError("Unsupport import format", code="unsupport_import_format")
        result = import_resource.import_data(
            dataset,
            dray_run=False,
            collect_failed_rows=True,
            raise_errors=True,
        )

        return Response(
            data={"message": "Import successed"}, status=status.HTTP_201_CREATED
        )

    def get_import_resource(self):
        if not self.import_resource:
            raise ImportError(detail="Set import resource")
        return self.import_resource()
