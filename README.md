# CI/CD Pipeline Demo

A practical example of implementing a CI/CD pipeline using GitHub Actions with a simple Flask web application.

## About This Project

This project demonstrates the core concepts of Continuous Integration and Continuous Deployment (CI/CD) using:
- **Flask**: A lightweight Python web framework
- **pytest**: For automated testing
- **GitHub Actions**: For CI/CD automation

## Project Structure

```
cicd-pipeline-demo/
├── app.py                      # Main Flask application
├── test_app.py                 # Automated tests
├── requirements.txt            # Python dependencies
├── .github/
│   └── workflows/
│       └── ci-cd.yml          # GitHub Actions pipeline configuration
└── README.md                   # This file
```

## The Application

The application provides two simple endpoints:

- `GET /hello/<name>` - Returns a personalized greeting
- `GET /health` - Health check endpoint for monitoring

## Running Locally

### Prerequisites
- Python 3.9 or higher
- pip (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/datatweets/cicd-pipeline-demo.git
cd cicd-pipeline-demo
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

The application will be available at `http://localhost:8008`

### Testing the Endpoints

Try these URLs in your browser or using curl:

```bash
# Test the greeting endpoint
curl http://localhost:8008/hello/World

# Test the health check
curl http://localhost:8008/health
```

## Running Tests

Run the automated tests locally:

```bash
pytest test_app.py -v
```

Expected output:
```
test_app.py::test_hello_endpoint PASSED
test_app.py::test_health_endpoint PASSED
```

## CI/CD Pipeline

The pipeline automatically runs when:
- Code is pushed to the `main` branch
- A pull request is created targeting `main`

### Pipeline Stages

1. **Test Job** (Continuous Integration)
   - Checks out the code
   - Sets up Python 3.9
   - Installs dependencies
   - Runs automated tests

2. **Deploy Staging Job** (Continuous Deployment)
   - Only runs if tests pass
   - Only runs on `main` branch
   - Simulates deployment to staging environment

### Viewing Pipeline Results

1. Go to your repository on GitHub
2. Click the "Actions" tab
3. Select a workflow run to see detailed logs

✅ Green checkmark = Success
❌ Red X = Failure

## How It Works

### The CI/CD Workflow

```
Developer pushes code
         ↓
GitHub Actions triggered
         ↓
    Test Job runs
    - Install dependencies
    - Run tests
         ↓
    Tests Pass? ───No──→ Pipeline fails, notify developer
         ↓
        Yes
         ↓
   On main branch?
         ↓
        Yes
         ↓
Deploy to Staging
```

## Security Best Practices

⚠️ **Important Security Notes:**

- Never commit credentials or secrets to your code
- Use GitHub Secrets for sensitive information
- Use secure protocols (SSH, HTTPS) for deployment
- Implement proper access controls
- Rotate credentials regularly

## Next Steps

To extend this project:

1. **Add More Tests**: Increase test coverage
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
