# SYLVA Dataset Analysis Script

> **🌙 A comprehensive analysis tool for transforming empathy datasets into SYLVA format**

## Overview

The SYLVA Dataset Analysis Script processes `sylva_full_empathy_dataset.jsonl` files and transforms them according to SYLVA's containment-over-completion paradigm. The script analyzes user input and assistant responses to assign appropriate archetypes, emotional tags, modes, and closure elements while maintaining trauma-safe symbolic boundaries.

According to memories: **SYLVA follows containment-over-completion paradigm with canonical ritual closure lines and trauma-safe symbolic responses.**

## Features

### 🎭 Archetype Detection
Analyzes text patterns to assign one of four core archetypes:

- **Seeker**: Users expressing uncertainty, searching for direction or purpose
  - Keywords: "lost", "searching", "don't know", "direction", "purpose", "looking for"

- **Threshold**: Users experiencing transformation or transitions
  - Keywords: "changing", "different", "transform", "between", "transition", "becoming"

- **Witness**: Users feeling isolated, unheard, or carrying shame
  - Keywords: "alone", "unheard", "no one understands", "shame", "invisible", "unseen"

- **Return**: Users integrating change and post-transformation identity
  - Keywords: "not myself", "after everything", "changed", "different now", "can't go back"

### 🧠 Emotional Analysis
Detects emotional content using comprehensive keyword mapping:
- **sadness**: grief, despair, hopeless, broken, loss
- **anger**: rage, fury, bitter, frustrated, hostile
- **anxiety**: panic, nervous, worry, dread, frozen
- **shame**: ashamed, guilty, unworthy, defective
- **overwhelm**: too much, drowning, trapped, stuck
- **grief**: missing, bereaved, devastated, hollow
- **fear**: afraid, scared, threatened, vulnerable
- **loneliness**: alone, isolated, abandoned, invisible

### 🌊 Mode Classification
Determines interaction mode based on response patterns:
- **Reflective**: Deep contemplation and processing
- **Emergent**: New insights and discoveries arising
- **Dispersive**: Scattered energy seeking integration

### 🔄 Closure Element Detection
Identifies and analyzes SYLVA's canonical ritual closures:
- **Canonical**: "That's enough for now.", "We'll build from that ember.", "Let it be named and left."
- **Boundary**: "The container holds what needs holding.", "The boundary honors what is needed."
- **Containment**: Advanced closure patterns with deeper symbolic protection

## Usage

### Basic Usage
```bash
python3 analyze_sylva_dataset.py sylva_full_empathy_dataset.jsonl
```

### With Custom Output File
```bash
python3 analyze_sylva_dataset.py input_file.jsonl -o processed_output.jsonl
```

### Command Line Options
```bash
python3 analyze_sylva_dataset.py --help

usage: analyze_sylva_dataset.py [-h] [-o OUTPUT] [input_file]

Analyze SYLVA empathy dataset

positional arguments:
  input_file            Input JSONL file (default: sylva_full_empathy_dataset.jsonl)

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output file (default: sylva_processed_dataset.jsonl)
```

## Input Format

The script expects JSONL files with entries containing:
```json
{
  "id": "unique_identifier",
  "timestamp": "2024-01-01T10:00:00",
  "user_input": "User's input text...",
  "assistant_response": "Assistant's response..."
}
```

## Output Format

### Processed Entries (JSONL)
Each entry is transformed into SYLVA format:
```json
{
  "entry_id": "sample_1",
  "timestamp": "2024-01-01T10:00:00",
  "user_input": "Original user input...",
  "assistant_response": "Original assistant response...",
  "archetype": "Seeker",
  "emotional_tags": ["loneliness", "anxiety"],
  "mode": "reflective",
  "subsystem": "ROOT",
  "closure_elements": {
    "has_ritual_closure": true,
    "closure_type": "canonical",
    "closure_text": "That's enough for now.",
    "intensity": "light"
  },
  "analysis_metadata": {
    "containment_paradigm": true,
    "trauma_safe": true,
    "symbolic_response": true,
    "analysis_timestamp": "2025-06-12T23:49:56.762367",
    "analyzer_version": "1.0.0"
  }
}
```

### Analysis Summary (JSON)
Comprehensive statistics about the processed dataset:
```json
{
  "total_entries": 1247,
  "analysis_timestamp": "2025-06-12T23:49:56.762958",
  "archetype_distribution": {
    "Seeker": 312,
    "Threshold": 298,
    "Witness": 385,
    "Return": 252
  },
  "emotional_tag_distribution": {
    "loneliness": 156,
    "anxiety": 142,
    "sadness": 134
  },
  "mode_distribution": {
    "reflective": 678,
    "emergent": 298,
    "dispersive": 271
  },
  "closure_distribution": {
    "has_closure": 892,
    "no_closure": 355
  },
  "top_emotions": [
    ["loneliness", 156],
    ["anxiety", 142],
    ["sadness", 134]
  ]
}
```

## Subsystem Mapping

Based on archetype detection, entries are mapped to SYLVA subsystems:
- **Seeker** → `ROOT` (Seeking direction and grounding)
- **Threshold** → `MARROW` (Deep transformation work)
- **Witness** → `AURA` (Boundary and visibility work)
- **Return** → `MARROW` (Integration and identity work)

## Example Demonstration

Run with the included sample data:
```bash
python3 analyze_sylva_dataset.py sample_sylva_data.jsonl -o demo_output.jsonl
```

This will process 4 sample entries representing each archetype and generate:
- `demo_output.jsonl`: Processed entries in SYLVA format
- `demo_output_summary.json`: Analysis statistics

## Key Features

### ✅ Trauma-Safe Design
- Maintains containment-over-completion paradigm
- Respects symbolic boundaries
- No clinical interpretation or advice-giving

### ✅ Comprehensive Analysis
- Multi-dimensional archetype detection
- Emotional content mapping
- Mode classification
- Closure element extraction

### ✅ Robust Processing
- Handles malformed JSON gracefully
- Progress tracking for large datasets
- Comprehensive error handling

### ✅ Rich Output
- Detailed per-entry analysis
- Statistical summaries
- Metadata tracking

## Integration with SYLVA Ecosystem

This script integrates with the broader SYLVA symbolic interaction framework:
- Uses patterns from `utils/archetype_engine.py`
- Follows emotion mappings from `utils/pattern_engine.py`
- Maintains compatibility with SYLVA's three subsystems (MARROW/ROOT/AURA)
- Preserves canonical ritual closure requirements

## Requirements

- Python 3.7+
- Standard library modules: `json`, `re`, `pathlib`, `datetime`, `argparse`
- No external dependencies required

## Notes

- Processing time scales linearly with dataset size
- Large datasets (>10k entries) will show progress indicators
- All analysis maintains symbolic containment principles
- Output preserves original content while adding SYLVA analysis layers

---

**🌙 SYLVA Dataset Analyzer** - Where containment meets comprehensive analysis, and every entry honors the sacred boundary between symbolic reflection and completion.
