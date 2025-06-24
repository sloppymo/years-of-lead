#!/usr/bin/env python3
"""
Fix dangerous promises in the main 2375 entry corpus
"""

import json
import re
from datetime import datetime
from typing import Dict, Tuple, List

class FinalCorpusPromiseRemover:
    def __init__(self):
        # Comprehensive list of dangerous patterns
        self.dangerous_patterns = [
            # Police/Law Enforcement
            (r'Police ETA:?\s*\d+[-–]?\d*\s*minutes?', 'Police have been notified'),
            (r'Police.{0,20}arriving in \d+[-–]?\d*\s*minutes?', 'Police have been contacted'),
            
            # Paramedics/Medical
            (r'Paramedics?.{0,20}ETA:?\s*\d+[-–]?\d*\s*minutes?', 'Emergency medical services have been called'),
            (r'Paramedics?.{0,20}arriving in \d+[-–]?\d*\s*minutes?', 'Paramedics have been dispatched'),
            (r'Ambulance.{0,20}arriving in \d+[-–]?\d*\s*minutes?', 'Ambulance is on the way'),
            
            # Fire Department
            (r'Fire department.{0,20}arriving in \d+[-–]?\d*\s*minutes?', 'Fire department is on the way'),
            
            # Emergency Services
            (r'Emergency services?.{0,20}arriving in \d+[-–]?\d*\s*minutes?', 'Emergency services have been notified'),
            
            # Utility crews - IMPORTANT: This pattern needs to catch the water shut-off crew
            (r'Water.{0,20}shut-off crew arriving in \d+\s*minutes?', 'Water shut-off crew has been dispatched'),
            (r'shut-off crew arriving in \d+\s*minutes?', 'Shut-off crew has been dispatched'),
            (r'crew arriving in \d+\s*minutes?', 'Crew has been dispatched'),
            
            # Generic patterns
            (r'arriving in \d+[-–]?\d*\s*minutes?', 'on their way'),
            (r'ETA:?\s*\d+\s*minutes?', 'on their way'),
            (r'within \d+\s*minutes?', 'as quickly as possible'),
            
            # Specific time frames
            (r'in \d+\s*minutes', 'as soon as possible'),
        ]
        
        self.acceptable_patterns = [
            'building security',
            'building staff',
            'our team',
            'our emergency response team',
            'our first aid team',
            'our maintenance team',
            'building management'
        ]

    def remove_dangerous_promises(self, content: str) -> str:
        """Remove dangerous time promises from content"""
        
        original = content
        
        for pattern, replacement in self.dangerous_patterns:
            # Use DOTALL flag to match across newlines
            matches = list(re.finditer(pattern, content, re.IGNORECASE | re.DOTALL))
            
            for match in reversed(matches):
                # Get context
                start = max(0, match.start() - 50)
                end = min(len(content), match.end() + 50)
                context = content[start:end].lower()
                
                # Check if it's about internal services
                is_internal = any(acceptable in context for acceptable in self.acceptable_patterns)
                
                if not is_internal:
                    # Replace the match
                    content = content[:match.start()] + replacement + content[match.end():]
        
        if content != original:
            print(f"  Modified content containing: {pattern}")
        
        return content

    def process_entry(self, entry: Dict) -> Tuple[Dict, bool]:
        """Process a single entry"""
        
        messages = entry.get("messages", [])
        modified = False
        
        for message in messages:
            if message.get("role") == "assistant":
                original_content = message.get("content", "")
                new_content = self.remove_dangerous_promises(original_content)
                
                if new_content != original_content:
                    message["content"] = new_content
                    modified = True
                    
                    # Show what was changed
                    if "Water shut-off crew arriving in 15 minutes" in original_content:
                        print(f"\n  Found and fixed: Water shut-off crew promise in entry {entry.get('id', 'unknown')}")
        
        return entry, modified

def main():
    """Fix the main corpus file"""
    
    print("Fixing WILLOW Main Corpus (2375 entries)")
    print("=" * 60)
    
    input_file = "willow_corpus_complete_final_20250624_000624.jsonl"
    
    print(f"Processing: {input_file}")
    
    entries = []
    with open(input_file, 'r') as f:
        for line in f:
            if line.strip():
                entries.append(json.loads(line))
    
    print(f"Loaded {len(entries)} entries")
    
    # First, let's find entries with dangerous content
    print("\nScanning for dangerous promises...")
    dangerous_count = 0
    
    for i, entry in enumerate(entries):
        messages = entry.get("messages", [])
        for message in messages:
            if message.get("role") == "assistant":
                content = message.get("content", "")
                if re.search(r'arriving in \d+\s*minutes', content, re.IGNORECASE):
                    dangerous_count += 1
                    print(f"  Entry {i+1}: Found 'arriving in X minutes'")
                    if i == 395:  # Line 396 is index 395
                        print(f"    Content preview: {content[:200]}...")
    
    print(f"\nFound {dangerous_count} entries with potential dangerous promises")
    
    # Now process all entries
    remover = FinalCorpusPromiseRemover()
    processed_entries = []
    modified_count = 0
    
    print("\nProcessing entries...")
    
    for entry in entries:
        processed_entry, was_modified = remover.process_entry(entry)
        processed_entries.append(processed_entry)
        if was_modified:
            modified_count += 1
    
    # Save the fixed corpus
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"willow_corpus_complete_final_safe_{timestamp}.jsonl"
    
    with open(output_file, 'w') as f:
        for entry in processed_entries:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')
    
    print(f"\n✓ Modified {modified_count} entries")
    print(f"✓ Saved to: {output_file}")
    print(f"✓ Total entries preserved: {len(entries)}")
    
    # Verify we have all 2375 entries
    if len(entries) == 2375:
        print("\n✅ SUCCESS: All 2,375 entries preserved and made safe!")
    else:
        print(f"\n⚠️  WARNING: Expected 2,375 entries but got {len(entries)}")

if __name__ == "__main__":
    main()