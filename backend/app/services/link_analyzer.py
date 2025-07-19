"""
Link Security Analysis Service
Analyzes URLs for phishing, lookalike domains, and security threats
"""

import re
import dns.resolver
import tldextract
from urllib.parse import urlparse, urljoin
from fuzzywuzzy import fuzz
from validators import url as url_validator
from typing import Dict, List, Tuple, Optional
import logging

logger = logging.getLogger(__name__)

class LinkAnalyzer:
    """Comprehensive link security analyzer"""
    
    def __init__(self):
        # Known legitimate domains (could be loaded from config)
        self.legitimate_domains = {
            'google.com', 'gmail.com', 'google.de',
            'microsoft.com', 'outlook.com', 'hotmail.com',
            'apple.com', 'icloud.com',
            'paypal.com', 'paypal.de',
            'amazon.com', 'amazon.de',
            'ebay.com', 'ebay.de',
            'facebook.com', 'instagram.com', 'twitter.com',
            'linkedin.com', 'github.com',
            'dropbox.com', 'onedrive.com',
            'zoom.us', 'teams.microsoft.com',
            'slack.com', 'discord.com'
        }
        
        # Suspicious TLDs
        self.suspicious_tlds = {
            '.tk', '.ml', '.ga', '.cf', '.gq',  # Free TLDs often used for phishing
            '.xyz', '.top', '.club', '.online'  # Cheap TLDs
        }
        
        # Phishing indicators
        self.phishing_keywords = {
            'login', 'signin', 'secure', 'verify', 'confirm', 'update',
            'account', 'password', 'security', 'banking', 'payment',
            'urgent', 'immediate', 'action', 'required', 'suspended',
            'compromised', 'hacked', 'breach', 'fraud', 'suspicious'
        }
        
        # Common brand names for lookalike detection
        self.brand_names = {
            'google', 'gmail', 'microsoft', 'outlook', 'hotmail',
            'apple', 'icloud', 'paypal', 'amazon', 'ebay',
            'facebook', 'instagram', 'twitter', 'linkedin',
            'dropbox', 'onedrive', 'zoom', 'teams', 'slack'
        }

    def analyze_links(self, html_content: str, plain_text: str) -> Dict:
        """
        Analyze all links in email content for security threats
        
        Args:
            html_content: HTML content of the email
            plain_text: Plain text content of the email
            
        Returns:
            Dictionary with analysis results
        """
        links = self._extract_links(html_content, plain_text)
        
        if not links:
            return {
                'status': 'safe',
                'score': 0,
                'details': ['Keine Links in der E-Mail gefunden'],
                'links': []
            }
        
        analysis_results = []
        total_score = 0
        max_score = len(links) * 100
        
        for link in links:
            link_analysis = self._analyze_single_link(link)
            analysis_results.append(link_analysis)
            total_score += link_analysis['score']
        
        # Calculate overall status
        avg_score = total_score / len(links) if links else 0
        
        if avg_score >= 80:
            status = 'critical'
        elif avg_score >= 60:
            status = 'danger'
        elif avg_score >= 30:
            status = 'warning'
        else:
            status = 'safe'
        
        return {
            'status': status,
            'score': int(avg_score),
            'details': self._generate_summary_details(analysis_results),
            'links': analysis_results
        }

    def _extract_links(self, html_content: str, plain_text: str) -> List[Dict]:
        """Extract all links from HTML and plain text"""
        links = []
        
        # Extract from HTML
        if html_content:
            # Find all <a> tags
            href_pattern = r'<a[^>]+href=["\']([^"\']+)["\'][^>]*>([^<]*)</a>'
            html_links = re.findall(href_pattern, html_content, re.IGNORECASE)
            
            for href, text in html_links:
                links.append({
                    'url': href,
                    'display_text': text.strip(),
                    'source': 'html'
                })
        
        # Extract from plain text
        if plain_text:
            # Find URLs in plain text
            url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
            text_links = re.findall(url_pattern, plain_text)
            
            for url in text_links:
                links.append({
                    'url': url,
                    'display_text': url,
                    'source': 'text'
                })
        
        return links

    def _analyze_single_link(self, link_data: Dict) -> Dict:
        """Analyze a single link for security threats"""
        url = link_data['url']
        display_text = link_data['display_text']
        
        # Basic URL validation
        if not url_validator(url):
            return {
                'url': url,
                'display_text': display_text,
                'status': 'critical',
                'score': 100,
                'details': ['Ungültige URL-Format'],
                'threats': ['invalid_url']
            }
        
        # Parse URL
        try:
            parsed_url = urlparse(url)
            domain = parsed_url.netloc.lower()
        except Exception as e:
            logger.error(f"Error parsing URL {url}: {e}")
            return {
                'url': url,
                'display_text': display_text,
                'status': 'critical',
                'score': 100,
                'details': ['URL konnte nicht geparst werden'],
                'threats': ['parse_error']
            }
        
        threats = []
        details = []
        score = 0
        
        # 1. Check for suspicious TLD
        if self._has_suspicious_tld(domain):
            threats.append('suspicious_tld')
            details.append(f'Verdächtige Top-Level-Domain: {self._get_tld(domain)}')
            score += 20
        
        # 2. Check for lookalike domains
        lookalike_result = self._check_lookalike_domain(domain)
        if lookalike_result['is_lookalike']:
            threats.append('lookalike_domain')
            details.append(f'Lookalike-Domain erkannt: {lookalike_result["original"]} → {domain}')
            score += 40
        
        # 3. Check for phishing keywords in URL
        phishing_keywords = self._check_phishing_keywords(url)
        if phishing_keywords:
            threats.append('phishing_keywords')
            details.append(f'Phishing-Keywords gefunden: {", ".join(phishing_keywords)}')
            score += 15
        
        # 4. Check for URL shortening services
        if self._is_url_shortener(domain):
            threats.append('url_shortener')
            details.append('URL-Shortener erkannt (kann versteckte Ziele haben)')
            score += 25
        
        # 5. Check for IP addresses instead of domains
        if self._is_ip_address(domain):
            threats.append('ip_address')
            details.append('IP-Adresse statt Domain verwendet')
            score += 30
        
        # 6. Check for mismatched display text
        if self._check_display_text_mismatch(url, display_text):
            threats.append('text_mismatch')
            details.append('Link-Text stimmt nicht mit Ziel-URL überein')
            score += 35
        
        # 7. Check for non-HTTPS
        if parsed_url.scheme != 'https':
            threats.append('non_https')
            details.append('Nicht-HTTPS Verbindung (unsicher)')
            score += 10
        
        # 8. Check for suspicious subdomains
        if self._has_suspicious_subdomain(domain):
            threats.append('suspicious_subdomain')
            details.append('Verdächtige Subdomain erkannt')
            score += 20
        
        # Determine status
        if score >= 80:
            status = 'critical'
        elif score >= 60:
            status = 'danger'
        elif score >= 30:
            status = 'warning'
        else:
            status = 'safe'
        
        return {
            'url': url,
            'display_text': display_text,
            'status': status,
            'score': min(score, 100),
            'details': details,
            'threats': threats,
            'domain': domain,
            'parsed_url': {
                'scheme': parsed_url.scheme,
                'netloc': parsed_url.netloc,
                'path': parsed_url.path,
                'query': parsed_url.query
            }
        }

    def _has_suspicious_tld(self, domain: str) -> bool:
        """Check if domain has suspicious TLD"""
        tld = self._get_tld(domain)
        return tld in self.suspicious_tlds

    def _get_tld(self, domain: str) -> str:
        """Extract TLD from domain"""
        extracted = tldextract.extract(domain)
        return f".{extracted.suffix}"

    def _check_lookalike_domain(self, domain: str) -> Dict:
        """Check for lookalike domains using fuzzy matching"""
        extracted = tldextract.extract(domain)
        domain_name = extracted.domain
        
        for brand in self.brand_names:
            # Check for exact substring matches
            if brand in domain_name and domain_name != brand:
                similarity = fuzz.ratio(domain_name, brand)
                if similarity >= 70:  # 70% similarity threshold
                    return {
                        'is_lookalike': True,
                        'original': brand,
                        'similarity': similarity
                    }
            
            # Check for character substitutions
            if len(domain_name) == len(brand):
                similarity = fuzz.ratio(domain_name, brand)
                if similarity >= 80:
                    return {
                        'is_lookalike': True,
                        'original': brand,
                        'similarity': similarity
                    }
        
        return {'is_lookalike': False}

    def _check_phishing_keywords(self, url: str) -> List[str]:
        """Check for phishing keywords in URL"""
        url_lower = url.lower()
        found_keywords = []
        
        for keyword in self.phishing_keywords:
            if keyword in url_lower:
                found_keywords.append(keyword)
        
        return found_keywords

    def _is_url_shortener(self, domain: str) -> bool:
        """Check if domain is a URL shortener"""
        shorteners = {
            'bit.ly', 'tinyurl.com', 'goo.gl', 't.co', 'is.gd',
            'v.gd', 'ow.ly', 'su.pr', 'twurl.nl', 'snipurl.com',
            'short.to', 'BudURL.com', 'ping.fm', 'tr.im', 'zip.net'
        }
        return domain in shorteners

    def _is_ip_address(self, domain: str) -> bool:
        """Check if domain is an IP address"""
        ip_pattern = r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
        return bool(re.match(ip_pattern, domain))

    def _check_display_text_mismatch(self, url: str, display_text: str) -> bool:
        """Check if display text doesn't match URL"""
        if not display_text or display_text == url:
            return False
        
        # Extract domain from URL
        try:
            parsed_url = urlparse(url)
            url_domain = parsed_url.netloc.lower()
        except:
            return False
        
        # Check if display text contains the domain
        return url_domain not in display_text.lower()

    def _has_suspicious_subdomain(self, domain: str) -> bool:
        """Check for suspicious subdomains"""
        extracted = tldextract.extract(domain)
        subdomain = extracted.subdomain.lower()
        
        suspicious_subdomains = {
            'secure', 'login', 'signin', 'verify', 'confirm',
            'update', 'account', 'password', 'security',
            'banking', 'payment', 'urgent', 'immediate'
        }
        
        return subdomain in suspicious_subdomains

    def _generate_summary_details(self, analysis_results: List[Dict]) -> List[str]:
        """Generate summary details from all link analyses"""
        details = []
        
        critical_links = [r for r in analysis_results if r['status'] == 'critical']
        danger_links = [r for r in analysis_results if r['status'] == 'danger']
        
        if critical_links:
            details.append(f'{len(critical_links)} kritisch verdächtige Links gefunden')
        
        if danger_links:
            details.append(f'{len(danger_links)} gefährliche Links gefunden')
        
        # Count specific threats
        threat_counts = {}
        for result in analysis_results:
            for threat in result.get('threats', []):
                threat_counts[threat] = threat_counts.get(threat, 0) + 1
        
        for threat, count in threat_counts.items():
            threat_names = {
                'lookalike_domain': 'Lookalike-Domains',
                'phishing_keywords': 'Phishing-Keywords',
                'url_shortener': 'URL-Shortener',
                'ip_address': 'IP-Adressen',
                'text_mismatch': 'Text-URL-Mismatches',
                'non_https': 'Nicht-HTTPS Links',
                'suspicious_tld': 'Verdächtige TLDs'
            }
            details.append(f'{count}x {threat_names.get(threat, threat)}')
        
        return details 