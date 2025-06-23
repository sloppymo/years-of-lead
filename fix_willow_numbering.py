#!/usr/bin/env python3
"""
Fix numbering gaps in Willow corpus to ensure continuous IDs
"""

import json
from typing import List, Dict
import argparse

def renumber_entries(entries: List[Dict], starting_id: int = 1) -> List[Dict]:
    """Renumber entries with continuous IDs."""
    renumbered = []
    
    for i, entry in enumerate(entries):
        new_entry = entry.copy()
        new_id = starting_id + i
        old_id = entry['id']
        new_entry['id'] = f"WILLOW_{new_id}"
        
        # Also update conversation_id if it exists in process_metrics
        if 'process_metrics' in new_entry and 'conversation_id' in new_entry['process_metrics']:
            # Keep the prefix but update the number
            conv_prefix = new_entry['process_metrics']['conversation_id'].split('_')[0]
            new_entry['process_metrics']['conversation_id'] = f"{conv_prefix}_{new_id}"
        
        # Add metadata about renumbering
        new_entry['renumbering_info'] = {
            'original_id': old_id,
            'renumbered': True,
            'renumber_date': '2024-01-15'
        }
        
        renumbered.append(new_entry)
    
    return renumbered

def process_files(input_files: List[str], output_file: str):
    """Process multiple files and create a single renumbered output."""
    all_entries = []
    
    # Load all entries
    for filename in input_files:
        print(f"Loading {filename}...")
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        entry = json.loads(line)
                        all_entries.append(entry)
            print(f"  Loaded {len([e for e in all_entries if 'id' in e])} entries")
        except FileNotFoundError:
            print(f"  File not found: {filename}")
        except Exception as e:
            print(f"  Error loading file: {e}")
    
    print(f"\nTotal entries loaded: {len(all_entries)}")
    
    # Sort by current ID number to maintain relative order
    all_entries.sort(key=lambda x: int(x['id'].split('_')[1]))
    
    # Renumber
    print("\nRenumbering entries...")
    renumbered_entries = renumber_entries(all_entries)
    
    # Write output
    print(f"\nWriting to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        for entry in renumbered_entries:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')
    
    # Print summary
    print(f"\nRenumbering complete!")
    print(f"Total entries: {len(renumbered_entries)}")
    print(f"ID range: WILLOW_1 to WILLOW_{len(renumbered_entries)}")
    print(f"Output file: {output_file}")
    
    # Show mapping sample
    print("\nSample ID mappings (first 10):")
    for entry in renumbered_entries[:10]:
        if 'renumbering_info' in entry:
            print(f"  {entry['renumbering_info']['original_id']} → {entry['id']}")

def main():
    parser = argparse.ArgumentParser(description='Fix numbering gaps in Willow corpus')
    parser.add_argument('--input-files', nargs='+', required=True, help='Input JSONL files in order')
    parser.add_argument('--output-file', required=True, help='Output JSONL file')
    parser.add_argument('--starting-id', type=int, default=1, help='Starting ID number (default: 1)')
    
    args = parser.parse_args()
    
    process_files(args.input_files, args.output_file)

if __name__ == "__main__":
    # If no command line args, run with default files
    import sys
    if len(sys.argv) == 1:
        # Default processing
        input_files = [
            'willow_corpus_complete_safe.jsonl',  # 843 entries (1-843)
            'willow_batch_500_v2_safe.jsonl'      # 500 entries (will become 844-1343)
        ]
        output_file = 'willow_corpus_renumbered_1343.jsonl'
        
        print("Running with default files...")
        print(f"Input files: {input_files}")
        print(f"Output file: {output_file}")
        print()
        
        process_files(input_files, output_file)
    else:
        main()