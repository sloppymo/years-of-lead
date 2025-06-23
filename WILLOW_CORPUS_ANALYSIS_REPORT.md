# WILLOW Corpus Analysis Report

## Executive Summary

The WILLOW corpus currently contains **1,558 entries** designed for a legally cautious, emotionally regulated AI system for tenant support and staff training. The analysis reveals significant gaps in achieving the target dataset structure of 3,000 entries for the 500-unit residential housing pilot.

## Current Dataset Statistics

### 1. Total Entries: 1,558

### 2. User Type Distribution (Inferred)
- **Resident-facing**: 1,552 entries (99.6%)
- **Staff-facing**: 6 entries (0.4%)

**Critical Gap**: The corpus is severely lacking staff-facing entries, with only 6 out of the target 1,200.

### 3. Complexity Level Distribution
- **Critical**: 242 entries (15.5%)
- **High**: 510 entries (32.7%)
- **Medium**: 282 entries (18.1%)
- **Low**: 70 entries (4.5%)
- **Unknown**: 454 entries (29.1%)

**Data Quality Issue**: 454 entries (29.1%) are missing complexity level classification.

### 4. Tier Distribution
- **Tier 1 (Containment)**: 1,301 entries (83.5%)
- **Tier 1.5 (Transitional)**: 192 entries (12.3%)
- **Tier 2 (Action)**: 1,422 entries (91.3%)
- **Tier 3 (Escalation)**: 0 entries (0%)

**Critical Gap**: No Tier 3 escalation scenarios exist in the current corpus.

### 5. Category Coverage
- **Total unique categories**: 85
- **Well-represented** (100+ entries): 6 categories
- **Underrepresented** (<50 entries): 75 categories

Top categories:
1. Unknown: 454 entries
2. Climate infrastructure: 100 entries
3. Digital divide: 100 entries
4. Mental health crisis: 100 entries
5. Economic displacement: 100 entries
6. Family separation: 100 entries

## Gap Analysis Against Target Structure

### Target Distribution:
- **Total**: 3,000 entries
  - Resident-facing: 1,800 (60%)
  - Staff-facing: 1,200 (40%)
- **Tier Distribution**: 60% Tier 1, 35% Tier 2, 5% Tier 3
- **Categories**: 12-15 well-balanced categories

### Current Gaps:

#### 1. User Type Gaps
| User Type | Current | Target | Gap | % Complete |
|-----------|---------|--------|-----|------------|
| Resident | 1,552 | 1,800 | 248 | 86.2% |
| Staff | 6 | 1,200 | 1,194 | 0.5% |
| **Total** | **1,558** | **3,000** | **1,442** | **51.9%** |

#### 2. Tier Distribution Gaps

**Resident Entries:**
| Tier | Current | Target | Gap | Status |
|------|---------|--------|-----|--------|
| Tier 1 | 1,295 | 1,080 | -215 | Over-represented |
| Tier 2 | 1,416 | 630 | -786 | Significantly over |
| Tier 3 | 0 | 90 | 90 | Missing entirely |

**Staff Entries:**
| Tier | Current | Target | Gap | Status |
|------|---------|--------|-----|--------|
| Tier 1 | 6 | 720 | 714 | Severely under |
| Tier 2 | 6 | 420 | 414 | Severely under |
| Tier 3 | 0 | 60 | 60 | Missing entirely |

#### 3. Category Balance Issues
- 454 entries (29.1%) have no category classification
- 75 out of 85 categories have fewer than 50 entries
- Only 6 categories have 100+ entries
- Many critical categories are underrepresented:
  - Life safety emergencies: <10 entries
  - Legal protection scenarios: <25 entries
  - Staff training scenarios: <10 entries
  - Escalation protocols: 0 entries

## Priority Roadmap for Dataset Completion

### Total Entries Needed: 1,442
- Resident entries needed: 248
- Staff entries needed: 1,194

### Phase 1: Critical Safety & Legal (Weeks 1-2)
**350 total entries**

#### Batch 1.1: Life Safety Emergencies
- 100 resident entries (80% Tier 1, 20% Tier 2)
- 75 staff entries (70% Tier 1, 25% Tier 2, 5% Tier 3)
- Categories: fire_safety, medical_emergency, domestic_violence, child_endangerment

#### Batch 1.2: Legal Protection
- 100 resident entries (60% Tier 1, 35% Tier 2, 5% Tier 3)
- 75 staff entries (50% Tier 1, 40% Tier 2, 10% Tier 3)
- Categories: illegal_eviction, discrimination, retaliation, privacy_violations

### Phase 2: Mental Health & Crisis (Weeks 3-4)
**450 total entries**

#### Batch 2.1: Mental Health Support
- 125 resident entries (75% Tier 1, 25% Tier 2)
- 100 staff entries (70% Tier 1, 30% Tier 2)
- Categories: mental_health_crisis, substance_abuse, hoarding, self_harm_risk

#### Batch 2.2: Complex Trauma Response
- 125 resident entries (80% Tier 1, 20% Tier 2)
- 100 staff entries (75% Tier 1, 25% Tier 2)
- Categories: trauma_triggers, dissociation, panic_attacks, crisis_escalation

### Phase 3: Routine Operations (Weeks 5-6)
**550 total entries**

#### Batch 3.1: Maintenance & Repairs
- 150 resident entries (30% Tier 1, 65% Tier 2, 5% Tier 3)
- 125 staff entries (20% Tier 1, 70% Tier 2, 10% Tier 3)

#### Batch 3.2: Administrative Issues
- 150 resident entries (40% Tier 1, 55% Tier 2, 5% Tier 3)
- 125 staff entries (30% Tier 1, 60% Tier 2, 10% Tier 3)

### Phase 4: Community & Relationships (Weeks 7-8)
**450 total entries**

#### Batch 4.1: Neighbor Relations
- 125 resident entries (50% Tier 1, 45% Tier 2, 5% Tier 3)
- 100 staff entries (40% Tier 1, 50% Tier 2, 10% Tier 3)

#### Batch 4.2: Community Building
- 125 resident entries (40% Tier 1, 55% Tier 2, 5% Tier 3)
- 100 staff entries (30% Tier 1, 60% Tier 2, 10% Tier 3)

### Phase 5: Edge Cases & Integration (Weeks 9-10)
**350 total entries**

#### Batch 5.1: Complex Multi-Issue
- 100 resident entries (60% Tier 1, 35% Tier 2, 5% Tier 3)
- 75 staff entries (50% Tier 1, 40% Tier 2, 10% Tier 3)

#### Batch 5.2: Cultural & Linguistic
- 100 resident entries (55% Tier 1, 40% Tier 2, 5% Tier 3)
- 75 staff entries (45% Tier 1, 45% Tier 2, 10% Tier 3)

## Key Recommendations

### 1. Immediate Actions
- **Fix data quality**: Add missing user_type, complexity_level, and category fields to existing entries
- **Create staff training corpus**: Urgent need for 1,194 staff-facing entries
- **Add Tier 3 scenarios**: Create 150 escalation scenarios (90 resident, 60 staff)

### 2. Balance Adjustments
- Reduce Tier 2 representation in resident entries
- Increase Tier 1 representation in new entries
- Ensure each category has at least 100-200 entries

### 3. Quality Assurance
- Implement consistent field validation
- Review legal safety across all responses
- Ensure trauma-informed approach consistency
- Validate tier progression logic

### 4. Priority Categories for Expansion
1. Life safety emergencies
2. Legal protection scenarios
3. Staff de-escalation training
4. Mental health crisis support
5. Multi-issue complex scenarios
6. Cultural and linguistic accommodation
7. Escalation protocols

## Conclusion

The WILLOW corpus has a solid foundation with 1,558 entries but requires significant expansion to meet the pilot requirements. The most critical gap is the near-absence of staff-facing training scenarios (only 0.5% complete). Additionally, the lack of Tier 3 escalation scenarios and the imbalance in tier distribution need immediate attention.

Following the proposed 10-week roadmap will bring the corpus to the target 3,000 entries with appropriate distribution across user types, tiers, and categories, ensuring comprehensive coverage for the 500-unit residential housing pilot.