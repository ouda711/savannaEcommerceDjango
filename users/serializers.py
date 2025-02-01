from rest_framework.validators import UniqueValidator
from rest_framework import serializers

from users.models import AppUser


class UserUsernameAndIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = ['id', 'username']


class RegistrationSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=False)
    username = serializers.CharField(validators=[UniqueValidator(queryset=AppUser.objects.all())])
    email = serializers.CharField(validators=[UniqueValidator(queryset=AppUser.objects.all())])
    password = serializers.CharField(write_only=True)  # do not return password in response
    password_confirmation = serializers.CharField(write_only=True)

    def create(self, validated_data):
        validated_data.pop('password_confirmation')
        user = AppUser.objects.create_user(**validated_data)
        return user

    def validate_password(self, password):
        password_confirmation = self.context.get('request').data.get('password_confirmation')

        if password != password_confirmation:
            raise serializers.ValidationError('password and password confirmation do not match')
        return password

    class Meta:
        model = AppUser
        fields = ['first_name', 'last_name', 'username', 'email', 'phone_number','password_confirmation', 'password']