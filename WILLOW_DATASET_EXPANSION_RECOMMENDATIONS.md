# WILLOW Dataset Expansion Recommendations

## Executive Summary

After analyzing the 1,233 entries in the WILLOW corpus, I've identified several areas where additional scenarios would strengthen the AI's ability to handle complex tenant situations with empathy, legal safety, and practical effectiveness.

## 1. **Intersectional Identity Scenarios**

### Current Gap
Limited representation of scenarios where multiple marginalized identities intersect (e.g., LGBTQ+ seniors, disabled immigrants, neurodivergent parents).

### Recommended Additions
- Trans tenant needing safety during transition
- Elderly immigrant with language barriers and health issues  
- Autistic parent navigating noise complaints about their child
- Formerly incarcerated person rebuilding life
- Indigenous tenant maintaining cultural practices

### Example Scenario Structure
```json
{
  "id": "WILLOW_1234",
  "scenario": "trans_safety_transition",
  "messages": [
    {
      "role": "tenant",
      "content": "Starting transition, worried about neighbor reactions"
    },
    {
      "role": "willow",
      "content": "Your safety during this important time is our priority. Let's create a support plan: updated name on all building systems, discrete mail handling, and I'll ensure staff use correct pronouns. You deserve to live authentically here."
    }
  ]
}
```

## 2. **Climate/Disaster Response Scenarios**

### Current Gap
Limited coverage of climate emergencies and natural disasters affecting housing.

### Recommended Additions
- Wildfire evacuation and return protocols
- Extreme heat wave with power grid failures
- Flood damage and displacement support
- Hurricane preparation for building community
- Earthquake damage assessment and support

### Key Elements
- Trauma-informed disaster response
- Community mutual aid coordination
- Insurance navigation support
- Temporary housing arrangements
- Promise-free recovery timelines

## 3. **Technology Accessibility Scenarios**

### Current Gap
Insufficient coverage of digital divide issues affecting vulnerable tenants.

### Recommended Additions
- Senior struggling with digital rent payment
- Low-income family needing internet for school
- Blind tenant navigating app-based building systems
- Tenant without smartphone needing building access
- Digital privacy concerns with smart building features

## 4. **Complex Legal Situations**

### Current Gap
Need more nuanced legal scenarios beyond basic eviction prevention.

### Recommended Additions
- Tenant with restraining order needing security protocols
- Undocumented tenant fearful of ICE raids
- Custody disputes affecting housing stability
- Tenant witnessing crimes needing protection
- Fair housing accommodation disputes

### Critical Elements
- Non-promissory legal information
- Resource connections without guarantees
- Trauma-informed legal crisis support
- Privacy and safety prioritization

## 5. **Collective Tenant Scenarios**

### Current Gap
Most scenarios focus on individual tenants rather than collective issues.

### Recommended Additions
- Tenants organizing for building improvements
- Group complaint about management company
- Building-wide pest infestation response
- Collective bargaining for rent stabilization
- Community response to hate incidents

## 6. **Youth-Specific Scenarios**

### Current Gap
Limited coverage of young adult tenants with unique challenges.

### Recommended Additions
- First-time renter anxiety and questions
- College student struggling with roommates
- Young person aging out of foster care
- Teen parent needing support systems
- Young adult escaping family abuse

## 7. **End-of-Life and Grief Scenarios**

### Current Gap
Insufficient coverage of death, dying, and grief in housing context.

### Recommended Additions
- Tenant with terminal diagnosis needing modifications
- Family member died in unit, next steps
- Hospice care accommodation needs
- Grief support after community member loss
- Estate clearance with sensitivity

## 8. **Substance Use Complexity**

### Current Gap
Need more nuanced substance use scenarios beyond basic recovery.

### Recommended Additions
- Harm reduction support requests
- Medical marijuana accommodation needs
- Overdose prevention site concerns
- Recovery house transition support
- Family affected by tenant's substance use

## 9. **Economic Complexity Scenarios**

### Current Gap
Need scenarios reflecting modern economic challenges.

### Recommended Additions
- Cryptocurrency income verification issues
- Gig economy workers with irregular income
- Student loan forgiveness impact on rent
- Inflation affecting fixed-income seniors
- Remote work visa complications

## 10. **Cultural Celebration Scenarios**

### Current Gap
More positive cultural scenarios needed beyond problem-solving.

### Recommended Additions
- Organizing building Iftar dinner
- Day of the Dead altar in common space
- Diwali decoration collaboration
- Pride month building activities
- Indigenous ceremony space needs

## Implementation Recommendations

### 1. **Scenario Development Process**
- Consult with affected communities for authenticity
- Review with legal team for liability protection
- Test with trauma-informed care specialists
- Validate cultural sensitivity with community leaders

### 2. **Quality Metrics to Maintain**
- Promise-free language throughout
- Tier 1 always focuses on emotional containment
- Concrete resources without guarantees
- Cultural humility and learning stance
- Community-building opportunities where appropriate

### 3. **Training Data Balance**
- Aim for 100-150 scenarios per category
- Ensure complexity levels are distributed evenly
- Include positive/celebratory scenarios (20% minimum)
- Balance individual vs. collective scenarios
- Represent diverse geographic and cultural contexts

### 4. **Continuous Improvement**
- Regular review of emerging housing challenges
- Feedback loops from deployment experiences
- Annual bias and sensitivity audits
- Community advisory board input
- Ongoing legal compliance reviews

## Conclusion

These expansions would create a more comprehensive, intersectional, and legally sound dataset that better serves all tenants while protecting property management from liability. The additions emphasize human dignity, practical support, and community resilience while maintaining the careful balance of empathy without promises that makes WILLOW effective.