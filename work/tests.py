from django.test import TestCase
from .models import Loading
from machinery.models import Truck, BrandCatalog, TruckCatalog


class LoadingTestCase(TestCase):
    def setUp(self):
        self.brand = BrandCatalog.objects.create(name='TestTruck')
        self.truck_catalog = TruckCatalog.objects.create(brand=self.brand,
                                    model='TestModel', max_weight=100000)
        self.truck = Truck.objects.create(truck_catalog=self.truck_catalog, board_number='123')
        self.loading = Loading.objects.create(truck=self.truck, weight=200000, over_weight=0)

    def tearDown(self):
        del self.brand
        del self.truck_catalog
        del self.truck
        del self.loading

    def test_loading_ower_weight_calc(self):
        self.assertEqual(self.loading.over_weight, 50)
