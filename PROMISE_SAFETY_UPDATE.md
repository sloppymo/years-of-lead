# WILLOW Corpus - Promise Safety Update

## Critical Safety Issue Resolved

**Date**: 2025-06-24  
**Issue**: Corpus contained dangerous promises about external service ETAs  
**Resolution**: All concrete time promises for services we don't control have been removed

## What Was Fixed

### ❌ REMOVED - Dangerous Promises
- "Police ETA: 3-5 minutes"
- "Paramedics arriving in 6 minutes"  
- "Fire department ETA: 4 minutes"
- "Emergency services arriving in 5-7 minutes"
- "Ambulance ETA: 8 minutes"
- "Gas company ETA: 7 minutes"
- Any specific arrival times for external services

### ✅ REPLACED WITH - Safe Language
- "Police have been notified"
- "Emergency medical services have been called"
- "Fire department has been notified"
- "Emergency services have been contacted"
- "on their way" / "as quickly as possible"
- Focus on actions taken, not arrival times

### ✅ KEPT - Internal Service Promises Only
- "Building security arriving in 30 seconds"
- "Our emergency team will be there in 2 minutes"
- "Building staff arriving in 90 seconds"
- Services we directly control and can guarantee

## Files Updated

1. **willow_expansion_final_excellence_20250624_010121.jsonl**
   - 59 entries modified
   - Safe version: `willow_expansion_final_excellence_20250624_010121_safe_20250624_011659.jsonl`

2. **willow_corpus_complete_final.jsonl**
   - Already safe (0 modifications needed)
   - Safe version: `willow_corpus_complete_final_safe_20250624_011659.jsonl`

## Legal Protection Achieved

This update ensures:
1. **No liability** for external service response times
2. **No false expectations** about arrival times we can't control
3. **Focus on actions** we ARE taking (notifying, dispatching, coordinating)
4. **Only promise times** for our own staff/services
5. **Legal protection** from claims about delayed external services
6. **Maintained empathy** while being legally responsible

## Key Principle

**NEVER promise specific ETAs for services we don't control:**
- Police, Fire, Paramedics, Ambulance
- Utility companies (gas, electric, water)  
- Any third-party emergency services

**ONLY promise times for services we control:**
- Building security
- Building staff
- Our emergency response teams
- Our maintenance teams

## Implementation Going Forward

All future corpus entries must follow this principle. When dealing with emergencies:
1. Focus on what actions we're taking
2. Avoid specific arrival times for external services
3. Use phrases like "on their way" or "have been notified"
4. Only give ETAs for our own staff/services
5. Maintain urgency without creating liability