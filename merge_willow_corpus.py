#!/usr/bin/env python3
"""
Merge two Willow corpus files, removing duplicates and maintaining quality.
"""

import json
import sys
from collections import defaultdict
from typing import Dict, List, Set

def load_jsonl(filename: str) -> List[Dict]:
    """Load a JSONL file and return list of entries."""
    entries = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            try:
                entry = json.loads(line.strip())
                entries.append(entry)
            except json.JSONDecodeError as e:
                print(f"Error parsing line {line_num} in {filename}: {e}")
    return entries

def extract_id(entry: Dict) -> str:
    """Extract the WILLOW ID from an entry."""
    return entry.get('id', '')

def analyze_differences(file1_entries: List[Dict], file2_entries: List[Dict]):
    """Analyze differences between two sets of entries."""
    file1_ids = {extract_id(e) for e in file1_entries}
    file2_ids = {extract_id(e) for e in file2_entries}
    
    only_in_file1 = file1_ids - file2_ids
    only_in_file2 = file2_ids - file1_ids
    in_both = file1_ids & file2_ids
    
    print(f"\nAnalysis Results:")
    print(f"File 1 total entries: {len(file1_entries)}")
    print(f"File 2 total entries: {len(file2_entries)}")
    print(f"Unique to File 1: {len(only_in_file1)}")
    print(f"Unique to File 2: {len(only_in_file2)}")
    print(f"In both files: {len(in_both)}")
    
    if only_in_file1:
        print(f"\nIDs only in File 1: {sorted(list(only_in_file1))[:10]}...")
    if only_in_file2:
        print(f"\nIDs only in File 2: {sorted(list(only_in_file2))[:10]}...")
    
    return only_in_file1, only_in_file2, in_both

def merge_entries(file1_entries: List[Dict], file2_entries: List[Dict]) -> List[Dict]:
    """Merge entries from two files, removing duplicates."""
    # Create dictionaries for easy lookup
    file1_dict = {extract_id(e): e for e in file1_entries}
    file2_dict = {extract_id(e): e for e in file2_entries}
    
    # Start with all entries from file2 (Documents version - more complete)
    merged_dict = file2_dict.copy()
    
    # Add any unique entries from file1
    for id, entry in file1_dict.items():
        if id not in merged_dict:
            merged_dict[id] = entry
    
    # Sort by ID number
    sorted_entries = []
    for id in sorted(merged_dict.keys(), key=lambda x: int(x.replace('WILLOW_', '') if x.startswith('WILLOW_') else 0)):
        sorted_entries.append(merged_dict[id])
    
    return sorted_entries

def validate_entry(entry: Dict) -> bool:
    """Validate that an entry has required fields."""
    required_fields = ['id', 'scenario', 'messages']
    return all(field in entry for field in required_fields)

def save_merged_corpus(entries: List[Dict], output_file: str):
    """Save merged entries to a new JSONL file."""
    valid_entries = [e for e in entries if validate_entry(e)]
    
    print(f"\nSaving {len(valid_entries)} valid entries to {output_file}")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for entry in valid_entries:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')
    
    print(f"Merged corpus saved to {output_file}")

def main():
    if len(sys.argv) != 4:
        print("Usage: python merge_willow_corpus.py <file1> <file2> <output_file>")
        print("Example: python merge_willow_corpus.py willow_corpus_final_clean.jsonl willow_corpus_from_documents.jsonl willow_corpus_merged_final.jsonl")
        sys.exit(1)
    
    file1 = sys.argv[1]
    file2 = sys.argv[2]
    output_file = sys.argv[3]
    
    print(f"Loading {file1}...")
    file1_entries = load_jsonl(file1)
    
    print(f"Loading {file2}...")
    file2_entries = load_jsonl(file2)
    
    # Analyze differences
    only_in_file1, only_in_file2, in_both = analyze_differences(file1_entries, file2_entries)
    
    # Merge entries
    print("\nMerging entries...")
    merged_entries = merge_entries(file1_entries, file2_entries)
    
    # Save merged corpus
    save_merged_corpus(merged_entries, output_file)
    
    # Final statistics
    print(f"\nFinal Statistics:")
    print(f"Original File 1: {len(file1_entries)} entries")
    print(f"Original File 2: {len(file2_entries)} entries")
    print(f"Merged Total: {len(merged_entries)} unique entries")

if __name__ == "__main__":
    main()