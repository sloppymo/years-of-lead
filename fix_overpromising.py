#!/usr/bin/env python3
"""
Fix overpromising issues in WILLOW datasets by replacing definitive promises
with appropriate qualifiers and realistic language.
"""

import json
import re
import glob
from typing import Dict, List, Tuple

# Define replacement patterns for overpromising language
REPLACEMENTS = [
    # Timeline promises
    (r'\bcoming TODAY\b', 'being prioritized for urgent response'),
    (r'\bTODAY\b(?! at)', 'as soon as possible'),
    (r'\bNOW\b', 'immediately prioritized'),
    (r'\bimmediately\b', 'right away'),
    (r'\bright away\b', 'as quickly as possible'),
    (r'\btomorrow\b', 'soon, typically within 24-48 hours'),
    (r'\bin (\d+) minutes\b', r'typically within \1-30 minutes'),
    (r'\bin (\d+) hours?\b', r'typically within \1-4 hours'),
    (r'\barrives? in (\d+)', r'typically arrives within \1-30'),
    (r'\bwithin (\d+) minutes\b', r'typically within \1-30 minutes'),
    
    # Direct action promises
    (r"I've (already |auto-)?scheduled", "I can help coordinate scheduling for"),
    (r"I've (already |auto-)?programmed", "I can help arrange programming of"),
    (r"I've (already |auto-)?generated", "I can help generate"),
    (r"I've (already |auto-)?dispatched", "I'm requesting dispatch of"),
    (r"I'll process", "I'll help facilitate processing of"),
    (r"I'll set (up|that up)", "I can help arrange"),
    (r"I'm sending", "I can help arrange for"),
    (r"I'll send", "I can help arrange to send"),
    (r"I'm setting up", "I can help coordinate"),
    (r"I'll arrange", "I can help coordinate"),
    (r"I'll install", "I can request installation of"),
    (r"I'll add you", "I can help add you"),
    (r"I'll register you", "I can help with registration"),
    (r"We'll have", "We typically can arrange for"),
    (r"We'll send", "We can typically arrange"),
    (r"We can send", "We can typically arrange"),
    (r"I can send", "I can help arrange"),
    (r"Sending (.*?) today", r"Can arrange \1, typically same-day"),
    (r"Setting up:", "Can help coordinate:"),
    
    # Availability promises
    (r'\b(is|are) available\b', 'may be available'),
    (r'\bhas availability\b', 'typically has availability'),
    (r'\bin stock\b', 'typically in stock'),
    (r'\bready\b(?! to)', 'typically ready'),
    (r'\bconfirmed\b', 'tentatively confirmed, subject to availability'),
    (r'\bguaranteed\b', 'prioritized'),
    
    # Financial promises
    (r'\bno cost\b', 'typically no cost'),
    (r'\bzero penalties\b', 'may qualify for penalty waiver'),
    (r'\bfree\b', 'typically free'),
    (r'\bapproved for\b', 'may qualify for'),
    (r'\bqualify for\b', 'may qualify for'),
    (r'\b(\d+)% (off|discount|reduction)\b', r'up to \1% \2, subject to approval'),
    
    # Will/shall statements
    (r"\bwill be\b", "should be"),
    (r"\bwill have\b", "typically will have"),
    (r"\bI'll (\w+) you\b", r"I can help \1 you"),
    (r"\bWe'll\b", "We'll work to"),
    (r"\byou'll get\b", "you'll typically receive"),
    
    # Definitive statements
    (r'\bensure\b', 'work to ensure'),
    (r'\bguarantee\b', 'prioritize'),
    (r'\bdefinitely\b', 'typically'),
    (r'\bpromise\b', 'aim to'),
    
    # Legal/policy promises
    (r"I'm stopping the eviction", "I'm requesting a review of the eviction"),
    (r"eviction halted", "eviction review requested"),
    (r"qualifies? for", "may qualify for"),
    (r"have (a|an) (.*?) available", r"may have \1 \2 available"),
    
    # Specific fixes
    (r"Done!", "I'll help get that arranged!"),
    (r"Consider it done", "I'll help coordinate that"),
    (r"Scheduled and confirmed", "Scheduling requested"),
    (r"(\d+) AM confirmed", r"\1 AM tentatively scheduled"),
]

def fix_overpromising(text: str) -> str:
    """Apply all replacement patterns to fix overpromising language."""
    for pattern, replacement in REPLACEMENTS:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    
    # Add qualifiers where needed
    if "typically" not in text and "may" not in text and "subject to" not in text:
        # Add appropriate qualifiers for certain phrases
        if any(phrase in text.lower() for phrase in ["can help", "typically", "may", "work to", "aim to"]):
            pass  # Already has qualifier
        elif "repair" in text or "maintenance" in text:
            text = text.replace("repair", "repair, subject to availability,")
        elif "fund" in text or "assistance" in text:
            text = text.replace(".", ", subject to availability and approval.")
    
    return text

def process_jsonl_file(filepath: str) -> Tuple[int, int]:
    """Process a JSONL file and fix overpromising issues."""
    print(f"\nProcessing {filepath}...")
    
    entries = []
    changes_made = 0
    total_entries = 0
    
    # Read the file
    with open(filepath, 'r') as f:
        for line in f:
            if line.strip():
                entry = json.loads(line)
                entries.append(entry)
                total_entries += 1
    
    # Process each entry
    for entry in entries:
        if 'messages' in entry:
            for message in entry['messages']:
                if message.get('role') == 'willow':
                    original = message['content']
                    fixed = fix_overpromising(original)
                    
                    if fixed != original:
                        message['content'] = fixed
                        changes_made += 1
                        print(f"  Fixed: {entry.get('id', 'Unknown ID')}")
                        print(f"    Original: {original[:80]}...")
                        print(f"    Fixed: {fixed[:80]}...")
    
    # Write back to file
    with open(filepath, 'w') as f:
        for entry in entries:
            f.write(json.dumps(entry) + '\n')
    
    return changes_made, total_entries

def main():
    """Process all WILLOW JSONL files."""
    print("Starting overpromising fixes...")
    
    # Find all WILLOW JSONL files
    files = glob.glob('willow_*.jsonl')
    
    total_changes = 0
    total_entries = 0
    
    for filepath in sorted(files):
        changes, entries = process_jsonl_file(filepath)
        total_changes += changes
        total_entries += entries
    
    print(f"\n{'='*50}")
    print(f"Total files processed: {len(files)}")
    print(f"Total entries processed: {total_entries}")
    print(f"Total changes made: {total_changes}")
    print(f"{'='*50}")

if __name__ == "__main__":
    main()