from rest_framework import serializers

from like_grow_app.models import Roles


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = "__all__"
