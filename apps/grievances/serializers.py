

from rest_framework import serializers
from django.contrib.gis.geos import Point
from apps.grievances.models import Grievance


# ======================================================
# 📝 Main Grievance Serializer
# ======================================================

class GrievanceSerializer(serializers.ModelSerializer):
    latitude = serializers.FloatField(write_only=True)
    longitude = serializers.FloatField(write_only=True)

    class Meta:
        model = Grievance
        fields = [
            "id",
            "title",
            "description",
            "image",
            "department",
            "priority",
            "latitude",
            "longitude",
            "status",
            "created_at",
        ]
        read_only_fields = [
            "department",
            "priority",
            "status",
            "created_at",
        ]

    def create(self, validated_data):
        # Remove latitude & longitude before saving
        lat = validated_data.pop("latitude")
        lon = validated_data.pop("longitude")

        # Convert to GIS Point
        validated_data["location"] = Point(lon, lat)

        # DO NOT set department here
        # View will set department="Pending"

        return Grievance.objects.create(**validated_data)


# ======================================================
# 🔄 Status Update Serializer (FOR OFFICER)
# ======================================================

class GrievanceStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grievance
        fields = ["status"]
