# WILLOW Corpus Tags Summary

## Overview
The WILLOW corpus has been enhanced with comprehensive tags to improve training, routing, and analysis capabilities. These tags enable sophisticated AI behavior and better resource allocation.

## Tag Categories

### 1. **Urgency Level** (`urgency_level`)
Detects crisis levels for appropriate routing and response timing.
- `immediate` - Emergency situations requiring instant response (26.6%)
- `high` - Urgent matters needing same-day attention (16.3%)
- `medium` - Standard concerns with normal response time (47.5%)
- `low` - Information requests or non-urgent queries (9.6%)

### 2. **Primary Emotion** (`primary_emotion`)
Identifies emotional state for empathy-based routing.
- `neutral` - Calm, information-seeking (83.1%)
- `frustration` - Annoyed or irritated (9.9%)
- `fear` - Scared or anxious (3.5%)
- `anger` - Angry or furious (1.9%)
- `sadness` - Depressed or hopeless (1.7%)

### 3. **Legal Risk Level** (`legal_risk_level`)
Assesses potential legal liability for compliance routing.
- `low` - Minimal legal concerns (86.5%)
- `medium` - Some legal considerations (12.8%)
- `high` - Significant legal risk requiring careful handling (0.7%)

### 4. **Topics** (`topics`)
Multi-label classification for content routing.
- `documentation` - Forms, paperwork, notices (52.7%)
- `payment` - Rent, fees, financial matters (43.5%)
- `maintenance` - Repairs, fixes, property issues (40.1%)
- `safety` - Security, danger, emergencies (37.8%)
- `health` - Medical, wellness concerns (23.4%)
- `policy` - Rules, lease terms, regulations (18.4%)
- `neighbor` - Inter-resident conflicts (6.6%)
- `general` - Uncategorized queries (11.5%)

### 5. **Complexity Score** (`complexity_score`)
1-10 scale measuring conversation difficulty for resource allocation.
- Considers message count, existing complexity level, and legal risk
- Most entries fall in 5-7 range (66.2%)
- Critical situations score 9-10 (12.9%)

### 6. **Language Features** (`language_features`)
Detailed linguistic analysis:
- `word_count` - Total words in conversation
- `avg_sentence_length` - Complexity indicator
- `question_count` - Number of questions asked
- `exclamation_count` - Emotional intensity marker
- `all_caps_words` - Shouting/emphasis detection
- `contains_profanity` - Flag for inappropriate language
- `multilingual` - Non-English text detection

### 7. **Response/Training Metrics**
Quality indicators based on user type:

**For Tenant Entries** (`response_metrics`):
- `response_count` - Number of AI responses
- `uses_tier_system` - Proper tier implementation
- `avg_response_length` - Response comprehensiveness
- `empathy_indicators` - Count of empathetic phrases
- `action_oriented` - Concrete help offered
- `sets_boundaries` - Appropriate limitations

**For Staff Entries** (`training_metrics`):
- `has_routing_logic` - Includes decision trees
- `has_training_objectives` - Clear learning goals
- `demonstrates_de_escalation` - Conflict resolution
- `shows_empowerment_language` - Choice-offering
- `includes_follow_up` - Commitment to check back

### 8. **Conversation Dynamics** (`conversation_dynamics`)
Flow pattern analysis:
- `pattern` - Type of conversation flow
  - `successful_de_escalation` - Anger/fear → neutral
  - `steady_state` - Consistent emotion throughout
  - `escalation` - Increasing tension
  - `variable` - Mixed emotional states
- `exchange_count` - Number of back-and-forth exchanges
- `emotion_trajectory` - Emotional progression array

### 9. **Cultural Sensitivity** (`cultural_sensitivity_needed`)
Flags cultural considerations:
- `present` - Boolean indicator (3.3% of entries)
- `markers` - Specific cultural elements detected:
  - `religious_references`
  - `family_structure_mentioned`
  - `dietary_needs`
  - `language_preference`
  - `cultural_holidays`

### 10. **Accessibility Considerations** (`accessibility_considerations`)
Identifies special needs:
- `present` - Boolean indicator (34.6% of entries)
- `types` - Specific accessibility needs:
  - `mobility` - Physical accessibility
  - `visual` - Sight-related accommodations
  - `hearing` - Audio/communication needs
  - `cognitive` - Understanding support
  - `communication` - Language barriers

## Additional Metadata
Each entry also includes:
- `tags_added_date` - When tags were generated
- `tags_version` - Tag schema version (currently 2.0)
- `content_hash` - Unique content identifier

## Usage Examples

### 1. Crisis Routing
```python
if entry["tags"]["urgency_level"] == "immediate":
    route_to_emergency_team()
elif entry["tags"]["legal_risk_level"] == "high":
    route_to_legal_specialist()
```

### 2. Empathy-Based Response
```python
emotion = entry["tags"]["primary_emotion"]
if emotion in ["fear", "sadness"]:
    use_extra_empathy_mode()
elif emotion == "anger":
    use_de_escalation_protocol()
```

### 3. Resource Allocation
```python
if entry["tags"]["complexity_score"] >= 8:
    assign_senior_specialist()
elif entry["tags"]["cultural_sensitivity_needed"]["present"]:
    assign_culturally_trained_agent()
```

### 4. Quality Assurance
```python
if entry["tags"]["response_metrics"]["empathy_indicators"] < 2:
    flag_for_empathy_training()
if not entry["tags"]["response_metrics"]["sets_boundaries"]:
    flag_for_boundary_training()
```

## Benefits

1. **Improved Routing** - Direct queries to appropriate specialists
2. **Better Training** - Identify gaps in staff capabilities
3. **Risk Management** - Flag high-risk situations early
4. **Cultural Competence** - Ensure appropriate cultural handling
5. **Accessibility** - Accommodate special needs properly
6. **Quality Control** - Monitor and improve response quality
7. **Analytics** - Deep insights into tenant needs and patterns
8. **Personalization** - Tailor responses to emotional states

## Future Enhancements

Additional tags that could be added:
- Seasonal patterns (heating in winter, AC in summer)
- Time-of-day urgency adjustments
- Historical interaction patterns
- Sentiment progression tracking
- Resolution success indicators
- Tenant satisfaction predictors