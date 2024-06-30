from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from rest_framework import serializers

UserModel = get_user_model()


class RegisterUserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    bio = serializers.CharField(source='profile__bio')
    profile_picture = serializers.FileField(source='profile__profile_picture')

    errors_map = {
        "password_mismatch": _("The two password fields did not match."),
    }

    class Meta:
        model = UserModel
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'bio', 'profile_picture')

    def validate(self, data):
        password1 = data.get('password1')
        password2 = data.get('password2')

        if password1 and password2 and password1 != password2:
            raise serializers.ValidationError({
                "password": self.errors_map["password_mismatch"]
            })

        return data

    def create(self, validated_data):
        password1 = validated_data.pop('password1')
        validated_data.pop('password2')

        profile_picture = validated_data.pop('profile__profile_picture')
        bio = validated_data.pop('profile__bio')

        user = UserModel.objects.create(**validated_data)
        user.set_password(password1)
        user.save()

        user.profile.profile_picture = profile_picture
        user.profile.bio = bio
        user.profile.save()

        return user
