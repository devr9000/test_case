from django.test import TestCase
from .models import BrandCatalog, TruckCatalog


# Create your tests here.
class TruckTestCase(TestCase):
    def setUp(self):
        BrandCatalog.objects.create(name='TestTruck')

    def test_brand_catalog_instance(self):
        self.assertIsInstance(BrandCatalog.objects.get(name='TestTruck'), BrandCatalog)

    def test_brand_catalog_name(self):
        self.assertEqual(BrandCatalog.objects.get(name='TestTruck').name, 'TestTruck')

    def test_brand_catalog_id(self):
        self.assertIsNotNone(BrandCatalog.objects.get(name='TestTruck').id)
        self.assertGreater(BrandCatalog.objects.get(name='TestTruck').id, 0)


class TruckCatalogTestCase(TestCase):
    def setUp(self):
        TruckCatalog.objects.create(brand=BrandCatalog.objects.create(name='TestBrand'),
                                    model='TestModel', max_weight=100000)

    def test_truck_catalog_instance(self):
        self.assertIsInstance(TruckCatalog.objects.get(model='TestModel'), TruckCatalog)

    def test_truck_catalog_model_name(self):
        self.assertEqual(TruckCatalog.objects.get(model='TestModel').model, 'TestModel')

    def test_truck_catalog_id(self):
        self.assertIsNotNone(TruckCatalog.objects.get(model='TestModel').id)
        self.assertGreater(TruckCatalog.objects.get(model='TestModel').id, 0)

    def test_truck_catalog_brand_instance(self):
        self.assertIsInstance(TruckCatalog.objects.get(model='TestModel').brand, BrandCatalog)

    def test_truck_catalog_brand(self):
        self.assertEqual(TruckCatalog.objects.get(model='TestModel').brand.name, 'TestBrand')

    def test_truck_catalog_brand_id(self):
        self.assertIsNotNone(TruckCatalog.objects.get(model='TestModel').brand.id)
        self.assertGreater(TruckCatalog.objects.get(model='TestModel').brand.id, 0)
