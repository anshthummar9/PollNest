# 🗳️ PollNest

PollNest is a fully functional, community-driven web application designed to manage polls efficiently. Users can create specialized communities, join existing ones, and participate in polls. Community administrators have full control over managing their members and polls, while users can vote once per poll and instantly view results. Built with Django, it provides a secure, intuitive, and highly responsive interface using Bootstrap 5.

---

## ✨ Features

### 🏢 Community Management
- **Create & Join:** Users can easily create new communities or join existing ones.
- **Admin Controls:** Community creators act as admins capable of managing members and adjusting community settings.
- **Member Ejection:** Admins can safely remove malicious or inactive members from their communities.
- **Safe Exit:** Members can leave communities they are no longer interested in.

### 📊 Poll Management
- **Community-Scoped Polls:** Polls are strictly assigned to specific communities.
- **Admin Exclusive:** Only community admins can create, edit, toggle (active/inactive), and delete polls within their community.
- **Fair Voting:** Users can cast their vote **strictly once** per poll.
- **Real-Time Results:** View beautiful, real-time vote distributions and statistics instantly.

### 🔒 Security & User Experience
- **Authentication:** Secure user registration, login, and logout flows.
- **Responsive UI:** A modern, mobile-friendly interface styled with Bootstrap 5 and Bootstrap Icons.
- **Protection:** Actions are context-aware and protected by robust Django backend validation.

---

## 💻 Tech Stack

- **Backend:** Python (Django) 🐍  
- **Frontend:** HTML, CSS, JavaScript (Bootstrap 5) 💻  
- **Database:** SQLite 🗄️  
- **Version Control:** Git 🔧  

---

## ⚙️ Installation

1. **Clone the repository:**

```bash
git clone https://github.com/anshthummar9/PollNest.git
cd PollNest

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
