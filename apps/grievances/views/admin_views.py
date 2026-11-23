

# from rest_framework.viewsets import ModelViewSet
# from rest_framework.permissions import IsAdminUser
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.views import APIView

# from django.http import HttpResponse
# import openpyxl
# from reportlab.pdfgen import canvas

# from apps.grievances.models import Grievance
# from apps.grievances.serializers import (
#     GrievanceSerializer,
#     GrievanceStatusUpdateSerializer,
# )

# # 🔔 Notification Celery task
# from apps.notifications.tasks import create_notification

# # 📧 Email Celery task
# from apps.grievances.tasks import send_grievance_email


# # =========================================================
# # ADMIN GRIEVANCE MANAGEMENT
# # =========================================================

# class AdminGrievanceViewSet(ModelViewSet):
#     """
#     Admin:
#     - View all grievances
#     - Update grievance status
#     - Delete grievances
#     """

#     queryset = Grievance.objects.all().order_by("-created_at")
#     permission_classes = [IsAdminUser]

#     def get_serializer_class(self):
#         if self.action in ["partial_update", "update"]:
#             return GrievanceStatusUpdateSerializer
#         return GrievanceSerializer

#     # 🔥 Runs AFTER status update
#     def perform_update(self, serializer):

#         grievance = self.get_object()
#         old_status = grievance.status
#         old_department = grievance.department

#         grievance = serializer.save()

#         # 🔔 Notify citizen
#         create_notification.delay(
#             grievance.user.id,
#             f"Your grievance #{grievance.id} status changed to {grievance.status}"
#         )

#         # 📧 EMAIL: Department Assigned
#         if grievance.department != old_department:
#             send_grievance_email.delay(
#                 subject="Complaint Assigned to Department",
#                 message=f"""
# Hello {grievance.user.username},

# Your complaint '{grievance.title}' has been assigned to the {grievance.department} department.

# Our team will review it soon.

# Smart Grievance System
# """,
#                 recipient_list=[grievance.user.email],
#             )

#         # 📧 EMAIL: Status Updated
#         if grievance.status != old_status:
#             send_grievance_email.delay(
#                 subject="Complaint Status Updated",
#                 message=f"""
# Hello {grievance.user.username},

# The status of your complaint '{grievance.title}' has been updated.

# New Status: {grievance.status}

# Smart Grievance System
# """,
#                 recipient_list=[grievance.user.email],
#             )

#         # 📧 EMAIL: Complaint Resolved
#         if grievance.status.lower() == "resolved":
#             send_grievance_email.delay(
#                 subject="Complaint Resolved",
#                 message=f"""
# Hello {grievance.user.username},

# Your complaint '{grievance.title}' has been resolved.

# Please check the system and provide feedback.

# Smart Grievance System
# """,
#                 recipient_list=[grievance.user.email],
#             )

#         # 📧 EMAIL: Complaint Rejected
#         if grievance.status.lower() == "rejected":
#             send_grievance_email.delay(
#                 subject="Complaint Rejected",
#                 message=f"""
# Hello {grievance.user.username},

# Your complaint '{grievance.title}' has been rejected after review.

# If you need further help, please contact support.

# Smart Grievance System
# """,
#                 recipient_list=[grievance.user.email],
#             )

#     def destroy(self, request, *args, **kwargs):
#         instance = self.get_object()
#         instance.delete()

#         return Response(
#             {"message": "Grievance deleted successfully"},
#             status=status.HTTP_200_OK
#         )

    
    


# from rest_framework.views import APIView
# from rest_framework.permissions import IsAdminUser
# from rest_framework.response import Response
# from django.http import HttpResponse
# from apps.grievances.models import Grievance

# import openpyxl
# from io import BytesIO

# from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
# from reportlab.lib.pagesizes import A4
# from reportlab.lib.styles import getSampleStyleSheet
# from reportlab.lib import colors


# class MonthlyReportView(APIView):

#     permission_classes = [IsAdminUser]

#     def get(self, request):

#         month = request.GET.get("month")
#         year = request.GET.get("year")
#         format_type = request.GET.get("type", "excel").lower()

#         if not month or not year:
#             return Response(
#                 {"error": "month and year are required"},
#                 status=400
#             )

#         month = int(month)
#         year = int(year)

#         grievances = Grievance.objects.filter(
#             created_at__month=month,
#             created_at__year=year
#         )

#         departments = ["water", "road", "garbage", "sewage", "light"]

#         report_data = []

#         for dept in departments:
#             # dept_grievances = grievances.filter(department__iexact=dept)
#             dept_grievances = grievances.filter(department__name__iexact=dept).distinct()
#             report_data.append({
#                 "department": dept.capitalize(),
#                 "total": dept_grievances.count(),
#                 "pending": dept_grievances.filter(status="pending").count(),
#                 "resolved": dept_grievances.filter(status="resolved").count(),
#                 "rejected": dept_grievances.filter(status="rejected").count(),
#             })

#         if format_type == "pdf":
#             return self.generate_pdf(report_data, month, year)

#         return self.generate_excel(report_data, month, year)

#     # -------------------------------------------------
#     # Excel Report
#     # -------------------------------------------------

#     def generate_excel(self, report_data, month, year):

#         wb = openpyxl.Workbook()
#         ws = wb.active
#         ws.title = "Monthly Report"

#         ws.append(["Department", "Total", "Pending", "Resolved", "Rejected"])

#         for row in report_data:
#             ws.append([
#                 row["department"],
#                 row["total"],
#                 row["pending"],
#                 row["resolved"],
#                 row["rejected"],
#             ])

#         response = HttpResponse(
#             content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
#         )

#         response["Content-Disposition"] = f"attachment; filename=grievance_report_{month}_{year}.xlsx"

#         wb.save(response)

#         return response

#     # -------------------------------------------------
#     # Professional PDF Report
#     # -------------------------------------------------

#     def generate_pdf(self, report_data, month, year):

#         response = HttpResponse(content_type="application/pdf")
#         response["Content-Disposition"] = f"attachment; filename=grievance_report_{month}_{year}.pdf"

#         buffer = BytesIO()

#         doc = SimpleDocTemplate(
#             buffer,
#             pagesize=A4,
#             rightMargin=40,
#             leftMargin=40,
#             topMargin=40,
#             bottomMargin=40
#         )

#         styles = getSampleStyleSheet()
#         elements = []

#         # =============================
#         # TITLE (Smart Grievance System)
#         # =============================

#         title = Paragraph(
#             "<b>SMART GRIEVANCE SYSTEM</b>",
#             styles["Title"]
#         )

#         subtitle = Paragraph(
#             "<b>AI Powered Citizen Complaint Monitoring Platform</b>",
#             styles["Heading2"]
#         )

#         report_title = Paragraph(
#             f"<b>Monthly Grievance Report - {month}/{year}</b>",
#             styles["Heading3"]
#         )

#         elements.append(title)
#         elements.append(subtitle)
#         elements.append(Spacer(1, 10))
#         elements.append(report_title)
#         elements.append(Spacer(1, 30))

#         # =============================
#         # TABLE DATA
#         # =============================

#         table_data = [
#             ["Department", "Total", "Pending", "Resolved", "Rejected"]
#         ]

#         for row in report_data:
#             table_data.append([
#                 row["department"],
#                 row["total"],
#                 row["pending"],
#                 row["resolved"],
#                 row["rejected"]
#             ])

#         table = Table(table_data, colWidths=[120, 80, 80, 80, 80])

#         table.setStyle(TableStyle([

#             ("BACKGROUND", (0,0), (-1,0), colors.darkblue),
#             ("TEXTCOLOR", (0,0), (-1,0), colors.whitesmoke),

#             ("ALIGN", (1,1), (-1,-1), "CENTER"),

#             ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),

#             ("FONTSIZE", (0,0), (-1,-1), 11),

#             ("BOTTOMPADDING", (0,0), (-1,0), 10),

#             ("GRID", (0,0), (-1,-1), 1, colors.black),

#             ("BACKGROUND", (0,1), (-1,-1), colors.beige)

#         ]))

#         elements.append(table)

#         elements.append(Spacer(1, 40))

#         # =============================
#         # FOOTER
#         # =============================

#         footer = Paragraph(
#             "Generated by Smart Grievance System • AI Enabled Civic Issue Monitoring",
#             styles["Normal"]
#         )

#         elements.append(footer)

#         doc.build(elements)

#         pdf = buffer.getvalue()
#         buffer.close()

#         response.write(pdf)

#         return response



# from rest_framework.viewsets import ModelViewSet
# from rest_framework.permissions import IsAdminUser
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.views import APIView

# from django.http import HttpResponse
# from io import BytesIO

# import openpyxl

# from reportlab.platypus import (
#     SimpleDocTemplate,
#     Table,
#     TableStyle,
#     Paragraph,
#     Spacer
# )
# from reportlab.lib.pagesizes import A4
# from reportlab.lib.styles import getSampleStyleSheet
# from reportlab.lib import colors

# from apps.grievances.models import Grievance, OfficerAction
# from apps.grievances.serializers import (
#     GrievanceSerializer,
#     GrievanceStatusUpdateSerializer,
# )

# # 🔔 Notification Celery task
# from apps.notifications.tasks import create_notification

# # 📧 Email Celery task
# from apps.grievances.tasks import send_grievance_email


# # =========================================================
# # ADMIN GRIEVANCE MANAGEMENT
# # =========================================================

# class AdminGrievanceViewSet(ModelViewSet):

#     queryset = Grievance.objects.all().order_by("-created_at")
#     permission_classes = [IsAdminUser]

#     def get_serializer_class(self):
#         if self.action in ["partial_update", "update"]:
#             return GrievanceStatusUpdateSerializer
#         return GrievanceSerializer

#     def perform_update(self, serializer):

#         grievance = self.get_object()
#         old_status = grievance.status
#         old_department = grievance.department

#         grievance = serializer.save()

#         # 🔔 Notify citizen
#         create_notification.delay(
#             grievance.user.id,
#             f"Your grievance #{grievance.id} status changed to {grievance.status}"
#         )

#         # 📧 EMAIL: Department Assigned
#         if grievance.department != old_department:
#             send_grievance_email.delay(
#                 subject="Complaint Assigned to Department",
#                 message=f"""
# Hello {grievance.user.username},

# Your complaint '{grievance.title}' has been assigned to the {grievance.department} department.

# Smart Grievance System
# """,
#                 recipient_list=[grievance.user.email],
#             )

#         # 📧 EMAIL: Status Updated
#         if grievance.status != old_status:
#             send_grievance_email.delay(
#                 subject="Complaint Status Updated",
#                 message=f"""
# Hello {grievance.user.username},

# New Status: {grievance.status}
# """,
#                 recipient_list=[grievance.user.email],
#             )

#         # 📧 EMAIL: Resolved
#         if grievance.status.lower() == "resolved":
#             send_grievance_email.delay(
#                 subject="Complaint Resolved",
#                 message=f"Your complaint '{grievance.title}' has been resolved.",
#                 recipient_list=[grievance.user.email],
#             )

#         # 📧 EMAIL: Rejected
#         if grievance.status.lower() == "rejected":
#             send_grievance_email.delay(
#                 subject="Complaint Rejected",
#                 message=f"Your complaint '{grievance.title}' was rejected.",
#                 recipient_list=[grievance.user.email],
#             )

#     def destroy(self, request, *args, **kwargs):
#         instance = self.get_object()
#         instance.delete()

#         return Response(
#             {"message": "Grievance deleted successfully"},
#             status=status.HTTP_200_OK
#         )


# # =========================================================
# # 🆕 ESCALATED COMPLAINTS API
# # =========================================================

# class EscalatedComplaintsAPIView(APIView):

#     permission_classes = [IsAdminUser]

#     def get(self, request):
#         grievances = Grievance.objects.filter(status="escalated")

#         data = []
#         for g in grievances:
#             data.append({
#                 "id": g.id,
#                 "title": g.title,
#                 "description": g.description,
#                 "priority": g.priority,
#                 "status": g.status,
#                 "officer": str(g.assigned_to) if g.assigned_to else None,
#                 "created_at": g.created_at,
#             })

#         return Response({
#             "total_escalated": len(data),
#             "complaints": data
#         })


# # =========================================================
# # 🆕 TAKE ACTION ON OFFICER API
# # =========================================================

# class TakeActionOnOfficerAPIView(APIView):

#     permission_classes = [IsAdminUser]

#     def post(self, request, grievance_id):

#         try:
#             grievance = Grievance.objects.get(id=grievance_id)
#         except Grievance.DoesNotExist:
#             return Response({"error": "Complaint not found"}, status=404)

#         if grievance.status != "escalated":
#             return Response(
#                 {"error": "Only escalated complaints allowed"},
#                 status=400
#             )

#         officer = grievance.assigned_to

#         if not officer:
#             return Response({"error": "No officer assigned"}, status=400)

#         action_type = request.data.get("action_type")
#         reason = request.data.get("reason")

#         # ✅ Save log
#         OfficerAction.objects.create(
#             grievance=grievance,
#             officer=officer,
#             action_type=action_type,
#             reason=reason
#         )

#         # ⚠️ WARNING
#         if action_type == "WARNING":
#             message = f"Warning sent to {officer}"

#         # 🔄 REASSIGN
#         elif action_type == "REASSIGN":
#             grievance.assigned_to = None
#             grievance.status = "pending"
#             grievance.save()

#             message = "Complaint reassigned successfully"

#         else:
#             return Response({"error": "Invalid action"}, status=400)

#         return Response(
#             {
#                 "message": message,
#                 "action": action_type
#             },
#             status=200
#         )


# # =========================================================
# # 📊 MONTHLY REPORT
# # =========================================================

# class MonthlyReportView(APIView):

#     permission_classes = [IsAdminUser]

#     def get(self, request):

#         month = request.GET.get("month")
#         year = request.GET.get("year")
#         format_type = request.GET.get("type", "excel").lower()

#         if not month or not year:
#             return Response(
#                 {"error": "month and year are required"},
#                 status=400
#             )

#         month = int(month)
#         year = int(year)

#         grievances = Grievance.objects.filter(
#             created_at__month=month,
#             created_at__year=year
#         )

#         departments = ["water", "road", "garbage", "sewage", "light"]
#         report_data = []

#         for dept in departments:
#             dept_grievances = grievances.filter(
#                 department__name__iexact=dept
#             ).distinct()

#             report_data.append({
#                 "department": dept.capitalize(),
#                 "total": dept_grievances.count(),
#                 "pending": dept_grievances.filter(status="pending").count(),
#                 "resolved": dept_grievances.filter(status="resolved").count(),
#                 "rejected": dept_grievances.filter(status="rejected").count(),
#             })

#         if format_type == "pdf":
#             return self.generate_pdf(report_data, month, year)

#         return self.generate_excel(report_data, month, year)

#     def generate_excel(self, report_data, month, year):

#         wb = openpyxl.Workbook()
#         ws = wb.active
#         ws.title = "Monthly Report"

#         ws.append(["Department", "Total", "Pending", "Resolved", "Rejected"])

#         for row in report_data:
#             ws.append([
#                 row["department"],
#                 row["total"],
#                 row["pending"],
#                 row["resolved"],
#                 row["rejected"],
#             ])

#         response = HttpResponse(
#             content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
#         )

#         response["Content-Disposition"] = (
#             f"attachment; filename=report_{month}_{year}.xlsx"
#         )

#         wb.save(response)
#         return response

#     def generate_pdf(self, report_data, month, year):

#         response = HttpResponse(content_type="application/pdf")
#         response["Content-Disposition"] = (
#             f"attachment; filename=report_{month}_{year}.pdf"
#         )

#         buffer = BytesIO()

#         doc = SimpleDocTemplate(buffer, pagesize=A4)
#         styles = getSampleStyleSheet()
#         elements = []

#         elements.append(Paragraph("Smart Grievance System", styles["Title"]))
#         elements.append(Spacer(1, 20))

#         table_data = [["Department", "Total", "Pending", "Resolved", "Rejected"]]

#         for row in report_data:
#             table_data.append([
#                 row["department"],
#                 row["total"],
#                 row["pending"],
#                 row["resolved"],
#                 row["rejected"]
#             ])

#         table = Table(table_data)

#         table.setStyle(TableStyle([
#             ("GRID", (0, 0), (-1, -1), 1, colors.black),
#         ]))

#         elements.append(table)

#         doc.build(elements)

#         pdf = buffer.getvalue()
#         buffer.close()

#         response.write(pdf)
#         return response


# from rest_framework.viewsets import ModelViewSet
# from rest_framework.permissions import IsAdminUser
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.views import APIView
# from rest_framework.exceptions import ValidationError  # ✅ NEW

# from django.http import HttpResponse
# from io import BytesIO

# import openpyxl

# from reportlab.platypus import (
#     SimpleDocTemplate,
#     Table,
#     TableStyle,
#     Paragraph,
#     Spacer
# )
# from reportlab.lib.pagesizes import A4
# from reportlab.lib.styles import getSampleStyleSheet
# from reportlab.lib import colors

# from django.contrib.auth import get_user_model  # ✅ NEW

# from apps.grievances.models import Grievance, OfficerAction
# from apps.grievances.serializers import (
#     GrievanceSerializer,
#     GrievanceStatusUpdateSerializer,
# )

# # 🔔 Notification Celery task
# from apps.notifications.tasks import create_notification

# # 📧 Email Celery task
# from apps.grievances.tasks import send_grievance_email


# # =========================================================
# # ADMIN GRIEVANCE MANAGEMENT
# # =========================================================

# class AdminGrievanceViewSet(ModelViewSet):

#     queryset = Grievance.objects.all().order_by("-created_at")
#     permission_classes = [IsAdminUser]

#     def get_serializer_class(self):
#         if self.action in ["partial_update", "update"]:
#             return GrievanceStatusUpdateSerializer
#         return GrievanceSerializer

#     def perform_update(self, serializer):

#         grievance = self.get_object()
#         old_status = grievance.status
#         old_department = grievance.department

#         # ======================================================
#         # 🚀 AUTO ASSIGN OFFICER ON ESCALATION
#         # ======================================================
#         new_status = serializer.validated_data.get("status")

#         if new_status == "escalated":

#             if not serializer.instance.assigned_to:

#                 User = get_user_model()
#                 grievance_instance = serializer.instance

#                 # ✅ Get first department
#                 dept = grievance_instance.department.first()

#                 if not dept:
#                     raise ValidationError({
#                         "error": "No department assigned to complaint"
#                     })

#                 # ✅ Find officer of that department
#                 officer = User.objects.filter(
#                     # role="officer",
#                     role__iexact="officer",

#                     # department=dept
#                     department__iexact=dept.name.strip()
#                 ).first()
#                 print("Officer found:", officer)

#                 if not officer:
#                     raise ValidationError({
#                         "error": f"No officer found for department {dept.name}"
#                     })

#                 # ✅ Assign officer automatically
#                 serializer.instance.assigned_to = officer

#         # ======================================================

#         grievance = serializer.save()

#         # 🔔 Notify citizen
#         create_notification.delay(
#             grievance.user.id,
#             f"Your grievance #{grievance.id} status changed to {grievance.status}"
#         )

#         # 📧 EMAIL: Department Assigned
#         if grievance.department != old_department:
#             send_grievance_email.delay(
#                 subject="Complaint Assigned to Department",
#                 message=f"""
# Hello {grievance.user.username},

# Your complaint '{grievance.title}' has been assigned to the {grievance.department} department.

# Smart Grievance System
# """,
#                 recipient_list=[grievance.user.email],
#             )

#         # 📧 EMAIL: Status Updated
#         if grievance.status != old_status:
#             send_grievance_email.delay(
#                 subject="Complaint Status Updated",
#                 message=f"""
# Hello {grievance.user.username},

# New Status: {grievance.status}
# """,
#                 recipient_list=[grievance.user.email],
#             )

#         # 📧 EMAIL: Resolved
#         if grievance.status.lower() == "resolved":
#             send_grievance_email.delay(
#                 subject="Complaint Resolved",
#                 message=f"Your complaint '{grievance.title}' has been resolved.",
#                 recipient_list=[grievance.user.email],
#             )

#         # 📧 EMAIL: Rejected
#         if grievance.status.lower() == "rejected":
#             send_grievance_email.delay(
#                 subject="Complaint Rejected",
#                 message=f"Your complaint '{grievance.title}' was rejected.",
#                 recipient_list=[grievance.user.email],
#             )

#     def destroy(self, request, *args, **kwargs):
#         instance = self.get_object()
#         instance.delete()

#         return Response(
#             {"message": "Grievance deleted successfully"},
#             status=status.HTTP_200_OK
#         )


# # =========================================================
# # 🆕 ESCALATED COMPLAINTS API
# # =========================================================

# class EscalatedComplaintsAPIView(APIView):

#     permission_classes = [IsAdminUser]

#     def get(self, request):
#         grievances = Grievance.objects.filter(status="escalated")

#         data = []
#         for g in grievances:
#             data.append({
#                 "id": g.id,
#                 "title": g.title,
#                 "description": g.description,
#                 "priority": g.priority,
#                 "status": g.status,
#                 "officer": str(g.assigned_to) if g.assigned_to else None,
#                 "created_at": g.created_at,
#             })

#         return Response({
#             "total_escalated": len(data),
#             "complaints": data
#         })


# # =========================================================
# # 🆕 TAKE ACTION ON OFFICER API
# # =========================================================

# class TakeActionOnOfficerAPIView(APIView):

#     permission_classes = [IsAdminUser]

#     def post(self, request, grievance_id):

#         try:
#             grievance = Grievance.objects.get(id=grievance_id)
#         except Grievance.DoesNotExist:
#             return Response({"error": "Complaint not found"}, status=404)

#         if grievance.status != "escalated":
#             return Response(
#                 {"error": "Only escalated complaints allowed"},
#                 status=400
#             )

#         officer = grievance.assigned_to

#         if not officer:
#             return Response({"error": "No officer assigned"}, status=400)

#         action_type = request.data.get("action_type")
#         reason = request.data.get("reason")

#         # ✅ Save log
#         OfficerAction.objects.create(
#             grievance=grievance,
#             officer=officer,
#             action_type=action_type,
#             reason=reason
#         )

#         if action_type == "WARNING":
#             message = f"Warning sent to {officer}"

#         elif action_type == "REASSIGN":
#             grievance.assigned_to = None
#             grievance.status = "pending"
#             grievance.save()
#             message = "Complaint reassigned successfully"

#         else:
#             return Response({"error": "Invalid action"}, status=400)

#         return Response(
#             {
#                 "message": message,
#                 "action": action_type
#             },
#             status=200
#         )


# # =========================================================
# # 📊 MONTHLY REPORT
# # =========================================================

# class MonthlyReportView(APIView):

#     permission_classes = [IsAdminUser]

#     def get(self, request):

#         month = request.GET.get("month")
#         year = request.GET.get("year")
#         format_type = request.GET.get("type", "excel").lower()

#         if not month or not year:
#             return Response(
#                 {"error": "month and year are required"},
#                 status=400
#             )

#         month = int(month)
#         year = int(year)

#         grievances = Grievance.objects.filter(
#             created_at__month=month,
#             created_at__year=year
#         )

#         departments = ["water", "road", "garbage", "sewage", "light"]
#         report_data = []

#         for dept in departments:
#             dept_grievances = grievances.filter(
#                 department__name__iexact=dept
#             ).distinct()

#             report_data.append({
#                 "department": dept.capitalize(),
#                 "total": dept_grievances.count(),
#                 "pending": dept_grievances.filter(status="pending").count(),
#                 "resolved": dept_grievances.filter(status="resolved").count(),
#                 "rejected": dept_grievances.filter(status="rejected").count(),
#             })

#         if format_type == "pdf":
#             return self.generate_pdf(report_data, month, year)

#         return self.generate_excel(report_data, month, year)

#     def generate_excel(self, report_data, month, year):

#         wb = openpyxl.Workbook()
#         ws = wb.active
#         ws.title = "Monthly Report"

#         ws.append(["Department", "Total", "Pending", "Resolved", "Rejected"])

#         for row in report_data:
#             ws.append([
#                 row["department"],
#                 row["total"],
#                 row["pending"],
#                 row["resolved"],
#                 row["rejected"],
#             ])

#         response = HttpResponse(
#             content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
#         )

#         response["Content-Disposition"] = (
#             f"attachment; filename=report_{month}_{year}.xlsx"
#         )

#         wb.save(response)
#         return response

#     def generate_pdf(self, report_data, month, year):

#         response = HttpResponse(content_type="application/pdf")
#         response["Content-Disposition"] = (
#             f"attachment; filename=report_{month}_{year}.pdf"
#         )

#         buffer = BytesIO()

#         doc = SimpleDocTemplate(buffer, pagesize=A4)
#         styles = getSampleStyleSheet()
#         elements = []

#         elements.append(Paragraph("Smart Grievance System", styles["Title"]))
#         elements.append(Spacer(1, 20))

#         table_data = [["Department", "Total", "Pending", "Resolved", "Rejected"]]

#         for row in report_data:
#             table_data.append([
#                 row["department"],
#                 row["total"],
#                 row["pending"],
#                 row["resolved"],
#                 row["rejected"]
#             ])

#         table = Table(table_data)

#         table.setStyle(TableStyle([
#             ("GRID", (0, 0), (-1, -1), 1, colors.black),
#         ]))

#         elements.append(table)

#         doc.build(elements)

#         pdf = buffer.getvalue()
#         buffer.close()

#         response.write(pdf)
#         return response

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError

from django.http import HttpResponse
from io import BytesIO

import openpyxl

from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer
)
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

from django.contrib.auth import get_user_model

from apps.grievances.models import Grievance, OfficerAction
from apps.grievances.serializers import (
    GrievanceSerializer,
    GrievanceStatusUpdateSerializer,
)

from apps.notifications.tasks import create_notification
from apps.grievances.tasks import send_grievance_email

# 🔥 NEW IMPORT
from apps.grievances.services.rejection_service import handle_rejection


# =========================================================
# ADMIN GRIEVANCE MANAGEMENT
# =========================================================

class AdminGrievanceViewSet(ModelViewSet):

    queryset = Grievance.objects.all().order_by("-created_at")
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        if self.action in ["partial_update", "update"]:
            return GrievanceStatusUpdateSerializer
        return GrievanceSerializer

    def perform_update(self, serializer):

        grievance = self.get_object()
        old_status = grievance.status
        old_department = grievance.department

        request_data = self.request.data

        # ======================================================
        # 🚫 HANDLE REJECTION (NEW FEATURE)
        # ======================================================
        if request_data.get("status") == "rejected":

            proof = self.request.FILES.get("rejection_proof")
            reason = request_data.get("rejection_reason")

            result = handle_rejection(
                grievance=grievance,
                user=self.request.user,
                proof=proof,
                reason=reason
            )

            # 🔔 Notification
            create_notification.delay(
                grievance.user.id,
                f"Your grievance #{grievance.id} has been rejected by admin."
            )

            # 📧 Email
            send_grievance_email.delay(
                subject="Complaint Rejected",
                message=f"""
Hello {grievance.user.username},

Your complaint '{grievance.title}' has been rejected.

Reason:
{reason}

Smart Grievance System
""",
                recipient_list=[grievance.user.email],
            )

            return

        # ======================================================
        # 🚀 AUTO ASSIGN OFFICER ON ESCALATION
        # ======================================================
        new_status = serializer.validated_data.get("status")

        if new_status == "escalated":

            if not serializer.instance.assigned_to:

                User = get_user_model()
                grievance_instance = serializer.instance

                dept = grievance_instance.department.first()

                if not dept:
                    raise ValidationError({
                        "error": "No department assigned to complaint"
                    })

                officer = User.objects.filter(
                    role__iexact="officer",
                    department__iexact=dept.name.strip()
                ).first()

                if not officer:
                    raise ValidationError({
                        "error": f"No officer found for department {dept.name}"
                    })

                serializer.instance.assigned_to = officer

        # ======================================================

        grievance = serializer.save()

        # 🔔 Notification
        create_notification.delay(
            grievance.user.id,
            f"Your grievance #{grievance.id} status changed to {grievance.status}"
        )

        # 📧 EMAIL: Department Assigned
        if grievance.department != old_department:
            send_grievance_email.delay(
                subject="Complaint Assigned to Department",
                message=f"""
Hello {grievance.user.username},

Your complaint '{grievance.title}' has been assigned to the {grievance.department} department.

Smart Grievance System
""",
                recipient_list=[grievance.user.email],
            )

        # 📧 EMAIL: Status Updated
        if grievance.status != old_status:
            send_grievance_email.delay(
                subject="Complaint Status Updated",
                message=f"""
Hello {grievance.user.username},

New Status: {grievance.status}
""",
                recipient_list=[grievance.user.email],
            )

        # 📧 EMAIL: Resolved
        if grievance.status.lower() == "resolved":
            send_grievance_email.delay(
                subject="Complaint Resolved",
                message=f"Your complaint '{grievance.title}' has been resolved.",
                recipient_list=[grievance.user.email],
            )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()

        return Response(
            {"message": "Grievance deleted successfully"},
            status=status.HTTP_200_OK
        )


# =========================================================
# 🆕 ESCALATED COMPLAINTS API
# =========================================================

class EscalatedComplaintsAPIView(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request):
        grievances = Grievance.objects.filter(status="escalated")

        data = []
        for g in grievances:
            data.append({
                "id": g.id,
                "title": g.title,
                "description": g.description,
                "priority": g.priority,
                "status": g.status,
                "officer": str(g.assigned_to) if g.assigned_to else None,
                "created_at": g.created_at,
            })

        return Response({
            "total_escalated": len(data),
            "complaints": data
        })


# =========================================================
# 🆕 TAKE ACTION ON OFFICER API
# =========================================================

class TakeActionOnOfficerAPIView(APIView):

    permission_classes = [IsAdminUser]

    def post(self, request, grievance_id):

        try:
            grievance = Grievance.objects.get(id=grievance_id)
        except Grievance.DoesNotExist:
            return Response({"error": "Complaint not found"}, status=404)

        if grievance.status != "escalated":
            return Response(
                {"error": "Only escalated complaints allowed"},
                status=400
            )

        officer = grievance.assigned_to

        if not officer:
            return Response({"error": "No officer assigned"}, status=400)

        action_type = request.data.get("action_type")
        reason = request.data.get("reason")

        OfficerAction.objects.create(
            grievance=grievance,
            officer=officer,
            action_type=action_type,
            reason=reason
        )

        if action_type == "WARNING":
            message = f"Warning sent to {officer}"

        elif action_type == "REASSIGN":
            grievance.assigned_to = None
            grievance.status = "pending"
            grievance.save()
            message = "Complaint reassigned successfully"

        else:
            return Response({"error": "Invalid action"}, status=400)

        return Response(
            {
                "message": message,
                "action": action_type
            },
            status=200
        )


# =========================================================
# 📊 MONTHLY REPORT
# =========================================================

class MonthlyReportView(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request):

        month = request.GET.get("month")
        year = request.GET.get("year")
        format_type = request.GET.get("type", "excel").lower()

        if not month or not year:
            return Response(
                {"error": "month and year are required"},
                status=400
            )

        month = int(month)
        year = int(year)

        grievances = Grievance.objects.filter(
            created_at__month=month,
            created_at__year=year
        )

        departments = ["water", "road", "garbage", "sewage", "light"]
        report_data = []

        for dept in departments:
            dept_grievances = grievances.filter(
                department__name__iexact=dept
            ).distinct()

            report_data.append({
                "department": dept.capitalize(),
                "total": dept_grievances.count(),
                "pending": dept_grievances.filter(status="pending").count(),
                "resolved": dept_grievances.filter(status="resolved").count(),
                "rejected": dept_grievances.filter(status="rejected").count(),
            })

        if format_type == "pdf":
            return self.generate_pdf(report_data, month, year)

        return self.generate_excel(report_data, month, year)

    def generate_excel(self, report_data, month, year):

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Monthly Report"

        ws.append(["Department", "Total", "Pending", "Resolved", "Rejected"])

        for row in report_data:
            ws.append([
                row["department"],
                row["total"],
                row["pending"],
                row["resolved"],
                row["rejected"],
            ])

        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        response["Content-Disposition"] = (
            f"attachment; filename=report_{month}_{year}.xlsx"
        )

        wb.save(response)
        return response

    def generate_pdf(self, report_data, month, year):

        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = (
            f"attachment; filename=report_{month}_{year}.pdf"
        )

        buffer = BytesIO()

        doc = SimpleDocTemplate(buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        elements = []

        elements.append(Paragraph("Smart Grievance System", styles["Title"]))
        elements.append(Spacer(1, 20))

        table_data = [["Department", "Total", "Pending", "Resolved", "Rejected"]]

        for row in report_data:
            table_data.append([
                row["department"],
                row["total"],
                row["pending"],
                row["resolved"],
                row["rejected"]
            ])

        table = Table(table_data)

        table.setStyle(TableStyle([
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ]))

        elements.append(table)

        doc.build(elements)

        pdf = buffer.getvalue()
        buffer.close()

        response.write(pdf)
        return response