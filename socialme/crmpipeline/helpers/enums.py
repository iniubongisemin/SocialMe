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
    DISBURSER = "DISBURSER", "DISBURSER"
    MANAGER = "MANAGER", "MANAGER"
    MEMBER = "MEMBER", "MEMBER"
    OWNER = "OWNER", "OWNER"
    REVIEWER = "REVIEWER", "REVIEWER"
    SALES_MAN = "SALES_MAN", "SALES_MAN"
    SUB_ADMIN = "SUB_ADMIN", "SUB_ADMIN"
    SUPERVISOR = "SUPERVISOR", "SUPERVISOR"


class UserStatus(TextChoices):
    ACTIVE = "ACTIVE", "ACTIVE"
    NOT_JOINED = "NOT_JOINED", "NOT_JOINED"
    SUSPENDED = "SUSPENDED", "SUSPENDED"