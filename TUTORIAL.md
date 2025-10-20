# Complete CI/CD Pipeline Tutorial: From Zero to Automated Deployment

## Table of Contents
1. [Introduction](#introduction)
2. [What is CI/CD?](#what-is-cicd)
3. [Understanding the Application](#understanding-the-application)
4. [The Testing Strategy](#the-testing-strategy)
5. [GitHub Actions CI/CD Pipeline](#github-actions-cicd-pipeline)
6. [Step-by-Step Guide](#step-by-step-guide)
7. [What Happens When You Push Code](#what-happens-when-you-push-code)
8. [Troubleshooting](#troubleshooting)
9. [Best Practices](#best-practices)
10. [Next Steps](#next-steps)

---

## Introduction

This tutorial demonstrates a complete CI/CD (Continuous Integration/Continuous Deployment) pipeline using:
- **Python Flask** - A lightweight web framework
- **pytest** - Testing framework for Python
- **GitHub Actions** - CI/CD automation platform

By the end of this tutorial, you'll understand how automated testing and deployment works in modern software development.

---

## What is CI/CD?

### Continuous Integration (CI)
The practice of automatically testing code changes whenever they're pushed to the repository.

**Benefits:**
- Catch bugs early
- Ensure code quality
- Reduce integration problems
- Fast feedback for developers

### Continuous Deployment (CD)
The practice of automatically deploying code to staging/production after it passes all tests.

**Benefits:**
- Faster releases
- Reduced manual errors
- Consistent deployment process
- Quick rollbacks if needed

### The CI/CD Workflow

```
Developer writes code
         ↓
    Commits changes
         ↓
  Pushes to GitHub
         ↓
GitHub Actions triggered
         ↓
    Code checked out
         ↓
 Dependencies installed
         ↓
    Tests executed
         ↓
  ✅ Tests pass? ────No──→ ❌ Notify developer (stop here)
         ↓
        Yes
         ↓
   On main branch?
         ↓
        Yes
         ↓
  Deploy to staging
         ↓
✅ Deployment complete
```

---

## Understanding the Application

### Application Architecture

Our Flask application (`app.py`) is a simple REST API with three main components:

#### 1. **The Flask App Instance**
```python
from flask import Flask, jsonify

app = Flask(__name__)
```
- Creates a Flask web application
- `Flask(__name__)` initializes the app with the module name

#### 2. **Hello Endpoint** (`/hello/<name>`)
```python
@app.route('/hello/<name>')
def hello(name):
    """Return a personalized greeting."""
    return jsonify({'message': f'Hello, {name}!'})
```

**How it works:**
- URL pattern: `/hello/<name>` where `<name>` is a variable
- Example: `GET /hello/World`
- Response: `{"message": "Hello, World!"}`
- Uses `jsonify()` to return JSON format

**Testing it:**
```bash
curl http://localhost:8008/hello/Alice
# Returns: {"message":"Hello, Alice!"}
```

#### 3. **Health Check Endpoint** (`/health`)
```python
@app.route('/health')
def health():
    """Health check endpoint for monitoring."""
    return jsonify({'status': 'healthy'})
```

**How it works:**
- Simple endpoint that returns service status
- Used by monitoring tools to check if app is running
- Example: `GET /health`
- Response: `{"status": "healthy"}`

**Testing it:**
```bash
curl http://localhost:8008/health
# Returns: {"status":"healthy"}
```

#### 4. **Application Server**
```python
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8008)
```

**Configuration:**
- `host='0.0.0.0'` - Listen on all network interfaces (accessible from any IP)
- `port=8008` - Run on port 8008
- **Note:** In production, use a proper WSGI server like Gunicorn, not Flask's built-in server

### Why These Endpoints?

1. **`/hello/<name>`** - Demonstrates:
   - URL parameters
   - Dynamic responses
   - JSON API design

2. **`/health`** - Demonstrates:
   - Monitoring best practices
   - Service health checks
   - Load balancer integration points

---

## The Testing Strategy

### Test File Structure (`test_app.py`)

#### 1. **Imports**
```python
import pytest
from app import app
```
- `pytest` - Testing framework
- `from app import app` - Import our Flask application

#### 2. **Test Fixture**
```python
@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
```

**What is a fixture?**
- Reusable setup code for tests
- Runs before each test function
- Provides a test client to make requests

**How it works:**
1. `app.config['TESTING'] = True` - Enables testing mode
2. `app.test_client()` - Creates a fake client for testing
3. `yield client` - Provides client to test functions
4. Automatically cleans up after each test

#### 3. **Test: Hello Endpoint**
```python
def test_hello_endpoint(client):
    """Test the hello endpoint returns correct greeting."""
    response = client.get('/hello/World')
    assert response.status_code == 200
    assert response.json['message'] == 'Hello, World!'
```

**Step by step:**
1. `client.get('/hello/World')` - Makes GET request to endpoint
2. `assert response.status_code == 200` - Checks for success status
3. `assert response.json['message'] == 'Hello, World!'` - Validates response content

**What's being tested:**
- ✅ Endpoint is accessible
- ✅ Returns HTTP 200 (OK)
- ✅ Response format is correct JSON
- ✅ Message content is accurate

#### 4. **Test: Health Endpoint**
```python
def test_health_endpoint(client):
    """Test the health check endpoint."""
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json['status'] == 'healthy'
```

**What's being tested:**
- ✅ Health check is accessible
- ✅ Returns HTTP 200 (OK)
- ✅ Status is 'healthy'

### Running Tests Locally

```bash
# Install dependencies
pip3 install -r requirements.txt

# Run all tests
pytest test_app.py -v

# Run with detailed output
pytest test_app.py -vv

# Run specific test
pytest test_app.py::test_hello_endpoint -v

# Run with coverage report
pytest test_app.py --cov=app --cov-report=html
```

**Expected output:**
```
===================== test session starts =====================
platform darwin -- Python 3.13.2, pytest-7.4.3, pluggy-1.6.0
collected 2 items                                             

test_app.py::test_hello_endpoint PASSED                 [ 50%]
test_app.py::test_health_endpoint PASSED                [100%]

====================== 2 passed in 0.25s ======================
```

---

## GitHub Actions CI/CD Pipeline

### Pipeline File (`.github/workflows/ci-cd.yml`)

#### 1. **Pipeline Metadata**
```yaml
name: CI/CD Pipeline
```
- Defines the workflow name shown in GitHub Actions UI

#### 2. **Trigger Configuration**
```yaml
on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
```

**What triggers this pipeline:**
- `push` to `main` branch - When you push commits directly
- `pull_request` to `main` - When someone creates/updates a PR

**Why these triggers?**
- Ensures all code going to main is tested
- Catches issues before merging pull requests
- Provides fast feedback to developers

#### 3. **Job 1: Test (CI Stage)**

##### Job Configuration
```yaml
test:
  runs-on: ubuntu-latest
```
- `runs-on: ubuntu-latest` - Uses latest Ubuntu virtual machine
- GitHub provides free runners for public repositories

##### Step 1: Checkout Code
```yaml
- name: Checkout code
  uses: actions/checkout@v3
```

**What happens:**
- Downloads your repository code
- Checks out the specific commit/branch being tested
- `actions/checkout@v3` is a pre-built GitHub Action

##### Step 2: Setup Python
```yaml
- name: Set up Python
  uses: actions/setup-python@v4
  with:
    python-version: '3.9'
```

**What happens:**
- Installs Python 3.9 on the runner
- Sets up pip and virtualenv
- Configures PATH to use this Python version

**Why Python 3.9?**
- Stable, widely supported version
- Compatible with our dependencies
- Good balance of features and stability

##### Step 3: Install Dependencies
```yaml
- name: Install dependencies
  run: |
    pip install flask pytest
```

**What happens:**
- Runs shell command on the runner
- Installs Flask and pytest packages
- Uses pip (Python package manager)

**Alternative approach:**
```yaml
- name: Install dependencies
  run: |
    pip install -r requirements.txt
```

##### Step 4: Run Tests
```yaml
- name: Run tests
  run: |
    pytest test_app.py -v
```

**What happens:**
- Executes all tests in `test_app.py`
- `-v` flag provides verbose output
- If ANY test fails, the job fails

**This is the critical CI step:**
- ❌ Tests fail → Pipeline stops, deployment blocked
- ✅ Tests pass → Continue to deployment stage

#### 4. **Job 2: Deploy Staging (CD Stage)**

##### Job Configuration
```yaml
deploy_staging:
  needs: test  # Only runs if test job succeeds
  if: github.ref == 'refs/heads/main'  # Only on main branch
  runs-on: ubuntu-latest
```

**Dependencies and conditions:**
- `needs: test` - Waits for test job to complete successfully
- `if: github.ref == 'refs/heads/main'` - Only runs on main branch (not PRs)
- Creates a deployment pipeline: Test → Deploy

##### Deployment Step
```yaml
- name: Deploy to staging
  run: |
    echo "Deploying to staging environment..."
    # In production: Use secure deployment methods
```

**In this demo:**
- Simply prints a message (simulated deployment)
- In real projects, this would:
  - Connect to servers via SSH
  - Deploy Docker containers
  - Update Kubernetes clusters
  - Deploy to cloud platforms (AWS, Azure, GCP)
  - Run database migrations
  - Clear caches
  - Notify team members

**Production deployment example:**
```yaml
- name: Deploy to staging
  env:
    DEPLOY_KEY: ${{ secrets.STAGING_DEPLOY_KEY }}
  run: |
    # Setup SSH
    mkdir -p ~/.ssh
    echo "$DEPLOY_KEY" > ~/.ssh/id_rsa
    chmod 600 ~/.ssh/id_rsa
    
    # Deploy via SSH
    ssh user@staging-server.com 'bash -s' < deploy.sh
    
    # Verify deployment
    curl -f https://staging.example.com/health || exit 1
```

---

## Step-by-Step Guide

### Setup Your Local Environment

#### Step 1: Clone the Repository
```bash
# Clone from GitHub
git clone https://github.com/datatweets/cicd-pipeline-demo.git

# Navigate into directory
cd cicd-pipeline-demo

# Check the files
ls -la
```

**You should see:**
```
.github/          # GitHub Actions workflows
.gitignore        # Git ignore rules
README.md         # Project documentation
TUTORIAL.md       # This tutorial
app.py            # Flask application
requirements.txt  # Python dependencies
test_app.py       # Test suite
```

#### Step 2: Create Virtual Environment (Recommended)
```bash
# Create virtual environment
python3 -m venv .venv

# Activate it (macOS/Linux)
source .venv/bin/activate

# Activate it (Windows)
.venv\Scripts\activate

# Your prompt should change to show (.venv)
```

**Why use a virtual environment?**
- Isolates project dependencies
- Prevents conflicts with system packages
- Makes the project portable
- Good practice for Python development

#### Step 3: Install Dependencies
```bash
# Install Flask and pytest
pip3 install -r requirements.txt

# Verify installation
pip3 list | grep -E "flask|pytest"
```

**Expected output:**
```
flask       3.0.0
pytest      7.4.3
```

#### Step 4: Run Tests
```bash
# Run the test suite
pytest test_app.py -v
```

**Expected output:**
```
===================== test session starts =====================
test_app.py::test_hello_endpoint PASSED                 [ 50%]
test_app.py::test_health_endpoint PASSED                [100%]
====================== 2 passed in 0.25s ======================
```

✅ **If tests pass, your environment is set up correctly!**

#### Step 5: Run the Application
```bash
# Start the Flask server
python3 app.py
```

**Expected output:**
```
 * Serving Flask app 'app'
 * Debug mode: off
WARNING: This is a development server. Do not use it in production.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:8008
 * Running on http://192.168.1.100:8008
Press CTRL+C to quit
```

#### Step 6: Test the Endpoints

**Open a new terminal window** (keep the server running) and test:

```bash
# Test hello endpoint
curl http://localhost:8008/hello/World

# Expected response:
# {"message":"Hello, World!"}

# Test hello with your name
curl http://localhost:8008/hello/YourName

# Expected response:
# {"message":"Hello, YourName!"}

# Test health endpoint
curl http://localhost:8008/health

# Expected response:
# {"status":"healthy"}
```

**Or open in browser:**
- http://localhost:8008/hello/World
- http://localhost:8008/health

### Making Changes and Triggering CI/CD

#### Step 7: Make a Code Change

Let's add a new endpoint! Edit `app.py` and add:

```python
@app.route('/goodbye/<name>')
def goodbye(name):
    """Return a farewell message."""
    return jsonify({'message': f'Goodbye, {name}! See you soon!'})
```

**Full file should look like:**
```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/hello/<name>')
def hello(name):
    """Return a personalized greeting."""
    return jsonify({'message': f'Hello, {name}!'})

@app.route('/health')
def health():
    """Health check endpoint for monitoring."""
    return jsonify({'status': 'healthy'})

@app.route('/goodbye/<name>')  # NEW ENDPOINT
def goodbye(name):
    """Return a farewell message."""
    return jsonify({'message': f'Goodbye, {name}! See you soon!'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8008)
```

#### Step 8: Add a Test for New Endpoint

Edit `test_app.py` and add:

```python
def test_goodbye_endpoint(client):
    """Test the goodbye endpoint returns correct farewell."""
    response = client.get('/goodbye/World')
    assert response.status_code == 200
    assert response.json['message'] == 'Goodbye, World! See you soon!'
```

#### Step 9: Test Locally First
```bash
# Run tests to make sure they pass
pytest test_app.py -v

# Should show 3 passed tests now
```

**Expected output:**
```
test_app.py::test_hello_endpoint PASSED            [ 33%]
test_app.py::test_health_endpoint PASSED           [ 66%]
test_app.py::test_goodbye_endpoint PASSED          [100%]
====================== 3 passed in 0.25s ======================
```

#### Step 10: Commit and Push Changes
```bash
# Check what changed
git status

# Stage your changes
git add app.py test_app.py

# Commit with a descriptive message
git commit -m "Add goodbye endpoint with tests"

# Push to GitHub
git push origin main
```

**This push triggers the CI/CD pipeline! 🚀**

---

## What Happens When You Push Code

### Minute-by-minute breakdown

#### Minute 0:00 - You Push Code
```bash
git push origin main
```

**What happens:**
1. Git uploads your commits to GitHub
2. GitHub receives the push to `main` branch
3. GitHub checks for workflow files in `.github/workflows/`
4. Finds `ci-cd.yml` with trigger: `on: push: branches: [main]`
5. **Pipeline starts automatically!**

#### Minute 0:01 - Pipeline Initialized

**GitHub Actions:**
1. Creates a new workflow run
2. Assigns a unique run ID
3. Provisions an Ubuntu virtual machine (runner)
4. Sets up the environment

**You can watch this:**
1. Go to your GitHub repository
2. Click **"Actions"** tab
3. See your workflow run appear (yellow dot = running)

#### Minute 0:05 - Test Job Starts

**Step 1: Checkout code (5-10 seconds)**
```
Run actions/checkout@v3
Fetching the repository
Checking out commit abc123def456
```
- Downloads your repository
- Checks out the specific commit you pushed

**Step 2: Set up Python (10-15 seconds)**
```
Run actions/setup-python@v4
Setting up Python 3.9...
Successfully set up Python 3.9.18
```
- Installs Python 3.9
- Configures pip
- Caches Python for faster future runs

**Step 3: Install dependencies (15-20 seconds)**
```
Run pip install flask pytest
Collecting flask==3.0.0
Collecting pytest==7.4.3
Installing collected packages...
Successfully installed flask-3.0.0 pytest-7.4.3
```
- Installs Flask and pytest
- Downloads from PyPI (Python Package Index)

**Step 4: Run tests (5-10 seconds)**
```
Run pytest test_app.py -v
===================== test session starts =====================
test_app.py::test_hello_endpoint PASSED                 [ 33%]
test_app.py::test_health_endpoint PASSED                [ 66%]
test_app.py::test_goodbye_endpoint PASSED               [100%]
====================== 3 passed in 0.25s ======================
```

**✅ All tests passed!**

#### Minute 0:50 - Test Job Completes

**GitHub Actions updates:**
- Test job marked as ✅ **Passed**
- Green checkmark appears on commit
- Deploy job is now queued (because `needs: test` is satisfied)

#### Minute 0:51 - Deploy Job Starts

**Conditions checked:**
1. ✅ Test job passed (`needs: test`)
2. ✅ Branch is `main` (`if: github.ref == 'refs/heads/main'`)

**Deployment runs:**
```
Run deploy to staging
Deploying to staging environment...
```

**✅ Deployment complete!**

#### Minute 1:00 - Pipeline Complete

**Final status:**
- ✅ Test job: Passed
- ✅ Deploy job: Passed
- ✅ Overall workflow: Success

**Notifications sent:**
- Green checkmark on commit
- Email notification (if configured)
- Slack/Discord notification (if integrated)
- Status badge updated (if you have one)

### Visual Timeline

```
00:00 ─────► Push code to GitHub
00:01 ─────► Pipeline triggered
00:05 ─────► Checkout code
00:15 ─────► Setup Python
00:30 ─────► Install dependencies
00:45 ─────► Run tests
              │
              ├──► ❌ Tests fail → Pipeline stops
              │                    Notify developer
              │
              └──► ✅ Tests pass → Continue
00:50 ─────► Check if main branch
              │
              ├──► ❌ Not main → Stop (PR check only)
              │
              └──► ✅ Is main → Deploy
00:55 ─────► Deploy to staging
01:00 ─────► ✅ Complete!
```

---

## Troubleshooting

### Common Issues and Solutions

#### Issue 1: Tests Fail Locally

**Error:**
```
test_app.py::test_hello_endpoint FAILED
AssertionError: assert 'Hello World!' == 'Hello, World!'
```

**Solution:**
- Check your code matches the test expectations
- Pay attention to punctuation, spacing, capitalization
- Run tests in verbose mode: `pytest test_app.py -vv`

#### Issue 2: Import Error

**Error:**
```
ModuleNotFoundError: No module named 'flask'
```

**Solution:**
```bash
# Make sure virtual environment is activated
source .venv/bin/activate

# Reinstall dependencies
pip3 install -r requirements.txt

# Verify installation
pip3 list | grep flask
```

#### Issue 3: Pipeline Fails on GitHub

**Scenario:** Tests pass locally but fail in GitHub Actions

**Possible causes:**
1. **Different Python version**
   - Local: Python 3.13
   - GitHub: Python 3.9
   - Solution: Test with same version locally

2. **Missing dependencies**
   - Check `requirements.txt` is complete
   - Run: `pip freeze > requirements.txt`

3. **Environment-specific code**
   - Code that works only on your OS
   - Solution: Use cross-platform code

**How to debug:**
1. Go to Actions tab
2. Click failed workflow run
3. Click failed job
4. Expand failed step
5. Read error messages carefully

#### Issue 4: Port Already in Use

**Error:**
```
OSError: [Errno 48] Address already in use
```

**Solution:**
```bash
# Find process using port 8008
lsof -ti:8008

# Kill the process
kill -9 $(lsof -ti:8008)

# Or use a different port in app.py
app.run(host='0.0.0.0', port=8009)
```

#### Issue 5: Pipeline Not Triggering

**Possible causes:**
1. **Workflow file location wrong**
   - Must be: `.github/workflows/ci-cd.yml`
   - Check with: `ls -la .github/workflows/`

2. **YAML syntax error**
   - Validate at: https://www.yamllint.com/
   - Check indentation (use spaces, not tabs)

3. **Branch name mismatch**
   - Check: `git branch`
   - Must be on `main` branch

4. **GitHub Actions disabled**
   - Go to: Settings → Actions → General
   - Enable "Allow all actions"

---

## Best Practices

### 1. **Write Tests First (TDD)**

Instead of:
1. Write code
2. Write tests
3. Fix code to pass tests

Do:
1. Write failing test
2. Write code to pass test
3. Refactor

**Benefits:**
- Better code design
- 100% test coverage
- Fewer bugs

### 2. **Small, Frequent Commits**

❌ **Bad:**
```bash
git commit -m "Fixed stuff"  # After 3 days of changes
```

✅ **Good:**
```bash
git commit -m "Add user authentication endpoint"
git commit -m "Add tests for authentication"
git commit -m "Add input validation for login"
```

**Benefits:**
- Easy to review
- Easy to rollback
- Clear history

### 3. **Descriptive Commit Messages**

**Format:**
```
[Type] Brief summary (50 chars or less)

Detailed explanation if needed (wrap at 72 chars)

- Bullet points for multiple changes
- Reference issues: Fixes #123
```

**Types:**
- `feat:` New feature
- `fix:` Bug fix
- `test:` Add/update tests
- `docs:` Documentation
- `refactor:` Code restructuring
- `style:` Formatting
- `chore:` Maintenance

**Example:**
```
feat: Add goodbye endpoint

Implements a new /goodbye/<name> endpoint that returns
a farewell message. This complements the existing hello
endpoint and demonstrates route parameters.

- Add goodbye() function to app.py
- Add test_goodbye_endpoint() to test suite
- Update README with new endpoint documentation

Closes #42
```

### 4. **Keep Tests Fast**

- Aim for tests to run in under 1 minute
- Use fixtures to avoid repetition
- Mock external services (databases, APIs)
- Run slow tests separately (integration vs unit)

### 5. **Monitor Pipeline Health**

Set up notifications:
```yaml
# In .github/workflows/ci-cd.yml
on:
  workflow_run:
    workflows: ["CI/CD Pipeline"]
    types: [completed]

jobs:
  notify:
    runs-on: ubuntu-latest
    steps:
      - name: Notify team
        if: ${{ failure() }}
        run: |
          curl -X POST ${{ secrets.SLACK_WEBHOOK }} \
            -d '{"text":"Pipeline failed! Check it out."}'
```

### 6. **Security Best Practices**

**Never commit secrets:**
```bash
# ❌ BAD - Don't do this!
DATABASE_URL="postgresql://user:password@host/db"

# ✅ GOOD - Use GitHub Secrets
DATABASE_URL="${{ secrets.DATABASE_URL }}"
```

**Use GitHub Secrets:**
1. Go to Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Add: Name = `DATABASE_URL`, Value = `postgresql://...`
4. Reference in workflow: `${{ secrets.DATABASE_URL }}`

**Scan for vulnerabilities:**
```yaml
- name: Security scan
  run: |
    pip install safety
    safety check
```

### 7. **Implement Branch Protection**

Go to: Settings → Branches → Add rule

✅ Enable:
- Require pull request reviews
- Require status checks (CI) to pass
- Require branches to be up to date
- Include administrators

**Benefits:**
- No direct pushes to main
- All code is reviewed
- All code is tested
- Maintains quality

### 8. **Use Pull Request Workflow**

```bash
# Create feature branch
git checkout -b feature/new-endpoint

# Make changes
# ... edit files ...

# Commit changes
git commit -m "feat: Add new endpoint"

# Push to GitHub
git push origin feature/new-endpoint

# Create Pull Request on GitHub
# - CI runs automatically on PR
# - Request code review
# - Merge only after approval + passing tests
```

---

## Next Steps

### Level 1: Enhance Testing

#### Add Code Coverage
```bash
# Install coverage tool
pip install pytest-cov

# Run with coverage
pytest test_app.py --cov=app --cov-report=html

# Open htmlcov/index.html to see report
```

**Update workflow:**
```yaml
- name: Run tests with coverage
  run: |
    pip install pytest pytest-cov
    pytest test_app.py --cov=app --cov-report=xml

- name: Upload coverage
  uses: codecov/codecov-action@v3
```

#### Add More Test Types
```python
# Integration tests
def test_multiple_endpoints_in_sequence(client):
    client.get('/hello/Alice')
    client.get('/goodbye/Alice')
    health = client.get('/health')
    assert health.json['status'] == 'healthy'

# Error handling tests
def test_404_error(client):
    response = client.get('/nonexistent')
    assert response.status_code == 404

# Performance tests
def test_response_time(client):
    import time
    start = time.time()
    client.get('/hello/World')
    duration = time.time() - start
    assert duration < 0.1  # Should respond in under 100ms
```

### Level 2: Add Code Quality Tools

#### Linting (flake8)
```yaml
- name: Lint with flake8
  run: |
    pip install flake8
    flake8 app.py test_app.py --max-line-length=100
```

#### Code Formatting (black)
```yaml
- name: Check code formatting
  run: |
    pip install black
    black --check app.py test_app.py
```

#### Type Checking (mypy)
```yaml
- name: Type check
  run: |
    pip install mypy
    mypy app.py
```

### Level 3: Containerization

#### Create Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 8008

CMD ["gunicorn", "--bind", "0.0.0.0:8008", "app:app"]
```

#### Update requirements.txt
```
flask==3.0.0
pytest==7.4.3
gunicorn==21.2.0
```

#### Build and Run
```bash
# Build image
docker build -t flask-cicd-demo .

# Run container
docker run -p 8008:8008 flask-cicd-demo

# Test
curl http://localhost:8008/health
```

#### Add to CI/CD
```yaml
- name: Build Docker image
  run: docker build -t myapp:${{ github.sha }} .

- name: Push to registry
  run: |
    echo ${{ secrets.DOCKER_PASSWORD }} | docker login -u ${{ secrets.DOCKER_USERNAME }} --password-stdin
    docker push myapp:${{ github.sha }}
```

### Level 4: Deploy to Real Environment

#### Deploy to Heroku
```yaml
deploy_production:
  needs: test
  if: github.ref == 'refs/heads/main'
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v3
    - uses: akhileshns/heroku-deploy@v3.12.12
      with:
        heroku_api_key: ${{ secrets.HEROKU_API_KEY }}
        heroku_app_name: "your-app-name"
        heroku_email: "your-email@example.com"
```

#### Deploy to AWS (ECS)
```yaml
- name: Deploy to AWS ECS
  run: |
    aws ecs update-service \
      --cluster my-cluster \
      --service my-service \
      --force-new-deployment
  env:
    AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
    AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
```

#### Deploy to Kubernetes
```yaml
- name: Deploy to Kubernetes
  run: |
    kubectl set image deployment/flask-app \
      flask-app=myapp:${{ github.sha }}
    kubectl rollout status deployment/flask-app
```

### Level 5: Advanced Monitoring

#### Add Application Monitoring
```python
# app.py - Add Prometheus metrics
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)

@app.route('/hello/<name>')
@metrics.counter('hello_requests', 'Number of hello requests')
def hello(name):
    return jsonify({'message': f'Hello, {name}!'})
```

#### Add Health Checks
```python
@app.route('/health/liveness')
def liveness():
    """Kubernetes liveness probe"""
    return jsonify({'status': 'alive'})

@app.route('/health/readiness')
def readiness():
    """Kubernetes readiness probe"""
    # Check database connection, etc.
    return jsonify({'status': 'ready'})
```

#### Add Logging
```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/hello/<name>')
def hello(name):
    logger.info(f"Hello endpoint called with name: {name}")
    return jsonify({'message': f'Hello, {name}!'})
```

### Level 6: Multi-Environment Deployment

```yaml
jobs:
  deploy_staging:
    needs: test
    if: github.ref == 'refs/heads/main'
    environment: staging
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to staging
        run: ./deploy.sh staging

  deploy_production:
    needs: deploy_staging
    if: github.ref == 'refs/heads/main'
    environment: production
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to production
        run: ./deploy.sh production
      
      - name: Smoke test
        run: curl -f https://api.example.com/health
```

---

## Conclusion

You now have a complete understanding of:

✅ **Application Architecture** - How Flask APIs work  
✅ **Testing Strategy** - Writing effective tests with pytest  
✅ **CI/CD Pipeline** - Automating testing and deployment  
✅ **GitHub Actions** - Configuring workflows  
✅ **Best Practices** - Professional development workflows  
✅ **Next Steps** - Paths to expand your knowledge  

### Key Takeaways

1. **Automation saves time** - Once set up, CI/CD runs automatically
2. **Tests catch bugs early** - Before they reach production
3. **Small iterations work better** - Commit often, deploy frequently
4. **Documentation matters** - Help your future self and team
5. **Security is critical** - Never commit secrets

### Resources for Further Learning

**CI/CD:**
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [CI/CD Best Practices](https://www.atlassian.com/continuous-delivery/principles/continuous-integration-vs-delivery-vs-deployment)

**Python & Flask:**
- [Flask Documentation](https://flask.palletsprojects.com/)
- [pytest Documentation](https://docs.pytest.org/)

**DevOps:**
- [The Phoenix Project](https://itrevolution.com/the-phoenix-project/) (Book)
- [DevOps Roadmap](https://roadmap.sh/devops)

**Practice:**
- [Exercism Python Track](https://exercism.org/tracks/python)
- [GitHub Actions Learning Lab](https://lab.github.com/)

---

## Questions?

If you have questions or run into issues:

1. Check the [Troubleshooting](#troubleshooting) section
2. Review the [GitHub Actions logs](https://github.com/datatweets/cicd-pipeline-demo/actions)
3. Read error messages carefully
4. Search Stack Overflow
5. Ask in developer communities

**Happy Coding! 🚀**
