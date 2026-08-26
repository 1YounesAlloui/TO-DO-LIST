const { app, BrowserWindow } = require('electron');
const path = require('path');
const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');

// Dynamically resolve Django path based on environment
const appDir = app.isPackaged
  ? path.join(process.resourcesPath, 'app')
  : path.join(__dirname, '..', 'app');

// Automatically load environment variables
const envPath = path.join(appDir, '.env');
if (fs.existsSync(envPath)) {
  try {
    require('dotenv').config({ path: envPath });
  } catch (err) {
    console.log('dotenv package not installed, skipping automatic .env loading');
  }
}

let mainWindow;
let djangoProcess;

const DJANGO_PORT = 8080;
const DJANGO_URL = `http://127.0.0.1:${DJANGO_PORT}`;

// Resolve Python path inside appDir
const venvPython = path.join(appDir, 'venv', 'Scripts', 'python.exe');
const pythonPath = fs.existsSync(venvPython) ? venvPython : 'python';

function startDjango() {
  console.log(`Starting Django server...`);
  console.log(`Working directory: ${appDir}`);
  console.log(`Python interpreter: ${pythonPath}`);

  djangoProcess = spawn(pythonPath, ['manage.py', 'runserver', `127.0.0.1:${DJANGO_PORT}`], {
    cwd: appDir,
    env: { ...process.env, PYTHONUNBUFFERED: '1' }
  });

  djangoProcess.stdout.on('data', (data) => {
    console.log(`[Django] ${data.toString().trim()}`);
  });

  djangoProcess.stderr.on('data', (data) => {
    console.error(`[Django Error] ${data.toString().trim()}`);
  });

  djangoProcess.on('error', (err) => {
    console.error('[Django Process Error]:', err);
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

  mainWindow.setMenuBarVisibility(false);

  const checkServer = setInterval(() => {
    http.get(DJANGO_URL, (res) => {
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