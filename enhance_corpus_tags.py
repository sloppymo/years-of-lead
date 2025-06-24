#!/usr/bin/env python3
"""
Enhanced Tagging System for WILLOW Corpus
Adds comprehensive metadata tags to improve A100 training quality
"""

import json
import re
from typing import Dict, List, Set, Optional, Any
from datetime import datetime
from collections import defaultdict

class CorpusTagEnhancer:
    def __init__(self):
        # Tenant state indicators
        self.panic_indicators = {
            'high': ['help', 'emergency', 'dying', 'can\'t breathe', 'scared', 'terrified'],
            'medium': ['worried', 'anxious', 'concerned', 'stressed', 'upset'],
            'low': ['wondering', 'checking', 'noticed', 'question']
        }
        
        # Vulnerability markers
        self.vulnerability_markers = {
            'disability': ['wheelchair', 'disabled', 'mobility', 'assistance', 'medical condition'],
            'elderly': ['elderly', 'senior', 'years old', 'retired'],
            'children': ['baby', 'child', 'kids', 'infant', 'toddler'],
            'health': ['medication', 'oxygen', 'medical equipment', 'health condition'],
            'financial': ['can\'t afford', 'fixed income', 'lost job', 'struggling']
        }
        
        # Required services
        self.service_types = {
            'emergency': ['911', 'fire', 'police', 'ambulance', 'immediate'],
            'urgent_repair': ['no heat', 'no water', 'flooding', 'electrical', 'gas leak'],
            'standard_repair': ['broken', 'not working', 'repair', 'fix'],
            'maintenance': ['check', 'inspect', 'routine', 'scheduled'],
            'information': ['how to', 'when', 'policy', 'question about']
        }
        
        # Legal risk areas
        self.legal_risks = {
            'habitability': ['uninhabitable', 'can\'t live', 'dangerous', 'unsafe'],
            'discrimination': ['because I\'m', 'treated differently', 'unfair', 'singled out'],
            'privacy': ['entered without', 'no notice', 'privacy', 'unauthorized'],
            'retaliation': ['after I complained', 'since I reported', 'punishment'],
            'ada': ['accommodation', 'disability', 'accessible', 'modification']
        }
        
        # Cultural indicators
        self.cultural_markers = {
            'language': ['english', 'translate', 'interpreter', 'don\'t understand'],
            'religious': ['religious', 'prayer', 'sabbath', 'holiday', 'dietary'],
            'family': ['extended family', 'cultural', 'tradition', 'customs']
        }
        
        # Time sensitivity
        self.time_critical = {
            'immediate': ['right now', 'immediately', 'emergency', 'urgent', 'asap'],
            'today': ['today', 'this morning', 'this afternoon', 'tonight'],
            'soon': ['soon', 'quickly', 'as soon as', 'when possible'],
            'scheduled': ['appointment', 'scheduled', 'planned', 'arranged']
        }

    def analyze_tenant_state(self, text: str) -> Dict[str, Any]:
        """Analyze emotional and cognitive state of tenant"""
        text_lower = text.lower()
        
        # Arousal level
        arousal_score = 0
        for level, keywords in self.panic_indicators.items():
            if any(kw in text_lower for kw in keywords):
                arousal_score = {'high': 9, 'medium': 5, 'low': 2}[level]
                break
        
        # Coherence assessment
        coherence_markers = {
            'organized': len(text.split('.')) > 1 and len(text.split()) > 20,
            'punctuated': bool(re.search(r'[.!?]', text)),
            'capitalized': bool(re.search(r'^[A-Z]', text)),
            'complete_sentences': not text.startswith('...') and not text.endswith('...')
        }
        coherence_score = sum(coherence_markers.values()) * 2.5
        
        # Capacity indicators
        capacity_markers = {
            'solution_focused': any(word in text_lower for word in ['tried', 'checked', 'looked']),
            'help_seeking': any(word in text_lower for word in ['please', 'help', 'need']),
            'detail_oriented': len(re.findall(r'\d+', text)) > 0,
            'time_aware': any(word in text_lower for word in ['yesterday', 'today', 'hour', 'minute'])
        }
        capacity_score = sum(capacity_markers.values()) * 2.5
        
        return {
            'arousal_level': arousal_score,
            'coherence_level': coherence_score,
            'capacity_level': capacity_score,
            'state_indicators': {
                'panic_level': 'high' if arousal_score > 7 else 'medium' if arousal_score > 4 else 'low',
                'organization': 'structured' if coherence_score > 7 else 'fragmented' if coherence_score < 4 else 'moderate',
                'engagement': 'proactive' if capacity_score > 7 else 'reactive' if capacity_score < 4 else 'cooperative'
            }
        }

    def identify_vulnerabilities(self, text: str) -> List[str]:
        """Identify vulnerability factors requiring special consideration"""
        text_lower = text.lower()
        vulnerabilities = []
        
        for vuln_type, markers in self.vulnerability_markers.items():
            if any(marker in text_lower for marker in markers):
                vulnerabilities.append(vuln_type)
        
        # Additional contextual vulnerabilities
        if 'alone' in text_lower or 'by myself' in text_lower:
            vulnerabilities.append('isolation')
        if 'night' in text_lower or 'dark' in text_lower:
            vulnerabilities.append('time_vulnerable')
        if re.search(r'\b(afraid|scared|fear)\b', text_lower):
            vulnerabilities.append('fear_based')
            
        return vulnerabilities

    def classify_service_needs(self, text: str) -> Dict[str, Any]:
        """Classify required services and urgency"""
        text_lower = text.lower()
        services = defaultdict(list)
        
        for service_type, keywords in self.service_types.items():
            for keyword in keywords:
                if keyword in text_lower:
                    services[service_type].append(keyword)
        
        # Prioritize services
        priority_order = ['emergency', 'urgent_repair', 'standard_repair', 'maintenance', 'information']
        primary_service = None
        for service in priority_order:
            if services[service]:
                primary_service = service
                break
                
        return {
            'primary_service': primary_service or 'information',
            'all_services': dict(services),
            'service_count': sum(len(v) for v in services.values())
        }

    def assess_legal_risks(self, text: str) -> Dict[str, Any]:
        """Identify potential legal liability areas"""
        text_lower = text.lower()
        risks = defaultdict(list)
        
        for risk_type, indicators in self.legal_risks.items():
            for indicator in indicators:
                if indicator in text_lower:
                    risks[risk_type].append(indicator)
        
        risk_score = sum(len(v) for v in risks.values())
        
        return {
            'risk_areas': dict(risks),
            'risk_score': min(risk_score * 2, 10),
            'high_risk': risk_score > 2,
            'risk_types': list(risks.keys())
        }

    def detect_cultural_factors(self, text: str) -> List[str]:
        """Detect cultural and linguistic considerations"""
        text_lower = text.lower()
        factors = []
        
        for factor_type, markers in self.cultural_markers.items():
            if any(marker in text_lower for marker in markers):
                factors.append(factor_type)
        
        # Language detection hints
        if re.search(r'[¿¡áéíóúñü]', text):
            factors.append('spanish_chars')
        if re.search(r'[\u4e00-\u9fff]', text):
            factors.append('chinese_chars')
        if re.search(r'[\u0600-\u06ff]', text):
            factors.append('arabic_chars')
            
        return factors

    def evaluate_time_sensitivity(self, text: str) -> Dict[str, Any]:
        """Evaluate urgency and time sensitivity"""
        text_lower = text.lower()
        
        sensitivity_level = 'routine'
        sensitivity_score = 0
        matched_indicators = []
        
        for level, indicators in self.time_critical.items():
            for indicator in indicators:
                if indicator in text_lower:
                    matched_indicators.append(indicator)
                    if level == 'immediate':
                        sensitivity_level = 'critical'
                        sensitivity_score = 10
                    elif level == 'today' and sensitivity_score < 8:
                        sensitivity_level = 'urgent'
                        sensitivity_score = 8
                    elif level == 'soon' and sensitivity_score < 5:
                        sensitivity_level = 'priority'
                        sensitivity_score = 5
        
        return {
            'sensitivity_level': sensitivity_level,
            'sensitivity_score': sensitivity_score,
            'time_indicators': matched_indicators,
            'requires_immediate_response': sensitivity_score >= 8
        }

    def generate_comprehensive_tags(self, entry: Dict) -> Dict:
        """Generate comprehensive tags for a corpus entry"""
        tenant_text = entry.get('input', '')
        assistant_text = entry.get('output', '')
        
        # Analyze tenant state
        tenant_state = self.analyze_tenant_state(tenant_text)
        
        # Identify vulnerabilities
        vulnerabilities = self.identify_vulnerabilities(tenant_text)
        
        # Classify services
        service_needs = self.classify_service_needs(tenant_text)
        
        # Assess legal risks
        legal_risks = self.assess_legal_risks(tenant_text)
        
        # Detect cultural factors
        cultural_factors = self.detect_cultural_factors(tenant_text)
        
        # Evaluate time sensitivity
        time_sensitivity = self.evaluate_time_sensitivity(tenant_text)
        
        # Analyze assistant response quality
        response_tier = 1 if 'breathing' in assistant_text.lower() or 'notice' in assistant_text.lower() else 2
        uses_symbols = bool(re.search(r'[🌊🏔️❄️🌲⚓]', assistant_text))
        maintains_boundaries = 'promise' not in assistant_text.lower() and 'guarantee' not in assistant_text.lower()
        
        # Create enhanced entry
        enhanced_entry = entry.copy()
        enhanced_entry['tags'] = {
            'tenant_state': tenant_state,
            'vulnerabilities': vulnerabilities,
            'service_needs': service_needs,
            'legal_risks': legal_risks,
            'cultural_factors': cultural_factors,
            'time_sensitivity': time_sensitivity,
            'response_analysis': {
                'tier': response_tier,
                'uses_symbols': uses_symbols,
                'maintains_boundaries': maintains_boundaries,
                'word_count': len(assistant_text.split())
            },
            'metadata': {
                'tagged_date': datetime.now().isoformat(),
                'tag_version': '2.0',
                'requires_review': legal_risks['high_risk'] or time_sensitivity['requires_immediate_response']
            }
        }
        
        return enhanced_entry

    def process_corpus(self, input_file: str, output_file: str):
        """Process entire corpus with enhanced tags"""
        print(f"Processing corpus: {input_file}")
        
        enhanced_entries = []
        stats = defaultdict(int)
        
        with open(input_file, 'r') as f:
            for line_num, line in enumerate(f, 1):
                if line.strip():
                    try:
                        entry = json.loads(line)
                        enhanced = self.generate_comprehensive_tags(entry)
                        enhanced_entries.append(enhanced)
                        
                        # Collect statistics
                        stats['total_processed'] += 1
                        stats[f"tier_{enhanced['tags']['response_analysis']['tier']}"] += 1
                        if enhanced['tags']['vulnerabilities']:
                            stats['has_vulnerabilities'] += 1
                        if enhanced['tags']['legal_risks']['high_risk']:
                            stats['high_legal_risk'] += 1
                        if enhanced['tags']['time_sensitivity']['requires_immediate_response']:
                            stats['immediate_response'] += 1
                        
                        if line_num % 100 == 0:
                            print(f"Processed {line_num} entries...")
                            
                    except Exception as e:
                        print(f"Error processing line {line_num}: {e}")
                        stats['errors'] += 1
        
        # Write enhanced corpus
        with open(output_file, 'w') as f:
            for entry in enhanced_entries:
                f.write(json.dumps(entry, ensure_ascii=False) + '\n')
        
        # Generate report
        report = f"""
Enhanced Tagging Complete
========================
Total Entries: {stats['total_processed']}
Errors: {stats['errors']}

Response Tiers:
- Tier 1: {stats['tier_1']} ({stats['tier_1']/stats['total_processed']*100:.1f}%)
- Tier 2: {stats['tier_2']} ({stats['tier_2']/stats['total_processed']*100:.1f}%)

Special Considerations:
- With Vulnerabilities: {stats['has_vulnerabilities']} ({stats['has_vulnerabilities']/stats['total_processed']*100:.1f}%)
- High Legal Risk: {stats['high_legal_risk']} ({stats['high_legal_risk']/stats['total_processed']*100:.1f}%)
- Immediate Response: {stats['immediate_response']} ({stats['immediate_response']/stats['total_processed']*100:.1f}%)

Output: {output_file}
"""
        print(report)
        
        # Save report
        report_file = output_file.replace('.jsonl', '_tag_report.txt')
        with open(report_file, 'w') as f:
            f.write(report)
            f.write("\n\nSample Enhanced Entry:\n")
            f.write(json.dumps(enhanced_entries[0], indent=2))
        
        return stats

if __name__ == "__main__":
    enhancer = CorpusTagEnhancer()
    
    # Process the main corpus
    input_corpus = "willow_corpus_complete_final_no_time_promises_20250624_015146.jsonl"
    output_corpus = f"willow_corpus_enhanced_tags_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jsonl"
    
    stats = enhancer.process_corpus(input_corpus, output_corpus)
    
    print(f"\nEnhancement complete! Check {output_corpus} for results.")