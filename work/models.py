from django.db import models
from machinery import models as m
from storage import models as s
from django.utils import timezone


# Модель загрузки грузовика
class Loading(models.Model):
    truck = models.ForeignKey(m.Truck, on_delete=models.DO_NOTHING,
                              related_name='loading_truck', verbose_name='Загружаемый грузовик')
    weight = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='Текущий вес, т.')
    over_weight = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Перегруз, %', blank=True, default=0)

    def __str__(self):
        return '%s,%s' % (self.truck, self.weight)

    def save(self, *args, **kwargs):
        truck_max_weight = self.truck.truck_catalog.max_weight
        if truck_max_weight < self.weight:
            # self.over_weight = (1-(truck_max_weight/self.weight))*100
            self.over_weight = ((self.weight - truck_max_weight) / truck_max_weight) * 100
        super().save(*args, **kwargs)


# Модель руды в грузовике
class LoadingMinerals(models.Model):
    loading = models.ForeignKey(Loading, on_delete=models.DO_NOTHING,
                                related_name='loading', verbose_name='Загрузка')
    mineral = models.ForeignKey(s.Minerals, on_delete=models.DO_NOTHING,
                                related_name='loading_mineral', verbose_name='Руда')
    mineral_ratio = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Доля руды в грузовике, %')

    def __str__(self):
        return '%s,%s' % (self.loading, self.mineral)


# Модель разгрузки
class UnLoading(models.Model):
    loading = models.ForeignKey(Loading, on_delete=models.DO_NOTHING,
                                related_name='loading_truck', verbose_name='Разгружаемый грузовик')
    storage = models.ForeignKey(s.StorageCatalog, on_delete=models.DO_NOTHING,
                                related_name='storage_unloading', verbose_name='Склад разгрузки')
    date_unload = models.DateTimeField(verbose_name='Время разгрузки', default=timezone.now)

    def __str__(self):
        return '%s,%s' % (self.loading, self.storage)

    def save(self, *args, **kwargs):
        truck_weight = self.loading.weight
        storage_result = StorageResult.objects.get(storage=self.storage)
        storage_result.storage_prev_value = storage_result.storage_value
        new_storage_value = storage_result.storage_value + self.loading.weight
        minerals_in_truck = self.loading.loading.get_queryset()
        for el in minerals_in_truck:
            minerals_in_storage = StorageMineralsResult.objects.filter(storage=self.storage).get(mineral=el.mineral)
            #если такой минерал на складе уже есть
            if minerals_in_storage:
                new_ratio = ((el.mineral_ratio*self.loading.weight)\
                            +(minerals_in_storage.mineral_ratio*storage_result.storage_value))/(new_storage_value)
                minerals_in_storage.mineral_ratio=new_ratio
                minerals_in_storage.save()
            else:
            #если такого минерала на складе нет
                StorageMineralsResult.objects.create(storage=self.storage,
                                                     mineral=el.mineral,
                                                     mineral_ratio=el.mineral_ratio)
        storage_result.storage_value = new_storage_value
        storage_result.save()
        super().save(*args, **kwargs)


class StorageResult(models.Model):
    storage = models.ForeignKey(s.StorageCatalog, on_delete=models.DO_NOTHING, related_name='storage',
                                verbose_name='Склад')
    storage_value = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='Объем склада, т')
    storage_prev_value = models.DecimalField(max_digits=15, decimal_places=2,
                                             verbose_name='Объем склада до раззгрузки, т')

    def get_result(self):
        minerals = StorageMineralsResult.objects.filter(storage=self.storage)
        res_str = ''
        for el in minerals:
            res_str = res_str + el.get_str_description()
        return res_str


# Модель количества и отношения руды на складе
class StorageMineralsResult(models.Model):
    storage = models.ForeignKey(s.StorageCatalog, on_delete=models.DO_NOTHING, related_name='sklad',
                                verbose_name='Склад')
    mineral = models.ForeignKey(s.Minerals, on_delete=models.DO_NOTHING, related_name='mineral', verbose_name='Руда')
    mineral_ratio = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Доля руды на складе, %')

    def __str__(self):
        return '%s,%s,%s' % (self. storage, self.mineral_ratio, self.mineral.name)

    def get_str_description(self):
        return '%s %s, ' % (self.mineral_ratio, self.mineral.unit_name)
