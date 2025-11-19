#!/usr/bin/env python3
"""
DOM_010101 Fork Detective
Monitors GitHub for unauthorized forks and copies of your code
"""

import requests
import json
import time
from datetime import datetime
from pathlib import Path

GITHUB_TOKEN = None  # Set in .env.vault
YOUR_REPO = "Me10101-01/strategic-khaos"
SEARCH_QUERIES = [
    # Unique code snippets from your project
    "DOM_010101",
    "strategic-khaos",
    "neurospice",
    # Add unique function names, error messages, etc.
]

def search_github_code(query: str, github_token: str = None):
    """Search GitHub for code containing query"""
    headers = {'Accept': 'application/vnd.github.v3+json'}
    if github_token:
        headers['Authorization'] = f'token {github_token}'
    
    url = f"https://api.github.com/search/code?q={query}"
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data.get('items', [])
        else:
            print(f"❌ GitHub API error: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ Search failed: {e}")
        return []

def check_if_fork(repo_full_name: str, github_token: str = None):
    """Check if a repo is a fork and of what"""
    headers = {'Accept': 'application/vnd.github.v3+json'}
    if github_token:
        headers['Authorization'] = f'token {github_token}'
    
    url = f"https://api.github.com/repos/{repo_full_name}"
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return {
                'is_fork': data.get('fork', False),
                'parent': data.get('parent', {}).get('full_name', None),
                'created_at': data.get('created_at'),
                'updated_at': data.get('updated_at'),
                'stars': data.get('stargazers_count', 0),
                'url': data.get('html_url')
            }
        return None
    except Exception as e:
        print(f"❌ Repo check failed: {e}")
        return None

def detect_suspicious_copies():
    """Find potential unauthorized copies"""
    print("🔍 DOM_010101 Fork Detective")
    print("="*60)
    
    suspicious_repos = []
    
    for query in SEARCH_QUERIES:
        print(f"\n🔎 Searching for: {query}")
        results = search_github_code(query, GITHUB_TOKEN)
        
        for item in results:
            repo_name = item.get('repository', {}).get('full_name')
            
            # Skip your own repo
            if repo_name == YOUR_REPO:
                continue
            
            print(f"   📦 Found in: {repo_name}")
            
            # Check if it's a legitimate fork
            repo_info = check_if_fork(repo_name, GITHUB_TOKEN)
            
            if repo_info:
                if repo_info['parent'] == YOUR_REPO:
                    print(f"      ✅ Legitimate fork (attributed)")
                else:
                    print(f"      ⚠️  SUSPICIOUS - Not marked as fork!")
                    suspicious_repos.append({
                        'repo': repo_name,
                        'url': repo_info['url'],
                        'created': repo_info['created_at'],
                        'stars': repo_info['stars'],
                        'query_matched': query
                    })
        
        time.sleep(2)  # Rate limiting
    
    # Save report
    if suspicious_repos:
        output_dir = Path('research/fork-monitoring')
        output_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = output_dir / f"suspicious_forks_{timestamp}.json"
        
        with open(report_file, 'w') as f:
            json.dump({
                'timestamp': timestamp,
                'suspicious_count': len(suspicious_repos),
                'repos': suspicious_repos
            }, f, indent=2)
        
        print(f"\n⚠️  ALERT: {len(suspicious_repos)} suspicious repos detected!")
        print(f"📄 Report saved: {report_file}")
        
        # Generate DMCA template
        generate_dmca_template(suspicious_repos[0])
    else:
        print("\n✅ No suspicious copies detected. All clear!")

def generate_dmca_template(repo_info: dict):
    """Generate DMCA takedown notice template"""
    template = f"""
# DMCA Takedown Notice - TEMPLATE

**To:** GitHub DMCA Team (copyright@github.com)
**From:** [Your Name]
**Date:** {datetime.now().strftime("%Y-%m-%d")}

---

## Identification of Copyrighted Work

I am the owner of the copyrighted work located at:
https://github.com/{YOUR_REPO}

## Identification of Infringing Material

The following repository contains unauthorized copies of my copyrighted code:
{repo_info['url']}

**Evidence:**
- Contains code snippets matching: {repo_info['query_matched']}
- Not marked as a fork of my repository
- No attribution provided
- Created: {repo_info['created']}

## Statement of Good Faith Belief

I have a good faith belief that use of the copyrighted materials described above as allegedly infringing is not authorized by the copyright owner, its agent, or the law.

## Statement of Accuracy

I swear, under penalty of perjury, that the information in this notification is accurate and that I am the copyright owner or am authorized to act on behalf of the owner of an exclusive right that is allegedly infringed.

## Contact Information

[Your contact details]

---

**Legal Basis:**
- 17 U.S.C. § 512(c)(3) - DMCA Takedown Procedure
- Jacobsen v. Katzer, 535 F.3d 1373 - Open source licenses are enforceable

**Signed:** ____________________
"""
    
    output_dir = Path('research/fork-monitoring')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    dmca_file = output_dir / f"DMCA_template_{datetime.now().strftime('%Y%m%d')}.md"
    with open(dmca_file, 'w') as f:
        f.write(template)
    
    print(f"📝 DMCA template generated: {dmca_file}")

if __name__ == '__main__':
    detect_suspicious_copies()
