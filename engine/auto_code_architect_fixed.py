import os
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional

class AutoCodeArchitect:
    def __init__(self):
        self.desktop_path = Path.home() / "Desktop"
    
    def detect_request_type(self, query: str) -> Dict:
        query_lower = query.lower()
        
        language = self._detect_language(query_lower)
        project_type = self._detect_project_type(query_lower)
        project_name = self._extract_project_name(query)
        
        return {
            'language': language,
            'project_type': project_type,
            'project_name': project_name,
            'original_query': query
        }
    
    def _detect_language(self, query: str) -> str:
        query_lower = query.lower()
        if any(word in query_lower for word in ['python', 'flask', 'django', 'fastapi']):
            return 'python'
        elif any(word in query_lower for word in ['javascript', 'js', 'node', 'react', 'vue', 'angular']):
            return 'javascript'
        elif any(word in query_lower for word in ['java', 'spring']):
            return 'java'
        elif any(word in query_lower for word in ['c#', 'csharp', '.net']):
            return 'csharp'
        elif any(word in query_lower for word in ['php', 'laravel']):
            return 'php'
        elif any(word in query_lower for word in ['html', 'css', 'static']):
            return 'html'
        else:
            return 'python'
    
    def _detect_project_type(self, query: str) -> str:
        query_lower = query.lower()
        if any(phrase in query_lower for phrase in ['only html', 'html and css', 'static', 'frontend only']):
            return 'static'
        elif any(word in query_lower for word in ['react', 'vue', 'angular']):
            return 'spa'
        elif any(word in query_lower for word in ['api', 'rest', 'microservice']):
            return 'api'
        elif any(word in query_lower for word in ['desktop', 'gui', 'tkinter', 'electron']):
            return 'desktop'
        elif any(word in query_lower for word in ['mobile', 'android', 'ios']):
            return 'mobile'
        else:
            return 'web'
    
    def _extract_project_name(self, query: str) -> str:
        # Extract everything after 'generate code' or similar commands
        patterns = [
            r'generate\s+code\s+(.+?)(?:\s+using|\s+with|\s+in|$)',
            r'create\s+(?:a\s+)?(.+?)(?:\s+using|\s+with|\s+in|$)',
            r'build\s+(?:a\s+)?(.+?)(?:\s+using|\s+with|\s+in|$)',
            r'make\s+(?:a\s+)?(.+?)(?:\s+using|\s+with|\s+in|$)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, query, re.IGNORECASE)
            if match:
                name = match.group(1).strip()
                # Clean up the name
                name = re.sub(r'\b(app|application|project|system)\b', '', name, flags=re.IGNORECASE).strip()
                # Convert to title case and remove spaces
                name = ''.join(word.capitalize() for word in name.split())
                if name and len(name) > 2:
                    return name[:20] + 'App'
        
        # If no pattern matches, use the whole query after 'generate code'
        if 'generate code' in query.lower():
            name = query.lower().replace('generate code', '').strip()
            name = ''.join(word.capitalize() for word in name.split())
            if name:
                return name[:20] + 'App'
        
        return 'JarvisProject'
    
    def generate_code(self, request_info: Dict) -> Dict:
        return self._generate_project(request_info)
    
    def _generate_project(self, request_info: Dict) -> Dict:
        language = request_info['language']
        project_type = request_info['project_type']
        project_name = request_info['project_name']
        
        files = self._generate_project_files(request_info)
        
        return {
            'type': 'project',
            'project_name': project_name,
            'files': files,
            'language': language,
            'project_type': project_type
        }
    
    def _generate_project_files(self, request_info: Dict) -> Dict:
        files = {}
        language = request_info['language']
        project_type = request_info['project_type']
        project_name = request_info['project_name']
        
        files['README.md'] = self._generate_readme(project_name, project_type, language)
        
        if project_type == 'static' or language == 'html':
            files['index.html'] = self._generate_static_html(project_name, request_info['original_query'])
            files['style.css'] = self._generate_static_css()
            files['script.js'] = self._generate_static_js(project_name)
        elif language == 'javascript':
            files['server.js'] = self._generate_main_code(request_info)
            files['package.json'] = self._generate_package_json(project_name)
            if project_type != 'api':
                files['public/index.html'] = self._generate_html_template(project_name, request_info['original_query'])
                files['public/style.css'] = self._generate_css_styles()
        elif language == 'java':
            files['Main.java'] = self._generate_main_code(request_info)
            files['pom.xml'] = self._generate_maven_pom(project_name)
        elif language == 'csharp':
            files['Program.cs'] = self._generate_main_code(request_info)
            files[f'{project_name}.csproj'] = self._generate_csproj(project_name)
        elif language == 'php':
            files['index.php'] = self._generate_main_code(request_info)
            files['composer.json'] = self._generate_composer_json(project_name)
        elif language == 'python':
            files['app.py'] = self._generate_main_code(request_info)
            files['requirements.txt'] = self._generate_requirements(project_type)
            if project_type == 'web':
                files['templates/index.html'] = self._generate_html_template(project_name, request_info['original_query'])
                files['static/style.css'] = self._generate_css_styles()
        else:
            files['app.py'] = self._generate_main_code(request_info)
        
        return files
    
    def _generate_main_code(self, request_info: Dict) -> str:
        language = request_info['language']
        project_type = request_info['project_type']
        project_name = request_info['project_name']
        query = request_info['original_query']
        
        if language == 'python':
            return self._generate_python_code(project_name, query, project_type)
        elif language == 'javascript':
            return self._generate_javascript_code(project_name, query, project_type)
        elif language == 'java':
            return self._generate_java_code(project_name, query, project_type)
        elif language == 'csharp':
            return self._generate_csharp_code(project_name, query, project_type)
        elif language == 'php':
            return self._generate_php_code(project_name, query, project_type)
        else:
            return self._generate_python_code(project_name, query, project_type)
    
    def _generate_python_code(self, project_name: str, query: str = '', project_type: str = 'web') -> str:
        return self._generate_advanced_python_app(project_name, query, project_type)
    
    def _python_flask_app(self, project_name: str, query: str = '') -> str:
        # Generate code based on project name/type
        query_and_name = (query + ' ' + project_name).lower()
        
        if 'calculator' in query_and_name:
            return '''from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.json
        num1 = float(data['num1'])
        num2 = float(data['num2'])
        operation = data['operation']
        
        if operation == '+':
            result = num1 + num2
        elif operation == '-':
            result = num1 - num2
        elif operation == '*':
            result = num1 * num2
        elif operation == '/':
            result = num1 / num2 if num2 != 0 else "Cannot divide by zero"
        else:
            result = "Invalid operation"
            
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
'''
        elif 'library' in query.lower() and 'management' in query.lower():
            return '''from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from datetime import datetime, date, timedelta

app = Flask(__name__)
app.secret_key = 'library_secret'

def init_db():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    
    # Create users table
    c.execute("""CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE NOT NULL,
                  password TEXT NOT NULL,
                  role TEXT DEFAULT 'user',
                  name TEXT NOT NULL)""")
    
    # Create books table
    c.execute("""CREATE TABLE IF NOT EXISTS books
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  title TEXT NOT NULL,
                  author TEXT NOT NULL,
                  isbn TEXT UNIQUE,
                  category TEXT,
                  total_copies INTEGER DEFAULT 1,
                  available_copies INTEGER DEFAULT 1)""")
    
    # Create issued_books table
    c.execute("""CREATE TABLE IF NOT EXISTS issued_books
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  book_id INTEGER,
                  user_id INTEGER,
                  issue_date TEXT NOT NULL,
                  due_date TEXT NOT NULL,
                  return_date TEXT,
                  status TEXT DEFAULT 'issued')""")
    
    # Insert sample data
    c.execute("INSERT OR IGNORE INTO users (username, password, role, name) VALUES (?, ?, ?, ?)", 
              ('admin', 'admin123', 'admin', 'Administrator'))
    c.execute("INSERT OR IGNORE INTO users (username, password, role, name) VALUES (?, ?, ?, ?)", 
              ('user1', 'user123', 'user', 'John Doe'))
    c.execute("INSERT OR IGNORE INTO books (title, author, isbn, category, total_copies, available_copies) VALUES (?, ?, ?, ?, ?, ?)", 
              ('Python Programming', 'John Smith', '978-0123456789', 'Programming', 5, 5))
    
    conn.commit()
    conn.close()

@app.route('/')
def login():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    user = c.fetchone()
    conn.close()
    if user:
        session['user_id'] = user[0]
        session['username'] = user[1]
        session['role'] = user[3]
        return redirect('/dashboard')
    return redirect('/')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    search = request.args.get('search', '')
    sort_by = request.args.get('sort', 'title')
    query = 'SELECT * FROM books WHERE available_copies > 0'
    params = []
    if search:
        query += ' AND (title LIKE ? OR author LIKE ?)'
        params.extend([f'%{search}%', f'%{search}%'])
    if sort_by in ['title', 'author', 'category']:
        query += f' ORDER BY {sort_by}'
    c.execute(query, params)
    books = c.fetchall()
    conn.close()
    return render_template('dashboard.html', books=books, search=search, sort_by=sort_by)

@app.route('/issue/<int:book_id>')
def issue_book(book_id):
    if 'user_id' not in session:
        return redirect('/')
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute('SELECT available_copies FROM books WHERE id = ?', (book_id,))
    book = c.fetchone()
    if book and book[0] > 0:
        issue_date = date.today().strftime('%Y-%m-%d')
        due_date = (date.today() + timedelta(days=14)).strftime('%Y-%m-%d')
        c.execute('INSERT INTO issued_books (book_id, user_id, issue_date, due_date) VALUES (?, ?, ?, ?)', 
                  (book_id, session['user_id'], issue_date, due_date))
        c.execute('UPDATE books SET available_copies = available_copies - 1 WHERE id = ?', (book_id,))
        conn.commit()
    conn.close()
    return redirect('/dashboard')

@app.route('/return/<int:issue_id>')
def return_book(issue_id):
    if 'user_id' not in session:
        return redirect('/')
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute('SELECT book_id FROM issued_books WHERE id = ? AND user_id = ?', (issue_id, session['user_id']))
    result = c.fetchone()
    if result:
        book_id = result[0]
        return_date = date.today().strftime('%Y-%m-%d')
        c.execute('UPDATE issued_books SET return_date = ?, status = "returned" WHERE id = ?', (return_date, issue_id))
        c.execute('UPDATE books SET available_copies = available_copies + 1 WHERE id = ?', (book_id,))
        conn.commit()
    conn.close()
    return redirect('/dashboard')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
'''
        elif 'student' in query.lower() and 'management' in query.lower():
            return '''from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'student_secret'

def init_db():
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS students
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  student_id TEXT UNIQUE,
                  name TEXT NOT NULL,
                  email TEXT,
                  course TEXT,
                  year INTEGER,
                  gpa REAL DEFAULT 0.0)""")
    conn.commit()
    conn.close()

@app.route('/')
def dashboard():
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute('SELECT * FROM students ORDER BY name')
    students = c.fetchall()
    conn.close()
    return render_template('index.html', students=students)

@app.route('/add', methods=['POST'])
def add_student():
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute('INSERT INTO students (student_id, name, email, course, year, gpa) VALUES (?, ?, ?, ?, ?, ?)',
             (request.form['student_id'], request.form['name'], request.form['email'],
              request.form['course'], int(request.form['year']), float(request.form['gpa'])))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
'''
        elif 'todo' in query.lower():
            return '''from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS tasks
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  title TEXT NOT NULL,
                  description TEXT,
                  priority TEXT DEFAULT 'medium',
                  status TEXT DEFAULT 'pending',
                  created_date TEXT)""")
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute('SELECT * FROM tasks ORDER BY priority DESC')
    tasks = c.fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute('INSERT INTO tasks (title, description, priority, created_date) VALUES (?, ?, ?, ?)',
             (request.form['title'], request.form['description'], 
              request.form['priority'], datetime.now().strftime('%Y-%m-%d')))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
'''
        else:
            # Generate advanced Flask app based on detailed user requirements
            return self._generate_advanced_flask_app(project_name, query)
    
    def _generate_html_template(self, project_name: str, query: str = '') -> str:
        if 'calculator' in query.lower():
            return '''<!DOCTYPE html>
<html>
<head>
    <title>Calculator App</title>
    <link rel="stylesheet" href="/static/style.css">
</head>
<body>
    <div class="calculator">
        <h1>Calculator</h1>
        <div class="display">
            <input type="text" id="result" readonly>
        </div>
        <div class="buttons">
            <button onclick="clearDisplay()">C</button>
            <button onclick="appendToDisplay('/')">/</button>
            <button onclick="appendToDisplay('*')">*</button>
            <button onclick="deleteLast()">←</button>
            
            <button onclick="appendToDisplay('7')">7</button>
            <button onclick="appendToDisplay('8')">8</button>
            <button onclick="appendToDisplay('9')">9</button>
            <button onclick="appendToDisplay('-')">-</button>
            
            <button onclick="appendToDisplay('4')">4</button>
            <button onclick="appendToDisplay('5')">5</button>
            <button onclick="appendToDisplay('6')">6</button>
            <button onclick="appendToDisplay('+')">+</button>
            
            <button onclick="appendToDisplay('1')">1</button>
            <button onclick="appendToDisplay('2')">2</button>
            <button onclick="appendToDisplay('3')">3</button>
            <button onclick="calculate()" rowspan="2">=</button>
            
            <button onclick="appendToDisplay('0')" colspan="2">0</button>
            <button onclick="appendToDisplay('.')">,</button>
        </div>
    </div>
    
    <script>
        let display = document.getElementById('result');
        
        function appendToDisplay(value) {
            display.value += value;
        }
        
        function clearDisplay() {
            display.value = '';
        }
        
        function deleteLast() {
            display.value = display.value.slice(0, -1);
        }
        
        function calculate() {
            try {
                display.value = eval(display.value);
            } catch (error) {
                display.value = 'Error';
            }
        }
    </script>
</body>
</html>'''
        elif 'library' in query.lower():
            return '''<!DOCTYPE html>
<html>
<head>
    <title>Library Management System</title>
    <link rel="stylesheet" href="/static/style.css">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>
    <div class="login-container">
        <div class="login-card">
            <h1>Library Management System</h1>
            <form method="POST" action="/login">
                <input type="text" name="username" placeholder="Username" required>
                <input type="password" name="password" placeholder="Password" required>
                <button type="submit" class="btn-primary">Login</button>
            </form>
            <div class="demo-info">
                <p>Demo Accounts:</p>
                <p>Admin: admin / admin123</p>
                <p>User: user1 / user123</p>
            </div>
        </div>
    </div>
</body>
</html>'''
        elif 'student' in query.lower() and 'management' in query.lower():
            return '''<!DOCTYPE html>
<html>
<head>
    <title>Student Management System</title>
    <link rel="stylesheet" href="/static/style.css">
</head>
<body>
    <div class="container">
        <h1>Student Management System</h1>
        
        <div class="add-student">
            <h2>Add New Student</h2>
            <form method="POST" action="/add">
                <input type="text" name="student_id" placeholder="Student ID" required>
                <input type="text" name="name" placeholder="Full Name" required>
                <input type="email" name="email" placeholder="Email">
                <input type="text" name="course" placeholder="Course" required>
                <input type="number" name="year" placeholder="Year" min="1" max="4" required>
                <input type="number" name="gpa" placeholder="GPA" step="0.01" min="0" max="4">
                <button type="submit">Add Student</button>
            </form>
        </div>
        
        <div class="students-list">
            <h2>Students List</h2>
            <table>
                <thead>
                    <tr>
                        <th>Student ID</th>
                        <th>Name</th>
                        <th>Email</th>
                        <th>Course</th>
                        <th>Year</th>
                        <th>GPA</th>
                    </tr>
                </thead>
                <tbody>
                    {% for student in students %}
                    <tr>
                        <td>{{ student[1] }}</td>
                        <td>{{ student[2] }}</td>
                        <td>{{ student[3] }}</td>
                        <td>{{ student[4] }}</td>
                        <td>{{ student[5] }}</td>
                        <td>{{ student[6] }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
</body>
</html>'''
        elif 'todo' in query.lower():
            return '''<!DOCTYPE html>
<html>
<head>
    <title>Todo List Manager</title>
    <link rel="stylesheet" href="/static/style.css">
</head>
<body>
    <div class="container">
        <h1>Todo List Manager</h1>
        
        <div class="add-task">
            <h2>Add New Task</h2>
            <form method="POST" action="/add">
                <input type="text" name="title" placeholder="Task Title" required>
                <textarea name="description" placeholder="Description"></textarea>
                <select name="priority">
                    <option value="low">Low Priority</option>
                    <option value="medium" selected>Medium Priority</option>
                    <option value="high">High Priority</option>
                </select>
                <button type="submit">Add Task</button>
            </form>
        </div>
        
        <div class="tasks-list">
            <h2>Tasks</h2>
            {% for task in tasks %}
            <div class="task priority-{{ task[3] }}">
                <h3>{{ task[1] }}</h3>
                <p>{{ task[2] }}</p>
                <span class="priority">{{ task[3].title() }} Priority</span>
                <span class="status">{{ task[4].title() }}</span>
            </div>
            {% endfor %}
        </div>
    </div>
</body>
</html>'''
        else:
            return f'''<!DOCTYPE html>
<html>
<head>
    <title>{{{{ app_name }}}}</title>
    <link rel="stylesheet" href="/static/style.css">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>
    <div class="container">
        <header>
            <h1>{{{{ app_name }}}}</h1>
            <p>Complete Management System</p>
        </header>
        
        <div class="add-section">
            <h2>Add New Item</h2>
            <form method="POST" action="/add" class="add-form">
                <input type="text" name="name" placeholder="Name" required>
                <textarea name="description" placeholder="Description"></textarea>
                <input type="text" name="category" placeholder="Category">
                <button type="submit" class="btn-primary">Add Item</button>
            </form>
        </div>
        
        <div class="items-section">
            <h2>Items List</h2>
            <div class="items-grid">
                {{% for item in items %}}
                <div class="item-card">
                    <h3>{{{{ item[1] }}}}</h3>
                    <p>{{{{ item[2] or 'No description' }}}}</p>
                    <div class="item-meta">
                        <span class="category">{{{{ item[3] }}}}</span>
                        <span class="date">{{{{ item[5] }}}}</span>
                    </div>
                    <div class="item-actions">
                        <a href="/delete/{{{{ item[0] }}}}" class="btn-delete" onclick="return confirm('Delete this item?')">Delete</a>
                    </div>
                </div>
                {{% endfor %}}
            </div>
            
            {{% if not items %}}
            <div class="empty-state">
                <p>No items found. Add your first item above!</p>
            </div>
            {{% endif %}}
        </div>
    </div>
    
    <script>
        // Add some interactivity
        document.addEventListener('DOMContentLoaded', function() {{
            console.log('{{{{ app_name }}}} loaded successfully!');
        }});
    </script>
</body>
</html>'''
    
    def _generate_dashboard_template(self) -> str:
        return '''<!DOCTYPE html>
<html>
<head>
    <title>Library Dashboard</title>
    <link rel="stylesheet" href="/static/style.css">
</head>
<body>
    <div class="dashboard">
        <div class="sidebar">
            <h2>Library System</h2>
            <nav>
                <a href="/dashboard">Books</a>
                <a href="/my-books">My Books</a>
                <a href="/logout">Logout</a>
            </nav>
        </div>
        <div class="main-content">
            <div class="search-bar">
                <form method="GET">
                    <input type="text" name="search" placeholder="Search books..." value="{{ search }}">
                    <select name="sort">
                        <option value="title" {% if sort_by == 'title' %}selected{% endif %}>Title</option>
                        <option value="author" {% if sort_by == 'author' %}selected{% endif %}>Author</option>
                        <option value="category" {% if sort_by == 'category' %}selected{% endif %}>Category</option>
                    </select>
                    <button type="submit">Search</button>
                </form>
            </div>
            <div class="books-grid">
                {% for book in books %}
                <div class="book-card">
                    <h3>{{ book[1] }}</h3>
                    <p>Author: {{ book[2] }}</p>
                    <p>Category: {{ book[4] }}</p>
                    <p>Available: {{ book[6] }}/{{ book[5] }}</p>
                    <a href="/issue/{{ book[0] }}" class="btn-issue">Issue Book</a>
                </div>
                {% endfor %}
            </div>
        </div>
    </div>
</body>
</html>'''
    
    def _generate_css_styles(self) -> str:
        return '''body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 0;
    background-color: #f5f5f5;
}

.login-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
}

.login-card {
    background: white;
    padding: 40px;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    width: 300px;
}

.login-card h1 {
    text-align: center;
    color: #333;
    margin-bottom: 30px;
}

.login-card input {
    width: 100%;
    padding: 12px;
    margin: 10px 0;
    border: 1px solid #ddd;
    border-radius: 4px;
    box-sizing: border-box;
}

.btn-primary {
    width: 100%;
    padding: 12px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 16px;
}

.btn-primary:hover {
    background-color: #0056b3;
}

.demo-info {
    margin-top: 20px;
    padding: 15px;
    background-color: #f8f9fa;
    border-radius: 4px;
    font-size: 14px;
}

.dashboard {
    display: flex;
    height: 100vh;
}

.sidebar {
    width: 250px;
    background-color: #343a40;
    color: white;
    padding: 20px;
}

.sidebar h2 {
    margin-bottom: 30px;
}

.sidebar nav a {
    display: block;
    color: white;
    text-decoration: none;
    padding: 10px 0;
    border-bottom: 1px solid #495057;
}

.sidebar nav a:hover {
    background-color: #495057;
    padding-left: 10px;
}

.main-content {
    flex: 1;
    padding: 20px;
}

.search-bar {
    background: white;
    padding: 20px;
    border-radius: 8px;
    margin-bottom: 20px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.search-bar form {
    display: flex;
    gap: 10px;
    align-items: center;
}

.search-bar input, .search-bar select {
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
}

.search-bar button {
    padding: 10px 20px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

.books-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 20px;
}

.book-card {
    background: white;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.book-card h3 {
    margin-top: 0;
    color: #333;
}

.btn-issue {
    display: inline-block;
    padding: 8px 16px;
    background-color: #28a745;
    color: white;
    text-decoration: none;
    border-radius: 4px;
    margin-top: 10px;
}

.btn-issue:hover {
    background-color: #218838;
}'''
    
    def _generate_readme(self, project_name: str, project_type: str, language: str) -> str:
        return f'''# {project_name}

Generated by Jarvis Auto Code Architect

## Description
A {project_type} application built with {language.title()}.

## Installation

### Requirements
- {language.title()} (latest version recommended)

### Setup
1. Clone or download this project
2. Navigate to the project directory
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Run the main application:
```bash
python app.py
```

## Features
- Modern {project_type} interface
- Cross-platform compatibility
- Easy to extend and customize

## Generated by
Jarvis AI Assistant - Auto Code Architect
'''
    
    def _generate_static_html(self, project_name: str, query: str = '') -> str:
        """Generate advanced static HTML based on user requirements"""
        query_lower = query.lower()
        features = self._analyze_requirements(query_lower)
        
        # Determine project type
        if 'portfolio' in query_lower:
            return self._generate_portfolio_html(project_name, features)
        elif 'ecommerce' in query_lower or 'shop' in query_lower:
            return self._generate_portfolio_html(project_name, features)
        elif 'blog' in query_lower:
            return self._generate_portfolio_html(project_name, features)
        elif 'landing' in query_lower:
            return self._generate_portfolio_html(project_name, features)
        else:
            return self._generate_portfolio_html(project_name, features)
    
    def _generate_portfolio_html(self, project_name: str, features: dict) -> str:
        return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{project_name}</title>
    <link rel="stylesheet" href="style.css">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar">
        <div class="nav-container">
            <div class="nav-logo">
                <h2>Portfolio</h2>
            </div>
            <div class="nav-menu" id="nav-menu">
                <a href="#home" class="nav-link">Home</a>
                <a href="#about" class="nav-link">About</a>
                <a href="#skills" class="nav-link">Skills</a>
                <a href="#projects" class="nav-link">Projects</a>
                <a href="#contact" class="nav-link">Contact</a>
                {"<button class='theme-toggle' id='theme-toggle'><i class='fas fa-moon'></i></button>" if features['responsive'] else ""}
            </div>
            <div class="nav-toggle" id="nav-toggle">
                <span class="bar"></span>
                <span class="bar"></span>
                <span class="bar"></span>
            </div>
        </div>
    </nav>

    <!-- Hero Section -->
    <section id="home" class="hero">
        <div class="hero-container">
            <div class="hero-content">
                <h1 class="hero-title">Hi, I'm <span class="highlight">John Doe</span></h1>
                <p class="hero-subtitle">Full Stack Developer & UI/UX Designer</p>
                <p class="hero-description">I create amazing digital experiences that make people's lives easier.</p>
                <div class="hero-buttons">
                    <a href="#projects" class="btn btn-primary">View My Work</a>
                    <a href="#contact" class="btn btn-secondary">Get In Touch</a>
                </div>
            </div>
            <div class="hero-image">
                <div class="image-placeholder">
                    <i class="fas fa-user-circle"></i>
                </div>
            </div>
        </div>
    </section>

    <!-- About Section -->
    <section id="about" class="about">
        <div class="container">
            <h2 class="section-title">About Me</h2>
            <div class="about-content">
                <div class="about-text">
                    <p>I'm a passionate developer with 5+ years of experience creating web applications and user interfaces. I love turning complex problems into simple, beautiful designs.</p>
                    <div class="stats">
                        <div class="stat">
                            <h3>50+</h3>
                            <p>Projects Completed</p>
                        </div>
                        <div class="stat">
                            <h3>5+</h3>
                            <p>Years Experience</p>
                        </div>
                        <div class="stat">
                            <h3>100+</h3>
                            <p>Happy Clients</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Skills Section -->
    <section id="skills" class="skills">
        <div class="container">
            <h2 class="section-title">Skills & Technologies</h2>
            <div class="skills-grid">
                <div class="skill-card">
                    <i class="fab fa-html5"></i>
                    <h3>Frontend</h3>
                    <p>HTML5, CSS3, JavaScript, React, Vue.js</p>
                </div>
                <div class="skill-card">
                    <i class="fas fa-server"></i>
                    <h3>Backend</h3>
                    <p>Node.js, Python, PHP, Java, .NET</p>
                </div>
                <div class="skill-card">
                    <i class="fas fa-database"></i>
                    <h3>Database</h3>
                    <p>MySQL, PostgreSQL, MongoDB, SQLite</p>
                </div>
                <div class="skill-card">
                    <i class="fas fa-tools"></i>
                    <h3>Tools</h3>
                    <p>Git, Docker, AWS, Figma, Photoshop</p>
                </div>
            </div>
        </div>
    </section>

    <!-- Projects Section -->
    <section id="projects" class="projects">
        <div class="container">
            <h2 class="section-title">Featured Projects</h2>
            <div class="projects-grid">
                <div class="project-card">
                    <div class="project-image">
                        <div class="image-placeholder">
                            <i class="fas fa-image"></i>
                        </div>
                        <div class="project-overlay">
                            <a href="#" class="project-link"><i class="fas fa-external-link-alt"></i></a>
                            <a href="#" class="project-link"><i class="fab fa-github"></i></a>
                        </div>
                    </div>
                    <div class="project-content">
                        <h3>E-Commerce Platform</h3>
                        <p>Full-stack e-commerce solution with React and Node.js</p>
                        <div class="project-tech">
                            <span>React</span>
                            <span>Node.js</span>
                            <span>MongoDB</span>
                        </div>
                    </div>
                </div>
                
                <div class="project-card">
                    <div class="project-image">
                        <div class="image-placeholder">
                            <i class="fas fa-image"></i>
                        </div>
                        <div class="project-overlay">
                            <a href="#" class="project-link"><i class="fas fa-external-link-alt"></i></a>
                            <a href="#" class="project-link"><i class="fab fa-github"></i></a>
                        </div>
                    </div>
                    <div class="project-content">
                        <h3>Task Management App</h3>
                        <p>Collaborative task management with real-time updates</p>
                        <div class="project-tech">
                            <span>Vue.js</span>
                            <span>Firebase</span>
                            <span>CSS3</span>
                        </div>
                    </div>
                </div>
                
                <div class="project-card">
                    <div class="project-image">
                        <div class="image-placeholder">
                            <i class="fas fa-image"></i>
                        </div>
                        <div class="project-overlay">
                            <a href="#" class="project-link"><i class="fas fa-external-link-alt"></i></a>
                            <a href="#" class="project-link"><i class="fab fa-github"></i></a>
                        </div>
                    </div>
                    <div class="project-content">
                        <h3>Weather Dashboard</h3>
                        <p>Beautiful weather app with location-based forecasts</p>
                        <div class="project-tech">
                            <span>JavaScript</span>
                            <span>API</span>
                            <span>Chart.js</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Contact Section -->
    <section id="contact" class="contact">
        <div class="container">
            <h2 class="section-title">Get In Touch</h2>
            <div class="contact-content">
                <div class="contact-info">
                    <div class="contact-item">
                        <i class="fas fa-envelope"></i>
                        <div>
                            <h3>Email</h3>
                            <p>john.doe@example.com</p>
                        </div>
                    </div>
                    <div class="contact-item">
                        <i class="fas fa-phone"></i>
                        <div>
                            <h3>Phone</h3>
                            <p>+1 (555) 123-4567</p>
                        </div>
                    </div>
                    <div class="contact-item">
                        <i class="fas fa-map-marker-alt"></i>
                        <div>
                            <h3>Location</h3>
                            <p>New York, NY</p>
                        </div>
                    </div>
                </div>
                
                <form class="contact-form" id="contact-form">
                    <div class="form-group">
                        <input type="text" id="name" name="name" placeholder="Your Name" required>
                    </div>
                    <div class="form-group">
                        <input type="email" id="email" name="email" placeholder="Your Email" required>
                    </div>
                    <div class="form-group">
                        <input type="text" id="subject" name="subject" placeholder="Subject" required>
                    </div>
                    <div class="form-group">
                        <textarea id="message" name="message" placeholder="Your Message" rows="5" required></textarea>
                    </div>
                    <button type="submit" class="btn btn-primary">Send Message</button>
                </form>
            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer class="footer">
        <div class="container">
            <div class="footer-content">
                <p>&copy; 2024 John Doe. All rights reserved.</p>
                <div class="social-links">
                    <a href="#"><i class="fab fa-linkedin"></i></a>
                    <a href="#"><i class="fab fa-github"></i></a>
                    <a href="#"><i class="fab fa-twitter"></i></a>
                    <a href="#"><i class="fab fa-instagram"></i></a>
                </div>
            </div>
        </div>
    </footer>
        
        <div class="add-section">
            <h2>Add New Item</h2>
            <form id="addForm" class="add-form">
                <input type="text" id="itemName" placeholder="Item Name" required>
                <input type="text" id="itemCategory" placeholder="Category">
                <input type="number" id="itemQuantity" placeholder="Quantity" min="0">
                <input type="number" id="itemPrice" placeholder="Price" step="0.01" min="0">
                <textarea id="itemDescription" placeholder="Description"></textarea>
                <button type="submit" class="btn-primary">Add Item</button>
            </form>
        </div>
        
        <div class="items-section">
            <h2>Items List</h2>
            <div class="search-bar">
                <input type="text" id="searchInput" placeholder="Search items...">
                <select id="categoryFilter">
                    <option value="">All Categories</option>
                </select>
            </div>
            <div id="itemsList" class="items-grid">
                <!-- Items will be populated by JavaScript -->
            </div>
            <div id="emptyState" class="empty-state">
                <p>No items found. Add your first item above!</p>
            </div>
        </div>
    </div>
    
    <script src="script.js"></script>
</body>
</html>'''
    
    def _generate_static_css(self) -> str:
        return '''* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    padding: 20px;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    background: white;
    border-radius: 15px;
    box-shadow: 0 20px 40px rgba(0,0,0,0.1);
    overflow: hidden;
}

header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 40px;
    text-align: center;
}

header h1 {
    font-size: 2.5rem;
    margin-bottom: 10px;
}

header p {
    font-size: 1.2rem;
    opacity: 0.9;
}

.add-section {
    padding: 40px;
    background: #f8f9fa;
    border-bottom: 1px solid #e9ecef;
}

.add-section h2 {
    margin-bottom: 20px;
    color: #333;
}

.add-form {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 15px;
    align-items: end;
}

.add-form input,
.add-form textarea,
.add-form select {
    padding: 12px;
    border: 2px solid #e9ecef;
    border-radius: 8px;
    font-size: 16px;
    transition: border-color 0.3s;
}

.add-form input:focus,
.add-form textarea:focus {
    outline: none;
    border-color: #667eea;
}

.add-form textarea {
    grid-column: 1 / -1;
    resize: vertical;
    min-height: 80px;
}

.btn-primary {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    padding: 12px 24px;
    border-radius: 8px;
    font-size: 16px;
    cursor: pointer;
    transition: transform 0.2s;
}

.btn-primary:hover {
    transform: translateY(-2px);
}

.items-section {
    padding: 40px;
}

.items-section h2 {
    margin-bottom: 20px;
    color: #333;
}

.search-bar {
    display: flex;
    gap: 15px;
    margin-bottom: 30px;
}

.search-bar input,
.search-bar select {
    padding: 10px;
    border: 2px solid #e9ecef;
    border-radius: 8px;
    font-size: 14px;
}

.search-bar input {
    flex: 1;
}

.items-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 20px;
}

.item-card {
    background: white;
    border: 2px solid #e9ecef;
    border-radius: 12px;
    padding: 20px;
    transition: all 0.3s;
    position: relative;
}

.item-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    border-color: #667eea;
}

.item-card h3 {
    color: #333;
    margin-bottom: 10px;
    font-size: 1.3rem;
}

.item-card p {
    color: #666;
    margin-bottom: 15px;
    line-height: 1.5;
}

.item-meta {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 15px;
}

.category {
    background: #667eea;
    color: white;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: bold;
}

.quantity {
    background: #28a745;
    color: white;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: bold;
}

.price {
    background: #ffc107;
    color: #333;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: bold;
}

.item-actions {
    display: flex;
    gap: 10px;
}

.btn-delete {
    background: #dc3545;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 6px;
    font-size: 14px;
    cursor: pointer;
    text-decoration: none;
    transition: background 0.2s;
}

.btn-delete:hover {
    background: #c82333;
}

.empty-state {
    text-align: center;
    padding: 60px 20px;
    color: #666;
    font-size: 1.1rem;
}

@media (max-width: 768px) {
    .add-form {
        grid-template-columns: 1fr;
    }
    
    .search-bar {
        flex-direction: column;
    }
    
    .items-grid {
        grid-template-columns: 1fr;
    }
}'''
    
    def _generate_javascript_code(self, project_name: str, query: str = '', project_type: str = 'web') -> str:
        return self._generate_advanced_javascript_app(project_name, query, project_type)
    
    def _generate_java_code(self, project_name: str, query: str = '', project_type: str = 'web') -> str:
        return self._generate_advanced_java_app(project_name, query, project_type)
    
    def _generate_spring_boot(self, project_name: str, query: str = '') -> str:
        class_name = project_name.replace('App', '').replace(' ', '')
        return f'''package com.jarvis.{class_name.lower()};

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.*;
import org.springframework.stereotype.Service;
import java.util.*;
import java.time.LocalDateTime;

@SpringBootApplication
public class {class_name}Application {{
    public static void main(String[] args) {{
        SpringApplication.run({class_name}Application.class, args);
    }}
}}

@RestController
@RequestMapping("/api")
class {class_name}Controller {{
    private final {class_name}Service service;
    
    public {class_name}Controller({class_name}Service service) {{
        this.service = service;
    }}
    
    @GetMapping("/items")
    public List<Item> getAllItems() {{
        return service.getAllItems();
    }}
    
    @PostMapping("/items")
    public Item createItem(@RequestBody Item item) {{
        return service.createItem(item);
    }}
    
    @DeleteMapping("/items/{{id}}")
    public void deleteItem(@PathVariable Long id) {{
        service.deleteItem(id);
    }}
}}

@Service
class {class_name}Service {{
    private List<Item> items = new ArrayList<>();
    private Long nextId = 1L;
    
    public List<Item> getAllItems() {{
        return items;
    }}
    
    public Item createItem(Item item) {{
        item.setId(nextId++);
        item.setCreatedAt(LocalDateTime.now());
        items.add(item);
        return item;
    }}
    
    public void deleteItem(Long id) {{
        items.removeIf(item -> item.getId().equals(id));
    }}
}}

class Item {{
    private Long id;
    private String name;
    private String description;
    private String category;
    private LocalDateTime createdAt;
    
    // Constructors
    public Item() {{}}
    
    public Item(String name, String description, String category) {{
        this.name = name;
        this.description = description;
        this.category = category;
    }}
    
    // Getters and Setters
    public Long getId() {{ return id; }}
    public void setId(Long id) {{ this.id = id; }}
    
    public String getName() {{ return name; }}
    public void setName(String name) {{ this.name = name; }}
    
    public String getDescription() {{ return description; }}
    public void setDescription(String description) {{ this.description = description; }}
    
    public String getCategory() {{ return category; }}
    public void setCategory(String category) {{ this.category = category; }}
    
    public LocalDateTime getCreatedAt() {{ return createdAt; }}
    public void setCreatedAt(LocalDateTime createdAt) {{ this.createdAt = createdAt; }}
}}'''
    
    def _generate_advanced_flask_app(self, project_name: str, query: str = '') -> str:
        """Generate advanced Flask app based on user requirements"""
        query_lower = query.lower()
        
        # Analyze requirements
        has_auth = any(word in query_lower for word in ['login', 'register', 'user', 'auth', 'account'])
        has_charts = any(word in query_lower for word in ['chart', 'graph', 'visualization', 'analytics'])
        has_api = any(word in query_lower for word in ['api', 'rest', 'json'])
        has_file_upload = any(word in query_lower for word in ['upload', 'file', 'image'])
        has_email = any(word in query_lower for word in ['email', 'notification', 'mail'])
        has_search = any(word in query_lower for word in ['search', 'filter', 'find'])
        has_export = any(word in query_lower for word in ['export', 'pdf', 'csv', 'download'])
        
        # Determine database schema based on context
        if 'expense' in query_lower or 'finance' in query_lower:
            db_schema = self._get_expense_schema()
            routes = self._get_expense_routes()
        elif 'inventory' in query_lower or 'stock' in query_lower:
            db_schema = self._get_inventory_schema()
            routes = self._get_inventory_routes()
        elif 'student' in query_lower or 'school' in query_lower:
            db_schema = self._get_student_schema()
            routes = self._get_student_routes()
        elif 'employee' in query_lower or 'hr' in query_lower:
            db_schema = self._get_employee_schema()
            routes = self._get_employee_routes()
        else:
            db_schema = self._get_generic_schema()
            routes = self._get_generic_routes()
        
        # Generate imports based on features
        imports = ['from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, session']
        imports.append('import sqlite3')
        imports.append('from datetime import datetime, date')
        imports.append('import os')
        
        if has_auth:
            imports.append('from werkzeug.security import generate_password_hash, check_password_hash')
        if has_file_upload:
            imports.append('from werkzeug.utils import secure_filename')
        if has_email:
            imports.append('from flask_mail import Mail, Message')
        if has_export:
            imports.append('import csv')
            imports.append('import io')
        
        app_name = project_name.replace('App', '').lower()
        
        return f'''{"; ".join(imports)}

app = Flask(__name__)
app.secret_key = '{app_name}_secret_key_change_in_production'

# Configuration
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

{"# Email configuration" if has_email else ""}
{"app.config['MAIL_SERVER'] = 'smtp.gmail.com'" if has_email else ""}
{"app.config['MAIL_PORT'] = 587" if has_email else ""}
{"app.config['MAIL_USE_TLS'] = True" if has_email else ""}
{"mail = Mail(app)" if has_email else ""}

def init_db():
    conn = sqlite3.connect('{app_name}.db')
    c = conn.cursor()
    
{db_schema}
    
    conn.commit()
    conn.close()

{routes}

{self._get_auth_routes() if has_auth else ""}

{self._get_api_routes(app_name) if has_api else ""}

{self._get_chart_routes() if has_charts else ""}

{self._get_export_routes(app_name) if has_export else ""}

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    init_db()
    app.run(debug=True)
'''
    
    def _get_expense_schema(self) -> str:
        return '''    # Users table
    c.execute("""CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE NOT NULL,
                  email TEXT UNIQUE NOT NULL,
                  password_hash TEXT NOT NULL,
                  created_date TEXT NOT NULL)""")
    
    # Categories table
    c.execute("""CREATE TABLE IF NOT EXISTS categories
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  type TEXT NOT NULL,
                  color TEXT DEFAULT '#007bff')""")
    
    # Transactions table
    c.execute("""CREATE TABLE IF NOT EXISTS transactions
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  type TEXT NOT NULL,
                  amount REAL NOT NULL,
                  category_id INTEGER,
                  description TEXT,
                  date TEXT NOT NULL,
                  created_date TEXT NOT NULL,
                  FOREIGN KEY (user_id) REFERENCES users (id),
                  FOREIGN KEY (category_id) REFERENCES categories (id))""")
    
    # Insert default categories
    categories = [
        ('Food & Dining', 'expense', '#ff6b6b'),
        ('Transportation', 'expense', '#4ecdc4'),
        ('Shopping', 'expense', '#45b7d1'),
        ('Entertainment', 'expense', '#96ceb4'),
        ('Bills & Utilities', 'expense', '#feca57'),
        ('Salary', 'income', '#48dbfb'),
        ('Freelance', 'income', '#0abde3'),
        ('Investment', 'income', '#006ba6')
    ]
    c.executemany('INSERT OR IGNORE INTO categories (name, type, color) VALUES (?, ?, ?)', categories)'''
    
    def _get_expense_routes(self) -> str:
        return '''@app.route('/')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('{app_name}.db')
    c = conn.cursor()
    
    # Get current month transactions
    current_month = datetime.now().strftime('%Y-%m')
    c.execute("""SELECT t.*, cat.name as category_name, cat.color 
                 FROM transactions t 
                 JOIN categories cat ON t.category_id = cat.id 
                 WHERE t.user_id = ? AND t.date LIKE ?
                 ORDER BY t.date DESC""", (session['user_id'], f'{current_month}%'))
    transactions = c.fetchall()
    
    # Calculate totals
    c.execute("""SELECT 
                    SUM(CASE WHEN type = 'income' THEN amount ELSE 0 END) as total_income,
                    SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END) as total_expense
                 FROM transactions 
                 WHERE user_id = ? AND date LIKE ?""", (session['user_id'], f'{current_month}%'))
    totals = c.fetchone()
    
    # Get categories
    c.execute('SELECT * FROM categories ORDER BY type, name')
    categories = c.fetchall()
    
    conn.close()
    
    balance = (totals[0] or 0) - (totals[1] or 0)
    
    return render_template('dashboard.html', 
                         transactions=transactions,
                         categories=categories,
                         total_income=totals[0] or 0,
                         total_expense=totals[1] or 0,
                         balance=balance)

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('{app_name}.db')
    c = conn.cursor()
    c.execute("""INSERT INTO transactions 
                 (user_id, type, amount, category_id, description, date, created_date) 
                 VALUES (?, ?, ?, ?, ?, ?, ?)""",
             (session['user_id'], request.form['type'], float(request.form['amount']),
              int(request.form['category_id']), request.form.get('description', ''),
              request.form['date'], datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    conn.commit()
    conn.close()
    
    flash('Transaction added successfully!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/delete_transaction/<int:transaction_id>')
def delete_transaction(transaction_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('{app_name}.db')
    c = conn.cursor()
    c.execute('DELETE FROM transactions WHERE id = ? AND user_id = ?', 
             (transaction_id, session['user_id']))
    conn.commit()
    conn.close()
    
    flash('Transaction deleted successfully!', 'success')
    return redirect(url_for('dashboard'))'''
    
    def _generate_advanced_python_app(self, project_name: str, query: str = '', project_type: str = 'web') -> str:
        """Generate advanced Python app based on user requirements"""
        query_lower = query.lower()
        
        if 'fastapi' in query_lower or project_type == 'api':
            return self._python_flask_app(project_name, query)
        elif 'django' in query_lower:
            return self._python_flask_app(project_name, query)
        else:
            return self._python_flask_app(project_name, query)
    
    def _generate_advanced_javascript_app(self, project_name: str, query: str = '', project_type: str = 'web') -> str:
        """Generate advanced JavaScript app based on user requirements"""
        query_lower = query.lower()
        features = self._analyze_requirements(query_lower)
        
        if 'react' in query_lower:
            return self._generate_node_api(project_name, query)
        elif 'vue' in query_lower:
            return self._generate_node_api(project_name, query)
        elif 'node' in query_lower or project_type == 'api':
            return self._generate_node_api(project_name, query)
        else:
            return self._generate_node_api(project_name, query)
    
    def _generate_advanced_java_app(self, project_name: str, query: str = '', project_type: str = 'web') -> str:
        """Generate advanced Java app based on user requirements"""
        query_lower = query.lower()
        
        if 'spring' in query_lower:
            return self._generate_spring_boot(project_name, query)
        else:
            return self._java_console(project_name, query)
    
    def _analyze_requirements(self, query: str) -> dict:
        """Analyze user requirements and return feature flags"""
        return {
            'auth': any(word in query for word in ['login', 'register', 'user', 'auth', 'account', 'signin']),
            'database': any(word in query for word in ['database', 'sqlite', 'mysql', 'postgres', 'data', 'store']),
            'api': any(word in query for word in ['api', 'rest', 'json', 'endpoint']),
            'charts': any(word in query for word in ['chart', 'graph', 'visualization', 'analytics', 'dashboard']),
            'file_upload': any(word in query for word in ['upload', 'file', 'image', 'document']),
            'email': any(word in query for word in ['email', 'notification', 'mail', 'smtp']),
            'search': any(word in query for word in ['search', 'filter', 'find', 'query']),
            'export': any(word in query for word in ['export', 'pdf', 'csv', 'download', 'report']),
            'realtime': any(word in query for word in ['realtime', 'websocket', 'live', 'chat']),
            'payment': any(word in query for word in ['payment', 'stripe', 'paypal', 'billing']),
            'responsive': any(word in query for word in ['responsive', 'mobile', 'bootstrap', 'css']),
            'security': any(word in query for word in ['security', 'encryption', 'ssl', 'secure']),
            'testing': any(word in query for word in ['test', 'testing', 'unit test', 'pytest']),
            'deployment': any(word in query for word in ['deploy', 'docker', 'heroku', 'aws']),
            'admin': any(word in query for word in ['admin', 'management', 'dashboard', 'control panel'])
        }
    
    def _generate_fastapi_app_old(self, project_name: str, query: str, features: dict) -> str:
        """Generate advanced FastAPI application"""
        app_name = project_name.replace('App', '').lower()
        
        imports = ['from fastapi import FastAPI, HTTPException, Depends, status']
        imports.append('from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials')
        imports.append('from pydantic import BaseModel')
        imports.append('import sqlite3')
        imports.append('from datetime import datetime, timedelta')
        imports.append('import jwt')
        imports.append('import bcrypt')
        
        if features['file_upload']:
            imports.append('from fastapi import UploadFile, File')
        if features['email']:
            imports.append('import smtplib')
        if features['export']:
            imports.append('import pandas as pd')
        
        return f'''{chr(10).join(imports)}

app = FastAPI(title="{project_name}", description="Advanced {app_name} API")
security = HTTPBearer()

# Database setup
def init_db():
    conn = sqlite3.connect('{app_name}.db')
    c = conn.cursor()
    
    # Users table
    c.execute("""CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE NOT NULL,
                  email TEXT UNIQUE NOT NULL,
                  password_hash TEXT NOT NULL,
                  is_active BOOLEAN DEFAULT TRUE,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")
    
    # Main data table
    c.execute("""CREATE TABLE IF NOT EXISTS items
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  title TEXT NOT NULL,
                  description TEXT,
                  category TEXT,
                  status TEXT DEFAULT 'active',
                  metadata JSON,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  FOREIGN KEY (user_id) REFERENCES users (id))""")
    
    conn.commit()
    conn.close()

# Pydantic models
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class ItemCreate(BaseModel):
    title: str
    description: str = None
    category: str = "general"
    metadata: dict = {{}}

class ItemResponse(BaseModel):
    id: int
    title: str
    description: str
    category: str
    status: str
    created_at: str

# Authentication
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=24)
    to_encode.update({{"exp": expire}})
    return jwt.encode(to_encode, "secret_key", algorithm="HS256")

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, "secret_key", algorithms=["HS256"])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Routes
@app.post("/register")
def register(user: UserCreate):
    conn = sqlite3.connect('{app_name}.db')
    c = conn.cursor()
    
    # Hash password
    password_hash = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    
    try:
        c.execute("INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
                 (user.username, user.email, password_hash))
        conn.commit()
        return {{"message": "User created successfully"}}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Username or email already exists")
    finally:
        conn.close()

@app.post("/login")
def login(user: UserLogin):
    conn = sqlite3.connect('{app_name}.db')
    c = conn.cursor()
    c.execute("SELECT password_hash FROM users WHERE username = ?", (user.username,))
    result = c.fetchone()
    conn.close()
    
    if result and bcrypt.checkpw(user.password.encode('utf-8'), result[0]):
        access_token = create_access_token(data={{"sub": user.username}})
        return {{"access_token": access_token, "token_type": "bearer"}}
    
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/items", response_model=list[ItemResponse])
def get_items(current_user: str = Depends(get_current_user)):
    conn = sqlite3.connect('{app_name}.db')
    c = conn.cursor()
    c.execute("""SELECT i.* FROM items i 
                 JOIN users u ON i.user_id = u.id 
                 WHERE u.username = ? ORDER BY i.created_at DESC""", (current_user,))
    items = c.fetchall()
    conn.close()
    
    return [ItemResponse(
        id=item[0], title=item[2], description=item[3], 
        category=item[4], status=item[5], created_at=item[7]
    ) for item in items]

@app.post("/items")
def create_item(item: ItemCreate, current_user: str = Depends(get_current_user)):
    conn = sqlite3.connect('{app_name}.db')
    c = conn.cursor()
    
    # Get user ID
    c.execute("SELECT id FROM users WHERE username = ?", (current_user,))
    user_id = c.fetchone()[0]
    
    c.execute("""INSERT INTO items (user_id, title, description, category, metadata) 
                 VALUES (?, ?, ?, ?, ?)""",
             (user_id, item.title, item.description, item.category, str(item.metadata)))
    conn.commit()
    conn.close()
    
    return {{"message": "Item created successfully"}}

@app.delete("/items/{{item_id}}")
def delete_item(item_id: int, current_user: str = Depends(get_current_user)):
    conn = sqlite3.connect('{app_name}.db')
    c = conn.cursor()
    c.execute("""DELETE FROM items WHERE id = ? AND user_id = 
                 (SELECT id FROM users WHERE username = ?)""", (item_id, current_user))
    conn.commit()
    conn.close()
    
    return {{"message": "Item deleted successfully"}}

{"@app.get('/export/csv')" if features['export'] else ""}
{"def export_csv(current_user: str = Depends(get_current_user)):" if features['export'] else ""}
{"    # Export functionality here" if features['export'] else ""}
{"    pass" if features['export'] else ""}

if __name__ == "__main__":
    init_db()
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''
    
    def _get_generic_schema(self) -> str:
        return '''    c.execute("""CREATE TABLE IF NOT EXISTS items
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      name TEXT NOT NULL,
                      description TEXT,
                      category TEXT,
                      status TEXT DEFAULT 'active',
                      created_date TEXT NOT NULL)""")
'''
    
    def _get_generic_routes(self) -> str:
        return '''@app.route('/')
def index():
    return render_template('index.html')

@app.route('/items')
def items():
    conn = sqlite3.connect('{app_name}.db')
    c = conn.cursor()
    c.execute('SELECT * FROM items ORDER BY created_date DESC')
    items = c.fetchall()
    conn.close()
    return render_template('items.html', items=items)
'''
    
    def _get_auth_routes(self) -> str:
        return '''@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Login logic here
        pass
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Registration logic here
        pass
    return render_template('register.html')
'''
    
    def _get_api_routes(self, app_name: str) -> str:
        return f'''@app.route('/api/items')
def api_items():
    conn = sqlite3.connect('{app_name}.db')
    c = conn.cursor()
    c.execute('SELECT * FROM items')
    items = c.fetchall()
    conn.close()
    return jsonify(items)
'''
    
    def _get_chart_routes(self) -> str:
        return '''@app.route('/api/charts')
def chart_data():
    # Chart data logic here
    return jsonify({'data': []})
'''
    
    def _get_export_routes(self, app_name: str) -> str:
        return f'''@app.route('/export/csv')
def export_csv():
    # CSV export logic here
    return "CSV export"
'''
    
    def _java_console(self, project_name: str, query: str = '') -> str:
        class_name = project_name.replace('App', '').replace(' ', '')
        return f'''public class {class_name} {{
    public static void main(String[] args) {{
        System.out.println("Welcome to {project_name}!");
        
        // Add your implementation here
        {class_name}Manager manager = new {class_name}Manager();
        manager.start();
    }}
}}

class {class_name}Manager {{
    public void start() {{
        System.out.println("{project_name} is running...");
        // Implementation goes here
    }}
}}'''
    
    def _generate_csharp_code(self, project_name: str, query: str = '', project_type: str = 'web') -> str:
        if project_type == 'web':
            return self._generate_aspnet_core(project_name, query)
        else:
            return self._generate_csharp_console(project_name, query)
    
    def _generate_php_code(self, project_name: str, query: str = '', project_type: str = 'web') -> str:
        if 'laravel' in query.lower():
            return self._generate_laravel_app(project_name, query)
        else:
            return self._generate_php_app(project_name, query)
    
    def _generate_node_api(self, project_name: str, query: str = '') -> str:
        app_name = project_name.replace('App', '').lower()
        return f'''const express = require('express');
const cors = require('cors');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;
const DATA_FILE = '{app_name}_data.json';

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static('public'));

// Initialize data file
if (!fs.existsSync(DATA_FILE)) {{
    fs.writeFileSync(DATA_FILE, JSON.stringify([]));
}}

// Helper functions
const readData = () => {{
    try {{
        const data = fs.readFileSync(DATA_FILE, 'utf8');
        return JSON.parse(data);
    }} catch (error) {{
        return [];
    }}
}};

const writeData = (data) => {{
    fs.writeFileSync(DATA_FILE, JSON.stringify(data, null, 2));
}};

// Routes
app.get('/api/items', (req, res) => {{
    const items = readData();
    res.json(items);
}});

app.post('/api/items', (req, res) => {{
    const items = readData();
    const newItem = {{
        id: Date.now(),
        ...req.body,
        createdAt: new Date().toISOString()
    }};
    items.push(newItem);
    writeData(items);
    res.status(201).json(newItem);
}});

app.put('/api/items/:id', (req, res) => {{
    const items = readData();
    const itemId = parseInt(req.params.id);
    const itemIndex = items.findIndex(item => item.id === itemId);
    
    if (itemIndex === -1) {{
        return res.status(404).json({{ error: 'Item not found' }});
    }}
    
    items[itemIndex] = {{ ...items[itemIndex], ...req.body }};
    writeData(items);
    res.json(items[itemIndex]);
}});

app.delete('/api/items/:id', (req, res) => {{
    const items = readData();
    const itemId = parseInt(req.params.id);
    const filteredItems = items.filter(item => item.id !== itemId);
    
    if (filteredItems.length === items.length) {{
        return res.status(404).json({{ error: 'Item not found' }});
    }}
    
    writeData(filteredItems);
    res.json({{ message: 'Item deleted successfully' }});
}});

app.listen(PORT, () => {{
    console.log(`{project_name} API running on port ${{PORT}}`);
}});'''
    
    def _generate_static_js(self, project_name: str) -> str:
        return f'''// {project_name} JavaScript
let items = JSON.parse(localStorage.getItem('items')) || [];
let categories = new Set();

// DOM Elements
const addForm = document.getElementById('addForm');
const itemsList = document.getElementById('itemsList');
const emptyState = document.getElementById('emptyState');
const searchInput = document.getElementById('searchInput');
const categoryFilter = document.getElementById('categoryFilter');

// Initialize app
document.addEventListener('DOMContentLoaded', function() {{
    renderItems();
    updateCategoryFilter();
    
    // Event listeners
    addForm.addEventListener('submit', addItem);
    searchInput.addEventListener('input', filterItems);
    categoryFilter.addEventListener('change', filterItems);
}});

// Add new item
function addItem(e) {{
    e.preventDefault();
    
    const name = document.getElementById('itemName').value;
    const category = document.getElementById('itemCategory').value || 'General';
    const quantity = parseInt(document.getElementById('itemQuantity').value) || 0;
    const price = parseFloat(document.getElementById('itemPrice').value) || 0;
    const description = document.getElementById('itemDescription').value;
    
    const newItem = {{
        id: Date.now(),
        name,
        category,
        quantity,
        price,
        description,
        createdDate: new Date().toLocaleDateString()
    }};
    
    items.push(newItem);
    categories.add(category);
    
    saveToStorage();
    renderItems();
    updateCategoryFilter();
    addForm.reset();
    
    // Show success message
    showMessage('Item added successfully!', 'success');
}}

// Render items
function renderItems(filteredItems = items) {{
    if (filteredItems.length === 0) {{
        itemsList.style.display = 'none';
        emptyState.style.display = 'block';
        return;
    }}
    
    itemsList.style.display = 'grid';
    emptyState.style.display = 'none';
    
    itemsList.innerHTML = filteredItems.map(item => `
        <div class="item-card">
            <h3>${{item.name}}</h3>
            <p>${{item.description || 'No description'}}</p>
            <div class="item-meta">
                <span class="category">${{item.category}}</span>
                <span class="quantity">Qty: ${{item.quantity}}</span>
                <span class="price">$${{item.price.toFixed(2)}}</span>
            </div>
            <div class="item-actions">
                <button class="btn-delete" onclick="deleteItem(${{item.id}})">
                    Delete
                </button>
            </div>
        </div>
    `).join('');
}}

// Delete item
function deleteItem(id) {{
    if (confirm('Are you sure you want to delete this item?')) {{
        items = items.filter(item => item.id !== id);
        saveToStorage();
        renderItems();
        updateCategoryFilter();
        showMessage('Item deleted successfully!', 'success');
    }}
}}

// Filter items
function filterItems() {{
    const searchTerm = searchInput.value.toLowerCase();
    const selectedCategory = categoryFilter.value;
    
    let filtered = items.filter(item => {{
        const matchesSearch = item.name.toLowerCase().includes(searchTerm) ||
                            item.description.toLowerCase().includes(searchTerm);
        const matchesCategory = !selectedCategory || item.category === selectedCategory;
        
        return matchesSearch && matchesCategory;
    }});
    
    renderItems(filtered);
}}

// Update category filter
function updateCategoryFilter() {{
    categories.clear();
    items.forEach(item => categories.add(item.category));
    
    categoryFilter.innerHTML = '<option value="">All Categories</option>' +
        Array.from(categories).map(cat => `<option value="${{cat}}">${{cat}}</option>`).join('');
}}

// Save to localStorage
function saveToStorage() {{
    localStorage.setItem('items', JSON.stringify(items));
}}

// Show message
function showMessage(message, type) {{
    const messageDiv = document.createElement('div');
    messageDiv.className = `message message-${{type}}`;
    messageDiv.textContent = message;
    messageDiv.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${{type === 'success' ? '#28a745' : '#dc3545'}};
        color: white;
        padding: 15px 20px;
        border-radius: 8px;
        z-index: 1000;
        animation: slideIn 0.3s ease;
    `;
    
    document.body.appendChild(messageDiv);
    
    setTimeout(() => {{
        messageDiv.remove();
    }}, 3000);
}}

// Add CSS animation
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {{
        from {{ transform: translateX(100%); opacity: 0; }}
        to {{ transform: translateX(0); opacity: 1; }}
    }}
`;
document.head.appendChild(style);'''
    
    def _generate_package_json(self, project_name: str) -> str:
        return f'''{{
  "name": "{project_name.lower()}",
  "version": "1.0.0",
  "description": "{project_name} - Generated by Jarvis",
  "main": "server.js",
  "scripts": {{
    "start": "node server.js",
    "dev": "nodemon server.js"
  }},
  "dependencies": {{
    "express": "^4.18.0",
    "cors": "^2.8.5",
    "body-parser": "^1.20.0"
  }},
  "devDependencies": {{
    "nodemon": "^2.0.20"
  }}
}}'''
    
    def _generate_requirements(self, project_type: str) -> str:
        if project_type == 'api':
            return "fastapi>=0.68.0\nuvicorn>=0.15.0\npydantic>=1.8.0"
        else:
            return "Flask>=2.0.0\nrequests>=2.25.0"
    
    def _generate_maven_pom(self, project_name: str) -> str:
        return f'''<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 
         http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.jarvis</groupId>
    <artifactId>{project_name.lower()}</artifactId>
    <version>1.0.0</version>
    <properties>
        <maven.compiler.source>11</maven.compiler.source>
        <maven.compiler.target>11</maven.compiler.target>
    </properties>
    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
            <version>2.7.0</version>
        </dependency>
    </dependencies>
</project>'''
    
    def create_project_on_desktop(self, project_data: Dict) -> str:
        try:
            project_name = project_data['project_name']
            project_path = self.desktop_path / project_name
            
            project_path.mkdir(exist_ok=True)
            
            for filename, content in project_data['files'].items():
                file_path = project_path / filename
                file_path.parent.mkdir(parents=True, exist_ok=True)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
            
            return f"Project '{project_name}' created successfully at: {project_path}"
            
        except Exception as e:
            return f"Error creating project: {str(e)}"

auto_code_architect = AutoCodeArchitect()

def generate_inline_code(query: str) -> str:
    """Generate inline code snippets"""
    query_lower = query.lower()
    
    # Detect programming language
    language = 'python'  # default
    if ' c ' in query_lower or query_lower.startswith('c ') or query_lower.endswith(' c'):
        language = 'c'
    elif 'java' in query_lower:
        language = 'java'
    elif 'javascript' in query_lower or 'js' in query_lower:
        language = 'javascript'
    elif 'cpp' in query_lower or 'c++' in query_lower:
        language = 'cpp'
    
    if 'add' in query_lower and 'number' in query_lower:
        if language == 'c':
            return """#include <stdio.h>

int add_two_numbers(int a, int b) {
    return a + b;
}

int main() {
    int num1, num2, result;
    printf("Enter first number: ");
    scanf("%d", &num1);
    printf("Enter second number: ");
    scanf("%d", &num2);
    result = add_two_numbers(num1, num2);
    printf("Sum: %d\n", result);
    return 0;
}"""
        elif language == 'java':
            return """import java.util.Scanner;

public class AddNumbers {
    public static int addTwoNumbers(int a, int b) {
        return a + b;
    }
    
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Enter first number: ");
        int num1 = scanner.nextInt();
        System.out.print("Enter second number: ");
        int num2 = scanner.nextInt();
        int result = addTwoNumbers(num1, num2);
        System.out.println("Sum: " + result);
        scanner.close();
    }
}"""
        elif language == 'javascript':
            return """function addTwoNumbers(a, b) {
    return a + b;
}

// Example usage
const num1 = parseFloat(prompt("Enter first number: "));
const num2 = parseFloat(prompt("Enter second number: "));
const result = addTwoNumbers(num1, num2);
console.log(`Sum: ${result}`);
alert(`Sum: ${result}`);"""
        else:  # Python
            return """def add_two_numbers(a, b):
    return a + b

# Example usage
num1 = float(input("Enter first number: "))
num2 = float(input("Enter second number: "))
result = add_two_numbers(num1, num2)
print(f"Sum: {result}")"""
    
    elif 'calculator' in query_lower:
        return """def calculator(a, b, operation):
    if operation == '+':
        return a + b
    elif operation == '-':
        return a - b
    elif operation == '*':
        return a * b
    elif operation == '/':
        return a / b if b != 0 else "Cannot divide by zero"
    else:
        return "Invalid operation"

# Full calculator program
while True:
    try:
        num1 = float(input("Enter first number: "))
        operation = input("Enter operation (+, -, *, /): ")
        num2 = float(input("Enter second number: "))
        
        result = calculator(num1, num2, operation)
        print(f"Result: {result}")
        
        if input("Continue? (y/n): ").lower() != 'y':
            break
    except ValueError:
        print("Invalid input! Please enter numbers.")"""
    
    elif 'factorial' in query_lower:
        return """def factorial(n):
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)

# Example usage
num = int(input("Enter a number: "))
if num < 0:
    print("Factorial is not defined for negative numbers")
else:
    result = factorial(num)
    print(f"Factorial of {num} is {result}")"""
    
    elif 'fibonacci' in query_lower:
        return """def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# Example usage
num = int(input("Enter number of terms: "))
print(f"Fibonacci sequence for {num} terms:")
for i in range(num):
    print(fibonacci(i), end=" ")
print()"""
    
    elif 'sort' in query_lower:
        return """def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

# Example usage
numbers = [64, 34, 25, 12, 22, 11, 90]
print(f"Original array: {numbers}")
sorted_numbers = bubble_sort(numbers.copy())
print(f"Sorted array: {sorted_numbers}")"""
    
    else:
        # Generate complete working code based on query keywords
        if 'prime' in query_lower:
            return """def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

# Example usage
num = int(input("Enter a number: "))
if is_prime(num):
    print(f"{num} is a prime number")
else:
    print(f"{num} is not a prime number")"""
        
        else:
            return f"""# Complete implementation for: {query}
def main():
    print("Program started")
    # Add your implementation here
    result = "Hello World"
    print(f"Result: {{result}}")
    return result

if __name__ == "__main__":
    main()"""

def write_code_at_cursor(code: str, file_path: str) -> str:
    """Write code at cursor position in active file"""
    try:
        # For now, append to end of file (cursor position detection would need IDE integration)
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write('\n\n' + code + '\n')
        return f"Code written to {file_path}"
    except Exception as e:
        return f"Error writing code: {str(e)}"

def generate_code_project(query: str) -> str:
    try:
        # Check if user wants inline code
        if any(word in query.lower() for word in ['write here', 'cursor', 'inline', 'here']):
            code = generate_inline_code(query)
            
            # Write at actual cursor position using clipboard method
            import pyautogui
            import pyperclip
            
            try:
                # Copy code to clipboard
                pyperclip.copy(code)
                
                # Paste at current cursor position
                pyautogui.hotkey('ctrl', 'v')
                
                return f"Code written at cursor position"
            except:
                # Fallback: write to active file
                active_file = r"c:\Users\Hp\Desktop\inp\run.py"
                with open(active_file, 'a', encoding='utf-8') as f:
                    f.write('\n\n' + code + '\n')
                return f"Code appended to run.py"
        
        # Otherwise create project
        request_info = auto_code_architect.detect_request_type(query)
        result = auto_code_architect.generate_code(request_info)
        
        creation_result = auto_code_architect.create_project_on_desktop(result)
        return f"Creating project on Desktop...\n\n{creation_result}\n\nProject Type: {result['project_type']}\nLanguage: {result['language']}"
    
    except Exception as e:
        return f"Error generating code: {str(e)}"