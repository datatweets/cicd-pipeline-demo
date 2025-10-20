# CI/CD Pipeline Demo

A comprehensive guide to implementing Continuous Integration and Continuous Deployment using GitHub Actions with a Flask web application.

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Project Structure](#project-structure)
4. [Installation and Setup](#installation-and-setup)
5. [Running the Application](#running-the-application)
6. [Testing](#testing)
7. [Understanding the CI/CD Pipeline](#understanding-the-cicd-pipeline)
8. [GitHub Actions Workflow](#github-actions-workflow)
9. [Making Changes and Triggering the Pipeline](#making-changes-and-triggering-the-pipeline)
10. [Common Commands](#common-commands)
11. [Troubleshooting](#troubleshooting)
12. [Security Best Practices](#security-best-practices)
13. [Next Steps](#next-steps)

## Overview

This project demonstrates a complete CI/CD pipeline implementation using:

- **Flask** - Lightweight Python web framework for building the API
- **pytest** - Testing framework for automated testing
- **GitHub Actions** - CI/CD automation platform

The application provides a simple REST API with endpoints for greetings and health checks. Every code change is automatically tested, and successful changes to the main branch are automatically deployed to a staging environment.

### What is CI/CD?

**Continuous Integration (CI)** is the practice of automatically testing code changes whenever they are pushed to the repository. This catches bugs early and ensures code quality.

**Continuous Deployment (CD)** is the practice of automatically deploying code to staging or production environments after it passes all tests. This enables faster releases and reduces manual errors.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.9 or higher**
- **pip** (Python package manager)
- **Git** (for version control)
- **A GitHub account** (for repository hosting and CI/CD)

## Project Structure

```
cicd-pipeline-demo/
├── .github/
│   └── workflows/
│       └── ci-cd.yml          # GitHub Actions CI/CD configuration
├── app.py                      # Flask application with REST API
├── test_app.py                 # Automated test suite using pytest
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git ignore rules
├── README.md                   # This file
└── TUTORIAL.md                 # Detailed tutorial and concepts
```

### Key Files

**app.py** - Contains the Flask application with two endpoints:
- `/hello/<name>` - Returns a personalized JSON greeting
- `/health` - Returns service health status

**test_app.py** - Contains automated tests for all endpoints

**.github/workflows/ci-cd.yml** - Defines the CI/CD pipeline that runs on GitHub Actions

**requirements.txt** - Lists all Python dependencies (Flask and pytest)

## Installation and Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/datatweets/cicd-pipeline-demo.git
cd cicd-pipeline-demo
```

### Step 2: Create a Virtual Environment (Required)

A virtual environment isolates project dependencies from your system Python installation. This prevents conflicts between different projects and keeps your system Python clean.

**Create the virtual environment:**

```bash
python -m venv .venv
```

This creates a `.venv` directory containing a separate Python environment.

**Activate the virtual environment:**

For macOS/Linux:
```bash
source .venv/bin/activate
```

For Windows:
```bash
.venv\Scripts\activate
```

When activated successfully, your terminal prompt will change to show `(.venv)` at the beginning:
```
(.venv) user@computer cicd-pipeline-demo %
```

**Important:** You must activate the virtual environment every time you open a new terminal session to work on this project.

### Step 3: Install Dependencies

With the virtual environment activated, install Flask and pytest:

```bash
pip install -r requirements.txt
```

**Note:** Use `pip` (not `pip3`) when inside an activated virtual environment. The virtual environment ensures you're using the correct Python version.

This command installs:
- Flask 3.0.0 - Web framework
- pytest 7.4.3 - Testing framework
- Werkzeug, Jinja2, and other dependencies required by Flask

You'll see output like:
```
Collecting flask==3.0.0
  Using cached flask-3.0.0-py3-none-any.whl
Collecting pytest==7.4.3
  Using cached pytest-7.4.3-py3-none-any.whl
Installing collected packages: ...
Successfully installed flask-3.0.0 pytest-7.4.3 ...
```

### Step 4: Verify Installation

Confirm packages are installed correctly in your virtual environment:

```bash
pip list | grep -E "flask|pytest"
```

Expected output:
```
flask       3.0.0
pytest      7.4.3
```

Alternatively, verify Python can import Flask:
```bash
python -c "import flask; print(f'Flask version: {flask.__version__}')"
```

Expected output:
```
Flask version: 3.0.0
```

## Running the Application

### Start the Flask Development Server

Make sure your virtual environment is activated (you should see `(.venv)` in your prompt), then run:

```bash
python app.py
```

**Note:** Use `python` (not `python3`) when inside an activated virtual environment.

Expected output:
```
 * Serving Flask app 'app'
 * Debug mode: off
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:8008
 * Running on http://192.168.1.x:8008
Press CTRL+C to quit
```

The application is now running on port 8008.

### Test the Endpoints

Open a new terminal window (keep the server running in the first terminal) and test the API:

**Test the greeting endpoint:**
```bash
curl http://localhost:8008/hello/World
```

Expected response:
```json
{"message":"Hello, World!"}
```

**Test with your name:**
```bash
curl http://localhost:8008/hello/Alice
```

Expected response:
```json
{"message":"Hello, Alice!"}
```

**Test the health check endpoint:**
```bash
curl http://localhost:8008/health
```

Expected response:
```json
{"status":"healthy"}
```

### Access in Browser

You can also access these URLs in your web browser:
- http://localhost:8008/hello/World
- http://localhost:8008/health

### Stop the Server

Press `Ctrl+C` in the terminal where the server is running.

## Testing

### Run All Tests

```bash
pytest test_app.py -v
```

Expected output:
```
===================== test session starts =====================
test_app.py::test_hello_endpoint PASSED                 [ 50%]
test_app.py::test_health_endpoint PASSED                [100%]
====================== 2 passed in 0.25s ======================
```

### Run Specific Test

```bash
pytest test_app.py::test_hello_endpoint -v
```

### Run Tests with Coverage

```bash
pytest test_app.py --cov=app --cov-report=html
```

This generates an HTML coverage report in the `htmlcov/` directory.

### Understanding the Tests

The test suite uses pytest with fixtures:

```python
@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
```

This fixture creates a test client that can make requests to the Flask app without actually starting a server.

## Understanding the CI/CD Pipeline

### The Workflow Process

```
Developer commits code
         ↓
  Pushes to GitHub
         ↓
GitHub Actions triggered
         ↓
    Checkout code
         ↓
   Setup Python 3.9
         ↓
 Install dependencies
         ↓
    Run tests
         ↓
  Tests pass?
    ↓        ↓
   Yes       No → Stop and notify
    ↓
Main branch?
    ↓        ↓
   Yes       No → Stop (PR check only)
    ↓
Deploy to staging
         ↓
  Complete (Success)
```

### Pipeline Triggers

The CI/CD pipeline runs automatically when:
1. Code is pushed to the `main` branch
2. A pull request is created or updated targeting `main`

### Pipeline Jobs

**Job 1: Test (CI Stage)**
- Duration: ~40-55 seconds
- Steps:
  1. Checkout code from repository
  2. Setup Python 3.9 environment
  3. Install dependencies (Flask, pytest)
  4. Run automated tests

**Job 2: Deploy (CD Stage)**
- Duration: ~10-15 seconds
- Conditions: Only runs if tests pass AND branch is `main`
- Steps:
  1. Simulate deployment to staging environment
  2. In production, this would deploy to actual servers

## GitHub Actions Workflow

### Viewing Pipeline Runs

1. Navigate to your repository on GitHub
2. Click the **Actions** tab
3. See list of workflow runs with status indicators:
   - Green checkmark = Success
   - Red X = Failed
   - Yellow dot = In progress

### Workflow Configuration

The pipeline is defined in `.github/workflows/ci-cd.yml`:

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      
      - name: Install dependencies
        run: pip install flask pytest
      
      - name: Run tests
        run: pytest test_app.py -v
  
  deploy_staging:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to staging
        run: echo "Deploying to staging environment..."
```

### Key Configuration Elements

- **on: push** - Triggers when code is pushed
- **on: pull_request** - Triggers when PR is created/updated
- **runs-on: ubuntu-latest** - Uses Ubuntu virtual machine
- **needs: test** - Deploy job waits for test job to complete
- **if: github.ref == 'refs/heads/main'** - Deploy only runs on main branch

## Making Changes and Triggering the Pipeline

### Example: Adding a New Endpoint

**Step 1: Add endpoint to app.py**

```python
@app.route('/goodbye/<name>')
def goodbye(name):
    """Return a farewell message."""
    return jsonify({'message': f'Goodbye, {name}! See you soon!'})
```

**Step 2: Add test to test_app.py**

```python
def test_goodbye_endpoint(client):
    """Test the goodbye endpoint returns correct farewell."""
    response = client.get('/goodbye/World')
    assert response.status_code == 200
    assert response.json['message'] == 'Goodbye, World! See you soon!'
```

**Step 3: Test locally**

```bash
pytest test_app.py -v
```

Verify all 3 tests pass.

**Step 4: Commit and push**

```bash
git add app.py test_app.py
git commit -m "feat: Add goodbye endpoint with tests"
git push origin main
```

**Step 5: Watch the pipeline**

Go to the Actions tab on GitHub and watch your pipeline run automatically.

### Development Workflow Best Practices

1. **Always test locally first** - Catch issues before pushing
2. **Write tests for new features** - Maintain test coverage
3. **Use descriptive commit messages** - Help others understand changes
4. **Create feature branches** - Keep main branch stable
5. **Use pull requests** - Enable code review before merging

## Common Commands

### Git Workflow

```bash
# Check repository status
git status

# Create a feature branch
git checkout -b feature/my-feature

# Stage changes
git add .

# Commit with descriptive message
git commit -m "feat: Add new feature"

# Push to GitHub
git push origin feature/my-feature

# Push to main (triggers CI/CD)
git push origin main
```

### Testing Commands

```bash
# Run all tests
pytest test_app.py -v

# Run specific test
pytest test_app.py::test_hello_endpoint

# Run with verbose output
pytest test_app.py -vv

# Run with coverage report
pytest test_app.py --cov=app --cov-report=html
```

### Flask Application

```bash
# Activate virtual environment first
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows

# Start application (inside activated venv)
python app.py

# Test endpoints (in a separate terminal)
curl http://localhost:8008/hello/World
curl http://localhost:8008/health

# Stop the server: Press Ctrl+C in the server terminal

# Kill process on port (if needed)
lsof -ti:8008 | xargs kill -9
```

### Managing Virtual Environment

```bash
# Create virtual environment (one time)
python -m venv .venv

# Activate virtual environment (every new terminal session)
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows

# Check you're in the virtual environment
which python  # Should show path inside .venv/

# Deactivate virtual environment
deactivate

# Install new package (inside activated venv)
pip install package-name

# Update requirements.txt (inside activated venv)
pip freeze > requirements.txt

# Install all packages from requirements.txt
pip install -r requirements.txt
```

## Troubleshooting

### Issue: Tests Fail Locally

**Problem:** Tests return errors or assertion failures

**Solution:**

```bash
# Make sure virtual environment is activated
source .venv/bin/activate

# Run tests with verbose output to see details
pytest test_app.py -vv

# Check if dependencies are installed in venv
pip list | grep -E "flask|pytest"

# Reinstall dependencies if needed
pip install -r requirements.txt
```

### Issue: Import Error

**Problem:** `ModuleNotFoundError: No module named 'flask'`

**Solution:**

```bash
# First, check if virtual environment is activated
# Your prompt should show (.venv) at the beginning

# If not activated, activate it:
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows

# Verify you're using the virtual environment's Python:
which python  # Should show path inside .venv/

# Install dependencies in the virtual environment:
pip install -r requirements.txt

# Verify Flask is installed:
python -c "import flask; print(flask.__version__)"
```

**Common cause:** Forgetting to activate the virtual environment before running commands.

### Issue: Port Already in Use

**Problem:** `OSError: [Errno 48] Address already in use`

**Solution:**
```bash
# Find process using port 8008
lsof -ti:8008

# Kill the process
kill -9 $(lsof -ti:8008)

# Or use a different port in app.py
# Change: app.run(host='0.0.0.0', port=8009)
```

### Issue: Pipeline Not Triggering

**Problem:** GitHub Actions workflow doesn't run after pushing code

**Solutions:**
1. Verify workflow file location: `.github/workflows/ci-cd.yml`
2. Check YAML syntax (no tabs, correct indentation)
3. Confirm branch name matches trigger configuration
4. Ensure GitHub Actions is enabled in repository settings

### Issue: Pipeline Fails but Tests Pass Locally

**Problem:** Tests pass locally but fail in GitHub Actions

**Common causes:**
- Python version differences (local vs. GitHub Actions)
- Missing dependencies in requirements.txt
- Environment-specific code
- File path issues (case sensitivity on Linux)

**Solution:**
1. Check GitHub Actions logs for specific error
2. Ensure requirements.txt includes all dependencies
3. Test with Python 3.9 locally (same as CI)
4. Avoid hard-coded paths or OS-specific code

### Getting Help

1. Check the CICD Pipeline Tutorial for detailed explanations
2. Review GitHub Actions logs for error details
3. Search error messages on Stack Overflow
4. Check Flask and pytest documentation

## Security Best Practices

### Protecting Sensitive Information

**Never commit these to your repository:**
- Passwords or API keys
- Database credentials
- SSH private keys
- OAuth tokens
- Secret keys

### Use GitHub Secrets

For sensitive configuration in CI/CD:

1. Go to repository Settings > Secrets and variables > Actions
2. Click "New repository secret"
3. Add name and value
4. Reference in workflow: `${{ secrets.SECRET_NAME }}`

Example:
```yaml
- name: Deploy
  env:
    API_KEY: ${{ secrets.API_KEY }}
  run: ./deploy.sh
```

### Additional Security Measures

- Enable branch protection rules
- Require pull request reviews before merging
- Require status checks to pass before merging
- Keep dependencies updated
- Use HTTPS for deployment
- Implement proper access controls
- Rotate credentials regularly
- Scan for vulnerabilities (e.g., `pip install safety; safety check`)

## Next Steps

### Enhance the Application

1. **Add More Endpoints**
   - Status endpoint with version info
   - Error handling for invalid requests
   - Request logging

2. **Improve Testing**
   - Add integration tests
   - Test error scenarios (404, 500)
   - Achieve 100% code coverage
   - Add performance tests

3. **Add Code Quality Tools**
   - Linting with flake8
   - Code formatting with black
   - Type checking with mypy
   - Security scanning

### Enhance the CI/CD Pipeline

4. **Add More Pipeline Stages**
   - Code linting stage
   - Security scanning stage
   - Build Docker images
   - Deploy to multiple environments

5. **Containerize the Application**
   - Create Dockerfile
   - Build images in CI
   - Push to container registry
   - Deploy containers

6. **Deploy to Production**
   - Heroku
   - AWS (ECS, Lambda, Elastic Beanstalk)
   - Azure App Service
   - Google Cloud Run
   - DigitalOcean App Platform



### Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [pytest Documentation](https://docs.pytest.org/)
- [CI/CD Best Practices](https://www.atlassian.com/continuous-delivery)
- [TUTORIAL.md](TUTORIAL.md) - Detailed concepts and explanations

## Summary

You now have a working CI/CD pipeline that:
- Automatically tests every code change
- Deploys to staging when tests pass
- Provides fast feedback on code quality
- Enables confident, frequent releases

The pipeline embodies modern software development practices: automated testing, continuous integration, and continuous deployment.

For a deeper understanding of the concepts, architecture, and advanced topics, see [TUTORIAL.md](TUTORIAL.md).
2. **Add Linting**: Integrate code quality tools (flake8, black)
3. **Add Code Coverage**: Track test coverage percentage
4. **Deploy to Production**: Add a production deployment stage
5. **Add Monitoring**: Integrate application monitoring
6. **Docker**: Containerize the application
7. **Database**: Add database integration and migrations

## Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [pytest Documentation](https://docs.pytest.org/)

## License

This is a demo project for educational purposes.
