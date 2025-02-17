### Step 1: Clone and Setup Virtual Environment
```bash
# Clone the repository
git clone [repository-url]
cd recruitment_platform

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
.\venv\Scripts\activate
# On Unix or MacOS:
source venv/bin/activate
```

### Step 2: Install Dependencies
```bash
# Install required packages
pip install -r requirements.txt
```

### Step 3: Database Setup
Create PostgreSQL Database using pgAdmin4
```sql
CREATE DATABASE easy_lodge;
```

### Step 4: Django Settings
In your Django project, navigate to settings.py and update the database configuration section to use PostgreSQL:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'easy_lodge',  # The database name you just created
        'USER': 'your_postgresql_user',  # Your PostgreSQL user
        'PASSWORD': 'your_postgresql_password',  # Your PostgreSQL password
        'HOST': 'localhost',
        'PORT': '5432',  # Your PostgreSQL server port (right click server properties)
    }
}
Make sure to replace your_postgresql_user and your_postgresql_password with your PostgreSQL user credentials.
```

### Step 5: Apply Migrations
Next, apply the migrations to create the necessary tables in your PostgreSQL database:
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Create a Superuser

To access the Django Admin panel, you need to create a superuser account:
```bash
python manage.py createsuperuser
Follow the prompts to set up your superuser account.
```

### Step 7: Run the Development Server

Start the development server:
```bash
python manage.py runserver
Visit http://127.0.0.1:8000/ in your browser to see the project in action.
```

### Step 8: Access the Admin Panel
```bash
To access the Django admin panel, go to http://127.0.0.1:8000/admin/ and log in using the superuser credentials you created earlier.
```

Step 9: Setup Frontend with React
Install Node.js and npm
Ensure Node.js is installed on your system. If not, download and install it from nodejs.org.

Install React App Dependencies
Navigate to the frontend directory and install the dependencies:

```bash
cd frontend
npm install
Start the React Development Server

Run the following command to start the React app:
npm start

The React app will run at http://localhost:3000.
```

### Step 10: Visit the Application
After starting both the Django backend and React frontend:

Django Backend: Visit http://127.0.0.1:8000 for backend-related tasks.
React Frontend: Visit http://localhost:3000 to interact with the React frontend.
