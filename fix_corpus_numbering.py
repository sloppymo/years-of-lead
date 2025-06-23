#!/usr/bin/env python3
"""
Fix numbering in Willow corpus to be sequential from WILLOW_1 to WILLOW_N.
"""

import json
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

def extract_id_number(entry: Dict) -> int:
    """Extract the numeric part of the WILLOW ID."""
    id_str = entry.get('id', '')
    if id_str.startswith('WILLOW_'):
        try:
            return int(id_str.replace('WILLOW_', ''))
        except ValueError:
            return 0
    return 0

def renumber_corpus(entries: List[Dict]) -> Tuple[List[Dict], Dict[str, str]]:
    """Renumber all entries sequentially."""
    # Sort by current ID number to maintain relative order
    sorted_entries = sorted(entries, key=extract_id_number)
    
    # Create mapping of old IDs to new IDs
    id_mapping = {}
    renumbered_entries = []
    
    for i, entry in enumerate(sorted_entries, 1):
        old_id = entry.get('id', '')
        new_id = f'WILLOW_{i}'
        id_mapping[old_id] = new_id
        
        # Create a deep copy and update the ID
        new_entry = json.loads(json.dumps(entry))  # Deep copy
        new_entry['id'] = new_id
        renumbered_entries.append(new_entry)
    
    return renumbered_entries, id_mapping

def main():
    print("Loading corpus for renumbering...")
    entries = load_corpus('willow_corpus_final_improved.jsonl')
    print(f"Loaded {len(entries)} entries")
    
    # Get current ID range
    id_numbers = [extract_id_number(e) for e in entries]
    print(f"Current ID range: WILLOW_{min(id_numbers)} to WILLOW_{max(id_numbers)}")
    
    # Renumber entries
    print("\nRenumbering entries sequentially...")
    renumbered_entries, id_mapping = renumber_corpus(entries)
    
    # Save renumbered corpus
    output_file = 'willow_corpus_final_renumbered.jsonl'
    with open(output_file, 'w', encoding='utf-8') as f:
        for entry in renumbered_entries:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')
    
    print(f"\nRenumbering complete!")
    print(f"New ID range: WILLOW_1 to WILLOW_{len(renumbered_entries)}")
    print(f"Saved to: {output_file}")
    
    # Save mapping for reference
    mapping_file = 'id_mapping.json'
    with open(mapping_file, 'w') as f:
        json.dump(id_mapping, f, indent=2)
    print(f"ID mapping saved to: {mapping_file}")
    
    # Show some examples of changes
    print("\nExample ID changes:")
    examples = list(id_mapping.items())[:5]
    for old, new in examples:
        if old != new:
            print(f"  {old} → {new}")
    
    # Check for any gaps in new sequence
    new_numbers = [i for i in range(1, len(renumbered_entries) + 1)]
    actual_numbers = [extract_id_number(e) for e in renumbered_entries]
    if new_numbers == actual_numbers:
        print("\n✅ New numbering is perfectly sequential with no gaps!")
    else:
        print("\n❌ Warning: New numbering still has issues")

if __name__ == "__main__":
    main()