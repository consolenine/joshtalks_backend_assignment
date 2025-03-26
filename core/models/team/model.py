from django.db import models
from django.utils.translation import gettext_lazy as _

from ..user import User


class Team(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey("User", on_delete=models.RESTRICT, related_name="owned_teams")
    members = models.ManyToManyField("User", through='TeamRoles', related_name="teams")

    def __str__(self):
        return self.name

class TeamRoles(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey("Team", on_delete=models.CASCADE)

    class Roles(models.TextChoices):
        MANAGER = 'manager', _('Manager')
        MEMBER = 'member', _('Member')

    role = models.CharField(max_length=10, choices=Roles, default=Roles.MEMBER)

    def __str__(self):
        return f"{self.team.name} - {self.role} - {self.user.username}"