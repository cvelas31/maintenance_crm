from django.forms import ModelForm, Textarea
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import Customer, Order, OrderComments


class ReadOnlyFieldsMixin(object):
    readonly_fields = ()

    def __init__(self, *args, **kwargs):
        super(ReadOnlyFieldsMixin, self).__init__(*args, **kwargs)
        for field in (field for name, field in self.fields.items() if name in self.readonly_fields):
            field.widget.attrs['disabled'] = 'true'
            field.required = False

    def clean(self):
        cleaned_data = super(ReadOnlyFieldsMixin, self).clean()
        for field in self.readonly_fields:
            cleaned_data[field] = getattr(self.instance, field)
        return cleaned_data


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user']


class CreateOrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['customer', 'status', 'date_closed']
        widgets = {
            'descripcion': Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super(CreateOrderForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class UpdateImageForm(forms.Form):
    images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True,
                                                                    "accept": 'image/*'}))

    def __init__(self, *args, **kwargs):
        super(UpdateImageForm, self).__init__(*args, **kwargs)
        self.fields['images'].required = False
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class UpdateVideoForm(forms.Form):
    videos = forms.FileField(widget=forms.ClearableFileInput(
        attrs={
            "accept": 'video/*'}))

    def __init__(self, *args, **kwargs):
        super(UpdateVideoForm, self).__init__(*args, **kwargs)
        self.fields['videos'].required = False
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class UpdateOrderForm(ReadOnlyFieldsMixin, ModelForm):
    readonly_fields = ('customer', 'descripcion', 'title', 'equipo')

    class Meta:
        model = Order
        fields = '__all__'
        widgets = {
            'descripcion': Textarea(attrs={'rows': 4, 'readonly': True}),
        }

    def __init__(self, *args, **kwargs):
        super(UpdateOrderForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CreateOrderCommentForm(ModelForm):
    class Meta:
        model = OrderComments
        fields = '__all__'
        exclude = ['order', 'author', 'date_created']
        widgets = {
            'descripcion': Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super(CreateOrderCommentForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
