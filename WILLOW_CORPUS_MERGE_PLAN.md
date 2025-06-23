# Willow Corpus Merge Plan

## Current Situation
- **Workspace file**: `willow_corpus_final_clean.jsonl` - 1,443 entries
- **Your local file**: 1,558 entries (in Documents folder)
- **Difference**: 115 entries

## Merge Process (Once Local File is Available)

### Step 1: Analysis
1. Identify unique entries in local file
2. Check for duplicate IDs
3. Identify any conflicts or overlaps
4. Verify data integrity of both files

### Step 2: Deduplication Strategy
1. Keep the higher quality version when duplicates exist
2. Preserve unique entries from both files
3. Maintain chronological order by WILLOW_ID

### Step 3: Quality Checks
- Verify all entries have required fields
- Check for liability issues
- Ensure consistent formatting
- Validate arousal/capacity metrics

### Step 4: Create Merged File
- Combine unique entries
- Sort by WILLOW_ID
- Create backup of original files
- Document what was merged

## What I Need From You

Please upload your local file (from Documents folder) to the workspace. You can:
1. Copy it to the workspace directory, or
2. Upload it with a different name like `willow_corpus_documents_version.jsonl`

Once uploaded, I can:
- Compare the entries
- Identify the 115 missing entries
- Merge them appropriately
- Create a final consolidated version