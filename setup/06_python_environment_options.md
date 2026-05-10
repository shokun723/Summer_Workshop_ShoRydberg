# Step 6 — Python Environment Options

There are two common ways to run Python in VS Code.

---

## Option 1 — Use the local computer Python

This means using the Python installed directly on your computer.

**Example:**

```text
C:\Users\YourName\AppData\Local\Programs\Python\Python314\python.exe
```

### Pros

* Simple
* Fast to start
* Good for quick testing
* Fewer steps for beginners

### Cons

* Packages install globally
* Different projects can conflict with each other
* Harder to keep setups clean across multiple computers

---

## Option 2 — Use a virtual environment (recommended)

A virtual environment is a project-specific Python environment.

**Example:**

```text
project_folder\.venv\
```

### Pros

* Keeps packages isolated per project
* Cleaner and more professional
* Easier to reproduce the same setup on other computers
* Best practice for coding projects

### Cons

* One extra setup step
* Requires selecting/activating the environment

---

## Create a virtual environment (practice)

Run this inside your project folder (VS Code terminal):

```bash
python -m venv .venv_workshop
```

This creates a new environment:

```text
.venv_workshop
```

---

## Activate the environment

### PowerShell:

```powershell
.venv_workshop\Scripts\Activate.ps1
```

### Command Prompt:

```cmd
.venv_workshop\Scripts\activate.bat
```

---

## Verify activation

Your terminal should now show:

```text
(.venv_workshop)
```

This means the environment is active.

---

## Important: Do NOT push environments to GitHub

Virtual environments should NOT be uploaded to GitHub because:

* They are large
* They are specific to your computer
* They can break on other systems

---

## Create a `.gitignore` file

In your project folder, create a file named:

```text
.gitignore
```

Add the following:

```gitignore
# Virtual environments
.venv/
.venv_workshop/
env/
venv/

# Python cache
__pycache__/
*.pyc

# Jupyter checkpoints
.ipynb_checkpoints/

# VS Code settings (optional)
.vscode/
```

---

## If the environment was already tracked by Git

Run this once:

```bash
git rm -r --cached .venv_workshop
```

This removes it from Git tracking **without deleting it locally**.

---

## Important notes

* A virtual environment **uses your installed Python**
* It does NOT replace Python
* Each project can have its own environment
* `.gitignore` prevents environments from being uploaded to GitHub
