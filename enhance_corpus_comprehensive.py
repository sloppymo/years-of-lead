#!/usr/bin/env python3
"""
Comprehensive Corpus Enhancement Script
Transforms low-quality corpus entries into high-quality, A100-ready training data
"""

import json
import re
import random
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from collections import defaultdict

class ComprehensiveCorpusEnhancer:
    def __init__(self):
        # Tier 1 templates for emotional containment
        self.tier1_templates = {
            'opening': [
                "I'm here with you. {validation}",
                "I hear you, and {validation}",
                "Thank you for reaching out. {validation}",
                "{validation}, and I'm here to help navigate this together"
            ],
            'validation': [
                "what you're experiencing is completely unacceptable",
                "this situation is absolutely not okay",
                "you shouldn't have to deal with this",
                "your feelings about this are completely valid",
                "this is a serious issue that needs immediate attention"
            ],
            'breathing': [
                "Let's take a moment together. Can you take a slow breath with me? 🌊",
                "Before we continue, let's ground ourselves for just a moment. Notice three things you can see right now.",
                "I want to make sure you're in a safe space. Are you somewhere you feel secure right now?",
                "Let's pause together for just a second. Feel your feet on the floor if you can."
            ],
            'symbolic': {
                'water': "Like water finding its level 🌊",
                'mountain': "Steady as the mountain 🏔️",
                'tree': "Rooted like the ancient trees 🌲",
                'anchor': "Finding our anchor together ⚓"
            }
        }
        
        # Tier 2 action templates
        self.tier2_templates = {
            'emergency_action': [
                "I've immediately contacted our emergency maintenance team about {issue}.",
                "I've just notified our urgent response crew about {issue}.",
                "Our emergency team has been alerted and is mobilizing for {issue}."
            ],
            'standard_action': [
                "I've created a priority work order for {issue}.",
                "I've documented this issue and assigned it to our maintenance team.",
                "Your repair request for {issue} has been submitted with high priority."
            ],
            'timeline_safe': [
                "Response teams typically arrive within {timeframe}",
                "Our maintenance team usually addresses these issues within {timeframe}",
                "Based on similar situations, we often see resolution within {timeframe}"
            ],
            'follow_up': [
                "Your reference number is {ref_num}. This helps track everything.",
                "I've documented everything under case #{ref_num} for your records.",
                "Reference #{ref_num} - please keep this for any follow-up needs."
            ]
        }
        
        # Empowerment and choice language
        self.empowerment_language = {
            'choice': [
                "What would feel most helpful right now?",
                "Would you like me to also...",
                "You can decide if you'd prefer...",
                "What's your preference on..."
            ],
            'rights': [
                "You have the right to safe, habitable housing",
                "You're entitled to timely repairs for essential services",
                "Your rights as a tenant include...",
                "The law protects your right to..."
            ],
            'resources': [
                "There are additional resources available if needed",
                "I can connect you with tenant advocacy services",
                "Would information about emergency assistance be helpful?",
                "There are community resources that might help"
            ]
        }
        
        # Issue-specific responses
        self.issue_responses = {
            'no_heat': {
                'emergency': True,
                'timeline': '1-3 hours',
                'interim': "If you have space heaters available, those can help temporarily. Please use them safely - keep them 3 feet from anything flammable."
            },
            'no_water': {
                'emergency': True,
                'timeline': '30-90 minutes',
                'interim': "For immediate needs, there's emergency water available in the lobby. I can arrange for water delivery if needed."
            },
            'flooding': {
                'emergency': True,
                'timeline': '15-45 minutes',
                'interim': "Please move any valuables to higher ground if safe to do. If you can safely access the water shut-off valve, turning it clockwise will stop the flow."
            },
            'electrical': {
                'emergency': True,
                'timeline': '30-60 minutes',
                'interim': "Please avoid the affected area. If you smell burning or see sparks, evacuate immediately and call 911."
            },
            'pest': {
                'emergency': False,
                'timeline': '24-48 hours',
                'interim': "I understand how distressing this is. Our pest control team will need to do a thorough treatment."
            },
            'repair': {
                'emergency': False,
                'timeline': '1-3 business days',
                'interim': "I've marked this as a priority repair. Our team will coordinate with you on scheduling."
            }
        }

    def identify_issue_type(self, messages: List[Dict]) -> str:
        """Identify the primary issue from conversation"""
        tenant_messages = ' '.join([m['content'].lower() for m in messages if m.get('role') == 'tenant'])
        
        # Check for specific issues
        if any(term in tenant_messages for term in ['no heat', 'heat not working', 'freezing', 'heater broken']):
            return 'no_heat'
        elif any(term in tenant_messages for term in ['no water', 'water shut off', 'water not working']):
            return 'no_water'
        elif any(term in tenant_messages for term in ['flooding', 'water everywhere', 'leak', 'burst']):
            return 'flooding'
        elif any(term in tenant_messages for term in ['electrical', 'power', 'sparks', 'outlet']):
            return 'electrical'
        elif any(term in tenant_messages for term in ['pest', 'mice', 'roach', 'bug', 'rat']):
            return 'pest'
        else:
            return 'repair'

    def calculate_emotional_state(self, messages: List[Dict]) -> Dict[str, float]:
        """Calculate emotional state from messages"""
        tenant_msgs = [m for m in messages if m.get('role') == 'tenant']
        if not tenant_msgs:
            return {'arousal': 5.0, 'capacity': 5.0}
        
        # Use existing arousal/capacity if available
        last_tenant = tenant_msgs[-1]
        arousal = last_tenant.get('arousal', 5.0)
        capacity = last_tenant.get('capacity', 5.0)
        
        return {'arousal': arousal, 'capacity': capacity}

    def generate_tier1_response(self, issue_type: str, emotional_state: Dict[str, float]) -> str:
        """Generate a tier 1 emotional containment response"""
        # Select validation based on issue severity
        issue_info = self.issue_responses.get(issue_type, self.issue_responses['repair'])
        
        if issue_info['emergency']:
            validation = random.choice([
                "what you're experiencing is completely unacceptable",
                "this is an emergency situation that needs immediate attention",
                "this is absolutely not okay and I'm taking this very seriously"
            ])
        else:
            validation = random.choice(self.tier1_templates['validation'])
        
        # Build response
        opening = random.choice(self.tier1_templates['opening']).format(validation=validation)
        
        # Add breathing/grounding if high arousal
        response_parts = [opening]
        if emotional_state['arousal'] > 7:
            response_parts.append(random.choice(self.tier1_templates['breathing']))
        
        # Add symbolic element
        symbol_type = random.choice(list(self.tier1_templates['symbolic'].keys()))
        response_parts.append(self.tier1_templates['symbolic'][symbol_type])
        
        return '\n\n'.join(response_parts)

    def generate_tier2_response(self, issue_type: str, ref_num: str) -> str:
        """Generate a tier 2 action response"""
        issue_info = self.issue_responses.get(issue_type, self.issue_responses['repair'])
        
        response_parts = []
        
        # Action taken
        if issue_info['emergency']:
            action = random.choice(self.tier2_templates['emergency_action'])
        else:
            action = random.choice(self.tier2_templates['standard_action'])
        
        # Format action with issue type
        issue_desc = issue_type.replace('_', ' ')
        response_parts.append(action.format(issue=f"your {issue_desc} issue"))
        
        # Add timeline (safe language)
        timeline = random.choice(self.tier2_templates['timeline_safe'])
        response_parts.append(timeline.format(timeframe=issue_info['timeline']))
        
        # Add interim guidance if available
        if issue_info.get('interim'):
            response_parts.append(issue_info['interim'])
        
        # Add reference number
        ref_statement = random.choice(self.tier2_templates['follow_up'])
        response_parts.append(ref_statement.format(ref_num=ref_num))
        
        # Add empowerment element
        empowerment_type = random.choice(['choice', 'rights', 'resources'])
        empowerment = random.choice(self.empowerment_language[empowerment_type])
        response_parts.append(empowerment)
        
        return '\n\n'.join(response_parts)

    def enhance_single_entry(self, entry: Dict) -> Dict:
        """Enhance a single corpus entry"""
        enhanced = entry.copy()
        messages = enhanced.get('messages', [])
        
        if not messages:
            return enhanced
        
        # Identify issue and emotional state
        issue_type = self.identify_issue_type(messages)
        emotional_state = self.calculate_emotional_state(messages)
        
        # Find Willow messages to enhance
        for i, msg in enumerate(messages):
            if msg.get('role') == 'willow':
                # Determine tier
                tier = msg.get('tier', 'tier_1')
                
                if tier == 'tier_1':
                    # Generate tier 1 response
                    enhanced_content = self.generate_tier1_response(issue_type, emotional_state)
                else:
                    # Generate tier 2 response with reference number
                    ref_num = f"WR{random.randint(100000, 999999)}"
                    enhanced_content = self.generate_tier2_response(issue_type, ref_num)
                
                # Update message
                messages[i]['content'] = enhanced_content
                messages[i]['enhanced'] = True
                messages[i]['enhancement_version'] = '2.0'
        
        # Add metadata
        if 'metadata' not in enhanced:
            enhanced['metadata'] = {}
        
        enhanced['metadata']['enhancement'] = {
            'timestamp': datetime.now().isoformat(),
            'version': '2.0',
            'issue_type': issue_type,
            'emotional_state': emotional_state,
            'enhanced': True
        }
        
        return enhanced

    def process_corpus(self, input_file: str, output_file: str):
        """Process entire corpus with comprehensive enhancements"""
        print(f"Processing corpus: {input_file}")
        
        enhanced_entries = []
        stats = defaultdict(int)
        
        with open(input_file, 'r') as f:
            for line_num, line in enumerate(f, 1):
                if line.strip():
                    try:
                        entry = json.loads(line)
                        enhanced = self.enhance_single_entry(entry)
                        enhanced_entries.append(enhanced)
                        
                        stats['total_processed'] += 1
                        stats[f"issue_{enhanced['metadata']['enhancement']['issue_type']}"] += 1
                        
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
Comprehensive Enhancement Complete
==================================
Total Entries: {stats['total_processed']}
Errors: {stats['errors']}

Issues Processed:
"""
        for issue in ['no_heat', 'no_water', 'flooding', 'electrical', 'pest', 'repair']:
            count = stats.get(f'issue_{issue}', 0)
            report += f"- {issue}: {count}\n"
        
        report += f"\nOutput: {output_file}"
        
        print(report)
        
        # Save detailed report with examples
        report_file = output_file.replace('.jsonl', '_enhancement_report.txt')
        with open(report_file, 'w') as f:
            f.write(report)
            f.write("\n\nSample Enhanced Entries:\n")
            f.write("=" * 50 + "\n")
            
            # Show a few examples
            for i, entry in enumerate(enhanced_entries[:3]):
                f.write(f"\n\nExample {i+1}:\n")
                f.write("-" * 30 + "\n")
                f.write(f"ID: {entry.get('id', 'Unknown')}\n")
                f.write(f"Issue Type: {entry['metadata']['enhancement']['issue_type']}\n\n")
                
                for msg in entry.get('messages', []):
                    f.write(f"{msg.get('role').upper()}: {msg.get('content')}\n\n")
        
        return stats

    def validate_enhancement_quality(self, output_file: str):
        """Validate the quality of enhanced entries"""
        print(f"\nValidating enhancement quality...")
        
        quality_checks = defaultdict(int)
        
        with open(output_file, 'r') as f:
            for line in f:
                if line.strip():
                    entry = json.loads(line)
                    messages = entry.get('messages', [])
                    
                    for msg in messages:
                        if msg.get('role') == 'willow':
                            content = msg.get('content', '').lower()
                            
                            # Check for quality indicators
                            if 'i\'m here' in content or 'i hear you' in content:
                                quality_checks['has_empathy'] += 1
                            if 'i\'ve' in content and ('contacted' in content or 'notified' in content):
                                quality_checks['has_action'] += 1
                            if 'typically' in content or 'usually' in content:
                                quality_checks['has_safe_language'] += 1
                            if any(symbol in content for symbol in ['🌊', '🏔️', '🌲', '⚓']):
                                quality_checks['has_symbols'] += 1
                            if 'reference' in content or 'case #' in content:
                                quality_checks['has_reference'] += 1
                            
                            # Check for problems
                            if 'promise' in content or 'guarantee' in content:
                                quality_checks['has_promises'] += 1
                            if 'honey' in content or 'sweetie' in content:
                                quality_checks['has_infantilizing'] += 1
        
        # Print validation report
        total = quality_checks['has_empathy']  # Use one metric as proxy for total
        print(f"\nQuality Validation Results:")
        print(f"- Empathy expressions: {quality_checks['has_empathy']}")
        print(f"- Clear actions: {quality_checks['has_action']}")
        print(f"- Safe language: {quality_checks['has_safe_language']}")
        print(f"- Symbolic elements: {quality_checks['has_symbols']}")
        print(f"- Reference numbers: {quality_checks['has_reference']}")
        print(f"\nPotential Issues:")
        print(f"- Dangerous promises: {quality_checks['has_promises']}")
        print(f"- Infantilizing language: {quality_checks['has_infantilizing']}")

if __name__ == "__main__":
    enhancer = ComprehensiveCorpusEnhancer()
    
    # Use the quality metrics corpus as input
    input_corpus = "willow_corpus_quality_metrics_20250624_022136.jsonl"
    output_corpus = f"willow_corpus_enhanced_comprehensive_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jsonl"
    
    # Process corpus
    stats = enhancer.process_corpus(input_corpus, output_corpus)
    
    # Validate quality
    enhancer.validate_enhancement_quality(output_corpus)
    
    print(f"\nComprehensive enhancement complete! Check {output_corpus} for results.")