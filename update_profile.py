#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub Profile Auto-Updater
Dynamically updates your profile README with live stats, activities, and content
"""

import requests
import random
from datetime import datetime
import sys
import io
import os

# Force UTF-8 encoding for all I/O operations
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    os.environ['PYTHONIOENCODING'] = 'utf-8'

# Configuration - Set your GitHub username
GITHUB_USERNAME = "Drakaniia"  # Change this

def get_programming_joke():
    """Fetch a programming joke"""
    try:
        response = requests.get('https://v2.jokeapi.dev/joke/Programming?type=single', timeout=10)
        if response.status_code == 200:
            data = response.json()
            joke = data.get('joke', 'Why do programmers prefer dark mode? Less bugs!')
            # Remove problematic characters
            return joke.encode('ascii', 'ignore').decode('ascii')
    except:
        pass
    return "Debugging is like being the detective in a crime movie where you're also the murderer at the same time."

def get_dev_quote():
    """Fetch a developer quote"""
    try:
        response = requests.get('https://api.quotable.io/random?tags=technology', timeout=10)
        if response.status_code == 200:
            data = response.json()
            quote = f'"{data["content"]}" - {data["author"]}'
            return quote.encode('ascii', 'ignore').decode('ascii')
    except:
        pass
    return '"Code is like humor. When you have to explain it, it\'s bad." - Cory House'

def get_github_stats():
    """Fetch real GitHub stats"""
    try:
        response = requests.get(f'https://api.github.com/users/{GITHUB_USERNAME}', timeout=10)
        if response.status_code == 200:
            data = response.json()
            return {
                'public_repos': data.get('public_repos', 0),
                'followers': data.get('followers', 0),
                'following': data.get('following', 0),
                'created_at': data.get('created_at', ''),
                'bio': data.get('bio', 'Building cool stuff!'),
                'location': data.get('location', 'None')
            }
    except:
        pass
    return None

def get_latest_repos():
    """Fetch latest repositories"""
    try:
        response = requests.get(
            f'https://api.github.com/users/{GITHUB_USERNAME}/repos?sort=updated&per_page=5',
            timeout=10
        )
        if response.status_code == 200:
            repos = response.json()
            return [{
                'name': repo['name'],
                'description': repo['description'] or 'No description',
                'stars': repo['stargazers_count'],
                'language': repo['language'] or 'Unknown',
                'url': repo['html_url']
            } for repo in repos[:3]]  # Limit to top 3
    except:
        pass
    return []

def get_contribution_streak():
    """Calculate contribution streak (simulated)"""
    today = datetime.now()
    streak_days = random.randint(7, 365)
    return {
        'current_streak': streak_days,
        'longest_streak': max(streak_days, random.randint(30, 500)),
        'total_contributions': random.randint(100, 2000)
    }

def generate_activity_graph():
    """Generate ASCII activity graph"""
    # Use simpler characters that work across platforms
    levels = ['_', '+', '*', '#', '@']
    weeks = 12
    graph = ""
    
    for week in range(weeks):
        week_str = ""
        for day in range(7):
            intensity = random.choice(levels)
            week_str += intensity
        graph += week_str + "\n    "
    
    return graph.strip()

def get_tech_stack():
    """Return dynamic tech stack with progress bars"""
    techs = [
        ("Python", random.randint(70, 95)),
        ("JavaScript", random.randint(60, 90)),
        ("React", random.randint(50, 85)),
        ("Node.js", random.randint(55, 88)),
        ("Docker", random.randint(45, 80)),
        ("Git", random.randint(75, 95)),
    ]
    
    result = ""
    for tech, level in techs:
        bar_length = 20
        filled = int((level / 100) * bar_length)
        bar = "#" * filled + "-" * (bar_length - filled)
        result += f"{tech:<15} {bar} {level}%\n"
    
    return result

def generate_profile_readme():
    """Generate the complete profile README"""
    now = datetime.now()
    stats = get_github_stats()
    repos = get_latest_repos()
    streak = get_contribution_streak()
    joke = get_programming_joke()
    quote = get_dev_quote()
    activity = generate_activity_graph()
    tech_stack = get_tech_stack()
    
    bio = stats['bio'] if stats else 'Building cool stuff!'
    location = stats['location'] if stats else 'None'
    
    content = f"""# Hi there, I'm {GITHUB_USERNAME}!

<div align="center">

![Profile Views](https://komarev.com/ghpvc/?username={GITHUB_USERNAME}&color=blueviolet&style=flat-square)
![GitHub followers](https://img.shields.io/github/followers/{GITHUB_USERNAME}?style=social)
![GitHub stars](https://img.shields.io/github/stars/{GITHUB_USERNAME}?style=social)

</div>

## About Me

{bio} | Location: {location}

- Currently working on making GitHub profiles more dynamic
- Learning new technologies every day
- Ask me about coding, automation, and tech
- Fun fact: This README updates automatically!

## GitHub Stats

<div align="center">

### Current Streak: **{streak['current_streak']} days**
### Longest Streak: **{streak['longest_streak']} days**
### Total Contributions: **{streak['total_contributions']}**

</div>

## Contribution Activity

```
{activity}
```

## Tech Stack & Skills

```
{tech_stack}```

## Latest Projects
"""

    if repos:
        for repo in repos:
            # Truncate long descriptions and clean them
            desc = repo['description'][:100]
            if len(repo['description']) > 100:
                desc += "..."
            # Remove problematic characters
            desc = desc.encode('ascii', 'ignore').decode('ascii')
            
            content += f"""
### [{repo['name']}]({repo['url']})
> {desc}
- Stars: {repo['stars']} | Language: {repo['language']}
"""
    else:
        content += "\n*Loading repositories...*\n"

    content += f"""

## Connect With Me

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/{GITHUB_USERNAME})
[![Twitter](https://img.shields.io/badge/Twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white)](https://twitter.com/{GITHUB_USERNAME})
[![Email](https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:{GITHUB_USERNAME}@example.com)

## Quote of the Day

> {quote}

## Dev Humor

{joke}

---

<div align="center">

### Last Updated: {now.strftime('%B %d, %Y at %H:%M UTC')}

**This profile updates automatically every 6 hours!**

![Wave](https://raw.githubusercontent.com/mayhemantt/mayhemantt/Update/svg/Bottom.svg)

</div>

<!-- 
Auto-generated by GitHub Actions
Commit #{random.randint(1000, 9999)}
-->
"""

    return content

if __name__ == "__main__":
    try:
        print(f"Generating profile README for @{GITHUB_USERNAME}...")
        
        content = generate_profile_readme()
        
        # Write with UTF-8 encoding
        with open('README.md', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("Profile README generated successfully!")
        print("\n" + "="*60)
        print(content[:500] + "...")
        print("="*60)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)