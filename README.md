# Portfolio Creator Project

A Django-based web application that allows users to create and publish professional online portfolios. Users can choose from different templates, add their projects, skills, and contact information, and share their portfolio using a unique URL. This project also supports future NFC card integration.

## Technologies Used
- Python 3.12+
- Django 5.2.1
- PostgreSQL (recommended for production)
- HTML/CSS
- Bootstrap 5
- JavaScript

## Prerequisites
- Python 3.12 or newer
- Git

## Installation Guide
1. Clone the Repository
```bash
git clone https://github.com/yourusername/tapix.git
cd tapix
```
2. Create and Activate Virtual Environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python -m venv .venv
source .venv/bin/activate
```
3. Install Dependencies
```bash
pip install -r requirements.txt
```
4. Configure Environment Variables (In Progress)
Create a .env file in the project root:

For PostgreSQL (recommended for production):

5. Set Up Database
```python
python manage.py migrate
```
6. Create Initial Templates
```python
python manage.py create_initial_templates
```
7. Create a Superuser
8. Run Development Server
Visit http://127.0.0.1:8000/ in your browser to see the application.

## Project Structure
tapix/
├── portfolio_project/      # Project configuration
├── portfolios/             # Main application
│   ├── management/         # Custom management commands
│   ├── migrations/         # Database migrations
│   ├── models.py           # Database models
│   ├── views.py            # View functions
│   ├── urls.py             # URL routing
│   └── admin.py            # Admin configuration
├── templates/              # HTML templates
│   ├── base.html           # Base template
│   └── portfolios/         # Portfolio app templates
│       └── templates/      # Portfolio template files
│           ├── basic.html     # Basic portfolio template
│           └── modern.html    # Modern portfolio template
├── static/                 # Static files (CSS, JS, images)
│   └── images/
│       └── templates/      # Template preview images
├── manage.py               # Django management script
└── requirements.txt        # Project dependencies

Features
User registration and authentication
Create and edit portfolios
Choose from multiple portfolio templates
Add projects with descriptions and images
Add personal information and contact details
Public portfolio pages with unique URLs
Responsive design for mobile and desktop
Development Workflow
Create a feature branch from main
Implement your changes
Write or update tests if applicable
Ensure your code passes all tests
Submit a pull request
Common Tasks
Adding a New Portfolio Template
Create a new HTML template in templates
Add preview images in static/images/templates/
Update create_initial_templates.py
Database Migrations
When changing models:

Troubleshooting
Template Does Not Exist Error
Check if the template file exists in the correct directory
Ensure DIRS is properly configured in settings.py
Run python [manage.py](http://_vscodecontentref_/2) collectstatic if using static files
Database Issues
Check your database connection settings
Ensure all migrations have been applied
Deployment
For production deployment:

Set DEBUG=False in your environment
Configure a production database (PostgreSQL recommended)
Set up static files serving
Use a proper web server like Gunicorn
Configure HTTPS with a reverse proxy like Nginx
License
[Your chosen license here]

For any questions or issues, please open an issue on GitHub or contact the project maintainers.