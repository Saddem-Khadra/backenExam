from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(UserSerializer, self).__init__(*args, **kwargs)
        if self.context.get("method"):
            self.fields['password'].required = False
            self.fields['email'].required = False
            self.fields['alias'].required = False
            self.fields['dateOfBirth'].required = False

    class Meta:
        model = User
        depth = 1
        fields = ['id', 'first_name', 'last_name', 'email', 'alias', 'dateOfBirth', "friends", "password"]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        if self.context.get("add"):
            instance.friends.add(self.context.get("friend_id"))
        else:
            instance.friends.remove(self.context.get("friend_id"))
        return instance

    def to_representation(self, instance):
        response = super().to_representation(instance)
        for user in response.get("friends"):
            user.pop("password", None)
            user.pop('last_login', None)
            user.pop('is_superuser', None)
            user.pop('is_staff', None)
            user.pop('is_active', None)
            user.pop('date_joined', None)
            user.pop('groups', None)
            user.pop('user_permissions', None)
        return response
