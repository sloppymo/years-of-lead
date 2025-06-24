# WILLOW Corpus Enhancement Roadmap

## Overview
Transform the current 8.0/10 corpus into a 9.5/10 A100-ready dataset through systematic enhancements.

## Phase 1: Foundation (Week 1)
### 1.1 Enhanced Tagging System
- **Script**: `enhance_corpus_tags.py`
- **Input**: Current corpus with basic tags
- **Output**: Corpus with comprehensive tagging
- **New Tags**:
  - Tenant state descriptors
  - Vulnerability factors
  - Required services
  - Legal risk areas
  - Cultural considerations
  - Time sensitivity levels

### 1.2 Hybrid Timeline Implementation
- **Script**: `implement_hybrid_timelines.py`
- **Input**: No-time-promises corpus
- **Output**: Corpus with safe internal timelines
- **Features**:
  - "Typically" language for internal services
  - Time ranges instead of specific times
  - Contextual variations (business hours, weekends)
  - Confidence levels

## Phase 2: Quality Metrics (Week 2)
### 2.1 Response Quality Metadata
- **Script**: `add_quality_metrics.py`
- **Scoring Dimensions**:
  - Empathy score (1-10)
  - Action clarity (1-10)
  - Legal safety (1-10)
  - Urgency appropriateness (1-10)
  - Cultural sensitivity (1-10)
  - Trauma-informed rating (1-10)

### 2.2 Dialogue Flow Analysis
- **Script**: `analyze_dialogue_flow.py`
- **Metrics**:
  - Emotional arc tracking
  - Trust building moments
  - Consent checkpoints
  - Tier transition quality
  - Symbolic consistency

## Phase 3: Contextual Enhancement (Week 3)
### 3.1 Context Flags Addition
- **Script**: `add_contextual_awareness.py`
- **Context Types**:
  - Temporal (time, day, season)
  - Environmental (building type, location)
  - Operational (staffing levels)
  - Concurrent issues

### 3.2 Chain-of-Thought Reasoning
- **Script**: `add_willow_reasoning.py`
- **Components**:
  - Situation assessment
  - Priority factors
  - Response strategy
  - Risk mitigation

## Phase 4: Diversity Expansion (Week 4)
### 4.1 Scenario Generation
- **Script**: `generate_edge_cases.py`
- **New Scenarios**:
  - Invisible disabilities (200 entries)
  - Cultural/religious needs (150 entries)
  - Climate resilience (150 entries)
  - Multi-generational conflicts (100 entries)
  - Digital privacy concerns (100 entries)

### 4.2 Response Variations
- **Script**: `create_response_variations.py`
- **Variation Types**:
  - Warm maternal
  - Professional efficient
  - Peer supportive
  - Cultural variants

## Phase 5: A100 Optimization (Week 5)
### 5.1 Instruction Format Conversion
- **Script**: `convert_to_instruction_format.py`
- **Format**: System/Instruction/Input/Output/Reasoning

### 5.2 Reinforcement Learning Signals
- **Script**: `add_rl_signals.py`
- **Signals**: Reward, safety, helpfulness, outcome

## Implementation Schedule

### Week 1: Foundation
- Day 1-2: Develop and test enhanced tagging script
- Day 3-4: Implement hybrid timeline system
- Day 5: Validate legal safety maintained

### Week 2: Quality Metrics
- Day 1-2: Build quality scoring system
- Day 3-4: Analyze dialogue flows
- Day 5: Generate quality reports

### Week 3: Context & Reasoning
- Day 1-2: Add contextual flags
- Day 3-4: Implement reasoning chains
- Day 5: Test contextual responses

### Week 4: Diversity
- Day 1-3: Generate new scenarios
- Day 4-5: Create response variations

### Week 5: A100 Prep
- Day 1-2: Convert to instruction format
- Day 3-4: Add RL signals
- Day 5: Final validation

## Success Metrics

### Quantitative
- Total entries: 3,000+ (from 2,375)
- Average quality score: 9.0+
- Tag completeness: 95%+
- Response variations: 3+ per scenario

### Qualitative
- Legal safety maintained
- Urgency effectively communicated
- Cultural sensitivity demonstrated
- Edge cases covered

## Risk Mitigation
1. **Legal Review**: Each phase output reviewed for liability
2. **Incremental Testing**: Validate each enhancement
3. **Rollback Plan**: Keep versioned backups
4. **Quality Gates**: Must pass before next phase

## Deliverables
1. Enhanced corpus (3,000+ entries)
2. Quality metrics dashboard
3. A100-ready instruction dataset
4. Implementation documentation
5. Performance benchmarks

## Next Step
Begin Phase 1.1: Develop `enhance_corpus_tags.py`