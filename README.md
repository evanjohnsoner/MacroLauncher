# 🎯 MacroLauncher v4.4

## 💡 What is MacroLauncher?

MacroLauncher is a next-generation Python-based launcher designed to run and manage verified macros safely and automatically.  
It uses a secure cloud-based license system and includes a clean, modern interface with a built-in dependency installer.

Perfect for macro users, testers, or creators who want a reliable and self-maintaining launcher.

---

## ✨ Key Features

- 🪄 One-click launching — Start or stop any `.pyw` macro instantly  
- 🔒 Secure key verification — Validates your access key with Firebase  
- 💾 HWID protection — Each key is tied to one device automatically  
- ⚙️ Automatic dependency installer — Installs only missing packages  
- 📜 Smart installation logs — Real-time feedback inside the launcher  
- 💻 Lightweight UI — Simple, fast, and distraction-free  
- 🧠 Auto-settings editor — Each macro’s `settings.py` loads automatically  
- 🎥 Built-in tutorial links — Opens YouTube guides from each macro folder  
- 🌐 Version synchronization — Checks your local version with Firebase  

---

## ⚙️ How It Works

### 🔑 Key Validation
When you launch the app:
1. The launcher connects securely to a Server.
2. Your key is verified against the online database.
3. If unassigned, it links to your HWID (hardware ID) automatically.
4. If valid, you gain full access — otherwise, it shows a descriptive error.

---

### 🧱 Dependency Installer
- The launcher automatically runs `sys/install_requirements.bat` during startup.  
- It checks for:
  - Python 3.12+
  - Pip
  - customtkinter
  - requests
  - psutil
  - python-dotenv
  - pywinstyles
- Missing dependencies are installed automatically, and progress is displayed in real time.  
- The installer runs smoothly in the background without freezing the UI.  

✅ It also detects and installs dependencies from every macro’s subfolder recursively.

---

## 🚀 Getting Started

### 1️⃣ Run the Launcher
Simply double-click `launcher.exe`.

- The launcher will automatically check and install any missing dependencies.  

---

### 2️⃣ Enter Your Key
Once loaded:
- Enter your access key (provided).  
- The launcher verifies it online and assigns your HWID if new.  
- If valid, you can launch any macro instantly.

---

### 3️⃣ Add New Macros
To install a new macro:
1. Copy the macro folder into `/macros/`
2. Run the launcher like normal and it will auto-detect the macro
3. If it has extra dependencies, they’ll be installed automatically

Each macro can optionally include:
- `settings.py` → editable parameters  
- `instruct.txt` → YouTube or help link  
- `install_requirements.bat` → optional dependencies  

---

## 💬 Support

### Discord: pew.kk

💡 If the launcher fails to open, run `sys/install_requirements.bat` manually once, then relaunch.  
⚠️ Never run macros directly — always launch them through MacroLauncher to ensure proper token validation.

---

## 🧠 Notes

- Tested on Windows 11  
- Requires Internet connection
- Server access is secured
- HWID binding ensures fair key usage  
- Supports both `.pyw` and macro sub-dependencies  

---

### 🚀 Built by Ak  

🪶 MacroLauncher v4.4 — Secure, Automated, and Effortless.
