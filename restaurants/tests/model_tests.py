from django.test import TestCase

from restaurants.models import Restaurant


class RestaurantTestCase(TestCase):
    def setUp(self):
        self.number_of_restaurants = 50
        for i in range(0, self.number_of_restaurants):
            Restaurant.objects.create(label='My Test Restaurant')

    def test_queryset_exists(self):
        qs = Restaurant.objects.all()
        self.assertTrue(qs.exists())

    def test_queryset_count(self):
        qs = Restaurant.objects.all()
        self.assertEqual(qs.count(), self.number_of_restaurants)

    def test_slug_exists(self):
        obj = Restaurant.objects.first()
        self.assertIsNot(obj.slug, None)

    def test_unique_slug(self):
        qs = Restaurant.objects.all()
        for obj in qs:
            slug = obj.slug
            is_found = Restaurant.objects.exclude(id=obj.id).filter(slug__iexact=slug)
            self.assertEqual(is_found.count(), 0)

    def test_access_key_created(self):
        obj = Restaurant.objects.first()
        access_key = obj.access_key
        self.assertTrue(access_key is not None)
