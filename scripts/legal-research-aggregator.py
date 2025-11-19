#!/usr/bin/env python3
"""
DOM_010101 Legal Research Aggregator
Finds case law, statutes, and scholarly articles for IP protection
"""

import requests
from bs4 import BeautifulSoup
import json
import time
from pathlib import Path
from datetime import datetime
from urllib.parse import quote_plus, urljoin
import re

HEADERS = {
    'User-Agent': 'DOM_010101-LegalResearchBot/1.0 (Academic legal research; +https://github.com/Me10101-01/strategic-khaos)'
}

class LegalResearchAggregator:
    def __init__(self, output_dir='research/legal'):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        self.results = []
        
    def search_google_scholar_legal(self, query: str, max_results: int = 20):
        """Search Google Scholar for legal cases and articles"""
        print(f"⚖️  Searching Google Scholar (Legal) for: {query}")
        
        base_url = "https://scholar.google.com/scholar"
        params = {
            'q': query,
            'hl': 'en',
            'as_sdt': '6',  # Case law
            'num': min(max_results, 20)  # Max 20 per page
        }
        
        try:
            response = self.session.get(base_url, params=params, timeout=15)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            results = []
            for result in soup.find_all('div', class_='gs_ri')[:max_results]:
                title_elem = result.find('h3', class_='gs_rt')
                snippet_elem = result.find('div', class_='gs_rs')
                
                if title_elem:
                    # Extract link
                    link_elem = title_elem.find('a')
                    link = link_elem.get('href', '') if link_elem else ''
                    
                    # Clean title (remove [PDF], [HTML] tags)
                    title = re.sub(r'\[.*?\]', '', title_elem.get_text()).strip()
                    
                    # Extract citation info
                    meta_elem = result.find('div', class_='gs_a')
                    citation = meta_elem.get_text() if meta_elem else 'Unknown'
                    
                    results.append({
                        'source': 'Google Scholar (Legal)',
                        'title': title,
                        'citation': citation,
                        'url': link,
                        'snippet': snippet_elem.get_text() if snippet_elem else '',
                        'type': 'case_law' if 'court' in citation.lower() or 'v.' in title else 'article'
                    })
                
                time.sleep(2)  # Be respectful of rate limits
            
            print(f"   Found {len(results)} legal sources")
            return results
            
        except Exception as e:
            print(f"   ❌ Google Scholar search failed: {e}")
            return []
    
    def search_justia(self, query: str, max_results: int = 10):
        """Search Justia for case law"""
        print(f"⚖️  Searching Justia for: {query}")
        
        search_url = f"https://law.justia.com/search?query={quote_plus(query)}"
        
        try:
            response = self.session.get(search_url, timeout=15)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            results = []
            for result in soup.find_all('div', class_='search-result')[:max_results]:
                title_elem = result.find('h3')
                if title_elem:
                    link_elem = title_elem.find('a')
                    snippet_elem = result.find('p', class_='snippet')
                    
                    results.append({
                        'source': 'Justia',
                        'title': title_elem.get_text().strip(),
                        'url': urljoin('https://law.justia.com', link_elem.get('href', '')) if link_elem else '',
                        'snippet': snippet_elem.get_text().strip() if snippet_elem else '',
                        'type': 'case_law'
                    })
            
            print(f"   Found {len(results)} cases")
            return results
            
        except Exception as e:
            print(f"   ❌ Justia search failed: {e}")
            return []
    
    def search_govinfo_legal(self, query: str, max_results: int = 10):
        """Search govinfo.gov for statutes and regulations"""
        print(f"🏛️  Searching govinfo.gov for: {query}")
        
        search_url = f"https://www.govinfo.gov/app/search/{quote_plus(query)}"
        
        try:
            response = self.session.get(search_url, timeout=15)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            results = []
            for result in soup.find_all('div', class_='search-result-item')[:max_results]:
                title_elem = result.find('a', class_='package-link')
                if title_elem:
                    results.append({
                        'source': 'govinfo.gov',
                        'title': title_elem.get_text().strip(),
                        'url': urljoin('https://www.govinfo.gov', title_elem.get('href', '')),
                        'type': 'statute'
                    })
            
            print(f"   Found {len(results)} statutes/regulations")
            return results
            
        except Exception as e:
            print(f"   ❌ govinfo search failed: {e}")
            return []
    
    def search_cornell_lii(self, query: str, max_results: int = 10):
        """Search Cornell Legal Information Institute"""
        print(f"📚 Searching Cornell LII for: {query}")
        
        search_url = f"https://www.law.cornell.edu/search/site/{quote_plus(query)}"
        
        try:
            response = self.session.get(search_url, timeout=15)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            results = []
            for result in soup.find_all('div', class_='search-result')[:max_results]:
                title_elem = result.find('h3')
                if title_elem and title_elem.find('a'):
                    link = title_elem.find('a').get('href', '')
                    snippet_elem = result.find('p', class_='search-snippet')
                    
                    results.append({
                        'source': 'Cornell LII',
                        'title': title_elem.get_text().strip(),
                        'url': urljoin('https://www.law.cornell.edu', link),
                        'snippet': snippet_elem.get_text().strip() if snippet_elem else '',
                        'type': 'legal_reference'
                    })
            
            print(f"   Found {len(results)} legal references")
            return results
            
        except Exception as e:
            print(f"   ❌ Cornell LII search failed: {e}")
            return []
    
    def search_ssrn(self, query: str, max_results: int = 10):
        """Search SSRN for legal scholarship"""
        print(f"📄 Searching SSRN for: {query}")
        
        search_url = f"https://papers.ssrn.com/sol3/results.cfm?txtKeywordSearch={quote_plus(query)}"
        
        try:
            response = self.session.get(search_url, timeout=15)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            results = []
            # SSRN has dynamic content, this is simplified
            for result in soup.find_all('div', class_='paper')[:max_results]:
                title_elem = result.find('a', class_='title')
                if title_elem:
                    results.append({
                        'source': 'SSRN',
                        'title': title_elem.get_text().strip(),
                        'url': urljoin('https://papers.ssrn.com', title_elem.get('href', '')),
                        'type': 'legal_scholarship'
                    })
            
            print(f"   Found {len(results)} papers")
            return results
            
        except Exception as e:
            print(f"   ❌ SSRN search failed: {e}")
            return []
    
    def aggregate_legal_research(self, topics: list, max_per_source: int = 15):
        """Aggregate legal research from multiple sources on multiple topics"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        all_results = []
        
        for topic in topics:
            print(f"\n{'='*60}")
            print(f"📖 Researching: {topic}")
            print(f"{'='*60}\n")
            
            # Search all sources
            all_results.extend(self.search_google_scholar_legal(topic, max_per_source))
            time.sleep(3)
            
            all_results.extend(self.search_justia(topic, max_per_source))
            time.sleep(3)
            
            all_results.extend(self.search_govinfo_legal(topic, max_per_source))
            time.sleep(3)
            
            all_results.extend(self.search_cornell_lii(topic, max_per_source))
            time.sleep(3)
            
            all_results.extend(self.search_ssrn(topic, max_per_source))
            time.sleep(3)
        
        # Save results
        output_data = {
            'topics': topics,
            'timestamp': timestamp,
            'total_sources': len(all_results),
            'results': all_results
        }
        
        output_file = self.output_dir / f"legal_research_{timestamp}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Saved {len(all_results)} legal sources to {output_file}")
        
        # Generate markdown summary
        self.generate_legal_summary(output_data, output_file.with_suffix('.md'))
        
        return output_data
    
    def generate_legal_summary(self, data: dict, output_file: Path):
        """Generate markdown summary of legal research"""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"# Legal Research Summary\n\n")
            f.write(f"**Topics:** {', '.join(data['topics'])}\n")
            f.write(f"**Generated:** {data['timestamp']}\n")
            f.write(f"**Total Sources:** {data['total_sources']}\n\n")
            f.write("---\n\n")
            
            # Group by type
            by_type = {}
            for result in data['results']:
                result_type = result.get('type', 'other')
                if result_type not in by_type:
                    by_type[result_type] = []
                by_type[result_type].append(result)
            
            # Write by category
            type_names = {
                'case_law': '📜 Case Law',
                'statute': '📋 Statutes & Regulations',
                'legal_reference': '📚 Legal References',
                'legal_scholarship': '📄 Legal Scholarship',
                'article': '📰 Articles'
            }
            
            for result_type, results in by_type.items():
                f.write(f"## {type_names.get(result_type, result_type.title())}\n\n")
                
                for i, result in enumerate(results, 1):
                    f.write(f"### {i}. {result['title']}\n\n")
                    f.write(f"**Source:** {result['source']}\n")
                    
                    if 'citation' in result:
                        f.write(f"**Citation:** {result['citation']}\n")
                    
                    if result.get('url'):
                        f.write(f"**URL:** [{result['url']}]({result['url']})\n")
                    
                    if 'snippet' in result and result['snippet']:
                        snippet = result['snippet'][:500]
                        f.write(f"\n**Excerpt:** {snippet}...\n")
                    
                    f.write("\n---\n\n")
        
        print(f"✅ Legal summary: {output_file}")


def main():
    """Main research aggregation"""
    
    # IP Protection topics
    topics = [
        "open source software intellectual property protection",
        "trademark infringement online platforms",
        "copyright GPL license enforcement cases won",
        "defamation against software developers precedent",
        "royalty free license violation remedies",
        "DAO LLC legal structure case law",
        "software patent defensive publication",
        "trade secret protection open source",
        "DMCA takedown abuse counterclaim",
        "GitHub repository copyright ownership",
        "creative commons license enforcement",
        "anti-SLAPP motion software industry",
        "declaratory judgment patent infringement",
        "tortious interference business relations tech",
        "misappropriation trade secrets statute",
    ]
    
    aggregator = LegalResearchAggregator()
    
    print("🧠⚖️  DOM_010101 Legal Research Aggregator")
    print("="*60)
    print(f"Researching {len(topics)} legal topics")
    print(f"This will take ~{len(topics) * 5} minutes (respectful rate limiting)")
    print("="*60)
    
    results = aggregator.aggregate_legal_research(topics, max_per_source=8)
    
    print("\n" + "="*60)
    print(f"✅ Research complete!")
    print(f"   Total sources collected: {results['total_sources']}")
    print(f"   Topics covered: {len(topics)}")
    print(f"   Location: research/legal/")
    print("="*60)


if __name__ == '__main__':
    main()
