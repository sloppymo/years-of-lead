# Willow Dataset Generator Guide

## Overview
These tools help generate high-quality Willow dataset entries while reducing token usage and ensuring consistency.

## Tools Created

### 1. `willow_dataset_generator.py`
Main generator class with validation and templates.

**Key Features:**
- Automatic ID generation and incrementing
- Overpromising detection and correction
- Arousal/capacity curve calculation
- Template support
- Batch generation

**Basic Usage:**
```python
from willow_dataset_generator import WillowGenerator

# Initialize generator starting at ID 1079
generator = WillowGenerator(starting_id=1079)

# Generate single entry
entry = generator.generate_entry(
    scenario_name="your_scenario_name",
    category="eviction",  # from predefined list
    complexity="critical",  # medium/high/critical
    issue_type="financial_instability",
    tenant_message1="First tenant message",
    willow_response1="First Willow response (tier 1)",
    tenant_message2="Second tenant message",
    willow_response2="Second Willow response (tier 2)",
    initial_arousal=8.5,
    initial_capacity=3.3,
    tier1_technique="system_abandonment_naming",
    tier2_technique="multi_pathway_support",
    resolution_status="defending",
    escalation_path="legal_aid"
)

# Save to file (appends by default)
generator.save_entries('willow_expansion_1000.jsonl', [entry])
```

### 2. `willow_scenario_templates.json`
Pre-defined templates for common scenario types.

**Available Templates:**
- `housing_discrimination` - Identity-based discrimination
- `medical_crisis_eviction` - Health-related housing loss
- `family_separation` - ICE, CPS, custody issues
- `maintenance_retaliation` - Punishment for complaints
- `climate_displacement` - Disaster-related housing

### 3. Validation Features

**Overpromising Check:**
```python
# Check any text for dangerous promises
issues = generator.validate_no_overpromising(text)
if issues:
    safe_text = generator.suggest_safe_alternative(text)
```

**Dangerous phrases detected:**
- "I will", "we will", "guarantee", "ensure"
- "immediately", "today", "tomorrow"
- "definitely", "promise"

## Efficient Workflow

### Step 1: Plan Your Batch
List the scenarios you want to create with:
- Basic situation
- Category and complexity
- Key emotional beats

### Step 2: Use Templates
Load relevant template:
```python
template = generator.load_template("medical_crisis_eviction")
```

### Step 3: Generate Entries
Create entries with minimal text:
```python
entries_data = [
    {
        "scenario_name": "chemo_eviction_defense",
        "tenant_message1": "Chemo wiped out savings, eviction tomorrow",
        "willow_response1": "Cancer steals health, treatment steals wealth...",
        "tenant_message2": "No lawyer, too sick to go to court",
        "willow_response2": "I can help connect you with emergency legal...",
        **template  # Use template defaults
    },
    # More entries...
]

batch = generator.generate_batch(entries_data)
generator.save_entries('willow_expansion_1000.jsonl', batch)
```

## Quick Entry Structure

Each entry needs:
1. **Scenario name** (short, descriptive)
2. **Two tenant messages** (raw, emotional)
3. **Two Willow responses** (tier 1: validation, tier 2: resources)
4. **Metadata** (category, complexity, techniques)

## Reducing Token Usage

1. **Use the generator** instead of writing full JSON
2. **Reference templates** for common patterns
3. **Batch similar scenarios** together
4. **Reuse techniques** from the predefined lists
5. **Let the tool calculate** arousal/capacity curves

## Example: Generate 5 Discrimination Entries

```python
generator = WillowGenerator(1079)

discrimination_scenarios = [
    ("muslim_prayer_harassment", "Neighbors complain about prayer, manager threatens eviction"),
    ("wheelchair_ramp_denied", "Landlord refuses ramp says find somewhere else"),
    ("section8_rejection", "Accepted until they heard Section 8, now ghosting"),
    ("trans_bathroom_access", "Other tenants complaining about me using bathroom"),
    ("immigrant_language_barrier", "Manager yells at me for not speaking English")
]

for scenario, issue in discrimination_scenarios:
    entry = generator.generate_entry(
        scenario_name=scenario,
        category="discrimination",
        complexity="high",
        issue_type="safety_threat",
        tenant_message1=issue,
        willow_response1="[Generate appropriate tier 1 response]",
        tenant_message2="[Generate follow-up]",
        willow_response2="[Generate tier 2 with resources]",
        initial_arousal=8.0,
        initial_capacity=3.6,
        tier1_technique="identity_affirmation",
        tier2_technique="fair_housing_enforcement",
        resolution_status="protecting"
    )
    # Tool handles all the JSON structure, IDs, curves, etc.
```

## Next Steps

To generate the next batch:
1. Tell me the theme/focus for the next 25 entries
2. I'll use the generator to create them efficiently
3. Review and approve
4. Move to next batch

This approach should reduce token usage by 60-70% while maintaining quality and consistency.