# Django REST API with PostgreSQL

## 📌 Overview
This project is a Django REST API powered by Django Rest Framework (DRF) with PostgreSQL as the database. It provides a structured and scalable backend for web and mobile applications.

## 🛠️ Technologies Used
- **Django** - High-level Python web framework
- **Django REST Framework (DRF)** - Toolkit for building APIs
- **PostgreSQL** - Relational database for data storage
- **Docker** (Optional) - For containerized deployment
- **Gunicorn** - WSGI server for production
- **Simple JWT** - Authentication using JSON Web Tokens

---

## 🚀 Getting Started

### **1. Clone the Repository**
```bash
git clone https://github.com/yourusername/your-repo.git
cd your-repo
```

### **2. Create and Activate a Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### **3. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4. Configure Environment Variables**
Create a `.env` file in the root directory and add:
```env
SECRET_KEY=your_secret_key
DEBUG=True
DATABASE_URL=postgres://your_user:your_password@localhost:5432/your_db_name
```

### **5. Apply Migrations & Create a Superuser**
```bash
python manage.py migrate
python manage.py createsuperuser
```

### **6. Run the Development Server**
```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`

---

## 🔐 Authentication (JWT)
This API uses JWT for authentication. Obtain a token by sending a `POST` request:

**Endpoint:** `/api/token/`
```json
{
    "username": "your_username",
    "password": "your_password"
}
```
**Response:**
```json
{
    "refresh": "your_refresh_token",
    "access": "your_access_token"
}
```
To access protected routes, include the token in the Authorization header:
```bash
Authorization: Bearer your_access_token
```

---

## 📂 API Endpoints
| Method | Endpoint         | Description                |
|--------|------------------|----------------------------|
| POST   | `/api/token`     | Obtain JWT token          |
| POST   | `/api/token/refresh` | Refresh access token    |
| GET    | `/api/users`      | List users (Admin only)   |
| POST   | `/api/users/register` | Register a new user    |

---

## 🐳 Running with Docker (Optional)
### **1. Build and Run the Container**
```bash
docker-compose up --build
```
The API will be available at `http://localhost:8000/`

---

## 📝 License
This project is licensed under the MIT License.

---

## 👨‍💻 Author
**Ouda** - [GitHub](https://github.com/ouda711)

