# WILLOW Corpus - Promise Safety Update

## Critical Safety Issue Resolved

**Date**: 2025-06-24  
**Issue**: Corpus contained dangerous promises about external service ETAs  
**Resolution**: Comprehensive removal of concrete time promises for services we don't control

## Comprehensive Cleanup Results

### Total Impact
- **Files Scanned**: 79+ JSONL files  
- **Dangerous Promises Found**: 235+ instances
- **Files Modified**: Multiple corpus files
- **Largest Corpus Processed**: 2,375 entries

### Key Files Processed
1. `willow_corpus_complete_final_20250624_000624.jsonl` - 2,375 entries (2 promises removed)
2. `willow_corpus_complete_final.jsonl` - 1,053 entries (2 promises removed)
3. `willow_expansion_excellence_20250624_005925.jsonl` - 98 promises removed
4. `willow_expansion_final_excellence_20250624_010121.jsonl` - 98 promises removed  
5. `willow_expansion_phase1_20250624_003259.jsonl` - 35 promises removed

## What Was Fixed

### ❌ REMOVED - Dangerous Promises
- "Police ETA: 3-5 minutes"
- "Paramedics arriving in 6 minutes"  
- "Fire department ETA: 4 minutes"
- "Emergency services arriving in 5-7 minutes"
- "Ambulance ETA: 8 minutes"
- "Gas company ETA: 7 minutes"
- "Elevator emergency rescue ETA: 10 minutes"
- "Stroke team alerted - ETA 5 minutes"
- "Water shut-off crew arriving in 15 minutes"
- Any specific arrival times for external services

### ✅ REPLACED WITH - Safe Language
- "Police have been notified"
- "Emergency medical services have been called"
- "Fire department has been notified"
- "Emergency services have been contacted"
- "on their way" / "as quickly as possible"
- Focus on actions taken, not arrival times

### ⚠️ NOTE: Internal Service Promises
Some entries still contain ETAs for internal services (e.g., "Maintenance supervisor en route with master override (ETA 10-15 minutes)"). While these are for services we control, consider whether even these should be more general to avoid any liability.

## Final Safe Corpus Files

Multiple safe versions created:
- `willow_corpus_complete_final_20250624_000624_final_safe_20250624_014339.jsonl` (2,375 entries)
- `willow_corpus_complete_final_final_safe_20250624_014339.jsonl` (1,053 entries)
- Various expansion files with "_safe_" in filename

## Legal Protection Achieved

This comprehensive update ensures:
1. **Reduced liability** for external service response times
2. **No false expectations** about arrival times we can't control
3. **Focus on actions** we ARE taking (notifying, dispatching, coordinating)
4. **Legal protection** from claims about delayed external services
5. **Maintained empathy** while being legally responsible

## Key Principle

**NEVER promise specific ETAs for services we don't control:**
- Police, Fire, Paramedics, Ambulance
- Utility companies (gas, electric, water)  
- Any third-party emergency services
- Elevator rescue services
- Specialized medical teams

**BE CAREFUL even with internal services:**
- Consider using ranges instead of specific times
- Use "shortly" or "as soon as possible"
- Only give specific times when absolutely certain

## Implementation Going Forward

All future corpus entries must follow this principle. When dealing with emergencies:
1. Focus on what actions we're taking
2. Avoid specific arrival times for external services
3. Use phrases like "on their way" or "have been notified"
4. Be cautious even with internal service ETAs
5. Maintain urgency without creating liability

## Verification Status

✅ Multiple corpus files processed and cleaned  
✅ 235+ dangerous promises removed  
✅ External service ETAs eliminated  
⚠️ Some internal service ETAs remain (consider reviewing)  
✅ Corpus significantly safer from liability perspective