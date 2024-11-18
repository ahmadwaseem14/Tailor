from django.contrib import admin

# Register your models here.
from .models import Product,Booking

class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'sku', 'price', 'original_price', 'tag')  # Display title, SKU, price, original price, and tag
    search_fields = ('title', 'sku')  # Enable search functionality by title and SKU
    list_filter = ('tag',)  # Add filter for the 'tag' field

admin.site.register(Product, ProductAdmin)
# admin.py
from django.contrib import admin
from django.contrib import admin



from django.contrib import admin
from .models import Button, News
from .forms import DynamicSpecificationAdminForm

class ButtonAdmin(admin.ModelAdmin):
    form = DynamicSpecificationAdminForm
    list_display = ('name', 'description','sku')

admin.site.register(Button, ButtonAdmin)
from .models import Fabric
from .forms import DynamicFabricSpecificationAdminForm

@admin.register(Fabric)
class FabricAdmin(admin.ModelAdmin):
    form = DynamicFabricSpecificationAdminForm
    
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('product', 'fabric', 'button', 'city', 'name', 'phone_number', 'address', 'pickup_date', 'pickup_time')
 
    search_fields = ('name', 'phone_number', 'address', 'product__title', 'fabric__name', 'button__name', 'city__name')
    list_filter = ('pickup_date', 'city')
    readonly_fields = ('product', 'fabric', 'button', 'city')
    from django.contrib import admin
from .models import Job, JobApplication

class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'job_type', 'posted_on')
    search_fields = ('title', 'location', 'job_type')
    list_filter = ('job_type', 'location', 'posted_on')
    ordering = ('-posted_on',)
    date_hierarchy = 'posted_on'

class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'first_name', 'last_name', 'email', 'applied_on')
    search_fields = ('first_name', 'last_name', 'email', 'job__title')
    list_filter = ('applied_on', 'job__location', 'job__job_type')
    ordering = ('-applied_on',)
    date_hierarchy = 'applied_on'

admin.site.register(Job, JobAdmin)
admin.site.register(JobApplication, JobApplicationAdmin)
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title',  'posted_on')
    search_fields = ('title',  'content')
    list_filter = ('posted_on',)
    date_hierarchy = 'posted_on'
    ordering = ('-posted_on',)
from django.contrib import admin
from .models import Expense, ExpenseType

class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('expense_type', 'amount', 'date')
    list_filter = ('expense_type', 'date')
    search_fields = ('expense_type__name',)
    ordering = ('-date',)

class ExpenseTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# Register your models here
admin.site.register(Expense, ExpenseAdmin)
admin.site.register(ExpenseType, ExpenseTypeAdmin)
from django.utils.html import format_html
from .models import HomePageInfo

class HomePageInfoAdmin(admin.ModelAdmin):
    list_display = ('heading1', 'heading2', 'heading3', 'address', 'phone_number', 'email', 'image1_thumbnail', 'image2_thumbnail', 'image3_thumbnail')
    search_fields = ('heading1', 'heading2', 'heading3', 'address', 'phone_number', 'email')

    # Method to show images as thumbnails in the list view
    def image1_thumbnail(self, obj):
        if obj.image1:
            return format_html('<img src="{}" style="width: 100px; height: 100px; object-fit: cover;" />', obj.image1.url)
        return "No image"
    image1_thumbnail.short_description = 'Image 1'

    def image2_thumbnail(self, obj):
        if obj.image2:
            return format_html('<img src="{}" style="width: 100px; height: 100px; object-fit: cover;" />', obj.image2.url)
        return "No image"
    image2_thumbnail.short_description = 'Image 2'

    def image3_thumbnail(self, obj):
        if obj.image3:
            return format_html('<img src="{}" style="width: 100px; height: 100px; object-fit: cover;" />', obj.image3.url)
        return "No image"
    image3_thumbnail.short_description = 'Image 3'

    # Optional: You can also customize the form view if necessary
    fieldsets = (
        (None, {
            'fields': ('image1', 'heading1', 'image2', 'heading2', 'image3', 'heading3', 'address', 'phone_number', 'email')
        }),
    )

admin.site.register(HomePageInfo, HomePageInfoAdmin)  