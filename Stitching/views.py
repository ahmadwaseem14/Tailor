from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.utils import timezone

from .models import OTPLog
from .email import email_message
import random


from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
# Create your models here.
# models.py
from django.db import models
# Create your views here.
from django.shortcuts import render

def home(request):
    homepage_info = HomePageInfo.objects.first()
    return render(request, 'home/home.html', {'homepage_info': homepage_info})

def about(request):
    pass


def contact(request):
 pass
from django.http import JsonResponse
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from .forms import SubscriberForm
from .models import Subscriber

def subscribe(request):
    if request.method == 'POST':
        form = SubscriberForm(request.POST)

        # Validate the form first
        if form.is_valid():
            email = form.cleaned_data['email']  # Get the email from cleaned data

            # Check if the email already exists
            if Subscriber.objects.filter(email=email).exists():
                return JsonResponse({'success': False, 'message': "This email is already subscribed."})

            # Save the subscriber if the email is unique
            subscriber = form.save()

            # Render the HTML template
            subject = 'Thank you for subscribing!'
            html_content = render_to_string('email/subscription_email.html', {})
            
            # Send confirmation email
            email = EmailMessage(
                subject,
                html_content,
                'your_email@gmail.com',  # From email
                [subscriber.email],  # To email
            )
            email.content_subtype = 'html'  # Set content type to HTML
            email.send(fail_silently=False)

            return JsonResponse({'success': True, 'message': "Thank you for subscribing!"})
        
        # Handle case where form is not valid
        return JsonResponse({'success': False, 'message': "This email is already subscribed."})

    return JsonResponse({'success': False, 'message': "Invalid request."})
from .forms import ContactForm
from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import render
from django.core.mail import send_mail
def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            
            # Render the HTML email
            html_message = render_to_string('email/contact_us.html', {
                'name': name,
                'email': email,
                'phone': phone,
                'subject': subject,
                'message': message,
                'current_year': datetime.now().year,
            })

            # Send email
            send_mail(
                f"New Contact Us Message: {subject}",
                '',  # No plain text message
                'stylenest.pk@gmail.com',  # Replace with your email
                ['funwithelectricac@gmail.com'],  # Replace with the recipient's email
                html_message=html_message,
                fail_silently=False,
            )

            # Return a JSON response indicating success
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)

    else:
        form = ContactForm()

    # Render the form for GET requests
    return render(request, 'contact.html', {'form': form})
# LOGIN / REGISTER
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.utils import timezone

from .models import OTPLog
from .email import email_message
import random


from django.contrib.auth import authenticate, login
from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('/')
def login_view(request):
    context = {
        'title': 'Sign In'
    }

    if request.method == "POST":
        username = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect("/admin/")
            else:
                return redirect("/")
        else:
            context['login_error'] = "Invalid credentials!"

    return render(request, 'auth/login.html', context)



def register_view(request):
    context = {
        'title': 'Sign Up',
        'reg_errors': [],
    }
    if request.method == "POST":
        if request.POST.get('password1') == request.POST.get('password2'):
            if User.objects.filter(email=request.POST.get('email')).exists():
                context["reg_errors"].append("Email already in use!")
            else:
                request.session['user_type'] = request.POST.get('user_type')
                request.session['f_name'] = request.POST.get('f_name')
                request.session['l_name'] = request.POST.get('l_name')
                request.session['email'] = request.POST.get('email')
                request.session['password'] = request.POST.get('password1')

                try:
                    otp = OTPLog.objects.get(email=request.POST.get('email')).otp
                except OTPLog.DoesNotExist:  # More specific exception handling
                    otp = random.randint(100000, 999999)
                    OTPLog.objects.create(email=request.POST.get('email'), otp=otp)

                # Prepare the email content using the HTML template
                email_subject = 'Registration OTP'
                email_message = render_to_string('email/otp_email.html', {
                    'first_name': request.POST.get('f_name'),
                    'l_name': request.POST.get('l_name'),
                    'otp': otp,
                })

                # Send the email
                send_mail(
                    email_subject,
                    email_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [request.POST.get('email')],
                    html_message=email_message
                )

                return redirect("/signup/otp")
        else:
            context["reg_errors"].append("Passwords don't match!")
    return render(request, 'auth/register.html', context)

from django.contrib import messages
def send_otp_email(email, otp, first_name):
    subject = 'Your OTP for Registration'
    message = render_to_string('email/otp_email.html', {
        'otp': otp,
        'first_name': first_name,  # Add first name to the context
    })
    send_mail(subject, message, 'your_email@example.com', [email], fail_silently=False, html_message=message)
def reg_otp_view(request):
    context = {
        'title': 'OTP Verification',
        'email': request.session.get('email'),
        'first_name': request.session.get('f_name')  # Store first name in context if needed
    }

    if request.method == "POST":
        if 'resend_otp' in request.POST:
            # Resend OTP
            return resend_otp_view(request)

        otp_input = request.POST.get('otp')
        if otp_input is None:
            context['error'] = "OTP field is missing."
        else:
            try:
                otp = OTPLog.objects.get(email=request.session['email'])
                if otp.is_expired():
                    context['error'] = "OTP has expired. Please request a new one."
                elif int(otp_input) == otp.otp:
                    User.objects.create_user(
                        username=request.session['email'],
                        first_name=request.session['f_name'],
                        last_name=request.session['l_name'],
                        email=request.session['email'],
                        password=request.session['password']
                    )

                    user = authenticate(request, username=request.session['email'], password=request.session['password'])
                    if user is not None:
                        login(request, user)
                    return redirect('/')
                else:
                    context['error'] = "Wrong OTP"
            except OTPLog.DoesNotExist:
                context['error'] = "OTP does not exist. Please request a new one."
            except ValueError:
                context['error'] = "Invalid OTP format. Please enter a 6-digit OTP."

    return render(request, 'auth/otp.html', context)
def send_otp_email(email, otp, first_name):
    subject = 'Your OTP for Registration'
    message = render_to_string('email/otp_email.html', {
        'otp': otp,
        'first_name': first_name,  # Add first name to the context
    })
    send_mail(subject, message, 'your_email@example.com', [email], fail_silently=False, html_message=message)
def resend_otp_view(request):
    email = request.session.get('email')
    first_name = request.session.get('f_name')  # Get the first name from the session
    if email:
        try:
            otp = OTPLog.objects.get(email=email)
            otp.otp = random.randint(100000, 999999)
            otp.time_stamp = timezone.now()  # Update timestamp to reset expiration
            otp.save()
        except OTPLog.DoesNotExist:
            otp = OTPLog.objects.create(
                email=email,
                otp=random.randint(100000, 999999)
            )
        
        # Send the OTP email with the first name included
        send_otp_email(email, otp.otp, first_name)  # Use the updated send_otp_email function

        # Add a success message to be displayed on the frontend
        messages.success(request, "A new OTP has been resent to your email.")

    return redirect('/signup/otp')  # Redirect back to OTP page
    # Return the user to the OTP page with context containing messages
def error_page_view(request):
    return render(request, 'auth/error.html', {'title': 'Error'})
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.utils.translation import gettext_lazy as _  # Update import



def forgot_password_view(request):
    message = ''
    
    if request.method == "POST":
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            current_site = get_current_site(request)
            reset_link = f"{request.scheme}://{current_site.domain}/reset-password/{uid}/{token}/"
            
            subject = 'Password Reset Request'
            message = render_to_string('email/password_reset_email.html', {
                'user': user,
                'reset_link': reset_link,
                'domain': current_site.domain,
            })
            
            # Sending the email as HTML
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email], html_message=message)
            message = 'Password reset link has been sent to your email.'
        else:
            message = 'Email not found.'

    return render(request, 'auth/forgot_password.html', {'message': message})
    
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.utils.encoding import force_str

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render, redirect

def reset_password_view(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == "POST":
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)  # Keeps the user logged in after password change
                return redirect('/signin/')
        else:
            form = SetPasswordForm(user)

        return render(request, 'auth/password_reset_form.html', {'form': form})
    else:
        return render(request, 'auth/password_reset_invalid.html')
from .models import Product
from django.http import JsonResponse
from django.shortcuts import render
from .models import Product

from django.db.models import Q

def product_list(request):
    query = request.GET.get('q', '')
    sort_by = request.GET.get('sort', '')

    products = Product.objects.all()

    if query:
        products = products.filter(Q(title__icontains=query) | Q(sku__icontains=query))

    if sort_by == 'price_low':
        products = products.order_by('price')  # Low to High
    elif sort_by == 'price_high':
        products = products.order_by('-price')  # High to Low
    elif sort_by == 'name':
        products = products.order_by('title')  # Alphabetical order

    # Check if the request is AJAX
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        products_data = [{
            'title': product.title,
            'price': product.price,
            'image_url': product.image.url,
            'sku': product.sku,
            'original_price': product.original_price,  # Include original price if needed
            'tag': product.tag,  # Include tag if needed
        } for product in products]
        return JsonResponse(products_data, safe=False)

    return render(request, 'shop/shop.html', {
        'products': products,
        'query': query,
        'sort_by': sort_by,
    })

from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q
from .models import Button

def fabric_list(request):
    query = request.GET.get('q', '')
    sort_by = request.GET.get('sort', '')

    buttons = Fabric.objects.all()

    if query:
        buttons = buttons.filter(Q(name__icontains=query) | Q(sku__icontains=query))

    if sort_by == 'price_low':
        buttons = buttons.order_by('price')  # Low to High
    elif sort_by == 'price_high':
        buttons = buttons.order_by('-price')  # High to Low
    elif sort_by == 'name':
        buttons = buttons.order_by('name')  # Alphabetical order

    # Check if the request is AJAX
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        buttons_data = [{
            'name': button.name,
            'price': button.price,
            'image_url': button.image.url if button.image else '',
            'sku': button.sku,
            'original_price': button.original_price,
            'tag': button.tag if hasattr(button, 'tag') else '',
            'detail_url': reverse('fabric_detail', kwargs={'sku': button.sku}),  # Construct the full URL
        } for button in buttons]
        return JsonResponse(buttons_data, safe=False)

    return render(request, 'shop/fabric_list.html', {
        'buttons': buttons,
        'query': query,
        'sort_by': sort_by,
    })

from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Q
from django.urls import reverse
from .models import Button
def button_list(request):
    query = request.GET.get('q', '')
    sort_by = request.GET.get('sort', '')

    buttons = Button.objects.all()

    if query:
        buttons = buttons.filter(Q(name__icontains=query) | Q(sku__icontains=query))

    if sort_by == 'price_low':
        buttons = buttons.order_by('price')  # Low to High
    elif sort_by == 'price_high':
        buttons = buttons.order_by('-price')  # High to Low
    elif sort_by == 'name':
        buttons = buttons.order_by('name')  # Alphabetical order

    # Check if the request is AJAX
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        buttons_data = [{
            'name': button.name,
            'price': button.price,
            'image_url': button.image.url if button.image else '',
            'sku': button.sku,
            'original_price': button.original_price,
            'tag': button.tag if hasattr(button, 'tag') else '',
            'detail_url': reverse('button_detail', kwargs={'sku': button.sku}),  # Construct the full URL
        } for button in buttons]
        return JsonResponse(buttons_data, safe=False)

    return render(request, 'shop/button_list.html', {
        'buttons': buttons,
        'query': query,
        'sort_by': sort_by,
    })

from django.shortcuts import render, get_object_or_404
from .models import Button
def fabric_detail(request, sku):
    button = get_object_or_404(Fabric, sku=sku)
    specifications = button.specifications  # Assuming this is a list of dicts
    
    return render(request, 'shop/fabric.detail.html', {
        'button': button,
        'specifications': specifications,
    })    
def button_detail(request, sku):
    button = get_object_or_404(Button, sku=sku)
    specifications = button.specifications  # Assuming this is a list of dicts
    
    return render(request, 'shop/buttons.detail.html', {
        'button': button,
        'specifications': specifications,
    })    
    #booking 
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Product, Fabric, Button, City, Booking
from .forms import InitialBookingForm, BookingForm
from django.contrib.auth.decorators import login_required
def booking(request, product_sku):
    product = get_object_or_404(Product, sku=product_sku)
    step = request.GET.get('step', 'initial')
    
    # Step 1: Initial Booking Page
    if step == 'initial':
        if request.method == 'POST':
            form = InitialBookingForm(request.POST)
            if form.is_valid():
                has_fabric = form.cleaned_data['has_fabric']
                request.session['has_fabric'] = has_fabric
                if has_fabric == 'yes':
                    return JsonResponse({'redirect_url': f'/booking/{product_sku}/?step=select_button'})
                else:
                    return JsonResponse({'redirect_url': f'/booking/{product_sku}/?step=select_fabric'})
        else:
            form = InitialBookingForm()
        return render(request, 'initial_booking.html', {'form': form, 'product': product})

    # Step 2: Select Fabric
    elif step == 'select_fabric':
        fabrics = Fabric.objects.filter(in_stock=True)
        if request.method == 'POST':
            fabric_sku = request.POST.get('fabric_sku')
            fabric = get_object_or_404(Fabric, sku=fabric_sku)
            request.session['fabric_sku'] = fabric.sku
            return redirect(f'/booking/{product_sku}/?step=select_button&fabric_sku={fabric.sku}')
        return render(request, 'fabric_selection.html', {'fabrics': fabrics, 'product': product})

    # Step 3: Select Button
    elif step == 'select_button':
        fabric_sku = request.GET.get('fabric_sku')
        fabric = Fabric.objects.filter(sku=fabric_sku).first() if fabric_sku else None
        buttons = Button.objects.filter(in_stock=True)
        if request.method == 'POST':
            button_sku = request.POST.get('button_sku')
            button = get_object_or_404(Button, sku=button_sku)
            if fabric:
                return redirect(f'/booking/{product_sku}/?step=booking_form&fabric_sku={fabric.sku}&button_sku={button.sku}')
            else:
                return redirect(f'/booking/{product_sku}/?step=booking_form&button_sku={button.sku}')
        return render(request, 'button_selection.html', {'buttons': buttons, 'product': product, 'fabric': fabric})

    # Step 4: Booking Form
    elif step == 'booking_form':
        fabric_sku = request.GET.get('fabric_sku')
        button_sku = request.GET.get('button_sku')
        fabric = Fabric.objects.filter(sku=fabric_sku).first() if fabric_sku else None
        button = Button.objects.filter(sku=button_sku).first() if button_sku else None
        cities = City.objects.all()
        if request.method == 'POST':
            form = BookingForm(request.POST, request.FILES)
            if form.is_valid():
                city = form.cleaned_data['city']
                if city and not city.booking_open:
                    form.add_error('city', f"Bookings for {city.name} are currently closed.")
                else:
                    # Save the form data in the session
                    request.session['booking_data'] = {
                        'name': form.cleaned_data['name'],
                        'phone_number': form.cleaned_data['phone_number'],
                        'address': form.cleaned_data['address'],
                        'pickup_date': form.cleaned_data['pickup_date'].strftime('%Y-%m-%d'),
                        'pickup_time': form.cleaned_data['pickup_time'],
                        'city': city.pk,
                        'fabric': fabric.sku if fabric else None,
                        'button': button.sku if button else None,
                    }
                    return redirect(f'/booking/{product_sku}/?step=confirmation')
        else:
            form = BookingForm()
        return render(request, 'booking_form.html', {
            'form': form,
            'product': product,
            'fabric': fabric,
            'button': button,
            'cities': cities
        })

    # Step 5: Confirmation and Tracking
    elif step == 'confirmation':
        booking_data = request.session.get('booking_data', {})
        if not booking_data:
            return redirect(f'/booking/{product_sku}/?step=initial')
        
        product = get_object_or_404(Product, sku=product_sku)
        fabric = Fabric.objects.filter(sku=booking_data['fabric']).first() if booking_data.get('fabric') else None
        button = Button.objects.filter(sku=booking_data['button']).first() if booking_data.get('button') else None
        city = City.objects.get(pk=booking_data['city'])
        total_price = product.price
        if fabric:
            total_price += fabric.price
        if button:
            total_price += button.price
        
        if request.method == 'POST':
            booking = Booking(
                product=product,
                fabric=fabric,
                button=button,
                city=city,
                name=booking_data['name'],
                phone_number=booking_data['phone_number'],
                address=booking_data['address'],
                pickup_date=booking_data['pickup_date'],
                pickup_time=booking_data['pickup_time'],
                preference_image=booking_data.get('preference_image'),
                note=booking_data.get('note')
            )
            booking.save()
            
            # Redirect to a separate tracking page to avoid resubmission
            return redirect(f'/tracking/{booking.tracking_id}/')  # Use a dedicated tracking URL
        
        return render(request, 'confirmation.html', {
            "city": city,
            'product': product,
            'fabric': fabric,
            'button': button,
            'total_price': total_price,
            'booking_data': booking_data
        })

    # Redirect to initial step if no valid step is provided
    else:
        return redirect(f'/booking/{product_sku}/?step=initial')
from django.shortcuts import render, get_object_or_404

def tracking(request, tracking_id):
    booking = get_object_or_404(Booking, tracking_id=tracking_id)
    return render(request, 'tracking_id.html', {
        'booking': booking
    })

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Job, JobApplication
from .forms import JobApplicationForm

def job_list_view(request):
    jobs = Job.objects.all()
    return render(request, 'career.html', {'jobs': jobs})

def apply_for_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            job_application = form.save(commit=False)
            job_application.job = job
            job_application.save()
            return JsonResponse({'success': True, 'message': 'Application submitted successfully!'})
        else:
            return JsonResponse({'success': False, 'message': 'Form data is invalid!'})
    return JsonResponse({'success': False, 'message': 'Invalid request method!'})
from django.core.paginator import Paginator
from django.shortcuts import render
from .models import News
def news_lists(request):
    news_list = News.objects.all().order_by('-posted_on')
    paginator = Paginator(news_list, 6)  # 6 news items per page
    page_number = request.GET.get('page')
    news_items = paginator.get_page(page_number)
    return render(request, 'news.html', {'news_items': news_items , "news":news_list})
def news_detail(request, News_id):
    article = get_object_or_404(News, id=News_id)
    recent_articles = News.objects.order_by('-posted_on')[:5]
    return render(request, 'news_detail.html', {'article': article, 'recent_articles': recent_articles})
def book_now_view(request):
    fabrics = Fabric.objects.all()  # Fabric model should have `price` and `image` fields
    buttons = Button.objects.filter(in_stock=True)  # Button model should also have `price` and `image`
    cities = City.objects.all()

    if request.method == 'POST':
        form = BookingForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('success_page')
    else:
        form = BookingForm()

    return render(request, 'book_now.html', {
        'form': form,
        'fabrics': fabrics,
        'buttons': buttons,
        'cities': cities,
    })
from datetime import datetime, timedelta
from django.db.models import Sum
from django.shortcuts import render
from .models import Expense
import json
import calendar
from django.utils.timezone import now

def list_expenses(request):
    filter_type = request.GET.get('filter', 'total')
    min_date = request.GET.get('min_date')
    max_date = request.GET.get('max_date')

    # Ensure min_date and max_date are parsed as date objects if provided
    if min_date:
        min_date = datetime.strptime(min_date, '%Y-%m-%d').date()
    if max_date:
        max_date = datetime.strptime(max_date, '%Y-%m-%d').date()

    if filter_type == 'today':
        today = now().date()
        expenses = Expense.objects.filter(date=today)
        expense_data = expenses.values('date').annotate(total_amount=Sum('amount')).order_by('date')
        expense_labels = [today.strftime('%Y-%m-%d')]
        expense_data_values = [float(expense_data[0]['total_amount']) if expense_data else 0]
    elif filter_type == 'month':
        start_date = now().replace(day=1)  # Start of the current month
        end_date = now().replace(day=calendar.monthrange(now().year, now().month)[1])  # End of the current month
        expenses = Expense.objects.filter(date__range=[start_date, end_date])
        expense_data = expenses.values('date').annotate(total_amount=Sum('amount')).order_by('date')

        # Ensure you have all days of the month covered
        days_of_month = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]
        day_to_amount = {day.date(): 0 for day in days_of_month}

        for data in expense_data:
            day_to_amount[data['date']] = float(data['total_amount'])

        expense_labels = [day.strftime('%d %b') for day in days_of_month]
        expense_data_values = [day_to_amount[day.date()] for day in days_of_month]
    elif filter_type == 'year':
        expenses = Expense.objects.filter(date__year=now().year)
        expense_data = expenses.values('date__month').annotate(total_amount=Sum('amount')).order_by('date__month')
        expense_labels = [calendar.month_name[data['date__month']] for data in expense_data]
        expense_data_values = [float(data['total_amount']) for data in expense_data]
    else:  # 'total' filter
        if min_date and max_date:
            expenses = Expense.objects.filter(date__range=[min_date, max_date])
        else:
            expenses = Expense.objects.all()

        # Aggregate by month and year
        expense_data = expenses.values('date__year', 'date__month').annotate(total_amount=Sum('amount')).order_by('date__year', 'date__month')
        expense_labels = [f"{calendar.month_name[data['date__month']]} {data['date__year']}" for data in expense_data]
        expense_data_values = [float(data['total_amount']) for data in expense_data]

    total_filtered_expense = expenses.aggregate(Sum('amount'))['amount__sum'] or 0

    return render(request, 'admin/expense.html', {
        'expenses': expenses,
        'total_filtered_expense': total_filtered_expense,
        'filter_type': filter_type,
        'min_date': min_date,
        'max_date': max_date,
        'labels': json.dumps(expense_labels),
        'data': json.dumps(expense_data_values),
    })
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import AddExpenseForm
from .models import Expense

from django.views.generic import CreateView
from django.urls import reverse_lazy

class AddExpenseView(CreateView):
    model = Expense
    form_class = AddExpenseForm
    template_name = 'admin/add_expense.html'
    
    def get_success_url(self):
        if 'save_and_add' in self.request.POST:
            return reverse_lazy('add_expense')  # Redirects to the same page for adding a new expense
        return reverse_lazy('list_expenses')  # Redirects to the list view
    
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
from django.shortcuts import render, get_object_or_404, redirect
from .models import Expense
from .forms import AddExpenseForm
from django.shortcuts import render, get_object_or_404, redirect
from .models import Expense
from .forms import AddExpenseForm

def edit_expense(request, id):
    # Fetch the existing Expense object by its ID
    expense = get_object_or_404(Expense, id=id)

    # Handle the POST request
    if request.method == 'POST':
        form = AddExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()  # Save the updated Expense object
            return redirect('list_expenses')  # Redirect to the list of expenses
        else:
            return render(request, 'admin/edit_expense.html', {'form': form, 'expense': expense})

    # Handle the GET request
    else:
        form = AddExpenseForm(instance=expense)
        return render(request, 'admin/edit_expense.html', {'form': form, 'expense': expense})

def delete_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)
    if request.method == 'POST':
        expense.delete()
        messages.success(request, 'Expense deleted successfully!')
        return redirect('list_expenses')
    return render(request, 'confirm_delete.html', {'expense': expense})
# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import ExpenseType
from .forms import ExpenseCategoryForm

# List Categories
def list_expense_categories(request):
    categories = ExpenseType.objects.all()
    return render(request, 'admin/expense_category.html', {'categories': categories})

# Add Category
def add_expense_category(request):
    if request.method == 'POST':
        form = ExpenseCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added successfully!')
            return redirect('list_expense_categories')
    else:
        form = ExpenseCategoryForm()
    return render(request, 'admin/add_expense_category.html', {'form': form, 'title': 'Add Category'})

# Edit Category
def edit_expense_category(request, category_id):
    category = get_object_or_404(ExpenseType, id=category_id)
    if request.method == 'POST':
        form = ExpenseCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('list_expense_categories')
    else:
        form = ExpenseCategoryForm(instance=category)
    return render(request, 'admin/edit_expense_category.html', {'form': form, 'title': 'Edit Category'})
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from .models import ExpenseType

from django.contrib import messages
from django.db.models import ProtectedError
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from django.shortcuts import redirect
from .models import ExpenseType

class ExpenseCategoryDeleteView(DeleteView):
    model = ExpenseType
    success_url = reverse_lazy('list_expense_categories')  # Adjust to your URL name

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            # Attempt to delete the category
            self.object.delete()
            return redirect(self.success_url)
        except ProtectedError:
            # Send an error message if the category is in use
            messages.error(
                request,
                f"Cannot delete category '{self.object.name}' because it is associated with existing expenses."
            )
            return redirect(self.success_url)

from django.shortcuts import render
from .models import Product
from django.db.models import Q

def product_lists(request):
    query = request.GET.get('search', '')
    products = Product.objects.all()
    
    if query:
        products = products.filter(
            Q(title__icontains=query) | 
            Q(sku__icontains=query) | 
            Q(tag__icontains=query)
        )

    context = {
        'products': products,
    }
    return render(request, 'admin/outfit.html', context)
from .forms import ProductForm
from .models import Product
from django.urls import reverse

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Check if "Save and Add New" was clicked
            if 'save_and_add' in request.POST:
                return redirect(reverse('add_product'))  # Reload the add product form
            else:
                return redirect(reverse('product_lists'))  # Redirect to product list
    else:
        form = ProductForm()
    
    context = {'form': form}
    return render(request, 'admin/add_product.html', context)
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from .forms import ProductForm

# Edit Product View
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_lists')  # Redirect to product list after saving
    else:
        form = ProductForm(instance=product)
    return render(request, 'admin/edit_product.html', {'form': form})

# Delete Product View
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_lists')  # Redirect to product list after deletion
    return render(request, 'delete_product.html', {'product': product})
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Button
from django.db.models import Q

class ButtonListView(View):
    template_name = 'admin/button-admin.html'
    
    def get(self, request):
        # Get search query from request
        search_query = request.GET.get('search', '')
        
        # Filter buttons based on search query
        if search_query:
            buttons = Button.objects.filter(
                Q(name__icontains=search_query) |
                Q(sku__icontains=search_query)
            )
        else:
            buttons = Button.objects.all()
        
        context = {
            'buttons': buttons,
        }
        return render(request, self.template_name, context)
from django.shortcuts import render, redirect
from .forms import ButtonForm
from .models import Button

def add_button(request):
    if request.method == 'POST':
        form = ButtonForm(request.POST, request.FILES)
        
        if form.is_valid():
            # Save the button instance
            button = form.save()

            # Capture the dynamic specification fields
            spec_titles = request.POST.getlist('spec_title[]')
            spec_values = request.POST.getlist('spec_value[]')

            # Combine specifications into a list of dictionaries
            specifications = [
                {"title": title, "value": value}
                for title, value in zip(spec_titles, spec_values)
            ]

            # Save the specifications as JSON in the model
            button.specifications = specifications
            button.save()

            # Check if the "Save & Add More" button was clicked
            if 'save_add_more' in request.POST:
                return redirect('add_button')  # Redirect back to add another button
            else:
                return redirect('button_listss')  # Redirect to the list of buttons after save

    else:
        form = ButtonForm()

    return render(request, 'admin/add_button.html', {'form': form})


def edit_button(request, pk):
    button = get_object_or_404(Button, pk=pk)
    
    if request.method == 'POST':
        form = ButtonForm(request.POST, request.FILES, instance=button)
        
        if form.is_valid():
            button = form.save()

            # Capture the updated dynamic specification fields
            spec_titles = request.POST.getlist('spec_title[]')
            spec_values = request.POST.getlist('spec_value[]')

            # Combine specifications into a list of dictionaries
            specifications = [
                {"title": title, "value": value}
                for title, value in zip(spec_titles, spec_values)
            ]

            # Save the updated specifications as JSON in the model
            button.specifications = specifications
            button.save()

            return redirect('button_listss')  # Redirect to button list after saving

    else:
        # Prepopulate form and specifications
        form = ButtonForm(instance=button)
        specifications = button.specifications if button.specifications else []
    
    return render(request, 'admin/edit_button.html', {
        'form': form,
        'button': button,
        'specifications': specifications,
    })

class ButtonDeleteView(View):
    def get(self, request, pk):
        # Fetch the button instance to delete
        button = get_object_or_404(Button, pk=pk)
        return render(request, 'admin/delete_button.html', {'button': button})

    def post(self, request, pk):
        # Delete the button instance
        button = get_object_or_404(Button, pk=pk)
        button.delete()
        return redirect('button_listss')  # Redirect to the button list after deletion
    # Fabric
    
class FabricListView(View):
    template_name = 'admin/fabric-admin.html'
    
    def get(self, request):
        # Get search query from request
        search_query = request.GET.get('search', '')
        
        # Filter buttons based on search query
        if search_query:
            buttons = Fabric.objects.filter(
                Q(name__icontains=search_query) |
                Q(sku__icontains=search_query)
            )
        else:
            buttons = Fabric.objects.all()
        
        context = {
            'buttons': buttons,
        }
        return render(request, self.template_name, context)
from django.shortcuts import render, redirect
from .forms import FabricForm
from .models import Button

def add_fabric(request):
    if request.method == 'POST':
        form = FabricForm(request.POST, request.FILES)
        
        if form.is_valid():
            # Save the button instance
            button = form.save()

            # Capture the dynamic specification fields
            spec_titles = request.POST.getlist('spec_title[]')
            spec_values = request.POST.getlist('spec_value[]')

            # Combine specifications into a list of dictionaries
            specifications = [
                {"title": title, "value": value}
                for title, value in zip(spec_titles, spec_values)
            ]

            # Save the specifications as JSON in the model
            button.specifications = specifications
            button.save()

            # Check if the "Save & Add More" button was clicked
            if 'save_add_more' in request.POST:
                return redirect('add_fabric')  # Redirect back to add another button
            else:
                return redirect('fabric_listss')  # Redirect to the list of buttons after save

    else:
        form = FabricForm()

    return render(request, 'admin/add_fabric.html', {'form': form})


def edit_fabric(request, pk):
    button = get_object_or_404(Fabric, pk=pk)
    
    if request.method == 'POST':
        form = FabricForm(request.POST, request.FILES, instance=button)
        
        if form.is_valid():
            button = form.save()

            # Capture the updated dynamic specification fields
            spec_titles = request.POST.getlist('spec_title[]')
            spec_values = request.POST.getlist('spec_value[]')

            # Combine specifications into a list of dictionaries
            specifications = [
                {"title": title, "value": value}
                for title, value in zip(spec_titles, spec_values)
            ]

            # Save the updated specifications as JSON in the model
            button.specifications = specifications
            button.save()

            return redirect('fabric_listss')  # Redirect to button list after saving

    else:
        # Prepopulate form and specifications
        form = FabricForm(instance=button)
        specifications = button.specifications if button.specifications else []
    
    return render(request, 'admin/edit_fabric.html', {
        'form': form,
        'button': button,
        'specifications': specifications,
    })

class FabricDeleteView(View):
    def get(self, request, pk):
        # Fetch the button instance to delete
        button = get_object_or_404(Fabric, pk=pk)
        return render(request, 'admin/delete_fabric.html', {'button': button})

    def post(self, request, pk):
        # Delete the button instance
        button = get_object_or_404(Fabric, pk=pk)
        button.delete()
        return redirect('fabric_listss')  # Redirect to the button list after deletion
from django.shortcuts import render
from Stitching.models import Subscriber
from django.utils import timezone
from django.core.paginator import Paginator
from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Subscriber
def subscriber_list(request):
    # Get all subscribers and apply search if necessary
    search_query = request.GET.get('search', '').strip()
    sort_by = request.GET.get('sort_by', 'date_subscribed')  # Default sort by date_subscribed
    sort_order = request.GET.get('sort_order', 'desc')  # Default order descending

    # Filtering based on search query
    if search_query:
        subscribers = Subscriber.objects.filter(Q(email__icontains=search_query) | Q(date_subscribed__icontains=search_query)).order_by(
            f'-{sort_by}' if sort_order == 'desc' else sort_by
        )
    else:
        subscribers = Subscriber.objects.all().order_by(f'-{sort_by}' if sort_order == 'desc' else sort_by)

    # Pagination
    paginator = Paginator(subscribers, 10)  # Show 10 subscribers per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'admin/subscribtion_list.html', {
        'page_obj': page_obj,
        'search_query': search_query,
        'sort_by': sort_by,
        'sort_order': sort_order
    })

from .models import Job


def job_list(request):
    search_query = request.GET.get('q', '')

    # Filter jobs based on the search query
    if search_query:
        jobs = Job.objects.filter(title__icontains=search_query)
    else:
        jobs = Job.objects.all()

    # Pagination
    paginator = Paginator(jobs, 10)  # Show 10 jobs per page
    page_number = request.GET.get('page')
    jobs_page = paginator.get_page(page_number)

    return render(request, 'admin/job_list_admin.html', {'jobs': jobs_page})
from django.shortcuts import render, redirect, get_object_or_404
from .models import Job
from django.http import HttpResponse

# Add Job View
# Edit Job View
def edit_job(request, job_id):
    job = Job.objects.get(id=job_id)
    
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('job_list')  # Redirect to job list after editing the job
    else:
        form = JobForm(instance=job)

    return render(request, 'admin/edit_job.html', {'form': form, 'job': job})


# Edit Job View
from django.shortcuts import render, redirect
from .models import Job
from .forms import JobForm

# Add Job View
def add_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('job_list')  # Redirect to job list after saving the job
    else:
        form = JobForm()

    return render(request, 'admin/add_job.html', {'form': form})


# Delete Job View
def delete_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    job.delete()
    return redirect('job_list')  # Redirect to job list after deleting the job
class JobDeleteView(DeleteView):
    model = Job
    template_name = 'job_confirm_delete.html'
    success_url = reverse_lazy('job_list')
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from .models import JobApplication

class JobApplicationListView(ListView):
    model = JobApplication
    template_name = 'admin/job_application_list.html'
    context_object_name = 'applications'
    
    def get_queryset(self):
        # Get the 'status' parameter from the request; default to 'new' if not provided
        status = self.request.GET.get('status', None)
        
        # If status is 'all' or None, return all applications
        if status == 'all' or status is None:
            return JobApplication.objects.all()
        
        # Otherwise, filter by the selected status
        return JobApplication.objects.filter(status=status)

def change_status(request, pk):
    application = get_object_or_404(JobApplication, pk=pk)
    new_status = request.POST.get('status')
    if new_status in dict(JobApplication.STATUS_CHOICES):
        application.status = new_status
        application.save()
    return redirect('job_application_list')
from .models import News

def news_list(request):
    news_items = News.objects.all().order_by('-posted_on')
    return render(request, 'admin/news_list.html', {'news_items': news_items})    
from .forms import NewsForm

def add_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('news_list')  # Redirect to the news list page after saving
    else:
        form = NewsForm()
    return render(request, 'admin/add_news.html', {'form': form})
def edit_news(request, news_id):
    news_item = get_object_or_404(News, id=news_id)
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES, instance=news_item)
        if form.is_valid():
            form.save()
            return redirect('news_list')  # Redirect to the news list page after saving
    else:
        form = NewsForm(instance=news_item)
    return render(request, 'admin/edit_news.html', {'form': form})

def delete_news(request, news_id):
    news_item = get_object_or_404(News, id=news_id)
    news_item.delete()
    return redirect('news_list')  # Redirect to the news list page after deleting
from .models import HomePageInfo
from .forms import HomePageInfoForm

def home_page_info(request):
    homepage_info = HomePageInfo.objects.first()  # Assuming you have only one object for homepage info
    return render(request, 'admin/homepage_view.html', {'homepage_info': homepage_info})

def edit_home_page_info(request, pk):
    homepage_info = get_object_or_404(HomePageInfo, pk=pk)
    
    if request.method == 'POST':
        form = HomePageInfoForm(request.POST, request.FILES, instance=homepage_info)
        if form.is_valid():
            form.save()
            return redirect('home_page_info')  # Redirect to the home page info view after saving
    else:
        form = HomePageInfoForm(instance=homepage_info)
    
    return render(request, 'admin/edit_home_page_info.html', {'form': form, 'homepage_info': homepage_info})
from .forms import CityForm  # You will create this form later
from django.contrib import messages

# List Cities
def city_list(request):
    cities = City.objects.all()
    return render(request, 'admin/city_list.html', {'cities': cities})

# Add City
def add_city(request):
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "City added successfully!")
            return redirect('city_list')
    else:
        form = CityForm()
    return render(request, 'admin/city_add.html', {'form': form})

# Edit City
def edit_city(request, city_id):
    city = get_object_or_404(City, id=city_id)
    if request.method == 'POST':
        form = CityForm(request.POST, instance=city)
        if form.is_valid():
            form.save()
            messages.success(request, "City updated successfully!")
            return redirect('city_list')
    else:
        form = CityForm(instance=city)
    return render(request, 'admin/city_edit.html', {'form': form, 'city': city})

# Delete City
def delete_city(request, city_id):
    city = get_object_or_404(City, id=city_id)
    if request.method == 'POST':
        city.delete()
        messages.success(request, "City deleted successfully!")
        return redirect('city_list')
    return render(request, 'delete_city.html', {'city': city})
def fabric_search(request):
    query = request.GET.get('q', '')
    fabrics = Fabric.objects.filter(
        Q(name__icontains=query) | Q(sku__icontains=query)
    )
    return render(request, 'fabric_options.html', {'fabrics': fabrics})

def button_search(request):
    query = request.GET.get('q', '')
    buttons = Button.objects.filter(
        Q(name__icontains=query) | Q(sku__icontains=query)
    )
    return render(request, 'button_options.html', {'buttons': buttons})