from django.contrib import admin
from .models import *

# Register your models here.

# admin.site.register(Member)
admin.site.register(Issue)
admin.site.register(Return)
admin.site.register(Category)
admin.site.register(BookEntry)
admin.site.register(BookIssue)
admin.site.register(BookReturn)
admin.site.register(BookRenew)
admin.site.register(Barcode)


# @admin.register(BookEntry)
class BookEntry(admin.ModelAdmin):
    list_display = ["name", "email", "subject", "message"]
