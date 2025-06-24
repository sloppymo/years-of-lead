#!/usr/bin/env python3
"""
Hybrid Timeline Implementation for WILLOW Corpus
Adds safe, contextual timing information without making promises
"""

import json
import re
import random
from datetime import datetime
from typing import Dict, List, Tuple, Optional

class HybridTimelineImplementer:
    def __init__(self):
        # Service type to typical timeline mappings
        self.service_timelines = {
            'emergency': {
                'fire': {'range': '3-7 minutes', 'confidence': 'typically'},
                'police': {'range': '5-10 minutes', 'confidence': 'usually'},
                'ambulance': {'range': '5-12 minutes', 'confidence': 'typically'},
                '911': {'range': '3-10 minutes', 'confidence': 'typically'}
            },
            'urgent_repair': {
                'no_heat': {
                    'business_hours': {'range': '1-2 hours', 'confidence': 'often'},
                    'after_hours': {'range': '2-4 hours', 'confidence': 'typically'},
                    'weekend': {'range': '2-6 hours', 'confidence': 'usually'}
                },
                'no_water': {
                    'business_hours': {'range': '30-90 minutes', 'confidence': 'typically'},
                    'after_hours': {'range': '1-3 hours', 'confidence': 'often'},
                    'weekend': {'range': '2-4 hours', 'confidence': 'usually'}
                },
                'flooding': {
                    'any_time': {'range': '15-45 minutes', 'confidence': 'typically'}
                },
                'gas_leak': {
                    'any_time': {'range': '15-30 minutes', 'confidence': 'usually'}
                },
                'electrical': {
                    'business_hours': {'range': '1-3 hours', 'confidence': 'often'},
                    'after_hours': {'range': '2-4 hours', 'confidence': 'typically'}
                }
            },
            'standard_repair': {
                'default': {
                    'business_hours': {'range': '24-48 hours', 'confidence': 'typically'},
                    'submission_time': {'range': '1-3 business days', 'confidence': 'usually'}
                }
            },
            'maintenance': {
                'inspection': {'range': '3-5 business days', 'confidence': 'typically'},
                'routine': {'range': '5-7 business days', 'confidence': 'usually'},
                'scheduled': {'range': 'as scheduled', 'confidence': 'per appointment'}
            }
        }
        
        # Context-aware modifiers
        self.context_modifiers = {
            'weather': {
                'severe': 'Response times may be extended during severe weather',
                'snow': 'Winter conditions may affect response times',
                'heat_wave': 'High demand may impact response times'
            },
            'time_of_day': {
                'rush_hour': 'Traffic conditions may affect arrival times',
                'overnight': 'Limited staff overnight may affect non-emergency response',
                'holiday': 'Holiday schedules may impact service availability'
            },
            'building_factors': {
                'high_rise': 'Building access procedures may add time',
                'gated': 'Gate access coordination may be needed',
                'remote': 'Location may affect response times'
            }
        }
        
        # Safe phrasing templates
        self.timeline_phrases = {
            'emergency': [
                "Emergency services have been contacted and {confidence} arrive within {range}",
                "First responders are being dispatched - they {confidence} arrive within {range}",
                "{confidence} see emergency responders within {range} of dispatch"
            ],
            'urgent': [
                "Our emergency maintenance team {confidence} arrives within {range}",
                "Urgent repair crews {confidence} respond within {range}",
                "We {confidence} have someone there within {range}"
            ],
            'standard': [
                "Maintenance {confidence} addresses this within {range}",
                "Repair work is {confidence} scheduled within {range}",
                "This type of issue is {confidence} resolved within {range}"
            ],
            'contextual': [
                "During {context}, {modifier}",
                "Please note: {modifier}",
                "Current conditions: {modifier}"
            ]
        }

    def identify_service_type(self, text: str) -> Tuple[str, str]:
        """Identify the primary service type and subtype from text"""
        text_lower = text.lower()
        
        # Check emergency keywords first
        emergency_keywords = {
            'fire': ['fire', 'smoke', 'burning'],
            'police': ['police', 'crime', 'break-in', 'assault'],
            'ambulance': ['medical', 'injury', 'hurt', 'sick', 'ambulance'],
            '911': ['emergency', '911', 'help immediately']
        }
        
        for service, keywords in emergency_keywords.items():
            if any(kw in text_lower for kw in keywords):
                return ('emergency', service)
        
        # Check urgent repairs
        urgent_keywords = {
            'no_heat': ['no heat', 'heat not working', 'freezing', 'heater broken'],
            'no_water': ['no water', 'water shut off', 'water not working'],
            'flooding': ['flooding', 'water everywhere', 'leak', 'burst pipe'],
            'gas_leak': ['gas', 'smell gas', 'gas leak'],
            'electrical': ['no power', 'electrical', 'sparks', 'outlet smoking']
        }
        
        for service, keywords in urgent_keywords.items():
            if any(kw in text_lower for kw in keywords):
                return ('urgent_repair', service)
        
        # Check maintenance
        if any(word in text_lower for word in ['inspect', 'check', 'routine', 'scheduled']):
            if 'scheduled' in text_lower:
                return ('maintenance', 'scheduled')
            elif 'routine' in text_lower:
                return ('maintenance', 'routine')
            else:
                return ('maintenance', 'inspection')
        
        # Default to standard repair
        return ('standard_repair', 'default')

    def get_time_context(self, text: str) -> str:
        """Determine time context from text"""
        text_lower = text.lower()
        
        # Time of day indicators
        if any(word in text_lower for word in ['night', 'midnight', '2am', '3am', 'overnight']):
            return 'after_hours'
        elif any(word in text_lower for word in ['weekend', 'saturday', 'sunday']):
            return 'weekend'
        elif any(word in text_lower for word in ['business hours', 'work day', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday']):
            return 'business_hours'
        
        # Default based on common patterns
        return 'business_hours'

    def get_contextual_modifiers(self, text: str) -> List[str]:
        """Get relevant context modifiers"""
        modifiers = []
        text_lower = text.lower()
        
        # Weather conditions
        if any(word in text_lower for word in ['storm', 'snow', 'ice', 'blizzard']):
            modifiers.append(self.context_modifiers['weather']['snow'])
        elif any(word in text_lower for word in ['heat wave', 'hot', 'sweltering']):
            modifiers.append(self.context_modifiers['weather']['heat_wave'])
        
        # Building factors
        if 'floor' in text_lower and any(word in text_lower for word in ['20', '30', 'high']):
            modifiers.append(self.context_modifiers['building_factors']['high_rise'])
        elif 'gate' in text_lower:
            modifiers.append(self.context_modifiers['building_factors']['gated'])
        
        return modifiers

    def create_timeline_statement(self, service_type: str, subtype: str, context: str) -> Optional[str]:
        """Create a safe timeline statement"""
        if service_type not in self.service_timelines:
            return None
            
        service_info = self.service_timelines[service_type].get(subtype, {})
        
        # Get appropriate timeline based on context
        if context in service_info:
            timeline = service_info[context]
        elif 'any_time' in service_info:
            timeline = service_info['any_time']
        else:
            # Try to find a default
            for key in ['business_hours', 'default']:
                if key in service_info:
                    timeline = service_info[key]
                    break
            else:
                return None
        
        if not timeline:
            return None
            
        # Select appropriate phrase template
        if service_type == 'emergency':
            templates = self.timeline_phrases['emergency']
        elif service_type == 'urgent_repair':
            templates = self.timeline_phrases['urgent']
        else:
            templates = self.timeline_phrases['standard']
        
        # Create statement
        template = random.choice(templates)
        statement = template.format(
            confidence=timeline['confidence'],
            range=timeline['range']
        )
        
        return statement

    def enhance_response_with_timeline(self, response: str, timeline_info: Dict) -> str:
        """Enhance response text with timeline information"""
        if not timeline_info or not timeline_info.get('statement'):
            return response
        
        # Find appropriate insertion point
        # Look for action statements
        action_patterns = [
            r'(I\'ve (?:notified|contacted|alerted|reached out to)[^.]+\.)',
            r'((?:Emergency|Maintenance|Our) (?:services|team|crew)[^.]+\.)',
            r'(I\'m (?:sending|dispatching|arranging)[^.]+\.)'
        ]
        
        for pattern in action_patterns:
            match = re.search(pattern, response)
            if match:
                # Insert timeline after the action statement
                insertion_point = match.end()
                enhanced = (
                    response[:insertion_point] + 
                    f" {timeline_info['statement']}. " +
                    response[insertion_point:]
                )
                
                # Add modifiers if any
                if timeline_info.get('modifiers'):
                    modifier_text = ' '.join([
                        f"Please note: {mod}" 
                        for mod in timeline_info['modifiers'][:1]  # Limit to one modifier
                    ])
                    enhanced += f" {modifier_text}."
                
                return enhanced
        
        # If no action statement found, append to appropriate section
        if "I want you to know" in response:
            # Insert before emotional support section
            parts = response.split("I want you to know")
            enhanced = (
                parts[0].rstrip() + 
                f" {timeline_info['statement']}.\n\nI want you to know" +
                "I want you to know".join(parts[1:])
            )
            return enhanced
        
        # Default: append before closing
        return response.rstrip() + f"\n\n{timeline_info['statement']}."

    def process_entry(self, entry: Dict) -> Dict:
        """Process a single corpus entry to add hybrid timelines"""
        enhanced_entry = entry.copy()
        
        tenant_input = entry.get('input', '')
        assistant_output = entry.get('output', '')
        
        # Identify service needs
        service_type, subtype = self.identify_service_type(tenant_input)
        
        # Get time context
        time_context = self.get_time_context(tenant_input)
        
        # Get contextual modifiers
        modifiers = self.get_contextual_modifiers(tenant_input)
        
        # Create timeline statement
        timeline_statement = self.create_timeline_statement(service_type, subtype, time_context)
        
        # Only enhance if we have a valid timeline and it's not already present
        if timeline_statement and 'typically' not in assistant_output.lower():
            timeline_info = {
                'statement': timeline_statement,
                'modifiers': modifiers,
                'service_type': service_type,
                'subtype': subtype,
                'context': time_context
            }
            
            # Enhance the response
            enhanced_output = self.enhance_response_with_timeline(assistant_output, timeline_info)
            enhanced_entry['output'] = enhanced_output
            
            # Add metadata
            if 'metadata' not in enhanced_entry:
                enhanced_entry['metadata'] = {}
            
            enhanced_entry['metadata']['timeline_added'] = {
                'version': '1.0',
                'service_type': service_type,
                'subtype': subtype,
                'context': time_context,
                'has_modifiers': len(modifiers) > 0,
                'timestamp': datetime.now().isoformat()
            }
        
        return enhanced_entry

    def process_corpus(self, input_file: str, output_file: str):
        """Process entire corpus with hybrid timelines"""
        print(f"Processing corpus: {input_file}")
        
        enhanced_entries = []
        stats = {
            'total': 0,
            'enhanced': 0,
            'by_service': {},
            'errors': 0
        }
        
        with open(input_file, 'r') as f:
            for line_num, line in enumerate(f, 1):
                if line.strip():
                    try:
                        entry = json.loads(line)
                        enhanced = self.process_entry(entry)
                        enhanced_entries.append(enhanced)
                        
                        stats['total'] += 1
                        
                        # Track if enhanced
                        if enhanced.get('metadata', {}).get('timeline_added'):
                            stats['enhanced'] += 1
                            service = enhanced['metadata']['timeline_added']['service_type']
                            stats['by_service'][service] = stats['by_service'].get(service, 0) + 1
                        
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
Hybrid Timeline Implementation Complete
======================================
Total Entries: {stats['total']}
Enhanced: {stats['enhanced']} ({stats['enhanced']/stats['total']*100:.1f}%)
Errors: {stats['errors']}

Enhanced by Service Type:
"""
        for service, count in sorted(stats['by_service'].items()):
            report += f"- {service}: {count}\n"
        
        report += f"\nOutput: {output_file}"
        
        print(report)
        
        # Save report
        report_file = output_file.replace('.jsonl', '_timeline_report.txt')
        with open(report_file, 'w') as f:
            f.write(report)
            
            # Add sample enhanced entries
            f.write("\n\nSample Enhanced Entries:\n")
            f.write("=" * 50 + "\n")
            
            sample_count = 0
            for entry in enhanced_entries:
                if entry.get('metadata', {}).get('timeline_added') and sample_count < 3:
                    f.write(f"\nEntry ID: {entry.get('id', 'Unknown')}\n")
                    f.write(f"Service Type: {entry['metadata']['timeline_added']['service_type']}\n")
                    f.write(f"Input: {entry['input'][:100]}...\n")
                    f.write(f"Enhanced Output: {entry['output'][:200]}...\n")
                    f.write("-" * 50 + "\n")
                    sample_count += 1
        
        return stats

if __name__ == "__main__":
    implementer = HybridTimelineImplementer()
    
    # Use the enhanced tags corpus as input
    input_corpus = "willow_corpus_enhanced_tags_20250624_021742.jsonl"
    output_corpus = f"willow_corpus_hybrid_timelines_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jsonl"
    
    stats = implementer.process_corpus(input_corpus, output_corpus)
    
    print(f"\nTimeline implementation complete! Check {output_corpus} for results.")