# 🚀 Complete Guide: Upload Arctic DB Project to GitHub

## Prerequisites

Before starting, you'll need:
- ✅ Git installed on your machine
- ✅ GitHub account
- ✅ GitHub credentials (Personal Access Token or SSH key)

---

## Method 1: Using HTTPS with Personal Access Token (Easiest for Beginners)

### Step 1: Create Personal Access Token on GitHub

1. Go to [GitHub Settings](https://github.com/settings/tokens)
2. Click **"Generate new token"** → **"Generate new token (classic)"**
3. Fill in the form:
   - **Note**: `Arctic DB Project Token`
   - **Expiration**: Select preferred duration (90 days recommended)
   - **Select scopes**: Check:
     - ☑️ `repo` (Full control of private repositories)
     - ☑️ `workflow` (Update GitHub Actions)
4. Click **"Generate token"**
5. **Copy and save the token** (you won't see it again!)

### Step 2: Create Repository on GitHub

1. Go to [GitHub New Repository](https://github.com/new)
2. Fill in:
   - **Repository name**: `arcticdb-project` (or your preferred name)
   - **Description**: `Arctic DB Docker with S3 integration, REST API, and Python client`
   - **Visibility**: Choose `Public` or `Private`
   - **Initialize with**: Leave unchecked (we already have files)
3. Click **"Create repository"**
4. Copy the repository URL (e.g., `https://github.com/username/arcticdb-project.git`)

### Step 3: Add Remote and Push to GitHub

Navigate to your project directory:

```bash
cd arcticdb-project
```

Add the GitHub repository as remote:

```bash
git remote add origin https://github.com/YOUR_USERNAME/arcticdb-project.git
```

Verify the remote was added:

```bash
git remote -v
```

You should see:
```
origin  https://github.com/YOUR_USERNAME/arcticdb-project.git (fetch)
origin  https://github.com/YOUR_USERNAME/arcticdb-project.git (push)
```

Rename branch to `main` (recommended):

```bash
git branch -M main
```

Push to GitHub:

```bash
git push -u origin main
```

When prompted for authentication:
- **Username**: Your GitHub username
- **Password**: Paste your Personal Access Token

✅ **Done!** Your code is now on GitHub.

---

## Method 2: Using SSH (More Secure)

### Step 1: Generate SSH Key

If you don't have an SSH key, generate one:

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

Press Enter when asked for passphrase (or enter one for security):

```
Generating public/private ed25519 key pair.
Enter file in which to save the key (/home/user/.ssh/id_ed25519): [Press Enter]
Enter passphrase (empty for no passphrase): [Press Enter or enter passphrase]
```

View your public key:

```bash
cat ~/.ssh/id_ed25519.pub
```

Copy the entire output (starts with `ssh-ed25519`).

### Step 2: Add SSH Key to GitHub

1. Go to [GitHub SSH Keys Settings](https://github.com/settings/keys)
2. Click **"New SSH key"**
3. Fill in:
   - **Title**: `My Laptop` (or your device name)
   - **Key type**: `Authentication Key`
   - **Key**: Paste your public key
4. Click **"Add SSH key"**

Test SSH connection:

```bash
ssh -T git@github.com
```

You should see:
```
Hi YOUR_USERNAME! You've successfully authenticated...
```

### Step 3: Create Repository on GitHub

Same as Method 1 Step 2.

### Step 4: Add Remote and Push

Navigate to project:

```bash
cd arcticdb-project
```

Add SSH remote:

```bash
git remote add origin git@github.com:YOUR_USERNAME/arcticdb-project.git
```

Rename branch:

```bash
git branch -M main
```

Push to GitHub:

```bash
git push -u origin main
```

✅ **Done!** No password needed for future pushes.

---

## Method 3: GitHub CLI (Fastest Method)

### Step 1: Install GitHub CLI

**macOS (Homebrew):**
```bash
brew install gh
```

**Windows (Chocolatey):**
```bash
choco install gh
```

**Linux:**
```bash
sudo apt-get install gh
```

Or download from: https://github.com/cli/cli

### Step 2: Authenticate

```bash
gh auth login
```

Follow the prompts:
- **What is your preferred protocol?** → `HTTPS` (or `SSH`)
- **Authenticate with your GitHub credentials?** → `Y`
- **How would you like to authenticate GitHub CLI?** → Choose option (e.g., Login with web browser)

### Step 3: Create and Push Repository

Navigate to project:

```bash
cd arcticdb-project
```

Create repository on GitHub and push:

```bash
gh repo create arcticdb-project --source=. --remote=origin --push
```

Choose options:
- **Repository owner**: Your username
- **Repository visibility**: `Public` or `Private`

✅ **Done!** Repository created and files pushed in one command.

---

## Verify Files on GitHub

### Check what was pushed:

```bash
git log --oneline
```

You should see your commits.

### View on GitHub:

Go to `https://github.com/YOUR_USERNAME/arcticdb-project`

You should see all your files:
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
✅ .gitignore
✅ .env.example
✅ setup.sh
```

---

## Common Commands

### Check Git Status

```bash
git status
```

### View Remote

```bash
git remote -v
```

### Change Remote URL

If you made a mistake:

```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/arcticdb-project.git
git push -u origin main
```

### Update After Making Changes

After editing files locally:

```bash
git add .
git commit -m "Description of changes"
git push
```

### Clone Repository on Another Computer

```bash
git clone https://github.com/YOUR_USERNAME/arcticdb-project.git
cd arcticdb-project
```

---

## Troubleshooting

### Error: "remote origin already exists"

```bash
git remote remove origin
git remote add origin <your-url>
```

### Error: "fatal: could not read Username"

Using HTTPS? Make sure you're using Personal Access Token, not password.

```bash
# Verify stored credentials
git config --global credential.helper

# Clear saved credentials (macOS)
security-find-generic-password -l git.github.com -w | security delete-generic-password -l git.github.com

# Clear saved credentials (Windows)
cmdkey /delete:git:https://github.com

# Clear saved credentials (Linux)
rm ~/.git-credentials
```

### Error: "Permission denied (publickey)"

Using SSH? Make sure your public key is added to GitHub:

```bash
# Check SSH connection
ssh -vT git@github.com

# Test SSH key
ssh-keyscan github.com >> ~/.ssh/known_hosts
```

### Error: "src refspec main does not match any"

Your branch is named `master`, not `main`. Push as:

```bash
git push -u origin master
```

Or rename:

```bash
git branch -M main
git push -u origin main
```

---

## Next Steps After Pushing

### 1. Clone on Another Machine

```bash
git clone https://github.com/YOUR_USERNAME/arcticdb-project.git
cd arcticdb-project
docker-compose up -d
```

### 2. Set Up Collaborators

On GitHub repository page:
- Settings → Collaborators
- Click "Add people"
- Search for GitHub usernames

### 3. Create Issues

For tracking tasks:
- Click "Issues" tab
- Click "New issue"
- Add title and description

### 4. Create Pull Requests

For code review:
- Create new branch: `git checkout -b feature/my-feature`
- Make changes and push
- On GitHub, click "New Pull Request"

### 5. Enable GitHub Actions

For CI/CD (optional):
- Go to "Actions" tab
- Choose a workflow template
- Configure and commit

### 6. Set Up GitHub Pages (Optional)

Host documentation:
- Settings → Pages
- Select branch (main)
- Choose theme

---

## Summary Command Sequence

### Quick Setup (HTTPS)

```bash
# Navigate to project
cd arcticdb-project

# Create GitHub repo first at github.com/new

# Add remote
git remote add origin https://github.com/YOUR_USERNAME/arcticdb-project.git

# Rename to main
git branch -M main

# Push
git push -u origin main
```

### Quick Setup (SSH)

```bash
cd arcticdb-project
git remote add origin git@github.com:YOUR_USERNAME/arcticdb-project.git
git branch -M main
git push -u origin main
```

### Quick Setup (GitHub CLI)

```bash
cd arcticdb-project
gh repo create arcticdb-project --source=. --remote=origin --push
```

---

## GitHub Best Practices

✅ **DO:**
- Keep `.env` files out of version control (already in .gitignore)
- Write clear commit messages
- Use branches for features
- Update README with usage instructions
- Add LICENSE file
- Document configuration

❌ **DON'T:**
- Commit secrets or credentials
- Push large binary files
- Force push to main branch
- Ignore security warnings
- Leave stale branches

---

## Optional: Add More Files

### Add License

```bash
# MIT License
curl https://opensource.org/licenses/MIT -o LICENSE
git add LICENSE
git commit -m "Add MIT license"
git push
```

### Add GitHub Issue Templates

Create `.github/ISSUE_TEMPLATE/bug_report.md`:

```markdown
---
name: Bug report
about: Create a report to help us improve
---

## Describe the bug
A clear description of the bug.

## To Reproduce
Steps to reproduce the behavior.

## Expected behavior
What you expected to happen.

## Screenshots
If applicable, add screenshots.

## Environment
- OS: [e.g. Ubuntu 20.04]
- Python: [e.g. 3.11]
- Docker: [e.g. 24.0]
```

Push:

```bash
git add .github/
git commit -m "Add issue templates"
git push
```

### Add GitHub Actions Workflow

Create `.github/workflows/docker-build.yml`:

```yaml
name: Build Docker Image

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Build Docker image
        run: docker build -t arcticdb:latest .
      - name: Test image
        run: docker run --rm arcticdb:latest python -m pytest
```

Push:

```bash
git add .github/
git commit -m "Add GitHub Actions CI/CD"
git push
```

---

## View Your GitHub Repository

After pushing, visit:

```
https://github.com/YOUR_USERNAME/arcticdb-project
```

You'll see:
- All your files
- Commit history
- Branch information
- Recent activity

---

## Share Repository

To share with others, send them:

```
https://github.com/YOUR_USERNAME/arcticdb-project
```

They can clone with:

```bash
git clone https://github.com/YOUR_USERNAME/arcticdb-project.git
```

---

## 🎉 You're Done!

Your Arctic DB project is now on GitHub! 

**Next steps:**
1. Share the repository URL
2. Invite collaborators
3. Create issues for tasks
4. Start developing with version control!

---

**Questions? Check GitHub Help:** https://docs.github.com
