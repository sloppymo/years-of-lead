# Willow Training Dataset Analysis Report

## Executive Summary
The current dataset contains **203 entries**, of which **100 (49.3%) are synthetic scenarios** that are unsuitable for training. After removing these, we have **103 high-quality real scenarios**.

## Critical Issues Identified

### 1. Synthetic Scenarios (WILLOW_104-203)
**RECOMMENDATION: REMOVE ALL 100 SYNTHETIC ENTRIES**

Problems:
- **100% identical first messages**: Every synthetic scenario starts with "This is too much. I can't keep up with everything."
- **No housing context**: Issue type is "synthetic_test" with no real tenant problems
- **Formulaic responses**: Limited variation in Willow's responses
- **No realistic complexity**: Missing the nuanced situations found in real entries
- **Poor training value**: Would teach the model to give generic responses

Example of synthetic pattern:
```
Tenant: "This is too much. I can't keep up with everything."
Willow: "It sounds overwhelming. I'm tracking this with you. [symbol]"
Tenant: "I'm trying but nothing works. What's the point?"
Willow: "We can name that weight together. Shall we review what options remain?"
```

### 2. What's Working Well

The **103 real scenarios** demonstrate:
- **84 unique scenario types** covering diverse housing situations
- **Proper tier progression**: All follow the tier_1 → tier_1.5 → tier_2 pattern
- **Realistic dialogue**: Authentic tenant concerns with specific context
- **Trauma-informed responses**: Appropriate techniques and containment
- **Legal safety**: Process transparency without problematic promises
- **Rich metadata**: 77% include outcome data, 100% have full process metrics

## Scenario Coverage (After Cleaning)

Top categories represented:
1. Emergency habitability (heat, flooding, electrical)
2. Health & safety (mold, pests, medical equipment)
3. Discrimination & harassment
4. Mental health crises
5. Financial hardship
6. Disability accommodations
7. Cultural/religious conflicts
8. Domestic violence
9. Immigration concerns
10. Elderly tenant issues
11. LGBTQ+ discrimination
12. Language barriers

## Quality Metrics

### Strengths
- **Symbolic consistency**: Proper anchor introduction, echoing, and carrying
- **Arousal management**: Clear impact tracking showing de-escalation
- **Consent-based progression**: Explicit signals before tier advancement
- **Diversity**: Wide range of intersectional experiences represented

### Issues Found In Real Entries
- **7 instances of problematic promises** including:
  - "within 2 hours" (WILLOW_001, WILLOW_036)
  - "emergency...today" (WILLOW_004, WILLOW_014, WILLOW_050, WILLOW_072, WILLOW_095)
  - These create legal liability and should be revised
- ✓ Consistent tier progression patterns
- ✓ All required fields present
- ✓ Generally appropriate trauma-informed language

## Recommendations

### Immediate Action
1. **Remove all 100 synthetic scenarios** from the training corpus
2. **Fix 7 instances of problematic promises** in entries WILLOW_001, 004, 014, 036, 050, 072, 095
   - Replace "within 2 hours" → "as priority"
   - Replace "emergency...today" → "emergency status applied"
   - Replace specific timeframes with process updates
3. **Use cleaned corpus** with 103 high-quality entries
4. **Renumber entries** sequentially as WILLOW_001-103

### Future Enhancements
1. **Expand real scenarios** to reach 200+ entries by creating new ones based on:
   - Actual tenant support tickets
   - Community organization case studies
   - Housing advocate experiences

2. **Avoid synthetic data** unless it:
   - Uses diverse, realistic opening messages
   - Addresses specific housing issues
   - Includes contextual details
   - Varies response patterns

3. **Quality control** for new entries:
   - Unique opening situations
   - Specific housing context
   - Realistic dialogue progression
   - Complete metadata

## Final Assessment

After removing synthetic scenarios, the corpus contains **103 high-quality, diverse, trauma-informed training examples** that effectively demonstrate:
- Emotional containment techniques
- Tier-based progression
- Legal safety
- Cultural competency
- Crisis de-escalation

This cleaned dataset is suitable for training Willow to provide empathetic, effective tenant support while maintaining appropriate boundaries and legal safety.