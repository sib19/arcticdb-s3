# 📋 GitHub Upload - Quick Reference Card

## 🟢 3-MINUTE QUICK SETUP

### Step 1: Create Repo on GitHub
Visit: https://github.com/new
- Repo name: `arcticdb-project`
- Visibility: Public or Private
- Click "Create repository"
- Copy the repo URL

### Step 2: Push Your Code (Pick One Method)

#### Option A: HTTPS (Easiest)
```bash
cd arcticdb-project

git remote add origin https://github.com/YOUR_USERNAME/arcticdb-project.git
git branch -M main
git push -u origin main
```

#### Option B: SSH (More Secure)
```bash
cd arcticdb-project

git remote add origin git@github.com:YOUR_USERNAME/arcticdb-project.git
git branch -M main
git push -u origin main
```

#### Option C: GitHub CLI (Fastest)
```bash
cd arcticdb-project
gh repo create arcticdb-project --source=. --remote=origin --push
```

### Step 3: Verify
- Visit: `https://github.com/YOUR_USERNAME/arcticdb-project`
- See all your files there ✅

---

## 🔧 COMMON COMMANDS

### Setup
```bash
# Create SSH key (one time)
ssh-keygen -t ed25519 -C "your@email.com"

# Add SSH key to GitHub
cat ~/.ssh/id_ed25519.pub
# Copy and paste at github.com/settings/keys

# Create Personal Access Token (for HTTPS)
# Visit: github.com/settings/tokens
# Select scopes: repo, workflow
```

### First Time Push
```bash
# Navigate to project
cd arcticdb-project

# View current remote (if any)
git remote -v

# Add GitHub as remote (pick one)
git remote add origin https://github.com/USER/repo.git    # HTTPS
git remote add origin git@github.com:USER/repo.git        # SSH

# Rename branch to main
git branch -M main

# Push everything
git push -u origin main
```

### After Making Changes
```bash
# Check what changed
git status

# Stage all changes
git add .

# Commit with message
git commit -m "Description of changes"

# Push to GitHub
git push
```

### Fix Remote Issues
```bash
# View current remotes
git remote -v

# Remove wrong remote
git remote remove origin

# Add correct remote
git remote add origin <correct-url>

# Push
git push -u origin main
```

---

## 🚨 TROUBLESHOOTING

| Problem | Solution |
|---------|----------|
| "remote origin already exists" | `git remote remove origin` then `git remote add origin ...` |
| "fatal: could not read Username" | Using HTTPS? Use Personal Access Token, not password |
| "Permission denied (publickey)" | Using SSH? Add public key to GitHub settings |
| "src refspec main does not match any" | Rename: `git branch -M main` before push |
| "Everything up-to-date" | No changes to push. Make edits and commit first |

---

## 📝 EXAMPLE WORKFLOW

### Step 1: Create Local Project
```bash
cd /path/to/arcticdb-project
git status  # Should show existing commits
```

### Step 2: Create GitHub Repository
Visit: `https://github.com/new`
- Fill in name: `arcticdb-project`
- Click "Create repository"
- Copy the URL shown

### Step 3: Connect to GitHub
```bash
git remote add origin https://github.com/YOUR_USERNAME/arcticdb-project.git
git branch -M main
git push -u origin main
```

### Step 4: Verify on GitHub
Visit: `https://github.com/YOUR_USERNAME/arcticdb-project`
- See all files ✅
- See commit history ✅

### Step 5: Later Edits
```bash
# Make changes to files
nano app.py

# Stage and commit
git add .
git commit -m "Fixed bug in API"

# Push to GitHub
git push
```

---

## 🎯 VERIFY CHECKLIST

After pushing, verify on GitHub:

- ✅ All files visible on repository page
- ✅ Commit history shows your commits
- ✅ `.env` file NOT visible (should be in .gitignore)
- ✅ README.md displays as description
- ✅ Branches show "main" as default

---

## 🔐 SECURITY NOTES

### For HTTPS Login
1. Create Personal Access Token: `github.com/settings/tokens`
2. Select scopes: `repo`, `workflow`
3. Use token as password (not your GitHub password)
4. Token won't be stored on disk (Mac/Linux)

### For SSH (More Secure)
1. Create SSH key: `ssh-keygen -t ed25519 -C "your@email.com"`
2. Add public key: `github.com/settings/keys`
3. Never need password again for this repo

### Protect Your Credentials
- ✅ `.env` is in `.gitignore` (won't be pushed)
- ✅ Personal Access Token won't be stored
- ✅ SSH key stays on your computer
- ✅ Repository is ready for GitHub safely

---

## 📱 CLONE ON ANOTHER COMPUTER

After uploading, clone on another machine:

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/arcticdb-project.git

# Navigate into it
cd arcticdb-project

# Start working
docker-compose up -d
```

---

## 🤝 SHARE WITH OTHERS

Share repository URL:
```
https://github.com/YOUR_USERNAME/arcticdb-project
```

Others can:
- Star the repository (⭐)
- Clone and use it
- Create issues
- Submit pull requests (if enabled)

---

## 📊 WHAT GETS UPLOADED

### Will be uploaded ✅
```
✅ app.py
✅ arctic_client.py
✅ examples.py
✅ Dockerfile
✅ docker-compose.yml
✅ requirements.txt
✅ Makefile
✅ README.md
✅ API.md
✅ setup.sh
✅ .gitignore
✅ .env.example
✅ .git/ (commit history)
```

### Will NOT be uploaded ❌
```
❌ .env (credentials - in .gitignore)
❌ data/ (local data)
❌ logs/ (local logs)
❌ __pycache__/ (Python cache)
❌ .venv/ (virtual env)
```

---

## 🎯 FASTEST METHOD SUMMARY

```bash
# 1. Create repo on GitHub (github.com/new)

# 2. Navigate to local project
cd arcticdb-project

# 3. Connect to GitHub
git remote add origin https://github.com/YOUR_USERNAME/arcticdb-project.git

# 4. Set main branch
git branch -M main

# 5. Push everything
git push -u origin main

# 6. Done! Visit GitHub to verify
```

---

**Total time: 3 minutes** ⏱️

Still have questions? See: `GITHUB_UPLOAD_GUIDE.md` for detailed instructions
