# GitHub/Bitbucket Deployment Guide for Legislative Calendars

## Why This Is Better Than WordPress

✅ **Version control** - Track changes over time
✅ **Easy updates** - Just commit new files, URLs stay the same
✅ **No WordPress uploads** - Skip the admin panel
✅ **Professional** - Keep it with your other code/docs
✅ **Free hosting** - GitHub/Bitbucket serve files publicly for free

## Setup Instructions

### Step 1: Create a Repository

**Option A: GitHub (Recommended)**
1. Go to https://github.com/new
2. Name it: `legislative-calendars` (or whatever you prefer)
3. Make it **Public** (required for calendar subscriptions to work)
4. Add a README: Yes
5. Click "Create repository"

**Option B: Bitbucket**
1. Go to https://bitbucket.org/repo/create
2. Name it: `legislative-calendars`
3. Make it **Public**
4. Click "Create repository"

### Step 2: Upload Your ICS Files

**From Terminal/Command Line:**

```bash
# Navigate to where you generated the calendars
cd /path/to/legislative_calendar_project

# Initialize git (if not already)
git init

# Add GitHub/Bitbucket as remote
# For GitHub:
git remote add origin https://github.com/YOUR-USERNAME/legislative-calendars.git

# For Bitbucket:
git remote add origin https://bitbucket.org/YOUR-USERNAME/legislative-calendars.git

# Add the output files
git add output/*.ics

# Commit
git commit -m "Add 2026 legislative calendars"

# Push
git push -u origin main
```

**Or via Web Interface:**
1. In your repo, click "Add file" → "Upload files"
2. Drag all the `.ics` files from your `output/` folder
3. Commit directly to main branch

### Step 3: Get the Public URLs

Your ICS files will be accessible at these URLs:

**GitHub:**
```
https://raw.githubusercontent.com/YOUR-USERNAME/legislative-calendars/main/output/federal_legislative_calendar_2026.ics
```

**Bitbucket:**
```
https://bitbucket.org/YOUR-USERNAME/legislative-calendars/raw/main/output/federal_legislative_calendar_2026.ics
```

### Step 4: Test the URLs

1. Copy one of your URLs
2. Open it in a browser
3. It should either download or display the ICS file
4. If you see the raw ICS content, it's working!

### Step 5: Share with Your Team

Send this email:

**Subject:** Legislative Session Calendars - 2026

**Body:**
```
Hi team,

I've set up automatically-updating legislative calendars for 2026. 
Subscribe in Google Calendar to track when legislatures are in session.

Available Calendars:
• Federal (House + Senate): [paste URL]
• All States Combined: [paste URL]
• Individual states: [link to repo]

How to Subscribe:
1. Copy the calendar URL above
2. In Google Calendar, click + next to "Other calendars"
3. Select "From URL"
4. Paste the URL
5. Click "Add calendar"

View all available calendars:
https://github.com/YOUR-USERNAME/legislative-calendars

Questions? Reply to this email.
```

## Updating the Calendars

When session dates change or for 2027:

```bash
# Update the dates in generate_2026_calendars.py
# Re-run the script
python3 generate_2026_calendars.py

# Commit and push the new files
cd /path/to/legislative_calendar_project
git add output/*.ics
git commit -m "Update 2026 session dates"
git push
```

**Important:** Keep the same filenames! The URLs will stay the same, and Google Calendar will automatically detect the changes within 24 hours.

## Pro Tips

### 1. Create a README in Your Repo

Create a file called `README.md` in your repo:

```markdown
# Beekeeper Group Legislative Calendars

Automatically-updated ICS calendar files for federal and state legislative sessions.

## Available Calendars

Subscribe to these in Google Calendar:

- **Federal Legislative Calendar**: [Copy this URL](https://raw.githubusercontent.com/YOUR-USERNAME/legislative-calendars/main/output/federal_legislative_calendar_2026.ics)
- **California**: [Copy this URL](https://raw.githubusercontent.com/YOUR-USERNAME/legislative-calendars/main/output/california_legislative_calendar_2026.ics)
- **Indiana**: [Copy this URL](https://raw.githubusercontent.com/YOUR-USERNAME/legislative-calendars/main/output/indiana_legislative_calendar_2026.ics)
- [etc...]

## How to Subscribe

1. Copy the URL above
2. In Google Calendar: Click + next to "Other calendars"
3. Select "From URL"
4. Paste the URL and click "Add calendar"

## Updates

These calendars are updated as session dates change. Your subscribed calendar will automatically refresh within 24 hours.

Last updated: January 6, 2026
```

### 2. Use GitHub Pages (Optional)

You can create a nice webpage for your calendars:

1. In your repo settings, enable GitHub Pages
2. Create an `index.html` with styled links to your calendars
3. Share the page URL: `https://YOUR-USERNAME.github.io/legislative-calendars`

### 3. Set Up Automation (Advanced)

Create a GitHub Action to automatically regenerate calendars:

```yaml
# .github/workflows/update-calendars.yml
name: Update Legislative Calendars
on:
  schedule:
    - cron: '0 9 * * 1'  # Every Monday at 9am
  workflow_dispatch:  # Manual trigger

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: python3 generate_2026_calendars.py
      - run: |
          git config user.name github-actions
          git config user.email github-actions@github.com
          git add output/*.ics
          git commit -m "Auto-update calendars" || exit 0
          git push
```

## Quick Reference

| Action | Command |
|--------|---------|
| Generate calendars | `python3 generate_2026_calendars.py` |
| Update repo | `git add output/*.ics && git commit -m "Update" && git push` |
| View your calendars | `https://github.com/YOUR-USERNAME/legislative-calendars` |

## Questions?

Contact Landin for help with setup or Git questions.

---

**Last Updated**: January 6, 2026
**Repository**: https://github.com/YOUR-USERNAME/legislative-calendars
