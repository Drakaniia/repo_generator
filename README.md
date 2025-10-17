# 🤖 Self-Updating GitHub Repository

An automated bot that commits fresh content every hour using GitHub Actions - **runs permanently and completely free!**

## ✨ Features

- 🎨 Random ASCII art every hour
- 😄 Fresh programming jokes from APIs
- 💭 Inspirational tech quotes
- 🧠 Random interesting facts
- 🎯 Activity suggestions
- 📊 Fun fake statistics
- 📝 Entertaining changelog entries

## 🚀 Quick Setup (5 minutes)

### Step 1: Create Repository

1. Create a new GitHub repository (public or private)
2. Clone it to your local machine

### Step 2: Add Files

Create the following file structure:

```
your-repo/
├── .github/
│   └── workflows/
│       └── hourly-update.yml
├── auto_update.py
└── README.md
```

**Copy the contents from the artifacts provided:**
- `hourly-update.yml` → GitHub Actions workflow
- `auto_update.py` → Python script

### Step 3: Enable GitHub Actions

1. Go to your repository on GitHub
2. Click **Settings** → **Actions** → **General**
3. Under "Workflow permissions":
   - Select **"Read and write permissions"**
   - Check **"Allow GitHub Actions to create and approve pull requests"**
4. Click **Save**

### Step 4: Push and Activate

```bash
git add .
git commit -m "🚀 Initial setup for auto-update bot"
git push origin main
```

### Step 5: Verify It's Running

1. Go to the **Actions** tab in your repository
2. You should see the "Hourly Auto-Update" workflow
3. Click **"Run workflow"** to trigger it manually first
4. Check that `AUTO_UPDATE.md` was created

## ⚙️ How It Works

### Automatic Running
- GitHub Actions runs the workflow **every hour** automatically
- The cron schedule `0 * * * *` means "at minute 0 of every hour"
- Also triggers on pushes to keep the workflow active

### What Gets Updated
Each hour, the bot:
1. Fetches fresh jokes from joke APIs
2. Gets inspirational quotes
3. Retrieves random facts
4. Generates ASCII art
5. Creates fake statistics
6. Commits everything to `AUTO_UPDATE.md`

## 🎮 Manual Trigger

You can run it manually anytime:
1. Go to **Actions** tab
2. Select **"Hourly Auto-Update"**
3. Click **"Run workflow"**
4. Select branch (usually `main`)
5. Click green **"Run workflow"** button

## 🔧 Customization

### Change Frequency

Edit `.github/workflows/hourly-update.yml`:

```yaml
schedule:
  - cron: '0 * * * *'  # Every hour
  # - cron: '*/30 * * * *'  # Every 30 minutes
  # - cron: '0 */2 * * *'  # Every 2 hours
  # - cron: '0 0 * * *'  # Once per day at midnight
```

### Add More APIs

Edit `auto_update.py` and add more API calls in the `generate_content()` function.

Popular free APIs:
- https://api.adviceslip.com/advice - Random advice
- https://api.chucknorris.io/jokes/random - Chuck Norris jokes
- https://api.kanye.rest/ - Kanye quotes
- https://api.thecatapi.com/v1/images/search - Cat pictures

## 📊 Monitoring

### Check if it's running:
- **Actions tab** → See workflow runs
- **Commits** → Should have hourly commits
- **AUTO_UPDATE.md** → Should update every hour

### Troubleshooting

**Workflow not running?**
- Check if Actions are enabled in Settings
- Verify workflow permissions are set correctly
- GitHub may disable workflows after 60 days of repo inactivity

**To keep it active permanently:**
- Make at least one commit every 60 days
- Or manually trigger the workflow every 60 days
- Each automated commit counts as activity, so it keeps itself alive!

## 🎯 Why This Works Permanently

1. **GitHub Actions is free** for public repos (2,000 minutes/month for private)
2. **Self-sustaining**: Each commit counts as repo activity
3. **No server needed**: GitHub's infrastructure runs everything
4. **Zero maintenance**: Set it and forget it

## 📝 Notes

- The bot commits as `github-actions[bot]`
- All content is fetched fresh from APIs
- Runs 24/7 without any cost
- Great for keeping your GitHub activity graph green! 📈

## 🎉 That's It!

Your repository will now update automatically every hour, forever! 🚀

---

*Generated with ❤️ for automation enthusiasts*