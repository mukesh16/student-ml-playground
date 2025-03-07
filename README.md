# **Student ML Playground**
A web-based interactive platform for students to upload datasets, train machine learning models, and experiment with neural networks.

## **Features**
- Upload CSV files and store metadata in PostgreSQL  
- Preview uploaded datasets  
- Train machine learning models  
- View training results  
- Scalable backend using FastAPI and PostgreSQL  
- Interactive frontend using Streamlit  

---

## **Setup Instructions**

### **1. Clone the Repository**
```sh
git clone https://github.com/your-username/student-ml-playground.git
cd student-ml-playground
```

### **2. Create a Virtual Environment**
```sh
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate     # On Windows
```

### **3. Install Dependencies**
```sh
pip install -r requirements.txt
```

### **4. Configure PostgreSQL Database**
1. Start PostgreSQL and create a database:
    ```sql
    CREATE DATABASE student_ml_db;
    ```
2. Inside `backend.py`, update the database connection string:
    ```python
    DATABASE_URL = "postgresql://username:password@localhost/student_ml_db"
    ```

### **5. Initialize the Database**
Run the following command to create the necessary tables:
```sh
python init_db.py
```

### **6. Run the Backend**
Start the FastAPI backend:
```sh
uvicorn backend:app --reload
```
- Runs on `http://127.0.0.1:8000`

### **7. Run the Frontend**
Start the Streamlit frontend:
```sh
streamlit run frontend.py
```
- Runs on `http://localhost:8501`

---

## **Deployment on GitHub**
### **1. Initialize Git**
```sh
git init
git remote add origin https://github.com/your-username/student-ml-playground.git
```

### **2. Add & Commit Changes**
```sh
git add .
git commit -m "Initial commit"
```

### **3. Push to GitHub**
```sh
git branch -M main
git push -u origin main
```

---

## **Future Enhancements**
- Support for more ML models  
- User authentication  
- Cloud-based storage for datasets  

---

Now you’re all set! Let me know if you need any modifications before deployment.