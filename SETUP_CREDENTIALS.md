# 🔑 Setting Up Credentials

This project requires Google Cloud Vision API credentials for image detection features.

## Required Files (Not in GitHub)

These files are excluded from version control for security:
- `google-vision-credentials.json` - Google Cloud Vision API credentials

## Setup Instructions

### 1. Google Cloud Vision API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing project
3. Enable the **Cloud Vision API**
4. Go to **APIs & Services** → **Credentials**
5. Click **Create Credentials** → **Service Account**
6. Create a service account with **Cloud Vision API User** role
7. Click on the service account → **Keys** → **Add Key** → **JSON**
8. Download the JSON file
9. Rename it to `google-vision-credentials.json`
10. Place it in the project root directory

### 2. Environment Variables

Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

Update the values in `.env` as needed.

### 3. Verify Setup

Run the health check:
```bash
curl http://localhost:8000/health
```

You should see `"ok": true` in the response.

## ⚠️ Security Notes

- **NEVER** commit `google-vision-credentials.json` to GitHub
- **NEVER** share your credentials publicly
- Add credentials to `.gitignore` (already done)
- Use environment variables for sensitive data
- Rotate credentials if accidentally exposed
