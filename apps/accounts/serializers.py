



from rest_framework import serializers
from .models import User
import re
from apps.grievances.tasks import send_grievance_email   # ✔ import email task


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'password',
            'first_name',
            'last_name',
            'mobile',
            "email",
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
            email=validated_data.get('email'),
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            mobile=validated_data['mobile'],
            role='CITIZEN'
        )

        # 🚀 Send Welcome Email Notification
        send_grievance_email.delay(
            subject="Welcome to Smart Grievance System",
            message=f"""
Hello {user.username},

Your account has been successfully created in the Smart Grievance System.

You can now submit and track complaints online.

Thank you,
Smart Grievance Team
""",
            recipient_list=[user.email],
        )

        return user