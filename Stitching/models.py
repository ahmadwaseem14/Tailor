from django.db import models
from django.utils import timezone


from django.utils import timezone
from django.utils import timezone

class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    date_subscribed = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.email
    
class OTPLog(models.Model):
    email = models.EmailField(blank=True, null=True)
    otp = models.IntegerField(blank=True, null=True)
    time_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.otp)

    def is_expired(self):
        # Check if the OTP is older than 3 minutes
        expiration_time = self.time_stamp + timezone.timedelta(minutes=3)
        return timezone.now() > expiration_time

from django.utils.crypto import get_random_string

class Product(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2,default = 0)  # e.g. 99999.99
    original_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Optional original price
    image = models.ImageField(upload_to='products/')  # Ensure MEDIA_URL and MEDIA_ROOT are configured
    sku = models.CharField(max_length=4, unique=True, editable=False)  # SKU, auto-generated, 4-digit numeric
    tag = models.CharField(max_length=50, null=True, blank=True)  # Optional tag

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.sku:
            # Generate a 4-digit numeric SKU
            self.sku = self.generate_unique_sku()
        super(Product, self).save(*args, **kwargs)

    def generate_unique_sku(self):
        # Generate a unique 4-digit SKU
        while True:
            sku = get_random_string(length=4, allowed_chars='0123456789')
            if not Product.objects.filter(sku=sku).exists():
                return sku
            # models.py
from django.db import models

from django.db import models
from django.core.validators import MinValueValidator
from django.utils.crypto import get_random_string

class Button(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    specifications = models.JSONField(default=dict,  null=True, blank=True)  # Store specifications as key-value pairs
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    original_price = models.DecimalField(max_digits=10, decimal_places=2,  null=True, blank=True) 
    sku = models.CharField(max_length=4, unique=True, editable=False)  # SKU, auto-generated, 4-digit numeric
    image = models.ImageField(upload_to='products/', blank=False, null=False)
    video = models.FileField(upload_to='products/', blank=True, null=True)
    in_stock = models.BooleanField(default=True)
    def save(self, *args, **kwargs):
        if not self.sku:
            # Generate a 4-digit numeric SKU
            self.sku = self.generate_unique_sku()
        super(Button, self).save(*args, **kwargs)

    def generate_unique_sku(self):
        # Generate a unique 4-digit SKU
        while True:
            sku = get_random_string(length=4, allowed_chars='0123456789')
            if not Product.objects.filter(sku=sku).exists():
                return sku
    def __str__(self):
        return self.name
class Fabric(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    specifications = models.JSONField(default=dict,  null=True, blank=True)  # Store specifications as key-value pairs
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    original_price = models.DecimalField(max_digits=10, decimal_places=2,  null=True, blank=True) 
    sku = models.CharField(max_length=4, unique=True, editable=False)  # SKU, auto-generated, 4-digit numeric
    image = models.ImageField(upload_to='products/', blank=False, null=False)
    video = models.FileField(upload_to='products/', blank=True, null=True)
    in_stock = models.BooleanField(default=True)
    def save(self, *args, **kwargs):
        if not self.sku:
            # Generate a 4-digit numeric SKU
            self.sku = self.generate_unique_sku()
        super(Fabric, self).save(*args, **kwargs)

    def generate_unique_sku(self):
        # Generate a unique 4-digit SKU
        while True:
            sku = get_random_string(length=4, allowed_chars='0123456789')
            if not Fabric.objects.filter(sku=sku).exists():
                return sku
    def __str__(self):
        return self.name
class City(models.Model):
    name = models.CharField(max_length=255)
    booking_open = models.BooleanField(default=True)

    def __str__(self):
        return self.name
from django.db import models
import random

class Booking(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    fabric = models.ForeignKey(Fabric, on_delete=models.SET_NULL, null=True, blank=True)
    button = models.ForeignKey(Button, on_delete=models.SET_NULL, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=255, default="hi")  # New address field
    pickup_date = models.DateField()
    pickup_time = models.CharField(max_length=50)  # Use CharField for time ranges
    preference_image = models.ImageField(upload_to='preferences/', blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    tracking_id = models.IntegerField(unique=True, blank=True, null=True)  # Allow tracking_id to be null initially

    def save(self, *args, **kwargs):
        # Generate a unique tracking ID if not already set
        if not self.tracking_id:
            self.tracking_id = self.generate_tracking_id()  # Generate a custom numeric tracking ID
        super().save(*args, **kwargs)

    def generate_tracking_id(self, length=6):
        """Generate a random numeric tracking ID."""
        # Generate a unique tracking ID within the specified length
        tracking_id = ''.join(random.choices('0123456789', k=length))
        
        # Check for uniqueness in the database
        while Booking.objects.filter(tracking_id=tracking_id).exists():
            tracking_id = ''.join(random.choices('0123456789', k=length))  # Regenerate if not unique

        return int(tracking_id)  # Convert to integer

    def __str__(self):
        return f"Booking {self.tracking_id} for {self.name}"
    def __str__(self):
        return f"{self.name} - {self.product.title} Booking"
# models.py
class Job(models.Model):
    JOB_TYPE_CHOICES = [
        ('Full Time', 'Full Time'),
        ('Part Time', 'Part Time'),
        ('Contract', 'Contract'),
        ('Internship', 'Internship'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES)
    posted_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
from django.db import models

class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    posted_on = models.DateField()
    image = models.ImageField(upload_to='news_images/',blank=False)  # Assuming each news item has an image


class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    ]

    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone_no = models.CharField(max_length=20)
    email = models.EmailField()
    cv = models.FileField(upload_to='cv/')
    applied_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='new')

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.job.title}"
from django.db import models
import uuid
class ExpenseType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
class Expense(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    date = models.DateField(null=False)  # Removed the default date function
    expense_type = models.ForeignKey(ExpenseType, null=True, on_delete=models.PROTECT)
    amount = models.FloatField()

    def __str__(self):
        return f"{self.expense_type} - {self.amount}"

class HomePageInfo(models.Model):
    # Image and heading fields
    image1 = models.ImageField(upload_to='home_images/')
    heading1 = models.CharField(max_length=255)
    
    image2 = models.ImageField(upload_to='home_images/')
    heading2 = models.CharField(max_length=255)
    
    image3 = models.ImageField(upload_to='home_images/')
    heading3 = models.CharField(max_length=255)
    
    # Contact details
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return f"HomePageInfo ({self.id})"