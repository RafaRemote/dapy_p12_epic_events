from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .forms import EpicUserChangeForm, EpicUserCreationForm
from users.models import EpicUser


class EpicUserAdmin(BaseUserAdmin):
    form = EpicUserChangeForm
    add_form = EpicUserCreationForm
    list_display = ("username", "role", "is_staff", "is_admin", "is_superuser")
    list_filter = ("is_admin", "role", "groups")
    fieldsets = ((None, {"fields": ("username", "role")}),)
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "role", "password1", "password2"),
            },
        ),
    )
    search_fields = ("username",)
    ordering = ("username",)
    filter_horizontal = ()


class GroupsAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


admin.site.register(EpicUser, EpicUserAdmin)
admin.site.unregister(Group)
admin.site.register(Group, GroupsAdmin)


# can_add_account = Permission.objects.get(name="Can add account")
# can_add_event = Permission.objects.get(name="Can add event")

# epicuser = EpicUser.object.get(all)


# sales_team_permission = [
#     can_add_account,
#     can_add_event
# ]

# for perm in sales_team_permission:
#     sales_team.permissions.add(perm)
