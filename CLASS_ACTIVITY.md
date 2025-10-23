# Guided Class Activity: Feature Branch Workflow with CI/CD

## Overview

In this hands-on activity, you'll experience a real-world development workflow by adding new features to the Flask API. You'll learn how professional development teams work with:

- Feature branches
- Pull requests
- Code reviews
- Automated testing
- CI/CD pipeline execution
- Branch merging

**Time Required:** 45-60 minutes

**What You'll Build:** Two new API endpoints with tests

---

## Learning Objectives

By the end of this activity, you will be able to:

1. Create and work with feature branches
2. Write code and tests for new features
3. Push changes and create pull requests on GitHub
4. Review and merge pull requests
5. Watch the CI/CD pipeline execute automatically
6. Understand the complete development lifecycle

---

## Prerequisites

Before starting, ensure you have:

- ✅ Completed the basic setup from README.md
- ✅ Virtual environment activated (`source .venv/bin/activate`)
- ✅ All dependencies installed (`pip install -r requirements.txt`)
- ✅ Application running successfully (`python app.py`)
- ✅ Tests passing locally (`pytest test_app.py -v`)
- ✅ Git configured with your name and email
- ✅ GitHub repository forked to your account

---

## Part 1: Add a Goodbye Endpoint (15 minutes)

### Step 1.1: Create a Feature Branch

**Why?** Feature branches keep your main branch stable and allow you to work on features independently.

```bash
# Make sure you're on main branch
git checkout main

# Pull latest changes
git pull origin main

# Create and switch to new feature branch
git checkout -b feature/goodbye-endpoint

# Verify you're on the new branch
git branch
```

Expected output:
```
* feature/goodbye-endpoint
  main
```

The `*` shows your current branch.

### Step 1.2: Add the Goodbye Endpoint

Open `app.py` and add this new endpoint **after** the existing `/health` endpoint:

```python
@app.route('/goodbye/<name>')
def goodbye(name):
    """Return a farewell message."""
    return jsonify({'message': f'Goodbye, {name}! See you soon!'})
```

**Your `app.py` should now have 3 endpoints:**
1. `/hello/<name>` - Greeting
2. `/health` - Health check
3. `/goodbye/<name>` - Farewell (NEW!)

### Step 1.3: Test the New Endpoint Manually

Start the Flask server:
```bash
python app.py
```

In a **new terminal**, test the endpoint:
```bash
curl http://localhost:8008/goodbye/Alice
```

Expected response:
```json
{"message":"Goodbye, Alice! See you soon!"}
```

Try with different names:
```bash
curl http://localhost:8008/goodbye/Bob
curl http://localhost:8008/goodbye/Charlie
```

Stop the server (Ctrl+C) when done testing.

### Step 1.4: Add Automated Test

Open `test_app.py` and add this test **after** the existing tests:

```python
def test_goodbye_endpoint(client):
    """Test the goodbye endpoint returns correct farewell."""
    response = client.get('/goodbye/World')
    assert response.status_code == 200
    assert response.json['message'] == 'Goodbye, World! See you soon!'
```

### Step 1.5: Run Tests Locally

Always test locally before pushing:

```bash
pytest test_app.py -v
```

Expected output:
```
test_app.py::test_hello_endpoint PASSED     [ 33%]
test_app.py::test_health_endpoint PASSED    [ 66%]
test_app.py::test_goodbye_endpoint PASSED   [100%]

====================== 3 passed in 0.25s ======================
```

**If tests fail:**
- Check your code for typos
- Verify the endpoint message format matches the test
- Make sure you saved all files

### Step 1.6: Commit Your Changes

```bash
# Check what files changed
git status

# Stage the changes
git add app.py test_app.py

# Commit with a descriptive message
git commit -m "feat: Add goodbye endpoint with farewell messages"

# Push to GitHub
git push origin feature/goodbye-endpoint
```

**Understanding the commit message:**
- `feat:` - Indicates a new feature
- Descriptive but concise
- Follows conventional commits standard

### Step 1.7: Create a Pull Request

1. Go to your GitHub repository in a browser
2. You'll see a banner: **"Compare & pull request"** - Click it
3. Fill in the PR details:

**Title:**
```
Add Goodbye Endpoint
```

**Description:**
```
## Changes
- Added `/goodbye/<name>` endpoint that returns farewell messages
- Added comprehensive test coverage for the new endpoint

## Testing
- ✅ Tested manually with curl
- ✅ All automated tests passing (3/3)
- ✅ No breaking changes to existing endpoints

## Type of Change
- [x] New feature
- [ ] Bug fix
- [ ] Breaking change
```

4. Click **"Create pull request"**

### Step 1.8: Watch the CI/CD Pipeline

1. In your pull request, click the **"Checks"** tab
2. Watch the pipeline execute in real-time
3. You'll see:
   - ✅ **Checkout code** (5-10 seconds)
   - ✅ **Set up Python** (15-20 seconds)
   - ✅ **Install dependencies** (10-15 seconds)
   - ✅ **Run tests** (5-10 seconds)

**Total time:** ~40-55 seconds

**What's happening?**
- GitHub creates a fresh Ubuntu VM
- Installs Python and dependencies
- Runs your tests
- Reports success/failure

### Step 1.9: Merge the Pull Request

Once the checks pass (green checkmarks):

1. Click **"Merge pull request"**
2. Click **"Confirm merge"**
3. Optionally: Click **"Delete branch"** (good practice)

### Step 1.10: Watch the Deployment Pipeline

1. Go to the **"Actions"** tab
2. Find the latest workflow run (triggered by the merge)
3. Click on it to see details
4. Notice it has **2 jobs** this time:
   - ✅ **test** - Runs tests again
   - ✅ **deploy_staging** - Simulates deployment (only runs on main branch)

**Why test again?**
- Final verification before deployment
- Ensures nothing broke during merge
- Professional safety practice

### Step 1.11: Pull Changes Locally

```bash
# Switch back to main branch
git checkout main

# Pull the merged changes
git pull origin main

# Verify your feature is in main
git log --oneline -3
```

**Congratulations!** You've completed your first feature using professional Git workflow! 🎉

---

## Part 2: Add a Status Endpoint (20 minutes)

Now you'll repeat the process independently to reinforce the workflow.

### Step 2.1: Create Another Feature Branch

```bash
# Make sure you're on main
git checkout main

# Create new feature branch
git checkout -b feature/status-endpoint

# Verify
git branch
```

### Step 2.2: Add the Status Endpoint

Add this to `app.py` after the `/goodbye/<name>` endpoint:

```python
@app.route('/status')
def status():
    """Return detailed service status information."""
    import sys
    return jsonify({
        'status': 'operational',
        'version': '1.0.0',
        'python_version': sys.version.split()[0],
        'endpoints': [
            '/hello/<name>',
            '/goodbye/<name>',
            '/health',
            '/status'
        ]
    })
```

### Step 2.3: Test Manually

```bash
# Start server
python app.py

# In new terminal, test
curl http://localhost:8008/status
```

Expected response:
```json
{
  "endpoints": [
    "/hello/<name>",
    "/goodbye/<name>",
    "/health",
    "/status"
  ],
  "python_version": "3.9.x",
  "status": "operational",
  "version": "1.0.0"
}
```

### Step 2.4: Add Automated Test

Add to `test_app.py`:

```python
def test_status_endpoint(client):
    """Test the status endpoint returns service information."""
    response = client.get('/status')
    assert response.status_code == 200
    assert response.json['status'] == 'operational'
    assert response.json['version'] == '1.0.0'
    assert '/hello/<name>' in response.json['endpoints']
    assert '/status' in response.json['endpoints']
```

### Step 2.5: Run All Tests

```bash
pytest test_app.py -v
```

Expected: **4 tests passed** ✅

### Step 2.6: Commit and Push

```bash
git add app.py test_app.py
git commit -m "feat: Add status endpoint with service information"
git push origin feature/status-endpoint
```

### Step 2.7: Create Pull Request

1. Go to GitHub
2. Click **"Compare & pull request"**
3. Title: `Add Status Endpoint`
4. Description:

```
## Changes
- Added `/status` endpoint that returns:
  - Service operational status
  - Version information
  - Python version
  - List of all available endpoints

## Testing
- ✅ Manual testing completed
- ✅ All 4 automated tests passing
- ✅ No breaking changes

## Type of Change
- [x] New feature
```

5. Create the pull request

### Step 2.8: Review and Merge

1. Watch the CI/CD pipeline execute
2. Wait for green checkmarks
3. Merge the pull request
4. Delete the feature branch
5. Watch the deployment pipeline run

### Step 2.9: Pull Changes Locally

```bash
git checkout main
git pull origin main

# Verify both features are now in main
git log --oneline -5
```

---

## Part 3: Add an Error Handling Endpoint (20 minutes)

For advanced practice, add one more feature that demonstrates error handling.

### Step 3.1: Create Feature Branch

```bash
git checkout main
git checkout -b feature/calculate-endpoint
```

### Step 3.2: Add Calculation Endpoint with Error Handling

Add to `app.py`:

```python
@app.route('/calculate/<operation>/<int:num1>/<int:num2>')
def calculate(operation, num1, num2):
    """Perform basic calculations with error handling."""
    operations = {
        'add': num1 + num2,
        'subtract': num1 - num2,
        'multiply': num1 * num2,
        'divide': num1 / num2 if num2 != 0 else None
    }
    
    if operation not in operations:
        return jsonify({
            'error': 'Invalid operation',
            'valid_operations': list(operations.keys())
        }), 400
    
    result = operations[operation]
    
    if result is None:
        return jsonify({
            'error': 'Division by zero not allowed'
        }), 400
    
    return jsonify({
        'operation': operation,
        'num1': num1,
        'num2': num2,
        'result': result
    })
```

### Step 3.3: Test Manually

```bash
python app.py
```

In another terminal:
```bash
# Test addition
curl http://localhost:8008/calculate/add/5/3

# Test division
curl http://localhost:8008/calculate/divide/10/2

# Test error: division by zero
curl http://localhost:8008/calculate/divide/10/0

# Test error: invalid operation
curl http://localhost:8008/calculate/power/2/3
```

### Step 3.4: Add Comprehensive Tests

Add to `test_app.py`:

```python
def test_calculate_endpoint_addition(client):
    """Test calculate endpoint for addition."""
    response = client.get('/calculate/add/5/3')
    assert response.status_code == 200
    assert response.json['result'] == 8
    assert response.json['operation'] == 'add'

def test_calculate_endpoint_division(client):
    """Test calculate endpoint for division."""
    response = client.get('/calculate/divide/10/2')
    assert response.status_code == 200
    assert response.json['result'] == 5

def test_calculate_endpoint_division_by_zero(client):
    """Test calculate endpoint handles division by zero."""
    response = client.get('/calculate/divide/10/0')
    assert response.status_code == 400
    assert 'error' in response.json
    assert 'Division by zero' in response.json['error']

def test_calculate_endpoint_invalid_operation(client):
    """Test calculate endpoint handles invalid operations."""
    response = client.get('/calculate/power/2/3')
    assert response.status_code == 400
    assert 'error' in response.json
    assert 'Invalid operation' in response.json['error']
```

### Step 3.5: Run All Tests

```bash
pytest test_app.py -v
```

Expected: **8 tests passed** ✅

### Step 3.6: Complete the Workflow

```bash
# Commit
git add app.py test_app.py
git commit -m "feat: Add calculate endpoint with error handling"

# Push
git push origin feature/calculate-endpoint

# Create PR on GitHub
# Wait for CI/CD checks
# Merge when green
# Pull changes locally
git checkout main
git pull origin main
```

---

## Part 4: Review and Reflection (10 minutes)

### Check Your Final Application

1. Activate virtual environment
2. Start the application: `python app.py`
3. Test all endpoints:

```bash
# Original endpoints
curl http://localhost:8008/hello/Student
curl http://localhost:8008/health

# Your new endpoints
curl http://localhost:8008/goodbye/Student
curl http://localhost:8008/status
curl http://localhost:8008/calculate/multiply/6/7
```

### Review Your Git History

```bash
# See all your commits
git log --oneline --graph --all

# See branch history
git log --oneline --graph --decorate --all
```

### Check GitHub Actions History

1. Go to **Actions** tab on GitHub
2. Review all pipeline runs
3. Notice:
   - Pull request pipelines (test only)
   - Main branch pipelines (test + deploy)

---

## Discussion Questions

Discuss with your instructor or group:

1. **Why use feature branches instead of committing directly to main?**
   - Keeps main branch stable
   - Allows parallel development
   - Enables code review process
   - Easy to rollback if needed

2. **Why did the pipeline run twice for each feature?**
   - Once on the pull request (test only)
   - Once after merge to main (test + deploy)

3. **What happens if a test fails in the pipeline?**
   - Merge is blocked automatically
   - Deployment doesn't happen
   - Developer must fix the issue

4. **Why write tests before merging?**
   - Prevents bugs from reaching production
   - Documents expected behavior
   - Enables confident refactoring
   - Catches regressions early

5. **What's the difference between CI and CD in this activity?**
   - CI: Automated testing on every change
   - CD: Automated deployment after tests pass

---

## Challenge Exercises (Optional)

If you finish early or want more practice:

### Challenge 1: Add Input Validation

Add a new endpoint `/greet/<name>` that:
- Returns error if name is empty
- Returns error if name is longer than 50 characters
- Returns error if name contains numbers
- Write tests for all cases

### Challenge 2: Add Environment Info

Add a new endpoint `/env` that returns:
- Operating system information
- Server hostname
- Current timestamp
- Memory usage
- Write comprehensive tests

### Challenge 3: Add a POST Endpoint

Convert the calculate endpoint to accept POST requests with JSON:
```json
{
  "operation": "add",
  "numbers": [1, 2, 3, 4, 5]
}
```
Returns the sum/product of all numbers.

### Challenge 4: Add Documentation Endpoint

Create `/api/docs` that returns:
- All available endpoints
- Expected parameters
- Response formats
- Example usage

---

## What You Learned

✅ **Git Workflow**
- Creating feature branches
- Committing with meaningful messages
- Pushing to remote repository
- Pulling changes from main

✅ **GitHub Collaboration**
- Creating pull requests
- Writing PR descriptions
- Code review process
- Merging strategies

✅ **CI/CD Pipeline**
- Automated testing on every change
- Pipeline execution stages
- Test job vs deploy job
- Branch-specific workflows

✅ **Testing**
- Writing unit tests
- Testing success cases
- Testing error cases
- Running tests locally

✅ **Professional Development**
- Test before commit
- Small, focused changes
- Descriptive documentation
- Iterative development

---

## Next Steps

After completing this activity, you can:

1. **Explore the README.md** - Detailed setup and usage instructions
2. **Read TUTORIAL.md** - Deep dive into CI/CD concepts
3. **Experiment with more features** - Try adding your own ideas
4. **Break things intentionally** - See how the pipeline catches errors
5. **Modify the workflow** - Edit `.github/workflows/ci-cd.yml`

---

## Troubleshooting

### Issue: "Branch already exists"

```bash
# Delete local branch
git branch -D feature/goodbye-endpoint

# Start fresh
git checkout -b feature/goodbye-endpoint
```

### Issue: "Tests failing locally"

```bash
# Check Python version
python --version

# Reinstall dependencies
pip install -r requirements.txt

# Run tests with verbose output
pytest test_app.py -vv
```

### Issue: "Can't push to GitHub"

```bash
# Check remote URL
git remote -v

# Re-authenticate if needed
git push origin feature/goodbye-endpoint
```

### Issue: "Merge conflicts"

```bash
# Update your feature branch with main
git checkout feature/your-feature
git pull origin main
# Resolve conflicts in editor
git add .
git commit -m "Resolve merge conflicts"
git push origin feature/your-feature
```

---

## Resources

- **Git Documentation:** https://git-scm.com/doc
- **GitHub Actions:** https://docs.github.com/en/actions
- **Flask Documentation:** https://flask.palletsprojects.com/
- **pytest Documentation:** https://docs.pytest.org/

---

## Assessment Checklist

After completing the activity, you should be able to:

- [ ] Create and switch between Git branches
- [ ] Write new Flask endpoints
- [ ] Write corresponding pytest tests
- [ ] Test code locally before pushing
- [ ] Create descriptive pull requests
- [ ] Interpret CI/CD pipeline results
- [ ] Merge pull requests successfully
- [ ] Understand when deployment occurs
- [ ] Sync local repository with remote
- [ ] Explain the complete workflow to others

**Total Endpoints Created:** 6
- `/hello/<name>` (original)
- `/health` (original)
- `/goodbye/<name>` (Part 1)
- `/status` (Part 2)
- `/calculate/<operation>/<num1>/<num2>` (Part 3)

**Total Tests Written:** 8

**Total Pull Requests:** 3

**Total Pipeline Executions:** 6 (3 PRs + 3 merges)

Congratulations on completing the activity! 🎉
