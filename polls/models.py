from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Poll(models.Model):
    question = models.CharField(max_length=200)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.question

    def total_votes(self):
        return Vote.objects.filter(choice__poll=self).count()

class Choice(models.Model):
    poll = models.ForeignKey(Poll, related_name='choices', on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)

    def __str__(self):
        return self.choice_text

    def vote_count(self):
        return self.votes.count()

    def vote_percentage(self):
        total = self.poll.total_votes()
        if total == 0:
            return 0
        return round((self.vote_count() / total) * 100, 1)

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, related_name='votes', on_delete=models.CASCADE)
    voted_at = models.DateTimeField(default=timezone.now)

    class Meta:
        # Ensure a user can only vote once per poll
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'choice'],
                name='unique_user_choice'
            )
        ]

    def __str__(self):
        return f"{self.user.username} voted for {self.choice.choice_text}"
    
    def save(self, *args, **kwargs):
        # Additional check: ensure user hasn't voted on this poll already
        if not self.pk:  # Only check on creation
            poll = self.choice.poll
            if Vote.objects.filter(user=self.user, choice__poll=poll).exists():
                from django.core.exceptions import ValidationError
                raise ValidationError("You have already voted on this poll.")
        super().save(*args, **kwargs)