# WILLOW Corpus Difference Analysis

## File Comparison Summary

### Your Local File (Documents folder)
- **Total entries**: 1,558

### Workspace File (willow_corpus_final_clean.jsonl)
- **Total entries**: 1,443
- **Highest ID**: WILLOW_1658
- **Missing IDs**: 215

## Analysis

The workspace file has 1,443 entries but the IDs go up to WILLOW_1658, meaning there are 215 gaps in the numbering sequence. This explains why:

1. **Expected entries if continuous**: 1,658 entries (WILLOW_1 through WILLOW_1658)
2. **Actual entries in workspace**: 1,443 entries
3. **Gap**: 215 missing IDs

Your local file with 1,558 entries likely has:
- 115 additional entries that aren't in the workspace version (1,558 - 1,443 = 115)
- Possibly some of the missing IDs filled in
- Or additional entries beyond WILLOW_1658

## Missing ID Ranges in Workspace File

Some examples of missing ranges:
- WILLOW_1344 through WILLOW_1458 (115 consecutive missing entries)
- This appears to be a large gap before the routine housing batch (WILLOW_1559-1658)

## Recommendation

To fully understand the difference, you would need to:
1. Check what IDs are present in your local file that aren't in the workspace
2. Determine if your local file has entries beyond WILLOW_1658
3. Decide which version should be the authoritative source