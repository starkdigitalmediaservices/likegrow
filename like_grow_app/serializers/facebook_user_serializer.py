from rest_framework import serializers
from like_grow_app.models import FacebookUser

class FacebookUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacebookUser
        fields = '__all__'  # Specify fields accordingly
