#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Daily Commit Activity Bot
Creates meaningful commits throughout the day to maintain activity
"""

import random
from datetime import datetime
import json
import sys
import io
import os

# Force UTF-8 encoding for all I/O operations
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    # Set environment variable for subprocess UTF-8
    os.environ['PYTHONIOENCODING'] = 'utf-8'

def get_commit_message():
    """Generate meaningful commit messages"""
    activities = [
        "Update documentation",
        "Fix minor bug",
        "Add new feature idea",
        "Improve code structure",
        "Performance optimization",
        "Update configuration",
        "Update dependencies",
        "Deploy new version",
        "Security update",
        "Refactor code",
        "Release new version",
        "Update UI components",
        "Add internationalization",
        "Improve mobile responsiveness",
        "Improve SEO",
        "Add tests",
        "Add analytics",
        "Update build scripts",
        "Fix CI build",
        "Improve targeting"
    ]
    
    details = [
        "for better user experience",
        "based on user feedback",
        "to improve maintainability",
        "following best practices",
        "for production readiness",
        "with latest standards",
        "improving code quality",
        "enhancing performance",
        "fixing edge cases",
        "optimizing workflow"
    ]
    
    # Use simple emoji alternatives that work cross-platform
    emojis = {
        "documentation": "📝",
        "bug": "🐛",
        "feature": "✨",
        "structure": "🎨",
        "performance": "⚡",
        "config": "🔧",
        "deps": "📦",
        "deploy": "🚀",
        "security": "🔒",
        "refactor": "♻️",
        "release": "🎉",
        "ui": "💄",
        "i18n": "🌐",
        "mobile": "📱",
        "seo": "🔍",
        "test": "🧪",
        "analytics": "📊",
        "build": "🔨",
        "ci": "💚",
        "target": "🎯"
    }
    
    activity = random.choice(activities)
    detail = random.choice(details)
    
    # Try to add emoji, fallback to plain text if it fails
    try:
        emoji_key = activity.split()[0].lower()
        for key in emojis:
            if key in emoji_key:
                return f"{emojis[key]} {activity} {detail}"
    except:
        pass
    
    return f"{activity} {detail}"

def create_activity_log():
    """Create an activity log entry"""
    now = datetime.now()
    
    log_entry = {
        "timestamp": now.isoformat(),
        "activity_type": random.choice(["code", "review", "planning", "documentation"]),
        "description": get_commit_message(),
        "energy_level": random.randint(60, 100),
        "focus_score": random.randint(70, 100)
    }
    
    return log_entry

def update_activity_file():
    """Update the activity tracking file"""
    log_entry = create_activity_log()
    
    # Read existing logs
    try:
        with open('ACTIVITY_LOG.json', 'r', encoding='utf-8') as f:
            logs = json.load(f)
    except:
        logs = []
    
    # Add new entry
    logs.append(log_entry)
    
    # Keep only last 100 entries
    logs = logs[-100:]
    
    # Write back with UTF-8 encoding
    with open('ACTIVITY_LOG.json', 'w', encoding='utf-8') as f:
        json.dump(logs, f, indent=2, ensure_ascii=False)
    
    return log_entry

def update_daily_notes():
    """Update daily development notes"""
    now = datetime.now()
    
    tips = [
        "Remember to write clean, readable code",
        "Don't forget to test edge cases",
        "Code reviews make better developers",
        "Documentation is future you's best friend",
        "Small commits are better than big ones",
        "Always consider security implications",
        "Performance matters, but readability first",
        "Learn something new every day",
        "Collaboration beats solo coding",
        "Take breaks to avoid burnout"
    ]
    
    notes = f"""# Daily Development Notes

## {now.strftime('%A, %B %d, %Y')}

### Tip of the Day
{random.choice(tips)}

### Today's Progress
- Automated profile updates
- Maintained commit streak
- Improved code quality
- Learned new techniques

### Focus Areas
- Code optimization
- Better documentation
- Test coverage
- User experience

### Productivity Score
**{random.randint(75, 95)}%** - Great work! Keep it up!

---
*Last updated: {now.strftime('%H:%M:%S UTC')}*
"""
    
    # Write with UTF-8 encoding
    with open('DAILY_NOTES.md', 'w', encoding='utf-8') as f:
        f.write(notes)

if __name__ == "__main__":
    try:
        print("Creating daily activity...")
        
        # Update activity log
        entry = update_activity_file()
        print(f"Activity logged: {entry['description']}")
        
        # Update daily notes
        update_daily_notes()
        print("Daily notes updated!")
        
        print("\nAll files updated successfully!")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)