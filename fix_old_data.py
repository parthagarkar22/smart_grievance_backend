from apps.grievances.models import Grievance
from django.contrib.auth import get_user_model

User = get_user_model()

grievances = Grievance.objects.filter(
    status="escalated",
    assigned_to__isnull=True
)

fixed = 0
skipped = 0

for g in grievances:
    dept = g.department.first()

    if not dept:
        print(f"Skipped {g.id} → No department")
        skipped += 1
        continue

    officer = User.objects.filter(
        role__iexact="officer",
        department__icontains=dept.name.strip()
    ).first()

    if officer:
        g.assigned_to = officer
        g.save()
        print(f"Assigned {g.id} → {officer.username}")
        fixed += 1
    else:
        print(f"Skipped {g.id} → No officer for {dept.name}")
        skipped += 1

print("\n✅ FIXED:", fixed)
print("❌ SKIPPED:", skipped)