from django.db import models
from django.contrib.auth.models import User
from django.utils.text import Truncator
from markdown import markdown
from django.utils.html import mark_safe
from django.conf import settings

class Board(models.Model):
    name = models.CharField(max_length=30,unique=True)
    description = models.CharField(max_length=100)
    def __str__(self):
        return self.name

    def get_posts_count(self):
        return Post.objects.filter(topic__board=self).count()

    def get_last_post(self):
        return Post.objects.filter(topic__board=self).order_by('-created_at').first()

class Topic(models.Model):
    subject = models.CharField(max_length=255)
    last_updated = models.DateTimeField(auto_now_add=True)
    board = models.ForeignKey(Board,on_delete=models.CASCADE,related_name='topics')
    starter = models.ForeignKey(User,on_delete=models.CASCADE,related_name='topics')
    views = models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.subject
    
    def get_last_ten_posts(self):
        return self.posts.order_by('-created_at')[:10]
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("topic_posts",kwargs={"pk":self.board.pk,"topic_pk":self.pk})
    
class Post(models.Model):
    message = models.TextField(max_length=4000)
    topic = models.ForeignKey(Topic,on_delete=models.CASCADE,related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name='posts')
    updated_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True,related_name='+')
    """
    def __str__(self):
        truncated_message = Truncator(self.message)
        return truncated_message.char(30)
    """

    def get_message_as_markdown(self):
        #print(mark_safe(markdown(self.message,safe_mode='escape')))
        return mark_safe(markdown(markdown(self.message,safe_mode='escape')).replace("<img",'<img class="img-fluid mx-auto d-block"'))

    def __str__(self):
        return self.message



