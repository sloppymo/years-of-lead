# Willow Dataset Cleanup Actions

## Immediate Actions Required

### 1. Remove Synthetic Scenarios
- **Delete entries WILLOW_104-203** (100 synthetic scenarios)
- These all start with "This is too much. I can't keep up with everything."
- Lack real housing context and provide poor training value

### 2. Fix Problematic Promises (7 instances)

**WILLOW_001**: 
- Current: "Text HEAT for emergency repair within 2 hours"
- Fix to: "Text HEAT for priority emergency repair tracking"

**WILLOW_004**:
- Current: "Emergency crew today"
- Fix to: "Emergency crew request submitted with highest priority"

**WILLOW_014**:
- Current: "Emergency mold team TODAY"
- Fix to: "Emergency mold team request escalated"

**WILLOW_036**:
- Current: "Tech arriving within 2 hours"
- Fix to: "Tech dispatch requested as priority"

**WILLOW_050**:
- Current: "Emergency water extraction TODAY"
- Fix to: "Emergency water extraction flagged for immediate dispatch"

**WILLOW_072**:
- Current: "Emergency mold assessment today"
- Fix to: "Emergency mold assessment prioritized"

**WILLOW_095**:
- Current: "pushing for today"
- Fix to: "marked as urgent priority"

### 3. Final Corpus Structure
- After cleanup: 103 high-quality entries
- Renumber sequentially as WILLOW_001-103
- Save as `willow_training_corpus_production.jsonl`

## Verification Checklist
- [ ] All synthetic scenarios removed
- [ ] No promises of specific timeframes
- [ ] No guarantees of third-party actions
- [ ] Process transparency maintained
- [ ] Trauma-informed language preserved

## Result
A clean corpus of 103 diverse, legally safe, trauma-informed training examples ready for production use.