from django import forms
from django.contrib import admin

from dal import autocomplete
from import_export import fields
from import_export.resources import ModelResource

from mozillians.api.models import APIv2App
from mozillians.common.mixins import MozilliansAdminExportMixin


class APIv2AppResource(ModelResource):
    """APIv2App admin export resource."""
    email = fields.Field(attribute='owner__email')

    class Meta:
        model = APIv2App


class APIv2AppForm(forms.ModelForm):

    class Meta:
        model = APIv2App
        fields = ('__all__')
        widgets = {
            'owner': autocomplete.ModelSelect2(url='api-v2-autocomplete')
        }


class APIv2AppAdmin(MozilliansAdminExportMixin, admin.ModelAdmin):
    """APIv2App Admin."""
    list_display = ['name', 'owner', 'owner_email', 'privacy_level', 'enabled', 'last_used']
    list_filter = ['privacy_level', 'enabled']
    search_fields = ['name', 'key', 'owner__user__username']
    readonly_fields = ['last_used', 'created']

    def owner_email(self, obj):
        return obj.owner.email

    owner_email.admin_order_field = 'owner__user__email'
    owner_email.short_description = 'Email'

    form = APIv2AppForm
    resource_class = APIv2AppResource

    fieldsets = (
        ('Status', {
            'fields': ('enabled',),
        }),
        (None, {
            'fields': ('name', 'description', 'url', 'owner', 'privacy_level'),
        }),
        ('Important dates', {
            'fields': ('created', 'last_used')
        }),
        ('Key', {
            'fields': ('key',),
            'classes': ('collapse',)
        }),
    )


admin.site.register(APIv2App, APIv2AppAdmin)
