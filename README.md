# LexorX

LexorX is a Flask-based web application that allows users to generate AI-powered content with user authentication, image history storage, and a modern UI. The project integrates Google’s `google-genai` to generate content and uses SQLite with SQLAlchemy for persistent storage. Users can register, log in, generate images from prompts, and view previously generated results.

---

## Features

* User registration and authentication
* Secure session handling with Flask-Login
* AI-powered image generation using Google `google-genai`
* Upload-assisted image generation workflow
* Stores generated images per user
* Personal image history page
* SQLite database persistence
* Responsive frontend templates styled with modern UI components

---

## Technology Stack

**Backend**

* Python
* Flask
* Flask-Login
* Flask-WTF
* SQLAlchemy

**AI**

* google-genai

**Other Dependencies**

* Pillow
* email-validator
* gunicorn

**Database**

* SQLite

---

## Project Structure

```
LexorX
│
├── run.py                 # Application entry point
├── requirements.txt       # Dependencies
├── instance/
│   └── site.db            # SQLite database
│
├── app/
│   ├── __init__.py        # App factory and configuration
│   ├── models.py          # Database models
│   ├── forms.py           # WTForms definitions
│   ├── routes.py          # Application routes and logic
│   │
│   ├── templates/         # HTML templates
│   └── static/            # Static assets
```

---

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd LexorX-main
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate     # Linux / macOS
venv\Scripts\activate        # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Configuration

The application requires:

* A Flask `SECRET_KEY`
* A valid Google `google-genai` API key

`SECRET_KEY` and database URI are configured in `app/__init__.py`.

The Google API key value is referenced inside `app/routes.py`. Replace the placeholder with a valid key.

SQLite database is automatically created on first run.

---

## Running the Application

### Development

```bash
python run.py
```

The application starts in debug mode and runs on:

```
http://127.0.0.1:5000
```

---

## Usage

1. Open the application in the browser.
2. Register a new user account.
3. Log in.
4. Navigate to the image generation page.
5. Enter a prompt (and optionally provide an image where applicable).
6. Generate content.
7. View previously generated results in the History section.

---

## Database

* Uses SQLite
* Database file is stored in `instance/site.db`
* Tables managed via SQLAlchemy models

---

## Notes

* Ensure Google GenAI API access is enabled.
* Passwords in the current implementation are not hashed. This should be updated before production use.
* Replace placeholder API key and secret key before deployment.

---

## License

This project does not currently include a license file.
