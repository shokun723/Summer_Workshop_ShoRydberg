## Final Step — Log out of GitHub and clean setup

Before leaving, log out of all accounts so the next student can use the computer.

---

1. Log out of GitHub (browser)

Go to:

https://github.com/

Click your profile picture (top right)

Click:

Sign out

---

2. Log out of GitHub in VS Code

Open VS Code

Click the Accounts icon (bottom-left corner)

Click:

Sign out

---

3. Remove saved GitHub credentials (IMPORTANT)

On Windows:

Open the Start menu

Search:

Credential Manager

Open:

Credential Manager

Click:

Windows Credentials

Look for entries related to:

github.com  
git:https://github.com  

Click each one and select:

Remove

---

4. Clear Git user information

Open VS Code terminal and run:

git config --global --unset user.name
git config --global --unset user.email

---

5. Close VS Code

Close all VS Code windows.

---

6. Delete folders and docs 

delete folders and docs from last student.

---

7. Final check

Make sure:

- You are logged out of GitHub in the browser
- VS Code is not connected to any GitHub account
- No credentials remain saved

---

The computer is now ready for the next student.