from django.contrib.auth import get_user_model
from django.test import TestCase

from menu_scores.models import MenuScore
from menu_votes.models import MenuVote
from menus.models import Menu


class MenuVoteModelTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass')
        self.menu = Menu.objects.create(title='Test Menu', slug='test-menu')
        self.score = MenuScore.objects.create(label='Test Score')

    def test_menu_vote_creation(self):
        menu_vote = MenuVote.objects.create(user=self.user, menu=self.menu, score=self.score)
        self.assertEqual(menu_vote.user, self.user)
        self.assertEqual(menu_vote.menu, self.menu)
        self.assertEqual(menu_vote.score, self.score)
        self.assertIsNotNone(menu_vote.created_at)

    def test_menu_vote_string_representation(self):
        menu_vote = MenuVote.objects.create(user=self.user, menu=self.menu, score=self.score)
        expected_string = f'{self.user} | {self.menu.title} | {self.score}'
        self.assertEqual(str(menu_vote), expected_string)
