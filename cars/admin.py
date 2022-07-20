from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin


from . import models
from .resource import CarResourceExport, CarResourceImport


@admin.register(models.Car)
class CarAdmin(ImportExportActionModelAdmin):
    resource_class = CarResourceExport

    def get_import_resource_class(self):
        return CarResourceImport



@admin.register(models.BrandCar)
class BrandCarAdmin(admin.ModelAdmin):
    pass


@admin.register(models.ModelCar)
class ModelCarAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Colour)
class ColourAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Year)
class YearAdmin(admin.ModelAdmin):
    pass


