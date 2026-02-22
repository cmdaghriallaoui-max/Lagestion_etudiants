# Lagestion_etudiants - Student Management App

A Flask-based student management application with login, registration, and CRUD operations.

## Project Structure

```
├── app.py                 # Main Flask application
├── database.py            # Database connection and initialization
├── requirements.txt       # Python dependencies
├── vercel.json           # Vercel deployment configuration
├── .gitignore            # Git ignore rules
├── static/
│   ├── dashboard.css
│   └── style.css
└── templates/
    ├── dashboard.html
    ├── edit_student.html
    ├── login.html
    └── register.html
```

## Local Development

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run the Application
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Vercel Deployment

### Prerequisites
1. Vercel account (free at https://vercel.com)
2. GitHub account with this repository

### Changes Made for Vercel Compatibility

✅ **Modified app.py:**
- Added proper initialization to prevent database re-initialization on each request
- Made the secret key configurable via environment variables
- Added SQLite check before initialization

✅ **Updated requirements.txt:**
- Added all Flask dependencies for proper serverless support

✅ **vercel.json:**
- Already configured to route all requests to the Flask app

✅ **Added .gitignore:**
- Excludes unnecessary files like __pycache__, .DB files, and Vercel cache

### Deploy to Vercel

#### Step 1: Connect Your Repository
1. Go to https://vercel.com/dashboard
2. Click "Add New..." → "Project"
3. Select your GitHub repository (cmdaghriallaoui-max/Lagestion_etudiants)
4. Click "Import"

#### Step 2: Configure Environment Variables (Important!)
In the Vercel dashboard for your project:

1. Go to **Settings** → **Environment Variables**
2. Add the following:
   - **Key:** `SECRET_KEY` **Value:** `your-secret-key-here` (or use the default)
   - **Key:** `DATABASE_URL` **Value:** (optional for SQLite)

#### Step 3: Deploy
1. Click "Deploy"
2. Wait for the build to complete (2-3 minutes)
3. Your app will be available at your Vercel URL

### ⚠️ Important Notes about SQLite and Serverless

**SQLite Limitations on Vercel:**
- SQLite databases persist per deployment, but data is NOT retained between deployments
- Each new deployment creates a fresh database
- For production, consider migrating to a cloud database like:
  - PostgreSQL (via Neon, Railway, Heroku)
  - MongoDB
  - Firebase

**Current Setup:**
- The app uses SQLite (`students.db`) which is recreated on each deployment
- This is fine for development/testing
- For production persistence, update `database.py` to use a cloud database

### To Use a Cloud Database

1. **Option 1: PostgreSQL (Recommended)**
   ```bash
   pip install psycopg2-binary python-dotenv
   ```
   Update `database.py` to use PostgreSQL instead of SQLite

2. **Option 2: MongoDB**
   ```bash
   pip install pymongo python-dotenv
   ```

3. Add database connection string to Vercel Environment Variables

## Troubleshooting

### 502 Bad Gateway Error
- Check Vercel logs: Dashboard → Project → Deployments → Logs
- Ensure `requirements.txt` has all dependencies

### Database Not Persisting
- This is expected with SQLite on serverless
- Migrate to PostgreSQL or MongoDB for persistence

### Build Failures
- Check the `vercel.json` configuration
- Ensure `app.py` contains the Flask app instance

## Security Notes

⚠️ **Before Production:**
1. Change `secret_key` to a strong random value
2. Implement password hashing (use `werkzeug.security`)
3. Validate all user inputs
4. Add CSRF protection
5. Use HTTPS (Vercel provides this automatically)

## Git Credentials

Your git configuration has been set up with:
- Email: `c.mdaghriallaoui@esisa.ac.ma`
- Remote: `https://github.com/cmdaghriallaoui-max/Lagestion_etudiants.git`

## Next Steps

1. Test locally: `python app.py`
2. Push any changes: `git add . && git commit -m "message" && git push`
3. Deploy: Connect repo to Vercel and click Deploy

---

**Created:** February 2026
**Dependencies:** Flask 2.3.3
