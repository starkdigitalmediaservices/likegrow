from django.contrib.auth.models import User
from django.db import models
from like_grow_app.model.base import Base

# class FacebookUser(Base):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     facebook_id = models.CharField(max_length=255)
#     # Add other fields as required

#     class Meta:
#         db_table = 'facebook_user'

#     def __str__(self):
#         return str(self.pk)
    
from django.db import models

class FacebookUser(models.Model):
    user_id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    access_token = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
