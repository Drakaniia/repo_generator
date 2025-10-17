#!/usr/bin/env python3
"""
Self-Updating Repository Bot
Fetches random ASCII art, jokes, and fun content from APIs
"""

import random
import requests
from datetime import datetime
import time

def get_programming_joke():
    """Fetch a programming joke from API"""
    try:
        response = requests.get('https://official-joke-api.appspot.com/jokes/programming/random', timeout=10)
        if response.status_code == 200:
            joke_data = response.json()[0]
            return f"{joke_data['setup']} {joke_data['punchline']} 😄"
    except:
        pass
    
    # Fallback to JokeAPI
    try:
        response = requests.get('https://v2.jokeapi.dev/joke/Programming?type=single', timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('type') == 'single':
                return data['joke']
            else:
                return f"{data.get('setup', '')} {data.get('delivery', '')}"
    except:
        pass
    
    return "Why do programmers prefer dark mode? Because light attracts bugs! 🐛"

def get_ascii_art():
    """Fetch ASCII art from API"""
    ascii_options = [
        ('cat', 'https://catfact.ninja/fact'),
        ('dog', 'https://dog-api.kinduff.com/api/facts'),
        ('random', 'https://uselessfacts.jsph.pl/random.json?language=en')
    ]
    
    # Simple ASCII art patterns
    arts = [
        """
    ╔══════════════════════════════╗
    ║   AUTOMATIC UPDATE TIME!     ║
    ╚══════════════════════════════╝
        """,
        """
       /\\_/\\  
      ( o.o ) 
       > ^ <  Auto-commit cat!
        """,
        """
      ___
     {o,o}
     |)__)
     -"-"-  
    Wise owl commits!
        """,
        """
    ┌─┐
    ┴─┴
    ಠ_ರೃ  Indeed.
        """,
        """
       ___
      /   \\
     | O O |  Beep boop!
      \\___/
       |||
        """,
        """
    ☕ ✨ 🚀
    Coffee → Code → Commits
        """,
        """
      .-.
     (o o)
     | O |   Hello there!
      `---'
        """
    ]
    
    return random.choice(arts)

def get_random_fact():
    """Fetch a random interesting fact"""
    try:
        response = requests.get('https://uselessfacts.jsph.pl/random.json?language=en', timeout=10)
        if response.status_code == 200:
            return response.json().get('text', '')
    except:
        pass
    
    return None

def get_quote():
    """Fetch an inspirational quote"""
    try:
        response = requests.get('https://zenquotes.io/api/random', timeout=10)
        if response.status_code == 200:
            data = response.json()[0]
            return f'"{data["q"]}" - {data["a"]}'
    except:
        pass
    
    # Fallback API
    try:
        response = requests.get('https://api.quotable.io/random?tags=technology', timeout=10)
        if response.status_code == 200:
            data = response.json()
            return f'"{data["content"]}" - {data["author"]}'
    except:
        pass
    
    return None

def get_activity_emoji():
    """Fetch a random activity/emoji suggestion"""
    try:
        response = requests.get('https://www.boredapi.com/api/activity', timeout=10)
        if response.status_code == 200:
            data = response.json()
            return f"{data['activity']} (Type: {data['type']})"
    except:
        pass
    
    return None

CHANGELOG_ENTRIES = [
    "🎨 Improved the artistic quality of absolutely nothing",
    "🔧 Fixed a bug that didn't exist",
    "⚡ Made the code 0% faster",
    "🎉 Celebrated another successful automated commit",
    "🌟 Added some sparkle to the repository",
    "🤖 Taught the bot to love",
    "🎭 Performed routine theatrical maintenance",
    "🎪 Circus is in town - committed some fun!",
    "🎸 Rocked out with some fresh commits",
    "🧙‍♂️ Cast a spell of continuous integration",
    "🏆 Achieved nothing, but did it automatically",
    "🌈 Added more colors to the commit history",
    "🎲 Rolled the dice on this commit",
    "🍕 Pizza-flavored update deployed",
    "🦄 Unicorns approved this commit",
    "🎯 Hit the bullseye of meaningless updates",
    "🚀 Launched into the void of automation",
    "🎬 Directed another blockbuster commit",
    "🎨 Painted the town with git commits"
]

def generate_content():
    """Generate random content for the commit"""
    content = []
    
    # Add timestamp
    now = datetime.now()
    content.append(f"# 🤖 Auto-Update Log\n")
    content.append(f"**Update Time:** {now.strftime('%Y-%m-%d %H:%M:%S UTC')}\n")
    content.append(f"**Commit Number:** #{random.randint(1000, 9999)}\n\n")
    
    # Add random ASCII art
    content.append("## 🎨 ASCII Art of the Hour\n")
    ascii_art = get_ascii_art()
    content.append(f"```\n{ascii_art}\n```\n\n")
    
    # Add random joke
    content.append("## 😄 Programming Joke\n")
    joke = get_programming_joke()
    content.append(f"{joke}\n\n")
    
    # Add random quote
    quote = get_quote()
    if quote:
        content.append("## 💭 Inspirational Quote\n")
        content.append(f"{quote}\n\n")
    
    # Add random fact
    fact = get_random_fact()
    if fact:
        content.append("## 🧠 Random Fact\n")
        content.append(f"{fact}\n\n")
    
    # Add random activity suggestion
    activity = get_activity_emoji()
    if activity:
        content.append("## 🎯 Suggested Activity\n")
        content.append(f"Why not try: {activity}\n\n")
    
    # Add random changelog
    content.append("## 📝 What's New?\n")
    for _ in range(random.randint(2, 4)):
        content.append(f"- {random.choice(CHANGELOG_ENTRIES)}\n")
    
    # Add fun stats
    content.append(f"\n## 📊 Fun Stats\n")
    content.append(f"- 🎯 Productivity: {random.randint(0, 100)}%\n")
    content.append(f"- ☕ Coffee consumed: {random.randint(1, 10)} cups\n")
    content.append(f"- 🐛 Bugs created: {random.randint(0, 5)}\n")
    content.append(f"- 🎉 Fun level: {random.randint(80, 100)}%\n")
    content.append(f"- 🔥 Commit streak: {random.randint(1, 365)} days\n")
    
    # Add footer
    content.append(f"\n---\n")
    content.append(f"*Generated automatically by GitHub Actions* ⚡\n")
    
    return ''.join(content)

if __name__ == "__main__":
    print("🚀 Fetching fresh content from APIs...")
    
    # Generate content
    content = generate_content()
    
    # Write to README
    with open('AUTO_UPDATE.md', 'w') as f:
        f.write(content)
    
    print("✅ Content generated successfully!")
    print("\n" + "="*50)
    print(content)
    print("="*50)