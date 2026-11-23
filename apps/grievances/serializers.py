



# from rest_framework import serializers
# from django.contrib.gis.geos import Point
# from apps.grievances.models import Grievance


# # ======================================================
# # 📝 Main Grievance Serializer (With Address Logic)
# # ======================================================

# class GrievanceSerializer(serializers.ModelSerializer):

#     latitude = serializers.FloatField(source="location.y", read_only=True)
#     longitude = serializers.FloatField(source="location.x", read_only=True)

#     citizen_name = serializers.SerializerMethodField()
#     formatted_address = serializers.SerializerMethodField()

#     # 👮 Officer who resolved complaint
#     resolved_by_name = serializers.SerializerMethodField()

#     class Meta:
#         model = Grievance
#         fields = [
#             "id",
#             "title",
#             "description",
#             "image",

#             "before_image",
#             "after_image",
#             "resolution_note",

#             "department",
#             "priority",

#             "latitude",
#             "longitude",

#             "status",

#             "citizen_name",
#             "resolved_by_name",

#             "created_at",
#             "resolved_at",

#             "formatted_address",
#         ]

#         read_only_fields = [
#             "department",
#             "priority",
#             "status",
#             "created_at",
#             "resolved_at",
#         ]

#     # ---------------------------------------------------
#     # 👤 Citizen Name
#     # ---------------------------------------------------

#     def get_citizen_name(self, obj):
#         return f"{obj.user.first_name} {obj.user.last_name}".strip() or obj.user.username


#     # ---------------------------------------------------
#     # 👮 Officer who resolved complaint
#     # ---------------------------------------------------

#     def get_resolved_by_name(self, obj):
#         if obj.resolved_by:
#             return obj.resolved_by.username
#         return None


#     # ---------------------------------------------------
#     # 📍 Convert Coordinates to Google Maps Link
#     # ---------------------------------------------------

#     def get_formatted_address(self, obj):
#         return f"https://www.google.com/maps?q={obj.location.y},{obj.location.x}"


#     # ---------------------------------------------------
#     # 🗺 Create Point from Latitude/Longitude
#     # ---------------------------------------------------

#     def create(self, validated_data):

#         request = self.context.get("request")

#         lat = request.data.get("latitude")
#         lon = request.data.get("longitude")

#         if lat and lon:
#             validated_data["location"] = Point(float(lon), float(lat))

#         return Grievance.objects.create(**validated_data)


# # ======================================================
# # 🔄 Status Update Serializer
# # ======================================================

# class GrievanceStatusUpdateSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Grievance
#         fields = [
#             "status",
#             "before_image",
#             "after_image",
#             "resolution_note"
#         ]

#     def validate(self, data):

#         # ❌ Prevent update if already resolved
#         if self.instance.status == "resolved":
#             raise serializers.ValidationError(
#                 "This grievance is already resolved. Status cannot be changed."
#             )

#         # Fix frontend 'In Progress'
#         status = data.get("status", "").lower()

#         if status == "in progress":
#             data["status"] = "in_progress"

#         return data


# from rest_framework import serializers
# from django.contrib.gis.geos import Point
# from apps.grievances.models import Grievance
# from apps.departments.models import Department


# # ======================================================
# # 📝 Main Grievance Serializer (With Address Logic)
# # ======================================================

# class GrievanceSerializer(serializers.ModelSerializer):

#     latitude = serializers.FloatField(source="location.y", read_only=True)
#     longitude = serializers.FloatField(source="location.x", read_only=True)

#     citizen_name = serializers.SerializerMethodField()
#     formatted_address = serializers.SerializerMethodField()

#     # 👮 Officer who resolved complaint
#     resolved_by_name = serializers.SerializerMethodField()

#     # 🏢 Multiple Departments (Read Only)
#     department = serializers.StringRelatedField(many=True, read_only=True)

#     class Meta:
#         model = Grievance
#         fields = [
#             "id",
#             "title",
#             "description",
#             "image",

#             "before_image",
#             "after_image",
#             "resolution_note",

#             "department",
#             "priority",

#             "latitude",
#             "longitude",

#             "status",

#             "citizen_name",
#             "resolved_by_name",

#             "created_at",
#             "resolved_at",

#             "formatted_address",
#         ]

#         read_only_fields = [
#             "department",
#             "priority",
#             "status",
#             "created_at",
#             "resolved_at",
#         ]

#     # ---------------------------------------------------
#     # 👤 Citizen Name
#     # ---------------------------------------------------

#     def get_citizen_name(self, obj):
#         return f"{obj.user.first_name} {obj.user.last_name}".strip() or obj.user.username


#     # ---------------------------------------------------
#     # 👮 Officer who resolved complaint
#     # ---------------------------------------------------

#     def get_resolved_by_name(self, obj):
#         if obj.resolved_by:
#             return obj.resolved_by.username
#         return None


#     # ---------------------------------------------------
#     # 📍 Convert Coordinates to Google Maps Link
#     # ---------------------------------------------------

#     def get_formatted_address(self, obj):
#         return f"https://www.google.com/maps?q={obj.location.y},{obj.location.x}"


#     # ---------------------------------------------------
#     # 🗺 Create Point from Latitude/Longitude
#     # ---------------------------------------------------

#     def create(self, validated_data):

#         request = self.context.get("request")

#         lat = request.data.get("latitude")
#         lon = request.data.get("longitude")

#         if lat and lon:
#             validated_data["location"] = Point(float(lon), float(lat))

#         # remove department if frontend tries to send it
#         validated_data.pop("department", None)

#         grievance = Grievance.objects.create(**validated_data)

#         return grievance


# # ======================================================
# # 🔄 Status Update Serializer
# # ======================================================

# class GrievanceStatusUpdateSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Grievance
#         fields = [
#             "status",
#             "before_image",
#             "after_image",
#             "resolution_note"
#         ]

#     def validate(self, data):

#         # ❌ Prevent update if already resolved
#         if self.instance.status == "resolved":
#             raise serializers.ValidationError(
#                 "This grievance is already resolved. Status cannot be changed."
#             )

#         # Fix frontend 'In Progress'
#         status = data.get("status", "").lower()

#         if status == "in progress":
#             data["status"] = "in_progress"

#         return data


# from rest_framework import serializers
# from django.contrib.gis.geos import Point

# from apps.grievances.models import (
#     Grievance,
#     GrievanceDepartmentTask
# )

# from apps.departments.models import Department


# # ======================================================
# # 🏢 Department Task Serializer
# # ======================================================

# class DepartmentTaskSerializer(serializers.ModelSerializer):

#     department = serializers.CharField(source="department.name")

#     class Meta:
#         model = GrievanceDepartmentTask
#         fields = [
#             "department",
#             "status",
#             "before_image",
#             "after_image",
#             "resolution_note",
#             "resolved_at",
#         ]


# # ======================================================
# # 📝 Main Grievance Serializer
# # ======================================================

# class GrievanceSerializer(serializers.ModelSerializer):

#     latitude = serializers.FloatField(source="location.y", read_only=True)
#     longitude = serializers.FloatField(source="location.x", read_only=True)

#     citizen_name = serializers.SerializerMethodField()
#     formatted_address = serializers.SerializerMethodField()

#     resolved_by_name = serializers.SerializerMethodField()

#     # Existing department list
#     department = serializers.StringRelatedField(many=True, read_only=True)

#     # NEW: department tasks progress
#     department_tasks = DepartmentTaskSerializer(
#         many=True,
#         read_only=True
#     )

#     class Meta:
#         model = Grievance
#         fields = [
#             "id",
#             "title",
#             "description",
#             "image",

#             "before_image",
#             "after_image",
#             "resolution_note",

#             "department",
#             "department_tasks",

#             "priority",

#             "latitude",
#             "longitude",

#             "status",

#             "citizen_name",
#             "resolved_by_name",

#             "created_at",
#             "resolved_at",

#             "formatted_address",
#         ]

#         read_only_fields = [
#             "department",
#             "department_tasks",
#             "priority",
#             "status",
#             "created_at",
#             "resolved_at",
#         ]

#     # ---------------------------------------------------
#     # 👤 Citizen Name
#     # ---------------------------------------------------

#     def get_citizen_name(self, obj):
#         return f"{obj.user.first_name} {obj.user.last_name}".strip() or obj.user.username

#     # ---------------------------------------------------
#     # 👮 Officer who resolved complaint
#     # ---------------------------------------------------

#     def get_resolved_by_name(self, obj):
#         if obj.resolved_by:
#             return obj.resolved_by.username
#         return None

#     # ---------------------------------------------------
#     # 📍 Convert Coordinates to Google Maps Link
#     # ---------------------------------------------------

#     def get_formatted_address(self, obj):
#         return f"https://www.google.com/maps?q={obj.location.y},{obj.location.x}"

#     # ---------------------------------------------------
#     # 🗺 Create Point from Latitude/Longitude
#     # ---------------------------------------------------

#     def create(self, validated_data):

#         request = self.context.get("request")

#         lat = request.data.get("latitude")
#         lon = request.data.get("longitude")

#         if lat and lon:
#             validated_data["location"] = Point(float(lon), float(lat))

#         validated_data.pop("department", None)

#         grievance = Grievance.objects.create(**validated_data)

#         return grievance


# # ======================================================
# # 🔄 Status Update Serializer
# # ======================================================

# class GrievanceStatusUpdateSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Grievance
#         fields = [
#             "status",
#             "before_image",
#             "after_image",
#             "resolution_note"
#         ]

#     def validate(self, data):

#         if self.instance.status == "resolved":
#             raise serializers.ValidationError(
#                 "This grievance is already resolved."
#             )

#         status = data.get("status", "").lower()

#         if status == "in progress":
#             data["status"] = "in_progress"

#         return data


# from rest_framework import serializers
# from django.contrib.gis.geos import Point

# from apps.grievances.models import (
#     Grievance,
#     GrievanceDepartmentTask,
#     OfficerAction   # 🆕 NEW IMPORT
# )

# from apps.departments.models import Department


# # ======================================================
# # 🏢 Department Task Serializer
# # ======================================================

# class DepartmentTaskSerializer(serializers.ModelSerializer):

#     department = serializers.CharField(source="department.name")

#     class Meta:
#         model = GrievanceDepartmentTask
#         fields = [
#             "department",
#             "status",
#             "before_image",
#             "after_image",
#             "resolution_note",
#             "resolved_at",
#         ]


# # ======================================================
# # 🆕 Officer Action Serializer (NEW FEATURE)
# # ======================================================

# class OfficerActionSerializer(serializers.ModelSerializer):

#     officer_name = serializers.SerializerMethodField()

#     class Meta:
#         model = OfficerAction
#         fields = [
#             "id",
#             "action_type",
#             "reason",
#             "officer_name",
#             "created_at",
#         ]

#     def get_officer_name(self, obj):
#         return obj.officer.username


# # ======================================================
# # 📝 Main Grievance Serializer
# # ======================================================

# class GrievanceSerializer(serializers.ModelSerializer):

#     latitude = serializers.FloatField(source="location.y", read_only=True)
#     longitude = serializers.FloatField(source="location.x", read_only=True)

#     citizen_name = serializers.SerializerMethodField()
#     formatted_address = serializers.SerializerMethodField()

#     resolved_by_name = serializers.SerializerMethodField()

#     # Existing department list
#     department = serializers.StringRelatedField(many=True, read_only=True)

#     # Department tasks progress
#     department_tasks = DepartmentTaskSerializer(
#         many=True,
#         read_only=True
#     )

#     # 🆕 Officer action history (NEW FEATURE)
#     officer_actions = OfficerActionSerializer(
#         many=True,
#         read_only=True
#     )

#     class Meta:
#         model = Grievance
#         fields = [
#             "id",
#             "title",
#             "description",
#             "image",

#             "before_image",
#             "after_image",
#             "resolution_note",

#             "department",
#             "department_tasks",

#             "priority",

#             "latitude",
#             "longitude",

#             "status",

#             "citizen_name",
#             "resolved_by_name",

#             "created_at",
#             "resolved_at",

#             "formatted_address",

#             # 🆕 NEW FIELD
#             "officer_actions",
#         ]

#         read_only_fields = [
#             "department",
#             "department_tasks",
#             "priority",
#             "status",
#             "created_at",
#             "resolved_at",
#             "officer_actions",   # 🆕
#         ]

#     # ---------------------------------------------------
#     # 👤 Citizen Name
#     # ---------------------------------------------------

#     def get_citizen_name(self, obj):
#         return f"{obj.user.first_name} {obj.user.last_name}".strip() or obj.user.username

#     # ---------------------------------------------------
#     # 👮 Officer who resolved complaint
#     # ---------------------------------------------------

#     def get_resolved_by_name(self, obj):
#         if obj.resolved_by:
#             return obj.resolved_by.username
#         return None

#     # ---------------------------------------------------
#     # 📍 Convert Coordinates to Google Maps Link
#     # ---------------------------------------------------

#     def get_formatted_address(self, obj):
#         return f"https://www.google.com/maps?q={obj.location.y},{obj.location.x}"

#     # ---------------------------------------------------
#     # 🗺 Create Point from Latitude/Longitude
#     # ---------------------------------------------------

#     def create(self, validated_data):

#         request = self.context.get("request")

#         lat = request.data.get("latitude")
#         lon = request.data.get("longitude")

#         if lat and lon:
#             validated_data["location"] = Point(float(lon), float(lat))

#         validated_data.pop("department", None)

#         grievance = Grievance.objects.create(**validated_data)

#         return grievance


# # ======================================================
# # 🔄 Status Update Serializer
# # ======================================================

# class GrievanceStatusUpdateSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Grievance
#         fields = [
#             "status",
#             "before_image",
#             "after_image",
#             "resolution_note"
#         ]

#     def validate(self, data):

#         if self.instance.status == "resolved":
#             raise serializers.ValidationError(
#                 "This grievance is already resolved."
#             )

#         status = data.get("status", "").lower()

#         if status == "in progress":
#             data["status"] = "in_progress"

#         return data

# from rest_framework import serializers
# from django.contrib.gis.geos import Point

# from apps.grievances.models import (
#     Grievance,
#     GrievanceDepartmentTask,
#     OfficerAction
# )

# from apps.departments.models import Department


# # ======================================================
# # 🏢 Department Task Serializer
# # ======================================================

# class DepartmentTaskSerializer(serializers.ModelSerializer):

#     department = serializers.CharField(source="department.name")

#     class Meta:
#         model = GrievanceDepartmentTask
#         fields = [
#             "department",
#             "status",
#             "before_image",
#             "after_image",
#             "resolution_note",
#             "resolved_at",
#         ]


# # ======================================================
# # 🆕 Officer Action Serializer
# # ======================================================

# class OfficerActionSerializer(serializers.ModelSerializer):

#     officer_name = serializers.SerializerMethodField()

#     class Meta:
#         model = OfficerAction
#         fields = [
#             "id",
#             "action_type",
#             "reason",
#             "officer_name",
#             "created_at",
#         ]

#     def get_officer_name(self, obj):
#         return obj.officer.username


# # ======================================================
# # 📝 Main Grievance Serializer
# # ======================================================

# class GrievanceSerializer(serializers.ModelSerializer):

#     latitude = serializers.FloatField(source="location.y", read_only=True)
#     longitude = serializers.FloatField(source="location.x", read_only=True)

#     citizen_name = serializers.SerializerMethodField()
#     formatted_address = serializers.SerializerMethodField()
#     resolved_by_name = serializers.SerializerMethodField()
#     rejected_by_name = serializers.SerializerMethodField()  # 🆕

#     department = serializers.StringRelatedField(many=True, read_only=True)

#     department_tasks = DepartmentTaskSerializer(
#         many=True,
#         read_only=True
#     )

#     officer_actions = OfficerActionSerializer(
#         many=True,
#         read_only=True
#     )

#     class Meta:
#         model = Grievance
#         fields = [
#             "id",
#             "title",
#             "description",
#             "image",

#             "before_image",
#             "after_image",
#             "resolution_note",

#             # 🚫 Rejection fields (NEW)
#             "rejection_proof",
#             "rejection_reason",
#             "rejected_by_name",

#             "department",
#             "department_tasks",

#             "priority",

#             "latitude",
#             "longitude",

#             "status",

#             "citizen_name",
#             "resolved_by_name",

#             "created_at",
#             "resolved_at",

#             "formatted_address",

#             "officer_actions",
#         ]

#         read_only_fields = [
#             "department",
#             "department_tasks",
#             "priority",
#             "status",
#             "created_at",
#             "resolved_at",
#             "officer_actions",
#             "rejected_by_name",
#         ]

#     # ---------------------------------------------------
#     # 👤 Citizen Name
#     # ---------------------------------------------------

#     def get_citizen_name(self, obj):
#         return f"{obj.user.first_name} {obj.user.last_name}".strip() or obj.user.username

#     # ---------------------------------------------------
#     # 👮 Resolved By
#     # ---------------------------------------------------

#     def get_resolved_by_name(self, obj):
#         if obj.resolved_by:
#             return obj.resolved_by.username
#         return None

#     # ---------------------------------------------------
#     # 🚫 Rejected By (NEW)
#     # ---------------------------------------------------

#     def get_rejected_by_name(self, obj):
#         if obj.rejected_by:
#             return obj.rejected_by.username
#         return None

#     # ---------------------------------------------------
#     # 📍 Google Maps Link
#     # ---------------------------------------------------

#     def get_formatted_address(self, obj):
#         return f"https://www.google.com/maps?q={obj.location.y},{obj.location.x}"

#     # ---------------------------------------------------
#     # 🗺 Create Point from Latitude/Longitude
#     # ---------------------------------------------------

#     def create(self, validated_data):

#         request = self.context.get("request")

#         lat = request.data.get("latitude")
#         lon = request.data.get("longitude")

#         if lat and lon:
#             validated_data["location"] = Point(float(lon), float(lat))

#         validated_data.pop("department", None)

#         grievance = Grievance.objects.create(**validated_data)

#         return grievance


# # ======================================================
# # 🔄 Status Update Serializer (UPDATED)
# # ======================================================

# class GrievanceStatusUpdateSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Grievance
#         fields = [
#             "status",
#             "before_image",
#             "after_image",
#             "resolution_note",

#             # 🚫 NEW FIELDS
#             "rejection_proof",
#             "rejection_reason",
#         ]

#     def validate(self, data):

#         if self.instance.status == "resolved":
#             raise serializers.ValidationError(
#                 "This grievance is already resolved."
#             )

#         status = data.get("status", "").lower()

#         if status == "in progress":
#             data["status"] = "in_progress"

#         return data
    







from rest_framework import serializers
from django.contrib.gis.geos import Point

from apps.grievances.models import (
    Grievance,
    GrievanceDepartmentTask,
    OfficerAction
)

from apps.departments.models import Department


# ======================================================
# 🏢 Department Task Serializer
# ======================================================

class DepartmentTaskSerializer(serializers.ModelSerializer):

    department = serializers.CharField(source="department.name")

    class Meta:
        model = GrievanceDepartmentTask
        fields = [
            "department",
            "status",
            "before_image",
            "after_image",
            "resolution_note",
            "resolved_at",
        ]


# ======================================================
# 🆕 Officer Action Serializer
# ======================================================

class OfficerActionSerializer(serializers.ModelSerializer):

    officer_name = serializers.SerializerMethodField()

    class Meta:
        model = OfficerAction
        fields = [
            "id",
            "action_type",
            "reason",
            "officer_name",
            "created_at",
        ]

    def get_officer_name(self, obj):
        return obj.officer.username


# ======================================================
# 📝 Main Grievance Serializer
# ======================================================

class GrievanceSerializer(serializers.ModelSerializer):

    latitude = serializers.FloatField(source="location.y", read_only=True)
    longitude = serializers.FloatField(source="location.x", read_only=True)

    citizen_name = serializers.SerializerMethodField()
    resolved_by_name = serializers.SerializerMethodField()
    rejected_by_name = serializers.SerializerMethodField()

    formatted_address = serializers.SerializerMethodField()

    department = serializers.StringRelatedField(many=True, read_only=True)

    # 🔥 FIX: Show parent tasks for duplicates
    department_tasks = serializers.SerializerMethodField()

    officer_actions = OfficerActionSerializer(many=True, read_only=True)

    total_reports = serializers.SerializerMethodField()
    is_duplicate = serializers.BooleanField(read_only=True)
    parent_id = serializers.SerializerMethodField()

    class Meta:
        model = Grievance
        fields = [
            "id",
            "title",
            "description",
            "image",

            "before_image",
            "after_image",
            "resolution_note",

            "rejection_proof",
            "rejection_reason",
            "rejected_by_name",

            "department",
            "department_tasks",

            "priority",

            "latitude",
            "longitude",
            "formatted_address",

            "status",

            "citizen_name",
            "resolved_by_name",

            "created_at",
            "resolved_at",

            "officer_actions",

            "is_duplicate",
            "parent_id",
            "total_reports",
        ]

        read_only_fields = [
            "department",
            "department_tasks",
            "priority",
            "status",
            "created_at",
            "resolved_at",
            "officer_actions",
            "rejected_by_name",
            "is_duplicate",
            "parent_id",
            "total_reports",
        ]

    # ---------------------------------------------------
    # 👤 Citizen Name
    # ---------------------------------------------------

    def get_citizen_name(self, obj):
        full_name = f"{obj.user.first_name} {obj.user.last_name}".strip()
        return full_name if full_name else obj.user.username

    # ---------------------------------------------------
    # 👮 Resolved By
    # ---------------------------------------------------

    def get_resolved_by_name(self, obj):
        return obj.resolved_by.username if obj.resolved_by else None

    # ---------------------------------------------------
    # 🚫 Rejected By
    # ---------------------------------------------------

    def get_rejected_by_name(self, obj):
        return obj.rejected_by.username if obj.rejected_by else None

    # ---------------------------------------------------
    # 📍 Google Maps Link
    # ---------------------------------------------------

    def get_formatted_address(self, obj):
        return f"https://www.google.com/maps?q={obj.location.y},{obj.location.x}"

    # ---------------------------------------------------
    # 🔥 Department Tasks (PARENT SYNC)
    # ---------------------------------------------------

    def get_department_tasks(self, obj):
        if obj.is_duplicate and obj.parent:
            tasks = obj.parent.department_tasks.all()
        else:
            tasks = obj.department_tasks.all()

        return DepartmentTaskSerializer(tasks, many=True).data

    # ---------------------------------------------------
    # 🔥 Total Reports
    # ---------------------------------------------------

    def get_total_reports(self, obj):
        if obj.is_duplicate and obj.parent:
            return obj.parent.linked_users.count()
        return obj.linked_users.count()

    # ---------------------------------------------------
    # 🔥 Parent ID
    # ---------------------------------------------------

    def get_parent_id(self, obj):
        return obj.parent.id if obj.parent else None

    # ---------------------------------------------------
    # 🗺 Create
    # ---------------------------------------------------

    def create(self, validated_data):
        request = self.context.get("request")

        lat = request.data.get("latitude")
        lon = request.data.get("longitude")

        if lat and lon:
            validated_data["location"] = Point(float(lon), float(lat))

        validated_data.pop("department", None)

        return Grievance.objects.create(**validated_data)


# ======================================================
# 🔄 STATUS UPDATE SERIALIZER (🔥 FINAL FIX)
# ======================================================

class GrievanceStatusUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Grievance
        fields = [
            "status",
            "before_image",
            "after_image",
            "resolution_note",
            "rejection_proof",
            "rejection_reason",
        ]

    # ---------------------------------------------------
    # VALIDATION
    # ---------------------------------------------------

    def validate(self, data):

        if self.instance.status == "resolved":
            raise serializers.ValidationError(
                "This grievance is already resolved."
            )

        status = data.get("status", "").lower()

        if status == "in progress":
            data["status"] = "in_progress"

        return data

    # ---------------------------------------------------
    # 🔥 FINAL UPDATE LOGIC
    # ---------------------------------------------------

    def update(self, instance, validated_data):

        # 🔥 Always operate on parent
        if instance.is_duplicate and instance.parent:
            instance = instance.parent

        instance = super().update(instance, validated_data)

        # --------------------------------------------------
        # 🔥 SYNC RESOLVED
        # --------------------------------------------------
        if instance.status == "resolved":

            for dup in instance.duplicates.all():
                dup.status = "resolved"
                dup.resolved_at = instance.resolved_at
                dup.resolution_note = instance.resolution_note
                dup.department.set(instance.department.all())
                dup.save()

        # --------------------------------------------------
        # 🔥 SYNC REJECTED
        # --------------------------------------------------
        if instance.status == "rejected":

            for dup in instance.duplicates.all():
                dup.status = "rejected"
                dup.rejection_reason = instance.rejection_reason
                dup.rejection_proof = instance.rejection_proof
                dup.rejected_by = instance.rejected_by
                dup.save()

        return instance