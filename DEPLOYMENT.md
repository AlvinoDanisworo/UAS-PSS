# Deployment Guide for SimpleLMS

## 🚀 Deploy to Railway

### Prerequisites
- GitHub account with repository pushed
- Railway account (sign up at railway.app)

### Step-by-Step Deployment

1. **Go to Railway Dashboard**
   - Visit: https://railway.app
   - Click "New Project"
   - Select "Deploy from GitHub repo"

2. **Connect Repository**
   - Authorize Railway to access your GitHub
   - Select: `AlvinoDanisworo/UAS-PSS`
   - Railway will auto-detect the Dockerfile

3. **Add PostgreSQL Database**
   - Click "New" → "Database" → "Add PostgreSQL"
   - Railway will automatically provision a PostgreSQL instance

4. **Set Environment Variables**
   Click on your service → Variables → Add these:
   
   ```
   SECRET_KEY=generate-new-secret-key-here
   DEBUG=False
   ALLOWED_HOSTS=your-app-name.railway.app
   
   # Database (Railway will auto-populate these from PostgreSQL service)
   DB_ENGINE=django.db.backends.postgresql
   DB_NAME=${{Postgres.PGDATABASE}}
   DB_USER=${{Postgres.PGUSER}}
   DB_PASSWORD=${{Postgres.PGPASSWORD}}
   DB_HOST=${{Postgres.PGHOST}}
   DB_PORT=${{Postgres.PGPORT}}
   
   # JWT
   JWT_ACCESS_TOKEN_LIFETIME_HOURS=24
   JWT_REFRESH_TOKEN_LIFETIME_DAYS=7
   ```

5. **Generate SECRET_KEY**
   Run locally:
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

6. **Deploy**
   - Railway will automatically deploy
   - Wait for build to complete (2-5 minutes)
   - Your app will be available at: `https://your-app-name.railway.app`

7. **Create Superuser** (Optional)
   - Go to Railway Dashboard
   - Click your service → Settings → "Connect to PostgreSQL"
   - Or use Railway CLI:
   ```bash
   railway run python code/manage.py createsuperuser
   ```

### Troubleshooting

**Build fails:**
- Check logs in Railway dashboard
- Verify all environment variables are set
- Ensure PostgreSQL service is running

**Static files not loading:**
- Verify `whitenoise` is in requirements.txt
- Check `STATIC_ROOT` and `STATICFILES_STORAGE` in settings.py

**Database connection error:**
- Verify PostgreSQL service is linked
- Check database environment variables

### Cost
- **Free Tier**: $5 credit/month (enough for testing)
- **Pro**: $20/month (better for production)

---

## 🎨 Deploy to Render

### Steps

1. **Create Render Account**
   - Visit: https://render.com
   - Sign up with GitHub

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect repository: `AlvinoDanisworo/UAS-PSS`

3. **Configure Service**
   ```
   Name: simplelms
   Environment: Docker
   Region: Oregon (US West)
   Branch: main
   ```

4. **Add PostgreSQL Database**
   - Click "New +" → "PostgreSQL"
   - Name: `simplelms-db`
   - Instance Type: Free

5. **Set Environment Variables**
   In Web Service → Environment:
   ```
   SECRET_KEY=your-secret-key
   DEBUG=False
   ALLOWED_HOSTS=simplelms.onrender.com
   DB_ENGINE=django.db.backends.postgresql
   DB_NAME=<from PostgreSQL dashboard>
   DB_USER=<from PostgreSQL dashboard>
   DB_PASSWORD=<from PostgreSQL dashboard>
   DB_HOST=<from PostgreSQL dashboard>
   DB_PORT=5432
   ```

6. **Deploy**
   - Click "Create Web Service"
   - Render will build and deploy automatically

### Cost
- **Free Tier**: Available (with spin-down after inactivity)
- **Paid**: $7/month

---

## ⚡ Deploy to Vercel + Neon (Alternative)

**Not recommended for this project** - Complex setup required for Django + PostgreSQL.

Better alternatives: **Railway** or **Render**.

---

## 📝 Post-Deployment Checklist

- [ ] App is accessible via URL
- [ ] Static files loading correctly
- [ ] Database connected (no 500 errors)
- [ ] Admin panel accessible at `/admin`
- [ ] API endpoints working at `/api/v1/`
- [ ] Create superuser account
- [ ] Test login functionality
- [ ] Monitor logs for errors

---

## 🔐 Security Reminders

- ✅ Never commit `.env` file
- ✅ Use strong SECRET_KEY in production
- ✅ Set DEBUG=False in production
- ✅ Use HTTPS (Railway/Render provide this)
- ✅ Regularly update dependencies
- ✅ Monitor database backups

---

## 📞 Support

If deployment issues:
1. Check Railway/Render logs
2. Verify environment variables
3. Check GitHub repository settings
4. Review Django error messages

**Happy Deploying! 🚀**
