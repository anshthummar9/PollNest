# 🗳️ PollNest
PollNest is a fully functional web-based application designed to manage polls efficiently. Administrators can create and manage polls, while users can vote once per poll and instantly view results. Built with Django, it provides a secure, intuitive, and responsive interface suitable for both regular users and administrators.

---

## ✨ Features

- 🛠️ Admins can create, edit, and delete polls  
- 🗳️ Users can vote **once per poll**  
- 📊 View real-time voting results  
- 🌐 Responsive and user-friendly interface  
- 🔒 Secure voting system to prevent multiple votes  
- ⚡ Lightweight and easy to deploy  

---
## 💻 Tech Stack

- **Backend:** Python (Django) 🐍  
- **Frontend:** HTML, CSS, JavaScript 💻  
- **Database:** SQLite 🗄️  
- **Version Control:** Git 🔧  

---
## ⚙️ Installation

1. **Clone the repository:**

```bash
git clone https://github.com/anshthummar9/Polling_System.git
cd Polling_System

```

2. **Set up a virtual environment:**
```bash
python -m venv venv
# Activate the environment:
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Apply database migrations:**
```bash
python manage.py migrate
```

5. **Run the development server:**
```bash
python manage.py runserver
```
Visit http://127.0.0.1:8000/ in your browser. 🌐

