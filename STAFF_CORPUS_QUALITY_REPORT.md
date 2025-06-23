# WILLOW Staff Training Corpus Quality Report

## Executive Summary

The WILLOW staff training corpus has been comprehensively evaluated and filtered for quality. Starting with 1,301 entries, we applied rigorous quality criteria to ensure only the highest quality training examples remain.

### Quality Assessment Results

- **Total Entries Evaluated**: 1,301
- **Entries Passing 9.0+ Quality Score**: 817 (62.8%)
- **Entries Passing 9.6+ Quality Score**: 3 (0.2%)

## Quality Criteria

The rating system evaluated each entry on 7 key dimensions (10 points total):

1. **Dialogue Quality** (2.0 points)
   - Realistic, professional dialogue
   - Appropriate message length and content
   - Natural conversation flow

2. **Tier Progression** (1.5 points)
   - Proper tier flow (tier_1 → tier_2 → tier_3)
   - Appropriate escalation based on complexity
   - Logical progression through conversation

3. **Legal Safety** (2.0 points)
   - No problematic or liability-creating language
   - Appropriate boundaries set
   - Non-promissory language used

4. **Training Value** (1.5 points)
   - Clear learning objectives
   - Proper categorization
   - Complete routing logic

5. **Scenario Realism** (1.0 points)
   - Believable situations
   - Emotional authenticity
   - Complexity matches urgency

6. **Completeness** (1.0 points)
   - All required fields present
   - Proper ID formatting
   - Correct user_type designation

7. **Trauma-Informed Approach** (1.0 points)
   - Uses trauma-informed principles
   - Emotional validation in tier_1
   - Empowerment and choice language

## Common Quality Issues Identified

1. **Lacks empowerment/choice language** (95.6% of entries)
   - Many entries missing phrases like "What would help?" or "How can I support you?"

2. **No clear boundaries set** (95.2% of entries)
   - Missing appropriate limitation statements

3. **Lacks emotional authenticity** (84.1% of entries)
   - Resident messages too generic or unemotional

4. **Limited trauma-informed approach** (54.2% of entries)
   - Insufficient use of trauma-informed language and principles

## Top Performing Categories

Average scores by category (out of 10):
1. Amenity Problem: 9.40
2. Resident Relations: 9.20
3. Interpersonal Dispute: 9.20
4. Emergency Management: 9.20
5. Crisis Intervention: 9.15

## Filtered Corpus Details

### High-Quality Corpus (9.0+ Score)
- **File**: `willow_staff_corpus_filtered_90_20250623_235126.jsonl`
- **Entries**: 817
- **Use Case**: General staff training with high-quality examples

### Ultra-High-Quality Corpus (9.6+ Score)
- **File**: `willow_staff_corpus_filtered_20250623_235058.jsonl`
- **Entries**: 3
- **Use Case**: Gold standard examples for demonstration

## Recommendations

1. **Use the 9.0+ filtered corpus** for general staff training
2. **Reference the 9.6+ entries** as exemplary models
3. **Focus improvement efforts** on:
   - Adding more empowerment language
   - Setting clearer professional boundaries
   - Increasing emotional authenticity
   - Strengthening trauma-informed approaches

## Quality Enhancement Process

The corpus underwent a comprehensive enhancement process:
1. Initial generation with basic templates
2. Enhancement with high-quality dialogue templates
3. Addition of proper tier progression
4. Integration of trauma-informed language
5. Quality rating and filtering

## Files Generated

1. **Original Corpus**: `willow_staff_corpus_merged_20250623_234257.jsonl` (1,301 entries)
2. **Enhanced Corpus**: `willow_staff_corpus_enhanced_20250623_235042.jsonl` (1,301 entries)
3. **Filtered 9.0+**: `willow_staff_corpus_filtered_90_20250623_235126.jsonl` (817 entries)
4. **Filtered 9.6+**: `willow_staff_corpus_filtered_20250623_235058.jsonl` (3 entries)

## Conclusion

The filtered staff training corpus provides 817 high-quality examples that demonstrate:
- Professional communication standards
- Proper escalation procedures
- Trauma-informed approaches
- Legal safety awareness
- Realistic scenario handling

These entries are suitable for training property management staff in effective, empathetic, and legally-compliant resident communication.