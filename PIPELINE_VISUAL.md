# CI/CD Pipeline Visual Guide

## Overview Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    Developer Workflow                            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │  Write Code      │
                    │  app.py          │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │  Write Tests     │
                    │  test_app.py     │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │  Run Tests       │
                    │  pytest -v       │
                    └────────┬─────────┘
                             │
                    ┌────────┴─────────┐
                    │                  │
                ✅ Pass            ❌ Fail
                    │                  │
                    │                  └──► Fix Code ──┐
                    │                                   │
                    ▼                                   │
          ┌──────────────────┐                        │
          │  git add .       │◄───────────────────────┘
          │  git commit      │
          │  git push        │
          └────────┬─────────┘
                   │
                   ▼
┌────────────────────────────────────────────────────────────────┐
│                    GitHub Actions Pipeline                      │
└────────────────────────────────────────────────────────────────┘
                   │
                   ▼
       ┌───────────────────────┐
       │  Trigger Detected     │
       │  - Push to main       │
       │  - Pull Request       │
       └───────────┬───────────┘
                   │
                   ▼
       ┌───────────────────────┐
       │  Provision Runner     │
       │  Ubuntu VM            │
       └───────────┬───────────┘
                   │
                   ▼
┌──────────────────────────────────────────────────────────────┐
│                      TEST JOB (CI)                           │
└──────────────────────────────────────────────────────────────┘
                   │
                   ▼
       ┌───────────────────────┐
       │  Step 1: Checkout     │
       │  actions/checkout@v3  │
       │  ⏱ 5-10 seconds       │
       └───────────┬───────────┘
                   │
                   ▼
       ┌───────────────────────┐
       │  Step 2: Setup Python │
       │  Python 3.9           │
       │  ⏱ 10-15 seconds      │
       └───────────┬───────────┘
                   │
                   ▼
       ┌───────────────────────┐
       │  Step 3: Install Deps │
       │  pip install          │
       │  ⏱ 15-20 seconds      │
       └───────────┬───────────┘
                   │
                   ▼
       ┌───────────────────────┐
       │  Step 4: Run Tests    │
       │  pytest -v            │
       │  ⏱ 5-10 seconds       │
       └───────────┬───────────┘
                   │
          ┌────────┴─────────┐
          │                  │
      ✅ Pass            ❌ Fail
          │                  │
          │                  ▼
          │         ┌─────────────────┐
          │         │  Stop Pipeline  │
          │         │  Notify Dev     │
          │         │  Red ❌         │
          │         └─────────────────┘
          │
          ▼
  ┌──────────────────┐
  │  Check Branch    │
  │  Is it main?     │
  └────────┬─────────┘
           │
  ┌────────┴─────────┐
  │                  │
main              Other
  │                  │
  │                  └──► Stop (PR check only)
  │
  ▼
┌──────────────────────────────────────────────────────────────┐
│                    DEPLOY JOB (CD)                           │
└──────────────────────────────────────────────────────────────┘
  │
  ▼
┌───────────────────────┐
│  Deploy to Staging    │
│  ⏱ 5-10 seconds       │
└───────────┬───────────┘
            │
            ▼
  ┌─────────────────────┐
  │  ✅ Success!        │
  │  Green Checkmark    │
  │  Notify Team        │
  └─────────────────────┘
```

## Detailed Step Breakdown

### Phase 1: Local Development (Your Computer)

```
┌─────────────────────────────────────────────────────┐
│  YOU (Developer)                                     │
├─────────────────────────────────────────────────────┤
│  1. Edit app.py                                      │
│     - Add new endpoint                               │
│     - Modify existing code                           │
│                                                      │
│  2. Edit test_app.py                                │
│     - Add corresponding tests                        │
│     - Ensure good coverage                           │
│                                                      │
│  3. Test Locally                                     │
│     $ pytest test_app.py -v                         │
│     ✅ All tests pass                               │
│                                                      │
│  4. Manual Testing                                   │
│     $ python3 app.py                                │
│     $ curl http://localhost:8008/hello/Test         │
│     ✅ Works as expected                            │
│                                                      │
│  5. Commit Changes                                   │
│     $ git add app.py test_app.py                    │
│     $ git commit -m "feat: Add new endpoint"        │
│                                                      │
│  6. Push to GitHub                                   │
│     $ git push origin main                          │
│     🚀 Triggers CI/CD pipeline!                     │
└─────────────────────────────────────────────────────┘
```

### Phase 2: GitHub Receives Push

```
┌─────────────────────────────────────────────────────┐
│  GITHUB (git push received)                          │
├─────────────────────────────────────────────────────┤
│  1. Receive commit                                   │
│     - Commit hash: abc123def                         │
│     - Branch: main                                   │
│     - Author: You                                    │
│                                                      │
│  2. Check for workflows                              │
│     - Scan .github/workflows/                        │
│     - Find ci-cd.yml                                 │
│                                                      │
│  3. Check triggers                                   │
│     on:                                              │
│       push:                                          │
│         branches: [main]  ✅ Match!                 │
│                                                      │
│  4. Queue workflow                                   │
│     - Create workflow run                            │
│     - Assign run ID: #42                             │
│     - Status: Queued 🟡                             │
└─────────────────────────────────────────────────────┘
```

### Phase 3: Runner Provisioning

```
┌─────────────────────────────────────────────────────┐
│  GITHUB ACTIONS (Infrastructure)                     │
├─────────────────────────────────────────────────────┤
│  1. Provision Virtual Machine                        │
│     - OS: Ubuntu 22.04 LTS                           │
│     - CPU: 2 cores                                   │
│     - RAM: 7 GB                                      │
│     - Disk: 14 GB SSD                                │
│     ⏱ ~30 seconds                                    │
│                                                      │
│  2. Install Base Tools                               │
│     - Git                                            │
│     - Docker                                         │
│     - curl, wget                                     │
│     - Build essentials                               │
│                                                      │
│  3. Start Runner                                     │
│     - Connect to GitHub                              │
│     - Status: Running 🟡                            │
│     - Ready to execute jobs                          │
└─────────────────────────────────────────────────────┘
```

### Phase 4: Test Job Execution (CI)

```
┌─────────────────────────────────────────────────────┐
│  JOB: test (runs-on: ubuntu-latest)                  │
├─────────────────────────────────────────────────────┤
│                                                      │
│  ▶ STEP 1: Checkout code                            │
│  ├─ Action: actions/checkout@v3                     │
│  ├─ What: Clone repository                          │
│  ├─ Command: git clone + checkout abc123            │
│  ├─ Duration: ~5-10 seconds                         │
│  └─ Result: ✅ Code downloaded                      │
│                                                      │
│  ▶ STEP 2: Set up Python                            │
│  ├─ Action: actions/setup-python@v4                 │
│  ├─ Version: 3.9                                    │
│  ├─ What: Install Python + pip                      │
│  ├─ Cache: Check for cached Python                  │
│  ├─ Duration: ~10-15 seconds                        │
│  └─ Result: ✅ Python 3.9.18 ready                  │
│                                                      │
│  ▶ STEP 3: Install dependencies                     │
│  ├─ Command: pip install flask pytest               │
│  ├─ What:                                            │
│  │   - Download packages from PyPI                  │
│  │   - Install Flask 3.0.0                          │
│  │   - Install pytest 7.4.3                         │
│  │   - Install their dependencies                   │
│  ├─ Duration: ~15-20 seconds                        │
│  └─ Result: ✅ Dependencies installed               │
│                                                      │
│  ▶ STEP 4: Run tests                                │
│  ├─ Command: pytest test_app.py -v                  │
│  ├─ What: Execute all test functions                │
│  ├─ Tests:                                           │
│  │   ✅ test_hello_endpoint                         │
│  │   ✅ test_health_endpoint                        │
│  ├─ Duration: ~5-10 seconds                         │
│  └─ Result: ✅ 2 passed in 0.25s                    │
│                                                      │
│  📊 JOB SUMMARY                                      │
│  ├─ Total time: ~40-55 seconds                      │
│  ├─ Status: ✅ Success                              │
│  └─ Next: Proceed to deploy job                     │
└─────────────────────────────────────────────────────┘
```

### Phase 5: Deploy Job Execution (CD)

```
┌─────────────────────────────────────────────────────┐
│  JOB: deploy_staging                                 │
│  (needs: test, if: github.ref == 'refs/heads/main') │
├─────────────────────────────────────────────────────┤
│                                                      │
│  ⚙️ PRE-CHECK CONDITIONS                             │
│  ├─ needs: test → ✅ Test job passed                │
│  ├─ if: main branch → ✅ Is main branch             │
│  └─ Decision: ✅ Run this job                       │
│                                                      │
│  ▶ STEP: Deploy to staging                          │
│  ├─ Command: echo "Deploying..."                    │
│  ├─ In real world, this would:                      │
│  │   • SSH to server                                │
│  │   • Pull latest code                             │
│  │   • Restart services                             │
│  │   • Run migrations                               │
│  │   • Health check                                 │
│  ├─ Duration: ~5-10 seconds                         │
│  └─ Result: ✅ Deployed                             │
│                                                      │
│  📊 JOB SUMMARY                                      │
│  ├─ Total time: ~10-15 seconds                      │
│  ├─ Status: ✅ Success                              │
│  └─ Environment: Staging is live!                   │
└─────────────────────────────────────────────────────┘
```

### Phase 6: Completion & Notification

```
┌─────────────────────────────────────────────────────┐
│  WORKFLOW COMPLETE                                   │
├─────────────────────────────────────────────────────┤
│                                                      │
│  📊 SUMMARY                                          │
│  ├─ Workflow: CI/CD Pipeline                        │
│  ├─ Run ID: #42                                     │
│  ├─ Trigger: Push to main                           │
│  ├─ Commit: abc123def                               │
│  ├─ Author: You                                     │
│  └─ Branch: main                                    │
│                                                      │
│  ✅ JOBS                                             │
│  ├─ test: Success (45s)                             │
│  └─ deploy_staging: Success (12s)                   │
│                                                      │
│  ⏱ TOTAL TIME                                        │
│  └─ 1 minute 2 seconds                              │
│                                                      │
│  📧 NOTIFICATIONS                                    │
│  ├─ ✅ Commit marked as passed                      │
│  ├─ 📧 Email sent to you                            │
│  ├─ 🔔 GitHub notification                          │
│  └─ 📊 Badge updated (if exists)                    │
│                                                      │
│  🔗 LINKS                                            │
│  ├─ View run: /actions/runs/42                      │
│  ├─ View logs: /actions/runs/42/logs                │
│  └─ Re-run: Available if needed                     │
└─────────────────────────────────────────────────────┘
```

## Timeline Visualization

```
Minute:Second    Event                           Status
─────────────    ─────                           ──────
00:00            Push code to GitHub             ⚡
00:01            GitHub receives push            📥
00:02            Workflow queued                 🟡
00:05            Runner provisioned              🟡
00:10            Checkout code (Step 1)          🟡
00:15            Setup Python (Step 2)           🟡
00:25            Install dependencies (Step 3)   🟡
00:40            Run tests (Step 4)              🟡
00:45            Tests complete                  ✅
00:46            Test job marked success         ✅
00:47            Check deploy conditions         ⚙️
00:48            Start deploy job                🟡
00:50            Deploy to staging               🟡
00:55            Deployment complete             ✅
00:57            Cleanup runner                  🧹
01:00            Workflow complete               ✅
01:01            Notifications sent              📧
```

## Conditional Flow

### Pull Request vs Main Branch Push

```
              ┌─────────────────┐
              │  Code Pushed    │
              └────────┬────────┘
                       │
              ┌────────▼────────┐
              │  Run Test Job   │
              └────────┬────────┘
                       │
              ┌────────▼────────┐
              │  Tests Pass?    │
              └────────┬────────┘
                       │
         ┌─────────────┴─────────────┐
         │                           │
     ✅ Pass                      ❌ Fail
         │                           │
         ▼                           ▼
┌────────────────┐          ┌──────────────┐
│  Check Branch  │          │  Stop & Fail │
└───────┬────────┘          │  Notify Dev  │
        │                   └──────────────┘
   ┌────┴────┐
   │         │
  main     other
   │         │
   ▼         ▼
┌──────┐  ┌──────────────┐
│Deploy│  │ Stop Here    │
│Job   │  │ (PR check    │
│Runs  │  │  only)       │
└──────┘  └──────────────┘
```

## What Gets Logged

### GitHub Actions UI Shows:

```
┌─────────────────────────────────────────────┐
│  Workflow Run #42                           │
├─────────────────────────────────────────────┤
│  ✅ CI/CD Pipeline                          │
│  on: push                                   │
│  abc123 feat: Add new endpoint              │
│  by: You                                    │
│  1m 2s ago                                  │
├─────────────────────────────────────────────┤
│  Jobs:                                      │
│  ✅ test (45s)                              │
│  ✅ deploy_staging (12s)                    │
├─────────────────────────────────────────────┤
│  Annotations:                               │
│  ✅ All checks have passed                  │
└─────────────────────────────────────────────┘

Click job for detailed logs:
┌─────────────────────────────────────────────┐
│  test                                        │
├─────────────────────────────────────────────┤
│  ▶ Set up job (2s)                          │
│  ▶ Checkout code (5s)                       │
│    │ git clone...                           │
│    │ Checked out abc123                     │
│    └─ ✅ Complete                           │
│  ▶ Set up Python (10s)                      │
│    │ Downloading Python 3.9.18...           │
│    │ Successfully set up Python             │
│    └─ ✅ Complete                           │
│  ▶ Install dependencies (18s)               │
│    │ pip install flask pytest               │
│    │ Successfully installed flask-3.0.0     │
│    │ Successfully installed pytest-7.4.3    │
│    └─ ✅ Complete                           │
│  ▶ Run tests (10s)                          │
│    │ ============ test session starts ===== │
│    │ test_app.py::test_hello PASSED [ 50%] │
│    │ test_app.py::test_health PASSED [100%]│
│    │ ========== 2 passed in 0.25s ========= │
│    └─ ✅ Complete                           │
│  ▶ Post Checkout code (1s)                 │
│  ▶ Complete job (0s)                        │
└─────────────────────────────────────────────┘
```

## Error Scenarios

### Scenario 1: Test Failure

```
Push Code → Trigger Pipeline → Run Tests → ❌ FAIL
                                              │
                                              ▼
                                    ┌──────────────────┐
                                    │  Pipeline Stops  │
                                    │  No Deployment   │
                                    ├──────────────────┤
                                    │  Notifications:  │
                                    │  • Red X on      │
                                    │    commit        │
                                    │  • Email sent    │
                                    │  • Log details   │
                                    │    available     │
                                    └──────────────────┘
```

### Scenario 2: Syntax Error

```
Push Code → Trigger Pipeline → Checkout → Install → Run Tests
                                                      │
                                                      ▼
                                            ❌ Import Error
                                            ModuleNotFoundError
                                                      │
                                                      ▼
                                            Pipeline Fails
                                            Check YAML syntax
```

---

**This visual guide complements the full [TUTORIAL.md](TUTORIAL.md)**
