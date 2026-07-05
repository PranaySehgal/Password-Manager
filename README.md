# 🔐 Password Manager

A secure command-line password manager built with Python that enables users to safely store and manage their credentials using strong encryption. The application uses Fernet encryption for protecting stored passwords, SQLAlchemy for database interactions, and Neon PostgreSQL for cloud-hosted storage. Its security model derives the encryption key from the user's master password during each authenticated session, ensuring that encryption keys are never stored.

---

## ✨ Features

* Secure user registration and login
* Master password authentication with salted password hashing
* Fernet encryption for all stored credentials
* Encryption key derived from the master password at login
* Add, retrieve, update, and delete stored credentials
* Secure password generator
* Vault Health Report based on password reuse and password age
* Duplicate password detection
* Secure account deletion with automatic removal of associated credentials
* Cloud-hosted storage using Neon PostgreSQL
* Environment-based configuration using `.env`

---

## 🛠️ Tech Stack

* **Language:** Python 3
* **Database:** Neon PostgreSQL
* **ORM:** SQLAlchemy
* **Encryption:** Cryptography (Fernet)
* **Configuration:** python-dotenv

---

## 🏗️ Architecture

The application follows a simple and secure workflow where every vault operation is performed only after successful user authentication.

```text
                          ┌──────────────┐
                          │    User      │
                          └──────┬───────┘
                                 │
                                 ▼
                    ┌────────────────────────┐
                    │ Command Line Interface │
                    └──────────┬─────────────┘
                               │
                               ▼
                    ┌────────────────────────┐
                    │ Login / Registration   │
                    └──────────┬─────────────┘
                               │
                 Verify Master Password Hash
                               │
                               ▼
               Derive Fernet Encryption Key
                               │
                               ▼
                    ┌────────────────────────┐
                    │       Main Menu        │
                    └──────────┬─────────────┘
                               │
      ┌──────────┬──────────┬──────────┬──────────┬────────────┐
      ▼          ▼          ▼          ▼          ▼
 Add Password Retrieve   Update     Delete    Vault Report
              Password   Password   Password
      │          │          │          │          │
      └──────────┴──────────┴──────────┴──────────┘
                               │
                               ▼
                   Encrypt / Decrypt Credentials
                               │
                               ▼
                     Neon PostgreSQL Database
```

---

## 🔄 Application Workflow

```text
User
   │
   ▼
Enter Master Password
   │
   ▼
Verify Password Hash
   │
   ▼
Derive Fernet Key
   │
   ▼
Main Menu
   │
   ├── Add Credential ─────► Encrypt ─────► Store
   │
   ├── Retrieve Credential ─► Decrypt ───► Display
   │
   ├── Update Credential ───► Encrypt ───► Store
   │
   ├── Delete Credential ───► Remove
   │
   └── Vault Health Report ─► Analyze Password Age & Reuse
```

---

## 🔒 Security

Security was the primary focus while designing this project.

* Master passwords are stored only as salted hashes.
* Master passwords are never stored in plaintext.
* Website credentials remain encrypted while stored in the database.
* The Fernet encryption key is derived from the user's master password during every authenticated session.
* Encryption keys are never stored in the database.
* Credentials are decrypted only after successful authentication.
* Sensitive configuration values are stored using environment variables.
* The application follows a **zero-recovery** security model. Since the encryption key is derived from the user's master password, a forgotten master password cannot be recovered, and neither can the encrypted vault.

---

## 🚀 Installation

Clone the repository:

```bash
git clone https://github.com/PranaySehgal/Password-Manager.git
cd password-manager
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file based on `.env.example` and configure your Neon PostgreSQL connection strings.

Run the application:

```bash
python init.py
```

---

## 📊 Vault Health Report

The Vault Health Report helps users evaluate the overall security of their stored credentials.

It analyzes:

* Password reuse across multiple accounts
* Password age
* Overall vault health score

This encourages users to replace weak or reused credentials before they become a security risk.

---

## 🤝 Contributing

Contributions, suggestions, and improvements are welcome. Feel free to fork the repository, open an issue, or submit a pull request.

---

## 📄 License

This project is licensed under the MIT License.

---

## ⚠️ Disclaimer

This project was developed for educational and portfolio purposes to demonstrate secure software engineering practices, encryption, authentication, and database management. It has not undergone an independent professional security audit and should not be considered production-ready without further security review.
