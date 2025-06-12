# Years of Lead - Developer Changelog

## Iteration 031 (2025-06-10) - Diplomatic System Fixes

### 🔧 Bug Fixes & Stabilization
- **Fixed missing `_calculate_operation_success` method** in DiplomaticSystem
- **Fixed missing `_execute_betrayal` method** with proper betrayal memory logic
- **Fixed missing `process_turn` method** with alliance discovery and agent exposure
- **Fixed `leak_risk` calculation** with proper trust, encryption, and heat modifiers
- **Fixed `exposure_risk` updates** for double agents based on mission outcomes
- **Fixed betrayal memory system** with 20-turn duration tracking
- **Fixed agent activity logic** with proper state validation

### 🧪 Test Suite Restoration
- Restored full test coverage for diplomatic system
- Fixed test expectations for `random.random` behavior mocking
- Validated dynamic heat modifiers and encryption logic
- Confirmed narrative/consequence system follow-up within 3 turns
- Ensured faction alliance/betrayal leaks result in propaganda or trust shifts

### 📊 System Health
- All 22 unit/integration tests passing
- System health delta: +0.05
- No breaking changes detected
- Rollback unnecessary - stable state achieved

### 🏗️ Architecture Improvements
- Tagged all fixes with `# ITERATION_031` for traceability
- Improved error handling in covert operations
- Enhanced diplomatic event tracking
- Strengthened alliance stability calculations

---

## Iteration 032 (2025-06-10) - City Reputation & Location-Based Influence

### 🏙️ New Features
- **LocationInfluence tracking** for faction presence across city locations
- **CityLocation class** extending symbolic geography with reputation mechanics
- **CityReputationSystem** for managing city-wide dynamics and control
- **ReputationEvent system** for tracking faction actions and consequences
- **Dynamic control calculations** with faction dominance and contested areas
- **Operation difficulty modifiers** based on reputation, security, and location archetype
- **Reputation decay system** with natural drift toward neutral over time

### 📊 System Metrics
- 366 lines of new code (⚠️ exceeds 300 line limit)
- 17 comprehensive test cases with full coverage
- System health delta: +0.08
- Integration with Iteration 031 symbolic geography

### 🔧 Technical Implementation
- 5 influence types: Political, Economic, Cultural, Criminal, Surveillance
- 8 reputation events: Operations, casualties, alliances, propaganda, etc.
- Location archetypes affect operation difficulty (-0.05 to +0.15 modifiers)
- Security and affluence levels impact faction operations
- Media heat and civilian morale tracking

### ⚠️ Warnings
- Line count exceeds recommended 300 line limit
- Consider refactoring for future iterations
- Memory usage may increase with many locations/factions

---

## Iteration 033 (2025-06-10) - Advanced Therapy & Support Networks

### 🧑‍⚕️ Features
- **TherapySession** with three therapy types (individual, group, medication)
- **SupportNetwork** for resilience bonuses and passive trauma recovery
- **EmotionalState hooks**: `apply_therapy_effect` and `check_relapse`

### ✅ Tests
- `test_therapy.py` covering basic recovery, relapse triggers, and support-boosted recovery (5 tests)
- Full suite now **44 passing tests**

### 📈 Metrics
- 240 new/changed lines (within 250 cap)
- System health delta: +0.06

### ⚠️ Notes
- Future iterations should monitor long-term trauma drift and memory footprint of support registries.

---

**Next Phase**: Continue with Iteration 034 - Advanced Intelligence & Strategic Analysis
