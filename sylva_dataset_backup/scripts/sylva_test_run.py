#!/usr/bin/env python3
import json
import sys
import os

# Import the main generator
from sylva_master_generator import generate_batch, save_batch, CATEGORIES

def test_generator():
    """Test the enhanced generator with batches 2-5"""
    
    print("🧪 SYLVA Generator Test Run")
    print("=" * 40)
    print("Generating batches 2-5 (entries 141-540)")
    print()
    
    # Global tracking for variety
    global_used_closures = []
    global_used_prompts = []
    
    # Generate 4 test batches
    for batch_num in range(2, 6):  # Batches 2, 3, 4, 5
        start_id = 41 + (batch_num - 1) * 100
        end_id = start_id + 99
        
        print(f"📝 Generating Batch {batch_num}: Entries {start_id}-{end_id}")
        
        # Generate batch
        batch_entries = generate_batch(start_id, 100, global_used_closures, global_used_prompts)
        
        # Save batch
        batch_file = save_batch(batch_entries, batch_num)
        
        # Validation
        categories_used = set(entry['metadata']['category'] for entry in batch_entries)
        closures_used = set(entry['closure'] for entry in batch_entries)
        
        print(f"✅ Batch {batch_num} complete:")
        print(f"   - Categories: {len(categories_used)}/{len(CATEGORIES)} ({list(categories_used)})")
        print(f"   - Unique closures: {len(closures_used)}")
        print(f"   - File: {batch_file}")
        print()
    
    print("🎉 Test batches complete!")
    print(f"📊 Total test entries generated: 400 (entries 141-540)")
    
    # Show sample entries from last batch
    print(f"\n📋 Sample entries from Batch 5:")
    with open('sylva_batch_005.json', 'r') as f:
        last_batch = json.load(f)
    
    for i in [0, 25, 50, 75, 99]:
        entry = last_batch[i]
        print(f"\n--- Entry {entry['entry_id']} ---")
        print(f"Category: {entry['metadata']['category']} / {entry['metadata']['subcategory']}")
        print(f"Context: {entry['metadata']['context']} | Age: {entry['metadata']['age_group']}")
        print(f"Prompt: \"{entry['prompt'][:80]}...\"")
        print(f"Response: \"{entry['response'][:80]}...\"")
        print(f"Closure: \"{entry['closure']}\"")

if __name__ == "__main__":
    test_generator()