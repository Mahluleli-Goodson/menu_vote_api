from django.test import TestCase
from access_keys.models import AccessKey


class AccessKeyModelTestCase(TestCase):
    def test_access_key_creation(self):
        access_key = AccessKey.objects.create(resource_key='test-resource-key', secret_key='test-secret-key')
        self.assertEqual(access_key.resource_key, 'test-resource-key')
        self.assertEqual(access_key.secret_key, 'test-secret-key')
        self.assertTrue(access_key.active)
        self.assertIsNotNone(access_key.created_at)
        self.assertIsNotNone(access_key.updated_at)

    def test_access_key_string_representation(self):
        access_key = AccessKey.objects.create(resource_key='test-resource-key', secret_key='test-secret-key')
        self.assertEqual(str(access_key), 'test-resource-key')
