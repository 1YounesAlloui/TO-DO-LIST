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

The Electron wrapper spawns `python.exe` directly (no shell activation) to run `manage.py runserver`. Because of that, the Python virtual environment (`venv/`) must live **inside `desktop-app/`**, not inside `app/` — `main.js` resolves the interpreter path relative to the Electron app's own directory in dev, and relative to the packaged app's `resources` folder once built.

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.10+**
- **Node.js 18+** & **npm**

---

### Step 1: Backend Dependencies

The virtual environment lives in `desktop-app/`, but the Django project itself still lives in `app/`. Create the venv from inside `desktop-app/`, then use it to install dependencies and run backend setup commands against `app/`:

- **Windows (PowerShell/CMD)**:
  ```bash
  cd desktop-app
  python -m venv venv
  .\venv\Scripts\activate
  ```
- **macOS/Linux**:
  ```bash
  cd desktop-app
  python3 -m venv venv
  source venv/bin/activate
  ```

With the venv active, install dependencies and run migrations against the Django project:
```bash
pip install django requests python-dotenv xhtml2pdf
cd ../app
python manage.py migrate
```

*(Optional)* Start the Django development server standalone:
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
   cd desktop-app
   ```
2. Install the Node dependencies:
   ```bash
   npm install
   ```
3. Confirm `desktop-app/venv/Scripts/python.exe` exists (from Step 1) — `main.js` expects the interpreter there and needs no manual path configuration.
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
│   ├── venv/                   # Python virtual environment (created locally, not committed)
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

Run the build tools from the `desktop-app` folder. `package.json` bundles `app/` and `venv/` as `extraResources`, copied as real files alongside the executable rather than zipped into `app.asar` — this is required because Node's `spawn()` cannot execute a binary from inside an asar archive.

- **Pack directory** (fast, no installer — use this to test packaging first):
  ```bash
  npm run pack
  ```
  Then run the executable directly from `dist/win-unpacked/` and confirm `resources/venv/Scripts/python.exe` and `resources/app/manage.py` both exist and the app launches without an ENOENT error.

- **Build Installer** (once `pack` works cleanly):
  ```bash
  npm run dist
  ```

Both commands output into the `dist/` directory inside `desktop-app/`.

---

## 📝 License

This project is open-source and free to customize.