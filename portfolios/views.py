from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Portfolio, PortfolioTemplate, ProjectSection, Project, Contact
from .forms import PortfolioForm, ProjectSectionForm, ProjectForm, ContactForm, RegisterForm
from django.http import Http404
from django.contrib.admin.views.decorators import staff_member_required
import subprocess
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import sys
import os

@staff_member_required
@require_POST
@csrf_exempt  # Only use this if you have issues with CSRF, otherwise keep CSRF protection!
def nfc_print(request):
    slug = request.POST.get('slug')
    if not slug:
        messages.error(request, "No slug provided.")
        return redirect('nfc_users_admin')
    
    # Use local development URL format instead of production
    url = f"http://127.0.0.1:8000/portfolio/{slug}/"
    
    try:
        script_path = os.path.join(os.path.dirname(__file__), 'send_to_arduino.py')
        result = subprocess.run(
            [sys.executable, 'send_to_arduino.py', url],
            capture_output=True, text=True, check=True
        )
        messages.success(request, f"Sent to Arduino: {url}")
    except subprocess.CalledProcessError as e:
        messages.error(request, f"Failed to send to Arduino: {e.stdout} {e.stderr}")
    return redirect('nfc_users_admin')

@staff_member_required
def nfc_users_admin(request):
    """Admin view for NFC card embedding"""
    from django.contrib.auth.models import User
    users = User.objects.all().order_by('username')
    user_data = []
    for user in users:
        active_portfolio = user.portfolios.filter(is_active=True, is_published=True).first()
        if active_portfolio:
            user_data.append({
                'username': user.username,
                'full_name': user.get_full_name() or user.username,
                'slug': active_portfolio.slug,
            })
    return render(request, 'portfolios/nfc_users_admin.html', {'user_data': user_data})

def template_preview(request, template_name):
    """Show a preview of a portfolio template with sample data"""
    # Get template by filename
    try:
        template = PortfolioTemplate.objects.get(template_file=f"{template_name}.html")
    except PortfolioTemplate.DoesNotExist:
        raise Http404("Template not found")
    
    # Create dummy portfolio data
    dummy_portfolio = {
        'title': 'John Doe',
        'tagline': 'Web Developer & Designer',
        'bio': 'John is a passionate developer who loves building modern and elegant web applications. With 5+ years of experience in frontend and backend technologies, he creates solutions that are both functional and beautiful.',
        'profile_image': None  # We'll handle this in the template
    }
    
    # Create dummy sections and projects
    dummy_sections = [{
        'title': 'Web Projects',
        'projects': [
            {
                'title': 'E-commerce Website',
                'description': 'A responsive e-commerce platform built with Django and React. Features include user authentication, product catalog, shopping cart, and payment integration.',
                'image': None,  # We'll handle this in the template
                'url': '#'
            },
            {
                'title': 'Portfolio Generator',
                'description': 'An application that allows users to create professional portfolios with customizable templates and easy content management.',
                'image': None,
                'url': '#'
            },
            {
                'title': 'Task Management App',
                'description': 'A productivity tool for organizing tasks with features like drag-and-drop organization, reminders, and team collaboration.',
                'image': None,
                'url': '#'
            }
        ]
    },
    {
        'title': 'Design Projects',
        'projects': [
            {
                'title': 'Brand Identity Design',
                'description': 'Created a complete brand identity including logo, color palette, typography, and brand guidelines for a tech startup.',
                'image': None,
                'url': '#'
            },
            {
                'title': 'UI/UX Redesign',
                'description': 'Redesigned the user interface of a mobile application to improve user experience and increase engagement.',
                'image': None,
                'url': '#'
            }
        ]
    }]
    
    # Create dummy contact info
    dummy_contact = {
        'email': 'john.doe@example.com',
        'phone': '+1 (555) 123-4567',
        'linkedin': 'https://linkedin.com/in/johndoe',
        'github': 'https://github.com/johndoe',
        'twitter': 'https://twitter.com/johndoe'
    }
    
    # Add these to the context
    dummy_portfolio['contact'] = dummy_contact
    
    # Render the template
    template_path = f"portfolios/templates/{template_name}.html"
    return render(request, template_path, {
        'portfolio': dummy_portfolio,
        'sections': dummy_sections,
        'is_preview': True  # Flag to indicate this is a preview
    })

def home(request):
    """Home page view"""
    templates = PortfolioTemplate.objects.all()
    return render(request, 'portfolios/home.html', {'templates': templates})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Account created for {user.username}!')
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})

# Check if this function exists and contains the correct query
@login_required
def choose_template(request):
    templates = PortfolioTemplate.objects.all()
    return render(request, 'portfolios/choose_template.html', {
        'templates': templates
    })

@login_required
def dashboard(request):
    """User dashboard to manage portfolios"""
    portfolios = Portfolio.objects.filter(user=request.user)
    return render(request, 'portfolios/dashboard.html', {'portfolios': portfolios})

@login_required
def choose_template(request):
    """View to choose a template for a new portfolio"""
    templates = PortfolioTemplate.objects.all()
    return render(request, 'portfolios/choose_template.html', {'templates': templates})

@login_required
def create_portfolio(request, template_id):
    """View to create a new portfolio with the selected template"""
    template = get_object_or_404(PortfolioTemplate, pk=template_id)
    
    if request.method == 'POST':
        form = PortfolioForm(request.POST, request.FILES)
        if form.is_valid():
            portfolio = form.save(commit=False)
            portfolio.user = request.user
            portfolio.template = template
            portfolio.save()
            
            # Create default section
            ProjectSection.objects.create(
                portfolio=portfolio,
                title="Projects",
                order=1
            )
            
            # Create empty contact info
            Contact.objects.create(portfolio=portfolio)
            
            messages.success(request, 'Portfolio created successfully!')
            return redirect('edit_portfolio', portfolio_id=portfolio.id)
    else:
        form = PortfolioForm(initial={'template': template})
    
    return render(request, 'portfolios/create_portfolio.html', {
        'form': form,
        'template': template
    })

@login_required
def toggle_active_portfolio(request, portfolio_id):
    """Toggle a portfolio as the user's active portfolio"""
    portfolio = get_object_or_404(Portfolio, pk=portfolio_id, user=request.user)
    
    # Set this portfolio as active (which will deactivate others)
    portfolio.is_active = True
    portfolio.save()
    
    messages.success(request, f'"{portfolio.title}" is now your active portfolio!')
    return redirect('dashboard')

@login_required
def edit_portfolio(request, portfolio_id):
    """View to edit a portfolio"""
    portfolio = get_object_or_404(Portfolio, pk=portfolio_id, user=request.user)
    
    if request.method == 'POST':
        form = PortfolioForm(request.POST, request.FILES, instance=portfolio)
        if form.is_valid():
            form.save()
            messages.success(request, 'Portfolio updated successfully!')
            return redirect('edit_portfolio', portfolio_id=portfolio.id)
    else:
        form = PortfolioForm(instance=portfolio)
    
    sections = portfolio.sections.all()
    
    return render(request, 'portfolios/edit_portfolio.html', {
        'portfolio': portfolio,
        'form': form,
        'sections': sections
    })

@login_required
def add_section(request, portfolio_id):
    """View to add a new section to portfolio"""
    portfolio = get_object_or_404(Portfolio, pk=portfolio_id, user=request.user)
    
    if request.method == 'POST':
        form = ProjectSectionForm(request.POST)
        if form.is_valid():
            section = form.save(commit=False)
            section.portfolio = portfolio
            section.order = portfolio.sections.count() + 1
            section.save()
            messages.success(request, 'Section added successfully!')
            return redirect('edit_portfolio', portfolio_id=portfolio.id)
    else:
        form = ProjectSectionForm()
    
    return render(request, 'portfolios/add_section.html', {
        'form': form,
        'portfolio': portfolio
    })

@login_required
def add_project(request, section_id):
    """View to add a project to a section"""
    section = get_object_or_404(ProjectSection, pk=section_id)
    portfolio = section.portfolio
    
    # Ensure the user owns this portfolio
    if portfolio.user != request.user:
        messages.error(request, "You don't have permission to edit this portfolio.")
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.section = section
            project.order = section.projects.count() + 1
            project.save()
            messages.success(request, 'Project added successfully!')
            return redirect('edit_portfolio', portfolio_id=portfolio.id)
    else:
        form = ProjectForm()
    
    return render(request, 'portfolios/add_project.html', {
        'form': form,
        'section': section,
        'portfolio': portfolio
    })

@login_required
def edit_contact(request, portfolio_id):
    """View to edit contact information"""
    portfolio = get_object_or_404(Portfolio, pk=portfolio_id, user=request.user)
    contact, created = Contact.objects.get_or_create(portfolio=portfolio)
    
    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            messages.success(request, 'Contact information updated successfully!')
            return redirect('edit_portfolio', portfolio_id=portfolio.id)
    else:
        form = ContactForm(instance=contact)
    
    return render(request, 'portfolios/edit_contact.html', {
        'form': form,
        'portfolio': portfolio
    })

def portfolio_detail(request, slug):
    """Public view for viewing a portfolio"""
    portfolio = get_object_or_404(Portfolio, slug=slug, is_published=True)
    sections = portfolio.sections.all()
    
    # Template path should point to templates/portfolios/templates/[template_file]
    template_name = f"portfolios/templates/{portfolio.template.template_file}"
    
    return render(request, template_name, {
        'portfolio': portfolio,
        'sections': sections
    })

# portfolios/views.py
def user_portfolio(request, username):
    """Redirect to a user's active portfolio or their first published portfolio"""
    user = get_object_or_404(User, username=username)
    
    # Try to find active portfolio
    active_portfolio = Portfolio.objects.filter(
        user=user, 
        is_published=True, 
        is_active=True
    ).first()
    
    # If no active portfolio, get the first published one
    if not active_portfolio:
        active_portfolio = Portfolio.objects.filter(
            user=user, 
            is_published=True
        ).first()
        
    # If we found a portfolio, redirect to it
    if active_portfolio:
        return redirect('portfolio_detail', slug=active_portfolio.slug)
    
    # If user has no published portfolios but is the current logged in user
    if request.user.username == username:
        messages.info(request, "You don't have any published portfolios yet. Create and publish a portfolio first!")
        return redirect('dashboard')
        
    # If we get here, the user has no published portfolios
    raise Http404("This user has no published portfolios.")