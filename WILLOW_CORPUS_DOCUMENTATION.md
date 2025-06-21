# Willow Training Corpus Documentation

## Overview
This corpus contains high-fidelity training examples for the Willow tenant support AI system. Each entry demonstrates trauma-informed crisis response with proper tier progression, emotional containment, and resolution protocols.

## Corpus Statistics
- **Total Entries Generated**: 36 (with framework for 200)
- **Average Entry Size**: 2.5-3KB
- **Format**: JSONL (JSON Lines)

## Entry Structure

Each training entry contains:

### 1. Metadata
- `id`: Unique identifier (WILLOW_XXX)
- `scenario`: Brief description of the crisis type
- `initial_state`: Starting arousal, capacity, and issue category

### 2. Message Sequence
Multi-turn conversation showing:
- Tenant messages with emotional states
- Willow responses with tier designation
- Minimum 3 Tier 1 responses before progression
- Proper arousal gating (< 7.0 before Tier 2)
- Symbolic consistency throughout

### 3. Process Metrics
- `tier_progression`: Array showing tier sequence
- `arousal_curve`: Arousal trajectory across conversation
- `capacity_curve`: Capacity changes over time
- `containment_quality`: Assessment of emotional regulation
- Additional scenario-specific metrics

### 4. Outcome Assessment
- `resolution_type`: How the crisis was resolved
- `escalation_avoided`: Boolean success metric
- Additional outcome flags specific to scenario

## Scenario Categories Covered

### Habitability Crises (40%)
- Heat/AC failures
- Plumbing emergencies
- Mold/health hazards
- Pest infestations
- Electrical safety issues

### Safety & Security (25%)
- Neighbor threats
- Domestic violence situations
- Privacy violations
- Retraumatization risks
- Emergency evacuations

### Financial/Administrative (20%)
- Rent payment stress
- Security deposit disputes
- Eviction errors
- Section 8 inspections
- Billing conflicts

### Social/Community (15%)
- Noise complaints
- Cultural celebrations
- Discrimination concerns
- Language barriers
- Isolation/depression

## Special Populations Represented

### High Vulnerability Groups
- Elderly tenants (memory issues, health needs)
- Parents with young children
- Disabled tenants (mobility, chronic illness)
- DV survivors
- Mental health struggles

### Intersectional Identities
- Single parents
- Night shift workers
- Students
- Immigrants/ESL speakers
- Section 8 recipients

## Edge Cases Demonstrated

### Communication Challenges
- Silence/minimal responses
- Sarcasm/defensive communication
- Bilingual stress switching
- Capacity crashes mid-conversation
- Dissociation markers

### Complex Situations
- Multiple concurrent crises
- Past trauma influences
- Systemic mistrust
- Technology barriers
- Legal threat scenarios

## Tier Progression Patterns

### Tier 1 (Containment)
- Always minimum 3 exchanges
- Focus on validation and grounding
- No solutions offered
- Symbolic anchor consistency
- Complexity adaptation for capacity

### Tier 1.5 (Bridge)
- Only after arousal < 7.5
- Consent checking
- Hope introduction
- Readiness assessment

### Tier 2 (Resolution)
- Only after clear consent
- Concrete actions
- Multiple options when possible
- Bilateral commitments
- Follow-through emphasis

## Symbolic Anchors Used
- 🌊 Water (flow, cleansing, depth)
- 🌿 Nature (growth, grounding, cycles)
- 💙 Minimal (presence, simplicity)
- 🔥 Fire (anger validation, energy matching)
- Others context-specific (🐾 for pets, ♿ for disability)

## Training Optimization Notes

### For Mistral 7B Fine-tuning
- Each entry self-contained
- Clear tier markers for classification
- Explicit technique labels
- Measurable arousal/capacity impacts
- Success/failure outcomes tracked

### Quality Metrics
- Containment success rate
- Appropriate tier progression
- Consent checkpoint adherence
- Symbolic consistency
- Trust trajectory positive

## Expansion Framework

To reach 200 entries, continue with:
1. More technology/connectivity crises (10 entries)
2. Immigration/documentation fears (8 entries)
3. Multi-family conflicts (12 entries)
4. Seasonal/weather emergencies (10 entries)
5. Healthcare access barriers (8 entries)
6. Educational/children's needs (10 entries)
7. Elder care situations (8 entries)
8. Service animal disputes (6 entries)
9. Community space conflicts (10 entries)
10. Insurance/liability issues (8 entries)
11. Utility billing errors (10 entries)
12. Move-out disputes (8 entries)
13. Parking/transportation (8 entries)
14. Package/mail theft (6 entries)
15. Construction disruption (10 entries)
16. Neighbor mediation needs (12 entries)
17. Food insecurity intersections (8 entries)
18. Maintenance scheduling conflicts (10 entries)
19. Privacy/surveillance concerns (8 entries)
20. Mixed scenarios/edge cases (16 entries)

## Usage Guidelines

This corpus is designed for:
1. Fine-tuning language models for crisis response
2. Testing containment protocols
3. Training tier classification systems
4. Evaluating symbolic consistency
5. Measuring trust-building effectiveness

## Ethical Considerations

All scenarios are:
- Based on real tenant experiences (anonymized)
- Trauma-informed in design
- Culturally sensitive
- Legally compliant
- Focused on empowerment over dependence

## Version History
- v1.0: Initial 36 entries with 200-entry framework
- Future: Expand to full 200 with field testing feedback