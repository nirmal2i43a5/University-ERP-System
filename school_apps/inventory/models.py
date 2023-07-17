from django.db import models
from django.db.models.fields import CharField, TextField, related
from student_management_app.models import CustomUser, Department, Branch
from django.utils import timezone
from django.core.exceptions import ValidationError

# Create your models here.

PROCUREMENT_STATUS = [
    ("pending", "Pending"),
    ("proc_approved", "Approved by procurement"),
    ("proc_rejected", "Rejected by procurement"),
    ("proc_pending", "Pending at procurement"),
    ("fin_approved", "Approved by finance"),
    ("fin_rejected", "Rejected by finance"),
    ("fin_pending", "Pending at finance"),
]

# ASSETS_CATEGORY=[
#     ('Electronics','Electronics'),
#     ('Furniture','Furniture'),
#     ('Stationaries','Stationaries')
# ]

DOCUMENT_TYPE = [
    ("quotation", "Quotation"),
    ("memo", "Memo"),
    ("p_order", "Purchase Order"),
]


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Assets(models.Model):
    name = models.CharField(max_length=255)
    details = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        permissions = (
            ("assets_assignment", "Can assign assets"),
            ("assets_return", "Can return assets"),
            ("assets_transfer", "Can transfer assets"),
        )

    def __str__(self):
        return self.name


class Vendor(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    contact_no = models.CharField(max_length=50)
    pan_number = models.CharField(max_length=50)
    vendor_documents = models.FileField(
        upload_to="inventory/vendor_doc", null=True, blank=True
    )

    def __str__(self):
        return self.name


class StatusOptions(models.Model):
    display_text = models.CharField(max_length=100)
    value = models.CharField(max_length=20)
    # goto_default = Branch.objects.get(name="Procurement").id
    goto_default = 1
    goto_branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        default=goto_default,
        related_name="status_gotodept",
    )
    current_branch = models.ForeignKey(
        Branch, on_delete=models.CASCADE, related_name="status_currentdept"
    )

    def __str__(self) -> str:
        return self.display_text


class ProcurementRequest(models.Model):
    requester = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="procurement_requester")
    requester_dept = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="procurement_dept",
        verbose_name="Department",
        null=True,
        blank=True,
    )
    requester_branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        verbose_name="Branch",
        related_name="requester_branch",
        null=True,
        blank=True,
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    item = models.ForeignKey(Assets, on_delete=models.CASCADE)
    amount = models.IntegerField()
    acquired = models.IntegerField(default=0)
    is_complete = models.BooleanField(default=False)
    requester_comment = models.TextField(null=True, blank=True)
    request_date = models.DateField(auto_now_add=True)

    # STATUS_DEFAULT = StatusOptions.objects.get(value='pending').id
    # STATUS_DEFAULT = 1
    # status = models.ForeignKey(StatusOptions, on_delete=models.CASCADE, default=STATUS_DEFAULT)
    procurement_personnel = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="procurement_personnel",
        null=True,
        blank=True,
        verbose_name="Latest action at Procurement dept. by: ",
    )
    finance_personnel = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="finance_personnel",
        null=True,
        blank=True,
        verbose_name="Latest action at Finance dept. by: ",
    )
    procurement_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Date of latest action at Procurement dept.: ",
    )
    finance_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Date of latest action at Finance dept.: ")
    procurement_comment = models.TextField(
        null=True, blank=True, verbose_name="Message from Procurement dept.: "
    )
    finance_comment = models.TextField(
        null=True, blank=True, verbose_name="Message from Procurement dept.: "
    )

    def clean(self):
        super(ProcurementRequest, self).clean()
        dept_exists = self.requester_dept is not None
        branch_exists = self.requester_branch is not None

        check = dept_exists ^ branch_exists
        if not check:
            raise ValidationError(
                "Only one of Branch or Department should be filled")

    def __str__(self) -> str:
        try:
            return (
                self.requester_dept.name
                + " - "
                + self.item.name
                + " ("
                + str(self.amount)
                + ")"
            )
        except BaseException:
            return (
                self.requester_branch.name
                + " - "
                + self.item.name
                + " ("
                + str(self.amount)
                + ")"
            )


class Transaction(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    procurement_order = models.ForeignKey(
        ProcurementRequest, on_delete=models.CASCADE, null=True, blank=True
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    item = models.ForeignKey(Assets, on_delete=models.CASCADE)
    amount = models.IntegerField()
    request_date = models.DateField()
    is_complete = models.BooleanField(default=False)
    completion_date = models.DateField(blank=True, null=True)

    def __str__(self) -> str:
        return self.vendor.name + " (" + str(self.request_date) + ")"


# class ProcurementStatus(models.Model):
#     procurement_request=models.ForeignKey(ProcurementRequest, on_delete=models.CASCADE)


class Document(models.Model):
    document_type = models.CharField(max_length=50, choices=DOCUMENT_TYPE)
    photo = models.FileField(
        upload_to="inventory/documents",
        null=True,
        blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    uploaded_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)


class Item(models.Model):
    id_no = models.CharField(max_length=50, unique=True, verbose_name="ID")
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name="Category",
        related_name="item_category",
    )
    item_type = models.ForeignKey(
        Assets,
        on_delete=models.CASCADE,
        verbose_name="Type",
        related_name="item_type")
    details = models.TextField(blank=True, null=True)
    source_transaction = models.ForeignKey(
        Transaction,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="source_transaction",
    )
    current_department = models.ForeignKey(
        Department, on_delete=models.CASCADE, null=True, blank=True
    )
    current_branch = models.ForeignKey(
        Branch, on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self) -> str:
        return self.id_no + " " + self.item_type.name


class assets_transfer(models.Model):
    from_dept = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="assets_transfer_from",
        null=True,
        blank=True,
    )
    from_branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        related_name="assets_transfer_from_branch",
        null=True,
        blank=True,
    )
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    to_dept = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="assets_transfer_to",
        null=True,
        blank=True,
    )
    to_branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        related_name="assets_transfer_to_branch",
        null=True,
        blank=True,
    )
    overseer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    transfer_date = models.DateField(auto_now_add=True)

    # def clean(self):
    #     super(ProcurementRequest, self).clean()
    #     from_dept_exists = self.from_dept != None
    #     from_branch_exists = self.from_branch != None

    #     to_dept_exists = self.to_dept != None
    #     to_branch_exists = self.to_branch != None

    #     from_check = from_dept_exists^from_branch_exists
    #     to_check = to_dept_exists^to_branch_exists
    #     if not (from_check):
    #         raise ValidationError('Source Department or Branch error')

    #     if not(to_check):
    #         raise ValidationError('Destination Department or Branch error')


class transaction_items(models.Model):
    transaction = models.ForeignKey(
        Transaction,
        on_delete=models.CASCADE,
        related_name="unregistered_transaction")
    item_type = models.ForeignKey(
        Assets, on_delete=models.CASCADE, related_name="unregistered_item_type"
    )
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name="unregistered_item",
        null=True,
        blank=True,
    )
    is_registered = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.item_type.name


class RepairRequest(models.Model):
    REPAIR_STATUS = [
        ("pending", "Pending"),
        ("fin_approved", "Approved by finance"),
        ("fin_rejected", "Rejected by finance"),
        ("fin_pending", "Pending at finance"),
        ("under_maint", "Under Repair"),
        ("complete", "Complete"),
    ]
    requester = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="repair_requester"
    )
    requester_dept = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="repair_requester_dept",
        verbose_name="Department",
        null=True,
        blank=True,
    )
    requester_branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        verbose_name="Branch",
        related_name="repair_requester_branch",
        null=True,
        blank=True,
    )
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name="repair_item")
    is_complete = models.BooleanField(default=False)
    requester_comment = models.TextField(null=True, blank=True)
    request_date = models.DateField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=REPAIR_STATUS,
        default="pending")
    finance_personnel = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="finance_personnel_repair",
        null=True,
        blank=True,
        verbose_name="Latest action at Finance dept. by: ",
    )
    finance_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Date of latest action at Finance dept.: ")
    finance_comment = models.TextField(
        null=True, blank=True, verbose_name="Message from Procurement dept.: "
    )
