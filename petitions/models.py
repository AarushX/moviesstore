from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Petition(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    requested_movie_title = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='petitions')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return self.title

    @property
    def yes_count(self) -> int:
        return self.votes.filter(value=True).count()


class PetitionVote(models.Model):
    petition = models.ForeignKey(Petition, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='petition_votes')
    value = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('petition', 'user')
        verbose_name = 'Petition Vote'
        verbose_name_plural = 'Petition Votes'

    def __str__(self) -> str:
        return f"{self.user} -> {self.petition} ({'Yes' if self.value else 'No'})"

# Create your models here.
