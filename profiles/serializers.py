from django.contrib.auth import get_user_model
from rest_framework import serializers

from profiles.models import Profile

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('id', 'first_name', 'last_name', 'username', 'email',)


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = ('id', 'bio', 'profile_picture', 'user')


class AuthorField(serializers.RelatedField):
    def to_representation(self, value):
        return ProfileSerializer(value).data

    def to_internal_value(self, data):
        return data
