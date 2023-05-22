from django.test import TestCase

from menus.models import Menu
from restaurants.models import Restaurant


class MenuTestCase(TestCase):
    def setUp(self):
        self.number_of_menus = 10
        self.restaurant = Restaurant.objects.create(label='My Test Restaurant')
        for i in range(0, self.number_of_menus):
            Menu.objects.create(
                restaurant=self.restaurant,
                title=f"My Test Menu {i}",
                description=f"Test description main {i}"
            )

    def test_queryset_exists(self):
        qs = Menu.objects.all()
        self.assertTrue(qs.exists())

    def test_queryset_count(self):
        qs = Menu.objects.all()
        self.assertEqual(qs.count(), self.number_of_menus)

    def test_slug_exists(self):
        obj = Menu.objects.last()
        self.assertIsNot(obj.slug, None)

    def test_unique_slug(self):
        qs = Menu.objects.all()
        for obj in qs:
            slug = obj.slug
            is_found = Menu.objects.exclude(id=obj.id).filter(slug__iexact=slug)
            self.assertEqual(is_found.count(), 0)

    def test_menu_linked_to_restaurant(self):
        restaurant = self.restaurant
        menu = Menu.objects.first()
        self.assertTrue(menu.restaurant.pk == restaurant.pk)

    def test_menu_not_added_without_title(self):
        with self.assertRaises(Exception):
            Menu.objects.create(
                title=None,
                restaurant=self.restaurant
            )

    def test_uuids_are_unique(self):
        uuid_list = Menu.objects.all().values_list('uuid', flat=True)
        unique_uuid_list = list(set(uuid_list))
        self.assertEqual(len(uuid_list), len(unique_uuid_list))
