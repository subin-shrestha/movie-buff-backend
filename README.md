movie buff django source code
=============================

To run locally, do the usual:

**1. Clone the source code to local machine**

    git clone git@github.com:subin-shrestha/movie-buff-backend.git


**2. Create a Python 3.6 virtualenv**

    virtualenv venv --python=python3

**3. Activate virtual env**

    source venv/bin/activate


**4. Install dependencies::**

    pip install -r requirements.txt

**5. Setup local settings**
    
create local_settings.py next to main settings.py and add email host settings

    EMAIL_HOST = ''
    EMAIL_HOST_USER = ''
    EMAIL_HOST_PASSWORD = ''
    EMAIL_PORT = ''

    ADMIN_EMAIL = ""

**6. Create database tables**

    ./manage.py migrate

**7. Create a superuser::**

   ./manage.py createsuperuser

**8. Run server**

    ./manage.py runserver 0.0.0.0:8000

**9. To run unit test**

    py.test

It will generate the test coverage report in html format.