# In your app, create the file context_processors.py if it doesn't already exist

from .models import HomePageInfo

def home_page_info(request):
    try:
        home_info = HomePageInfo.objects.first()  # Get the first record (assuming only one)
    except HomePageInfo.DoesNotExist:
        home_info = None

    return {
        'home_image1': home_info.image1.url if home_info else '',
        'home_heading1': home_info.heading1 if home_info else '',
        'home_image2': home_info.image2.url if home_info else '',
        'home_heading2': home_info.heading2 if home_info else '',
        'home_image3': home_info.image3.url if home_info else '',
        'home_heading3': home_info.heading3 if home_info else '',
        'home_address': home_info.address if home_info else '',
        'home_phone_number': home_info.phone_number if home_info else '',
        'home_email': home_info.email if home_info else '',
    }
