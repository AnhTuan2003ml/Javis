import os
import subprocess
import pyautogui
import time
import win32com.client
import requests
import webbrowser
from PIL import Image
from engine.dual_ai import dual_ai
import sqlite3
import json
from datetime import datetime, timedelta
from collections import Counter
import psutil

class UltimateAIExecutor:
    def __init__(self):
        self.confirmation_required = False  # Auto execution
        self.learning_db = os.path.join(os.path.expanduser('~'), '.jarvis_learning.db')
        self._init_learning_db()
        
        # Next move predictions control
        self.next_move_predictions_enabled = False
        

        
    def analyze_screen(self):
        """Capture and analyze current screen content"""
        screenshot = pyautogui.screenshot()
        screenshot.save('temp_screen.png')
        return self.analyze_image_content('temp_screen.png')
        
    def analyze_image_content(self, image_path):
        """Analyze image content using AI"""
        prompt = "Analyze this screenshot and describe what applications are open, what content is visible, and what the user might be doing."
        return f"Screen Analysis: Current screen shows various applications and content. Screenshot saved as {image_path}"
        
    def summarize_screen_content(self):
        """Provide detailed summary of screen content"""
        analysis = self.analyze_screen()
        return f"Screen Summary: {analysis}"
        
    def explain_google_search_results(self, query):
        """Search Google and explain results"""
        search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        webbrowser.open(search_url)
        return f"Opened Google search for: {query}. Results will explain the topic comprehensively."
        
    def read_and_explain_file(self, file_path):
        """Read file content and provide explanation"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return f"File Content Analysis:\n{content[:500]}..." if len(content) > 500 else f"File Content:\n{content}"
        except Exception as e:
            return f"Error reading file: {e}"
        
    def validate_command(self, command):
        """Basic security validation"""
        dangerous = ['format', 'del /f', 'rm -rf', 'shutdown /s']
        return not any(danger in command.lower() for danger in dangerous)
        
    def interpret_command(self, user_command):
        """AI interprets any natural command and decides execution method"""
        prompt = f"""
You are a Windows automation system. Convert user commands to executable code.

User Command: "{user_command}"

Output format:
METHOD: <system | pyautogui | office | screen | search | file | ai>
COMMAND: <exact Python code>

---

### 🧠 Available Tools:
- CMD commands
- PowerShell commands
- Python pyautogui (keyboard/mouse)
- win32com (Office automation)
- os.system / subprocess

---

### ⚙️ Rules for Method Selection:
- For typing or UI automation → use **pyautogui**
- For app control (open/close/run apps) → use **system** or **subprocess**
- For Office tasks (Word, Excel, PowerPoint) → use **office** with `win32com.client`
- For file/folder operations → use **system** with Python os commands
- For system actions (shutdown, restart, etc.) → use **cmd** or **powershell**
- For screen analysis/screenshot → use **screen** method
- For Google search explanation → use **search** method
- For file content analysis → use **file** method
- Decide the most accurate method automatically
- If unsure → default to `METHOD: system` using Python commands
- For system control (volume, brightness, shutdown, restart, etc.), use exact working Windows code.

---

### 💡 CAPABILITIES:
You can:
- Generate realistic, professional content for any topic
- Create or edit Office documents using `win32com.client`
- Run system commands or PowerShell scripts
- Automate typing, clicking, and window interactions via `pyautogui`
- Execute any system-level control through CMD or PowerShell
- Analyze screen content and explain what's visible
- Capture screenshots and describe applications/content
- Search Google and explain results
- Read and analyze file contents (txt, py, etc.)

---

### 📘 Office Logic:
If the user’s command involves:
- **Word** → Create properly formatted structured content (letters, resumes, reports)
- **PowerPoint** → Create slides (title + bullet points) with relevant content
- **Excel** → Create sheets, fill data, apply formulas, format tables
- **System or browser** → Open, control, or automate via CMD/Python/system calls

---

### 🧾 EXAMPLES


### ⚡ Examples of How to Handle Commands:

#### 🔊 Volume Control
- Increase volume:
  ```python
  METHOD: system
  COMMAND:
  import ctypes, time
  for _ in range(5):
      ctypes.windll.user32.keybd_event(0xAF, 0, 0, 0)
      time.sleep(0.1)
      
#### brightness control
METHOD: system
COMMAND:
import screen_brightness_control as sbc
current = sbc.get_brightness(display=0)[0]
sbc.set_brightness(min(current + 10, 100))
      
#### Simple Example: open notepad and type text
METHOD: pyautogui
COMMAND:
import os, time, pyautogui
os.system('start notepad')
time.sleep(3)
pyautogui.typewrite('hello world')

#### Save Example: save document (works for new txt files)
METHOD: pyautogui
COMMAND:
import pyautogui, time
pyautogui.hotkey('ctrl', 's')
time.sleep(2)
pyautogui.typewrite('document.txt')
pyautogui.press('enter')

#### Time Display Example: show current time
METHOD: pyautogui
COMMAND:
import os, time, pyautogui, datetime
os.system('start notepad')
time.sleep(3)
current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
pyautogui.typewrite(f'Current Time:')
pyautogui.press('enter')

#### Screen Analysis Example: analyze what's on screen
METHOD: screen
COMMAND:
import pyautogui, time, os, subprocess
screenshot = pyautogui.screenshot()
desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
screenshot_path = os.path.join(desktop_path, 'screen_analysis.png')
screenshot.save(screenshot_path)
try:
    import win32gui
    def enum_windows(hwnd, windows):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if title: windows.append(title)
    windows = []
    win32gui.EnumWindows(enum_windows, windows)
    visible_windows = [w for w in windows[:5] if w and len(w) > 3]
    print('Screen Analysis Complete:\\n- Screenshot saved: ' + screenshot_path + '\\n- Visible windows: ' + ', '.join(visible_windows) + '\\n- Active applications detected on screen')
except:
    windows = subprocess.check_output('tasklist /fo csv', shell=True).decode()
    apps = [line.split(',')[0].replace('"', '') for line in windows.split('\\n')[1:6] if 'exe' in line]
    print('Screen Analysis Complete:\\n- Screenshot saved: ' + screenshot_path + '\\n- Running apps: ' + ', '.join(apps))

#### Google Search Explanation Example: search and explain topic
METHOD: search
COMMAND:
import webbrowser, time
query = 'artificial intelligence'
search_url = 'https://www.google.com/search?q=' + query.replace(' ', '+')
webbrowser.open(search_url)
time.sleep(2)
print('Google Search Results for: ' + query + '\\n- Opened search results in browser\\n- Results will show comprehensive information about the topic\\n- Multiple sources and explanations available')

#### File Content Analysis Example: read and explain file
METHOD: file
COMMAND:
try:
    with open('ultimate_ai_executor.py', 'r', encoding='utf-8') as f:
        content = f.read()
    lines = content.split('\\n')
    classes = [line.strip() for line in lines if line.strip().startswith('class ')]
    functions = [line.strip() for line in lines if line.strip().startswith('def ') and 'self' in line]
    imports = [line.strip() for line in lines[:20] if line.strip().startswith('import') or line.strip().startswith('from')]
    print('File Analysis - ultimate_ai_executor.py:\\n')
    print('IMPORTS: ' + ', '.join([imp.split()[1] for imp in imports[:5]]))
    print('CLASSES: ' + ', '.join([cls.split()[1].rstrip(':') for cls in classes]))
    print('METHODS: ' + ', '.join([func.split('(')[0].replace('def ', '') for func in functions[:8]]))
    print('\\nPURPOSE: AI-powered Windows automation system with screen analysis, file reading, and Office automation capabilities')
except Exception as e:
    print('Error reading file: ' + str(e))

#### Screenshot + Word Example: take screenshot and insert in Word
METHOD: pyautogui
COMMAND:
import os, time, pyautogui, win32com.client
desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
screenshot_path = os.path.join(desktop_path, 'screenshot.png')
pyautogui.screenshot(screenshot_path)
time.sleep(1)
word = win32com.client.Dispatch('Word.Application')
word.Visible = True
doc = word.Documents.Add()
sel = word.Selection
sel.Font.Size = 16
sel.Font.Bold = True
sel.TypeText('SCREENSHOT REPORT\\n\\n')
sel.Font.Size = 12
sel.Font.Bold = False
sel.TypeText('Generated on ' + time.strftime('%B %d, %Y') + '\\n\\n')
sel.InlineShapes.AddPicture(screenshot_path)
report_path = os.path.join(desktop_path, 'report.docx')
doc.SaveAs(report_path)

#### File/Folder Operations: create folder
METHOD: system
COMMAND:
import os
os.makedirs(os.path.join(os.path.expanduser('~'), 'Desktop', 'foldername'), exist_ok=True)

#### Calculator + Notepad Example: calculate and transfer result
METHOD: pyautogui
COMMAND:
import os, time, pyautogui
os.system('calc')
time.sleep(3)
pyautogui.typewrite('25*8=')
time.sleep(1)
pyautogui.hotkey('ctrl', 'c')
time.sleep(1)
os.system('notepad')
time.sleep(3)
pyautogui.typewrite('Calculation Result: ')
pyautogui.hotkey('ctrl', 'v')
pyautogui.press('enter')
pyautogui.typewrite('Calculation Complete!')

#### Google Search Copy Paste Example: search, copy all, and paste in Word
METHOD: pyautogui
COMMAND:
import os, time, pyautogui, webbrowser, win32com.client
webbrowser.open('https://www.google.com/search?q=ml')
time.sleep(4)
pyautogui.hotkey('ctrl', 'a')
time.sleep(1)
pyautogui.hotkey('ctrl', 'c')
time.sleep(1)
word = win32com.client.Dispatch('Word.Application')
word.Visible = True
doc = word.Documents.Add()
time.sleep(2)
pyautogui.hotkey('ctrl', 'v')

#### YouTube Examples: open and play videos directly
METHOD: system
COMMAND:
import webbrowser, time, pyautogui
webbrowser.open('https://www.youtube.com/results?search_query=music+videos')
time.sleep(4)
pyautogui.click(640, 360)
time.sleep(2)
pyautogui.press('space')

#### WiFi Control: turn WiFi on/off using Settings app
METHOD: pyautogui
COMMAND:
import pyautogui, time, os
os.system('start ms-settings:network-wifi')
time.sleep(4)
pyautogui.press('tab')
time.sleep(0.5)
pyautogui.press('space')
time.sleep(1)
pyautogui.hotkey('alt', 'f4')

#### Night Light Control: turn night light on/off (DIRECT SPACE - NO TAB)
METHOD: pyautogui
COMMAND:
import pyautogui, time, os
os.system('start ms-settings:nightlight')
time.sleep(4)
pyautogui.press('space')
time.sleep(1)
pyautogui.hotkey('alt', 'f4')

#### Energy Saver Control: SEARCH METHOD - turn energy saver on/off using Windows search
METHOD: pyautogui
COMMAND:
import pyautogui, time, os
pyautogui.hotkey('win', 's')
time.sleep(2)
pyautogui.typewrite('customize power saving setting')
time.sleep(1)
pyautogui.press('enter')
time.sleep(3)
pyautogui.press('tab')
time.sleep(1)
pyautogui.hotkey('alt', 'f4')

#### Hotspot Control: turn mobile hotspot on/off (DIRECT SPACE - NO TAB)
METHOD: pyautogui
COMMAND:
import pyautogui, time, os
os.system('start ms-settings:network-mobilehotspot')
time.sleep(4)
pyautogui.press('space')
time.sleep(1)
pyautogui.hotkey('alt', 'f4')

#### Focus Assist Control: turn focus assist on/off (DIRECT SPACE - NO TAB)
METHOD: pyautogui
COMMAND:
import pyautogui, time, os
os.system('start ms-settings:quiethours')
time.sleep(4)
pyautogui.press('space')
time.sleep(1)
pyautogui.hotkey('alt', 'f4')

#### Location Services Control: turn location on/off (DIRECT SPACE - NO TAB)
METHOD: pyautogui
COMMAND:
import pyautogui, time, os
os.system('start ms-settings:privacy-location')
time.sleep(4)
pyautogui.press('space')
time.sleep(1)
pyautogui.hotkey('alt', 'f4')

#### Microphone Privacy Control: turn microphone access on/off
METHOD: pyautogui
COMMAND:
import pyautogui, time, os
os.system('start ms-settings:privacy-microphone')
time.sleep(4)
pyautogui.press('tab')
time.sleep(0.5)
pyautogui.press('space')
time.sleep(1)
pyautogui.hotkey('alt', 'f4')

#### Camera Privacy Control: turn camera access on/off
METHOD: pyautogui
COMMAND:
import pyautogui, time, os
os.system('start ms-settings:privacy-webcam')
time.sleep(4)
pyautogui.press('tab')
time.sleep(0.5)
pyautogui.press('space')
time.sleep(1)
pyautogui.hotkey('alt', 'f4')

#### Bluetooth Control: turn Bluetooth on/off using Settings app
METHOD: pyautogui
COMMAND:
import pyautogui, time, os
os.system('start ms-settings:bluetooth')
time.sleep(4)
pyautogui.press('tab')
time.sleep(0.3)
pyautogui.hotkey('shift', 'tab')
time.sleep(0.5)
pyautogui.press('space')
time.sleep(1)
pyautogui.hotkey('alt', 'f4')

#### Volume Control: adjust system volume
METHOD: system
COMMAND:
import pyautogui
pyautogui.press('volumeup')

#### Task Manager: open Windows task manager
METHOD: system
COMMAND:
import pyautogui
pyautogui.hotkey('ctrl', 'shift', 'esc')

#### System Info: display CPU, memory, battery usage
METHOD: system
COMMAND:
import psutil
print(f'CPU: {psutil.cpu_percent()}%')
print(f'Memory: {psutil.virtual_memory().percent}%')
print(f'Battery: {psutil.sensors_battery().percent if psutil.sensors_battery() else "N/A"}%')

#### Airplane Mode: toggle airplane mode
METHOD: pyautogui
COMMAND:
import pyautogui, time, os
os.system('start ms-settings:network-airplanemode')
time.sleep(4)
pyautogui.press('tab')
time.sleep(0.5)
pyautogui.press('space')
time.sleep(1)
pyautogui.hotkey('alt', 'f4')

#### Display Settings: open display settings
METHOD: pyautogui
COMMAND:
import pyautogui, time, os
os.system('start ms-settings:display')
time.sleep(3)

#### Sound Settings: open sound settings
METHOD: pyautogui
COMMAND:
import pyautogui, time, os
os.system('start ms-settings:sound')
time.sleep(3)

#### Power Settings: open power and battery settings
METHOD: pyautogui
COMMAND:
import pyautogui, time, os
os.system('start ms-settings:powersleep')
time.sleep(3)

#### Open Settings: open Windows settings
METHOD: system
COMMAND:
import os
os.system('start ms-settings:')

#### Open File Explorer: open file explorer
METHOD: system
COMMAND:
import os
os.system('explorer')

#### Open Control Panel: open Windows control panel
METHOD: system
COMMAND:
import os
os.system('control')

#### Open Registry Editor: open Windows registry editor
METHOD: system
COMMAND:
import os
os.system('regedit')

#### Open Device Manager: open Windows device manager
METHOD: system
COMMAND:
import os
os.system('devmgmt.msc')





#### 🟦 Word Example: create professional resume in Word
METHOD: office
COMMAND:
import win32com.client, time
word = win32com.client.Dispatch('Word.Application')
word.Visible = True
doc = word.Documents.Add()
sel = word.Selection
sel.Font.Name = 'Calibri'
sel.Font.Size = 16
sel.Font.Bold = True
sel.TypeText('JOHN DOE\\n')
sel.Font.Size = 12
sel.Font.Bold = False
sel.TypeText('Email: john@example.com | Phone: (555) 123-4567\\n\\n')
sel.Font.Size = 14
sel.Font.Bold = True
sel.TypeText('PROFESSIONAL SUMMARY\\n')
sel.Font.Size = 11
sel.Font.Bold = False
sel.TypeText('Results-driven professional with over 5 years in data analytics and automation...\\n\\n')
sel.Font.Bold = True
sel.TypeText('SKILLS\\n')
sel.Font.Bold = False
sel.TypeText('• Python, SQL, Excel Automation\\n• Data Visualization\\n• AI Integration\\n\\n')
sel.Font.Bold = True
sel.TypeText('EXPERIENCE\\n')
sel.Font.Bold = False
sel.TypeText('Data Analyst | DataCorp | 2020–Present\\n• Automated reports saving 12 hours/week\\n• Improved insights accuracy by 30%\\n\\n')

---

#### 🟧 PowerPoint Instructions:
For PowerPoint tasks:
- Generate 8-12 advanced slides with 4 to 5 short content
- Each slide must have 8-15 detailed bullet points with specific examples, statistics, case studies
- Include extensive technical details, real-world applications, industry insights
- Add multiple concept slides, implementation details, advanced features, future trends
- Use professional formatting with proper fonts and styling
- Handle file conflicts with unique timestamps
- Always use `win32com.client` PowerPoint automation

Example:
METHOD: office
COMMAND:
import win32com.client, time, os
try:
    ppt = win32com.client.Dispatch('PowerPoint.Application')
    ppt.Visible = True
    presentation = ppt.Presentations.Add()
    
    # Title Slide
    slide1 = presentation.Slides.Add(1, 1)
    slide1.Shapes.Title.TextFrame.TextRange.Text = "Advanced Topic Analysis: Comprehensive Deep Dive"
    slide1.Shapes.Placeholders(2).TextFrame.TextRange.Text = "Expert-Level Technical Overview and Strategic Implementation Guide\\nAdvanced Research and Industry Analysis\\nPresented by: AI Expert System\\nDate: " + time.strftime('%B %d, %Y')
    
    # Introduction & Background
    slide2 = presentation.Slides.Add(2, 2)
    slide2.Shapes.Title.TextFrame.TextRange.Text = "Comprehensive Introduction and Historical Context"
    slide2.Shapes.Placeholders(2).TextFrame.TextRange.Text = "• Advanced definition with comprehensive technical specifications and industry standards\\n• Historical evolution from inception to current state with key milestones and breakthroughs\\n• Core architectural principles and fundamental design patterns used in implementation\\n• Current market position with detailed statistics, adoption rates, and growth metrics\\n• Significance in modern technological ecosystem with impact analysis and future projections\\n• Comprehensive overview of benefits, limitations, challenges, and strategic considerations\\n• Detailed scope of analysis including methodology, data sources, and evaluation criteria\\n• Key stakeholders, industry leaders, and major contributors to field development\\n• Regulatory landscape, compliance requirements, and legal framework considerations\\n• Global market trends, regional variations, and cultural adaptation strategies"
    
    # Technical Architecture
    slide3 = presentation.Slides.Add(3, 2)
    slide3.Shapes.Title.TextFrame.TextRange.Text = "Advanced Technical Architecture and Core Components"
    slide3.Shapes.Placeholders(2).TextFrame.TextRange.Text = "• Primary system architecture with detailed component breakdown and interaction patterns\\n• Advanced algorithms and mathematical models with complexity analysis and optimization strategies\\n• Data structures, storage mechanisms, and retrieval systems with performance benchmarks\\n• Security frameworks, encryption protocols, and access control mechanisms\\n• Scalability considerations, load balancing, and distributed system design principles\\n• Integration capabilities with existing systems, APIs, and third-party services\\n• Performance metrics, benchmarking results, and comparative analysis with alternatives\\n• Quality assurance processes, testing methodologies, and validation frameworks\\n• Maintenance requirements, update procedures, and lifecycle management strategies\\n• Technical documentation standards, code quality metrics, and development best practices"
    
    # Implementation Details
    slide4 = presentation.Slides.Add(4, 2)
    slide4.Shapes.Title.TextFrame.TextRange.Text = "Advanced Implementation Strategies and Best Practices"
    slide4.Shapes.Placeholders(2).TextFrame.TextRange.Text = "• Step-by-step implementation methodology with detailed project planning and resource allocation\\n• Advanced configuration options, customization capabilities, and parameter optimization\\n• Integration patterns with enterprise systems, databases, and cloud infrastructure\\n• Development workflows, version control strategies, and collaborative development practices\\n• Testing strategies including unit testing, integration testing, and performance validation\\n• Deployment procedures, environment management, and continuous integration/deployment\\n• Monitoring and logging systems with real-time analytics and alerting mechanisms\\n• Troubleshooting guides, common issues resolution, and advanced debugging techniques\\n• Performance tuning, optimization strategies, and resource utilization management\\n• Documentation requirements, training materials, and knowledge transfer protocols"
    
    # Real-World Applications
    slide5 = presentation.Slides.Add(5, 2)
    slide5.Shapes.Title.TextFrame.TextRange.Text = "Comprehensive Real-World Applications and Industry Use Cases"
    slide5.Shapes.Placeholders(2).TextFrame.TextRange.Text = "• Healthcare sector implementations with specific case studies, ROI analysis, and patient outcomes\\n• Financial services applications including risk management, fraud detection, and regulatory compliance\\n• Manufacturing and industrial automation with efficiency improvements and cost reduction metrics\\n• Educational technology applications with learning outcome improvements and engagement statistics\\n• Entertainment and media industry transformations with audience analytics and content optimization\\n• Government and public sector implementations with citizen service improvements and cost savings\\n• Small and medium business applications with accessibility considerations and scalability options\\n• Enterprise-level deployments with integration challenges and organizational change management\\n• Startup and innovation ecosystem applications with rapid prototyping and market validation\\n• International implementations with localization requirements and cultural adaptation strategies"
    
    # Advanced Features
    slide6 = presentation.Slides.Add(6, 2)
    slide6.Shapes.Title.TextFrame.TextRange.Text = "Advanced Features and Cutting-Edge Capabilities"
    slide6.Shapes.Placeholders(2).TextFrame.TextRange.Text = "• Machine learning integration with predictive analytics and intelligent automation capabilities\\n• Advanced data processing with real-time analytics, pattern recognition, and anomaly detection\\n• Cloud-native architecture with microservices, containerization, and serverless computing\\n• Advanced security features including zero-trust architecture and advanced threat protection\\n• Artificial intelligence integration with natural language processing and computer vision\\n• Advanced user interface design with responsive layouts and accessibility compliance\\n• API ecosystem with comprehensive documentation, SDKs, and developer tools\\n• Advanced reporting and visualization with interactive dashboards and business intelligence\\n• Mobile-first design with cross-platform compatibility and offline functionality\\n• Advanced customization options with plugin architecture and extensibility frameworks"
    
    # Benefits & ROI
    slide7 = presentation.Slides.Add(7, 2)
    slide7.Shapes.Title.TextFrame.TextRange.Text = "Comprehensive Benefits Analysis and Return on Investment"
    slide7.Shapes.Placeholders(2).TextFrame.TextRange.Text = "• Quantifiable efficiency improvements with detailed metrics, benchmarks, and comparative analysis\\n• Cost reduction strategies with comprehensive financial analysis and long-term projections\\n• Quality enhancement measures with customer satisfaction improvements and retention statistics\\n• Scalability advantages for growing organizations with capacity planning and resource optimization\\n• Innovation opportunities with competitive market positioning and differentiation strategies\\n• Risk mitigation strategies with comprehensive risk assessment and contingency planning\\n• Sustainability benefits with environmental impact analysis and corporate responsibility metrics\\n• Productivity gains with workforce optimization and skill development requirements\\n• Market expansion opportunities with new revenue streams and business model innovations\\n• Strategic advantages with competitive intelligence and market positioning analysis"
    
    # Apply advanced formatting
    for slide_num in range(1, 8):
        slide = presentation.Slides(slide_num)
        slide.Shapes.Title.TextFrame.TextRange.Font.Name = "Calibri"
        slide.Shapes.Title.TextFrame.TextRange.Font.Size = 24
        slide.Shapes.Title.TextFrame.TextRange.Font.Bold = True
        slide.Shapes.Title.TextFrame.TextRange.Font.Color.RGB = 0x1F4E79
        if slide_num > 1:
            slide.Shapes.Placeholders(2).TextFrame.TextRange.Font.Name = "Calibri"
            slide.Shapes.Placeholders(2).TextFrame.TextRange.Font.Size = 14
            slide.Shapes.Placeholders(2).TextFrame.TextRange.ParagraphFormat.SpaceAfter = 6
    
    filename = f'C:\\\\Users\\\\Public\\\\Advanced_Presentation_{int(time.time())}.pptx'
    presentation.SaveAs(filename)

---

#### 🟩 Excel Example: create sales report in Excel
METHOD: office
COMMAND:
import win32com.client
excel = win32com.client.Dispatch('Excel.Application')
excel.Visible = True
workbook = excel.Workbooks.Add()
sheet = workbook.Sheets(1)
sheet.Name = "Sales Report"
sheet.Cells(1, 1).Value = "Product"
sheet.Cells(1, 2).Value = "Sales"
sheet.Cells(2, 1).Value = "Laptop"
sheet.Cells(2, 2).Value = 12000
sheet.Cells(3, 1).Value = "Smartphone"
sheet.Cells(3, 2).Value = 8500
sheet.Cells(4, 1).Value = "Tablet"
sheet.Cells(4, 2).Value = 4000
sheet.Cells(6, 1).Value = "Total"
sheet.Cells(6, 2).Formula = "=SUM(B2:B4)"
sheet.Columns.AutoFit()

---

### Screen Analysis Commands:
- "what am I using on screen" → METHOD: screen
- "explain my screen" → METHOD: screen  
- "analyze screen content" → METHOD: screen
- "summarize screen" → METHOD: screen

### Search & Explain Commands:
- "search google for [topic] and explain" → METHOD: search
- "explain google results for [topic]" → METHOD: search

### File Analysis Commands:
- "read a.txt file" → METHOD: file
- "explain content of [filename]" → METHOD: file
- "analyze [filename]" → METHOD: file

### Next Move Control Commands:
- "disable next move predictions" → METHOD: system, COMMAND: from engine.ultimate_ai_executor import ultimate_ai; print(ultimate_ai.disable_next_move_predictions())
- "enable next move predictions" → METHOD: system, COMMAND: from engine.ultimate_ai_executor import ultimate_ai; print(ultimate_ai.enable_next_move_predictions())
- "next move status" → METHOD: system, COMMAND: from engine.ultimate_ai_executor import ultimate_ai; print(f"Next move predictions: {'Enabled' if ultimate_ai.get_next_move_status() else 'Disabled'}")
You are an expert automation system. Windows automation system. CRITICAL SAVE RULES: For save commands, use METHOD: pyautogui with this logic: pyautogui.hotkey('ctrl', 's'), wait 2 seconds, then type filename and press enter. This handles both existing files (Ctrl+S) and new files (Save As dialog). NEVER use office automation for simple save operations. For volume commands, use METHOD: system with ctypes. For screen analysis, use METHOD: screen. For Google search, use METHOD: search. For file content analysis, use METHOD: file. For YouTube/video commands, use METHOD: system with webbrowser.open(). For browser automation, use METHOD: pyautogui with clicks and typing. For 'disable next move predictions' or 'enable next move predictions' commands, use METHOD: system with ultimate_ai control methods.
Now generate the proper output for this command:
"{user_command}"
"""

        
        # Try 70B model first for complex automation tasks
        try:
            from groq import Groq
            from engine.groq_config import GROQ_API_KEY
            groq_client = Groq(api_key=GROQ_API_KEY)
            
            response = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000
            )
            result = response.choices[0].message.content.strip()
            if result:
                return result
        except Exception as e:
            print(f"70B model failed: {e}, falling back to dual_ai")
        
        # Fallback to dual_ai
        from engine.dual_ai import dual_ai
        result = dual_ai._answer_question(prompt)
        if result:
            return result

    def run_cmd(self, command):
        print(f"[CMD] -> {command}")
        subprocess.run(command, shell=True)

    def run_powershell(self, command):
        print(f"[PowerShell] -> {command}")
        subprocess.run(["powershell", "-Command", command], shell=True)

    def run_python_subprocess(self, command):
        print(f"[Python Subprocess] -> {command}")
        subprocess.Popen(command, shell=True)

    def run_system_call(self, command):
        print(f"[System Call] -> {command}")
        if command.startswith('os.system(') or 'import' in command:
            exec(command, globals())
        else:
            os.system(command)

    def run_pyautogui(self, command):
        print(f"[PyAutoGUI] executing ->")
        exec_globals = {
            'os': os,
            'time': time,
            'pyautogui': pyautogui,
            'subprocess': subprocess
        }
        exec(command, exec_globals)

    def run_office(self, command):
        print(f"[Office Automation] executing ->")
        exec(command, globals())
        
    def run_screen_analysis(self, command):
        print(f"[Screen Analysis] executing ->")
        exec_globals = {
            'pyautogui': pyautogui,
            'time': time,
            'os': os,
            'subprocess': subprocess,
            'win32gui': None
        }
        try:
            import win32gui
            exec_globals['win32gui'] = win32gui
        except:
            pass
        exec(command, exec_globals)
        
    def run_search_explanation(self, command):
        print(f"[Search & Explain] executing ->")
        exec_globals = {
            'webbrowser': webbrowser,
            'requests': requests
        }
        exec(command, exec_globals)
        
    def run_file_analysis(self, command):
        print(f"[File Analysis] executing ->")
        exec(command, globals())
    
    def _init_learning_db(self):
        conn = sqlite3.connect(self.learning_db)
        conn.execute('''CREATE TABLE IF NOT EXISTS command_history 
                       (id INTEGER PRIMARY KEY, command TEXT, method TEXT, 
                        success INTEGER, timestamp TEXT, context TEXT)''')
        conn.execute('''CREATE TABLE IF NOT EXISTS user_patterns 
                       (id INTEGER PRIMARY KEY, pattern TEXT, frequency INTEGER, 
                        last_used TEXT, context TEXT)''')
        conn.close()
    
    def success_failure_tracker(self, command, method, success, context=""):
        conn = sqlite3.connect(self.learning_db)
        conn.execute('INSERT INTO command_history VALUES (NULL, ?, ?, ?, ?, ?)',
                    (command, method, success, datetime.now().isoformat(), context))
        conn.commit()
        conn.close()
    
    def next_action_predictor(self):
        conn = sqlite3.connect(self.learning_db)
        cursor = conn.execute('SELECT command, COUNT(*) as freq FROM command_history WHERE success=1 GROUP BY command ORDER BY freq DESC LIMIT 5')
        predictions = [row[0] for row in cursor.fetchall()]
        conn.close()
        return predictions
    
    def pattern_learning(self, command):
        conn = sqlite3.connect(self.learning_db)
        cursor = conn.execute('SELECT frequency FROM user_patterns WHERE pattern=?', (command,))
        result = cursor.fetchone()
        if result:
            conn.execute('UPDATE user_patterns SET frequency=?, last_used=? WHERE pattern=?',
                        (result[0] + 1, datetime.now().isoformat(), command))
        else:
            conn.execute('INSERT INTO user_patterns VALUES (NULL, ?, 1, ?, "")',
                        (command, datetime.now().isoformat()))
        conn.commit()
        conn.close()
    

    
    def smart_error_recovery(self, failed_command, error_msg):
        recovery_map = {
            "chrome": "start msedge",
            "notepad": "start wordpad",
            "excel": "start calc",
            "word": "start notepad"
        }
        
        for app, alternative in recovery_map.items():
            if app in failed_command.lower():
                print(f"🔄 Auto-recovery: Trying {alternative} instead")
                os.system(alternative)
                return True
        return False
    

    
    def execute_command(self, user_command):
        """Main function to execute any desktop command"""
        try:
            # Get AI response for the command
            ai_response = self.get_ai_response(user_command)
            if not ai_response:
                return "Command not recognized"
            
            # Parse METHOD and COMMAND from AI response
            lines = ai_response.split('\n')
            method = None
            command = []
            
            for line in lines:
                if line.startswith('METHOD:'):
                    method = line.replace('METHOD:', '').strip()
                elif line.startswith('COMMAND:'):
                    command = []
                elif method and line.strip():
                    command.append(line)
            
            if not method or not command:
                return "Invalid command format"
            
            # Execute based on method
            command_code = '\n'.join(command)
            
            if method == 'system':
                self.run_system_call(command_code)
            elif method == 'pyautogui':
                self.run_pyautogui(command_code)
            elif method == 'office':
                self.run_office(command_code)
            elif method == 'ai':
                exec(command_code, globals())
            elif method == 'ai_office':
                exec(command_code, globals())
            elif method == 'screen':
                self.run_screen_analysis(command_code)
            elif method == 'search':
                self.run_search_explanation(command_code)
            elif method == 'file':
                self.run_file_analysis(command_code)
            else:
                return f"Unknown method: {method}"
            
            return "Command executed successfully"
            
        except Exception as e:
            return f"Error executing command: {str(e)}"
    
    def workflow_automation(self, trigger_command):
        workflows = {
            "morning_routine": ["check calendar", "open email", "check weather"],
            "work_setup": ["open excel", "open chrome", "open notepad"],
            "presentation_mode": ["open powerpoint", "close distractions", "set focus mode"]
        }
        
        for workflow, commands in workflows.items():
            if workflow in trigger_command.lower():
                print(f"🤖 Executing workflow: {workflow}")
                for cmd in commands:
                    print(f"  → {cmd}")
                return True
        return False
    

    
    def behavioral_analytics(self):
        conn = sqlite3.connect(self.learning_db)
        cursor = conn.execute('SELECT command, COUNT(*) as freq FROM command_history GROUP BY command ORDER BY freq DESC LIMIT 10')
        top_commands = cursor.fetchall()
        
        cursor = conn.execute('SELECT AVG(success) as success_rate FROM command_history')
        success_rate = cursor.fetchone()[0] or 0
        
        conn.close()
        
        return {
            "top_commands": top_commands,
            "success_rate": success_rate * 100,
            "total_commands": len(top_commands)
        }
    
    def adaptive_command_optimization(self, command):
        conn = sqlite3.connect(self.learning_db)
        cursor = conn.execute('SELECT method, AVG(success) as success_rate FROM command_history WHERE command LIKE ? GROUP BY method ORDER BY success_rate DESC',
                             (f"%{command}%",))
        best_method = cursor.fetchone()
        conn.close()
        
        if best_method and best_method[1] > 0.8:
            return best_method[0]
        return "system"
    
    def predict_next_move(self, current_command):
        """AI predicts next logical action based on context"""
        if not self.next_move_predictions_enabled:
            return []
        
        prompt = f"""
You are an expert workflow predictor. Based on what the user just did, predict the MOST LOGICAL next action.

User's current action: "{current_command}"

🧠 CONTEXT ANALYSIS:
- If they opened/created something → suggest saving, formatting, or adding content
- If they wrote/typed content → suggest saving, copying, or sharing
- If they searched/browsed → suggest bookmarking, downloading, or taking notes
- If they took screenshot → suggest editing, saving, or sharing
- If they opened app → suggest common first actions in that app
- If they saved something → suggest opening, sharing, or creating backup
- If they created document → suggest adding content, formatting, or printing
- If they sent message → suggest checking replies or sending to others
- If they made calculation → suggest saving result or using in document
- If they opened media → suggest adjusting volume, fullscreen, or sharing

💡 SMART SUGGESTIONS:
- Be specific and immediately actionable
- Consider professional workflows
- Think about what 90% of users do next
- Suggest productive follow-up actions
- Include creative and useful options

📋 EXAMPLES:
- "open notepad write hello" → "Save the document"
- "create presentation about AI" → "Add more slides"
- "take screenshot" → "Edit the image"
- "search google for python" → "Bookmark useful results"
- "open calculator" → "Copy the result"
- "send email to john" → "Check for replies"
- "create folder documents" → "Move files to folder"
- "open spotify" → "Create new playlist"

Output ONLY the suggestion (2-5 words):
"""
        
        try:
            from engine.dual_ai import dual_ai
            
            suggestion = dual_ai._answer_question(prompt)
            
            # Clean the suggestion
            suggestion = suggestion.replace('[', '').replace(']', '').strip()
            
            return [suggestion] if suggestion else []
        except:
            return []
    

    

    
    def _generate_smart_response(self, command, method):
        """Generate intelligent response based on executed command"""
        prompt = f"""
User executed command: "{command}"
Execution method: {method}
Status: SUCCESS

Generate a brief, natural response confirming what was accomplished.

Examples:
- "open notepad" → "Notepad opened successfully"
- "create presentation" → "Presentation created"
- "take screenshot" → "Screenshot captured"
- "search google" → "Google search completed"

Be concise (3-6 words). Output ONLY the response.
"""
        
        try:
            from engine.dual_ai import dual_ai
            
            result = dual_ai._answer_question(prompt)
            if result:
                return result
        except:
            # Fallback responses
            if "open" in command:
                app = command.replace("open", "").strip()
                return f"{app} opened successfully"
            elif "create" in command:
                return "Creation completed"
            elif "search" in command:
                return "Search completed"
            else:
                return "Command executed successfully"

    def execute(self, user_command):
        """Universal execution of any natural language command"""
        self.pattern_learning(user_command)
        
        if self.workflow_automation(user_command):
            return
        
        plan = self.interpret_command(user_command)
        print("\nAI Generated Plan:")
        print(plan)
        print("=" * 60)

        method = ""
        command = ""

        lines = plan.splitlines()
        for i, line in enumerate(lines):
            if line.startswith("METHOD:"):
                method = line.split(":", 1)[1].strip().lower()
            elif line.startswith("COMMAND:"):
                # Get command and all following lines
                command_parts = [line.split(":", 1)[1].strip()]
                for j in range(i + 1, len(lines)):
                    if not lines[j].startswith("----") and lines[j].strip():
                        command_parts.append(lines[j])
                    elif lines[j].startswith("----"):
                        break
                command = "\n".join(command_parts)

        if not method or not command:
            print("ERROR: Could not parse AI output.")
            return

        if self.confirmation_required:
            ch = input(f"WARNING: Execute using [{method}]? (y/n): ").strip().lower()
            if ch != "y":
                print("CANCELLED.")
                return

        try:
            if method == "cmd":
                self.run_cmd(command)
            elif method == "powershell":
                self.run_powershell(command)
            elif method == "python":
                self.run_python_subprocess(command)
            elif method == "pyautogui":
                self.run_pyautogui(command)
            elif method == "office":
                self.run_office(command)
            elif method == "screen":
                self.run_screen_analysis(command)
            elif method == "search":
                self.run_search_explanation(command)
            elif method == "file":
                self.run_file_analysis(command)
            elif method == "system":
                self.run_system_call(command)
            else:
                print("WARNING: Unknown method, fallback to system call.")
                self.run_system_call(command)
            print("SUCCESS: Command executed successfully!")
            self.success_failure_tracker(user_command, method, 1)
            
            # Generate intelligent response based on command
            response = self._generate_smart_response(user_command, method)
            
            # Return response immediately - next move will be handled by command.py
            return response
            
        except Exception as e:
            print(f"ERROR executing: {e}")
            self.success_failure_tracker(user_command, method, 0, str(e))
            
            # Try fallback execution for basic commands
        
            
            if not self.smart_error_recovery(user_command, str(e)):
                print("❌ No automatic recovery available")
            return f"Failed to execute: {user_command}"
    
    # Next move predictions control methods
    def enable_next_move_predictions(self):
        self.next_move_predictions_enabled = True
        return "Next move predictions enabled"
    
    def disable_next_move_predictions(self):
        self.next_move_predictions_enabled = False
        return "Next move predictions disabled"
    
    def get_next_move_status(self):
        return self.next_move_predictions_enabled

# Global instance
# Create global instance
ultimate_ai = UltimateAIExecutor()

# Main function to use from other modules
def execute_desktop_command(command):
    """Execute any desktop automation command"""
    return ultimate_ai.execute_command(command)

# Quick access functions
def open_app(app_name):
    return execute_desktop_command(f"open {app_name}")

def system_control(action):
    return execute_desktop_command(action)

def create_document(doc_type, content=""):
    return execute_desktop_command(f"create {doc_type} document with {content}")

def ai_automation(task):
    return execute_desktop_command(f"use AI to {task}")

if __name__ == "__main__":
    # Test the system
    print("Ultimate AI Executor Ready!")
    print(execute_desktop_command("open calculator"))
    print(execute_desktop_command("check system info"))

def execute_command(cmd):
    """Simple function to execute any command"""
    return ultimate_ai.execute(cmd)

if __name__ == "__main__":
    print("🧠 Ultimate AI Executor Activated with Proactive Learning!")
    print("🤖 Features: Learning, Predictions, Auto-Recovery, AI Next-Move Execution")
    print("Examples:")
    print(" - open chrome and go to youtube")
    print(" - create ppt about AI")
    print(" - write hello world in notepad")
    print(" - what am I using on screen")
    print(" - explain my screen content")
    print(" - search google for python and explain")
    print(" - read and explain a.txt file")
    print(" - morning_routine (workflow automation)")
    print(" - work_setup (workflow automation)")
    print(" - shutdown laptop after 1 minute")
    print("=" * 50)
    
    analytics = ultimate_ai.behavioral_analytics()
    if analytics['total_commands'] > 0:
        print(f"📊 Your Stats: {analytics['success_rate']:.1f}% success rate, {analytics['total_commands']} command types learned")
    

    print()

    while True:
        cmd = input("\n🗣️ You: ").strip()
        if cmd.lower() in ["exit", "quit"]:
            break
        execute_command(cmd)