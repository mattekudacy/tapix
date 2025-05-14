from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth import login
from django.contrib import messages
from .models import Portfolio, PortfolioTemplate, ProjectSection, Project, Contact
from .forms import PortfolioForm, ProjectSectionForm, ProjectForm, ContactForm, RegisterForm
from django.http import Http404

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