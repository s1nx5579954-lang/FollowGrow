from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import secrets

class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(max_length=300, blank=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name='profiles')
    line_user_id = models.CharField(max_length=100, blank=True, null=True)
    line_link_code = models.CharField(max_length=10, blank=True, null=True)

    def generate_line_link_code(self):
        self.line_link_code = secrets.token_hex(3).upper()
        self.save()
        return self.line_link_code
        
    def __str__(self):
        return f"{self.user.username}のプロフィール"
    


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)