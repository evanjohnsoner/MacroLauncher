# 🎯 MacroLauncher v4.4  

## 💡 What is MacroLauncher?  

**MacroLauncher** is a modern Python-based launcher that automatically manages, updates, and runs your macros.  
It includes a built-in dependency manager, key validation through a secure server, and a clean, lightweight interface.  

It’s designed for macro creators and testers who want a plug-and-play launcher that handles setup for them.  

---

## ✨ Key Features  

- ⚡ **One-click launch** — start any macro instantly  
- 🔑 **Key validation** — verifies your access key through a secure server  
- 💻 **Device binding** — each key automatically links to your device  
- ⚙️ **Smart dependency installer** — installs only what’s missing  
- 📦 **Macro-level dependency setup** — scans and installs from each macro’s own folder  
- 🧠 **Automatic key saving** — remembers your verified access key securely  
- 🚀 **Fast startup** — optimized installer and GUI for instant launch  
- 🧩 **Auto-detect macros** — new macros in the `/macros` folder appear automatically  

---

## 🧱 How It Works  

### 🔑 Key Validation  
1. When launched, the app connects to the online **server**.  
2. Your **access key** is checked against the **database**.  
3. If it’s new, it’s automatically linked to your device.  
4. If valid, you gain instant access to all available macros.  

---

### 🧩 Dependency Manager  

- The launcher runs `sys/install_requirements.bat` on startup.  
- It checks for and installs only missing dependencies like:  
  - `customtkinter`  
  - `requests`  
  - `python-dotenv`  
  - `psutil`  
  - `pywinstyles`  
- Automatically installs **Python 3.12+** if not found.  
- Runs quietly in the background while showing smooth progress in the UI.  
- Also detects and installs dependencies from every macro’s own `install_requirements.bat` file.  

✅ No unnecessary logs or text files — just a fast, self-maintaining setup.  

---

## 🚀 Getting Started  

### 1️⃣ Install via GitHub ZIP  

1. Go to the repository’s GitHub page.  
2. Click the green **“Code”** button → choose **“Download ZIP”**.  
3. Extract the ZIP anywhere on your PC (recommended: `C:\MacroLauncher`).  
4. Open the folder and double-click `launcher.pyw` (or `launcher.exe` if compiled).  

MacroLauncher will:  
- Check for Python and install it automatically if missing  
- Verify all required dependencies  
- Connect to the server and confirm your key and version  

---

### 2️⃣ Activate with Your Key  

- Enter your access key when prompted.  
- If valid, it will automatically bind to your device.  
- Once verified, it’s saved for future sessions.  

---

### 3️⃣ Add New Macros  

To add a new macro:  
1. Drop the macro folder into `/macros/`.  
2. Each macro can include its own:  
   - `install_requirements.bat` → installs missing packages  
   - `settings.py` → configuration file  
   - `instruct.txt` → guide or notes  
3. Relaunch MacroLauncher — it will auto-detect and prepare them.  

---

## ⚙️ Developer Notes  

- Each dependency script installs only what’s missing — no re-installs.  
- Compatible with both `.py` and `.pyw` macro files.  
- GUI built with `customtkinter`, optimized for smooth startup.  
- When compiled, all theme assets are bundled to prevent missing-file errors.  

---

## 💬 Support  

🛠 **Discord:** `pew.kk`  

💡 If the launcher doesn’t open:  
- Run `sys/install_requirements.bat` manually once, then relaunch.  
- Ensure you have an active Internet connection for version and key validation.  

---

## 🧠 Requirements  

- **Windows 10 or 11**  
- **Internet connection** (for key and version checks)  
- **Python 3.12+** (installed automatically if missing)  

---

### 🪶 Built by Ak  
**MacroLauncher v4.4** — Smart, Lightweight, and Self-Maintaining.  
