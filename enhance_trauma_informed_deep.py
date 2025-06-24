#!/usr/bin/env python3
"""
Deep Trauma-Informed Enhancement for WILLOW Corpus
Implements all 5 trauma-informed principles systematically
"""

import json
import re
import random
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from collections import defaultdict

class TraumaInformedEnhancer:
    def __init__(self):
        # Five core principles of trauma-informed care
        self.principles = {
            'safety': {
                'physical': [
                    "First, I want to ensure you're physically safe right now.",
                    "Your immediate safety is my primary concern.",
                    "Are you in a secure location where you feel protected?",
                    "Let's make sure you're safe before we proceed."
                ],
                'emotional': [
                    "I'm here to support you through this difficult situation.",
                    "Your feelings are valid and I'm listening without judgment.",
                    "This is a safe space to share what you're experiencing.",
                    "I recognize how overwhelming this must feel."
                ]
            },
            'trustworthiness': {
                'transparency': [
                    "Let me explain exactly what I can do and what the process involves.",
                    "Here's what will happen step by step, with realistic timeframes.",
                    "I'll be completely transparent about what to expect.",
                    "I want to be clear about both what I can and cannot do."
                ],
                'consistency': [
                    "You can count on me to follow through on these actions.",
                    "I'll keep you updated at each stage of the process.",
                    "My commitment to helping you remains constant.",
                    "You'll receive consistent updates as things progress."
                ]
            },
            'peer_support': {
                'connection': [
                    "You're not alone in dealing with this.",
                    "Many tenants have successfully navigated similar situations.",
                    "There's a community of support available to you.",
                    "Others have found these resources helpful in similar circumstances."
                ],
                'resources': [
                    "I can connect you with tenant advocacy groups if that would help.",
                    "There are peer support services available for situations like this.",
                    "Would you like information about community resources?",
                    "Local support groups have experience with these challenges."
                ]
            },
            'collaboration': {
                'shared_decisions': [
                    "What approach would work best for your situation?",
                    "Let's figure out the best path forward together.",
                    "Your input is essential in determining our next steps.",
                    "How would you prefer we handle this?"
                ],
                'mutual_respect': [
                    "I respect your perspective and want to understand your priorities.",
                    "Your expertise about your own situation guides our approach.",
                    "We're partners in resolving this issue.",
                    "Your voice matters in every decision we make."
                ]
            },
            'empowerment': {
                'choice': [
                    "You have several options available - let me outline them.",
                    "The choice of how to proceed is ultimately yours.",
                    "You're in control of which path we take.",
                    "Here are your options, and you can decide what feels right."
                ],
                'voice': [
                    "Your concerns deserve to be heard and addressed.",
                    "Speaking up about this took courage, and I honor that.",
                    "Your voice is powerful in advocating for your needs.",
                    "You have every right to express what you need."
                ],
                'strengths': [
                    "You're already taking positive steps by reaching out.",
                    "Your resilience in this situation is evident.",
                    "You've shown great strength in handling this so far.",
                    "The fact that you're advocating for yourself is powerful."
                ]
            }
        }
        
        # Tier-specific implementation
        self.tier_implementation = {
            'tier_1': ['safety', 'trustworthiness', 'collaboration'],
            'tier_2': ['empowerment', 'peer_support', 'trustworthiness']
        }
        
        # Issue-specific trauma considerations
        self.issue_trauma_focus = {
            'no_heat': {
                'primary': 'safety',
                'secondary': 'empowerment',
                'specific': "I understand how the cold affects both physical and emotional well-being."
            },
            'flooding': {
                'primary': 'safety',
                'secondary': 'peer_support',
                'specific': "Water damage can feel violating - your space has been disrupted."
            },
            'noise': {
                'primary': 'empowerment',
                'secondary': 'collaboration',
                'specific': "Chronic noise affects sleep and mental health - this is serious."
            },
            'mold': {
                'primary': 'safety',
                'secondary': 'trustworthiness',
                'specific': "Health concerns, especially for children, require urgent attention."
            }
        }

    def analyze_trauma_indicators(self, messages: List[Dict]) -> Dict[str, Any]:
        """Analyze messages for trauma indicators"""
        tenant_messages = [m['content'].lower() for m in messages if m.get('role') == 'tenant']
        all_text = ' '.join(tenant_messages)
        
        indicators = {
            'high_distress': any(word in all_text for word in ['cant breathe', 'dying', 'emergency', 'help me']),
            'vulnerability': any(word in all_text for word in ['baby', 'elderly', 'disabled', 'sick']),
            'past_trauma': any(word in all_text for word in ['again', 'always', 'never listen', 'no one cares']),
            'isolation': any(word in all_text for word in ['alone', 'no one', 'nobody helps']),
            'powerlessness': any(word in all_text for word in ['cant', 'nothing works', 'given up', 'hopeless'])
        }
        
        # Calculate trauma sensitivity level
        sensitivity_score = sum(indicators.values())
        sensitivity_level = 'high' if sensitivity_score >= 3 else 'moderate' if sensitivity_score >= 1 else 'low'
        
        return {
            'indicators': indicators,
            'sensitivity_level': sensitivity_level,
            'primary_need': self.identify_primary_need(indicators)
        }

    def identify_primary_need(self, indicators: Dict[str, bool]) -> str:
        """Identify primary trauma-informed need based on indicators"""
        if indicators['high_distress'] or indicators['vulnerability']:
            return 'safety'
        elif indicators['past_trauma'] or indicators['powerlessness']:
            return 'empowerment'
        elif indicators['isolation']:
            return 'peer_support'
        else:
            return 'collaboration'

    def select_principle_responses(self, principles_needed: List[str], 
                                  trauma_analysis: Dict[str, Any]) -> Dict[str, str]:
        """Select appropriate responses for each principle"""
        selected = {}
        
        for principle in principles_needed:
            if principle == 'safety':
                # Prioritize based on distress level
                if trauma_analysis['indicators']['high_distress']:
                    selected[principle] = random.choice(self.principles['safety']['physical'])
                else:
                    selected[principle] = random.choice(self.principles['safety']['emotional'])
            
            elif principle == 'trustworthiness':
                selected[principle] = random.choice(self.principles['trustworthiness']['transparency'])
            
            elif principle == 'peer_support':
                if trauma_analysis['indicators']['isolation']:
                    selected[principle] = random.choice(self.principles['peer_support']['connection'])
                else:
                    selected[principle] = random.choice(self.principles['peer_support']['resources'])
            
            elif principle == 'collaboration':
                selected[principle] = random.choice(self.principles['collaboration']['shared_decisions'])
            
            elif principle == 'empowerment':
                if trauma_analysis['indicators']['powerlessness']:
                    selected[principle] = random.choice(self.principles['empowerment']['voice'])
                else:
                    selected[principle] = random.choice(self.principles['empowerment']['choice'])
        
        return selected

    def enhance_response_with_trauma_principles(self, content: str, tier: str, 
                                              trauma_analysis: Dict[str, Any],
                                              issue_type: str) -> str:
        """Enhance response with trauma-informed principles"""
        # Get principles for this tier
        principles_needed = self.tier_implementation.get(tier, ['safety', 'empowerment'])
        
        # Adjust based on trauma analysis
        if trauma_analysis['sensitivity_level'] == 'high':
            # Always include safety for high sensitivity
            if 'safety' not in principles_needed:
                principles_needed.insert(0, 'safety')
        
        # Get principle responses
        principle_responses = self.select_principle_responses(principles_needed, trauma_analysis)
        
        # Structure the enhanced response
        enhanced_parts = []
        
        # For tier 1, start with safety if high distress
        if tier == 'tier_1' and trauma_analysis['sensitivity_level'] == 'high':
            if 'safety' in principle_responses:
                enhanced_parts.append(principle_responses['safety'])
                del principle_responses['safety']
        
        # Add existing content (but enhanced)
        if content:
            # Look for places to integrate principles
            lines = content.split('\n')
            integrated = False
            
            for i, line in enumerate(lines):
                # After empathy statement, add trustworthiness
                if i == 0 and 'trustworthiness' in principle_responses:
                    lines.insert(1, principle_responses['trustworthiness'])
                    del principle_responses['trustworthiness']
                    integrated = True
                    break
            
            enhanced_parts.extend(lines)
        
        # Add remaining principles
        for principle, response in principle_responses.items():
            enhanced_parts.append(response)
        
        # Add issue-specific trauma acknowledgment if applicable
        if issue_type in self.issue_trauma_focus:
            enhanced_parts.append(self.issue_trauma_focus[issue_type]['specific'])
        
        # For tier 2, always end with empowerment
        if tier == 'tier_2':
            empowerment_close = random.choice(self.principles['empowerment']['strengths'])
            enhanced_parts.append(empowerment_close)
        
        # Join with appropriate spacing
        enhanced = '\n\n'.join([part for part in enhanced_parts if part.strip()])
        
        return enhanced

    def process_entry(self, entry: Dict) -> Dict:
        """Process entry with deep trauma-informed enhancement"""
        enhanced = entry.copy()
        messages = enhanced.get('messages', [])
        
        # Analyze trauma indicators
        trauma_analysis = self.analyze_trauma_indicators(messages)
        
        # Detect issue type
        issue_type = enhanced.get('metadata', {}).get('enhancement', {}).get('issue_type', 'standard')
        
        # Process each Willow message
        changes_made = False
        for i, msg in enumerate(messages):
            if msg.get('role') == 'willow':
                tier = msg.get('tier', 'tier_1')
                original_content = msg.get('content', '')
                
                enhanced_content = self.enhance_response_with_trauma_principles(
                    original_content, tier, trauma_analysis, issue_type
                )
                
                if enhanced_content != original_content:
                    messages[i]['content'] = enhanced_content
                    messages[i]['trauma_enhanced'] = True
                    messages[i]['trauma_principles'] = self.tier_implementation[tier]
                    changes_made = True
        
        # Add metadata
        if changes_made:
            if 'metadata' not in enhanced:
                enhanced['metadata'] = {}
            
            enhanced['metadata']['trauma_enhancement'] = {
                'timestamp': datetime.now().isoformat(),
                'sensitivity_level': trauma_analysis['sensitivity_level'],
                'primary_need': trauma_analysis['primary_need'],
                'indicators': trauma_analysis['indicators'],
                'version': '2.0'
            }
        
        return enhanced

    def process_corpus(self, input_file: str, output_file: str):
        """Process corpus with deep trauma-informed enhancement"""
        print(f"Applying deep trauma-informed enhancement to: {input_file}")
        
        enhanced_entries = []
        stats = defaultdict(int)
        sensitivity_distribution = defaultdict(int)
        
        with open(input_file, 'r') as f:
            for line_num, line in enumerate(f, 1):
                if line.strip():
                    try:
                        entry = json.loads(line)
                        enhanced = self.process_entry(entry)
                        enhanced_entries.append(enhanced)
                        
                        stats['total'] += 1
                        if enhanced.get('metadata', {}).get('trauma_enhancement'):
                            stats['enhanced'] += 1
                            level = enhanced['metadata']['trauma_enhancement']['sensitivity_level']
                            sensitivity_distribution[level] += 1
                        
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
        self.generate_report(stats, sensitivity_distribution, output_file)
        
        return stats

    def generate_report(self, stats: Dict, sensitivity_dist: Dict, output_file: str):
        """Generate trauma-informed enhancement report"""
        report = f"""
Deep Trauma-Informed Enhancement Complete
=========================================
Total Entries: {stats['total']}
Enhanced: {stats['enhanced']} ({stats['enhanced']/max(stats['total'],1)*100:.1f}%)
Errors: {stats['errors']}

Trauma Sensitivity Distribution:
- High Sensitivity: {sensitivity_dist['high']} ({sensitivity_dist['high']/max(stats['enhanced'],1)*100:.1f}%)
- Moderate Sensitivity: {sensitivity_dist['moderate']} ({sensitivity_dist['moderate']/max(stats['enhanced'],1)*100:.1f}%)
- Low Sensitivity: {sensitivity_dist['low']} ({sensitivity_dist['low']/max(stats['enhanced'],1)*100:.1f}%)

All 5 Trauma-Informed Principles Implemented:
1. Safety (Physical & Emotional)
2. Trustworthiness & Transparency
3. Peer Support
4. Collaboration & Mutuality
5. Empowerment, Voice & Choice

Output: {output_file}
"""
        print(report)
        
        # Save detailed report
        report_file = output_file.replace('.jsonl', '_trauma_report.txt')
        with open(report_file, 'w') as f:
            f.write(report)
            f.write("\n\nImplementation Details:\n")
            f.write("- Tier 1 focuses on: Safety, Trustworthiness, Collaboration\n")
            f.write("- Tier 2 focuses on: Empowerment, Peer Support, Trustworthiness\n")
            f.write("- High distress triggers immediate safety responses\n")
            f.write("- Powerlessness triggers empowerment focus\n")
            f.write("- Isolation triggers peer support connections\n")

if __name__ == "__main__":
    enhancer = TraumaInformedEnhancer()
    
    # Process ETA-enhanced corpus
    input_file = "willow_corpus_eta_enhanced_20250624_023528.jsonl"
    output_file = f"willow_corpus_trauma_enhanced_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jsonl"
    
    stats = enhancer.process_corpus(input_file, output_file)
    
    print(f"\nTrauma-informed enhancement complete! Output: {output_file}")