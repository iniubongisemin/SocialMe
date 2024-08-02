from django.db.models import TextChoices


# Create your enumeration type(s) here.
class NotificationTypes(TextChoices):
    HR_MANAGEMENT = "HR_MANAGEMENT", "HR_MANAGEMENT"
    SALES = "SALES", "SALES"
    SPEND_MANAGEMENT = "SPEND_MANAGEMENT", "SPEND_MANAGEMENT"
    STOCK = "STOCK", "STOCK"


class TeamType(TextChoices):
    PAYROLL = "PAYROLL", "PAYROLL"
    SALES = "SALES", "SALES"
    SPEND_MGMT = "SPEND_MGMT", "SPEND_MGMT"
    STOCK = "STOCK", "STOCK"


class TeamType(TextChoices):
    PAYROLL = "PAYROLL", "PAYROLL"
    SALES = "SALES", "SALES"
    SPEND_MGMT = "SPEND_MGMT", "SPEND_MGMT"
    STOCK = "STOCK", "STOCK"


class UserRole(TextChoices):
    ADMIN = "ADMIN", "ADMIN"
    SALES_LEAD = "SALES_LEAD", "SALES_LEAD"
    MEMBER = "MEMBER", "MEMBER"
    OWNER = "OWNER", "OWNER"
    SALES_OFFICER = "SALES_OFFICER", "SALES_OFFICER"


class UserStatus(TextChoices):
    ACTIVE = "ACTIVE", "ACTIVE"
    NOT_JOINED = "NOT_JOINED", "NOT_JOINED"
    SUSPENDED = "SUSPENDED", "SUSPENDED"