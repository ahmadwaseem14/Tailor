# forms.py
from django import forms
from .models import Subscriber


class SubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['email']
class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Name'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    phone = forms.CharField(max_length=15, required=True, widget=forms.TextInput(attrs={'placeholder': 'Phone'}))
    subject = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Subject'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Message', 'cols': 30, 'rows': 10}))
    # forms.py
from django import forms



from django import forms
from .models import Button

from django.forms.widgets import Textarea

class JSONFieldWidget(Textarea):
    def render(self, name, value, attrs=None, renderer=None):
        # Render the JSON field as a text area
        return super().render(name, value, attrs, renderer)

class DynamicSpecificationAdminForm(forms.ModelForm):
    specifications = forms.JSONField(widget=JSONFieldWidget, required=False)

    class Meta:
        model = Button
        fields = ['name', 'description', 'price', 'original_price', 'image', 'video']
from django import forms
from .models import Button

class DynamicSpecificationForm(forms.ModelForm):
    class Meta:
        model = Button
        fields = ['name', 'description', 'price', 'original_price', 'image', 'video', 'in_stock']  # Include the static fields
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Initialize an empty list of specifications for dynamic form generation
        self.specification_count = len(self.initial.get('specifications', []))
        self.specifications = self.initial.get('specifications', [])

        # Dynamically generate spec fields (Title and Value)
        for i in range(self.specification_count):
            self.fields[f'spec_title_{i}'] = forms.CharField(
                label=f'Spec Title {i+1}',
                required=False,
                initial=self.specifications[i].get('title', '')  # Set initial value if available
            )
            self.fields[f'spec_value_{i}'] = forms.CharField(
                label=f'Spec Value {i+1}',
                required=False,
                initial=self.specifications[i].get('value', '')  # Set initial value if available
            )
        
        # Add a button to add new specification fields
        self.fields['new_specification'] = forms.CharField(
            widget=forms.HiddenInput(),
            required=False
        )

    def clean_specifications(self):
        # Convert the input into a list of dicts with 'title' and 'value'
        specifications = []
        for i in range(self.specification_count):
            title = self.cleaned_data.get(f'spec_title_{i}')
            value = self.cleaned_data.get(f'spec_value_{i}')
            if title and value:
                specifications.append({'title': title, 'value': value})
        return specifications
from django import forms
from .models import Fabric

# forms.py
from django import forms
from .models import Button

class ButtonForm(forms.ModelForm):
    class Meta:
        model = Button
        fields = ['name', 'description', 'price', 'original_price', 'image', 'video', 'in_stock']
class FabricForm(forms.ModelForm):
    class Meta:
        model = Fabric
        fields = ['name', 'description', 'price', 'original_price', 'image', 'video', 'in_stock']        

    # Optionally, you can add custom validation for fields like SKU here.
from .models import Job

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'location', 'job_type']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'job_type': forms.Select(),
        }
class DynamicFabricSpecificationAdminForm(forms.ModelForm):
    specifications = forms.JSONField(widget=JSONFieldWidget, required=False)

    class Meta:
        model = Fabric
        fields = ['name', 'description', 'price', 'original_price', 'image', 'video']  # Adjust fields as needed

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Initialize empty specs
        self.specification_count = len(self.initial.get('specifications', {}))
        for i in range(self.specification_count):
            self.fields[f'spec_title_{i}'] = forms.CharField(
                label=f'Spec Title {i+1}',
                required=False
            )
            self.fields[f'spec_value_{i}'] = forms.CharField(
                label=f'Spec Value {i+1}',
                required=False
            )
from django import forms
from .models import Fabric

class DynamicFabricSpecificationForm(forms.ModelForm):
    class Meta:
        model = Fabric
        fields = ['name', 'description']  # Include static fields

    def clean_sku(self):
        sku = self.cleaned_data['sku']
        if Fabric.objects.exclude(pk=self.instance.pk).filter(sku=sku).exists():
            raise forms.ValidationError("A fabric with this SKU already exists.")
        return sku

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Initialize empty specs
        self.specification_count = len(self.initial.get('specifications', {}))
        for i in range(self.specification_count):
            self.fields[f'spec_title_{i}'] = forms.CharField(
                label=f'Spec Title {i+1}',
                required=False
            )
            self.fields[f'spec_value_{i}'] = forms.CharField(
                label=f'Spec Value {i+1}',
                required=False
            )
            

from .models import Fabric, Button, Booking

class InitialBookingForm(forms.Form):
    has_fabric = forms.ChoiceField(choices=[('yes', 'Yes'), ('no', 'No')], widget=forms.RadioSelect, label="Do you have fabric available, or would you like to browse our options?")


from .models import Booking, City
from .validators import validate_mobile_number 

class BookingForm(forms.ModelForm):
    TIME_CHOICES = [
        ('10:00 AM - 12:00 PM', '10:00 AM - 12:00 PM'),
        ('12:00 PM - 2:00 PM', '12:00 PM - 2:00 PM'),
        ('2:00 PM - 4:00 PM', '2:00 PM - 4:00 PM'),
        ('4:00 PM - 6:00 PM', '4:00 PM - 6:00 PM'),
        ('6:00 PM - 8:00 PM', '6:00 PM - 8:00 PM'),
    ]

    city = forms.ModelChoiceField(queryset=City.objects.all(), widget=forms.Select(attrs={'class': 'city-select'}))
    pickup_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'datepicker'}))
    pickup_time = forms.ChoiceField(
        choices=TIME_CHOICES,
        widget=forms.Select(attrs={'class': 'timepicker'})
    )
    address = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'address-input'}))
    phone_number = forms.CharField(
        max_length=15,
        validators=[validate_mobile_number],
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. +923001234567'})
    )
    preference_image = forms.ImageField(required=False)  # Assuming preference_image is an ImageField
    note = forms.CharField(max_length=255, required=False, widget=forms.Textarea(attrs={'class': 'note-input'}))

    class Meta:
        model = Booking
        fields = ['name', 'phone_number', 'address', 'pickup_date', 'pickup_time', 'preference_image', 'note', 'city']

    def clean_pickup_time(self):
        time_range = self.cleaned_data['pickup_time']
        # Perform any additional validation if needed
        return time_range
from django import forms
from .models import Job, JobApplication


class JobFilterForm(forms.Form):
    location = forms.ChoiceField(choices=[], required=False)
    job_type = forms.ChoiceField(choices=[], required=False)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Populate choices dynamically in the __init__ method
        self.fields['location'].choices = [('', 'All Locations')] + [(loc, loc) for loc in Job.objects.values_list('location', flat=True).distinct()]
        self.fields['job_type'].choices = [('', 'All Types')] + [(jt, jt) for jt in Job.objects.values_list('job_type', flat=True).distinct()]
class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['first_name', 'last_name', 'address', 'phone_no', 'email', 'cv']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_no': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'cv': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
# forms.py
from django import forms
from .models import Expense

class AddExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['date', 'expense_type', 'amount']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add custom classes to other fields for styling
        self.fields['expense_type'].widget.attrs.update({'class': 'form-control'})
        self.fields['amount'].widget.attrs.update({'class': 'form-control'})

from .models import ExpenseType

class ExpenseCategoryForm(forms.ModelForm):
    class Meta:
        model = ExpenseType
        fields = ['name', 'description']
from .models import Product
# forms.py
from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'price', 'original_price', 'image', 'tag']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'original_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'tag': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'original_price': 'Original Price (Optional)',
            'tag': 'Tag (Optional)',
        }
from .models import News

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content', 'posted_on', 'image']
from .models import HomePageInfo

class HomePageInfoForm(forms.ModelForm):
    class Meta:
        model = HomePageInfo
        fields = ['image1', 'heading1', 'image2', 'heading2', 'image3', 'heading3', 'address', 'phone_number', 'email']        
from .models import City

class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ['name', 'booking_open']
        widgets = {
            'booking_open': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }        