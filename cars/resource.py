from import_export import resources
from import_export.fields import Field
from datetime import datetime

from . import models


class CarResourceExport(resources.ModelResource):
    """
    Resource для экспорта
    """
    brand = Field()
    model_car = Field()
    colour = Field()
    year = Field()
    date_of_sts = Field()

    def get_queryset(self):
        return models.Car.objects_car.all()

    def dehydrate_brand(self, obj):
        return obj.model_car.brand.name_of_brand

    def dehydrate_colour(self, obj):
        return obj.colour.name_of_colour

    def dehydrate_year(self, obj):
        return obj.year.year_of_release

    def dehydrate_model_car(self, obj):
        return obj.model_car.name_of_model

    def dehydrate_date_of_sts(self, obj):
        return obj.date_of_sts.strftime('%d.%m.%Y')

    class Meta:
        model = models.Car
        fields = (
            'id', 'registration_number', 'brand', 'model_car', 'colour', 'year', 'vin', 'sts_number', 'date_of_sts',
        )
        export_order = fields


class CarResourceImport(resources.ModelResource):
    """
    Resource для импорта
    """

    def before_import_row(self, row, **kwargs):
        brand_car, _ = models.BrandCar.objects.get_or_create(name_of_brand=row['brand'].lower())
        model_car, _ = models.ModelCar.objects.get_or_create(name_of_model=row['model_car'].lower(), brand=brand_car)
        colour_car, _ = models.Colour.objects.get_or_create(name_of_colour=row['colour'].lower())
        year_car, _ = models.Year.objects.get_or_create(year_of_release=row['year'])
        if isinstance(row['date_of_sts'], str):
            row['date_of_sts'] = datetime.strptime(row['date_of_sts'], '%d.%m.%Y')
        row['model_car'] = model_car.id
        row['year'] = year_car.id
        row['colour'] = colour_car.id

    class Meta:
        model = models.Car
        fields = (
            'id', 'registration_number', 'model_car', 'colour', 'year', 'vin', 'sts_number', 'date_of_sts',
        )
