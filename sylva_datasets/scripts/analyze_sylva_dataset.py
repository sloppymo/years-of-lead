#!/usr/bin/env python3
"""SYLVA Dataset Analysis Script"""

import json
import re
from typing import Dict, List, Any
from pathlib import Path
from datetime import datetime
import argparse


class SylvaDatasetAnalyzer:
    def __init__(self):
        self.archetype_patterns = {
            "Seeker": {
                "keywords": [
                    "lost",
                    "searching",
                    "don't know",
                    "direction",
                    "purpose",
                    "looking for",
                    "trying to find",
                    "which way",
                    "confused",
                    "wandering",
                    "seeking",
                    "need to find",
                    "where do I",
                ]
            },
            "Threshold": {
                "keywords": [
                    "changing",
                    "different",
                    "transform",
                    "between",
                    "transition",
                    "becoming",
                    "shifting",
                    "turning point",
                    "crossroads",
                    "edge",
                    "border",
                    "neither",
                    "both",
                    "in-between",
                    "crossing",
                ]
            },
            "Witness": {
                "keywords": [
                    "alone",
                    "unheard",
                    "no one understands",
                    "shame",
                    "invisible",
                    "nobody sees",
                    "unseen",
                    "silent",
                    "isolated",
                    "hidden",
                    "secret",
                    "bearing witness",
                    "holding",
                    "carrying",
                ]
            },
            "Return": {
                "keywords": [
                    "not myself",
                    "after everything",
                    "changed",
                    "different now",
                    "used to be",
                    "before",
                    "can't go back",
                    "not the same",
                    "forever altered",
                    "transformed",
                    "new person",
                    "coming back",
                ]
            },
        }

        self.emotion_keywords = {
            "sadness": [
                "sad",
                "depressed",
                "hurt",
                "crying",
                "tears",
                "grief",
                "mourning",
                "despair",
                "defeated",
                "hopeless",
                "empty",
                "broken",
                "tired",
                "loss",
            ],
            "anger": [
                "hate",
                "rage",
                "furious",
                "bitter",
                "angry",
                "mad",
                "irritated",
                "frustrated",
                "annoyed",
                "outraged",
                "livid",
                "seething",
                "hostile",
            ],
            "anxiety": [
                "panic",
                "nervous",
                "worry",
                "anxious",
                "jittery",
                "restless",
                "uneasy",
                "apprehensive",
                "dread",
                "horror",
                "paralyzed",
                "frozen",
                "stressed",
            ],
            "shame": [
                "ashamed",
                "embarrassed",
                "dirty",
                "guilt",
                "shameful",
                "disgusting",
                "unworthy",
                "defective",
                "damaged",
                "tainted",
                "contaminated",
                "impure",
            ],
            "overwhelm": [
                "too much",
                "can't breathe",
                "drowning",
                "suffocating",
                "crushed",
                "buried",
                "trapped",
                "stuck",
                "numb",
                "disconnected",
                "overwhelmed",
            ],
            "grief": [
                "missing",
                "gone",
                "died",
                "death",
                "bereaved",
                "grieving",
                "heartbroken",
                "devastated",
                "destroyed",
                "shattered",
                "void",
                "hollow",
                "left behind",
            ],
            "fear": [
                "afraid",
                "scared",
                "terrified",
                "horrified",
                "petrified",
                "frightened",
                "intimidated",
                "threatened",
                "vulnerable",
                "exposed",
                "unsafe",
                "danger",
            ],
            "loneliness": [
                "alone",
                "lonely",
                "isolated",
                "separated",
                "disconnected",
                "abandoned",
                "rejected",
                "excluded",
                "left out",
                "ignored",
                "invisible",
                "forgotten",
            ],
        }

        self.mode_patterns = {
            "emergent": {
                "indicators": [
                    "new",
                    "sudden",
                    "unexpected",
                    "surprise",
                    "emerge",
                    "arise",
                    "appear",
                    "just realized",
                    "suddenly",
                    "out of nowhere",
                ]
            },
            "reflective": {
                "indicators": [
                    "think",
                    "consider",
                    "reflect",
                    "ponder",
                    "wonder",
                    "contemplate",
                    "examine",
                    "looking back",
                    "remembering",
                    "processing",
                ]
            },
            "dispersive": {
                "indicators": [
                    "scattered",
                    "everywhere",
                    "all over",
                    "confused",
                    "mixed",
                    "chaotic",
                    "unclear",
                    "fragmented",
                    "pieces",
                    "bits",
                ]
            },
        }

        self.closure_patterns = [
            r"That's enough for now\.?",
            r"We'll build from that ember\.?",
            r"Let it be named and left\.?",
            r"The container holds what needs holding\.?",
            r"What has been witnessed can rest here\.?",
            r"The boundary honors what is needed\.?",
        ]

    def detect_archetype(self, user_input: str, assistant_response: str) -> str:
        combined_text = f"{user_input} {assistant_response}".lower()
        archetype_scores = {}

        for archetype, data in self.archetype_patterns.items():
            score = 0
            for keyword in data["keywords"]:
                if keyword in combined_text:
                    score += 1
            archetype_scores[archetype] = score

        if not any(archetype_scores.values()):
            return "Seeker"

        return max(archetype_scores.items(), key=lambda x: x[1])[0]

    def detect_emotional_tags(self, user_input: str) -> List[str]:
        text_lower = user_input.lower()
        detected_emotions = []

        for emotion, keywords in self.emotion_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    if emotion not in detected_emotions:
                        detected_emotions.append(emotion)
                    break

        return detected_emotions

    def detect_mode(self, user_input: str, assistant_response: str) -> str:
        combined_text = f"{user_input} {assistant_response}".lower()
        mode_scores = {}

        for mode, data in self.mode_patterns.items():
            score = 0
            for indicator in data["indicators"]:
                if indicator in combined_text:
                    score += 1
            mode_scores[mode] = score

        response_lower = assistant_response.lower()

        if any(word in response_lower for word in ["reflect", "consider", "remember"]):
            mode_scores["reflective"] = mode_scores.get("reflective", 0) + 2

        if any(
            word in response_lower for word in ["emerge", "arise", "new", "discover"]
        ):
            mode_scores["emergent"] = mode_scores.get("emergent", 0) + 2

        if any(
            word in response_lower for word in ["contain", "hold", "gather", "center"]
        ):
            mode_scores["dispersive"] = mode_scores.get("dispersive", 0) + 2

        if not any(mode_scores.values()):
            return "reflective"

        return max(mode_scores.items(), key=lambda x: x[1])[0]

    def extract_closure_elements(self, assistant_response: str) -> Dict[str, Any]:
        closure_data = {
            "has_ritual_closure": False,
            "closure_type": None,
            "closure_text": None,
            "intensity": "light",
        }

        for pattern in self.closure_patterns:
            match = re.search(pattern, assistant_response, re.IGNORECASE)
            if match:
                closure_data["has_ritual_closure"] = True
                closure_data["closure_text"] = match.group(0)

                closure_text = match.group(0).lower()
                if (
                    "container holds" in closure_text
                    or "boundary honors" in closure_text
                ):
                    closure_data["intensity"] = "medium"
                    closure_data["closure_type"] = "boundary"
                elif any(
                    canonical in closure_text
                    for canonical in ["that's enough", "build from", "named and left"]
                ):
                    closure_data["intensity"] = "light"
                    closure_data["closure_type"] = "canonical"

                break

        return closure_data

    def analyze_entry(self, entry: Dict[str, Any]) -> Dict[str, Any]:
        user_input = entry.get("user_input", "")
        assistant_response = entry.get("assistant_response", "")

        archetype = self.detect_archetype(user_input, assistant_response)
        emotional_tags = self.detect_emotional_tags(user_input)
        mode = self.detect_mode(user_input, assistant_response)
        closure_elements = self.extract_closure_elements(assistant_response)

        sylva_entry = {
            "entry_id": entry.get("id", f"entry_{datetime.now().timestamp()}"),
            "timestamp": entry.get("timestamp", datetime.now().isoformat()),
            "user_input": user_input,
            "assistant_response": assistant_response,
            "archetype": archetype,
            "emotional_tags": emotional_tags,
            "mode": mode,
            "closure_elements": closure_elements,
            "analysis_metadata": {
                "containment_paradigm": True,
                "trauma_safe": True,
                "symbolic_response": True,
                "analysis_timestamp": datetime.now().isoformat(),
                "analyzer_version": "1.0.0",
            },
        }

        subsystem_mapping = {
            "Seeker": "ROOT",
            "Threshold": "MARROW",
            "Witness": "AURA",
            "Return": "MARROW",
        }
        sylva_entry["subsystem"] = subsystem_mapping.get(archetype, "ROOT")

        return sylva_entry

    def process_dataset(
        self, input_file: str, output_file: str = None
    ) -> List[Dict[str, Any]]:
        input_path = Path(input_file)

        if not input_path.exists():
            print(f"Error: Input file '{input_file}' not found.")
            return []

        processed_entries = []

        try:
            with open(input_path, "r", encoding="utf-8") as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if not line:
                        continue

                    try:
                        entry = json.loads(line)
                        processed_entry = self.analyze_entry(entry)
                        processed_entries.append(processed_entry)

                        if line_num % 100 == 0:
                            print(f"Processed {line_num} entries...")

                    except json.JSONDecodeError as e:
                        print(f"Warning: Could not parse line {line_num}: {e}")
                    except Exception as e:
                        print(f"Warning: Error processing line {line_num}: {e}")

        except Exception as e:
            print(f"Error reading file: {e}")
            return []

        print(f"Successfully processed {len(processed_entries)} entries.")

        if output_file:
            self.save_processed_data(processed_entries, output_file)

        return processed_entries

    def save_processed_data(
        self, processed_entries: List[Dict[str, Any]], output_file: str
    ):
        try:
            with open(output_file, "w", encoding="utf-8") as f:
                for entry in processed_entries:
                    json.dump(entry, f, ensure_ascii=False)
                    f.write("\n")

            print(
                f"Saved {len(processed_entries)} processed entries to '{output_file}'"
            )
            self.save_analysis_summary(
                processed_entries, Path(output_file).stem + "_summary.json"
            )

        except Exception as e:
            print(f"Error saving processed data: {e}")

    def save_analysis_summary(
        self, processed_entries: List[Dict[str, Any]], summary_file: str
    ):
        if not processed_entries:
            return

        archetype_counts = {}
        emotion_counts = {}
        mode_counts = {}
        closure_counts = {"has_closure": 0, "no_closure": 0}

        for entry in processed_entries:
            archetype = entry.get("archetype", "Unknown")
            archetype_counts[archetype] = archetype_counts.get(archetype, 0) + 1

            for emotion in entry.get("emotional_tags", []):
                emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1

            mode = entry.get("mode", "Unknown")
            mode_counts[mode] = mode_counts.get(mode, 0) + 1

            if entry.get("closure_elements", {}).get("has_ritual_closure", False):
                closure_counts["has_closure"] += 1
            else:
                closure_counts["no_closure"] += 1

        summary = {
            "total_entries": len(processed_entries),
            "analysis_timestamp": datetime.now().isoformat(),
            "archetype_distribution": archetype_counts,
            "emotional_tag_distribution": emotion_counts,
            "mode_distribution": mode_counts,
            "closure_distribution": closure_counts,
            "top_emotions": sorted(
                emotion_counts.items(), key=lambda x: x[1], reverse=True
            )[:5],
        }

        try:
            with open(summary_file, "w", encoding="utf-8") as f:
                json.dump(summary, f, indent=2, ensure_ascii=False)
            print(f"Saved analysis summary to '{summary_file}'")
        except Exception as e:
            print(f"Error saving summary: {e}")


def main():
    parser = argparse.ArgumentParser(description="Analyze SYLVA empathy dataset")
    parser.add_argument(
        "input_file",
        nargs="?",
        default="sylva_full_empathy_dataset.jsonl",
        help="Input JSONL file",
    )
    parser.add_argument(
        "-o", "--output", default="sylva_processed_dataset.jsonl", help="Output file"
    )

    args = parser.parse_args()

    print("🌙 SYLVA Dataset Analyzer")
    print("=" * 50)
    print("Analyzing entries for:")
    print("• Archetypes (Seeker, Threshold, Witness, Return)")
    print("• Emotional tags based on content analysis")
    print("• Modes (reflective/emergent/dispersive)")
    print("• Ritual closure elements")
    print("• SYLVA format transformation")
    print("=" * 50)

    analyzer = SylvaDatasetAnalyzer()
    processed_entries = analyzer.process_dataset(args.input_file, args.output)

    if processed_entries:
        print(f"✨ Analysis complete! Check '{args.output}' for results.")
    else:
        print("❌ No entries processed. Check input file.")


if __name__ == "__main__":
    main()
