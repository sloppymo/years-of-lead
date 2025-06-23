#!/usr/bin/env python3
"""
Fix overpromising language in Willow dataset entries.
Based on legal liability audit findings.
"""

import json
import re
from typing import Dict, List, Tuple, Optional
import argparse

class WillowOverpromisingFixer:
    """Identifies and fixes overpromising language patterns in Willow responses."""
    
    def __init__(self):
        # High-risk phrases that need immediate replacement
        self.high_risk_patterns = {
            # Promises of immediate action
            r"immediately|right now|ASAP|as quickly as possible prioritized": "as soon as possible",
            r"will fix this|we'll fix this|I'll fix this": "we'll work to address this",
            r"will be fixed|will be resolved": "should be addressed",
            r"I'll handle|I'll take care of|Let me handle": "I'll help with",
            r"we will ensure|I'll ensure|ensure you": "we'll work to",
            r"I'll make sure|make sure|making sure": "I'll do my best to help",
            r"guaranteed|definitely|absolutely|certainly": "likely",
            r"promise|I promise|we promise": "we'll try",
            
            # Legal judgments
            r"is illegal|that's illegal|violates the law": "may not comply with regulations",
            r"by law|legally required|law requires": "regulations typically require",
            r"your rights|tenant rights|legal rights": "typical tenant protections",
            r"violation|violating|violated": "potential issue",
            
            # Timeline commitments
            r"within (\d+) hours?|in (\d+) hours?": "as soon as possible",
            r"within (\d+) minutes?|in (\d+) minutes?": "shortly",
            r"today|tonight|tomorrow": "soon",
            r"24-48 hours|24 hours|48 hours": "as soon as possible",
            
            # Financial commitments
            r"we'll cover|we will cover|cover the cost": "we can explore coverage options",
            r"reimburse|reimbursement|refund": "potential reimbursement",
            r"waive fees|waiving fees|no fees": "fee review possible",
            r"compensation|compensate": "we'll review options",
            
            # Absolute safety assurances
            r"you're safe now|you'll be safe|keep you safe": "we're working on your safety",
            r"never happen again|won't happen again": "we'll work to prevent this",
            r"protected|protection guaranteed": "protection measures in place",
        }
        
        # Moderate risk phrases
        self.moderate_risk_patterns = {
            r"should be|will be|going to be": "may be",
            r"I can|we can": "I can help explore",
            r"available|ready": "potentially available",
            r"scheduled|confirmed": "tentatively scheduled",
            r"approved|authorized": "under review",
            r"initiated|started|begun": "being processed",
            r"your (\w+) is protected": "we're working to protect your \\1",
        }
        
        # Phrases to add for safety
        self.safety_additions = [
            "subject to availability",
            "pending review",
            "typically",
            "in most cases",
            "we'll do our best",
            "I'll help coordinate",
            "let me check on that",
            "I'll look into",
            "options include",
            "possible solutions",
        ]
        
        # Good containment phrases to preserve
        self.good_phrases = [
            "let me check",
            "I'll help",
            "we'll work on",
            "under review",
            "being processed",
            "I'll do my best",
            "typically available",
            "should be able to",
            "we'll explore",
            "options available",
        ]
    
    def calculate_risk_score(self, text: str) -> Tuple[int, List[str]]:
        """Calculate risk score (1-10) and identify problematic phrases."""
        score = 10  # Start with perfect score
        issues = []
        
        # Check for high-risk patterns (score 1-3)
        for pattern, _ in self.high_risk_patterns.items():
            if re.search(pattern, text, re.IGNORECASE):
                score = min(score, 3)
                issues.append(f"High-risk: {pattern}")
        
        # Check for moderate patterns (score 4-6)
        for pattern, _ in self.moderate_risk_patterns.items():
            if re.search(pattern, text, re.IGNORECASE) and score > 3:
                score = min(score, 6)
                issues.append(f"Moderate: {pattern}")
        
        # Check for good containment (boost score)
        good_count = sum(1 for phrase in self.good_phrases if phrase in text.lower())
        if good_count > 0 and score > 6:
            score = min(10, score + good_count)
        
        return score, issues
    
    def fix_text(self, text: str, aggressive: bool = False) -> str:
        """Fix overpromising language in text."""
        fixed = text
        
        # Apply high-risk replacements
        for pattern, replacement in self.high_risk_patterns.items():
            fixed = re.sub(pattern, replacement, fixed, flags=re.IGNORECASE)
        
        # Apply moderate replacements if aggressive
        if aggressive:
            for pattern, replacement in self.moderate_risk_patterns.items():
                fixed = re.sub(pattern, replacement, fixed, flags=re.IGNORECASE)
        
        # Add safety language if not already present
        if not any(safety in fixed.lower() for safety in ["subject to", "pending", "typically", "may"]):
            # Add to end of appropriate sentences
            if fixed.endswith('.'):
                fixed = fixed[:-1] + ", subject to availability."
        
        return fixed
    
    def process_entry(self, entry: Dict, aggressive: bool = False) -> Tuple[Dict, bool, List[str]]:
        """Process a single entry and return fixed version."""
        modified = False
        all_issues = []
        fixed_entry = entry.copy()
        
        # Process all messages
        if 'messages' in entry:
            fixed_messages = []
            for msg in entry['messages']:
                if msg.get('role') == 'willow':
                    original = msg.get('content', '')
                    score, issues = self.calculate_risk_score(original)
                    
                    if score < 7 or (aggressive and score < 9):
                        fixed = self.fix_text(original, aggressive)
                        if fixed != original:
                            modified = True
                            fixed_msg = msg.copy()
                            fixed_msg['content'] = fixed
                            fixed_msg['original_content'] = original
                            fixed_msg['risk_score'] = score
                            fixed_messages.append(fixed_msg)
                            all_issues.extend(issues)
                        else:
                            fixed_messages.append(msg)
                    else:
                        fixed_messages.append(msg)
                else:
                    fixed_messages.append(msg)
            
            fixed_entry['messages'] = fixed_messages
        
        return fixed_entry, modified, all_issues
    
    def analyze_file(self, filename: str) -> Dict:
        """Analyze a file and return statistics."""
        stats = {
            'total_entries': 0,
            'high_risk_entries': 0,
            'moderate_risk_entries': 0,
            'safe_entries': 0,
            'risk_distribution': {},
            'common_issues': {},
            'sample_problems': []
        }
        
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    entry = json.loads(line)
                    stats['total_entries'] += 1
                    
                    # Analyze all Willow messages
                    entry_score = 10
                    entry_issues = []
                    
                    if 'messages' in entry:
                        for msg in entry['messages']:
                            if msg.get('role') == 'willow':
                                score, issues = self.calculate_risk_score(msg.get('content', ''))
                                entry_score = min(entry_score, score)
                                entry_issues.extend(issues)
                    
                    # Categorize
                    if entry_score <= 3:
                        stats['high_risk_entries'] += 1
                        if len(stats['sample_problems']) < 5:
                            stats['sample_problems'].append({
                                'id': entry.get('id'),
                                'score': entry_score,
                                'issues': entry_issues[:3]  # First 3 issues
                            })
                    elif entry_score <= 6:
                        stats['moderate_risk_entries'] += 1
                    else:
                        stats['safe_entries'] += 1
                    
                    # Track distribution
                    stats['risk_distribution'][entry_score] = stats['risk_distribution'].get(entry_score, 0) + 1
                    
                    # Track common issues
                    for issue in entry_issues:
                        stats['common_issues'][issue] = stats['common_issues'].get(issue, 0) + 1
        
        return stats
    
    def fix_file(self, input_file: str, output_file: str, aggressive: bool = False, 
                 target_ids: Optional[List[str]] = None) -> Dict:
        """Fix overpromising in a file."""
        stats = {
            'processed': 0,
            'modified': 0,
            'skipped': 0,
            'errors': 0
        }
        
        with open(input_file, 'r', encoding='utf-8') as f_in, \
             open(output_file, 'w', encoding='utf-8') as f_out:
            
            for line in f_in:
                if line.strip():
                    try:
                        entry = json.loads(line)
                        entry_id = entry.get('id', '')
                        
                        # Skip if targeting specific IDs and this isn't one
                        if target_ids and entry_id not in target_ids:
                            f_out.write(line)
                            stats['skipped'] += 1
                            continue
                        
                        fixed_entry, modified, issues = self.process_entry(entry, aggressive)
                        stats['processed'] += 1
                        
                        if modified:
                            stats['modified'] += 1
                            # Add metadata about fixes
                            fixed_entry['liability_fixes'] = {
                                'fixed': True,
                                'issues_found': len(issues),
                                'fix_date': '2024-01-15'
                            }
                        
                        f_out.write(json.dumps(fixed_entry, ensure_ascii=False) + '\n')
                        
                    except Exception as e:
                        print(f"Error processing entry: {e}")
                        stats['errors'] += 1
                        f_out.write(line)  # Write original on error
        
        return stats


def main():
    parser = argparse.ArgumentParser(description='Fix overpromising in Willow dataset')
    parser.add_argument('input_file', help='Input JSONL file')
    parser.add_argument('output_file', help='Output JSONL file')
    parser.add_argument('--analyze-only', action='store_true', help='Only analyze, don\'t fix')
    parser.add_argument('--aggressive', action='store_true', help='Apply aggressive fixes')
    parser.add_argument('--target-ids', nargs='+', help='Only fix specific entry IDs')
    
    args = parser.parse_args()
    
    fixer = WillowOverpromisingFixer()
    
    if args.analyze_only:
        print("Analyzing file for overpromising language...")
        stats = fixer.analyze_file(args.input_file)
        
        print(f"\nAnalysis Results:")
        print(f"Total entries: {stats['total_entries']}")
        print(f"High risk (1-3): {stats['high_risk_entries']} ({stats['high_risk_entries']/stats['total_entries']*100:.1f}%)")
        print(f"Moderate risk (4-6): {stats['moderate_risk_entries']} ({stats['moderate_risk_entries']/stats['total_entries']*100:.1f}%)")
        print(f"Safe (7-10): {stats['safe_entries']} ({stats['safe_entries']/stats['total_entries']*100:.1f}%)")
        
        print(f"\nRisk Score Distribution:")
        for score in sorted(stats['risk_distribution'].keys()):
            count = stats['risk_distribution'][score]
            print(f"  Score {score}: {count} entries")
        
        print(f"\nMost Common Issues:")
        for issue, count in sorted(stats['common_issues'].items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"  {issue}: {count} occurrences")
        
        print(f"\nSample High-Risk Entries:")
        for problem in stats['sample_problems']:
            print(f"  {problem['id']} (score: {problem['score']})")
            for issue in problem['issues']:
                print(f"    - {issue}")
    
    else:
        print(f"Fixing overpromising language...")
        print(f"Mode: {'Aggressive' if args.aggressive else 'Standard'}")
        if args.target_ids:
            print(f"Targeting IDs: {args.target_ids}")
        
        stats = fixer.fix_file(args.input_file, args.output_file, 
                              aggressive=args.aggressive, 
                              target_ids=args.target_ids)
        
        print(f"\nProcessing Complete:")
        print(f"Processed: {stats['processed']}")
        print(f"Modified: {stats['modified']}")
        print(f"Skipped: {stats['skipped']}")
        print(f"Errors: {stats['errors']}")
        print(f"\nOutput written to: {args.output_file}")


if __name__ == "__main__":
    import sys
    # If no command line args, run a test
    if len(sys.argv) == 1:
        # Test the fixer
        fixer = WillowOverpromisingFixer()
        
        test_texts = [
            "I'll fix this immediately and ensure it never happens again.",
            "This is illegal and we'll cover all costs right away.",
            "You're safe now and I'll make sure of it.",
            "Let me check what options are available.",
            "We'll work to address this as soon as possible.",
        ]
        
        print("Testing overpromising detection and fixes:\n")
        for text in test_texts:
            score, issues = fixer.calculate_risk_score(text)
            fixed = fixer.fix_text(text, aggressive=True)
            print(f"Original: {text}")
            print(f"Score: {score}/10")
            print(f"Issues: {issues}")
            print(f"Fixed: {fixed}")
            print()
    else:
        main()