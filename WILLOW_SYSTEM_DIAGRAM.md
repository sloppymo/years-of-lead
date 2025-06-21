# Willow Integrated System Architecture Diagram

## System Flow Visualization

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        WILLOW INTEGRATED CRISIS SUPPORT                      │
└─────────────────────────────────────────────────────────────────────────────┘

                                  USER MESSAGE
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         1. BILINGUAL CRISIS DETECTOR                         │
│  • Detects language switching (ES, ZH, AR, TL)                              │
│  • Monitors code-switching patterns                                         │
│  • Checks arousal + language correlation                                    │
│  ┌─────────────────────────────────────────────┐                          │
│  │ IF: High Arousal + Language Switch          │───────► HUMAN ROUTING     │
│  │     → Route to bilingual specialist         │         (Immediate)       │
│  └─────────────────────────────────────────────┘                          │
└─────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                       2. CAPACITY DECAY ANALYZER                            │
│  • Tracks cognitive capacity (0-10 scale)                                   │
│  • Detects rapid decline patterns                                           │
│  • Identifies dissociation markers                                          │
│  ┌─────────────────────────────────────────────┐                          │
│  │ IF: Capacity < 2.0 (Severe Exhaustion)      │───────► HUMAN ROUTING     │
│  │     → Emergency escalation                  │         (High Priority)    │
│  └─────────────────────────────────────────────┘                          │
└─────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                     3. GLOBAL TIER FLOW CONTROLLER                          │
│  • Enforces therapeutic progression                                         │
│  • Tier 1 (Containment) → 1.5 (Bridge) → 2 (Action)                       │
│  • Requires: Min 2 Tier 1, Arousal < 7, Consent                           │
│  ┌─────────────────────────────────────────────┐                          │
│  │ IF: Arousal > 9.5 + Capacity < 2            │───────► HUMAN ROUTING     │
│  │     → Crisis escalation                     │         (Immediate)        │
│  └─────────────────────────────────────────────┘                          │
└─────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    4. CAPACITY-AWARE ADAPTATION                             │
│  • Adjusts language complexity based on capacity                            │
│  • Emergency simplification mode                                            │
│  • Grounding prioritization                                                 │
└─────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                     5. UNIFIED SYMBOLIC ANCHOR                              │
│  • Wraps response with consistent symbols                                   │
│  • Maintains continuity across all message types                           │
│  • Styles: Traditional 💙, Nature 🌊, Minimal •, None                      │
└─────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
                              FINAL RESPONSE
```

## Edge Case Handling

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          EDGE CASE RESOLVER                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│  Rapid Fire Messages  │  "I see many messages. Let's breathe together ⚡→💙" │
│  Contradictions       │  "Changing your mind is okay. I'm here 🔄"         │
│  Language Switching   │  "Continue in whatever language feels natural 🌍"   │
│  Dissociation        │  "Notice one thing you can touch right now 🌿"      │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Escalation Decision Matrix

```
┌─────────────────────┬─────────────────┬───────────────┬──────────────────┐
│     CONDITION       │     TRIGGER     │   PRIORITY    │   SPECIALIST     │
├─────────────────────┼─────────────────┼───────────────┼──────────────────┤
│ Capacity < 2.0      │ Severe Exhaust  │ High          │ Crisis Support   │
│ Arousal > 9.5 +     │ Crisis State    │ Immediate     │ Crisis Support   │
│ Capacity < 2        │                 │               │                  │
│ Language Switch +   │ Bilingual       │ High          │ Bilingual        │
│ Arousal > 8.0       │ Crisis          │               │ (ES/ZH/AR/TL)    │
│ Dissociation        │ Safety Risk     │ Immediate     │ Clinical Team    │
│ Markers             │                 │               │                  │
│ Session > 30min +   │ Prolonged       │ Medium        │ Senior Support   │
│ No Progress         │ Crisis          │               │                  │
└─────────────────────┴─────────────────┴───────────────┴──────────────────┘
```

## Response Examples by System State

### Tier 1 - High Capacity (💚 Stable)
```
User: "My heat is broken!"
Willow: "I'm here with you. Having no heat is unacceptable. 🌊"
```

### Tier 1 - Declining Capacity (🟡 Monitor)
```
User: "can't think straight"
Willow: "This is overwhelming. Breathe with me. 🌊"
```

### Tier 1 - Low Capacity (🔴 Alert)
```
User: "..."
Willow: "I'm here. 🌊"
```

### Tier 2 - With Consent (💚 Ready)
```
User: "Yes, what are my options?"
Willow: "When ready:
1. Text HEAT for emergency team 🌊
2. Reply SAFE if secure
3. Text STATUS for updates"
```

### Escalation - Bilingual Crisis (🚨 Route)
```
User: "AYUDA!! No puedo más!!"
Willow: "Estoy conectándote con alguien que habla español. Un momento. 🌍"
```

## Session Lifecycle

```
START SESSION
     │
     ├─→ Initialize User Context
     │   • Symbolic preference
     │   • Language profile
     │   • Baseline capacity
     │
     ├─→ Process Messages
     │   │
     │   ├─→ Update States
     │   │   • Track capacity
     │   │   • Monitor arousal
     │   │   • Detect patterns
     │   │
     │   └─→ Generate Response
     │       • Apply all systems
     │       • Check escalation
     │       • Maintain continuity
     │
     └─→ End Session
         • Generate metrics
         • Store patterns
         • Clean up state
```

## Key Innovation Points

1. **First AI to enforce trauma-informed tier progression**
2. **Pioneering capacity-aware language adaptation**
3. **Novel symbolic continuity across all interaction types**
4. **Advanced multilingual crisis detection**
5. **Multiple independent escalation pathways**
6. **Graceful degradation at every level**