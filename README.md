# 🔐 Password Manager

A secure command-line password manager built with **Python**, **SQLAlchemy**, **Fernet encryption**, and **Neon PostgreSQL**. The application follows a **zero-knowledge architecture**, ensuring that user passwords remain encrypted at all times and cannot be recovered if the master password is lost.

## Features

* Secure user registration and authentication
* Zero-knowledge security model
* Password encryption using Fernet
* Salted hashing for master passwords
* Cloud-backed storage with Neon PostgreSQL
* Password generator
* Password strength analysis
* Duplicate password detection
* Session timeout for improved security
* Automatic clipboard clearing
* Add, retrieve, update, and delete stored passwords
* Complete user deletion with associated vault cleanup

## Tech Stack

* Python 3
* SQLAlchemy
* PostgreSQL (Neon)
* Cryptography (Fernet)
* python-dotenv

## Project Structure

```
password-manager/
│
├── src/
├── screenshots/
├── tests/
├── README.md
├── requirements.txt
├── .env.example
└── LICENSE
```

## Installation

### Clone the repository

```bash
git clone https://github.com/<your-username>/password-manager.git
cd password-manager
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Create a `.env` file

Use the provided `.env.example` as a template.

Example:

```env
USERS_connection_string=YOUR_USERS_DATABASE_URL
VAULTS_connection_string=YOUR_VAULT_DATABASE_URL
```

### Run the application

```bash
python src/main.py
```

## Security

This project is designed around a **zero-knowledge principle**.

* Master passwords are never stored in plaintext.
* Passwords are encrypted before being stored in the database.
* Encryption keys are derived from user credentials.
* Clipboard contents are automatically cleared after copying passwords.
* User sessions automatically expire after inactivity.
* If a master password is forgotten, stored passwords cannot be recovered by design.

## Future Improvements

* Two-factor authentication (TOTP)
* Password sharing
* Secure password import/export
* GUI version
* Browser extension
* Automated backup and restore

## Screenshots

Add screenshots of the application inside the `screenshots/` folder and reference them here.

## License

This project is licensed under the MIT License.

## Disclaimer

This project was built for educational and portfolio purposes to demonstrate secure software engineering practices. While it implements modern security concepts, it has not undergone an independent professional security audit and should not be relied upon as a production password manager without further review.
