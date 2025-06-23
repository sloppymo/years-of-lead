# WILLOW Corpus Analysis Report - UPDATED

## Executive Summary

The WILLOW corpus currently contains **17,278 total entries** across multiple files, far exceeding the target of 3,000 entries for the 500-unit residential housing pilot. However, the distribution is heavily skewed toward resident-facing content, with staff training scenarios significantly underrepresented.

## Current Dataset Statistics (All Files Combined)

### 1. Total Entries: 17,278
- This includes duplicates across different corpus versions
- The unique content is estimated at ~2,000-3,000 entries

### 2. User Type Distribution
- **Resident-facing**: 17,168 entries (99.4%)
- **Staff-facing**: 110 entries (0.6%)

**Critical Finding**: While the corpus exceeds the total target, staff training content represents less than 1% of entries, far below the 40% target.

### 3. Staff Entry Locations
Staff training entries are found in:
- `willow_enhanced_100_entries.jsonl`: 50 staff entries
- `willow_staff_administrative_50.jsonl`: 50 staff entries
- `willow_enhanced_schema_examples.jsonl`: 10 staff entries

### 4. Complexity Level Distribution
- **Critical**: 3,156 entries (18.3%)
- **High**: 5,321 entries (30.8%)
- **Medium**: 2,437 entries (14.1%)
- **Low**: 601 entries (3.5%)
- **Unknown**: 5,763 entries (33.4%)

**Data Quality Issue**: One-third of entries lack complexity classification.

### 5. Category Coverage
- **Total unique categories**: 85+
- **Well-represented** (600+ entries each):
  - Climate infrastructure: 800
  - Digital divide: 800
  - Economic displacement: 800
  - Mental health crisis: 799
  - Family separation: 798
  - Boundary crisis: 732
- **Unknown category**: 5,763 entries (33.4%)

## Revised Gap Analysis

### For a Curated 3,000 Entry Dataset:

#### 1. User Type Balance
| User Type | Current | Target | Action Needed |
|-----------|---------|--------|---------------|
| Resident | 17,168 | 1,800 | Select best 1,800 |
| Staff | 110 | 1,200 | Generate 1,090 more |

#### 2. Primary Gap: Staff Training Content
- **Current**: 110 entries (0.6% of total)
- **Target**: 1,200 entries (40% of final dataset)
- **Gap**: 1,090 staff training scenarios needed

#### 3. Content Curation Needs
Given the corpus has 17,000+ resident entries but needs only 1,800:
- Deduplicate entries across corpus versions
- Select highest quality entries with proper tier distribution
- Ensure category balance
- Fix entries missing category/complexity classifications

## Key Findings

1. **Abundance of Resident Content**: With 17,000+ resident-facing entries, the challenge is curation and quality selection rather than generation.

2. **Severe Staff Training Gap**: Only 110 staff training entries exist, requiring generation of 1,090 additional scenarios to meet the 40% target.

3. **Data Quality Issues**: 
   - 33% of entries lack proper categorization
   - Multiple duplicate versions exist across files
   - Tier 3 escalation scenarios may be underrepresented

4. **File Organization**: The corpus is spread across 18+ files with overlapping content, requiring consolidation and deduplication.

## Revised Recommendations

### 1. Immediate Priority: Staff Training Content
Generate 1,090 staff training entries focusing on:
- De-escalation techniques
- Legal compliance training
- Crisis intervention protocols
- Documentation best practices
- Fair housing scenarios
- Emergency response procedures
- Difficult resident interactions
- Team coordination scenarios

### 2. Corpus Consolidation
- Deduplicate entries across all files
- Create a single authoritative corpus
- Properly tag all entries with user_type field
- Fix missing category/complexity classifications

### 3. Quality-Based Selection for Residents
From the 17,000+ resident entries, select the best 1,800 based on:
- Proper tier distribution (60% Tier 1, 35% Tier 2, 5% Tier 3)
- Category balance across 12-15 key categories
- Legal safety and trauma-informed quality
- Complexity level distribution

### 4. Final Dataset Structure
Create a curated 3,000-entry dataset:
- 1,800 resident entries (selected from existing)
- 1,200 staff entries (110 existing + 1,090 new)
- Proper tier distribution maintained
- All entries properly categorized and tagged

## Conclusion

The WILLOW corpus contains abundant resident-facing content but severely lacks staff training scenarios. The path forward requires:
1. Massive generation effort for staff training content (1,090 entries)
2. Careful curation and selection from existing resident entries
3. Data quality improvements and deduplication
4. Proper organization into a single, well-structured dataset

The good news is that the resident-facing content is already largely complete, allowing focus on the critical gap in staff training materials.