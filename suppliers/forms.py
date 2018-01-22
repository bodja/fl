from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import gettext_lazy as _

from suppliers.models import Supplier


class SupplierCreationForm(forms.ModelForm):
    """
    Mostly taken from django.contrib.auth.forms.UserCreationForm
    To be able to set a password
    """
    error_messages = {
        'password_mismatch': _('The two password fields didn\'t match.'),
    }
    password1 = forms.CharField(
        label=_('Password'),
        strip=False,
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_('Password confirmation'),
        widget=forms.PasswordInput,
        strip=False,
        help_text=_('Enter the same password as before, for verification.'),
    )

    class Meta:
        model = Supplier
        fields = ('code', 'title')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs.update(
                {'autofocus': True})

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get('password2')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error('password2', error)

    def save(self, commit=True):
        supplier = super().save(commit=False)
        supplier.set_password(self.cleaned_data['password1'])
        if commit:
            supplier.save()
        return supplier


class SupplierChangeForm(forms.ModelForm):
    """
    Mostly taken from django.contrib.auth.forms.UserChangeForm
    To be able to set a password
    """
    password = ReadOnlyPasswordHashField(
        label=_('Password'),
        help_text=_(
            'Raw passwords are not stored, so there is no way to see this '
            'supplier\'s password, but you can change the password using '
            '<a href=\'{}\'>this form</a>.'
        ),
    )

    class Meta:
        model = Supplier
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].help_text = self.fields['password'].help_text.format('../password/')

    def clean_password(self):
        # Regardless of what the supplier provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial['password']
