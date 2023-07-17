from os import name
from django.urls import path
from .views import *
from student_management_system.views import asset_home

app_name = "inventory"

urlpatterns = [
    path(
        "add_category/",
        CategoryCreateView.as_view(),
        name="create_category"),
    path("add_assets/", AssetsCreateView.as_view(), name="create_asset"),
    path("add_item/", ItemCreateView.as_view(), name="create_item"),
    path("add_vendor/", VendorCreateView.as_view(), name="create_vendor"),
    path("inventory/", AssetsListView.as_view(), name="inventory_list"),
    path("vendors/", VendorListView.as_view(), name="vendor_list"),
    path("category/", CategoryListView.as_view(), name="category_list"),
    path(
        "transfer_history/",
        TransferListView.as_view(),
        name="transfer_history"),
    path("items/", ItemsListView.as_view(), name="item_list"),
    path(
        "assets_assignment/",
        assets_department_assignment,
        name="assets_department_assignment",
    ),
    path("assets_transfer/", assets_dept_transfer, name="assets_transfer"),
    path("assignment_list/<str:pk>", assignment_list, name="assignment_list"),
    path("assets_return/", assets_return, name="assets_return"),
    # Procurement
    path(
        "create_procurement_request/",
        CreateProcurementRequest.as_view(),
        name="create_procurement_request",
    ),
    path(
        "procurement_requests/",
        ProcurementRequestListView.as_view(),
        name="procurement_list",
    ),
    path("procurement_status/", change_status, name="change_status"),
    path(
        "procurement_details/<str:pk>", procurement_details, name="procurement_details"
    ),
    # Transaction
    path(
        "add_transaction/", TransactionCreateView.as_view(), name="create_transaction"
    ),
    path(
        "transactions/",
        TransactionListView.as_view(),
        name="transaction_list"),
    # path('transaction_complete/', transaction_complete, name='transaction_complete'),
    # Repair
    path("add_repair/", RepairCreateView.as_view(), name="create_repair"),
    path("repairs/", RepairListView.as_view(), name="repair_list"),
    path("repair_status/", change_repair_status, name="change_repair_status"),
    # Ajax
    path("ajax/get_item_list", get_items_ajax, name="get_items_ajax"),
    path(
        "ajax/get_item_details", get_items_details_ajax, name="get_items_details_ajax"
    ),
    path(
        "ajax/get_dept_amount",
        get_dept_amount_ajax,
        name="get_dept_amount_ajax"),
    path(
        "ajax/get_dept_assets",
        get_dept_assets_ajax,
        name="get_dept_assets_ajax"),
    path(
        "ajax/get_branch_assets", get_branch_assets_ajax, name="get_branch_assets_ajax"
    ),
    path("ajax/show_modal", show_modal, name="show_modal"),
    path(
        "ajax/register_new_inventory_ajax",
        register_new_inventory_ajax,
        name="register_new_inventory_ajax",
    ),
    path(
        "ajax/transaction_register_item",
        transaction_register_item,
        name="transaction_register_item",
    ),
    path(
        "asset-management/",
        asset_home,
        name="asset-management"),
    # for sidebar
]
