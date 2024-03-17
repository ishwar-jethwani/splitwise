from django.contrib import admin

from .models import (
    MemberUser,
    Profile,
    Expense,
    Transaction,
    Split,
)
admin.site.register((
    MemberUser,
    Profile,
    Expense,
    Transaction,
    Split,
))
# Register your models here.
