#!/usr/bin/env python3
"""
Fix errors and issues in Willow corpus based on detailed analysis.
"""

import json
import re
from typing import Dict, List, Tuple

def load_corpus(filename: str) -> List[Dict]:
    """Load the corpus file."""
    entries = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                entries.append(json.loads(line.strip()))
            except json.JSONDecodeError:
                continue
    return entries

def fix_grammatical_glitches(content: str) -> Tuple[str, bool]:
    """Fix broken/repeated phrases and grammatical glitches."""
    original = content
    
    # Fix repeated "work to" patterns
    patterns = [
        (r"work to work to work to we'll work to", "work to ensure we"),
        (r"we'll work to we'll work to", "we'll work to"),
        (r"work to work to", "work to"),
        (r"we'll work to're", "we're working to ensure you're"),
        (r"we'll work to won't", "we'll ensure you won't"),
        (r"work to(?:\s+work to)+", "work to"),  # Multiple repetitions
    ]
    
    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
    
    # Fix other repetitive patterns
    content = re.sub(r"(\b\w+\b)(?:\s+\1){2,}", r"\1", content)  # Remove word repetitions
    
    # Fix broken contractions
    content = re.sub(r"\bto're\b", "to ensure you're", content)
    content = re.sub(r"\bto won't\b", "to ensure you won't", content)
    
    return content, content != original

def improve_awkward_phrasing(content: str) -> Tuple[str, bool]:
    """Replace awkward 'help explore' phrasing with more natural language."""
    original = content
    
    # Replace "help explore" patterns
    replacements = [
        (r"I can help explore arranging", "I can help arrange"),
        (r"I can help explore finding", "I can help find"),
        (r"I can help explore getting", "I can help get"),
        (r"I can help explore scheduling", "I can help schedule"),
        (r"I can help explore connecting", "I can help connect"),
        (r"help explore (\w+ing)", r"help \1"),  # General pattern
    ]
    
    for pattern, replacement in replacements:
        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
    
    # Add softer language around commitments
    if "I can help" in content and "subject to" not in content:
        # Add natural disclaimer at the end if making commitments
        if any(word in content.lower() for word in ['arrange', 'schedule', 'find', 'get']):
            content = content.rstrip('.') + " - let me see what options are available."
    
    return content, content != original

def streamline_disclaimers(content: str) -> Tuple[str, bool]:
    """Reduce repetitive disclaimers while maintaining legal safety."""
    original = content
    
    # Count disclaimer occurrences
    disclaimer_count = content.count("subject to availability")
    
    if disclaimer_count > 1:
        # Keep only the first disclaimer in lists
        lines = content.split('\n')
        disclaimer_seen = False
        new_lines = []
        
        for line in lines:
            if "subject to availability" in line:
                if not disclaimer_seen:
                    disclaimer_seen = True
                    new_lines.append(line)
                else:
                    # Remove disclaimer from subsequent lines
                    new_line = re.sub(r",?\s*subject to availability(?:\s+and approval)?", "", line)
                    new_lines.append(new_line)
            else:
                new_lines.append(line)
        
        content = '\n'.join(new_lines)
        
        # Add a single disclaimer at the end if removed from list items
        if disclaimer_seen and disclaimer_count > 1:
            if not content.rstrip().endswith('.'):
                content += '.'
            content += " All options subject to availability and standard approval processes."
    
    return content, content != original

def fix_overpromising_timelines(content: str) -> Tuple[str, bool]:
    """Replace overly specific timeline promises with realistic commitments."""
    original = content
    
    # Fix overly specific timelines
    timeline_replacements = [
        (r"within the hour", "as soon as possible"),
        (r"in the next hour", "right away"),
        (r"within (\d+) hours?", r"within \1 business hours"),
        (r"immediately", "as a priority"),
        (r"right now", "right away"),
        (r"I'm personally clearing", "I'm arranging for someone to clear"),
        (r"sending maintenance immediately", "prioritizing maintenance"),
    ]
    
    for pattern, replacement in timeline_replacements:
        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
    
    return content, content != original

def check_emotional_regulation(entry: Dict) -> Dict:
    """Ensure emotional regulation is appropriate."""
    # Check for positive arousal impacts that might need adjustment
    messages = entry.get('messages', [])
    
    for msg in messages:
        if msg.get('role') == 'willow' and msg.get('arousal_impact', 0) > 0:
            # Positive arousal impact - check if it's justified
            content = msg.get('content', '')
            
            # If it's acknowledging severity, that's okay
            if any(word in content.lower() for word in ['serious', 'emergency', 'urgent', 'dangerous']):
                # Add calming element if not present
                if not any(word in content.lower() for word in ['help', 'support', 'together', 'safe']):
                    msg['content'] = content.rstrip('.') + ". I'm here to help you through this."
                    msg['arousal_impact'] = -0.1  # Slight calming effect
    
    return entry

def process_entry(entry: Dict) -> Tuple[Dict, List[str]]:
    """Process a single entry and fix all identified issues."""
    fixes_applied = []
    entry_copy = json.loads(json.dumps(entry))  # Deep copy
    
    messages = entry_copy.get('messages', [])
    
    for msg in messages:
        if msg.get('role') == 'willow':
            content = msg.get('content', '')
            original_content = content
            
            # Apply fixes in order
            content, fixed = fix_grammatical_glitches(content)
            if fixed:
                fixes_applied.append('grammatical_glitches')
            
            content, fixed = improve_awkward_phrasing(content)
            if fixed:
                fixes_applied.append('awkward_phrasing')
            
            content, fixed = streamline_disclaimers(content)
            if fixed:
                fixes_applied.append('disclaimer_streamlined')
            
            content, fixed = fix_overpromising_timelines(content)
            if fixed:
                fixes_applied.append('timeline_adjusted')
            
            msg['content'] = content
            
            # Track if content was modified
            if content != original_content:
                msg['content_fixed'] = True
    
    # Check emotional regulation
    entry_copy = check_emotional_regulation(entry_copy)
    
    # Add metadata about fixes
    if fixes_applied:
        entry_copy['error_fixes_applied'] = list(set(fixes_applied))
    
    return entry_copy, fixes_applied

def main():
    print("Loading corpus for error fixing...")
    entries = load_corpus('willow_corpus_final_renumbered.jsonl')
    print(f"Loaded {len(entries)} entries")
    
    # Track statistics
    total_fixes = 0
    fix_types = {
        'grammatical_glitches': 0,
        'awkward_phrasing': 0,
        'disclaimer_streamlined': 0,
        'timeline_adjusted': 0
    }
    
    # Process all entries
    fixed_entries = []
    entries_with_fixes = []
    
    for i, entry in enumerate(entries):
        fixed_entry, fixes = process_entry(entry)
        fixed_entries.append(fixed_entry)
        
        if fixes:
            total_fixes += 1
            entries_with_fixes.append({
                'id': entry.get('id'),
                'fixes': fixes
            })
            for fix in fixes:
                if fix in fix_types:
                    fix_types[fix] += 1
    
    # Save fixed corpus
    output_file = 'willow_corpus_final_fixed.jsonl'
    with open(output_file, 'w', encoding='utf-8') as f:
        for entry in fixed_entries:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')
    
    print(f"\nError Fixing Complete!")
    print(f"Total entries processed: {len(entries)}")
    print(f"Entries with fixes: {total_fixes}")
    print(f"\nFixes by type:")
    for fix_type, count in fix_types.items():
        print(f"  {fix_type}: {count}")
    
    print(f"\nFixed corpus saved to: {output_file}")
    
    # Show examples of fixes
    if entries_with_fixes:
        print("\nExample fixes applied:")
        for example in entries_with_fixes[:5]:
            print(f"  {example['id']}: {', '.join(example['fixes'])}")
    
    # Special check for WILLOW_46 mentioned in the analysis
    for entry in fixed_entries:
        if entry.get('id') == 'WILLOW_46':
            print(f"\nSpecial check - WILLOW_46:")
            for msg in entry.get('messages', []):
                if msg.get('role') == 'willow' and 'content_fixed' in msg:
                    print(f"  Fixed: {msg.get('content')[:100]}...")

if __name__ == "__main__":
    main()