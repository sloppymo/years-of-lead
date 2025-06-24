#!/usr/bin/env python3
"""
Add Specific ETAs to WILLOW Corpus
Implements specific response times for emergency services
"""

import json
import re
import random
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from collections import defaultdict

class SpecificETAEnhancer:
    def __init__(self):
        # Specific ETA ranges based on service type and context
        self.emergency_etas = {
            'police': {
                'urban': {'min': 3, 'max': 4, 'unit': 'minutes'},
                'suburban': {'min': 8, 'max': 12, 'unit': 'minutes'},
                'rural': {'min': 15, 'max': 25, 'unit': 'minutes'},
                'high_priority': {'min': 2, 'max': 3, 'unit': 'minutes'}
            },
            'fire': {
                'urban': {'min': 4, 'max': 6, 'unit': 'minutes'},
                'suburban': {'min': 10, 'max': 15, 'unit': 'minutes'},
                'rural': {'min': 20, 'max': 30, 'unit': 'minutes'},
                'high_priority': {'min': 3, 'max': 5, 'unit': 'minutes'}
            },
            'paramedics': {
                'urban': {'min': 6, 'max': 8, 'unit': 'minutes'},
                'suburban': {'min': 12, 'max': 18, 'unit': 'minutes'},
                'rural': {'min': 25, 'max': 35, 'unit': 'minutes'},
                'high_priority': {'min': 5, 'max': 7, 'unit': 'minutes'}
            },
            'building_security': {
                'any': {'min': 2, 'max': 3, 'unit': 'minutes'},
                'high_rise': {'min': 3, 'max': 5, 'unit': 'minutes'},
                'multi_building': {'min': 4, 'max': 6, 'unit': 'minutes'}
            },
            'emergency_maintenance': {
                'critical': {'min': 15, 'max': 30, 'unit': 'minutes'},
                'urgent': {'min': 30, 'max': 60, 'unit': 'minutes'},
                'standard': {'min': 60, 'max': 120, 'unit': 'minutes'}
            }
        }
        
        # Maintenance-specific ETAs
        self.maintenance_etas = {
            'no_heat': {
                'emergency': {'min': 30, 'max': 60, 'unit': 'minutes'},
                'standard': {'min': 1, 'max': 2, 'unit': 'hours'},
                'after_hours': {'min': 2, 'max': 4, 'unit': 'hours'}
            },
            'no_water': {
                'emergency': {'min': 20, 'max': 40, 'unit': 'minutes'},
                'standard': {'min': 45, 'max': 90, 'unit': 'minutes'}
            },
            'flooding': {
                'emergency': {'min': 10, 'max': 20, 'unit': 'minutes'},
                'water_damage': {'min': 30, 'max': 45, 'unit': 'minutes'}
            },
            'electrical': {
                'emergency': {'min': 20, 'max': 30, 'unit': 'minutes'},
                'standard': {'min': 1, 'max': 3, 'unit': 'hours'}
            },
            'gas_leak': {
                'emergency': {'min': 10, 'max': 15, 'unit': 'minutes'},
                'utility_company': {'min': 20, 'max': 30, 'unit': 'minutes'}
            }
        }
        
        # Context modifiers
        self.time_modifiers = {
            'rush_hour': 1.5,  # 50% longer during rush hour
            'overnight': 1.2,  # 20% longer overnight
            'weekend': 1.3,    # 30% longer on weekends
            'holiday': 1.5,    # 50% longer on holidays
            'severe_weather': 2.0  # Double during severe weather
        }

    def detect_issue_and_context(self, messages: List[Dict]) -> Tuple[str, str, List[str]]:
        """Detect the issue type and context from messages"""
        tenant_text = ' '.join([m['content'].lower() for m in messages if m.get('role') == 'tenant'])
        
        # Detect issue type
        issue_type = 'standard'
        if any(word in tenant_text for word in ['fire', 'smoke', 'burning']):
            issue_type = 'fire'
        elif any(word in tenant_text for word in ['police', 'crime', 'break-in', 'assault', 'threat']):
            issue_type = 'police'
        elif any(word in tenant_text for word in ['medical', 'injury', 'hurt', 'ambulance', 'sick', 'heart']):
            issue_type = 'paramedics'
        elif any(word in tenant_text for word in ['no heat', 'freezing', 'heater']):
            issue_type = 'no_heat'
        elif any(word in tenant_text for word in ['no water', 'water off']):
            issue_type = 'no_water'
        elif any(word in tenant_text for word in ['flood', 'leak', 'water everywhere']):
            issue_type = 'flooding'
        elif any(word in tenant_text for word in ['electrical', 'sparks', 'power out']):
            issue_type = 'electrical'
        elif any(word in tenant_text for word in ['gas', 'smell gas']):
            issue_type = 'gas_leak'
        
        # Detect location context
        location = 'urban'  # Default
        if any(word in tenant_text for word in ['suburbs', 'subdivision']):
            location = 'suburban'
        elif any(word in tenant_text for word in ['rural', 'country', 'farm']):
            location = 'rural'
        elif any(word in tenant_text for word in ['high rise', 'tower', 'floor 20', 'floor 30']):
            location = 'high_rise'
        
        # Detect time modifiers
        modifiers = []
        if any(word in tenant_text for word in ['rush hour', 'traffic', '5pm', '6pm', '8am']):
            modifiers.append('rush_hour')
        if any(word in tenant_text for word in ['night', 'midnight', '2am', '3am']):
            modifiers.append('overnight')
        if any(word in tenant_text for word in ['weekend', 'saturday', 'sunday']):
            modifiers.append('weekend')
        if any(word in tenant_text for word in ['storm', 'snow', 'ice', 'hurricane']):
            modifiers.append('severe_weather')
        
        return issue_type, location, modifiers

    def calculate_specific_eta(self, service_type: str, location: str, modifiers: List[str]) -> str:
        """Calculate specific ETA with modifiers"""
        # Get base ETA
        eta_data = None
        if service_type in self.emergency_etas:
            service_etas = self.emergency_etas[service_type]
            eta_data = service_etas.get(location, service_etas.get('urban'))
        elif service_type in self.maintenance_etas:
            service_etas = self.maintenance_etas[service_type]
            eta_data = service_etas.get('emergency', service_etas.get('standard'))
        
        # Default fallback if no data found
        if eta_data is None:
            eta_data = {'min': 30, 'max': 60, 'unit': 'minutes'}
        
        # Apply modifiers
        modifier_factor = 1.0
        for mod in modifiers:
            if mod in self.time_modifiers:
                modifier_factor *= self.time_modifiers[mod]
        
        # Calculate final ETA
        min_time = int(eta_data['min'] * modifier_factor)
        max_time = int(eta_data['max'] * modifier_factor)
        
        # Format based on urgency
        if service_type in ['police', 'fire', 'paramedics']:
            return f"{min_time}-{max_time} {eta_data['unit']}"
        else:
            # For non-emergency, use single estimate
            avg_time = (min_time + max_time) // 2
            return f"{avg_time} {eta_data['unit']}"

    def enhance_tier2_with_eta(self, content: str, issue_type: str, location: str, modifiers: List[str]) -> str:
        """Enhance tier 2 response with specific ETAs"""
        # Check if already has specific ETA
        if re.search(r'\d+-\d+ minutes', content):
            return content
        
        # Calculate appropriate ETA
        eta = self.calculate_specific_eta(issue_type, location, modifiers)
        
        # Find where to insert ETA
        enhanced = content
        
        # Pattern 1: After "Response teams typically arrive"
        pattern1 = r'(Response teams? typically arrive within )([^.]+)'
        if re.search(pattern1, enhanced):
            enhanced = re.sub(pattern1, f'\\1{eta}', enhanced)
            return enhanced
        
        # Pattern 2: After "Expected arrival"
        pattern2 = r'(Expected arrival: )([^.]+)'
        if re.search(pattern2, enhanced):
            enhanced = re.sub(pattern2, f'\\1{eta}', enhanced)
            return enhanced
        
        # Pattern 3: After emergency dispatch mention
        if 'dispatched' in enhanced.lower() or 'mobilizing' in enhanced.lower():
            # Add ETA information after dispatch mention
            lines = enhanced.split('\n')
            for i, line in enumerate(lines):
                if 'dispatch' in line.lower() or 'mobiliz' in line.lower():
                    # Determine service name
                    service_name = self.get_service_name(issue_type)
                    eta_statement = f"\n{service_name} ETA: {eta}"
                    
                    # Insert after current line
                    if i < len(lines) - 1:
                        lines.insert(i + 1, eta_statement)
                    else:
                        lines.append(eta_statement)
                    break
            
            enhanced = '\n'.join(lines)
            return enhanced
        
        # Pattern 4: Add to action list if present
        if 'Actions taken:' in enhanced or "I've completed the following" in enhanced:
            # Find the action list
            lines = enhanced.split('\n')
            for i, line in enumerate(lines):
                if re.match(r'^[•\-\d]', line.strip()) and 'team' in line.lower():
                    # Add ETA to this line
                    lines[i] = line.rstrip() + f' (ETA: {eta})'
                    break
            enhanced = '\n'.join(lines)
            return enhanced
        
        # Default: Add ETA statement at appropriate location
        service_name = self.get_service_name(issue_type)
        eta_statement = f"{service_name} ETA: {eta}."
        
        # Find good insertion point
        if '\n\n' in enhanced:
            parts = enhanced.split('\n\n', 2)
            if len(parts) >= 2:
                enhanced = parts[0] + '\n\n' + eta_statement + '\n\n' + '\n\n'.join(parts[1:])
        else:
            enhanced += f"\n\n{eta_statement}"
        
        return enhanced

    def get_service_name(self, issue_type: str) -> str:
        """Get appropriate service name for ETA statement"""
        service_names = {
            'police': 'Police',
            'fire': 'Fire department',
            'paramedics': 'Paramedics',
            'building_security': 'Building security',
            'no_heat': 'Emergency heating repair',
            'no_water': 'Emergency plumbing',
            'flooding': 'Water damage response team',
            'electrical': 'Emergency electrician',
            'gas_leak': 'Gas company emergency team'
        }
        return service_names.get(issue_type, 'Emergency response team')

    def process_entry(self, entry: Dict) -> Dict:
        """Process a single entry to add specific ETAs"""
        enhanced = entry.copy()
        messages = enhanced.get('messages', [])
        
        # Detect context
        issue_type, location, modifiers = self.detect_issue_and_context(messages)
        
        # Track if we made changes
        changes_made = False
        
        # Process each message
        for i, msg in enumerate(messages):
            if msg.get('role') == 'willow' and msg.get('tier') == 'tier_2':
                original_content = msg.get('content', '')
                enhanced_content = self.enhance_tier2_with_eta(
                    original_content, issue_type, location, modifiers
                )
                
                if enhanced_content != original_content:
                    messages[i]['content'] = enhanced_content
                    messages[i]['eta_enhanced'] = True
                    changes_made = True
        
        # Add metadata
        if changes_made:
            if 'metadata' not in enhanced:
                enhanced['metadata'] = {}
            
            enhanced['metadata']['eta_enhancement'] = {
                'timestamp': datetime.now().isoformat(),
                'issue_type': issue_type,
                'location': location,
                'modifiers': modifiers,
                'version': '1.0'
            }
        
        return enhanced

    def process_corpus(self, input_file: str, output_file: str):
        """Process entire corpus to add specific ETAs"""
        print(f"Adding specific ETAs to: {input_file}")
        
        enhanced_entries = []
        stats = defaultdict(int)
        
        with open(input_file, 'r') as f:
            for line_num, line in enumerate(f, 1):
                if line.strip():
                    try:
                        entry = json.loads(line)
                        enhanced = self.process_entry(entry)
                        enhanced_entries.append(enhanced)
                        
                        stats['total'] += 1
                        if enhanced.get('metadata', {}).get('eta_enhancement'):
                            stats['enhanced'] += 1
                            stats[f"issue_{enhanced['metadata']['eta_enhancement']['issue_type']}"] += 1
                        
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
        self.generate_report(stats, output_file)
        
        return stats

    def generate_report(self, stats: Dict, output_file: str):
        """Generate enhancement report"""
        report = f"""
Specific ETA Enhancement Complete
=================================
Total Entries: {stats['total']}
Enhanced: {stats['enhanced']} ({stats['enhanced']/max(stats['total'],1)*100:.1f}%)
Errors: {stats['errors']}

Enhanced by Issue Type:
"""
        for issue in ['police', 'fire', 'paramedics', 'no_heat', 'no_water', 'flooding', 'electrical']:
            count = stats.get(f'issue_{issue}', 0)
            if count > 0:
                report += f"- {issue}: {count}\n"
        
        report += f"\nOutput: {output_file}"
        
        print(report)
        
        # Save report
        report_file = output_file.replace('.jsonl', '_eta_report.txt')
        with open(report_file, 'w') as f:
            f.write(report)

if __name__ == "__main__":
    enhancer = SpecificETAEnhancer()
    
    # Process salvageable entries
    input_file = "willow_corpus_salvageable_20250624_023332.jsonl"
    output_file = f"willow_corpus_eta_enhanced_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jsonl"
    
    stats = enhancer.process_corpus(input_file, output_file)
    
    print(f"\nETA enhancement complete! Output: {output_file}")