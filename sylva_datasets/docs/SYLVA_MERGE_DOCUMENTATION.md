# SYLVA Dataset Merge Script — Documentation

## 🎭 Overview

The **SYLVA Dataset Merge Script** (`merge_sylva_datasets.py`) creates a unified therapeutic corpus from multiple SYLVA datasets with proper ID management, source tracking, and duplicate detection.

## 📁 Input Files Expected

```
therapeutic_dataset_8000_complete.json    # Primary 8000-entry dataset
therapeutic_dataset_extended.json         # Extended dataset  
therapeutic_dataset_final_2000.json       # Final 2000-entry dataset
```

## 🎯 Core Features

### 1. **Source Tagging**
Each entry receives a `source_set` field indicating origin:
- `"8000_set"` - Primary therapeutic dataset
- `"extended_set"` - Extended therapeutic dataset  
- `"final_2000_set"` - Final therapeutic dataset

### 2. **ID Reindexing**
Prevents ID collisions with strategic reindexing:
- **8000 set**: IDs 1-8000 (preserved)
- **Extended set**: IDs 10001-15000 (reindexed)
- **Final 2000 set**: IDs 20001-22000 (reindexed)

### 3. **Duplicate Detection**
Case-insensitive prompt analysis identifies:
- Exact duplicate prompts across datasets
- Duplicate groups and counts
- Duplication rate statistics

### 4. **Data Validation**
Ensures structural integrity:
- Required SYLVA fields present
- Non-empty prompts and responses
- Valid JSON structure
- Entry count verification

## 📊 Output Files

### `sylva_dataset_merged.json`
```json
{
  "metadata": {
    "dataset_name": "SYLVA Unified Therapeutic Corpus",
    "version": "1.0", 
    "generation_date": "2024-01-16",
    "total_entries": 15000,
    "source_breakdown": {
      "8000_set": 8000,
      "extended_set": 5000,
      "final_2000_set": 2000
    },
    "id_ranges": {
      "8000_set": "1-8000",
      "extended_set": "10001-15000",
      "final_2000_set": "20001-22000"
    },
    "duplicate_summary": {
      "total_duplicates": 245,
      "unique_prompts": 14755
    }
  },
  "entries": [
    {
      "entry_id": 1,
      "prompt": "...",
      "response": "...",
      "closure": "...",
      "metadata": { ... },
      "source_set": "8000_set",
      "original_entry_id": 1
    }
  ]
}
```

### `sylva_prompt_duplicates_report.json`
```json
{
  "analysis_date": "2024-01-16",
  "total_entries_analyzed": 15000,
  "summary": {
    "total_duplicate_groups": 85,
    "total_duplicate_entries": 245,
    "unique_prompts": 14755,
    "duplication_rate": 1.63
  },
  "duplicate_groups": {
    "normalized_prompt_hash": {
      "count": 3,
      "entries": [
        {
          "entry_id": 1245,
          "source_set": "8000_set",
          "original_prompt": "I feel overwhelmed by work stress..."
        }
      ],
      "example_prompt": "I feel overwhelmed by work stress..."
    }
  }
}
```

## 🚀 Usage

### Basic Execution
```bash
python3 merge_sylva_datasets.py
```

### Process Flow
1. **Load Datasets** - Reads and validates input JSON files
2. **Reindex Entries** - Applies new ID ranges and source tags
3. **Validate Structure** - Ensures SYLVA field requirements
4. **Detect Duplicates** - Analyzes prompt similarity
5. **Save Outputs** - Creates merged dataset and duplicate report
6. **Final Validation** - Verifies output integrity

## 📋 Entry Structure

### Input Entry (Original)
```json
{
  "entry_id": 42,
  "prompt": "I feel trapped in negative thought patterns...",
  "response": "These patterns often form as protection...",
  "closure": "That's enough for now.",
  "metadata": {
    "category": "anxiety",
    "subcategory": "rumination", 
    "age_group": "adult",
    "context": "cognitive"
  }
}
```

### Output Entry (Merged)
```json
{
  "entry_id": 10042,
  "prompt": "I feel trapped in negative thought patterns...",
  "response": "These patterns often form as protection...",
  "closure": "That's enough for now.",
  "metadata": {
    "category": "anxiety",
    "subcategory": "rumination",
    "age_group": "adult", 
    "context": "cognitive"
  },
  "source_set": "extended_set",
  "original_entry_id": 42
}
```

## 🔍 Quality Assurance

### Validation Checks
- ✅ Required fields present (`entry_id`, `prompt`, `response`, `source_set`)
- ✅ Non-empty prompt and response content
- ✅ Unique entry IDs across merged dataset
- ✅ Proper JSON structure and formatting
- ✅ Metadata preservation from source datasets

### Error Handling
- Missing files handled gracefully (warnings, not errors)
- Invalid JSON entries skipped with counts
- Structural validation before saving
- Comprehensive error reporting

## 📈 Statistics Tracking

The script provides detailed statistics:

```
📊 Final Statistics:
   📁 Output: sylva_dataset_merged.json
   📄 Duplicate Report: sylva_prompt_duplicates_report.json  
   📈 Total Entries: 15,247
   🔄 Unique Prompts: 14,892
   📋 Source Breakdown:
      8000_set: 8000 entries
      extended_set: 5247 entries
      final_2000_set: 2000 entries
```

## 🛠️ Customization

### Modify ID Ranges
Edit the `dataset_configs` in `merge_datasets()`:
```python
dataset_configs = [
    {
        'file': 'your_dataset_1.json',
        'source_set': 'custom_set_1', 
        'start_id': 1,
        'expected_range': (1, 5000)
    },
    # Add more datasets...
]
```

### Custom Validation Rules
Override `validate_entry_structure()` for specific requirements:
```python
def validate_entry_structure(self, entry: Dict) -> bool:
    required_fields = ['entry_id', 'prompt', 'response', 'custom_field']
    # Custom validation logic...
```

## 🎉 Success Metrics

A successful merge produces:
- **Zero ID collisions** across all source datasets
- **Complete source traceability** via `source_set` tags
- **Comprehensive duplicate analysis** for data quality review
- **Valid JSON structure** ready for model training
- **Preserved metadata** from all source datasets

## 🔧 Troubleshooting

### Common Issues

**File Not Found**
```
⚠️  Warning: therapeutic_dataset_8000_complete.json not found, skipping...
```
→ Ensure all input files are in the working directory

**Invalid JSON Structure**
```
❌ JSON Error in file.json: Unexpected token
```
→ Validate JSON syntax in source files

**High Duplication Rate**
```
Duplication rate: 45.2%
```
→ Review duplicate report for data quality assessment

**Memory Issues with Large Datasets**
→ Consider processing in chunks or increasing available RAM

## 📝 Example Workflow

```bash
# 1. Prepare input datasets
ls *.json
# therapeutic_dataset_8000_complete.json
# therapeutic_dataset_extended.json
# therapeutic_dataset_final_2000.json

# 2. Run merge
python3 merge_sylva_datasets.py

# 3. Verify outputs
ls sylva_*
# sylva_dataset_merged.json
# sylva_prompt_duplicates_report.json

# 4. Review statistics
grep -A 10 "Final Statistics" merge_output.log
```

## 🎯 Production Readiness

The merged dataset is optimized for:
- **Machine Learning Training** - Consistent structure and metadata
- **Therapeutic AI Models** - SYLVA framework compliance
- **Data Analysis** - Source tracking and duplicate identification
- **Quality Control** - Comprehensive validation and reporting

Ready for immediate deployment in therapeutic AI applications following the SYLVA containment-over-completion paradigm.