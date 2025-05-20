# Stray Animal App

This is a Flask web application for reporting and managing stray animal cases.

## Features

- User signup and login
- NGO login with code number
- Submit reports with description, location, and image upload
- View reports and update status
- Notice reports with NGO contact info
- Session management and access control

## Requirements

- Python 3.8+
- Flask
- Werkzeug
- SQLite3

## Setup

1. Install dependencies:

```
pip install -r requirements.txt
```

2. Initialize the database:

```
sqlite3 stray_animals.db < init_db.sql
```

3. Run the app:

```
python app.py
```

## Deployment on Deta.sh

1. Create a Deta account at https://deta.sh/
2. Install Deta CLI:

```
curl -fsSL https://get.deta.dev/cli.sh | sh
```

3. Login to Deta CLI:

```
deta login
```

4. Initialize a new Deta project in your app directory:

```
deta new --python
```

5. Deploy the app:

```
deta deploy
```

6. Access the public URL provided by Deta to use the app on your phone.

## Notes

- Ensure the `static/uploads` directory exists and is writable for image uploads.
- Update `app.py` if needed to handle environment variables for production.
