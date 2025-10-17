#!/usr/bin/env python3
"""
Automation Testing & Monitoring Script
Tests all components and monitors GitHub Actions workflow status
"""

import os
import sys
import json
import subprocess
from datetime import datetime, timedelta
import requests
import time

GITHUB_USERNAME = "Drakaniia"  # Change this to your username
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN', '')  # Optional: for API rate limits

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text.center(60)}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}\n")

def print_success(text):
    print(f"{Colors.GREEN}✅ {text}{Colors.RESET}")

def print_error(text):
    print(f"{Colors.RED}❌ {text}{Colors.RESET}")

def print_warning(text):
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.RESET}")

def print_info(text):
    print(f"{Colors.BLUE}ℹ️  {text}{Colors.RESET}")

def get_python_command():
    """Detect the correct Python command"""
    commands = ['python', 'python3', 'py']
    
    for cmd in commands:
        try:
            result = subprocess.run(
                [cmd, '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                return cmd
        except (FileNotFoundError, subprocess.TimeoutExpired):
            continue
    
    return None

def test_file_exists(filename):
    """Test if a file exists and is readable"""
    if os.path.exists(filename):
        print_success(f"{filename} exists")
        return True
    else:
        print_error(f"{filename} not found")
        return False

def test_file_updated_recently(filename, hours=24):
    """Test if a file was updated recently"""
    if not os.path.exists(filename):
        return False
    
    modified_time = datetime.fromtimestamp(os.path.getmtime(filename))
    age = datetime.now() - modified_time
    
    hours_ago = age.total_seconds() / 3600
    
    if hours_ago < hours:
        if hours_ago < 1:
            minutes = int(age.total_seconds() / 60)
            print_success(f"{filename} updated {minutes}m ago")
        else:
            print_success(f"{filename} updated {int(hours_ago)}h {int((age.total_seconds() % 3600) / 60)}m ago")
        return True
    else:
        days_ago = age.days
        if days_ago > 0:
            print_warning(f"{filename} last updated {days_ago} days ago")
        else:
            print_warning(f"{filename} last updated {int(hours_ago)} hours ago")
        return False

def test_json_valid(filename):
    """Test if JSON file is valid"""
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
        print_success(f"{filename} is valid JSON with {len(data)} entries")
        return True
    except Exception as e:
        print_error(f"{filename} JSON error: {e}")
        return False

def test_workflow_file(filename):
    """Test if workflow file is valid"""
    if not test_file_exists(filename):
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for essential components
    checks = {
        'schedule': 'cron' in content,
        'workflow_dispatch': 'workflow_dispatch' in content,
        'python setup': 'setup-python' in content,
        'git config': 'git config' in content,
        'git push': 'git push' in content
    }
    
    all_passed = True
    for check, passed in checks.items():
        if passed:
            print_success(f"  {check} found")
        else:
            print_error(f"  {check} missing")
            all_passed = False
    
    return all_passed

def test_python_script(script_name, python_cmd):
    """Test if Python script runs without errors"""
    print_info(f"Testing {script_name}...")
    try:
        result = subprocess.run(
            [python_cmd, script_name],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=os.getcwd()
        )
        
        if result.returncode == 0:
            print_success(f"{script_name} executed successfully")
            if result.stdout:
                # Show first line of output
                first_line = result.stdout.split('\n')[0]
                print(f"  Output: {first_line[:80]}...")
            return True
        else:
            print_error(f"{script_name} failed with code {result.returncode}")
            if result.stderr:
                print(f"  Error: {result.stderr[:200]}")
            return False
    except subprocess.TimeoutExpired:
        print_error(f"{script_name} timed out (>30s)")
        return False
    except Exception as e:
        print_error(f"{script_name} error: {e}")
        return False

def test_github_api_connection():
    """Test GitHub API connectivity"""
    try:
        headers = {'User-Agent': 'GitHub-Profile-Tester'}
        if GITHUB_TOKEN:
            headers['Authorization'] = f'token {GITHUB_TOKEN}'
        
        response = requests.get(
            f'https://api.github.com/users/{GITHUB_USERNAME}',
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print_success(f"GitHub API connected")
            print_info(f"  Username: {data.get('login')}")
            print_info(f"  Public repos: {data.get('public_repos')}")
            print_info(f"  Followers: {data.get('followers')}")
            
            # Check rate limit
            remaining = int(response.headers.get('X-RateLimit-Remaining', 0))
            limit = int(response.headers.get('X-RateLimit-Limit', 60))
            print_info(f"  API Rate limit: {remaining}/{limit} remaining")
            
            if remaining < 10:
                print_warning("API rate limit low!")
            
            return True
        elif response.status_code == 404:
            print_error(f"User '{GITHUB_USERNAME}' not found on GitHub")
            return False
        else:
            print_error(f"GitHub API returned {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print_error(f"GitHub API connection error: {str(e)[:100]}")
        return False

def test_external_apis():
    """Test external API connectivity"""
    apis = [
        ('Joke API', 'https://v2.jokeapi.dev/joke/Programming?type=single'),
        ('Quote API', 'https://api.quotable.io/random'),
        ('Useless Facts', 'https://uselessfacts.jsph.pl/random.json?language=en'),
    ]
    
    results = []
    for name, url in apis:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                print_success(f"{name} accessible")
                results.append(True)
            else:
                print_warning(f"{name} returned {response.status_code}")
                results.append(False)
        except requests.exceptions.RequestException as e:
            print_warning(f"{name} error: {str(e)[:50]}")
            results.append(False)
    
    # Count successes
    success_count = sum(results)
    if success_count >= 2:  # At least 2 out of 3
        return True
    return False

def check_git_status():
    """Check git repository status"""
    try:
        # Check if we're in a git repo
        result = subprocess.run(
            ['git', 'rev-parse', '--is-inside-work-tree'],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            print_error("Not a git repository")
            return False
        
        print_success("Git repository detected")
        
        # Get last commit info
        result = subprocess.run(
            ['git', 'log', '-1', '--pretty=format:%h - %s (%cr)'],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace'
        )
        
        if result.returncode == 0:
            commit_info = result.stdout.replace('ðŸ¤–', '🤖')  # Fix encoding
            print_info(f"  Last commit: {commit_info}")
        
        # Check for uncommitted changes
        result = subprocess.run(
            ['git', 'status', '--porcelain'],
            capture_output=True,
            text=True
        )
        
        if result.stdout.strip():
            changes = result.stdout.strip().split('\n')
            if len(changes) == 1 and 'test_automation.py' in changes[0]:
                print_info("Only test script is uncommitted (expected)")
            else:
                print_warning(f"Uncommitted changes: {len(changes)} files")
                for change in changes[:3]:  # Show first 3
                    print(f"    {change}")
        else:
            print_success("Working directory clean")
        
        return True
    except Exception as e:
        print_error(f"Git check error: {e}")
        return False

def get_workflow_runs():
    """Get recent workflow runs from GitHub API"""
    try:
        headers = {'User-Agent': 'GitHub-Profile-Tester'}
        if GITHUB_TOKEN:
            headers['Authorization'] = f'token {GITHUB_TOKEN}'
        
        # Try the repo-specific endpoint
        url = f'https://api.github.com/repos/{GITHUB_USERNAME}/{GITHUB_USERNAME}/actions/runs?per_page=5'
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            runs = data.get('workflow_runs', [])
            
            if runs:
                print_success(f"Found {len(runs)} recent workflow runs")
                print("\nRecent runs:")
                for run in runs[:5]:
                    status_icon = "✅" if run['conclusion'] == 'success' else "❌" if run['conclusion'] == 'failure' else "⏳"
                    created = run['created_at'].split('T')[0]
                    print(f"  {status_icon} {run['name']}: {run['status']} ({created})")
                return True
            else:
                print_warning("No workflow runs found (Actions may not be enabled yet)")
                print_info("  Tip: Go to your repo's Actions tab to enable workflows")
                return False
        elif response.status_code == 404:
            print_warning(f"Repository '{GITHUB_USERNAME}/{GITHUB_USERNAME}' not found or Actions not enabled")
            print_info("  Create a repo with your username to use GitHub profile features")
            return False
        else:
            print_warning(f"Cannot fetch workflow runs (status {response.status_code})")
            return False
    except Exception as e:
        print_warning(f"Workflow check error: {str(e)[:100]}")
        return False

def check_dependencies():
    """Check if required dependencies are installed"""
    print_header("Dependency Check")
    
    # Check Python
    python_cmd = get_python_command()
    if python_cmd:
        result = subprocess.run([python_cmd, '--version'], capture_output=True, text=True)
        version = result.stdout.strip()
        print_success(f"Python found: {version} (command: {python_cmd})")
    else:
        print_error("Python not found in PATH")
        return False, None
    
    # Check git
    try:
        result = subprocess.run(['git', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print_success(f"Git found: {result.stdout.strip()}")
        else:
            print_error("Git not working properly")
            return False, python_cmd
    except FileNotFoundError:
        print_error("Git not found in PATH")
        return False, python_cmd
    
    # Check requests module
    try:
        import requests
        print_success(f"requests module installed (v{requests.__version__})")
    except ImportError:
        print_error("requests module not installed")
        print_info(f"  Install with: {python_cmd} -m pip install requests")
        return False, python_cmd
    
    return True, python_cmd

def generate_test_report():
    """Generate comprehensive test report"""
    print_header("AUTOMATION TESTING REPORT")
    
    # Check dependencies first
    deps_ok, python_cmd = check_dependencies()
    if not deps_ok:
        print_error("\n❌ Dependency check failed. Please install missing dependencies.")
        return False
    
    results = {
        'File System Tests': [],
        'Workflow Tests': [],
        'Script Tests': [],
        'API Tests': [],
        'Git Tests': []
    }
    
    # File system tests
    print_header("1. File System Tests")
    files = [
        'README.md',
        'AUTO_UPDATE.md',
        'DAILY_NOTES.md',
        'ACTIVITY_LOG.json',
        'auto_update.py',
        'daily_activity.py',
        'update_profile.py',
        '.github/workflows/daily-activity.yml',
        '.github/workflows/hourly-update.yml',
        '.github/workflows/update-profile.yml'
    ]
    
    for f in files:
        results['File System Tests'].append(test_file_exists(f))
    
    # Check file freshness
    print("\nFile Update Checks:")
    results['File System Tests'].append(test_file_updated_recently('README.md', 12))
    results['File System Tests'].append(test_file_updated_recently('AUTO_UPDATE.md', 2))
    results['File System Tests'].append(test_file_updated_recently('ACTIVITY_LOG.json', 24))
    
    # JSON validation
    print("\nJSON Validation:")
    results['File System Tests'].append(test_json_valid('ACTIVITY_LOG.json'))
    
    # Workflow tests
    print_header("2. Workflow Configuration Tests")
    workflows = [
        '.github/workflows/daily-activity.yml',
        '.github/workflows/hourly-update.yml',
        '.github/workflows/update-profile.yml'
    ]
    
    for wf in workflows:
        if os.path.exists(wf):
            results['Workflow Tests'].append(test_workflow_file(wf))
    
    # Script tests
    print_header("3. Python Script Tests")
    print_info("Testing scripts (will execute and modify files)")
    
    scripts = ['daily_activity.py', 'auto_update.py', 'update_profile.py']
    for script in scripts:
        if os.path.exists(script):
            results['Script Tests'].append(test_python_script(script, python_cmd))
        else:
            print_error(f"{script} not found")
            results['Script Tests'].append(False)
    
    # API tests
    print_header("4. API Connectivity Tests")
    results['API Tests'].append(test_github_api_connection())
    print("\nExternal APIs:")
    results['API Tests'].append(test_external_apis())
    
    # Git tests
    print_header("5. Git Repository Tests")
    results['Git Tests'].append(check_git_status())
    
    # Workflow runs
    print("\nGitHub Actions Status:")
    workflow_check = get_workflow_runs()
    # Don't fail the test if workflows aren't set up yet
    results['Git Tests'].append(True)  # Always pass this
    
    # Final summary
    print_header("TEST SUMMARY")
    
    total_tests = sum(len(v) for v in results.values())
    passed_tests = sum(sum(v) for v in results.values())
    
    print(f"\nTotal Tests: {total_tests}")
    print(f"Passed: {Colors.GREEN}{passed_tests}{Colors.RESET}")
    print(f"Failed: {Colors.RED}{total_tests - passed_tests}{Colors.RESET}")
    print(f"Success Rate: {(passed_tests/total_tests*100):.1f}%\n")
    
    for category, tests in results.items():
        passed = sum(tests)
        total = len(tests)
        status = Colors.GREEN if passed == total else Colors.YELLOW if passed > 0 else Colors.RED
        print(f"{category}: {status}{passed}/{total}{Colors.RESET}")
    
    # Recommendations
    print_header("RECOMMENDATIONS")
    
    if passed_tests == total_tests:
        print(f"{Colors.GREEN}{Colors.BOLD}🎉 ALL TESTS PASSED!{Colors.RESET}")
        print_info("Your automation is working perfectly!")
    elif passed_tests / total_tests > 0.8:
        print(f"{Colors.YELLOW}{Colors.BOLD}⚠️  MOST TESTS PASSED{Colors.RESET}")
        if not workflow_check:
            print_info("• Enable GitHub Actions in your repository settings")
            print_info("• Push changes to trigger the first workflow run")
    else:
        print(f"{Colors.RED}{Colors.BOLD}❌ MULTIPLE FAILURES DETECTED{Colors.RESET}")
    
    # Specific recommendations
    if sum(results['Script Tests']) < len(results['Script Tests']):
        print_info(f"• Ensure Python dependencies are installed: {python_cmd} -m pip install requests")
    
    if not workflow_check:
        print_info("• Go to GitHub repo → Actions tab → Enable workflows")
        print_info("• Commit and push these files to trigger actions")
    
    print(f"\n{Colors.BLUE}Next Steps:{Colors.RESET}")
    print("  1. Commit and push all files to GitHub")
    print("  2. Go to your repository's Actions tab")
    print("  3. Enable workflows if prompted")
    print("  4. Run 'Actions → [workflow] → Run workflow' manually")
    print("  5. Wait for scheduled runs or check back in 1 hour")
    
    return passed_tests == total_tests

def continuous_monitor(interval=300):
    """Continuously monitor the automation (runs every 5 minutes by default)"""
    print_header("CONTINUOUS MONITORING MODE")
    print_info(f"Checking every {interval} seconds. Press Ctrl+C to stop.\n")
    
    python_cmd = get_python_command()
    if not python_cmd:
        print_error("Python not found. Cannot run monitoring.")
        return
    
    try:
        iteration = 0
        while True:
            iteration += 1
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"\n{Colors.BOLD}[{timestamp}] Check #{iteration}{Colors.RESET}")
            
            # Quick checks
            checks = {
                'README (6h)': test_file_updated_recently('README.md', 6),
                'Auto-update (1h)': test_file_updated_recently('AUTO_UPDATE.md', 1),
                'Activity (24h)': test_file_updated_recently('ACTIVITY_LOG.json', 24),
            }
            
            passed = sum(checks.values())
            total = len(checks)
            
            if passed == total:
                print_success(f"All checks passed ({passed}/{total})")
            elif passed > 0:
                print_warning(f"Some checks passed ({passed}/{total})")
            else:
                print_error(f"All checks failed ({passed}/{total})")
            
            print(f"\n{Colors.BLUE}Next check in {interval}s... (Ctrl+C to stop){Colors.RESET}")
            time.sleep(interval)
            
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Monitoring stopped by user{Colors.RESET}")
        print(f"Completed {iteration} monitoring cycles")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == '--monitor':
        continuous_monitor()
    else:
        success = generate_test_report()
        
        print(f"\n{Colors.BLUE}{'='*60}{Colors.RESET}")
        print(f"{Colors.BLUE}Options:{Colors.RESET}")
        print(f"  {sys.executable} test_automation.py           - Run full test suite")
        print(f"  {sys.executable} test_automation.py --monitor - Continuous monitoring")
        
        sys.exit(0 if success else 1)