from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from .views import error_page_view
from .views import forgot_password_view, reset_password_view
from .views import login_view, register_view, reg_otp_view,resend_otp_view
from .views import logout_view
from django.conf import settings
from .views import ButtonListView
from .views import FabricListView
from .views import ButtonDeleteView
from .views import FabricDeleteView
from .views import JobDeleteView
from .views import JobApplicationListView, change_status
from .views import AddExpenseView
from .views import ExpenseCategoryDeleteView
# from .views import select_fabric_view
from django.conf.urls.static import static
urlpatterns = [
     path('news-ADMIN/', views.news_list, name='news_list'),
    path('news-ADMIN/add/', views.add_news, name='add_news'),
    path('news-ADMIN/edit/<int:news_id>/', views.edit_news, name='edit_news'),
    path('news-ADMIN/delete/<int:news_id>/', views.delete_news, name='delete_news'),
    path('applications/', JobApplicationListView.as_view(), name='job_application_list'),
    path('applications/<int:pk>/change_status/', change_status, name='change_status'),
    path('add-product/', views.add_product, name='add_product'),
    path('products/', views.product_lists, name='product_lists'),
 path('expenses', views.list_expenses, name='list_expenses'),
         path('expenses/edit/<int:id>', views.edit_expense, name='edit_expense'),
 path('categories/', views.list_expense_categories, name='list_expense_categories'),
    path('categories/add/', views.add_expense_category, name='add_expense_category'),
    path('categories/edit/<int:category_id>/', views.edit_expense_category, name='edit_expense_category'),
     path('expenses/add/', AddExpenseView.as_view(), name='add_expense'),
    path('', views.home, name='home'),       # Home page
    path('subscriber_list/', views.subscriber_list, name='subscriber_list'),  # Add this line
        path('add_fabric/', views.add_fabric, name='add_fabric'),  # Add this line
    path('add_button/', views.add_button, name='add_button'),  # Add this line
    # path('contact/', views.contact, name='contact'), # Contact page
     path('subscribe/', views.subscribe, name='subscribe'),
      path('contact/', views.contact_us, name='contact_us'),
        path('signin/', login_view, name='login'),
        path('list/buttons/', ButtonListView.as_view(), name='button_listss'),
        path('list/Fabrics/', FabricListView.as_view(), name='fabric_listss'),
            path('edit_button/<int:pk>/', views.edit_button, name='edit_button'),
             path('edit_fabric/<int:pk>/', views.edit_fabric, name='edit_fabric'),
    path('signup/', register_view, name='register'),
    path('signup/otp', reg_otp_view, name='otp'),
    path('logout', LogoutView.as_view(), name="logout"),
    path('reset_password/', PasswordResetView.as_view(), name="reset_password"),
    path('reset_pass_sent/', PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset_pass_complete/', PasswordResetCompleteView.as_view(), name="password_reset_complete"),
     path('error/', error_page_view, name='error_page'),
     path('logout/', logout_view, name='logout'),
         path('news/', views.news_lists, name='news_lists'),
    # path('news/<int:id>/', news_detail, name='news_detail'),
 path('expense/delete/<int:expense_id>/', views.delete_expense, name='delete_expense'),
      path('auth/signup/otp/resend', resend_otp_view, name='resend_otp'),
      path('forgot-password/', forgot_password_view, name='forgot_password'),
       path('shop/', views.product_list, name='product_list'),
       path('career/', views.job_list_view, name='job_list'),
    path('apply/<int:job_id>/', views.apply_for_job, name='apply_for_job'),
           path('gallery/button/<str:sku>/', views.button_detail, name='button_detail'),
     path('gallery/button/', views.button_list, name='button_list'),
            path('gallery/fabric/<str:sku>/', views.fabric_detail, name='fabric_detail'),
     path('gallery/fabric/', views.fabric_list, name='fabric_list'),
 path('booking/<str:product_sku>/', views.booking, name='booking'),
 path('news/<int:News_id>/', views.news_detail, name='news_detail'),
    path('reset-password/<uidb64>/<token>/', reset_password_view, name='reset_password'),
     path('product/edit/<int:pk>/', views.edit_product, name='edit_product'),
    path('product/delete/<int:pk>/', views.delete_product, name='delete_product'),
      path('button/delete/<int:pk>/', ButtonDeleteView.as_view(), name='button_delete'),
           path('fabric/delete/<int:pk>/', FabricDeleteView.as_view(), name='fabric_delete'),
            path('edit-job/<int:job_id>/', views.edit_job, name='edit_job'),
    path('delete-job/<int:job_id>/', views.delete_job, name='delete_job'),
     path('tracking/<str:tracking_id>/', views.tracking, name='tracking'),
      path('expense-category/<int:pk>/delete/', ExpenseCategoryDeleteView.as_view(), name='delete_expense_category'),
      path('admin-jobs/', views.job_list, name='job_list'),
         path('add-job/', views.add_job, name='add_job'),
             path('job/<int:pk>/delete/', JobDeleteView.as_view(), name='job_delete'),
                 path('home_page_info/', views.home_page_info, name='home_page_info'),
    path('edit_home_page_info/<int:pk>/', views.edit_home_page_info, name='edit_homepage_info'),
     path('cities/', views.city_list, name='city_list'),
    path('cities/add/', views.add_city, name='add_city'),
     path('fabric-search/', views.fabric_search, name='fabric_search'),
    path('cities/edit/<int:city_id>/', views.edit_city, name='edit_city'),
    path('cities/delete/<int:city_id>/', views.delete_city, name='delete_city'),
     path('button-search/', views.button_search, name='button_search'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)