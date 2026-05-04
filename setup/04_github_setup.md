# Step 4 — GitHub Setup

In this step, you will:

* Log into GitHub
* Create your own copy of the workshop repository
* Add instructors as collaborators
* Clone your copy to your computer
* Save your work to your own repository

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

```text id="h0r7f3"
Sign in with GitHub
```

5. A browser window will open
6. Click:

```text id="z5nq3y"
Authorize Visual Studio Code
```

---

## 2. Fork the workshop repository (IMPORTANT)

Your instructor will provide a repository link.

1. Open the workshop repository in your browser
2. Click:

```text id="w4n6d2"
Fork
```

(top-right corner)

3. Keep the default settings
4. Click:

```text id="k9x2p1"
Create fork
```

👉 This creates your own copy of the repository under your account.

---

## 3. Rename your repository

After forking, rename your repository:

1. Go to your forked repository
2. Click:

```text id="v2c8r0"
Settings
```

3. Change the name to:

```text id="q7p1e4"
summer-workshop-yourname
```

4. Click:

```text id="j3m9s6"
Rename
```

---

## 4. Add instructors as collaborators

1. In your repository, go to:

```text id="t8f4b2"
Settings → Collaborators
```

2. Click:

```text id="d6k1x7"
Add people
```

3. Add your instructor(s)

---

## 5. Clone your repository (your work)

1. Open your repository
2. Click:

```text id="p2n7w5"
Code
```

3. Copy the HTTPS link

---

## 6. Clone using VS Code

1. Open VS Code
2. Press:

```text id="m4v9c2"
Ctrl + Shift + P
```

3. Type:

```text id="b8y3q1"
Git: Clone
```

4. Paste your repository link
5. Choose a location
6. Click:

```text id="z1k6t8"
Open
```

👉 This will:

* Create a folder
* Download your repository
* Open it in VS Code

---

## 7. Work on the files

* Edit notebooks
* Follow instructions
* Save your work

All changes will be saved in your repository only.

---

## 8. Save your work to GitHub

In VS Code terminal:

```bash id="x9d2m4"
git add .
git commit -m "My progress"
git push
```

---

## 9. Verify

Go to your repository in the browser.

You should see your changes updated.

---

## 💡 Notes

* Your repository is a copy of the instructor’s repository
* You can edit files without affecting the original
* All your work is saved in your own repository
* Instructors can view your progress if added as collaborators
