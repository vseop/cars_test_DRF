from rest_framework import serializers
from .models import BrandCar, ModelCar, Colour, Year, Car


class CarSerializer(serializers.ModelSerializer):
    """Вывод машины"""
    brand = serializers.CharField(source='model_car.brand.name_of_brand', max_length=50)
    model_car = serializers.CharField(source='model_car.name_of_model', max_length=50)
    colour = serializers.CharField(source='colour.name_of_colour', max_length=50)
    year = serializers.CharField(source='year.year_of_release', max_length=4)

    class Meta:
        model = Car
        fields = '__all__'
        read_only_fields = ('created_at',)

    def create(self, validated_data):
        brand_model_car = validated_data.pop('model_car')
        name_of_brand = brand_model_car['brand']['name_of_brand'].lower()
        name_of_model = brand_model_car.get('name_of_model').lower()
        name_of_colour = validated_data.pop('colour').get('name_of_colour').lower()
        year_of_release = validated_data.pop('year').get('year_of_release')
        colour_car, _ = Colour.objects.get_or_create(name_of_colour=name_of_colour)
        year_car, _ = Year.objects.get_or_create(year_of_release=year_of_release)
        brand_car, _ = BrandCar.objects.get_or_create(name_of_brand=name_of_brand)
        model_car, _ = ModelCar.objects.get_or_create(name_of_model=name_of_model, brand=brand_car)
        car = Car.objects.create(model_car=model_car, colour=colour_car, year=year_car, **validated_data)
        return car

    def update(self, instance, validated_data):
        name_of_colour = validated_data.get('colour').get('name_of_colour').lower()
        year_of_release = validated_data.pop('year').get('year_of_release')
        brand_model_car = validated_data.pop('model_car')
        name_of_brand = brand_model_car['brand']['name_of_brand'].lower()
        name_of_model = brand_model_car.get('name_of_model').lower()
        brand_car, _ = BrandCar.objects.get_or_create(name_of_brand=name_of_brand)

        instance.model_car, _ = ModelCar.objects.get_or_create(name_of_model=name_of_model, brand=brand_car)
        instance.year, _ = Year.objects.get_or_create(year_of_release=year_of_release)
        instance.colour, _ = Colour.objects.get_or_create(name_of_colour=name_of_colour)
        instance.registration_number = validated_data.get('registration_number', instance.registration_number)
        instance.vin = validated_data.get('vin', instance.vin)
        instance.sts_number = validated_data.get('sts_number', instance.sts_number)
        instance.date_of_sts = validated_data.get('date_of_sts', instance.date_of_sts)
        instance.save()
        return instance
