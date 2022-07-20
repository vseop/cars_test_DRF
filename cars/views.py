from rest_framework import viewsets, permissions
from rest_framework import filters

from .mixins import ExportMixin, ImportMixin
from .models import Car
from .resource import CarResourceExport, CarResourceImport
from .serializers import CarSerializer


class CarViewSet(ExportMixin, ImportMixin, viewsets.ModelViewSet):
    """
    Вывод списка, создание, добавление, import и export ТС
    """
    serializer_class = CarSerializer
    queryset = Car.objects_car.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = (
        'year__year_of_release', 'registration_number', 'colour__name_of_colour', 'model_car__name_of_model',
        'model_car__brand__name_of_brand', 'vin', 'sts_number',
    )

    export_filename = "car_info"
    export_resource = CarResourceExport

    import_resource = CarResourceImport

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            permission_classes = (permissions.IsAuthenticated,)
        else:
            permission_classes = (permissions.IsAdminUser,)
        return [permission() for permission in permission_classes]
