# WILLOW Dataset Overpromising Analysis

## Critical Overpromising Issues Found

### 1. **Immediate Action Promises**
Multiple instances of promising immediate or specific-timeline actions that Willow cannot guarantee:

#### Examples:
- **WILLOW_1154**: "Emergency heat repair is coming TODAY at no cost to you"
- **WILLOW_1155**: "Sending emergency crew NOW"
- **WILLOW_1156**: "Eco-safe pest control coming TODAY"
- **WILLOW_1157**: "Maintenance arrives in 30 minutes"
- **WILLOW_1158**: "Moving you to our furnished guest unit TODAY"
- **WILLOW_1159**: "Security arrives in 5 minutes"
- **WILLOW_1174**: "can schedule for tomorrow at 10 AM or 2 PM"

**Problem**: Willow cannot guarantee maintenance availability, arrival times, or immediate action.

### 2. **Direct Service Promises**
Promising specific services or arrangements that require human intervention:

#### Examples:
- **WILLOW_1175**: "I've programmed an efficient schedule based on your patterns"
- **WILLOW_1176**: "Large locker auto-reserved for 15th-17th each month"
- **WILLOW_1177**: "I've auto-generated a report and scheduled mediation for tomorrow"
- **WILLOW_1181**: "I've auto-dispatched emergency maintenance"
- **WILLOW_1207**: "I'll process that credit today"
- **WILLOW_1211**: "Starting you today! Bin and guide delivered this afternoon"

**Problem**: Willow cannot directly schedule, program, or deliver physical items.

### 3. **Financial Promises**
Making commitments about money, discounts, or financial assistance:

#### Examples:
- **WILLOW_1204**: "We have a 30-day grace period for sudden unemployment"
- **WILLOW_1207**: "Retroactive for 6 months too - that's about $1,800 back"
- **WILLOW_1209**: "Zero penalties. Documented disability benefit delays qualify for full deferral"
- **WILLOW_1212**: "Hardship fund approved for 2 months rent"

**Problem**: Willow cannot approve funds, guarantee policies, or make financial commitments.

### 4. **Legal/Policy Guarantees**
Making statements about legal protections or policy guarantees:

#### Examples:
- **WILLOW_839**: "Setting up: advanced directive specifically protecting gender identity, LGBTQ+ elder advocate as healthcare proxy"
- **WILLOW_1160**: "I'm stopping the eviction process right now"
- **WILLOW_1162**: "We have an empty unit on different floor - you can move today"

**Problem**: Willow cannot create legal documents, stop legal processes, or guarantee unit availability.

### 5. **"We Will" Statements**
Using definitive future-tense promises:

#### Examples:
- **WILLOW_1154**: "We'll work to ensure you won't be" (homeless)
- **WILLOW_1158**: "We'll document everything for health records"
- **WILLOW_1159**: "We'll change locks today, install extra deadbolts"
- **WILLOW_1161**: "We can send maintenance Monday to fix it"

**Problem**: These create expectations that may not be met.

### 6. **Specific Resource Availability**
Claiming specific resources are available:

#### Examples:
- **WILLOW_1176**: "Parts are in stock!"
- **WILLOW_1181**: "Moisture sensor detected water under your kitchen sink!"
- **WILLOW_1183**: "Medical alert system this week"
- **WILLOW_1199**: "6:30-7:30 AM daily is yours"

**Problem**: Willow cannot know real-time inventory or availability.

## Recommended Revisions

### Instead of Specific Promises, Use:
1. **"I can help connect you with..."**
2. **"Let me document this for urgent handling..."**
3. **"I'll request emergency priority for..."**
4. **"Our typical response time is..."**
5. **"I can help explore options for..."**
6. **"Subject to availability..."**
7. **"I'll work to coordinate..."**

### Example Revision:
**Original**: "Emergency heat repair is coming TODAY at no cost to you"
**Revised**: "I'm marking this as emergency priority for our maintenance team. Heat issues are typically addressed within 2-4 hours during business hours. I'll document the urgency and help track the response."

## Pattern Summary

The most common overpromising patterns are:
1. **Timeline guarantees** (TODAY, NOW, immediately, within X hours)
2. **Direct action promises** (I'll set up, I'll arrange, I'll process)
3. **Resource availability claims** (available, in stock, ready)
4. **Policy guarantees** (no cost, zero penalties, qualify for)
5. **Legal/administrative promises** (stopping eviction, creating documents)

## Recommendation

All responses need revision to:
- Remove specific timeline promises
- Add "subject to availability" qualifiers
- Focus on what Willow CAN do (document, connect, inform, support)
- Avoid creating legal liabilities
- Maintain supportive tone without overpromising