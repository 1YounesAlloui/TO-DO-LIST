const { app, BrowserWindow } = require('electron');
const path = require('path');
const { spawn } = require('child_process');
const http = require('http');

let mainWindow;
let djangoProcess;

const DJANGO_PORT = 8080;
const DJANGO_URL = `http://127.0.0.1:${DJANGO_PORT}`;

// The workspace directory where the database and code reside
const workspaceDir = 'C:\\Users\\AZUR\\OneDrive\\Bureau\\to-do-list';

function startDjango() {
  const pythonPath = path.join(workspaceDir, 'venv', 'Scripts', 'python.exe');
  const managePyPath = path.join(workspaceDir, 'app', 'manage.py');

  console.log(`Starting Django server...`);
  console.log(`Working directory: ${path.join(workspaceDir, 'app')}`);
  console.log(`Python interpreter: ${pythonPath}`);

  djangoProcess = spawn(pythonPath, ['manage.py', 'runserver', `127.0.0.1:${DJANGO_PORT}`], {
    cwd: path.join(workspaceDir, 'app'),
    env: { ...process.env, PYTHONUNBUFFERED: '1' }
  });

  djangoProcess.stdout.on('data', (data) => {
    console.log(`[Django] ${data.toString().trim()}`);
  });

  djangoProcess.stderr.on('data', (data) => {
    console.error(`[Django Error] ${data.toString().trim()}`);
  });

  djangoProcess.on('close', (code) => {
    console.log(`Django process exited with code ${code}`);
  });
}

function createMainWindow() {
  mainWindow = new BrowserWindow({
    width: 1300,
    height: 850,
    icon: path.join(__dirname, 'icon.ico'),
    title: "Document Workspace",
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js')
    }
  });

  // Remove default menu bar for a clean, app-like appearance
  mainWindow.setMenuBarVisibility(false);

  // Poll the Django server URL until it responds, then load it
  const checkServer = setInterval(() => {
    http.get(DJANGO_URL, (res) => {
      // If we get any HTTP response, the server is up
      clearInterval(checkServer);
      mainWindow.loadURL(DJANGO_URL);
    }).on('error', () => {
      console.log('Waiting for Django server to start...');
    });
  }, 400);

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

app.whenReady().then(() => {
  startDjango();
  createMainWindow();
});

app.on('window-all-closed', () => {
  // Gracefully terminate the Django server when all Electron windows are closed
  if (djangoProcess) {
    console.log('Terminating Django server...');
    if (process.platform === 'win32') {
      spawn('taskkill', ['/pid', djangoProcess.pid, '/f', '/t']);
    } else {
      djangoProcess.kill('SIGINT');
    }
  }
  if (process.platform !== 'darwin') {
    app.quit();
  }
});
