from django.db import models
from accounts.models import User
from django.urls import reverse


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    body = models.TextField()
    slug = models.SlugField()
    title = models.CharField(max_length=100, null=True, blank=True)
    is_active=models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        return f'{self.slug} - {self.updated}'


    def likes_count(self):
        return self.plikes.count()

    def user_can_like(self, user):
        user_like = user.ulikes.filter(post=self)
        if user_like.exists():
            return False
        return True



class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ucomments',null=True,blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='pcomments',null=True,blank=True)
    body = models.TextField(max_length=400)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.body[:30]}'


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ulikes',null=True,blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='plikes',null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} liked {self.post.slug}'