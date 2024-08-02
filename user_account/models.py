from django.db import models
from django.contrib.auth.models import User

from reviews.models import Review, Work


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    def __str__(self):
        return self.user.username


class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='search_history')
    search_term = models.CharField(max_length=500)
    search_url = models.URLField(max_length=600)
    searched_at = models.DateTimeField(auto_now_add=True)


class ReviewHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review_history')
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    review_url = models.URLField(max_length=200)
    reviewed_at = models.DateTimeField(auto_now_add=True)