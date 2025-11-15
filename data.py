import os
import requests
from datetime import datetime

def fetch_github_stats():
    username = "m-nouman"
    token = os.getenv('GITHUB_TOKEN')
    
    headers = {
        'Authorization': f'token {token}',
        'User-Agent': 'README-Stats-Updater'
    }
    
    # Fetch user data
    user_url = f"https://api.github.com/users/{username}"
    user_response = requests.get(user_url, headers=headers)
    user_data = user_response.json()
    
    # Fetch repositories
    repos_url = f"https://api.github.com/users/{username}/repos?per_page=100"
    repos_response = requests.get(repos_url, headers=headers)
    repos_data = repos_response.json()
    
    # Calculate statistics
    total_stars = sum(repo['stargazers_count'] for repo in repos_data)
    total_forks = sum(repo['forks_count'] for repo in repos_data)
    total_repos = len(repos_data)
    
    # Analyze languages
    languages = {}
    for repo in repos_data:
        lang = repo.get('language')
        if lang:
            languages[lang] = languages.get(lang, 0) + 1
    
    # Sort and get top languages
    sorted_languages = sorted(languages.items(), key=lambda x: x[1], reverse=True)[:8]
    
    # Generate language bars
    language_bars = []
    for lang, count in sorted_languages:
        percentage = round((count / total_repos) * 100)
        bars = '█' * round(percentage / 5) + '░' * (20 - round(percentage / 5))
        language_bars.append(f"{lang:<15} {bars} {percentage}%")
    
    return {
        'username': username,
        'public_repos': user_data.get('public_repos', 0),
        'followers': user_data.get('followers', 0),
        'following': user_data.get('following', 0),
        'total_stars': total_stars,
        'total_forks': total_forks,
        'language_bars': '\n'.join(language_bars),
        'top_languages': sorted_languages[:5]
    }

def update_readme(stats):
    with open('README.md', 'r') as file:
        content = file.read()
    
    # Find and replace the stats section
    new_stats_section = f"""## 📊 **Real-Time GitHub Analytics**

<div align="center">

### 📈 **GitHub Profile Stats**
- **Public Repositories**: {stats['public_repos']}
- **Followers**: {stats['followers']}
- **Following**: {stats['following']}
- **Total Stars**: {stats['total_stars']}
- **Total Forks**: {stats['total_forks']}

### 💻 **Language Distribution**
