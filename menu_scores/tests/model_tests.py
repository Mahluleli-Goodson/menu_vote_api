from django.test import TestCase
from menu_scores.models import MenuScore


class MenuScoreModelTestCase(TestCase):
    def test_menu_score_creation(self):
        menu_score = MenuScore.objects.create(label='Test Score')
        self.assertEqual(menu_score.label, 'Test Score')
        self.assertIsNotNone(menu_score.uuid)
        self.assertIsNotNone(menu_score.created_at)
        self.assertIsNotNone(menu_score.updated_at)

    def test_menu_score_string_representation(self):
        menu_score = MenuScore.objects.create(label='Test Score')
        self.assertEqual(str(menu_score), 'Test Score')
