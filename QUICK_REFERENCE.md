# Quick Reference Card - CI/CD Pipeline Demo

## 🚀 Quick Start

### Local Setup
```bash
# Clone repository
git clone https://github.com/datatweets/cicd-pipeline-demo.git
cd cicd-pipeline-demo

# Install dependencies
pip3 install -r requirements.txt

# Run tests
pytest test_app.py -v

# Start app
python3 app.py
```

### Test Endpoints
```bash
curl http://localhost:8008/hello/World
curl http://localhost:8008/health
```

---

## 📝 File Structure

```
cicd-pipeline-demo/
├── .github/workflows/
│   └── ci-cd.yml           # GitHub Actions pipeline
├── app.py                  # Flask application
├── test_app.py            # Test suite
├── requirements.txt        # Python dependencies
├── README.md              # Project overview
├── TUTORIAL.md            # Complete tutorial
└── QUICK_REFERENCE.md     # This file
```

---

## 🔧 Common Commands

### Testing
```bash
# Run all tests
pytest test_app.py -v

# Run specific test
pytest test_app.py::test_hello_endpoint -v

# Run with coverage
pytest test_app.py --cov=app --cov-report=html

# Verbose output
pytest test_app.py -vv
```

### Git Workflow
```bash
# Check status
git status

# Create feature branch
git checkout -b feature/my-feature

# Stage changes
git add .

# Commit with message
git commit -m "feat: Add new feature"

# Push to GitHub
git push origin feature/my-feature

# Push to main (triggers CI/CD)
git push origin main
```

### Flask App
```bash
# Start development server
python3 app.py

# Run on different port
# Edit app.py: app.run(host='0.0.0.0', port=8009)

# Stop server
# Press Ctrl+C

# Kill process on port
lsof -ti:8008 | xargs kill -9
```

---

## 📋 API Endpoints

### GET /hello/<name>
Returns personalized greeting
```bash
curl http://localhost:8008/hello/Alice
# Response: {"message":"Hello, Alice!"}
```

### GET /health
Health check endpoint
```bash
curl http://localhost:8008/health
# Response: {"status":"healthy"}
```

---

## 🔄 CI/CD Pipeline Flow

```
Push to GitHub
    ↓
GitHub Actions Triggered
    ↓
[Test Job]
├─ Checkout code
├─ Setup Python 3.9
├─ Install dependencies
└─ Run tests
    ↓
Tests Pass? ─── No ──→ ❌ Pipeline fails
    ↓
   Yes
    ↓
On main branch?
    ↓
   Yes
    ↓
[Deploy Job]
└─ Deploy to staging
    ↓
✅ Complete!
```

---

## 📊 GitHub Actions

### View Pipeline
1. Go to https://github.com/datatweets/cicd-pipeline-demo
2. Click **Actions** tab
3. See workflow runs

### Status Indicators
- 🟡 Yellow dot = Running
- ✅ Green checkmark = Success
- ❌ Red X = Failed

### Triggers
- Push to `main` branch
- Pull request to `main` branch

---

## 🐛 Troubleshooting

### Tests Fail
```bash
# Check error messages
pytest test_app.py -vv

# Verify dependencies
pip3 list | grep -E "flask|pytest"

# Reinstall dependencies
pip3 install -r requirements.txt
```

### Port in Use
```bash
# Find process using port 8008
lsof -ti:8008

# Kill the process
kill -9 $(lsof -ti:8008)
```

### Import Error
```bash
# Activate virtual environment (if using)
source .venv/bin/activate

# Verify Python path
which python3

# Check installed packages
pip3 list
```

### Pipeline Not Running
- Check `.github/workflows/ci-cd.yml` exists
- Verify YAML syntax (no tabs, proper indentation)
- Check branch name: `git branch`
- Verify GitHub Actions is enabled in Settings

---

## 📚 Adding New Features

### 1. Create New Endpoint
```python
# In app.py
@app.route('/goodbye/<name>')
def goodbye(name):
    return jsonify({'message': f'Goodbye, {name}!'})
```

### 2. Add Test
```python
# In test_app.py
def test_goodbye_endpoint(client):
    response = client.get('/goodbye/World')
    assert response.status_code == 200
    assert response.json['message'] == 'Goodbye, World!'
```

### 3. Test Locally
```bash
pytest test_app.py -v
```

### 4. Commit and Push
```bash
git add app.py test_app.py
git commit -m "feat: Add goodbye endpoint"
git push origin main
```

### 5. Watch Pipeline
Go to Actions tab and see it run automatically!

---

## 🔒 Security Checklist

- [ ] Never commit passwords or API keys
- [ ] Use GitHub Secrets for sensitive data
- [ ] Use `.gitignore` for local config files
- [ ] Review dependencies for vulnerabilities
- [ ] Use environment variables for config
- [ ] Enable branch protection rules
- [ ] Require code reviews for merges

---

## 🎯 Best Practices

### Commit Messages
```bash
# Good
git commit -m "feat: Add user authentication"
git commit -m "fix: Resolve health check timeout"
git commit -m "test: Add integration tests"

# Bad
git commit -m "changes"
git commit -m "fixed stuff"
git commit -m "WIP"
```

### Testing
- ✅ Write tests for new features
- ✅ Test both success and error cases
- ✅ Keep tests fast (< 1 second each)
- ✅ Use descriptive test names
- ✅ Test edge cases

### Code Quality
- ✅ Follow PEP 8 style guide
- ✅ Add docstrings to functions
- ✅ Use meaningful variable names
- ✅ Keep functions small and focused
- ✅ Remove commented-out code

---

## 📖 Additional Resources

### Documentation
- [Full Tutorial](TUTORIAL.md) - Complete step-by-step guide
- [README](README.md) - Project overview
- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [Flask Docs](https://flask.palletsprojects.com/)
- [pytest Docs](https://docs.pytest.org/)

### Quick Links
- Repository: https://github.com/datatweets/cicd-pipeline-demo
- Actions: https://github.com/datatweets/cicd-pipeline-demo/actions
- Issues: https://github.com/datatweets/cicd-pipeline-demo/issues

---

## 💡 Pro Tips

1. **Test locally before pushing** - Catches issues faster
2. **Use descriptive commit messages** - Helps team understand changes
3. **Keep PRs small** - Easier to review and merge
4. **Monitor pipeline health** - Fix failures quickly
5. **Document your changes** - Future you will thank you
6. **Use branch protection** - Prevents direct pushes to main
7. **Review pipeline logs** - Learn from failures
8. **Keep dependencies updated** - Security and features

---

## ⚡ Next Steps

1. ✅ Set up project locally
2. ✅ Run tests successfully
3. ✅ Make a code change
4. ✅ Watch CI/CD pipeline run
5. 📖 Read the full [TUTORIAL.md](TUTORIAL.md)
6. 🚀 Add your own features
7. 🔧 Customize the pipeline
8. 📦 Deploy to production

---

**Need help?** Check the [TUTORIAL.md](TUTORIAL.md) for detailed explanations!
