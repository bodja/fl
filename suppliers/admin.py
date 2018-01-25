from django.contrib.auth.admin import sensitive_post_parameters_m
from django.contrib import admin, messages
from django.contrib.admin.options import IS_POPUP_VAR
from django.contrib.admin.utils import unquote
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import path, reverse
from django.utils.html import escape
from django.utils.translation import gettext, gettext_lazy as _

from .forms import SupplierChangeForm, SupplierCreationForm
from .models import Supplier, Customer, Product, Transaction


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    """
    Mostly taken from django.contrib.auth.admin.UserAdmin
    To be able to set a password
    """
    list_display = [
        'id',
        'title',
        'code',
    ]
    search_fields = (
        'title',
        'code'
    )

    form = SupplierChangeForm
    add_form = SupplierCreationForm
    change_password_form = AdminPasswordChangeForm

    def get_form(self, request, obj=None, **kwargs):
        """
        Use special form during supplier creation
        """
        defaults = {}
        if obj is None:
            defaults['form'] = self.add_form
        defaults.update(kwargs)
        return super().get_form(request, obj, **defaults)

    def get_urls(self):
        return [
                   path('<id>/password/', self.admin_site.admin_view(
                       self.supplier_change_password),
                        name='supplier_password_change'),
               ] + super().get_urls()

    @sensitive_post_parameters_m
    def supplier_change_password(self, request, id, form_url=''):
        if not self.has_change_permission(request):
            raise PermissionDenied
        supplier = self.get_object(request, unquote(id))
        if supplier is None:
            raise Http404(_(
                '%(name)s object with primary key %(key)r does not exist.') % {
                              'name': self.model._meta.verbose_name,
                              'key': escape(id),
                          })
        if request.method == 'POST':
            form = self.change_password_form(supplier, request.POST)
            if form.is_valid():
                form.save()
                change_message = self.construct_change_message(request, form,
                                                               None)
                self.log_change(request, supplier, change_message)
                msg = gettext('Password changed successfully.')
                messages.success(request, msg)
                return HttpResponseRedirect(
                    reverse('%s:%s_%s_change' % (
                        self.admin_site.name,
                        supplier._meta.app_label,
                        supplier._meta.model_name,
                    ), args=(supplier.pk, ))
                )
        else:
            form = self.change_password_form(supplier)

        fieldsets = [(None, {'fields': list(form.base_fields)})]
        adminForm = admin.helpers.AdminForm(form, fieldsets, {})

        context = {
            'title': _('Change password: %s') % escape(supplier.code),
            'adminForm': adminForm,
            'form_url': form_url,
            'form': form,
            'is_popup': (IS_POPUP_VAR in request.POST or
                         IS_POPUP_VAR in request.GET),
            'add': True,
            'change': False,
            'has_delete_permission': False,
            'has_change_permission': True,
            'has_absolute_url': False,
            'opts': self.model._meta,
            'original': supplier,
            'save_as': False,
            'show_save': True,
        }
        context.update(self.admin_site.each_context(request))

        request.current_app = self.admin_site.name

        return TemplateResponse(
            request,
            'admin/auth/user/change_password.html',
            context,
        )


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'title',
        'code',
    ]
    search_fields = (
        'title',
        'code',
        # 'address',
    )
    raw_id_fields = (
        'supplier',
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'title',
        'code',
    ]
    search_fields = (
        'title',
        'code',
    )
    raw_id_fields = (
        'supplier',
    )


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'customer_id',
        'product_id',
        'cost',
        'price',
        'quantity',
        'delivered',
        # 'stopped',
    ]
    raw_id_fields = (
        'customer',
        'product',
    )
