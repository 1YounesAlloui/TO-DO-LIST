# 📝 Document Workspace & To-Do List App

An all-in-one productivity suite featuring a **rich document editor**, a **responsive kanban-style to-do list**, a **calendar planner**, **real-time analytics**, and an **integrated AI Assistant**. Built on a robust **Django backend** and wrapped in an **Electron desktop client**, it offers a fluid, native desktop feel.

---

## ✨ Features

- **📊 Productivity Analytics**: Live visual telemetry of task distribution by status, daily activity trend, and priority using interactive charts.
- **📅 Dynamic To-Do List & Calendar**: Full CRUD interface for tasks, priority assignments, custom statuses (Pending, In Progress, Done), and scheduled due dates.
- **✍️ Workspace Document Editor**: High-fidelity text editor linked to individual tasks with local persistence.
- **🤖 Integrated AI Intelligence Engine**:
  - Direct integration with **Groq** and **OpenRouter** APIs.
  - Built-in capabilities for text **Summarization** (executive takeaways) and **Humanization** (conversational, professional polishing).
  - Selectable top-tier LLM models (Llama 3.3, GPT-4o Mini, DeepSeek V3, Gemini 1.5 Pro, and more).
- **🎨 Custom Theme System**: Dynamic switcher featuring beautiful themes like *Mountain Dawn*, *Ocean Horizon*, *Desert Canyon*, *Forest Sanctuary*, and *Sunset Highlands*.
- **📄 Document Exporters**: Instant server-side PDF and MS Word (DOC) exports for documentation.
- **🖥️ Desktop Shell Wrapper**: Frameless Electron app wrapping the backend Python service, providing automatic background startup and termination.

---

## 🛠️ Architecture

The project splits responsibility across two directories:
1. **`app/`**: A Django 6.0 web application that exposes the backend APIs, template views, database models, export engines, and proxy configurations.
2. **`desktop-app/`**: An Electron application wrapper that handles the local desktop window execution and launches the Python interpreter to serve the Django backend in a subprocess.

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.10+**
- **Node.js 18+** & **npm**

---

### Step 1: Backend Setup (Django)

1. Open your terminal and navigate to the `app` directory:
   ```bash
   cd app
   ```
2. Create and activate a Python virtual environment:
   - **Windows (PowerShell/CMD)**:
     ```bash
     python -m venv venv
     .\venv\Scripts\activate
     ```
   - **macOS/Linux**:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
3. Install the required Python dependencies:
   ```bash
   pip install django requests python-dotenv xhtml2pdf
   ```
4. Run database migrations to set up the SQLite database:
   ```bash
   python manage.py migrate
   ```
5. *(Optional)* Start the Django development server standalone:
   ```bash
   python manage.py runserver 8080
   ```

---

### Step 2: Environment Configuration

Create a `.env` file inside the `app/` directory and populate it with your AI API keys:
```env
# Groq API Key (Optional, for Groq Models)
GROQ_API_KEY=your-groq-api-key-here

# OpenRouter API Key (Optional, for OpenRouter Models)
OPENROUTER_API_KEY=your-openrouter-api-key-here
```

---

### Step 3: Desktop App Setup (Electron)

1. Navigate to the `desktop-app` directory:
   ```bash
   cd ../desktop-app
   ```
2. Install the Node dependencies:
   ```bash
   npm install
   ```
3. **Important Configuration:** Open `desktop-app/main.js` and edit the `workspaceDir` path (around line 13) to point to your absolute project root folder:
   ```javascript
   // Change this to the absolute path of this project on your system
   const workspaceDir = 'C:\\path\\to\\TO-DO-LIST-main';
   ```
4. Launch the application:
   ```bash
   npm start
   ```

---

## 📁 Project Structure

```
├── app/                        # Django Backend
│   ├── app/                    # Django Project Core Settings/URLs
│   ├── templates/              # HTML Templates (Base, Home, Editor, AI)
│   ├── todo/                   # Main App Logic (Models, Views, Static CSS/JS)
│   │   ├── static/             # Static Assets (Style Sheets, JavaScript files)
│   │   ├── system_prompt.txt   # Base Prompt constraints for the AI Agent
│   │   ├── models.py           # Database models (Tasks and Content fields)
│   │   └── views.py            # AI proxies, stats engines, CRUD, and exports
│   └── manage.py               # Django management CLI script
│
├── desktop-app/                # Electron Desktop Wrapper
│   ├── icon.ico / icon.png     # Application icons
│   ├── main.js                 # Subprocess spawner & Electron Window setup
│   ├── package.json            # Electron dependency configurations
│   └── preload.js              # IPC bridge scripts
│
├── app_icon.ico                # Root level application icon
└── .gitignore                  # Git untracked pattern filters
```

---

## 💾 Exporting & Build

To compile a native distribution of the desktop application, run the build tools from the `desktop-app` folder:
- **Build Installer**:
  ```bash
  npm run dist
  ```
- **Pack directory**:
  ```bash
  npm run pack
  ```

This packages the app into the `dist/` directory inside `desktop-app/` using `electron-builder`.

---

## 📝 License

This project is open-source and free to customize.
