#!/usr/bin/env python3
import json
import time
import os
from typing import List
from pathlib import Path
from sylva_master_generator import generate_batch, save_batch, combine_batches, CATEGORIES

def generate_dataset_chunks(start_batch: int = 6, end_batch: int = 100, chunk_size: int = 10):
    """Generate the SYLVA dataset in manageable chunks"""
    
    print("🎭 SYLVA Production Dataset Generator")
    print("=" * 60)
    print(f"Target: Complete dataset (entries 41-10,000)")
    print(f"Generating batches {start_batch}-{end_batch} in chunks of {chunk_size}")
    print(f"Total entries to generate: {(end_batch - start_batch + 1) * 100}")
    print()
    
    # Global tracking for variety
    global_used_closures = []
    global_used_prompts = []
    batch_files = []
    
    # Add existing batch files
    for i in range(1, start_batch):
        batch_file = f"sylva_batch_{i:03d}.json"
        if Path(batch_file).exists():
            batch_files.append(batch_file)
    
    total_start_time = time.time()
    
    # Generate in chunks
    for chunk_start in range(start_batch, end_batch + 1, chunk_size):
        chunk_end = min(chunk_start + chunk_size - 1, end_batch)
        
        print(f"🔄 Processing Chunk: Batches {chunk_start}-{chunk_end}")
        chunk_start_time = time.time()
        
        # Generate batches in current chunk
        for batch_num in range(chunk_start, chunk_end + 1):
            start_id = 41 + (batch_num - 1) * 100
            
            print(f"  📝 Generating Batch {batch_num}: Entries {start_id}-{start_id + 99}")
            
            # Generate and save batch
            batch_entries = generate_batch(start_id, 100, global_used_closures, global_used_prompts)
            batch_file = save_batch(batch_entries, batch_num)
            batch_files.append(batch_file)
            
            # Quick validation
            categories_used = len(set(entry['metadata']['category'] for entry in batch_entries))
            unique_closures = len(set(entry['closure'] for entry in batch_entries))
            
            print(f"    ✅ Complete - {categories_used}/{len(CATEGORIES)} categories, {unique_closures} closures")
            
            # Memory management
            if len(global_used_closures) > 1000:
                global_used_closures = global_used_closures[-500:]
            if len(global_used_prompts) > 1000:
                global_used_prompts = global_used_prompts[-500:]
        
        # Chunk completion summary
        chunk_time = time.time() - chunk_start_time
        total_batches_done = chunk_end
        progress = (total_batches_done / end_batch) * 100
        
        print(f"  🎉 Chunk {chunk_start}-{chunk_end} complete in {chunk_time:.1f}s")
        print(f"  📊 Progress: {total_batches_done}/{end_batch} batches ({progress:.1f}%)")
        print()
    
    # Final combination and summary
    total_time = time.time() - total_start_time
    print(f"🎉 All batches generated in {total_time:.1f}s!")
    print(f"📁 Combining {len(batch_files)} batch files...")
    
    total_entries = combine_batches(batch_files)
    
    print(f"✨ SYLVA Dataset Complete!")
    print(f"📊 Final Statistics:")
    print(f"   - Total entries: {total_entries}")
    print(f"   - Target range: Entries 41-10,000")
    print(f"   - Categories: {len(CATEGORIES)}")
    print(f"   - Generation time: {total_time:.1f} seconds")
    print(f"💾 Master file: sylva_dataset_complete.json")
    
    return total_entries

def generate_sample_ranges():
    """Generate specific sample ranges for testing"""
    
    print("🧪 SYLVA Sample Range Generator")
    print("=" * 40)
    
    # Generate next 10 batches (6-15) for immediate validation
    print("Generating next 10 batches (6-15) for validation...")
    
    global_used_closures = []
    global_used_prompts = []
    batch_files = []
    
    # Add existing files
    for i in range(1, 6):
        batch_file = f"sylva_batch_{i:03d}.json"
        if Path(batch_file).exists():
            batch_files.append(batch_file)
    
    # Generate batches 6-15
    for batch_num in range(6, 16):
        start_id = 41 + (batch_num - 1) * 100
        print(f"📝 Batch {batch_num}: Entries {start_id}-{start_id + 99}")
        
        batch_entries = generate_batch(start_id, 100, global_used_closures, global_used_prompts)
        batch_file = save_batch(batch_entries, batch_num)
        batch_files.append(batch_file)
        
        categories = len(set(entry['metadata']['category'] for entry in batch_entries))
        print(f"  ✅ Complete - {categories}/10 categories covered")
    
    # Create partial dataset
    total_entries = combine_batches(batch_files, "sylva_dataset_partial.json")
    
    print(f"\n🎉 Sample generation complete!")
    print(f"📊 Generated: {total_entries} entries (batches 1-15)")
    print(f"💾 File: sylva_dataset_partial.json")
    
    return total_entries

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--sample":
        # Generate sample batches for validation
        generate_sample_ranges()
    elif len(sys.argv) > 1 and sys.argv[1] == "--full":
        # Generate complete dataset
        generate_dataset_chunks(start_batch=6, end_batch=100, chunk_size=10)
    else:
        print("🎭 SYLVA Dataset Generation Options")
        print("=" * 40)
        print("Available commands:")
        print("  python3 sylva_production_runner.py --sample  # Generate batches 6-15 (1,500 entries)")
        print("  python3 sylva_production_runner.py --full    # Generate full dataset (10,000 entries)")
        print()
        print("Current status:")
        
        # Check existing files
        existing_batches = []
        for i in range(1, 101):
            batch_file = f"sylva_batch_{i:03d}.json"
            if Path(batch_file).exists():
                existing_batches.append(i)
        
        if existing_batches:
            print(f"  📁 Existing batches: {min(existing_batches)}-{max(existing_batches)} ({len(existing_batches)} batches)")
            print(f"  📊 Estimated entries: {len(existing_batches) * 100}")
        else:
            print("  📁 No existing batches found")
        
        print()
        print("Recommendation: Start with --sample to validate, then --full for complete dataset")