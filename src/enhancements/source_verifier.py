"""
Source verification for news articles.
Checks domain credibility and verifies with NewsAPI.
"""

import requests
from urllib.parse import urlparse
from datetime import datetime
from typing import Dict, Optional, List

# Trusted news sources with credibility scores (0-10)
TRUSTED_DOMAINS = {
    # Tier 1: International wire services (10/10)
    'reuters.com': 10,
    'apnews.com': 10,
    'bbc.com': 10,
    'bbc.co.uk': 10,
    
    # Tier 2: Major newspapers (9/10)
    'nytimes.com': 9,
    'washingtonpost.com': 9,
    'theguardian.com': 9,
    'wsj.com': 9,
    'ft.com': 9,
    
    # Tier 3: Established news networks (8/10)
    'cnn.com': 8,
    'nbcnews.com': 8,
    'abcnews.go.com': 8,
    'cbsnews.com': 8,
    'npr.org': 8,
    
    # Tier 4: Business/Tech news (7-8/10)
    'forbes.com': 8,
    'bloomberg.com': 8,
    'techcrunch.com': 7,
    'theverge.com': 7,
    
    # Tier 5: Other credible sources (6-7/10)
    'usatoday.com': 7,
    'latimes.com': 7,
    'time.com': 6,
    'newsweek.com': 6,
}

# Known fake news and satire sites
FAKE_NEWS_DOMAINS = {
    'worldnewsdailyreport.com',
    'nationalreport.net',
    'empirenews.net',
    'huzlers.com',
    'react365.com',
    'clickhole.com',
    'theonion.com',  # Satire
    'beforeitsnews.com',
    'newslo.com',
    'newsbuzzlive.com',
    'dailybuzzlive.com',
}


class SourceVerifier:
    """Verify news source credibility"""
    
    def __init__(self, newsapi_key: Optional[str] = None):
        """
        Initialize source verifier
        
        Args:
            newsapi_key: NewsAPI key for verification (get free at newsapi.org)
        """
        self.newsapi_key = newsapi_key
    
    def check_domain_credibility(self, url: str) -> Dict:
        """
        Check domain credibility based on known lists
        
        Args:
            url: Article URL
            
        Returns:
            dict with credibility information
        """
        try:
            domain = urlparse(url).netloc.replace('www.', '')
            
            # Check if known fake
            if domain in FAKE_NEWS_DOMAINS:
                return {
                    'domain': domain,
                    'credibility_score': 0,
                    'status': 'KNOWN_FAKE',
                    'trusted': False,
                    'category': 'Fake News / Satire',
                    'recommendation': 'DO NOT TRUST'
                }
            
            # Check if trusted
            if domain in TRUSTED_DOMAINS:
                score = TRUSTED_DOMAINS[domain]
                return {
                    'domain': domain,
                    'credibility_score': score,
                    'status': 'TRUSTED',
                    'trusted': True,
                    'category': self._get_category(score),
                    'recommendation': 'HIGHLY CREDIBLE' if score >= 9 else 'CREDIBLE'
                }
            
            # Unknown domain - check age with whois
            return self._check_domain_age(domain)
            
        except Exception as e:
            return {
                'domain': 'unknown',
                'credibility_score': 0,
                'status': 'ERROR',
                'trusted': False,
                'error': str(e)
            }
    
    def _get_category(self, score: int) -> str:
        """Get category based on score"""
        if score >= 9:
            return 'Major News Organization'
        elif score >= 7:
            return 'Established News Source'
        else:
            return 'Known Source'
    
    def _check_domain_age(self, domain: str) -> Dict:
        """Check domain age (older domains more credible)"""
        try:
            import whois
            w = whois.whois(domain)
            
            creation_date = w.creation_date
            if isinstance(creation_date, list):
                creation_date = creation_date[0]
            
            if creation_date:
                age_years = (datetime.now() - creation_date).days / 365
                
                # Score based on age
                if age_years > 10:
                    score = 6
                    status = 'ESTABLISHED'
                elif age_years > 5:
                    score = 5
                    status = 'MATURE'
                elif age_years > 2:
                    score = 4
                    status = 'VERIFIED'
                else:
                    score = 2
                    status = 'NEW_DOMAIN'
                
                return {
                    'domain': domain,
                    'credibility_score': score,
                    'status': status,
                    'domain_age': f'{age_years:.1f} years',
                    'created': creation_date.strftime('%Y-%m-%d'),
                    'trusted': age_years > 2,
                    'recommendation': 'CHECK CAREFULLY' if age_years < 2 else 'UNKNOWN SOURCE'
                }
        except:
            pass
        
        return {
            'domain': domain,
            'credibility_score': 0,
            'status': 'UNKNOWN',
            'trusted': False,
            'recommendation': 'VERIFY CAREFULLY'
        }
    
    def verify_with_newsapi(self, article_title: str, max_results: int = 10) -> Dict:
        """
        Verify article with NewsAPI
        
        Args:
            article_title: Title or excerpt to search
            max_results: Maximum results to return
            
        Returns:
            dict with verification results
        """
        if not self.newsapi_key:
            return {
                'checked': False,
                'error': 'NewsAPI key not provided'
            }
        
        try:
            url = 'https://newsapi.org/v2/everything'
            params = {
                'q': article_title[:100],  # Limit query length
                'apiKey': self.newsapi_key,
                'language': 'en',
                'sortBy': 'relevancy',
                'pageSize': max_results
            }
            
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            if data.get('status') == 'ok':
                articles = data.get('articles', [])
                
                # Extract sources
                sources = []
                for article in articles:
                    source_name = article.get('source', {}).get('name')
                    if source_name:
                        sources.append({
                            'name': source_name,
                            'url': article.get('url'),
                            'title': article.get('title'),
                            'published': article.get('publishedAt')
                        })
                
                # Check if any trusted sources
                trusted_sources = [
                    s['name'] for s in sources 
                    if any(t in s.get('url', '') for t in TRUSTED_DOMAINS.keys())
                ]
                
                return {
                    'checked': True,
                    'found': len(articles) > 0,
                    'total_results': data.get('totalResults', 0),
                    'sources': sources,
                    'trusted_sources_found': trusted_sources,
                    'credibility': 'HIGH' if trusted_sources else 'MEDIUM' if sources else 'LOW',
                    'recommendation': 'VERIFIED' if trusted_sources else 'UNVERIFIED'
                }
            else:
                return {
                    'checked': True,
                    'found': False,
                    'error': data.get('message', 'Unknown error')
                }
                
        except Exception as e:
            return {
                'checked': False,
                'error': str(e)
            }
    
    def comprehensive_check(self, url: str, article_title: str) -> Dict:
        """
        Perform comprehensive source verification
        
        Args:
            url: Article URL
            article_title: Article title for NewsAPI search
            
        Returns:
            dict with all verification results
        """
        domain_check = self.check_domain_credibility(url)
        newsapi_check = self.verify_with_newsapi(article_title)
        
        # Calculate overall credibility
        domain_score = domain_check.get('credibility_score', 0)
        newsapi_credibility = newsapi_check.get('credibility', 'LOW')
        
        overall_score = domain_score
        if newsapi_credibility == 'HIGH':
            overall_score = min(10, overall_score + 2)
        elif newsapi_credibility == 'MEDIUM':
            overall_score = min(10, overall_score + 1)
        
        return {
            'domain_check': domain_check,
            'newsapi_check': newsapi_check,
            'overall_credibility_score': overall_score,
            'overall_status': 'CREDIBLE' if overall_score >= 7 else 'QUESTIONABLE' if overall_score >= 4 else 'NOT CREDIBLE',
            'recommendation': self._get_recommendation(overall_score, domain_check, newsapi_check)
        }
    
    def _get_recommendation(self, score: int, domain: Dict, newsapi: Dict) -> str:
        """Generate recommendation based on all checks"""
        if domain.get('status') == 'KNOWN_FAKE':
            return 'FAKE NEWS SOURCE - Do not trust'
        
        if score >= 8:
            return 'Highly credible source - Likely authentic'
        elif score >= 6:
            return 'Credible source - Cross-check important claims'
        elif score >= 4:
            return 'Unknown source - Verify independently'
        else:
            return 'Low credibility - Treat with high skepticism'


# Convenience functions
def check_source(url: str, newsapi_key: Optional[str] = None) -> Dict:
    """Quick source credibility check"""
    verifier = SourceVerifier(newsapi_key=newsapi_key)
    return verifier.check_domain_credibility(url)


if __name__ == '__main__':
    # Test source verification
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python source_verifier.py <url> [newsapi_key]")
        print("\nExample:")
        print("  python source_verifier.py https://www.bbc.com/news/article")
        print("  python source_verifier.py https://suspicious-site.com abc123key")
        sys.exit(1)
    
    url = sys.argv[1]
    newsapi_key = sys.argv[2] if len(sys.argv) > 2 else None
    
    verifier = SourceVerifier(newsapi_key=newsapi_key)
    
    print(f"\nChecking source: {url}\n")
    print("="*60)
    
    # Domain check
    domain_result = verifier.check_domain_credibility(url)
    print(f"Domain: {domain_result.get('domain')}")
    print(f"Status: {domain_result.get('status')}")
    print(f"Credibility Score: {domain_result.get('credibility_score')}/10")
    print(f"Trusted: {domain_result.get('trusted')}")
    print(f"Recommendation: {domain_result.get('recommendation')}")
    print("="*60)
