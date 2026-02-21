




from rest_framework import serializers
from .models import User
import re


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'username',
            'password',
            'first_name',
            'last_name',
            'mobile',
        )

    def validate_mobile(self, value):
        if not re.match(r'^[6-9]\d{9}$', value):
            raise serializers.ValidationError("Mobile number must be 10 digits")
        return value

    def validate_password(self, value):
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise serializers.ValidationError(
                "Password must contain at least one special character"
            )
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            mobile=validated_data['mobile'],
            role='CITIZEN'
        )
        return user
