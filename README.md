# Stray Animal Reporting App

This is a Flask web application for reporting stray animals.

## Setup and Deployment

### Local Setup

1. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Initialize the database:
   ```
   sqlite3 stray_animals.db < init_db.sql
   ```

4. Run the app:
   ```
   python app.py
   ```

### Deploying to Heroku

1. Create a Heroku account and install the Heroku CLI.

2. Login to Heroku:
   ```
   heroku login
   ```

3. Create a new Heroku app:
   ```
   heroku create your-app-name
   ```

4. Push the code to GitHub (if not already done):
   ```
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/yourusername/your-repo.git
   git push -u origin main
   ```

5. Deploy to Heroku:
   ```
   git push heroku main
   ```

6. Open the app in your browser:
   ```
   heroku open
   ```

You can now access the app on your phone using the Heroku app URL.

## Notes

- The app uses SQLite, which is not ideal for production. For production, consider using a managed database service.
- Uploaded images are saved in `static/uploads`.
