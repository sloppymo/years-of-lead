#!/usr/bin/env python3
"""
WILLOW Dataset Liability Removal Script
Removes time-specific promises and legal liability language from the corpus
"""

import json
import re
import sys
from typing import Dict, List, Tuple

# Liability patterns to replace
LIABILITY_PATTERNS = [
    # Time-specific promises
    (r'within \d+ hours?', 'as quickly as possible'),
    (r'within \d+ minutes?', 'right away'),
    (r'in \d+ hours?', 'soon'),
    (r'in \d+ minutes?', 'shortly'),
    (r'\d+ minutes? away', 'on the way'),
    (r'by \d+[ap]m', 'today'),
    (r'by \d+:\d+[ap]m', 'today'),
    (r'tomorrow \d+[ap]m', 'tomorrow'),
    (r'tomorrow at \d+[ap]m', 'tomorrow'),
    
    # Third-party commitments
    (r'(Tech|Technician|Plumber|Electrician|Maintenance|Locksmith) (dispatched|coming|arriving|scheduled)',
     r'\1 being contacted'),
    (r'Emergency (crew|team|service) arriving', 'Emergency response being coordinated'),
    (r'Police will arrive', 'Police being notified'),
    (r'Security dispatched', 'Security being alerted'),
    
    # Guaranteed outcomes
    (r"You're safe now", "Working to ensure your safety"),
    (r'This ends today', 'Addressing this urgently'),
    (r'This stops today', 'Taking immediate action'),
    (r'will be fixed', 'working on fixing'),
    (r'will arrive', 'being arranged'),
    (r'Full remediation guaranteed', 'Comprehensive remediation planned'),
    
    # Specific promises
    (r'Text [A-Z]+ for emergency repair', 'Text for urgent assistance'),
    (r'Portable heaters available at office', 'Checking on portable heater availability'),
    (r'Hotel voucher if not fixed', 'Exploring temporary accommodation options'),
    (r'Bars installed by', 'Security measures being arranged'),
    (r'Your lock rekeyed today', 'Lock replacement being prioritized'),
    (r'Eviction cancelled NOW', 'Working to resolve eviction notice immediately'),
    (r'Generator (\d+) minutes away', 'Generator being rushed to you'),
]

# Additional phrases to soften
SOFTEN_PHRASES = {
    'will be': 'working on',
    'I promise': 'I understand the urgency',
    'guaranteed': 'prioritized',
    'definitely': 'working to ensure',
    'You have my word': 'This is our priority',
    'I guarantee': 'I\'m committed to',
}


def clean_message(content: str) -> Tuple[str, List[str]]:
    """Clean a single message of liability issues"""
    original = content
    changes = []
    
    # Apply regex patterns
    for pattern, replacement in LIABILITY_PATTERNS:
        if re.search(pattern, content, re.IGNORECASE):
            new_content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
            if new_content != content:
                changes.append(f"Replaced '{pattern}' pattern")
                content = new_content
    
    # Apply phrase replacements
    for phrase, replacement in SOFTEN_PHRASES.items():
        if phrase in content:
            content = content.replace(phrase, replacement)
            changes.append(f"Softened '{phrase}'")
    
    return content, changes


def process_entry(entry: Dict) -> Tuple[Dict, List[str]]:
    """Process a single JSONL entry"""
    changes = []
    
    if 'messages' not in entry:
        return entry, changes
    
    # Process each message
    for i, message in enumerate(entry['messages']):
        if message.get('role') == 'willow' and 'content' in message:
            cleaned_content, msg_changes = clean_message(message['content'])
            if msg_changes:
                entry['messages'][i]['content'] = cleaned_content
                changes.extend([f"Message {i}: {change}" for change in msg_changes])
    
    # Add metadata
    if changes:
        entry['liability_reviewed'] = True
        entry['auto_cleaned'] = True
    
    return entry, changes


def main():
    input_file = 'willow_training_corpus_final.jsonl'
    output_file = 'willow_training_corpus_cleaned.jsonl'
    
    print(f"Processing {input_file}...")
    
    total_changes = 0
    entries_modified = 0
    
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line_num, line in enumerate(infile, 1):
            try:
                entry = json.loads(line)
                cleaned_entry, changes = process_entry(entry)
                
                if changes:
                    entries_modified += 1
                    total_changes += len(changes)
                    print(f"\nEntry {entry.get('id', line_num)}: {len(changes)} changes")
                    for change in changes[:3]:  # Show first 3 changes
                        print(f"  - {change}")
                    if len(changes) > 3:
                        print(f"  ... and {len(changes) - 3} more")
                
                json.dump(cleaned_entry, outfile)
                outfile.write('\n')
                
            except json.JSONDecodeError as e:
                print(f"Error processing line {line_num}: {e}")
                continue
    
    print(f"\n{'='*50}")
    print(f"Liability Removal Complete!")
    print(f"{'='*50}")
    print(f"Total entries processed: {line_num}")
    print(f"Entries modified: {entries_modified}")
    print(f"Total changes made: {total_changes}")
    print(f"Output saved to: {output_file}")
    
    # Generate summary report
    report_file = 'liability_removal_report.txt'
    with open(report_file, 'w') as report:
        report.write("WILLOW Dataset Liability Removal Report\n")
        report.write("="*50 + "\n\n")
        report.write(f"Input file: {input_file}\n")
        report.write(f"Output file: {output_file}\n")
        report.write(f"Total entries: {line_num}\n")
        report.write(f"Entries modified: {entries_modified}\n")
        report.write(f"Total changes: {total_changes}\n")
        report.write(f"Modification rate: {entries_modified/line_num*100:.1f}%\n")
    
    print(f"\nDetailed report saved to: {report_file}")


if __name__ == "__main__":
    main()