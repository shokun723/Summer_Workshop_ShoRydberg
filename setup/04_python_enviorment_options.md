# Step 4 — Python Environment Options

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

## Important notes

* A virtual environment **uses your installed Python**
* It does NOT replace Python
* Each project can have its own environment
