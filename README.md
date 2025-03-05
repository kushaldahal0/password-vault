# Password Vault Backend

A simple password vault backend built with **Django REST Framework (DRF)** and **Class-Based Views (CBV)**, using **PostgreSQL** for secure data storage.

## Features 
-  **JWT Authentication** – Secure token-based authentication  
-  **SHA-256 Hashing** – Ensures password integrity  
-  **AES Encryption (Fernet)** – Encrypts stored passwords  
-  **RESTful API** – Easily manage stored credentials  

## Installation & Setup 🛠️

### 1️⃣ Clone the Repository  
```bash
git clone https://github.com/your-username/password-vault-backend.git
cd password-vault-backend
```
### 2️⃣ Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```
### 4️⃣ Set Up Environment Variables
Create a .env file and add:
```ini
SECRET_KEY=your_django_secret_key
FERNET_KEY=your_generated_fernet_key
POSTGRES_USER=your_postgres_database_user
POSTGRES_PASSWORD=your_postgres_database_password
POSTGRES_HOST=your_postgres_database_host
POSTGRES_PORT=your_postgres_database_port
POSTGRES_DATABASE=your_postgres_database_name
```
To generate a Fernet key:
```python
from cryptography.fernet import Fernet
print(Fernet.generate_key().decode())
```
### 5️⃣ Apply Migrations & Run Server
```bash
python manage.py migrate
python manage.py runserver
```
# API Endpoints
| Method | Endpoint                | Description                        |
|--------|-------------------------|------------------------------------|
| POST   | /api/signup/            | Register a new user               |
| POST   | /api/login/             | Login and obtain JWT token        |
| POST   | /api/logout/            | Logout                            |
| GET    | /api/passwords/          | Retrieve all stored passwords     |
| POST   | /api/passwords/          | Add a new password entry          |
| GET    | /api/passwords/{id}/     | Retrieve a specific password      |
| DELETE | /api/passwords/{id}/     | Delete a password entry           |
