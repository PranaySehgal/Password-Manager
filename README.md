# 🔐 Password Manager v2.0.0

A secure command-line Password Manager built with Python that allows users to safely store, retrieve, update, delete, export, and import passwords using modern cryptographic techniques.

The project focuses on security, usability, and clean architecture while providing an intuitive natural-language command interface.

---

# Features

### Account Management

* User Registration
* Secure Login
* Change Master Password
* Delete User Account

### Password Vault

* Add Passwords
* Retrieve Passwords using filters
* Update Existing Passwords
* Delete Passwords
* Vault Statistics & Reports

### Secure Backup & Restore (v2.0.0)

* Export encrypted password vault
* Separate export password generated automatically
* Import encrypted backups
* Merge missing accounts into existing vault
* Override existing passwords during import
* Versioned backup format for future compatibility

### Natural Language CLI

Instead of using numbered menus, the application understands commands such as:

* Create Password
* Add Password
* Save Account
* Fetch Accounts
* Show Passwords
* Delete Password
* Update Password
* Change Master Password
* Export Passwords
* Import Passwords
* Logout

---

# Security

## Master Password Protection

* Passwords are hashed using **Argon2** before storage.
* Plaintext master passwords are never stored.

## Password Encryption

* Every stored password is encrypted using **Fernet (AES-128 in CBC mode with HMAC authentication)**.
* Encryption keys are derived using **PBKDF2-HMAC-SHA256** with a unique salt.

## Backup Security

* Exported passwords are protected using a **separate randomly generated export password**.
* Import requires the correct export password before any password can be restored.
* Imported passwords are automatically re-encrypted using the current user's master password.

## Brute Force Protection

* Progressive login delays help slow repeated incorrect password attempts.

---

# Technologies Used

* Python
* SQLAlchemy
* SQLite / SQL Database
* Cryptography
* Argon2
* Python-dotenv

---

# Project Structure

```text
Password-Manager/
│
├── login.py
├── menu.py
├── export.py
├── accessVault.py
├── addIntoVault.py
├── updateVault.py
├── deleteVault.py
├── deleteUser.py
├── updateMasterPassword.py
├── passwordRecognizerAndGenerator.py
├── vaultReport.py
├── Exports/
├── .env
└── README.md
```

---

# Installation

Clone the repository:

```bash
git clone https://github.com/PranaySehgal/Password-Manager.git
```

Move into the project directory:

```bash
cd Password-Manager
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure your `.env` file with the required database connection string and application settings.

Run the application.

---

# Future Improvements

* AI-powered command understanding
* Multi-backup selection during import
* Password history
* Secure password sharing
* Cross-platform installer
* Automatic encrypted cloud backups
* GUI version

---

# Disclaimer

This project was built for educational and portfolio purposes while following modern security practices. Users are encouraged to review the source code before storing sensitive information.

---

# License

This project is released under the MIT License.
