from django.core.management.base import BaseCommand
from portfolios.models import PortfolioTemplate

class Command(BaseCommand):
    help = 'Create initial portfolio templates'

    def handle(self, *args, **kwargs):
        # Check if templates already exist
        if PortfolioTemplate.objects.exists():
            self.stdout.write(self.style.WARNING('Templates already exist. No templates were created.'))
            return

        # Basic template
        PortfolioTemplate.objects.create(
            name='Basic Portfolio',
            description='A clean, simple portfolio layout perfect for showcasing your projects.',
            template_file='basic.html'
        )
        
        # Modern template
        PortfolioTemplate.objects.create(
            name='Modern Portfolio',
            description='A modern, visually appealing portfolio with a sleek design.',
            template_file='modern.html'
        )
        
        self.stdout.write(self.style.SUCCESS('Successfully created initial templates!'))