# Step 4 — GitHub Setup

In this step, you will:

* Log into GitHub
* Create your own repository
* Add instructors as collaborators
* Clone BOTH repositories:

  * Workshop repository (instructions)
  * Your personal repository (your work)

---

## 1. Create or log into GitHub

Go to:

https://github.com/

* If you don’t have an account → click **Sign up**
* If you already have one → click **Sign in**

---

## 1.5 Log into GitHub in VS Code (IMPORTANT)

Even if you logged into GitHub in your browser, you must also log in inside VS Code.

1. Open VS Code
2. Look at the bottom-left corner
3. Click the Accounts icon (👤)
4. Select:

```text
Sign in with GitHub
```

5. A browser window will open
6. Click:

```text
Authorize Visual Studio Code
```

---

## 2. Create your own repository (your work)

Now, on the browser:

1. Click the **"+" (top right corner)**
2. Select:

```text
New repository
```

3. Fill in:

* Repository name:

```text
summer-workshop-yourname
```

(Replace *yourname* with your name)

* Visibility:

```text
Private
```

---

## 3. Initialize your repository (IMPORTANT)

Before clicking **Create repository**, enable:

```text
✔ Add a README file
✔ Add .gitignore → select "Python"
```

Leave:

```text
License → No license
```

4. Click:

```text
Create repository
```

---

## 4. Add instructors as collaborators

1. Open your repository
2. Go to:

```text
Settings → Collaborators
```

3. Click:

```text
Add people
```

4. Add your instructor(s)

---

## 5. Clone the workshop repository (instructions)

Your instructor will provide a link.

1. Open the link
2. Click:

```text
Code
```

3. Copy the HTTPS link

---

## 6. Clone using VS Code

1. Open VS Code
2. Press:

```text
Ctrl + Shift + P
```

3. Type:

```text
Git: Clone
```

4. Paste the workshop repository link
5. Choose a location
6. Click:

```text
Open
```

 This folder contains the instructions and starter files.

---

## 7. Clone your repository (your work)

Repeat the same steps:

1. Press:

```text
Ctrl + Shift + P
```

2. Select:

```text
Git: Clone
```

3. Paste YOUR repository link
4. Choose a location
5. Click:

```text
Open
```

 This is the folder where your work will be saved.

---

## 8. Copy workshop files into your repository

Now copy files from the workshop repository into your repository.

You can:

* Drag and drop files in VS Code
* Or copy/paste between folders

---

## 9. Save your work to GitHub

In your repository folder (NOT the workshop folder):

Open terminal and run:

```bash
git add .
git commit -m "Initial workshop setup"
git push
```

---

## 10. Verify

Go to your GitHub repository in your browser.

You should now see your files uploaded.

---

## 💡 Notes

* Workshop repository = instructions (do NOT push here)
* Your repository = your work (push here)
* Always make sure you are working in the correct folder
