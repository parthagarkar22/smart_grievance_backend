

# from rest_framework import serializers
# from .models import Feedback


# class FeedbackSerializer(serializers.ModelSerializer):

#     department = serializers.ReadOnlyField(source='grievance.department')
#     officer_name = serializers.ReadOnlyField(source='officer.username')

#     class Meta:
#         model = Feedback
#         fields = "__all__"
#         read_only_fields = ["created_at"]



from rest_framework import serializers
from .models import Feedback


# class FeedbackSerializer(serializers.ModelSerializer):

#     officer_name = serializers.ReadOnlyField(source='officer.username')
#     department = serializers.ReadOnlyField(source='officer.department.name')

#     class Meta:
#         model = Feedback
#         fields = "__all__"
#         read_only_fields = ["created_at"]



class FeedbackSerializer(serializers.ModelSerializer):

    officer_name = serializers.ReadOnlyField(source='officer.username')
    department = serializers.ReadOnlyField(source='officer.department.name')

    class Meta:
        model = Feedback
        fields = "__all__"
        read_only_fields = ["created_at", "officer"]

