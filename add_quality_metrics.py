#!/usr/bin/env python3
"""
Quality Metrics Addition for WILLOW Corpus
Adds comprehensive quality scoring to each corpus entry
"""

import json
import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from collections import defaultdict

class QualityMetricsAnalyzer:
    def __init__(self):
        # Empathy indicators
        self.empathy_markers = {
            'validation': [
                'i hear you', 'i understand', 'that must be', 'completely understand',
                'absolutely', 'of course', 'naturally', 'i can imagine'
            ],
            'acknowledgment': [
                'unacceptable', 'not okay', 'shouldn\'t have to', 'deserve better',
                'right to', 'valid concern', 'legitimate'
            ],
            'presence': [
                'i\'m here', 'with you', 'not alone', 'by your side',
                'together', 'support you', 'care about'
            ],
            'emotional_mirroring': [
                'frustrating', 'difficult', 'challenging', 'overwhelming',
                'stressful', 'concerning', 'worrying'
            ]
        }
        
        # Action clarity indicators
        self.action_clarity = {
            'specific_actions': [
                'i\'ve contacted', 'i\'ve notified', 'i\'ve sent', 'i\'ve arranged',
                'i\'m calling', 'i\'m dispatching', 'i\'ve documented'
            ],
            'clear_next_steps': [
                'next step', 'what happens now', 'here\'s what', 'process is',
                'timeline', 'expect', 'will happen'
            ],
            'contact_info': [
                'reference number', 'case number', 'contact', 'reach',
                'phone', 'email', 'available'
            ]
        }
        
        # Legal safety indicators
        self.legal_safety = {
            'dangerous_promises': [
                'i promise', 'i guarantee', 'definitely will', 'absolutely will',
                'for sure', 'without fail', 'no matter what'
            ],
            'safe_language': [
                'typically', 'usually', 'often', 'working to', 'aiming to',
                'our goal', 'we strive', 'process includes'
            ],
            'boundary_maintenance': [
                'i wish i could', 'if i could', 'beyond my ability',
                'can\'t directly', 'not able to', 'outside my scope'
            ]
        }
        
        # Urgency appropriateness
        self.urgency_response = {
            'emergency_keywords': [
                'fire', 'gas', 'flood', 'no heat', 'no water', 'electrical',
                'smoke', 'sparks', 'medical', 'injury', 'safety'
            ],
            'emergency_actions': [
                '911', 'emergency', 'immediately', 'urgent', 'priority',
                'right away', 'dispatched', 'on their way'
            ],
            'de_escalation': [
                'safe place', 'breathing', 'moment', 'step back',
                'one thing at a time', 'focus on', 'right now'
            ]
        }
        
        # Cultural sensitivity markers
        self.cultural_sensitivity = {
            'inclusive_language': [
                'your family', 'your needs', 'your situation', 'respect',
                'understand your', 'cultural', 'religious', 'dietary'
            ],
            'avoiding_assumptions': [
                'if you\'re comfortable', 'would you prefer', 'let me know',
                'your preference', 'what works for you'
            ]
        }
        
        # Trauma-informed indicators
        self.trauma_informed = {
            'safety': [
                'safe', 'secure', 'protected', 'safety first',
                'well-being', 'take care of yourself'
            ],
            'choice': [
                'your choice', 'you decide', 'up to you', 'when you\'re ready',
                'at your pace', 'your comfort', 'your preference'
            ],
            'collaboration': [
                'work together', 'partner with', 'alongside', 'with you',
                'your input', 'your thoughts', 'what do you think'
            ],
            'transparency': [
                'here\'s what', 'process is', 'timeline', 'to be clear',
                'full picture', 'honest', 'transparent'
            ],
            'empowerment': [
                'your rights', 'you can', 'your power', 'advocate',
                'resources', 'options', 'choices available'
            ]
        }

    def calculate_empathy_score(self, text: str) -> Tuple[float, Dict[str, int]]:
        """Calculate empathy score based on language markers"""
        text_lower = text.lower()
        scores = defaultdict(int)
        
        for category, markers in self.empathy_markers.items():
            for marker in markers:
                if marker in text_lower:
                    scores[category] += 1
        
        # Weight different categories
        weighted_score = (
            scores['validation'] * 2.5 +
            scores['acknowledgment'] * 2.0 +
            scores['presence'] * 2.0 +
            scores['emotional_mirroring'] * 1.5
        )
        
        # Normalize to 0-10 scale
        final_score = min(10, weighted_score)
        
        return final_score, dict(scores)

    def calculate_action_clarity(self, text: str) -> Tuple[float, Dict[str, int]]:
        """Calculate how clear and actionable the response is"""
        text_lower = text.lower()
        scores = defaultdict(int)
        
        for category, markers in self.action_clarity.items():
            for marker in markers:
                if marker in text_lower:
                    scores[category] += 1
        
        # Weight categories
        weighted_score = (
            scores['specific_actions'] * 3.0 +
            scores['clear_next_steps'] * 2.5 +
            scores['contact_info'] * 1.5
        )
        
        # Normalize
        final_score = min(10, weighted_score * 1.5)
        
        return final_score, dict(scores)

    def calculate_legal_safety(self, text: str) -> Tuple[float, Dict[str, int]]:
        """Calculate legal safety score (higher is safer)"""
        text_lower = text.lower()
        scores = defaultdict(int)
        
        # Check for dangerous promises (negative points)
        for marker in self.legal_safety['dangerous_promises']:
            if marker in text_lower:
                scores['dangerous_promises'] += 1
        
        # Check for safe language (positive points)
        for marker in self.legal_safety['safe_language']:
            if marker in text_lower:
                scores['safe_language'] += 1
        
        # Check for boundary maintenance (positive points)
        for marker in self.legal_safety['boundary_maintenance']:
            if marker in text_lower:
                scores['boundary_maintenance'] += 1
        
        # Calculate score (penalize promises heavily)
        final_score = 10 - (scores['dangerous_promises'] * 3)
        final_score += scores['safe_language'] * 1.5
        final_score += scores['boundary_maintenance'] * 1.0
        
        # Ensure 0-10 range
        final_score = max(0, min(10, final_score))
        
        return final_score, dict(scores)

    def calculate_urgency_appropriateness(self, tenant_text: str, assistant_text: str) -> Tuple[float, Dict[str, int]]:
        """Calculate if urgency response matches the situation"""
        tenant_lower = tenant_text.lower()
        assistant_lower = assistant_text.lower()
        
        scores = defaultdict(int)
        
        # Detect emergency in tenant message
        emergency_level = 0
        for keyword in self.urgency_response['emergency_keywords']:
            if keyword in tenant_lower:
                emergency_level += 1
        
        # Check assistant response
        for action in self.urgency_response['emergency_actions']:
            if action in assistant_lower:
                scores['emergency_response'] += 1
        
        for technique in self.urgency_response['de_escalation']:
            if technique in assistant_lower:
                scores['de_escalation'] += 1
        
        # Calculate appropriateness
        if emergency_level > 2:  # High emergency
            final_score = min(10, scores['emergency_response'] * 3)
        elif emergency_level > 0:  # Some urgency
            final_score = min(10, scores['emergency_response'] * 2 + scores['de_escalation'])
        else:  # Non-emergency
            # Penalize over-reaction
            final_score = 10 - scores['emergency_response']
        
        return final_score, dict(scores)

    def calculate_cultural_sensitivity(self, text: str) -> Tuple[float, Dict[str, int]]:
        """Calculate cultural sensitivity score"""
        text_lower = text.lower()
        scores = defaultdict(int)
        
        for marker in self.cultural_sensitivity['inclusive_language']:
            if marker in text_lower:
                scores['inclusive'] += 1
        
        for marker in self.cultural_sensitivity['avoiding_assumptions']:
            if marker in text_lower:
                scores['non_assumptive'] += 1
        
        # Base score of 7 (neutral), can go up with positive markers
        final_score = 7.0
        final_score += scores['inclusive'] * 0.5
        final_score += scores['non_assumptive'] * 0.5
        
        final_score = min(10, final_score)
        
        return final_score, dict(scores)

    def calculate_trauma_informed_score(self, text: str) -> Tuple[float, Dict[str, int]]:
        """Calculate trauma-informed approach score"""
        text_lower = text.lower()
        scores = defaultdict(int)
        
        # Check all five principles
        for principle, markers in self.trauma_informed.items():
            for marker in markers:
                if marker in text_lower:
                    scores[principle] += 1
        
        # Equal weight to all principles
        total_indicators = sum(scores.values())
        principles_present = len([v for v in scores.values() if v > 0])
        
        # Score based on both coverage and depth
        final_score = (principles_present * 1.5) + (total_indicators * 0.3)
        final_score = min(10, final_score)
        
        return final_score, dict(scores)

    def analyze_conversation_quality(self, messages: List[Dict]) -> Dict[str, Any]:
        """Analyze the quality of an entire conversation"""
        # Find tenant and assistant messages
        tenant_messages = [m for m in messages if m.get('role') == 'tenant']
        assistant_messages = [m for m in messages if m.get('role') == 'willow']
        
        if not tenant_messages or not assistant_messages:
            return {
                'error': 'Missing tenant or assistant messages',
                'scores': {}
            }
        
        # Combine messages for analysis
        tenant_text = ' '.join([m.get('content', '') for m in tenant_messages])
        assistant_text = ' '.join([m.get('content', '') for m in assistant_messages])
        
        # Calculate all scores
        empathy_score, empathy_details = self.calculate_empathy_score(assistant_text)
        action_score, action_details = self.calculate_action_clarity(assistant_text)
        legal_score, legal_details = self.calculate_legal_safety(assistant_text)
        urgency_score, urgency_details = self.calculate_urgency_appropriateness(tenant_text, assistant_text)
        cultural_score, cultural_details = self.calculate_cultural_sensitivity(assistant_text)
        trauma_score, trauma_details = self.calculate_trauma_informed_score(assistant_text)
        
        # Calculate overall quality score
        overall_score = (
            empathy_score * 0.20 +
            action_score * 0.20 +
            legal_score * 0.25 +  # Higher weight for legal safety
            urgency_score * 0.15 +
            cultural_score * 0.10 +
            trauma_score * 0.10
        )
        
        return {
            'overall_score': round(overall_score, 2),
            'dimension_scores': {
                'empathy': round(empathy_score, 2),
                'action_clarity': round(action_score, 2),
                'legal_safety': round(legal_score, 2),
                'urgency_appropriateness': round(urgency_score, 2),
                'cultural_sensitivity': round(cultural_score, 2),
                'trauma_informed': round(trauma_score, 2)
            },
            'details': {
                'empathy': empathy_details,
                'action': action_details,
                'legal': legal_details,
                'urgency': urgency_details,
                'cultural': cultural_details,
                'trauma': trauma_details
            },
            'flags': {
                'has_promises': legal_details.get('dangerous_promises', 0) > 0,
                'low_empathy': empathy_score < 5,
                'unclear_actions': action_score < 5,
                'legal_risk': legal_score < 7,
                'urgency_mismatch': urgency_score < 5
            }
        }

    def process_entry(self, entry: Dict) -> Dict:
        """Process a single corpus entry to add quality metrics"""
        enhanced_entry = entry.copy()
        
        # Get messages
        messages = entry.get('messages', [])
        
        # Analyze quality
        quality_analysis = self.analyze_conversation_quality(messages)
        
        # Add quality metrics
        if 'metadata' not in enhanced_entry:
            enhanced_entry['metadata'] = {}
        
        enhanced_entry['metadata']['quality_metrics'] = {
            'version': '1.0',
            'timestamp': datetime.now().isoformat(),
            'scores': quality_analysis['dimension_scores'],
            'overall_score': quality_analysis['overall_score'],
            'flags': quality_analysis['flags'],
            'analysis_details': quality_analysis['details']
        }
        
        # Add quality tier
        overall = quality_analysis['overall_score']
        if overall >= 9.0:
            quality_tier = 'excellent'
        elif overall >= 8.0:
            quality_tier = 'good'
        elif overall >= 7.0:
            quality_tier = 'acceptable'
        elif overall >= 6.0:
            quality_tier = 'needs_improvement'
        else:
            quality_tier = 'poor'
        
        enhanced_entry['metadata']['quality_metrics']['quality_tier'] = quality_tier
        
        return enhanced_entry

    def process_corpus(self, input_file: str, output_file: str):
        """Process entire corpus with quality metrics"""
        print(f"Processing corpus: {input_file}")
        
        enhanced_entries = []
        stats = defaultdict(int)
        quality_distribution = defaultdict(int)
        
        with open(input_file, 'r') as f:
            for line_num, line in enumerate(f, 1):
                if line.strip():
                    try:
                        entry = json.loads(line)
                        enhanced = self.process_entry(entry)
                        enhanced_entries.append(enhanced)
                        
                        stats['total_processed'] += 1
                        
                        # Track quality distribution
                        quality_tier = enhanced['metadata']['quality_metrics']['quality_tier']
                        quality_distribution[quality_tier] += 1
                        
                        # Track flags
                        flags = enhanced['metadata']['quality_metrics']['flags']
                        for flag, value in flags.items():
                            if value:
                                stats[f'flag_{flag}'] += 1
                        
                        if line_num % 100 == 0:
                            print(f"Processed {line_num} entries...")
                            
                    except Exception as e:
                        print(f"Error processing line {line_num}: {e}")
                        stats['errors'] += 1
        
        # Write enhanced corpus
        with open(output_file, 'w') as f:
            for entry in enhanced_entries:
                f.write(json.dumps(entry, ensure_ascii=False) + '\n')
        
        # Calculate average scores
        total_scores = defaultdict(float)
        for entry in enhanced_entries:
            scores = entry['metadata']['quality_metrics']['scores']
            for dimension, score in scores.items():
                total_scores[dimension] += score
        
        avg_scores = {
            dim: round(total / stats['total_processed'], 2) 
            for dim, total in total_scores.items()
        }
        
        # Generate report
        report = f"""
Quality Metrics Analysis Complete
=================================
Total Entries: {stats['total_processed']}
Errors: {stats['errors']}

Quality Distribution:
"""
        for tier in ['excellent', 'good', 'acceptable', 'needs_improvement', 'poor']:
            count = quality_distribution[tier]
            pct = count / stats['total_processed'] * 100
            report += f"- {tier}: {count} ({pct:.1f}%)\n"
        
        report += f"\nAverage Scores by Dimension:\n"
        for dim, score in sorted(avg_scores.items()):
            report += f"- {dim}: {score}/10\n"
        
        report += f"\nQuality Flags:\n"
        for flag in ['has_promises', 'low_empathy', 'unclear_actions', 'legal_risk', 'urgency_mismatch']:
            count = stats.get(f'flag_{flag}', 0)
            pct = count / stats['total_processed'] * 100
            report += f"- {flag}: {count} ({pct:.1f}%)\n"
        
        report += f"\nOutput: {output_file}"
        
        print(report)
        
        # Save detailed report
        report_file = output_file.replace('.jsonl', '_quality_report.txt')
        with open(report_file, 'w') as f:
            f.write(report)
            
            # Add examples of each quality tier
            f.write("\n\nExamples by Quality Tier:\n")
            f.write("=" * 50 + "\n")
            
            for tier in ['excellent', 'good', 'needs_improvement']:
                f.write(f"\n{tier.upper()} Examples:\n")
                f.write("-" * 30 + "\n")
                
                count = 0
                for entry in enhanced_entries:
                    if entry['metadata']['quality_metrics']['quality_tier'] == tier and count < 2:
                        f.write(f"\nID: {entry.get('id', 'Unknown')}\n")
                        f.write(f"Overall Score: {entry['metadata']['quality_metrics']['overall_score']}\n")
                        f.write(f"Scores: {entry['metadata']['quality_metrics']['scores']}\n")
                        
                        # Get first tenant message
                        tenant_msg = next((m for m in entry.get('messages', []) if m.get('role') == 'tenant'), None)
                        if tenant_msg:
                            f.write(f"Tenant: {tenant_msg.get('content', '')[:100]}...\n")
                        
                        count += 1
        
        return stats, avg_scores

if __name__ == "__main__":
    analyzer = QualityMetricsAnalyzer()
    
    # Process the enhanced corpus
    import sys
    input_corpus = sys.argv[1] if len(sys.argv) > 1 else "willow_corpus_enhanced_comprehensive_20250624_022323.jsonl"
    output_corpus = f"willow_corpus_quality_metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jsonl"
    
    stats, avg_scores = analyzer.process_corpus(input_corpus, output_corpus)
    
    print(f"\nQuality analysis complete! Check {output_corpus} for results.")