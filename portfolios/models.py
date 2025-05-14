from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify

class PortfolioTemplate(models.Model):
    """Model representing different portfolio templates"""
    name = models.CharField(max_length=100)
    description = models.TextField()
    preview_image = models.ImageField(upload_to='template_previews/', blank=True, null=True)  # Make optional
    template_file = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Portfolio(models.Model):
    """Model representing a user's portfolio"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='portfolios')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    template = models.ForeignKey(PortfolioTemplate, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    
    # Basic info
    tagline = models.CharField(max_length=255, blank=True)
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('portfolio_detail', kwargs={'slug': self.slug})
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.user.username}-{self.title}")
        super().save(*args, **kwargs)

class ProjectSection(models.Model):
    """Model representing sections in the portfolio"""
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='sections')
    title = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.portfolio.title} - {self.title}"

class Project(models.Model):
    """Model representing portfolio projects"""
    section = models.ForeignKey(ProjectSection, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='project_images/', blank=True, null=True)
    url = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.title

class Contact(models.Model):
    """Model for contact information on portfolio"""
    portfolio = models.OneToOneField(Portfolio, on_delete=models.CASCADE, related_name='contact')
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    linkedin = models.URLField(blank=True)
    github = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    
    def __str__(self):
        return f"Contact for {self.portfolio.title}"