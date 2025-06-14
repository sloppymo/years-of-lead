#!/usr/bin/env python3
"""
SYLVA Dataset Merge Script — Unified Therapeutic Corpus Generation

Merges three SYLVA therapeutic datasets into one unified, model-ready JSON file
with no ID collisions, source tags, and duplicate prompt detection.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any, Tuple, Set
from collections import defaultdict, Counter
import hashlib

class SylvaDatasetMerger:
    def __init__(self):
        self.datasets = {}
        self.merged_data = []
        self.duplicate_report = {}
        self.stats = {
            'total_entries': 0,
            'source_counts': {},
            'duplicate_prompts': 0,
            'unique_prompts': 0
        }
    
    def load_dataset(self, filepath: str, source_name: str) -> List[Dict[str, Any]]:
        """Load and validate a dataset file"""
        try:
            if not Path(filepath).exists():
                print(f"⚠️  Warning: {filepath} not found, skipping...")
                return []
            
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if not isinstance(data, list):
                print(f"❌ Error: {filepath} is not a list format")
                return []
            
            print(f"✅ Loaded {filepath}: {len(data)} entries")
            return data
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON Error in {filepath}: {e}")
            return []
        except Exception as e:
            print(f"❌ Error loading {filepath}: {e}")
            return []
    
    def normalize_prompt(self, prompt: str) -> str:
        """Normalize prompt for duplicate detection (case-insensitive, whitespace-cleaned)"""
        return prompt.lower().strip().replace('\n', ' ').replace('\r', ' ')
    
    def reindex_entries(self, entries: List[Dict], source_set: str, start_id: int) -> List[Dict]:
        """Reindex entries with new IDs and add source_set field"""
        reindexed = []
        
        for i, entry in enumerate(entries):
            # Create new entry with reindexed ID and source tag
            new_entry = entry.copy()
            new_entry['entry_id'] = start_id + i
            new_entry['source_set'] = source_set
            
            # Preserve original entry_id as reference
            if 'entry_id' in entry:
                new_entry['original_entry_id'] = entry['entry_id']
            
            reindexed.append(new_entry)
        
        return reindexed
    
    def detect_duplicates(self, all_entries: List[Dict]) -> Dict[str, Any]:
        """Detect duplicate prompts across all entries"""
        prompt_map = defaultdict(list)
        
        # Group entries by normalized prompt
        for entry in all_entries:
            if 'prompt' in entry:
                normalized = self.normalize_prompt(entry['prompt'])
                prompt_map[normalized].append({
                    'entry_id': entry['entry_id'],
                    'source_set': entry['source_set'],
                    'original_prompt': entry['prompt']
                })
        
        # Find duplicates
        duplicates = {}
        duplicate_count = 0
        
        for normalized_prompt, entries in prompt_map.items():
            if len(entries) > 1:
                duplicates[normalized_prompt] = {
                    'count': len(entries),
                    'entries': entries,
                    'example_prompt': entries[0]['original_prompt']
                }
                duplicate_count += len(entries) - 1  # Count extra duplicates
        
        return {
            'total_duplicate_groups': len(duplicates),
            'total_duplicate_entries': duplicate_count,
            'unique_prompts': len(prompt_map) - duplicate_count,
            'duplicate_details': duplicates
        }
    
    def validate_entry_structure(self, entry: Dict) -> bool:
        """Validate that an entry has required SYLVA fields"""
        required_fields = ['entry_id', 'prompt', 'response', 'source_set']
        
        for field in required_fields:
            if field not in entry:
                return False
        
        # Check for empty values
        if not entry['prompt'] or not entry['response']:
            return False
        
        return True
    
    def merge_datasets(self) -> bool:
        """Main merge process"""
        print("🎭 SYLVA Dataset Merger")
        print("=" * 50)
        
        # Dataset configurations
        dataset_configs = [
            {
                'file': 'therapeutic_dataset_8000_complete.json',
                'source_set': '8000_set',
                'start_id': 1,
                'expected_range': (1, 8000)
            },
            {
                'file': 'therapeutic_dataset_extended.json', 
                'source_set': 'extended_set',
                'start_id': 10001,
                'expected_range': (10001, 15000)
            },
            {
                'file': 'therapeutic_dataset_final_2000.json',
                'source_set': 'final_2000_set', 
                'start_id': 20001,
                'expected_range': (20001, 22000)
            }
        ]
        
        all_entries = []
        
        # Load and process each dataset
        for config in dataset_configs:
            print(f"\n📂 Processing {config['file']}...")
            
            # Load dataset
            entries = self.load_dataset(config['file'], config['source_set'])
            
            if not entries:
                print(f"⚠️  Skipping empty dataset: {config['file']}")
                continue
            
            # Reindex entries
            reindexed = self.reindex_entries(
                entries, 
                config['source_set'], 
                config['start_id']
            )
            
            # Validate entries
            valid_entries = []
            invalid_count = 0
            
            for entry in reindexed:
                if self.validate_entry_structure(entry):
                    valid_entries.append(entry)
                else:
                    invalid_count += 1
            
            if invalid_count > 0:
                print(f"⚠️  Skipped {invalid_count} invalid entries from {config['file']}")
            
            print(f"✅ Processed {len(valid_entries)} valid entries")
            print(f"   ID Range: {config['start_id']}-{config['start_id'] + len(valid_entries) - 1}")
            
            all_entries.extend(valid_entries)
            self.stats['source_counts'][config['source_set']] = len(valid_entries)
        
        if not all_entries:
            print("❌ No valid entries found in any dataset!")
            return False
        
        self.merged_data = all_entries
        self.stats['total_entries'] = len(all_entries)
        
        print(f"\n📊 Merge Summary:")
        print(f"   Total entries: {self.stats['total_entries']}")
        for source, count in self.stats['source_counts'].items():
            print(f"   {source}: {count} entries")
        
        return True
    
    def generate_duplicate_report(self) -> bool:
        """Generate duplicate detection report"""
        print(f"\n🔍 Analyzing prompt duplicates...")
        
        duplicate_analysis = self.detect_duplicates(self.merged_data)
        
        self.duplicate_report = {
            'analysis_date': '2024-01-16',
            'total_entries_analyzed': len(self.merged_data),
            'summary': {
                'total_duplicate_groups': duplicate_analysis['total_duplicate_groups'],
                'total_duplicate_entries': duplicate_analysis['total_duplicate_entries'], 
                'unique_prompts': duplicate_analysis['unique_prompts'],
                'duplication_rate': round(
                    (duplicate_analysis['total_duplicate_entries'] / len(self.merged_data)) * 100, 2
                ) if self.merged_data else 0
            },
            'duplicate_groups': duplicate_analysis['duplicate_details']
        }
        
        print(f"   Duplicate groups: {duplicate_analysis['total_duplicate_groups']}")
        print(f"   Duplicate entries: {duplicate_analysis['total_duplicate_entries']}")
        print(f"   Unique prompts: {duplicate_analysis['unique_prompts']}")
        print(f"   Duplication rate: {self.duplicate_report['summary']['duplication_rate']}%")
        
        self.stats.update({
            'duplicate_prompts': duplicate_analysis['total_duplicate_entries'],
            'unique_prompts': duplicate_analysis['unique_prompts']
        })
        
        return True
    
    def save_merged_dataset(self, output_file: str = 'sylva_dataset_merged.json') -> bool:
        """Save the merged dataset"""
        try:
            print(f"\n💾 Saving merged dataset to {output_file}...")
            
            # Add metadata header
            output_data = {
                'metadata': {
                    'dataset_name': 'SYLVA Unified Therapeutic Corpus',
                    'version': '1.0',
                    'generation_date': '2024-01-16',
                    'total_entries': len(self.merged_data),
                    'source_breakdown': self.stats['source_counts'],
                    'id_ranges': {
                        '8000_set': '1-8000',
                        'extended_set': '10001-15000', 
                        'final_2000_set': '20001-22000'
                    },
                    'duplicate_summary': {
                        'total_duplicates': self.stats['duplicate_prompts'],
                        'unique_prompts': self.stats['unique_prompts']
                    }
                },
                'entries': self.merged_data
            }
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Merged dataset saved: {len(self.merged_data)} entries")
            return True
            
        except Exception as e:
            print(f"❌ Error saving merged dataset: {e}")
            return False
    
    def save_duplicate_report(self, output_file: str = 'sylva_prompt_duplicates_report.json') -> bool:
        """Save the duplicate analysis report"""
        try:
            print(f"💾 Saving duplicate report to {output_file}...")
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(self.duplicate_report, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Duplicate report saved")
            return True
            
        except Exception as e:
            print(f"❌ Error saving duplicate report: {e}")
            return False
    
    def validate_final_output(self, merged_file: str) -> bool:
        """Validate the final merged dataset"""
        print(f"\n🔍 Validating final output...")
        
        try:
            with open(merged_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Check structure
            if 'metadata' not in data or 'entries' not in data:
                print("❌ Invalid structure: missing metadata or entries")
                return False
            
            entries = data['entries']
            
            # Check entry count
            expected_count = data['metadata']['total_entries']
            if len(entries) != expected_count:
                print(f"❌ Entry count mismatch: expected {expected_count}, got {len(entries)}")
                return False
            
            # Check ID uniqueness
            ids = [entry['entry_id'] for entry in entries if 'entry_id' in entry]
            if len(ids) != len(set(ids)):
                print("❌ Duplicate entry IDs found")
                return False
            
            # Check required fields
            missing_fields = 0
            for entry in entries[:10]:  # Sample check
                if not self.validate_entry_structure(entry):
                    missing_fields += 1
            
            if missing_fields > 0:
                print(f"⚠️  {missing_fields}/10 sample entries have missing fields")
            
            print("✅ Final validation passed")
            return True
            
        except Exception as e:
            print(f"❌ Validation error: {e}")
            return False
    
    def run_merge(self) -> bool:
        """Execute the complete merge process"""
        try:
            # Step 1: Merge datasets
            if not self.merge_datasets():
                return False
            
            # Step 2: Analyze duplicates
            if not self.generate_duplicate_report():
                return False
            
            # Step 3: Save merged dataset
            if not self.save_merged_dataset():
                return False
            
            # Step 4: Save duplicate report
            if not self.save_duplicate_report():
                return False
            
            # Step 5: Validate output
            if not self.validate_final_output('sylva_dataset_merged.json'):
                return False
            
            # Final summary
            print(f"\n🎉 SYLVA Dataset Merge Complete!")
            print(f"📊 Final Statistics:")
            print(f"   📁 Output: sylva_dataset_merged.json")
            print(f"   📄 Duplicate Report: sylva_prompt_duplicates_report.json")
            print(f"   📈 Total Entries: {self.stats['total_entries']}")
            print(f"   🔄 Unique Prompts: {self.stats['unique_prompts']}")
            print(f"   📋 Source Breakdown:")
            for source, count in self.stats['source_counts'].items():
                print(f"      {source}: {count} entries")
            
            return True
            
        except Exception as e:
            print(f"❌ Merge process failed: {e}")
            return False

def main():
    """Main execution function"""
    merger = SylvaDatasetMerger()
    
    success = merger.run_merge()
    
    if success:
        print(f"\n✨ Merge completed successfully!")
        print(f"Ready for model training with unified SYLVA corpus.")
    else:
        print(f"\n💥 Merge failed - check error messages above")
        exit(1)

if __name__ == "__main__":
    main()