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

### Step 9: Setup Frontend with React
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

After starting both the Django backend and React frontend, you can access the following:

#### Django Backend:
- Visit [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin) for backend-related tasks.

#### Admin Interface:
![Admin](https://github.com/user-attachments/assets/5a00799b-f7e1-4bd5-9fc2-f332f1f1860c)

---

### Backend Screenshots

#### User Management:
- **User View:**  
  ![User](https://github.com/user-attachments/assets/8d1884a6-e206-4d0c-9c60-eb1fa9a33f34)
  
- **Add User:**  
  ![User Add](https://github.com/user-attachments/assets/5c4d473f-4449-4763-a4e4-7519f81901ea)
  
- **Edit User:**  
  ![User Edit](https://github.com/user-attachments/assets/9c7dcf9b-9602-41d8-a23f-c143576e9f8a)
  
- **Edit User (Alternate View):**  
  ![User Edit 2](https://github.com/user-attachments/assets/7959f973-7d48-4422-b49e-96e03d5e5f06)

#### Guest Management:
- **Guest View:**  
  ![Guest View](https://github.com/user-attachments/assets/6e321d75-32b9-4f34-966f-9eaa1c9be71c)
  
- **Edit Guest:**  
  ![Guest Edit](https://github.com/user-attachments/assets/fd6f38bd-2c45-4802-91a0-8b060676b645)
  
- **Add Guest:**  
  ![Guest Add](https://github.com/user-attachments/assets/f05395f3-ad05-49ef-b5d3-210bd85d2d29)

#### Room Management:
- **Rooms View:**  
  ![Rooms View](https://github.com/user-attachments/assets/287ec8be-9e3a-4493-85e9-316c61e28fe7)
  
- **Edit Room:**  
  ![Rooms Edit](https://github.com/user-attachments/assets/757295d1-c918-48a4-a758-ea09c1ff3766)
  
- **Add Room:**  
  ![Rooms Add](https://github.com/user-attachments/assets/419e9659-30b9-4ed2-9f52-c1234d7c77c0)

#### Booking Management:
- **Add Booking:**  
  ![Bookings Add](https://github.com/user-attachments/assets/b52c8ee6-32d2-485b-ba44-4451109c35cb)
  
- **Bookings View:**  
  ![Bookings View](https://github.com/user-attachments/assets/36edcf6f-87d7-4d1b-9128-29207419c7cf)
  
- **Edit Booking:**  
  ![Booking Edit](https://github.com/user-attachments/assets/467eb6b0-5146-43e8-b09d-dcaa6b1f2081)
  

React Frontend: Visit http://localhost:3000 to interact with the React frontend.




