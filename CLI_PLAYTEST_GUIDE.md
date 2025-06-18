# Years of Lead - Interactive CLI Playtest Guide

## 🎯 Testing Mission Failures & Cascading Effects

This guide will walk you through a systematic CLI playthrough to test and observe:
- Mission failure scenarios and their consequences
- Emotional impact on agents from failed missions
- Relationship changes between agents
- Cascading effects across the resistance network
- Dynamic narrative generation from failures

---

## 🚀 Getting Started

### 1. Launch the Game
```bash
python main.py --mode cli
```

### 2. Initial Setup
The game will start with sample agents and factions. Note the initial status:
- Agent emotional states
- Faction resources
- Network stress levels

---

## 📋 Phase 1: Baseline Assessment

### Step 1: Check Agent Status
```
Command: [2] agents
```
**What to observe:**
- Initial stress levels of all agents
- Emotional states (if available)
- Skills and backgrounds
- Current locations

**Take notes on:**
- Which agents have high stress (>70)
- Any agents with trauma indicators
- Skill levels for mission planning

### Step 2: Review Faction Resources
```
Main menu will show faction resources
```
**Initial baselines:**
- The Resistance: $150, Influence: 30, Personnel: 8
- Student Movement: $50, Influence: 70, Personnel: 15  
- Workers Union: $200, Influence: 40, Personnel: 12

---

## 🎯 Phase 2: Mission Failure Testing

### Test Mission 1: High-Risk Sabotage Mission

#### Create the Mission
```
Command: [8] createmission
```
**Mission Setup:**
- Type: Sabotage
- Target: Government facility
- Difficulty: High
- Description: "Plant explosives in communications center"

#### Assign Stressed Agents
```
Command: [9] addtomission
```
**Strategy for testing failure:**
- Assign agents with highest stress levels
- Use agents with trauma indicators
- Choose agents with lower relevant skills

#### Execute and Observe
```
Command: [10] execmission
```

**Key Observations to Make:**
1. **Mission Outcome:** Note the specific failure type
2. **Immediate Consequences:** Resource losses, agent status changes
3. **Emotional Impact:** How agents' psychological states change
4. **Narrative Generation:** The story created from the failure

---

### Test Mission 2: Cascade Effect Mission

#### Wait for Effects to Propagate
```
Command: [1] advance (advance turn)
```
**Observe changes:**
- Agent stress levels after mission failure
- Faction resource impacts
- Any new events triggered

#### Create Follow-up Mission
```
Command: [8] createmission
```
**Mission Setup:**
- Type: Rescue (to save failed agents)
- Use remaining traumatized agents
- Higher difficulty due to increased security

#### Execute and Document Cascading Effects
```
Command: [10] execmission
```

**Critical Observations:**
1. How the first failure affects the second mission
2. Compounding stress on agents
3. Resource depletion cascade
4. Network-wide morale impact

---

## 🧠 Phase 3: Psychological Impact Analysis

### Deep Dive into Agent Psychology
```
Command: [2] agents
```

For each agent, document:

#### Emotional State Changes
- **Pre-mission emotions**
- **Post-mission emotions** 
- **Trauma accumulation**
- **Effectiveness reduction**

#### Stress Progression
- **Initial stress levels**
- **Post-mission stress**
- **Compound stress from multiple failures**
- **Breaking points (stress >90)**

#### Behavioral Changes
- **Decision-making impairment**
- **Mission effectiveness reduction**
- **Relationship strain indicators**

---

## 🌊 Phase 4: Cascading Effects Documentation

### Network-Wide Impact Assessment

#### Advance Multiple Turns
```
Command: [1] advance (repeat 3-5 times)
```

**Track progression of:**
1. **Faction Resource Depletion**
   - Money reduction from failed missions
   - Influence loss from public failures
   - Personnel losses from captures

2. **Operational Capability Degradation**
   - Reduced mission success rates
   - Increased mission difficulty
   - Agent availability reduction

3. **Morale and Loyalty Erosion**
   - Faction loyalty changes
   - Inter-agent relationship strain
   - Recruitment difficulty increases

#### Test Recovery Scenarios
```
Commands: [4] addtask, [8] createmission
```

**Create low-risk missions to test:**
- Can the network recover from failures?
- How long does trauma persist?
- What breaks the failure cascade?

---

## 📊 Data Collection Template

### Mission Execution Log

| Mission # | Type | Agents Used | Pre-Stress Avg | Outcome | Post-Stress Avg | Consequences |
|-----------|------|-------------|----------------|---------|-----------------|--------------|
| 1 | Sabotage | Agent A, B | 45% | Catastrophic Failure | 78% | 2 agents captured, $50 lost |
| 2 | Rescue | Agent C | 78% | Complete Failure | 95% | Agent C captured, morale -20 |

### Emotional Impact Tracking

| Agent | Pre-Mission Fear | Post-Mission Fear | Trauma Level | Effectiveness |
|-------|------------------|-------------------|--------------|---------------|
| Agent A | 0.2 | 0.8 | 0.6 | Severely Reduced |
| Agent B | 0.3 | 0.7 | 0.4 | Moderately Reduced |

### Cascade Effect Timeline

| Turn | Event | Network Stress | Resources Lost | Narrative Impact |
|------|-------|----------------|----------------|------------------|
| 1 | Mission 1 Fails | Low → High | $50, 2 agents | "Operation blown" |
| 2 | Security Crackdown | High → Critical | Safe house compromised | "Network under siege" |
| 3 | Rescue Attempt Fails | Critical | 1 more agent | "Desperation sets in" |

---

## 🎭 Advanced Testing Scenarios

### Scenario A: Complete Network Collapse
1. Execute 3-4 high-risk missions consecutively
2. Use traumatized agents for each mission
3. Document the point of network breakdown
4. Observe narrative evolution

### Scenario B: Recovery from Disaster
1. Create catastrophic failure scenario
2. Switch to only low-risk missions
3. Test trauma recovery over time
4. Document resilience mechanisms

### Scenario C: Emotional Contagion Testing
1. Have one highly traumatized agent
2. Assign them to missions with stable agents
3. Observe trauma spreading through relationships
4. Document relationship degradation

---

## 🔍 Key Metrics to Track

### Mission-Level Metrics
- **Success Rate Degradation:** How failures reduce future success
- **Compound Difficulty:** How security increases after failures
- **Resource Burn Rate:** Acceleration of resource consumption

### Agent-Level Metrics  
- **Stress Accumulation Rate:** How quickly agents break down
- **Trauma Persistence:** How long psychological damage lasts
- **Effectiveness Correlation:** Relationship between trauma and performance

### Network-Level Metrics
- **Cascade Amplification:** How failures multiply across the network
- **Recovery Time:** How long it takes to stabilize after disasters
- **Breaking Point:** The threshold where the network collapses

---

## 📖 Narrative Analysis Framework

### Document Narrative Evolution
Track how the story changes with failures:

1. **Initial Tone:** Hope, determination, optimism
2. **First Failure:** Setback, concern, regrouping
3. **Cascade Begins:** Desperation, fear, questioning
4. **Network Stress:** Paranoia, mistrust, survival focus
5. **Breaking Point:** Collapse, retreat, or radical change

### Key Narrative Moments
- First agent capture
- First mission catastrophic failure
- First agent psychological breakdown
- Network security compromise
- Leadership crisis emergence

---

## 🎯 Testing Checklist

### Pre-Playtest Setup
- [ ] Note initial agent emotional states
- [ ] Record baseline faction resources
- [ ] Document network stress levels
- [ ] Prepare data tracking spreadsheet

### During Missions
- [ ] Screenshot/record mission outcome screens
- [ ] Note exact emotional impact numbers
- [ ] Track resource changes
- [ ] Document narrative text generation

### Between Missions
- [ ] Advance turns to see delayed effects
- [ ] Check for new events triggered
- [ ] Monitor agent relationship changes
- [ ] Assess faction standing

### Post-Playtest Analysis
- [ ] Calculate failure cascade statistics
- [ ] Analyze narrative coherence
- [ ] Identify breaking points
- [ ] Document recovery mechanisms

---

## 🚀 Running the Full Test

### Quick Start Commands:
```bash
# Launch game
python main.py --mode cli

# Essential command sequence for failure testing:
# [2] → Check agent status
# [8] → Create high-risk mission  
# [9] → Assign stressed agents
# [10] → Execute mission
# [1] → Advance turn
# [2] → Check emotional impact
# Repeat cycle with increasingly traumatized agents
```

### Expected Timeline:
- **Phase 1 (Baseline):** 10-15 minutes
- **Phase 2 (Mission Testing):** 20-30 minutes  
- **Phase 3 (Psychology Analysis):** 15-20 minutes
- **Phase 4 (Cascade Documentation):** 15-25 minutes
- **Total:** 60-90 minutes for comprehensive test

---

This systematic approach will give you deep insights into how your simulation handles failure scenarios and creates meaningful narrative consequences from those failures. 