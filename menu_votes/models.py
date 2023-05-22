from django.conf import settings
from django.db import models

from menu_scores.models import MenuScore
from menus.models import Menu

User = settings.AUTH_USER_MODEL


class MenuVote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, null=False, blank=False)
    score = models.ForeignKey(MenuScore, on_delete=models.CASCADE, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} | {self.menu.title} | {self.score}'
