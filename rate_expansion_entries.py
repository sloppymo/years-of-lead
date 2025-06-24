#!/usr/bin/env python3
"""
Rate WILLOW expansion entries for quality across multiple dimensions
"""

import json
from datetime import datetime
from typing import Dict, List, Tuple

class ExpansionEntryRater:
    def __init__(self):
        self.rating_criteria = {
            "dialogue_quality": {
                "weight": 0.15,
                "checks": [
                    "natural_language",
                    "appropriate_tone",
                    "clear_communication",
                    "no_jargon"
                ]
            },
            "tier_progression": {
                "weight": 0.20,
                "checks": [
                    "proper_tier1_containment",
                    "appropriate_tier2_action",
                    "logical_flow",
                    "no_premature_solutioning"
                ]
            },
            "legal_safety": {
                "weight": 0.20,
                "checks": [
                    "no_promises",
                    "process_transparency",
                    "clear_limitations",
                    "no_liability_language"
                ]
            },
            "emergency_response": {
                "weight": 0.15,
                "checks": [
                    "appropriate_urgency",
                    "clear_protocols",
                    "specific_timelines",
                    "proper_escalation"
                ]
            },
            "trauma_informed": {
                "weight": 0.15,
                "checks": [
                    "emotional_validation",
                    "safety_focus",
                    "empowerment_language",
                    "no_minimizing"
                ]
            },
            "scenario_realism": {
                "weight": 0.10,
                "checks": [
                    "believable_situation",
                    "appropriate_complexity",
                    "realistic_responses",
                    "practical_solutions"
                ]
            },
            "completeness": {
                "weight": 0.05,
                "checks": [
                    "has_metadata",
                    "proper_tags",
                    "clear_category",
                    "all_fields_present"
                ]
            }
        }
        
        # Problematic patterns to check for
        self.red_flags = [
            "will definitely",
            "guarantee",
            "promise",
            "honey",
            "sweetie",
            "darling",
            "calm down",
            "don't worry",
            "everything will be fine",
            "nothing to worry about"
        ]
        
        # Positive patterns to look for
        self.green_flags = [
            "I hear you",
            "I understand",
            "Your safety",
            "I'm dispatching",
            "emergency services",
            "right now",
            "immediately",
            "ETA",
            "I'm here with you",
            "You're being brave"
        ]

    def rate_entry(self, entry: Dict) -> Tuple[float, Dict[str, float], List[str]]:
        """Rate a single entry and return score, breakdown, and notes"""
        scores = {}
        notes = []
        
        # Extract messages for analysis
        messages = entry.get("messages", [])
        if not messages:
            return 0.0, {}, ["No messages found"]
        
        # Rate each criterion
        scores["dialogue_quality"] = self._rate_dialogue_quality(messages, notes)
        scores["tier_progression"] = self._rate_tier_progression(messages, notes)
        scores["legal_safety"] = self._rate_legal_safety(messages, notes)
        scores["emergency_response"] = self._rate_emergency_response(entry, messages, notes)
        scores["trauma_informed"] = self._rate_trauma_informed(messages, notes)
        scores["scenario_realism"] = self._rate_scenario_realism(entry, messages, notes)
        scores["completeness"] = self._rate_completeness(entry, notes)
        
        # Calculate weighted total
        total_score = sum(
            scores[criterion] * self.rating_criteria[criterion]["weight"]
            for criterion in scores
        )
        
        return total_score, scores, notes

    def _rate_dialogue_quality(self, messages: List[Dict], notes: List[str]) -> float:
        """Rate the quality of dialogue"""
        score = 10.0
        
        # Check for red flags
        for msg in messages:
            content = msg.get("content", "").lower()
            for red_flag in self.red_flags:
                if red_flag in content:
                    score -= 2.0
                    notes.append(f"Red flag found: '{red_flag}'")
        
        # Check for natural language
        assistant_messages = [m for m in messages if m.get("role") == "assistant"]
        if not assistant_messages:
            score -= 3.0
            notes.append("No assistant messages found")
        else:
            # Check for appropriate tone
            for msg in assistant_messages:
                content = msg.get("content", "")
                if len(content) < 50:
                    score -= 1.0
                    notes.append("Response too short")
                if len(content) > 500:
                    score -= 0.5
                    notes.append("Response too long")
        
        return max(0, score)

    def _rate_tier_progression(self, messages: List[Dict], notes: List[str]) -> float:
        """Rate the tier progression logic"""
        score = 10.0
        
        # Find tier 1 and tier 2 messages
        tier1_found = False
        tier2_found = False
        tier1_before_tier2 = True
        
        for i, msg in enumerate(messages):
            if msg.get("role") == "assistant":
                metadata = msg.get("metadata", {})
                tier = metadata.get("tier") or msg.get("tier")
                
                if tier == "tier_1":
                    tier1_found = True
                    if tier2_found:
                        tier1_before_tier2 = False
                elif tier == "tier_2":
                    tier2_found = True
        
        if not tier1_found:
            score -= 3.0
            notes.append("No tier 1 response found")
        
        if not tier2_found:
            score -= 3.0
            notes.append("No tier 2 response found")
        
        if not tier1_before_tier2:
            score -= 4.0
            notes.append("Tier progression out of order")
        
        # Check tier 1 is containment focused
        for msg in messages:
            if msg.get("role") == "assistant":
                metadata = msg.get("metadata", {})
                tier = metadata.get("tier") or msg.get("tier")
                if tier == "tier_1":
                    content = msg.get("content", "").lower()
                    if any(action in content for action in ["calling 911", "dispatching", "will arrive"]):
                        score -= 2.0
                        notes.append("Tier 1 contains premature action")
                        break
        
        return max(0, score)

    def _rate_legal_safety(self, messages: List[Dict], notes: List[str]) -> float:
        """Rate legal safety compliance"""
        score = 10.0
        
        dangerous_phrases = [
            "will definitely",
            "guarantee",
            "promise",
            "ensure your",
            "make sure you get",
            "you'll receive"
        ]
        
        good_phrases = [
            "working to",
            "in process",
            "coordinating",
            "I've initiated",
            "I'm dispatching"
        ]
        
        for msg in messages:
            if msg.get("role") == "assistant":
                content = msg.get("content", "").lower()
                
                # Check for dangerous promises
                for phrase in dangerous_phrases:
                    if phrase in content:
                        score -= 3.0
                        notes.append(f"Dangerous promise: '{phrase}'")
                
                # Check for good process language
                good_found = False
                for phrase in good_phrases:
                    if phrase in content:
                        good_found = True
                        break
                
                if not good_found and "tier_2" in str(msg.get("metadata", {})):
                    score -= 1.0
        
        return max(0, score)

    def _rate_emergency_response(self, entry: Dict, messages: List[Dict], notes: List[str]) -> float:
        """Rate emergency response appropriateness"""
        score = 10.0
        
        category = entry.get("category", "")
        is_emergency = any(term in category for term in ["earthquake", "fire", "flood", "heart_attack", "stroke", "break_in", "gas_leak"])
        
        if is_emergency:
            # Should have urgent response
            emergency_terms = ["911", "emergency", "immediately", "right now", "urgent"]
            found_urgency = False
            
            for msg in messages:
                if msg.get("role") == "assistant":
                    content = msg.get("content", "").lower()
                    if any(term in content for term in emergency_terms):
                        found_urgency = True
                        break
            
            if not found_urgency:
                score -= 3.0
                notes.append("Emergency scenario lacks urgency")
            
            # Should have specific timelines
            timeline_terms = ["minutes", "eta", "arrival", "on the way", "dispatched"]
            found_timeline = False
            
            for msg in messages:
                if msg.get("role") == "assistant" and "tier_2" in str(msg.get("metadata", {})):
                    content = msg.get("content", "").lower()
                    if any(term in content for term in timeline_terms):
                        found_timeline = True
                        break
            
            if not found_timeline:
                score -= 2.0
                notes.append("No specific timeline provided")
        
        return max(0, score)

    def _rate_trauma_informed(self, messages: List[Dict], notes: List[str]) -> float:
        """Rate trauma-informed approach"""
        score = 10.0
        
        # Check for validation
        validation_terms = ["I hear", "I understand", "I can see", "must be", "sounds", "I believe you"]
        found_validation = False
        
        for msg in messages:
            if msg.get("role") == "assistant" and "tier_1" in str(msg.get("metadata", {})):
                content = msg.get("content", "")
                if any(term in content for term in validation_terms):
                    found_validation = True
                    break
        
        if not found_validation:
            score -= 3.0
            notes.append("Lacks emotional validation")
        
        # Check for minimizing language
        minimizing_terms = ["just", "simply", "only", "don't worry", "calm down", "it's okay"]
        
        for msg in messages:
            if msg.get("role") == "assistant":
                content = msg.get("content", "").lower()
                for term in minimizing_terms:
                    if term in content:
                        score -= 1.5
                        notes.append(f"Minimizing language: '{term}'")
                        break
        
        return max(0, score)

    def _rate_scenario_realism(self, entry: Dict, messages: List[Dict], notes: List[str]) -> float:
        """Rate scenario realism"""
        score = 10.0
        
        # Check if scenario is believable
        if len(messages) < 2:
            score -= 3.0
            notes.append("Conversation too short")
        
        # Check for appropriate complexity
        category = entry.get("category", "")
        complexity = entry.get("complexity_level", "")
        
        if "emergency" in category and complexity != "critical":
            score -= 2.0
            notes.append("Emergency not marked as critical")
        
        # Check for realistic user messages
        user_messages = [m for m in messages if m.get("role") in ["user", "resident"]]
        if user_messages:
            first_msg = user_messages[0].get("content", "")
            if len(first_msg) < 20:
                score -= 2.0
                notes.append("Initial user message too brief")
        
        return max(0, score)

    def _rate_completeness(self, entry: Dict, notes: List[str]) -> float:
        """Rate entry completeness"""
        score = 10.0
        
        required_fields = ["id", "user_type", "category", "messages", "complexity_level", "tags"]
        
        for field in required_fields:
            if field not in entry:
                score -= 2.0
                notes.append(f"Missing field: {field}")
        
        # Check tags
        if "tags" in entry:
            required_tags = ["urgency_level", "primary_emotion", "topics"]
            tags = entry.get("tags", {})
            for tag in required_tags:
                if tag not in tags:
                    score -= 1.0
                    notes.append(f"Missing tag: {tag}")
        
        return max(0, score)

def main():
    """Rate all expansion entries"""
    
    import sys
    
    # Check if filename provided as argument
    if len(sys.argv) > 1:
        target_file = sys.argv[1]
    else:
        # Find expansion file
        import glob
        expansion_files = glob.glob("willow_expansion_phase1_*.jsonl")
        if not expansion_files:
            print("No expansion files found!")
            return
        
        # Use the main expansion file (not enhanced)
        target_file = "willow_expansion_phase1_20250624_003259.jsonl"
        if target_file not in expansion_files:
            target_file = sorted(expansion_files)[0]
    
    print(f"Rating entries from: {target_file}")
    print("=" * 80)
    
    # Load entries
    entries = []
    with open(target_file, 'r') as f:
        for line in f:
            entries.append(json.loads(line))
    
    print(f"Loaded {len(entries)} entries for rating\n")
    
    # Rate entries
    rater = ExpansionEntryRater()
    ratings = []
    
    # Score distribution
    score_buckets = {
        "9.5+": 0,
        "9.0-9.5": 0,
        "8.5-9.0": 0,
        "8.0-8.5": 0,
        "7.5-8.0": 0,
        "7.0-7.5": 0,
        "6.5-7.0": 0,
        "<6.5": 0
    }
    
    # Category performance
    category_scores = {}
    
    # Rate each entry
    for entry in entries:
        score, breakdown, notes = rater.rate_entry(entry)
        
        rating_data = {
            "id": entry.get("id"),
            "category": entry.get("category"),
            "user_type": entry.get("user_type"),
            "score": score,
            "breakdown": breakdown,
            "notes": notes
        }
        
        ratings.append(rating_data)
        
        # Update buckets
        if score >= 9.5:
            score_buckets["9.5+"] += 1
        elif score >= 9.0:
            score_buckets["9.0-9.5"] += 1
        elif score >= 8.5:
            score_buckets["8.5-9.0"] += 1
        elif score >= 8.0:
            score_buckets["8.0-8.5"] += 1
        elif score >= 7.5:
            score_buckets["7.5-8.0"] += 1
        elif score >= 7.0:
            score_buckets["7.0-7.5"] += 1
        elif score >= 6.5:
            score_buckets["6.5-7.0"] += 1
        else:
            score_buckets["<6.5"] += 1
        
        # Track category performance
        category = entry.get("category", "unknown")
        if category not in category_scores:
            category_scores[category] = []
        category_scores[category].append(score)
    
    # Calculate statistics
    all_scores = [r["score"] for r in ratings]
    avg_score = sum(all_scores) / len(all_scores)
    min_score = min(all_scores)
    max_score = max(all_scores)
    
    # Find best and worst entries
    sorted_ratings = sorted(ratings, key=lambda x: x["score"], reverse=True)
    best_entries = sorted_ratings[:5]
    worst_entries = sorted_ratings[-5:]
    
    # Generate report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"expansion_quality_report_{timestamp}.md"
    
    with open(report_file, 'w') as f:
        f.write("# WILLOW Expansion Phase 1 Quality Report\n\n")
        f.write(f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**File Analyzed**: `{target_file}`\n")
        f.write(f"**Total Entries**: {len(entries)}\n\n")
        
        f.write("## Overall Statistics\n\n")
        f.write(f"- **Average Score**: {avg_score:.2f}/10\n")
        f.write(f"- **Minimum Score**: {min_score:.2f}/10\n")
        f.write(f"- **Maximum Score**: {max_score:.2f}/10\n")
        f.write(f"- **Standard Deviation**: {(sum((s - avg_score)**2 for s in all_scores) / len(all_scores))**0.5:.2f}\n\n")
        
        f.write("## Score Distribution\n\n")
        f.write("| Score Range | Count | Percentage |\n")
        f.write("|-------------|-------|------------|\n")
        for bucket, count in score_buckets.items():
            percentage = (count / len(entries)) * 100
            f.write(f"| {bucket} | {count} | {percentage:.1f}% |\n")
        
        f.write("\n## Category Performance\n\n")
        f.write("| Category | Avg Score | Count |\n")
        f.write("|----------|-----------|-------|\n")
        
        category_averages = []
        for category, scores in category_scores.items():
            avg = sum(scores) / len(scores)
            category_averages.append((category, avg, len(scores)))
        
        for category, avg, count in sorted(category_averages, key=lambda x: x[1], reverse=True)[:10]:
            f.write(f"| {category} | {avg:.2f} | {count} |\n")
        
        f.write("\n## Top 5 Best Entries\n\n")
        for i, entry in enumerate(best_entries, 1):
            f.write(f"### {i}. {entry['id']} (Score: {entry['score']:.2f})\n")
            f.write(f"- **Category**: {entry['category']}\n")
            f.write(f"- **User Type**: {entry['user_type']}\n")
            f.write(f"- **Strengths**: {', '.join(k for k, v in entry['breakdown'].items() if v >= 9)}\n")
            if entry['notes']:
                f.write(f"- **Notes**: {entry['notes'][0]}\n")
            f.write("\n")
        
        f.write("\n## Bottom 5 Entries (Need Improvement)\n\n")
        for i, entry in enumerate(worst_entries, 1):
            f.write(f"### {i}. {entry['id']} (Score: {entry['score']:.2f})\n")
            f.write(f"- **Category**: {entry['category']}\n")
            f.write(f"- **User Type**: {entry['user_type']}\n")
            f.write(f"- **Weaknesses**: {', '.join(k for k, v in entry['breakdown'].items() if v < 7)}\n")
            if entry['notes']:
                f.write(f"- **Issues**: {'; '.join(entry['notes'][:3])}\n")
            f.write("\n")
        
        f.write("\n## Common Issues Found\n\n")
        all_notes = []
        for rating in ratings:
            all_notes.extend(rating['notes'])
        
        from collections import Counter
        note_counts = Counter(all_notes)
        
        f.write("| Issue | Occurrences |\n")
        f.write("|-------|-------------|\n")
        for note, count in note_counts.most_common(10):
            f.write(f"| {note} | {count} |\n")
        
        f.write("\n## Recommendations\n\n")
        
        if avg_score < 8.0:
            f.write("1. **Critical**: Average score below 8.0 indicates systematic issues\n")
        
        if score_buckets["<6.5"] > 10:
            f.write("2. **High Priority**: More than 10 entries scored below 6.5\n")
        
        if "No tier 1 response found" in [n for r in ratings for n in r['notes']]:
            f.write("3. **Tier System**: Some entries missing proper tier progression\n")
        
        if "Dangerous promise" in [n for r in ratings for n in r['notes']]:
            f.write("4. **Legal Risk**: Found entries with promissory language\n")
        
        f.write("\n## Quality Threshold Analysis\n\n")
        above_9 = sum(1 for s in all_scores if s >= 9.0)
        above_85 = sum(1 for s in all_scores if s >= 8.5)
        above_8 = sum(1 for s in all_scores if s >= 8.0)
        
        f.write(f"- Entries scoring 9.0+: {above_9} ({(above_9/len(entries)*100):.1f}%)\n")
        f.write(f"- Entries scoring 8.5+: {above_85} ({(above_85/len(entries)*100):.1f}%)\n")
        f.write(f"- Entries scoring 8.0+: {above_8} ({(above_8/len(entries)*100):.1f}%)\n")
    
    # Save detailed ratings
    ratings_file = f"expansion_ratings_detail_{timestamp}.json"
    with open(ratings_file, 'w') as f:
        json.dump(ratings, f, indent=2)
    
    # Print summary
    print(f"Quality Rating Complete!")
    print(f"Average Score: {avg_score:.2f}/10")
    print(f"Entries scoring 9.0+: {above_9} ({(above_9/len(entries)*100):.1f}%)")
    print(f"Entries scoring 8.0+: {above_8} ({(above_8/len(entries)*100):.1f}%)")
    print(f"\nReport saved to: {report_file}")
    print(f"Detailed ratings: {ratings_file}")

if __name__ == "__main__":
    main()