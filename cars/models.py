from django.db import models


class LowerCharField(models.CharField):
    """
    Кастомное поле для приведение строки в нижний регистр
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_prep_value(self, value):
        return str(value).lower()


class CarManager(models.Manager):
    """
    Менеджер ТС
    """

    def get_queryset(self):
        return super().get_queryset().select_related('model_car__brand', 'colour', 'year', ).all()


class BrandCar(models.Model):
    """
    Марка машины
    """
    name_of_brand = LowerCharField(max_length=50, unique=True, verbose_name='Марка машины',
                                   help_text="формат: уникальное, max-50")

    def __str__(self):
        return self.name_of_brand


class ModelCar(models.Model):
    """
    Модель машины
    """
    name_of_model = LowerCharField(max_length=50, unique=True, verbose_name='Модель машины',
                                   help_text="формат: уникальное, max-50")
    brand = models.ForeignKey(BrandCar, related_name='related_model_car', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.brand.name_of_brand} - {self.name_of_model}'


class Colour(models.Model):
    """
    Цвет
    """
    name_of_colour = LowerCharField(max_length=50, unique=True, verbose_name='Цвет',
                                    help_text="формат: уникальное, max-50")

    def __str__(self):
        return self.name_of_colour


class Year(models.Model):
    """
    Год выпуска
    """
    year_of_release = models.PositiveSmallIntegerField(verbose_name='Год выпуска', unique=True,
                                                       help_text="формат: уникальное")

    def __str__(self):
        return f'{self.year_of_release}'


class Car(models.Model):
    """
    Транспортное средство
    """
    registration_number = models.CharField(max_length=100, unique=True, verbose_name='Регистрационный номер',
                                           help_text="формат: уникальное, max-100")
    model_car = models.ForeignKey(ModelCar, related_name='related_car_model', on_delete=models.SET_NULL, null=True)
    colour = models.ForeignKey(Colour, related_name='related_car_colour', on_delete=models.SET_NULL, null=True)
    year = models.ForeignKey(Year, related_name='related_car_year', on_delete=models.SET_NULL, null=True)
    vin = models.CharField(max_length=100, unique=True, verbose_name='VIN', help_text="формат: уникальное, max-100")
    sts_number = models.CharField(max_length=100, unique=True, verbose_name='Номер СТС', help_text="формат: уникальное, max-100")
    date_of_sts = models.DateField(verbose_name='Дата СТС')
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата создания')

    objects = models.Manager()
    objects_car = CarManager()

    def __str__(self):
        return f'{self.model_car.name_of_model}-{self.registration_number}'
