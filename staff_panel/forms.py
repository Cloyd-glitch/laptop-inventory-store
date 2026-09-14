from django import forms
from catalog.models import Laptop, Category, LaptopImage
from orders.models import Order, Booking
from payments.models import Payment
from accounts.models import User


class LaptopAdminForm(forms.ModelForm):
    class Meta:
        model = Laptop
        fields = [
            'brand', 'model_name', 'slug', 'category', 'condition',
            'processor', 'ram', 'storage', 'gpu', 'screen_size', 'operating_system',
            'price', 'stock_quantity', 'main_image', 'description', 'is_active',
        ]
        widgets = {
            'brand':            forms.TextInput(attrs={'class': 'sp-input', 'placeholder': 'e.g. Apple'}),
            'model_name':       forms.TextInput(attrs={'class': 'sp-input', 'placeholder': 'e.g. MacBook Pro 14'}),
            'slug':             forms.TextInput(attrs={'class': 'sp-input', 'placeholder': 'Auto-filled if blank'}),
            'category':         forms.Select(attrs={'class': 'sp-input'}),
            'condition':        forms.Select(attrs={'class': 'sp-input'}),
            'processor':        forms.TextInput(attrs={'class': 'sp-input', 'placeholder': 'e.g. Apple M3 Pro'}),
            'ram':              forms.TextInput(attrs={'class': 'sp-input', 'placeholder': 'e.g. 18GB LPDDR5'}),
            'storage':          forms.TextInput(attrs={'class': 'sp-input', 'placeholder': 'e.g. 512GB SSD'}),
            'gpu':              forms.TextInput(attrs={'class': 'sp-input', 'placeholder': 'e.g. 18-core GPU (optional)'}),
            'screen_size':      forms.TextInput(attrs={'class': 'sp-input', 'placeholder': 'e.g. 14.2 inch'}),
            'operating_system': forms.TextInput(attrs={'class': 'sp-input', 'placeholder': 'e.g. macOS Sequoia'}),
            'price':            forms.NumberInput(attrs={'class': 'sp-input', 'placeholder': '0.00', 'step': '0.01'}),
            'stock_quantity':   forms.NumberInput(attrs={'class': 'sp-input', 'min': '0'}),
            'description':      forms.Textarea(attrs={'class': 'sp-input', 'rows': 4}),
            'is_active':        forms.CheckboxInput(attrs={'class': 'sp-checkbox'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['slug'].required = False
        self.fields['main_image'].widget = forms.FileInput(attrs={'class': 'sp-file-input'})


class CategoryAdminForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'slug']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'sp-input', 'placeholder': 'Category name'}),
            'slug': forms.TextInput(attrs={'class': 'sp-input', 'placeholder': 'Auto-filled if blank'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['slug'].required = False


class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status', 'notes']
        widgets = {
            'status': forms.Select(attrs={'class': 'sp-input'}),
            'notes':  forms.Textarea(attrs={'class': 'sp-input', 'rows': 3}),
        }


class BookingStatusForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['status', 'notes']
        widgets = {
            'status': forms.Select(attrs={'class': 'sp-input'}),
            'notes':  forms.Textarea(attrs={'class': 'sp-input', 'rows': 3}),
        }

class UserAdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'avatar', 'first_name', 'last_name', 'username', 'email',
            'sex', 'bday', 'country', 'educational_background', 'role', 'is_active'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'sp-input'}),
            'last_name': forms.TextInput(attrs={'class': 'sp-input'}),
            'username': forms.TextInput(attrs={'class': 'sp-input'}),
            'email': forms.EmailInput(attrs={'class': 'sp-input'}),
            'sex': forms.TextInput(attrs={'class': 'sp-input', 'placeholder': 'e.g. Male, Female, Other'}),
            'bday': forms.DateInput(attrs={'class': 'sp-input', 'type': 'date'}),
            'country': forms.TextInput(attrs={'class': 'sp-input'}),
            'educational_background': forms.Textarea(attrs={'class': 'sp-input', 'rows': 3}),
            'role': forms.Select(attrs={'class': 'sp-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'sp-checkbox'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['avatar'].widget = forms.FileInput(attrs={'class': 'sp-file-input'})

