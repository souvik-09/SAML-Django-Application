# Django SAML Authentication Project

A Django-based web application that implements SAML (Security Assertion Markup Language) authentication for secure single sign-on (SSO) capabilities.

## Features

- SAML-based authentication
- Django REST Framework integration
- Secure user authentication and authorization
- CORS support for cross-origin requests
- SQLite database
- Django admin interface

## Prerequisites

- Python 3.x
- Virtual environment (recommended)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/souvik-09/SAML-Django-Application.git
cd myproject
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure your environment variables:
   - Create a `.env` file in the project root
   - Add necessary environment variables for:
     - SAML settings
     - Secret key
     - Debug mode

5. Run migrations:
```bash
python manage.py migrate
```

6. Create a superuser:
```bash
python manage.py createsuperuser
```

7. Run the development server:
```bash
python manage.py runserver
```

## Project Structure

```
myproject/
├── app/
│   ├── authentication/     # SAML authentication implementation
│   ├── migrations/         # Database migrations
│   ├── templates/          # HTML templates
│   ├── views/             # View implementations
│   └── ...
├── myproject/             # Project configuration
├── OpenText/              # OpenText integration
├── requirements.txt       # Project dependencies
└── manage.py             # Django management script
```

## Dependencies

- Django 4.2.11
- django-cors-headers 4.3.1
- djangorestframework 3.15.1
- python3-saml 1.16.0
- And other supporting packages (see requirements.txt)

## Configuration

### SAML Configuration

Configure your SAML settings in the appropriate configuration files:
- SP (Service Provider) settings
- IdP (Identity Provider) settings
- Certificate and key configurations

### Database Configuration

The project uses SQLite as the default database backend. The database file is located at `db.sqlite3` in the project root directory.

## Usage

1. Access the admin interface at `/admin/`
2. Configure SAML settings through the admin interface
3. Access the SAML authentication endpoints:
   - `/saml/login/` - Initiate SAML login
   - `/saml/metadata/` - View SAML metadata
   - `/saml/acs/` - Assertion Consumer Service endpoint

## Security Considerations

- Keep your private keys and certificates secure
- Use HTTPS in production
- Regularly update dependencies
- Follow Django security best practices

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

