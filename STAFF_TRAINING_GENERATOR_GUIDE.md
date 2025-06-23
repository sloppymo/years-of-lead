# WILLOW Staff Training Corpus Generator Guide

## Overview

Two Python scripts have been created to efficiently generate the 1,090 staff training entries needed for the WILLOW corpus:

1. **`generate_staff_training_corpus.py`** - Basic generator with comprehensive scenarios
2. **`generate_staff_training_advanced.py`** - Advanced generator with quality controls and customization

## Basic Generator Features

### Key Capabilities:
- Generates 1,090 entries automatically distributed across 21 categories
- Proper complexity distribution (15% low, 45% medium, 35% high, 5% critical)
- Realistic message exchanges with tier progression
- Diverse resident personas and staff roles
- Built-in scenario templates for each category

### Categories Covered:
- **Crisis & Emergency (25%)**: Crisis intervention, emergency response, de-escalation
- **Legal & Compliance (20%)**: Fair housing, discrimination prevention, documentation
- **Mental Health (15%)**: Trauma-informed care, substance abuse response
- **Communication (15%)**: Difficult conversations, conflict resolution
- **Operations (15%)**: Maintenance coordination, vendor management
- **Administrative (10%)**: Policy enforcement, team coordination

### Usage:
```bash
python3 generate_staff_training_corpus.py
```

Output: `willow_staff_training_corpus_[timestamp].jsonl`

## Advanced Generator Features

### Enhanced Capabilities:
- Quality scoring system (0-100) for each entry
- Legal safety checks to avoid problematic language
- Customizable category weights and complexity distribution
- Batch processing with progress tracking
- Metadata inclusion for review prioritization
- Edge case scenario generation
- Multiple output formats (JSONL or JSON)

### Quality Controls:
- Avoids problematic phrases ("calm down", "just", "obviously")
- Ensures professional language markers
- Checks for legal safety (no promises, admissions, threats)
- Validates tier progression logic
- Scores entries on multiple quality dimensions

### Command Line Options:
```bash
# Basic usage
python3 generate_staff_training_advanced.py

# Custom number of entries
python3 generate_staff_training_advanced.py --entries 500

# With quality filtering
python3 generate_staff_training_advanced.py --quality-threshold 80

# Include metadata and edge cases
python3 generate_staff_training_advanced.py --include-metadata --edge-cases

# Custom output format
python3 generate_staff_training_advanced.py --format json --output my_corpus.json

# Custom batch size
python3 generate_staff_training_advanced.py --batch-size 50
```

### Arguments:
- `--entries`: Number of entries to generate (default: 1090)
- `--batch-size`: Batch size for generation (default: 100)
- `--output`: Custom output filename
- `--format`: Output format - "jsonl" or "json" (default: jsonl)
- `--include-metadata`: Include generation metadata in entries
- `--edge-cases`: Include edge case scenarios
- `--quality-threshold`: Minimum quality score (0-100) for entries

## Generated Entry Structure

Each entry contains:
```json
{
  "id": "WILLOW_STAFF_0111",
  "scenario": "crisis_intervention_high_111",
  "scenario_description": "Elderly resident hasn't been seen for days...",
  "user_type": "staff",
  "category": "crisis_intervention",
  "category_group": "crisis_emergency",
  "complexity_level": "high",
  "initial_state": {
    "arousal": 7.5,
    "capacity": 4.5,
    "urgency": 7.0,
    "time_sensitivity": "urgent",
    "vulnerability_factor": "age"
  },
  "messages": [
    {
      "role": "resident",
      "content": "HELP ME NOW! My neighbor hasn't answered..."
    },
    {
      "role": "staff",
      "content": "I can hear how worried you are...",
      "tier": "tier_1",
      "techniques": ["active_listening", "emotional_validation"]
    }
  ],
  "routing_logic": {
    "primary_indicators": ["immediate_danger", "elderly_welfare"],
    "escalation_triggers": ["unresponsive_resident", "safety_concern"],
    "de_escalation_signs": ["information_gathered", "help_accepted"],
    "resolution_criteria": ["welfare_check_initiated", "emergency_contacted"]
  },
  "training_objectives": [
    "Recognize crisis indicators",
    "Maintain personal safety",
    "Coordinate emergency response",
    "Document for liability"
  ],
  "quality_metrics": {
    "overall_score": 85.5,
    "tier_coverage": ["tier_1", "tier_2"],
    "legal_safety": true,
    "professionalism_score": 12
  },
  "legal_risk_level": "high",
  "staff_role": "property_manager"
}
```

## Customization Tips

### 1. Modify Category Distribution
Edit the `category_weights` in `GenerationConfig`:
```python
config = GenerationConfig(
    category_weights={
        "crisis_emergency": 0.30,  # Increase crisis scenarios
        "legal_compliance": 0.25,  # More legal training
        "mental_health": 0.20,
        "communication": 0.10,
        "operations": 0.10,
        "administrative": 0.05
    }
)
```

### 2. Adjust Complexity Distribution
```python
config = GenerationConfig(
    complexity_distribution={
        "low": 0.10,      # Fewer simple scenarios
        "medium": 0.40,   # Balanced middle
        "high": 0.40,     # More challenging scenarios
        "critical": 0.10  # More crisis scenarios
    }
)
```

### 3. Add Custom Scenarios
Edit the `scenario_bank` in either generator to add specific situations your staff face.

### 4. Modify Quality Patterns
Update `quality_patterns` to enforce your organization's communication standards.

## Integration Workflow

1. **Generate Initial Corpus**:
   ```bash
   python3 generate_staff_training_corpus.py
   ```

2. **Review and Filter**:
   ```bash
   python3 generate_staff_training_advanced.py --quality-threshold 75
   ```

3. **Merge with Existing Entries**:
   - Combine with the 110 existing staff entries
   - Remove any duplicates
   - Ensure ID continuity

4. **Validate Final Dataset**:
   - Check tier distribution
   - Verify category balance
   - Review high-risk scenarios
   - Test with sample staff

## Quality Assurance Checklist

- [ ] All entries have proper `user_type: "staff"` field
- [ ] Tier progression follows trauma-informed principles
- [ ] No problematic language or promises
- [ ] Legal risk scenarios properly marked
- [ ] Training objectives align with category
- [ ] Realistic dialogue flow
- [ ] Appropriate complexity distribution
- [ ] Edge cases included for comprehensive training

## Performance Notes

- Basic generator: ~30-60 seconds for 1,090 entries
- Advanced generator: ~60-120 seconds with quality checks
- Memory usage: ~100-200MB for full corpus
- Output file size: ~5-10MB for 1,090 entries

## Next Steps

After generation:
1. Review a sample of generated entries for quality
2. Run through legal/compliance review for high-risk categories
3. Test with actual staff trainers for feedback
4. Integrate into main WILLOW corpus
5. Create training modules around the scenarios

The generators provide a solid foundation that can be refined based on your specific organizational needs and feedback from pilot testing.