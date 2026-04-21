## 7. Install notebook packages in your virtual environment

Before running notebooks, install the required Python packages inside your virtual environment.

---

1. Open VS Code

Open the workshop folder.

---

2. Open the terminal

In VS Code, open the terminal.

Make sure your virtual environment is activated.

You should see something like:

(.venv_workshop)

at the beginning of the terminal line.

---

3. Install the required packages

Run:

pip install -r requirements.txt

---

Notes:

- `ipykernel` is required for running notebooks with a virtual environment.
- `torch` and `torchvision` are required for the CNN notebook.
- `matplotlib` and `numpy` are also required by the notebook imports.
- If a package install fails, make sure the virtual environment is activated before running the commands.