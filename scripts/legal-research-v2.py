#!/usr/bin/env python3
"""
DOM_010101 Legal Research Aggregator v2
Uses APIs and reliable endpoints for legal research
"""

import requests
import json
import time
from pathlib import Path
from datetime import datetime
from urllib.parse import quote_plus

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

class LegalResearchV2:
    def __init__(self, output_dir='research/legal'):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        self.all_results = []
        
    def search_case_law_api(self, query: str, max_results: int = 20):
        """Use Case Law Access Project API (free, no key needed)"""
        print(f"⚖️  Searching Case.Law API for: {query}")
        
        base_url = "https://api.case.law/v1/cases/"
        params = {
            'search': query,
            'page_size': min(max_results, 100)
        }
        
        try:
            response = self.session.get(base_url, params=params, timeout=15)
            if response.status_code == 200:
                data = response.json()
                results = []
                
                for case in data.get('results', [])[:max_results]:
                    results.append({
                        'source': 'Case.law (Harvard)',
                        'title': case.get('name', 'Unknown'),
                        'citation': case.get('citations', [{}])[0].get('cite', 'No citation'),
                        'court': case.get('court', {}).get('name', 'Unknown court'),
                        'date': case.get('decision_date', 'Unknown'),
                        'url': case.get('frontend_url', ''),
                        'type': 'case_law'
                    })
                
                print(f"   ✅ Found {len(results)} cases")
                return results
            else:
                print(f"   ⚠️  API returned status {response.status_code}")
                return []
                
        except Exception as e:
            print(f"   ❌ Case.law search failed: {e}")
            return []
    
    def get_popular_ip_cases(self):
        """Get well-known IP cases (curated list)"""
        print("📚 Loading curated IP case list...")
        
        famous_cases = [
            {
                'title': 'Jacobsen v. Katzer',
                'citation': '535 F.3d 1373 (Fed. Cir. 2008)',
                'court': 'U.S. Court of Appeals for the Federal Circuit',
                'holding': 'Open source licenses are enforceable copyright licenses',
                'url': 'https://law.justia.com/cases/federal/appellate-courts/F3/535/1373/490782/',
                'significance': 'Established that GPL and similar licenses have legal teeth',
                'type': 'case_law',
                'source': 'Curated IP Database'
            },
            {
                'title': 'Oracle America, Inc. v. Google Inc.',
                'citation': '141 S. Ct. 1183 (2021)',
                'court': 'U.S. Supreme Court',
                'holding': 'Fair use applies to APIs; Google\'s use of Java APIs was transformative',
                'url': 'https://www.supremecourt.gov/opinions/20pdf/18-956_d18f.pdf',
                'significance': 'Major win for software interoperability and fair use',
                'type': 'case_law',
                'source': 'Curated IP Database'
            },
            {
                'title': 'Feist Publications, Inc. v. Rural Telephone Service Co.',
                'citation': '499 U.S. 340 (1991)',
                'court': 'U.S. Supreme Court',
                'holding': 'Facts are not copyrightable; compilations need originality',
                'url': 'https://supreme.justia.com/cases/federal/us/499/340/',
                'significance': 'Established originality requirement for copyright',
                'type': 'case_law',
                'source': 'Curated IP Database'
            },
            {
                'title': 'Golan v. Holder',
                'citation': '565 U.S. 302 (2012)',
                'court': 'U.S. Supreme Court',
                'holding': 'Congress can restore copyright to public domain works',
                'url': 'https://www.supremecourt.gov/opinions/11pdf/10-545.pdf',
                'significance': 'Important for understanding copyright restoration',
                'type': 'case_law',
                'source': 'Curated IP Database'
            },
            {
                'title': 'Community for Creative Non-Violence v. Reid',
                'citation': '490 U.S. 730 (1989)',
                'court': 'U.S. Supreme Court',
                'holding': 'Work-for-hire doctrine explained; contractor vs employee test',
                'url': 'https://supreme.justia.com/cases/federal/us/490/730/',
                'significance': 'Critical for determining code ownership',
                'type': 'case_law',
                'source': 'Curated IP Database'
            },
            {
                'title': 'MAI Systems Corp. v. Peak Computer, Inc.',
                'citation': '991 F.2d 511 (9th Cir. 1993)',
                'court': 'U.S. Court of Appeals for the Ninth Circuit',
                'holding': 'Loading software into RAM creates a copy under Copyright Act',
                'url': 'https://law.justia.com/cases/federal/appellate-courts/F2/991/511/361451/',
                'significance': 'Defined what constitutes copying in digital context',
                'type': 'case_law',
                'source': 'Curated IP Database'
            },
            {
                'title': 'ProCD, Inc. v. Zeidenberg',
                'citation': '86 F.3d 1447 (7th Cir. 1996)',
                'court': 'U.S. Court of Appeals for the Seventh Circuit',
                'holding': 'Shrinkwrap licenses are enforceable contracts',
                'url': 'https://law.justia.com/cases/federal/appellate-courts/F3/86/1447/499331/',
                'significance': 'Established enforceability of software licenses',
                'type': 'case_law',
                'source': 'Curated IP Database'
            },
            {
                'title': 'Apple Computer, Inc. v. Franklin Computer Corp.',
                'citation': '714 F.2d 1240 (3d Cir. 1983)',
                'court': 'U.S. Court of Appeals for the Third Circuit',
                'holding': 'Software is copyrightable as literary work',
                'url': 'https://law.justia.com/cases/federal/appellate-courts/F2/714/1240/376417/',
                'significance': 'Foundational case for software copyright',
                'type': 'case_law',
                'source': 'Curated IP Database'
            },
        ]
        
        print(f"   ✅ Loaded {len(famous_cases)} landmark cases")
        return famous_cases
    
    def get_relevant_statutes(self):
        """Get relevant IP statutes (curated)"""
        print("📋 Loading relevant statutes...")
        
        statutes = [
            {
                'title': '17 U.S.C. § 102 - Subject matter of copyright',
                'url': 'https://www.law.cornell.edu/uscode/text/17/102',
                'summary': 'Copyright protection subsists in original works of authorship',
                'relevance': 'Foundational copyright statute',
                'type': 'statute',
                'source': 'U.S. Code'
            },
            {
                'title': '17 U.S.C. § 106 - Exclusive rights in copyrighted works',
                'url': 'https://www.law.cornell.edu/uscode/text/17/106',
                'summary': 'Copyright owner has exclusive rights to reproduce, distribute, etc.',
                'relevance': 'Defines what rights you have in your code',
                'type': 'statute',
                'source': 'U.S. Code'
            },
            {
                'title': '17 U.S.C. § 107 - Fair use',
                'url': 'https://www.law.cornell.edu/uscode/text/17/107',
                'summary': 'Fair use is not infringement under certain conditions',
                'relevance': 'Critical defense against infringement claims',
                'type': 'statute',
                'source': 'U.S. Code'
            },
            {
                'title': '17 U.S.C. § 512 - DMCA safe harbor',
                'url': 'https://www.law.cornell.edu/uscode/text/17/512',
                'summary': 'Limits liability for online service providers',
                'relevance': 'Important if hosting user content',
                'type': 'statute',
                'source': 'U.S. Code'
            },
            {
                'title': '15 U.S.C. § 1125(a) - False designation of origin (Lanham Act)',
                'url': 'https://www.law.cornell.edu/uscode/text/15/1125',
                'summary': 'Protects against trademark infringement and false advertising',
                'relevance': 'Use this against copycats misrepresenting origin',
                'type': 'statute',
                'source': 'U.S. Code'
            },
            {
                'title': '18 U.S.C. § 1030 - Computer Fraud and Abuse Act (CFAA)',
                'url': 'https://www.law.cornell.edu/uscode/text/18/1030',
                'summary': 'Criminalizes unauthorized computer access',
                'relevance': 'Protection against hacking/unauthorized access',
                'type': 'statute',
                'source': 'U.S. Code'
            },
            {
                'title': '35 U.S.C. § 101 - Inventions patentable',
                'url': 'https://www.law.cornell.edu/uscode/text/35/101',
                'summary': 'Defines what can be patented',
                'relevance': 'Software patents (contentious but exists)',
                'type': 'statute',
                'source': 'U.S. Code'
            },
            {
                'title': 'California Anti-SLAPP statute (Cal. Code Civ. Proc. § 425.16)',
                'url': 'https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CCP&sectionNum=425.16',
                'summary': 'Protects against meritless lawsuits targeting free speech',
                'relevance': 'Shield against frivolous defamation suits',
                'type': 'statute',
                'source': 'California Law'
            },
            {
                'title': 'Uniform Trade Secrets Act (UTSA)',
                'url': 'https://www.law.cornell.edu/wex/uniform_trade_secrets_act',
                'summary': 'State-level protection for trade secrets',
                'relevance': 'Protects non-public aspects of your work',
                'type': 'statute',
                'source': 'Model State Law'
            },
        ]
        
        print(f"   ✅ Loaded {len(statutes)} key statutes")
        return statutes
    
    def get_defensive_resources(self):
        """Curated defensive legal resources"""
        print("🛡️  Loading defensive legal resources...")
        
        resources = [
            {
                'title': 'Electronic Frontier Foundation (EFF) - Coders\' Rights Project',
                'url': 'https://www.eff.org/issues/coders',
                'summary': 'Free legal resources for developers',
                'type': 'resource',
                'source': 'EFF'
            },
            {
                'title': 'Software Freedom Law Center',
                'url': 'https://softwarefreedom.org/',
                'summary': 'Legal services for FOSS projects',
                'type': 'resource',
                'source': 'SFLC'
            },
            {
                'title': 'GNU GPL Violations - FSF Compliance Lab',
                'url': 'https://www.fsf.org/licensing/licenses/gpl-violation',
                'summary': 'How to enforce GPL',
                'type': 'resource',
                'source': 'FSF'
            },
            {
                'title': 'Creative Commons Legal Database',
                'url': 'https://creativecommons.org/about/program-areas/legal-advocacy/',
                'summary': 'CC license enforcement cases',
                'type': 'resource',
                'source': 'Creative Commons'
            },
            {
                'title': 'Public Knowledge - Tech Policy',
                'url': 'https://publicknowledge.org/',
                'summary': 'Advocacy for tech freedom',
                'type': 'resource',
                'source': 'Public Knowledge'
            },
        ]
        
        print(f"   ✅ Loaded {len(resources)} defensive resources")
        return resources
    
    def aggregate_all(self):
        """Aggregate everything"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        print("\n" + "="*60)
        print("🧠⚖️  DOM_010101 Legal Research Aggregator v2")
        print("="*60 + "\n")
        
        all_results = []
        
        # Get curated cases
        all_results.extend(self.get_popular_ip_cases())
        time.sleep(1)
        
        # Get statutes
        all_results.extend(self.get_relevant_statutes())
        time.sleep(1)
        
        # Get resources
        all_results.extend(self.get_defensive_resources())
        time.sleep(1)
        
        # Try API search for additional cases
        search_terms = [
            "GPL enforcement",
            "copyright software",
            "trademark domain name",
            "trade secret software"
        ]
        
        for term in search_terms:
            results = self.search_case_law_api(term, max_results=5)
            all_results.extend(results)
            time.sleep(3)
        
        # Save
        output_data = {
            'timestamp': timestamp,
            'total_sources': len(all_results),
            'results': all_results
        }
        
        output_file = self.output_dir / f"legal_arsenal_{timestamp}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Saved {len(all_results)} sources to {output_file}")
        
        # Generate markdown
        self.generate_markdown(output_data, output_file.with_suffix('.md'))
        
        return output_data
    
    def generate_markdown(self, data: dict, output_file: Path):
        """Generate markdown summary"""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# Legal Arsenal - DOM_010101\n\n")
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
            
            # Write sections
            if 'case_law' in by_type:
                f.write("## 📜 Case Law\n\n")
                for i, case in enumerate(by_type['case_law'], 1):
                    f.write(f"### {i}. {case['title']}\n\n")
                    if 'citation' in case:
                        f.write(f"**Citation:** {case['citation']}\n")
                    if 'court' in case:
                        f.write(f"**Court:** {case['court']}\n")
                    if 'holding' in case:
                        f.write(f"**Holding:** {case['holding']}\n")
                    if 'significance' in case:
                        f.write(f"**Significance:** {case['significance']}\n")
                    if 'url' in case and case['url']:
                        f.write(f"**URL:** [{case['url']}]({case['url']})\n")
                    f.write("\n---\n\n")
            
            if 'statute' in by_type:
                f.write("## 📋 Statutes\n\n")
                for i, statute in enumerate(by_type['statute'], 1):
                    f.write(f"### {i}. {statute['title']}\n\n")
                    if 'summary' in statute:
                        f.write(f"**Summary:** {statute['summary']}\n")
                    if 'relevance' in statute:
                        f.write(f"**Relevance:** {statute['relevance']}\n")
                    if 'url' in statute:
                        f.write(f"**URL:** [{statute['url']}]({statute['url']})\n")
                    f.write("\n---\n\n")
            
            if 'resource' in by_type:
                f.write("## 🛡️ Defensive Resources\n\n")
                for i, resource in enumerate(by_type['resource'], 1):
                    f.write(f"### {i}. {resource['title']}\n\n")
                    if 'summary' in resource:
                        f.write(f"**Summary:** {resource['summary']}\n")
                    if 'url' in resource:
                        f.write(f"**URL:** [{resource['url']}]({resource['url']})\n")
                    f.write("\n---\n\n")
        
        print(f"✅ Markdown summary: {output_file}")


def main():
    aggregator = LegalResearchV2()
    aggregator.aggregate_all()
    
    print("\n" + "="*60)
    print("✅ Legal arsenal compiled!")
    print("   You now have:")
    print("   • Landmark IP cases with full citations")
    print("   • Key federal statutes")
    print("   • Defensive legal resources")
    print("   • Additional case law from Harvard API")
    print("\n   Location: research/legal/")
    print("="*60)


if __name__ == '__main__':
    main()
