<h1> E-commerce Django Project (CBV) </h1>

<h3> A simple e-commerce web application built using Django. </h3>
<p>
<a href="https://www.python.org" target="_blank"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="40" height="40"/> </a>
<a href="https://www.djangoproject.com/" target="_blank"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/django/django-original.svg" alt="django" width="40" height="40"/> </a>
<a href="https://getbootstrap.com" target="_blank"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/bootstrap/bootstrap-plain-wordmark.svg" alt="bootstrap" width="40" height="40"/> </a>
<a href="https://www.w3.org/html/" target="_blank"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/html5/html5-original-wordmark.svg" alt="html5" width="40" height="40"/> </a> <a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript" target="_blank">
</a>
<a href="https://www.sqlite.org/" target="_blank"> <img src="https://www.vectorlogo.zone/logos/sqlite/sqlite-icon.svg" alt="sqlite" width="40" height="40"/> </a>
<a href="https://www.sqlite.org/" target="_blank"> <img src="https://www.vectorlogo.zone/logos/postgresql/postgresql-icon.svg" alt="sqlite" width="40" height="40"/> </a>
<a href="https://www.sqlite.org/" target="_blank"> <img src="https://www.vectorlogo.zone/logos/redis/redis-icon.svg" alt="sqlite" width="40" height="40"/> </a>
</p>

## Features

- User authentication (Sign up, login, logout)
- Product listing with categories
- Shopping cart functionality
- Order management
- Payment integration
- Admin dashboard for product management

## Getting Started

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/MaryaRezvani/E-commerce.git
    cd E-commerce
    ```

2. Create a virtual environment:
    ```bash
    python -m venv env
    source env/bin/activate
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Apply migrations:
    ```bash
    python manage.py migrate
    ```

5. Create a superuser for the admin dashboard:
    ```bash
    python manage.py createsuperuser
    ```

6. Run the development server:
    ```bash
    python manage.py runserver
    ```

7. Access the application at `http://127.0.0.1:8000`.

### Configuration
To connect to Redis and run commands through the CLI, use the following command:
```bash
sudo systemctl enable redis
sudo systemctl start redis
sudo systemctl status redis
redis-cli
```  

### Contributing
If you want to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Make your changes and commit them.
4. Push to your branch.
5. Create a pull request.
