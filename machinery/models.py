from django.db import models


# Справочник грузовиков
class BrandCatalog(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')

    class Meta:
        verbose_name = 'Справочник производителей грузовиков'

    def __str__(self):
        return '%s' % self.name


# Справочник моделей
class TruckCatalog(models.Model):
    brand = models.ForeignKey(BrandCatalog, on_delete=models.CASCADE, related_name='brand', verbose_name='Марка')
    model = models.CharField(max_length=250, verbose_name='Наименование модели')
    max_weight = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='Грузоподъемность, т.')

    class Meta:
        verbose_name = 'Справочник моделей грузовиков'

    def __str__(self):
        return '%s,%s' % (self.brand.name, self.model)


# Грузовики в эксплуатации
class Truck(models.Model):
    truck_catalog = models.ForeignKey(TruckCatalog, on_delete=models.CASCADE, related_name='truck_catalog',
                              verbose_name='Марка, модель')
    board_number = models.CharField(max_length=50, verbose_name='Бортовой номер')

    class Meta:
        verbose_name = 'Грузовики в эксплуатации'

    def __str__(self):
        return '%s,%s' % (self.truck_catalog, self.board_number)
