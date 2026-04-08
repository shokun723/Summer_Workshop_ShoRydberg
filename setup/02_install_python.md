# Step 2 — Install Python (Windows)

## Overview

In this step, you will install Python on your system.
We will use the official Python installer from python.org.

---

## 1. Download Python

Go to:

https://www.python.org/downloads/

Click the yellow button:

**Download Python 3.x.x**

This automatically downloads the latest stable version for Windows.

---

## 2. Make sure you have the correct installer

The file you download should look like:

```
python-3.x.x-amd64.exe
```

This is the **Windows 64-bit installer** (recommended).

Do NOT download:

* embeddable zip files
* source code
* 32-bit version (unless you specifically need it)

---

## 3. Run the installer

Double-click the downloaded `.exe` file to launch the installer.

---

## 4. CRITICAL STEP (do NOT skip)

At the bottom of the installer window, check this box:

```
[✔] Add Python to PATH
```

This is REQUIRED or Python will not work correctly from the terminal.

---

## 5. Install Python

Click:

```
Install Now
```

Wait for the installation to complete.

---

## 6. Verify installation

Open **Command Prompt** and run:

```
python --version
```

You should see something like:

```
Python 3.x.x
```

---

# If you already have Python installed

Many users already have an older Python version (e.g., 3.7 or Anaconda).
This can cause conflicts.

---

## Option A — Clean install (Recommended)

1. Open:

   ```
   Control Panel → Programs → Uninstall a program
   ```

2. Uninstall:

   * Old Python versions (e.g., Python 3.7)
   * Anaconda / Miniconda (if installed)

3. Restart your computer (optional but recommended)

4. Install Python again following this guide

---

## Option B — Keep old versions (Advanced)

If you want to keep older Python versions:

1. Open:

   ```
   Environment Variables
   ```
2. Under **System variables**, edit:

   ```
   Path
   ```
3. Remove any old Python entries such as:

   ```
   Python37
   Anaconda3
   ```
4. Ensure your new Python path is included, for example:

   ```
   C:\Users\YourName\AppData\Local\Programs\Python\Python3xx\
   C:\Users\YourName\AppData\Local\Programs\Python\Python3xx\Scripts\
   ```

Windows uses the first Python it finds in PATH.

---

## 7. Troubleshooting

If `python --version` shows the wrong version:

* Close and reopen Command Prompt
* Restart your computer
* Re-check PATH settings
* Make sure no older Python (e.g., Anaconda) is overriding it

---

## Done

You now have Python installed and ready to use.
