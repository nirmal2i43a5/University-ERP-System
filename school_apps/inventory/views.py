import datetime
from student_management_app.models import AdminUser, CertificateTemplate, ExtraUser
from django import forms
from django.http.response import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from .models import *
from .forms import *
from django.contrib import messages
from django.urls import reverse
from django.db.models import Q
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required


# Create your views here.
# @permission_required('inventory.add_assets', raise_exception=True)
class AssetsCreateView(PermissionRequiredMixin, CreateView):
    permission_required = "inventory.add_assets"

    def get(self, request, *args, **kwargs):
        context = {"title": "Add Assets", "form": AssetsCreateForm()}
        return render(request, "inventory/add_form.html", context=context)

    def post(self, request, *args, **kwargs):
        form = AssetsCreateForm(request.POST)
        if form.is_valid():
            asset = form.save()
            asset.save()
            messages.success(request, "Item added.")
            return HttpResponseRedirect(reverse("inventory:inventory_list"))


class VendorCreateView(PermissionRequiredMixin, CreateView):
    permission_required = "inventory.add_vendor"

    def get(self, request, *args, **kwargs):
        context = {"title": "Add Vendor", "form": VendorCreateForm()}
        return render(request, "inventory/add_form.html", context=context)

    def post(self, request, *args, **kwargs):
        form = VendorCreateForm(request.POST)
        if form.is_valid():
            vendor = form.save()
            vendor.save()
            messages.success(request, "Vendor added.")
            return HttpResponseRedirect(reverse("inventory:vendor_list"))


class CategoryCreateView(PermissionRequiredMixin, CreateView):
    permission_required = "inventory.add_category"

    def get(self, request, *args, **kwargs):
        context = {"title": "Add Category", "form": CategoryCreateForm()}
        return render(request, "inventory/add_form.html", context=context)

    def post(self, request, *args, **kwargs):
        form = CategoryCreateForm(request.POST)
        if form.is_valid():
            category = form.save()
            category.save()
            messages.success(request, "Category added.")
            return HttpResponseRedirect(reverse("inventory:category_list"))


class ItemCreateView(PermissionRequiredMixin, CreateView):
    permission_required = "inventory.add_item"

    def get(self, request, *args, **kwargs):
        context = {"title": "Add Assets", "form": ItemCreateForm()}
        return render(request, "inventory/add_item.html", context=context)

    def post(self, request, *args, **kwargs):
        form = ItemCreateForm(request.POST)
        if form.is_valid():
            asset = form.save()
            asset.save()
            messages.success(request, "Item added.")
            return HttpResponseRedirect(reverse("inventory:inventory_list"))


class AssetsListView(PermissionRequiredMixin, ListView):
    permission_required = "inventory.view_assets"

    def get(self, request, *args, **kwargs):
        inventory = Assets.objects.all()
        inventory_assets = Item.objects.values_list("item_type", flat=True)
        inventory_count = []

        print(set(inventory_assets))
        for item in set(inventory_assets):
            item_list = Item.objects.filter(
                item_type=Assets.objects.get(pk=item))
            amount = item_list.count()
            inventory_count.append(amount)

        zipped = zip(inventory, inventory_count)
        context = {"zipped": zipped}
        return render(request, "inventory/inventory_list.html", context)


class TransferListView(PermissionRequiredMixin, ListView):
    permission_required = "inventory.view_assets_transfer"

    model = assets_transfer
    context_object_name = "assets_transfer"
    template_name = "inventory/transfer_history.html"


class CategoryListView(PermissionRequiredMixin, ListView):
    permission_required = "inventory.view_category"

    model = Category
    context_object_name = "category"
    template_name = "inventory/category_list.html"


class ItemsListView(PermissionRequiredMixin, ListView):
    permission_required = "inventory.view_item"
    model = Item
    context_object_name = "items"
    template_name = "inventory/item_list.html"


class VendorListView(PermissionRequiredMixin, ListView):
    permission_required = "inventory.view_vendor"
    model = Vendor
    context_object_name = "vendor"
    template_name = "inventory/vendor_list.html"


def assignment_list(request, pk):
    item = Assets.objects.get(pk=pk)
    # assignments = Item.objects.filter(Q(item_type=item), (~Q(current_department=None) | ~Q(current_branch=None)))
    assignments = Item.objects.filter(Q(item_type=item))
    assignments_count = assignments.count()
    # total = Item.objects.filter
    return render(
        request,
        "inventory/assignment_list.html",
        {"assets": assignments, "item": item, "count": assignments_count},
    )


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Assets Assignment~~~~~~~~~~~~~~~~~~~~~~~~
@permission_required("inventory.assets_assignment", raise_exception=True)
def assets_department_assignment(request):
    category = Category.objects.all()
    department = Department.objects.all()
    branch = Branch.objects.all()

    context = {
        "category": category,
        "department": department,
        "branch": branch}

    if request.method == "GET":
        return render(
            request,
            "inventory/assets_assignment.html",
            context=context)
    else:
        item = Item.objects.get(pk=request.POST["item"])
        department = Department.objects.get(pk=request.POST["department"])
        item.current_department = department
        item.save()

        assets_transfer.objects.create(
            from_dept=Department.objects.none(),
            to_dept=department,
            item=item,
            overseer=request.user,
        )

        msg_text = "{item} assigned to {department}."
        messages.success(
            request, msg_text.format(item=item, department=department.name)
        )
        return HttpResponseRedirect(reverse("inventory:inventory_list"))


@permission_required("inventory.assets_return", raise_exception=True)
def assets_return(request):
    item = Item.objects.get(pk=request.POST["item"])
    item.current_department = None
    item.current_branch = None
    item.save()

    msg_string = "{item} returned to inventory."
    messages.success(request, msg_string.format(item=item))
    return HttpResponseRedirect(reverse("inventory:inventory_list"))


def get_items_ajax(request):
    category = Category.objects.get(pk=request.GET["category"])
    item = Assets.objects.filter(category=category)

    context = {"items": item}
    return render(request, "ajax/item_list.html", context=context)


def get_items_details_ajax(request):
    item_type = Assets.objects.get(pk=request.GET["item"])
    items = Item.objects.filter(Q(item_type=item_type), Q(
        current_department=None), Q(current_branch=None))

    context = {"items": items}
    return render(request, "ajax/item_list.html", context=context)


def get_dept_amount_ajax(request):
    department = Department.objects.get(pk=request.GET["department"])
    item = Assets.objects.get(pk=request.GET["item"])

    try:
        amount = assets_assignment.objects.get(
            department=department, item=item).amount
    except BaseException:
        amount = 0
    # print('amount:',amount)
    return JsonResponse({"amount": amount})


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Assets Transfer~~~~~~~~~~~~~~~~~~~~~~~~~~
@permission_required("inventory.assets_transfer", raise_exception=True)
def assets_dept_transfer(request):
    department = Department.objects.all()

    context = {"department": department, "branch": Branch.objects.all()}
    if request.method == "GET":
        return render(
            request,
            "inventory/assets_transfer.html",
            context=context)
    else:
        destination = request.POST["destination"]
        source = request.POST["source"]

        item = Item.objects.get(pk=request.POST["item"])

        if source == "department":
            from_dept = Department.objects.get(pk=request.POST["from_dept"])
            print(from_dept)
        else:
            from_branch = Branch.objects.get(pk=request.POST["from_branch"])
            print(from_branch)

        if destination == "department":
            to_dept = Department.objects.get(pk=request.POST["to_dept"])
            item.current_department = to_dept
            item.current_branch = None
            item.save()
        else:
            to_branch = Branch.objects.get(pk=request.POST["to_branch"])
            print(to_branch)
            item.current_branch = to_branch
            item.current_department = None
            item.save()

        try:
            print("try1")
            assets_transfer.objects.create(
                from_dept=from_dept,
                to_dept=to_dept,
                item=item,
                overseer=request.user)
        except BaseException:
            try:
                print("try2")
                assets_transfer.objects.create(
                    from_dept=from_dept,
                    to_branch=to_branch,
                    item=item,
                    overseer=request.user,
                )
            except BaseException:
                try:
                    print("try3")
                    assets_transfer.objects.create(
                        from_branch=from_branch,
                        to_branch=to_branch,
                        item=item,
                        overseer=request.user,
                    )
                except BaseException:
                    try:
                        print("try4")
                        assets_transfer.objects.create(
                            from_branch=from_branch,
                            to_dept=to_dept,
                            item=item,
                            overseer=request.user,
                        )
                    except BaseException:
                        print("How did we get here\n")

        msg_string = "{item} transfer successful."
        messages.success(
            request,
            msg_string.format(
                item=item,
            ),
        )
        return HttpResponseRedirect(reverse("inventory:inventory_list"))


def get_dept_assets_ajax(request):
    department = Department.objects.get(pk=request.GET["department"])
    items = Item.objects.filter(Q(current_department=department))

    return render(
        request,
        "ajax/dept_item_list.html",
        context={
            "items": items})


def get_branch_assets_ajax(request):
    department = Branch.objects.get(pk=request.GET["branch"])
    items = Item.objects.filter(Q(current_branch=department))

    return render(
        request,
        "ajax/dept_item_list.html",
        context={
            "items": items})


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Procurement~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class ProcurementRequestListView(PermissionRequiredMixin, ListView):
    permission_required = "inventory.view_procurementrequest"

    def get(self, request, *args, **kwargs):
        procurement = ProcurementRequest.objects.all()
        try:
            print(request.user)
            user = AdminUser.objects.get(admin_user=request.user)
            department = Branch.objects.get(name="Administration")
            exempt = True
        except BaseException:
            user = ExtraUser.objects.get(extra_user=request.user)
            department = user.branch
            exempt = False

        context = {
            "procurement": procurement,
            "department": department,
            "exempt": exempt,
        }

        return render(
            request,
            "procurement/procurement_list.html",
            context=context)


class CreateProcurementRequest(PermissionRequiredMixin, CreateView):
    permission_required = "inventory.add_procurementrequest"

    def get(self, request, *args, **kwargs):
        procurement_form = ProcurementRequestCreateForm()
        context = {"form": ProcurementRequestCreateForm}
        return render(
            request,
            "procurement/create_procurement_request.html",
            context=context)

    def post(self, request, *args, **kwargs):
        form = ProcurementRequestCreateForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.requester = request.user
            # print(type(request.user))
            # print('\n')
            obj.save()

            msg_string = "Procurement request for {item} created."
            messages.success(request, msg_string.format(item=obj.item))
            return HttpResponseRedirect(
                reverse("inventory:create_procurement_request"))
        else:
            messages.error(request, list(form.errors))
            return HttpResponseRedirect(
                reverse("inventory:create_procurement_request"))


def show_modal(request):
    procurement_object = ProcurementRequest.objects.get(pk=request.GET["id"])
    status = StatusOptions.objects.all()

    exempt = check_exempt(request)
    if exempt:
        department = Branch.objects.get(name="Administration")
    else:
        user = ExtraUser.objects.get(extra_user=request.user)
        department = user.branch

    context = {
        "obj": procurement_object,
        "exempt": exempt,
        "status": status,
        "department": department,
    }

    return render(request, "procurement/procurement_modal_body.html", context)


def change_status(request):
    procurement_object = ProcurementRequest.objects.get(pk=request.GET["id"])
    status = StatusOptions.objects.get(value=request.GET["status"])
    print(status.value, "\n")
    comment = request.GET["comment"]

    procurement_object.status = status

    if status.value == "complete":
        procurement_object.is_complete = True

    if "proc" in status.value:
        print("in proc")
        procurement_object.procurement_personnel = request.user
        procurement_object.procurement_date = datetime.datetime.today()
        procurement_object.procurement_comment = comment
    if "fin" in status.value:
        print("in finance")
        procurement_object.finance_personnel = request.user
        procurement_object.finance_date = datetime.datetime.today()
        procurement_object.finance_comment = comment
    procurement_object.save()

    messages.success(request, "Status change successful.")
    return HttpResponseRedirect(reverse("inventory:procurement_list"))


def procurement_details(request, pk):
    procurement_obj = ProcurementRequest.objects.get(pk=pk)

    context = {"object": procurement_obj}
    return render(request, "procurement/procurement_details.html", context)


def check_exempt(request):
    try:
        user = AdminUser.objects.get(admin_user=request.user)
        exempt = True
    except BaseException:
        user = ExtraUser.objects.get(extra_user=request.user)
        exempt = False

    return exempt


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Transaction~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class TransactionCreateView(PermissionRequiredMixin, CreateView):
    permission_required = "inventory.add_transaction"

    def get(self, request, *args, **kwargs):
        context = {
            "title": "Add Transaction Record",
            "form": TransactionCreateForm()}
        return render(
            request,
            "transaction/create_transaction_record.html",
            context=context)

    def post(self, request, *args, **kwargs):
        form = TransactionCreateForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data["amount"]
            item_type = form.cleaned_data["item"]

            transaction = form.save()
            transaction.save()

            for i in range(0, amount):
                transaction_items.objects.create(
                    transaction=transaction,
                    item_type=item_type,
                )

            messages.success(request, "Transaction record added.")
            return HttpResponseRedirect(reverse("inventory:transaction_list"))
        else:
            messages.error(request, list(form.errors))
            return HttpResponseRedirect(
                reverse("inventory:create_transaction"))


class TransactionListView(PermissionRequiredMixin, ListView):
    permission_required = "inventory.view_transaction"

    def get(self, request, *args, **kwargs):
        transaction = Transaction.objects.all()
        context = {"transaction": transaction}

        return render(request, "transaction/transaction_list.html", context)

    def post(self, request, *args, **kwargs):
        transaction = Transaction.objects.get(pk=request.POST["transaction"])
        transaction.is_complete = True
        transaction.completion_date = datetime.datetime.today()
        transaction.save()

        transaction = Transaction.objects.all()
        context = {"transaction": transaction}

        messages.success(
            request,
            "Transaction completed. Please registered newly acquired items to inventory.",
        )
        return render(request, "transaction/transaction_list.html", context)


def register_new_inventory_ajax(request):
    print("Here")
    transaction = Transaction.objects.get(pk=request.GET["id"])
    items_transaction = transaction_items.objects.filter(
        transaction=transaction)
    department = Department.objects.all()
    branch = Branch.objects.all()
    print(items_transaction, "\n")

    context = {
        "transaction_item": items_transaction,
        "department": department,
        "branch": branch,
    }

    return render(
        request,
        "transaction/register_item_modal_body.html",
        context)


def transaction_register_item(request):
    new_item = transaction_items.objects.get(pk=request.GET["transaction_id"])
    destination = request.GET["destination"]
    item_id = request.GET["item_id"]

    if destination == "department":
        department = Department.objects.get(pk=request.GET["dept_id"])
        to_create = Item.objects.create(
            id_no=item_id,
            item_type=new_item.item_type,
            category=new_item.item_type.category,
            current_department=department,
            source_transaction=new_item.transaction,
        )
    elif destination == "branch":
        branch = Branch.objects.get(pk=request.GET["dept_id"])
        to_create = Item.objects.create(
            id_no=item_id,
            item_type=new_item.item_type,
            category=new_item.item_type.category,
            current_branch=branch,
            source_transaction=new_item.transaction,
        )
    else:
        to_create = Item.objects.create(
            id_no=item_id,
            item_type=new_item.item_type,
            category=new_item.item_type.category,
            source_transaction=new_item.transaction,
        )

    new_item.item = to_create
    new_item.is_registered = True
    new_item.save()

    return JsonResponse({"success": "True"})


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Repair~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class RepairCreateView(CreateView):
    def get(self, request, *args, **kwargs):
        try:
            user = AdminUser.objects.get(admin_user=request.user)
            department = Branch.objects.get(name="Administration")
            items = Item.objects.filter(current_branch=department)
        except BaseException:
            user = ExtraUser.objects.get(extra_user=request.user)
            department = user.branch
            try:
                items = Item.objects.filter(current_branch=department)
            except BaseException:
                items = Item.objects.filter(current_department=department)

        form = RepairCreateForm()
        form.fields["item"].queryset = items
        context = {"title": "Repair Request", "form": form}
        return render(request, "repair/repair_form.html", context=context)

    def post(self, request, *args, **kwargs):
        form = RepairCreateForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.requester = request.user
            obj.save()
            messages.success(request, "Repair request added.")
            return HttpResponseRedirect(reverse("inventory:repair_list"))


class RepairListView(ListView):
    model = RepairRequest
    context_object_name = "repair"
    template_name = "repair/repair_list.html"


def change_repair_status(request):
    new_status = request.GET["status"]
    repair = RepairRequest.objects.get(pk=request.GET["id"])

    repair.status = new_status
    repair.save()

    messages.success(request, "Status changed.")
    return HttpResponseRedirect(reverse("inventory:repair_list"))
