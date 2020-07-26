from django.db import models


class StorageCatalog(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')
    coords = models.CharField(max_length=250, verbose_name='Координаты склада')

    class Meta:
        verbose_name = 'Справочник складов'

    def __str__(self):
        return '%s' % self.name


class Minerals(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')
    unit_name = models.CharField(max_length=50, verbose_name='Обозначение')

    class Meta:
        verbose_name = 'Справочник руд'

    def __str__(self):
        return '%s' % self.name

