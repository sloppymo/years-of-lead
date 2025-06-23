# Willow Emergency Escalation Framework

## Challenge: Determining When Human Intervention is Required

Based on analysis of the Willow corpus, here's a framework for identifying situations that require immediate human attention:

## Tier 1: Immediate Life/Safety Threats (Escalate Within 1-2 Minutes)

### Medical Emergencies
- **Keywords**: "can't breathe", "chest pain", "bleeding", "unconscious", "overdose", "seizure"
- **Scenarios**: Oxygen equipment failure, dialysis needs, pregnancy complications
- **Arousal**: Typically 8.5+ 
- **Example**: "My mom's oxygen machine stopped working"

### Active Violence/Threats
- **Keywords**: "threatening me", "hitting", "weapon", "going to hurt"
- **Scenarios**: Domestic violence, neighbor threats, stalking
- **Arousal**: Usually 8.0+
- **Example**: "My ex is at the door threatening me"

### Suicidal/Self-Harm Risk
- **Keywords**: "want to die", "end it all", "not worth living", "goodbye"
- **Arousal**: Can be high (8+) OR dangerously low (2-3)
- **Capacity**: Often very low (<3.0)
- **Example**: "I can't do this anymore, goodbye"

### Child/Elder Safety
- **Keywords**: "baby", "child", "elderly parent" + any danger word
- **Scenarios**: Children in dangerous conditions, elder abuse
- **Example**: "Baby has fever and there's no heat"

## Tier 2: Urgent Safety/Legal Issues (Escalate Within 15-30 Minutes)

### Imminent Homelessness
- **Keywords**: "eviction tomorrow", "locked out", "sheriff coming"
- **Arousal**: 8.0+
- **Timeline**: <48 hours
- **Example**: "Court is tomorrow and I just found out"

### Major Habitability Violations
- **Keywords**: "no water", "no heat", "gas leak", "electrical sparking", "ceiling falling"
- **Duration**: >24 hours for essential services
- **Example**: "No heat for 3 days with sick children"

### Severe Mental Health Crisis
- **Arousal**: Sustained >8.0 for multiple exchanges
- **Capacity**: Consistently <3.0
- **Pattern**: Not responding to de-escalation techniques
- **Example**: Incoherent responses, extreme paranoia

## Tier 3: Complex Legal/Discrimination (Escalate Within 2-4 Hours)

### Clear Discrimination
- **Keywords**: "because I'm [protected class]", "won't rent to [group]"
- **Pattern**: Systematic targeting
- **Example**: "Manager said no Muslims allowed"

### Illegal Retaliation
- **Keywords**: "reported", "now evicting", "after I complained"
- **Pattern**: Adverse action after protected activity
- **Example**: "Filed health complaint, now getting evicted"

## Escalation Triggers

### Quantitative Metrics
1. **Arousal consistently >8.5** after 3 exchanges
2. **Capacity <2.5** with no improvement
3. **Multiple life safety keywords** in single message
4. **Explicit threats** of violence or self-harm

### Qualitative Patterns
1. **Dissociation/Incoherence**: "..." responses, word salad
2. **Escalating Despite Intervention**: Getting worse not better
3. **Multiple Crisis Factors**: Pregnancy + homelessness + violence
4. **Time-Sensitive**: "Tomorrow", "Tonight", "Right now"

### Special Populations
- **Pregnant tenants**: Lower threshold for medical concerns
- **Elderly (75+)**: Faster escalation for health issues
- **Disabled tenants**: Consider capacity limitations
- **Children involved**: Always err on side of caution

## De-escalation Attempt Requirements

Before escalating, Willow should:
1. **One grounding attempt** (breathing, feet on floor)
2. **One validation** of their experience
3. **One concrete help offer**

**EXCEPT** when:
- Active violence is occurring
- Medical emergency stated
- Suicide/self-harm expressed
- Child/elder in immediate danger

## Escalation Process

### Information to Capture
1. **Tenant ID/Unit**: For immediate location
2. **Issue Category**: Medical/Safety/Legal/Mental Health
3. **Urgency Level**: Immediate/Urgent/Soon
4. **Key Details**: In 1-2 sentences
5. **Arousal/Capacity**: Current levels
6. **Attempts Made**: What Willow tried

### Handoff Message Template
```
HUMAN NEEDED - [URGENCY]
Tenant: [ID/Unit]
Issue: [Brief description]
Risk: [Specific concern]
State: Arousal [X], Capacity [Y]
Tried: [What didn't work]
```

## False Positive Prevention

### Don't Escalate Just For:
- High emotion alone (if capacity >4)
- Past trauma mentions (unless activated)
- Angry language (if coherent)
- Legal threats (unless discrimination)
- Maintenance delays (unless habitability)

### Do Escalate For:
- Any combination of 2+ Tier 1 factors
- Sustained crisis despite intervention
- Explicit requests for human help
- Liability-creating situations

## Quality Metrics

Track:
- **False positive rate**: Target <10%
- **False negative rate**: Target <1% 
- **Average escalation time**: By tier
- **Human override rate**: When agents disagree

## Implementation Notes

1. **Err on side of caution**: Better false positive than missed crisis
2. **Cultural sensitivity**: Some cultures express distress differently
3. **Time of day matters**: Night/weekend = lower threshold
4. **Previous history**: Known mental health issues = faster escalation
5. **Liability awareness**: Some situations require human for legal protection

This framework should be regularly updated based on:
- Actual crisis outcomes
- Human responder feedback
- Legal/regulatory changes
- Emerging patterns in data