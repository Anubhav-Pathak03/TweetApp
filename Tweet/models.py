from django.db import models
from django.contrib.auth.models import User

class Tweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=240)
    picture = models.ImageField(upload_to='photos/', blank=True, null=True)
    created_add = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # 🔥 New field to track likes
    likes = models.ManyToManyField(User, related_name='liked_tweets', blank=True)

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return f'{self.user.username} - {self.text[:10]}'
class Comment(models.Model):
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.tweet.id}'
