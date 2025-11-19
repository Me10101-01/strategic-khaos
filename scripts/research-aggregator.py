#!/usr/bin/env python3
"""
DOM_010101 Academic Research Aggregator
Legitimately fetch public research from .gov, .org, .edu sources
"""

import requests
from bs4 import BeautifulSoup
import json
import time
from pathlib import Path
from datetime import datetime
from urllib.parse import quote_plus, urljoin
import argparse

# User agent to identify as a research bot
HEADERS = {
    'User-Agent': 'DOM_010101-ResearchBot/1.0 (Academic research aggregator; +https://github.com/Me10101-01/strategic-khaos)'
}

class ResearchAggregator:
    def __init__(self, output_dir='research'):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        
    def search_pubmed(self, query: str, max_results: int = 20):
        """Search PubMed Central for open-access papers"""
        print(f"🔬 Searching PubMed for: {query}")
        
        base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
        search_url = f"{base_url}esearch.fcgi?db=pmc&term={quote_plus(query)}&retmode=json&retmax={max_results}"
        
        try:
            response = self.session.get(search_url, timeout=10)
            data = response.json()
            
            ids = data.get('esearchresult', {}).get('idlist', [])
            print(f"   Found {len(ids)} papers")
            
            papers = []
            for pmcid in ids[:max_results]:
                # Get paper details
                fetch_url = f"{base_url}esummary.fcgi?db=pmc&id={pmcid}&retmode=json"
                details = self.session.get(fetch_url, timeout=10).json()
                
                if 'result' in details and pmcid in details['result']:
                    paper = details['result'][pmcid]
                    papers.append({
                        'source': 'PubMed Central',
                        'id': pmcid,
                        'title': paper.get('title', 'Unknown'),
                        'authors': paper.get('authors', []),
                        'url': f"https://www.ncbi.nlm.nih.gov/pmc/articles/PMC{pmcid}/",
                        'published': paper.get('pubdate', 'Unknown')
                    })
                
                time.sleep(0.5)  # Be respectful of API limits
            
            return papers
            
        except Exception as e:
            print(f"   ❌ PubMed search failed: {e}")
            return []
    
    def search_arxiv(self, query: str, max_results: int = 20):
        """Search arXiv for preprints"""
        print(f"📄 Searching arXiv for: {query}")
        
        base_url = "http://export.arxiv.org/api/query"
        params = {
            'search_query': f'all:{query}',
            'start': 0,
            'max_results': max_results
        }
        
        try:
            response = self.session.get(base_url, params=params, timeout=10)
            soup = BeautifulSoup(response.content, 'xml')
            
            papers = []
            for entry in soup.find_all('entry'):
                papers.append({
                    'source': 'arXiv',
                    'id': entry.id.text.split('/')[-1],
                    'title': entry.title.text.strip(),
                    'authors': [author.find('name').text for author in entry.find_all('author')],
                    'url': entry.id.text,
                    'abstract': entry.summary.text.strip() if entry.summary else '',
                    'published': entry.published.text if entry.published else 'Unknown'
                })
            
            print(f"   Found {len(papers)} papers")
            return papers
            
        except Exception as e:
            print(f"   ❌ arXiv search failed: {e}")
            return []
    
    def search_govinfo(self, query: str, max_results: int = 20):
        """Search govinfo.gov for government documents"""
        print(f"🏛️  Searching govinfo.gov for: {query}")
        
        # govinfo.gov has an API but requires authentication
        # Using public search instead
        search_url = f"https://www.govinfo.gov/app/search/{quote_plus(query)}"
        
        try:
            response = self.session.get(search_url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            papers = []
            results = soup.find_all('div', class_='result-item')[:max_results]
            
            for result in results:
                title_elem = result.find('a', class_='package-link')
                if title_elem:
                    papers.append({
                        'source': 'govinfo.gov',
                        'title': title_elem.text.strip(),
                        'url': urljoin('https://www.govinfo.gov', title_elem.get('href', '')),
                        'published': 'Unknown'
                    })
            
            print(f"   Found {len(papers)} documents")
            return papers
            
        except Exception as e:
            print(f"   ❌ govinfo search failed: {e}")
            return []
    
    def aggregate_research(self, query: str, sources=['pubmed', 'arxiv'], max_per_source: int = 20):
        """Aggregate research from multiple sources"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results = {
            'query': query,
            'timestamp': timestamp,
            'papers': []
        }
        
        if 'pubmed' in sources:
            results['papers'].extend(self.search_pubmed(query, max_per_source))
        
        if 'arxiv' in sources:
            results['papers'].extend(self.search_arxiv(query, max_per_source))
        
        if 'govinfo' in sources:
            results['papers'].extend(self.search_govinfo(query, max_per_source))
        
        # Save results
        output_file = self.output_dir / f"{query.replace(' ', '_')}_{timestamp}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Saved {len(results['papers'])} papers to {output_file}")
        
        # Generate markdown summary
        md_file = output_file.with_suffix('.md')
        self.generate_markdown_summary(results, md_file)
        
        return results
    
    def generate_markdown_summary(self, results: dict, output_file: Path):
        """Generate a markdown summary of research"""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"# Research: {results['query']}\n\n")
            f.write(f"**Aggregated:** {results['timestamp']}\n")
            f.write(f"**Total Papers:** {len(results['papers'])}\n\n")
            f.write("---\n\n")
            
            for i, paper in enumerate(results['papers'], 1):
                f.write(f"## {i}. {paper['title']}\n\n")
                f.write(f"**Source:** {paper['source']}\n")
                
                if 'authors' in paper and paper['authors']:
                    authors = paper['authors'][:3]  # First 3 authors
                    f.write(f"**Authors:** {', '.join(authors)}")
                    if len(paper['authors']) > 3:
                        f.write(f" et al. ({len(paper['authors'])} total)")
                    f.write("\n")
                
                f.write(f"**Published:** {paper.get('published', 'Unknown')}\n")
                f.write(f"**URL:** [{paper['url']}]({paper['url']})\n")
                
                if 'abstract' in paper and paper['abstract']:
                    abstract = paper['abstract'][:500]
                    f.write(f"\n**Abstract:** {abstract}...\n")
                
                f.write("\n---\n\n")
        
        print(f"✅ Markdown summary: {output_file}")


def main():
    parser = argparse.ArgumentParser(description='DOM_010101 Academic Research Aggregator')
    parser.add_argument('query', help='Search query')
    parser.add_argument('-s', '--sources', nargs='+', 
                       default=['pubmed', 'arxiv'],
                       choices=['pubmed', 'arxiv', 'govinfo'],
                       help='Sources to search')
    parser.add_argument('-n', '--max-per-source', type=int, default=20,
                       help='Max results per source')
    parser.add_argument('-o', '--output-dir', default='research',
                       help='Output directory')
    
    args = parser.parse_args()
    
    aggregator = ResearchAggregator(output_dir=args.output_dir)
    aggregator.aggregate_research(
        query=args.query,
        sources=args.sources,
        max_per_source=args.max_per_source
    )


if __name__ == '__main__':
    main()
