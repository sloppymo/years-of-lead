#!/usr/bin/env python3
"""
Scan Willow corpus for lower quality entries based on multiple criteria.
"""

import json
import re
from typing import Dict, List, Tuple

def load_corpus(filename: str) -> List[Dict]:
    """Load the corpus file."""
    entries = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            try:
                entry = json.loads(line.strip())
                entries.append(entry)
            except json.JSONDecodeError as e:
                print(f"Error parsing line {line_num}: {e}")
    return entries

def check_quality_issues(entry: Dict) -> List[str]:
    """Check for various quality issues in an entry."""
    issues = []
    
    # 1. Check for overpromising language
    overpromising_patterns = [
        r'\bwill\s+ensure\b', r'\bguarantee\b', r'\bpromise\b', 
        r'\bdefinitely\s+will\b', r'\bwill\s+definitely\b',
        r'\bwill\s+make\s+sure\b', r'\bwill\s+fix\b',
        r'\bwill\s+resolve\b', r'\bwill\s+get\s+this\s+sorted\b'
    ]
    
    # 2. Check for inappropriate endearments
    endearment_patterns = [
        r'\bhoney\b', r'\bsweetie\b', r'\bdarling\b', r'\bdear\b',
        r'\bhun\b', r'\bsweetheart\b', r'\blove\b'
    ]
    
    # 3. Check for missing trauma-informed elements
    trauma_indicators = [
        'arousal', 'capacity', 'tier_1', 'tier_2', 
        'validation', 'co-regulation', 'grounding'
    ]
    
    # 4. Check message content
    all_messages = []
    if 'messages' in entry:
        for msg in entry['messages']:
            if 'content' in msg:
                all_messages.append(msg['content'].lower())
    
    combined_text = ' '.join(all_messages)
    
    # Check for overpromising
    for pattern in overpromising_patterns:
        if re.search(pattern, combined_text, re.IGNORECASE):
            issues.append(f"Overpromising language: {pattern}")
    
    # Check for endearments
    for pattern in endearment_patterns:
        if re.search(pattern, combined_text, re.IGNORECASE):
            issues.append(f"Inappropriate endearment: {pattern}")
    
    # 5. Check for too short responses
    if len(all_messages) > 0:
        avg_length = sum(len(msg) for msg in all_messages) / len(all_messages)
        if avg_length < 50:
            issues.append("Very short responses")
    
    # 6. Check for missing tier progression
    has_tier_1 = 'tier_1' in combined_text or 'tier 1' in combined_text
    has_tier_2 = 'tier_2' in combined_text or 'tier 2' in combined_text
    
    # 7. Check for formulaic/repetitive language
    formulaic_phrases = [
        "i hear how", "that sounds really", "it makes sense that",
        "i understand this is", "thank you for sharing"
    ]
    formulaic_count = sum(1 for phrase in formulaic_phrases if phrase in combined_text)
    if formulaic_count > 3:
        issues.append(f"Highly formulaic language ({formulaic_count} standard phrases)")
    
    # 8. Check for missing emotional validation
    validation_words = ['valid', 'understand', 'hear', 'acknowledge', 'recognize']
    has_validation = any(word in combined_text for word in validation_words)
    if not has_validation and len(all_messages) > 2:
        issues.append("Missing emotional validation")
    
    # 9. Check for legal liability issues
    liability_phrases = [
        "we'll handle", "we'll take care", "don't worry about",
        "leave it to us", "we've got this", "count on us"
    ]
    for phrase in liability_phrases:
        if phrase in combined_text:
            issues.append(f"Liability concern: '{phrase}'")
    
    # 10. Check arousal/capacity metrics
    if 'initial_state' in entry:
        arousal = entry['initial_state'].get('arousal', 0)
        capacity = entry['initial_state'].get('capacity', 0)
        
        # High arousal without appropriate response
        if arousal > 8.0 and not any(word in combined_text for word in ['breathe', 'ground', 'safe', 'moment']):
            issues.append(f"High arousal ({arousal}) without grounding techniques")
        
        # Low capacity without appropriate support
        if capacity < 3.0 and not any(word in combined_text for word in ['simple', 'step', 'one thing', 'small']):
            issues.append(f"Low capacity ({capacity}) without simplified approach")
    
    return issues

def calculate_quality_score(issues: List[str]) -> int:
    """Calculate a quality score from 1-10 based on issues found."""
    # Start with perfect score
    score = 10
    
    # Deduct points for different issue types
    for issue in issues:
        if 'Overpromising' in issue:
            score -= 2
        elif 'endearment' in issue:
            score -= 3
        elif 'Liability' in issue:
            score -= 2
        elif 'formulaic' in issue:
            score -= 1
        elif 'validation' in issue:
            score -= 1
        elif 'arousal' in issue or 'capacity' in issue:
            score -= 1.5
        else:
            score -= 0.5
    
    return int(max(1, score))  # Minimum score of 1

def main():
    print("Scanning Willow corpus for quality issues...\n")
    
    entries = load_corpus('willow_corpus_final_clean.jsonl')
    print(f"Loaded {len(entries)} entries\n")
    
    low_quality_entries = []
    quality_distribution = {i: 0 for i in range(1, 11)}
    
    for entry in entries:
        issues = check_quality_issues(entry)
        score = calculate_quality_score(issues)
        quality_distribution[int(score)] += 1
        
        if score < 9:
            low_quality_entries.append({
                'id': entry.get('id', 'Unknown'),
                'score': score,
                'issues': issues,
                'scenario': entry.get('scenario', 'Unknown scenario')
            })
    
    # Sort by score (lowest first)
    low_quality_entries.sort(key=lambda x: x['score'])
    
    # Print summary
    print("Quality Score Distribution:")
    for score in range(10, 0, -1):
        count = quality_distribution[score]
        bar = '█' * (count // 10) + '▄' * ((count % 10) // 5)
        print(f"Score {score:2d}: {count:4d} entries {bar}")
    
    print(f"\nTotal entries with score < 9: {len(low_quality_entries)}")
    
    # Show worst entries
    print("\nLowest Quality Entries:")
    for i, entry in enumerate(low_quality_entries[:20]):  # Show top 20 worst
        print(f"\n{i+1}. {entry['id']} (Score: {entry['score']:.1f})")
        print(f"   Scenario: {entry['scenario']}")
        print("   Issues:")
        for issue in entry['issues'][:3]:  # Show first 3 issues
            print(f"   - {issue}")
        if len(entry['issues']) > 3:
            print(f"   ... and {len(entry['issues']) - 3} more issues")
    
    # Save detailed report
    with open('corpus_quality_report.json', 'w') as f:
        json.dump({
            'summary': {
                'total_entries': len(entries),
                'low_quality_count': len(low_quality_entries),
                'quality_distribution': quality_distribution
            },
            'low_quality_entries': low_quality_entries
        }, f, indent=2)
    
    print(f"\nDetailed report saved to corpus_quality_report.json")

if __name__ == "__main__":
    main()