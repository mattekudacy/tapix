from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('choose-template/', views.choose_template, name='choose_template'),
    path('create-portfolio/<int:template_id>/', views.create_portfolio, name='create_portfolio'),
    path('portfolio/<int:portfolio_id>/edit/', views.edit_portfolio, name='edit_portfolio'),
    path('add-section/<int:portfolio_id>/', views.add_section, name='add_section'),
    path('add-project/<int:section_id>/', views.add_project, name='add_project'),
    path('edit-contact/<int:portfolio_id>/', views.edit_contact, name='edit_contact'),
    path('portfolio/<slug:slug>/', views.portfolio_detail, name='portfolio_detail'),
    path('accounts/register/', views.register, name='register'),
    path('template-preview/<str:template_name>/', views.template_preview, name='template_preview'),
    path('portfolio/<int:portfolio_id>/set-active/', views.toggle_active_portfolio, name='toggle_active_portfolio'),
    path('u/<str:username>/', views.user_portfolio, name='user_portfolio'),
    path('nfc-admin/', views.nfc_users_admin, name='nfc_users_admin'),
    path('nfc-print/', views.nfc_print, name='nfc_print'),
]