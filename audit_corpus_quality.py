#!/usr/bin/env python3
"""
Quality Audit Script for WILLOW Corpus
Identifies salvageable entries and filters out unsalvageable ones
"""

import json
import sys
from datetime import datetime
from typing import Dict, List, Tuple, Any
from collections import defaultdict

class CorpusQualityAuditor:
    def __init__(self):
        self.salvage_thresholds = {
            'empathy': 3.0,  # Minimum empathy to be salvageable
            'action_clarity': 2.0,  # Minimum action clarity
            'legal_safety': 8.0,  # Must maintain legal safety
            'overall': 5.0  # Minimum overall to consider salvaging
        }
        
        self.enhancement_potential = {
            'empathy': 4.0,  # How much we can improve empathy
            'action_clarity': 5.0,  # How much we can improve actions
            'trauma_informed': 5.0,  # How much we can improve trauma approach
            'cultural_sensitivity': 2.0,  # How much we can improve cultural
            'urgency_appropriateness': 1.0  # Minor adjustments only
        }

    def calculate_salvageability(self, entry: Dict) -> Dict[str, Any]:
        """Determine if an entry can be salvaged to 9.0+ quality"""
        quality_metrics = entry.get('metadata', {}).get('quality_metrics', {})
        scores = quality_metrics.get('scores', {})
        overall = quality_metrics.get('overall_score', 0)
        
        # Check minimum thresholds
        if scores.get('legal_safety', 0) < self.salvage_thresholds['legal_safety']:
            return {
                'salvageable': False,
                'reason': 'Legal safety too low',
                'potential_score': overall
            }
        
        if overall < self.salvage_thresholds['overall']:
            return {
                'salvageable': False,
                'reason': 'Overall quality too low',
                'potential_score': overall
            }
        
        # Calculate potential improvement
        potential_scores = {}
        for dimension, current in scores.items():
            max_improvement = self.enhancement_potential.get(dimension, 0)
            potential_scores[dimension] = min(10, current + max_improvement)
        
        # Recalculate potential overall score
        potential_overall = (
            potential_scores.get('empathy', 0) * 0.20 +
            potential_scores.get('action_clarity', 0) * 0.20 +
            potential_scores.get('legal_safety', 0) * 0.25 +
            potential_scores.get('urgency_appropriateness', 0) * 0.15 +
            potential_scores.get('cultural_sensitivity', 0) * 0.10 +
            potential_scores.get('trauma_informed', 0) * 0.10
        )
        
        salvageable = potential_overall >= 9.0
        
        return {
            'salvageable': salvageable,
            'current_score': overall,
            'potential_score': round(potential_overall, 2),
            'improvement_needed': round(potential_overall - overall, 2),
            'dimensions_to_improve': {
                dim: round(potential_scores[dim] - scores.get(dim, 0), 2)
                for dim in potential_scores
                if potential_scores[dim] - scores.get(dim, 0) > 0.5
            }
        }

    def analyze_entry_patterns(self, entry: Dict) -> Dict[str, Any]:
        """Analyze patterns in entry to guide enhancement"""
        messages = entry.get('messages', [])
        patterns = {
            'has_tier1': False,
            'has_tier2': False,
            'message_count': len(messages),
            'avg_response_length': 0,
            'has_reference_number': False,
            'has_symbolic_elements': False,
            'has_grounding': False
        }
        
        willow_messages = [m for m in messages if m.get('role') == 'willow']
        if willow_messages:
            total_length = sum(len(m.get('content', '').split()) for m in willow_messages)
            patterns['avg_response_length'] = total_length / len(willow_messages)
            
            for msg in willow_messages:
                content = msg.get('content', '')
                if msg.get('tier') == 'tier_1':
                    patterns['has_tier1'] = True
                elif msg.get('tier') == 'tier_2':
                    patterns['has_tier2'] = True
                
                if 'WR' in content:
                    patterns['has_reference_number'] = True
                if any(symbol in content for symbol in ['🌊', '🏔️', '🌲', '⚓']):
                    patterns['has_symbolic_elements'] = True
                if 'breath' in content.lower() or 'ground' in content.lower():
                    patterns['has_grounding'] = True
        
        return patterns

    def categorize_improvement_needs(self, entry: Dict, salvage_info: Dict) -> List[str]:
        """Categorize what improvements are needed"""
        needs = []
        dims_to_improve = salvage_info.get('dimensions_to_improve', {})
        
        if dims_to_improve.get('empathy', 0) > 2:
            needs.append('major_empathy_enhancement')
        elif dims_to_improve.get('empathy', 0) > 0.5:
            needs.append('minor_empathy_enhancement')
            
        if dims_to_improve.get('action_clarity', 0) > 3:
            needs.append('major_action_enhancement')
        elif dims_to_improve.get('action_clarity', 0) > 1:
            needs.append('moderate_action_enhancement')
            
        if dims_to_improve.get('trauma_informed', 0) > 3:
            needs.append('deep_trauma_integration')
        elif dims_to_improve.get('trauma_informed', 0) > 1:
            needs.append('basic_trauma_enhancement')
            
        if dims_to_improve.get('cultural_sensitivity', 0) > 1:
            needs.append('cultural_enhancement')
            
        return needs

    def process_corpus(self, input_file: str):
        """Process corpus and create filtered versions"""
        print(f"Auditing corpus quality: {input_file}")
        
        stats = defaultdict(int)
        salvageable_entries = []
        excellent_entries = []
        removed_entries = []
        enhancement_categories = defaultdict(list)
        
        with open(input_file, 'r') as f:
            for line_num, line in enumerate(f, 1):
                if line.strip():
                    try:
                        entry = json.loads(line)
                        stats['total'] += 1
                        
                        # Get current quality
                        current_score = entry.get('metadata', {}).get('quality_metrics', {}).get('overall_score', 0)
                        
                        # Already excellent
                        if current_score >= 9.0:
                            excellent_entries.append(entry)
                            stats['already_excellent'] += 1
                            continue
                        
                        # Check salvageability
                        salvage_info = self.calculate_salvageability(entry)
                        
                        if salvage_info['salvageable']:
                            entry['salvage_info'] = salvage_info
                            entry['patterns'] = self.analyze_entry_patterns(entry)
                            entry['improvement_needs'] = self.categorize_improvement_needs(entry, salvage_info)
                            
                            salvageable_entries.append(entry)
                            stats['salvageable'] += 1
                            
                            # Categorize by improvement needs
                            for need in entry['improvement_needs']:
                                enhancement_categories[need].append(entry['id'])
                        else:
                            removed_entries.append({
                                'id': entry.get('id', f'Line_{line_num}'),
                                'reason': salvage_info['reason'],
                                'current_score': salvage_info['current_score']
                            })
                            stats['removed'] += 1
                            
                        if line_num % 100 == 0:
                            print(f"Processed {line_num} entries...")
                            
                    except Exception as e:
                        print(f"Error processing line {line_num}: {e}")
                        stats['errors'] += 1
        
        # Write filtered corpora
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Excellent entries (no enhancement needed)
        excellent_file = f"willow_corpus_excellent_{timestamp}.jsonl"
        with open(excellent_file, 'w') as f:
            for entry in excellent_entries:
                f.write(json.dumps(entry, ensure_ascii=False) + '\n')
        
        # Salvageable entries (need enhancement)
        salvageable_file = f"willow_corpus_salvageable_{timestamp}.jsonl"
        with open(salvageable_file, 'w') as f:
            for entry in salvageable_entries:
                f.write(json.dumps(entry, ensure_ascii=False) + '\n')
        
        # Generate audit report
        self.generate_audit_report(stats, enhancement_categories, removed_entries, 
                                  excellent_file, salvageable_file, timestamp)
        
        return {
            'excellent_file': excellent_file,
            'salvageable_file': salvageable_file,
            'stats': dict(stats),
            'categories': dict(enhancement_categories)
        }

    def generate_audit_report(self, stats: Dict, categories: Dict, removed: List,
                             excellent_file: str, salvageable_file: str, timestamp: str):
        """Generate detailed audit report"""
        report_file = f"corpus_quality_audit_{timestamp}.txt"
        
        with open(report_file, 'w') as f:
            f.write("WILLOW Corpus Quality Audit Report\n")
            f.write("=" * 60 + "\n\n")
            
            f.write("Summary Statistics:\n")
            f.write(f"- Total Entries: {stats['total']}\n")
            f.write(f"- Already Excellent (9.0+): {stats['already_excellent']} ({stats['already_excellent']/stats['total']*100:.1f}%)\n")
            f.write(f"- Salvageable: {stats['salvageable']} ({stats['salvageable']/stats['total']*100:.1f}%)\n")
            f.write(f"- Removed: {stats['removed']} ({stats['removed']/stats['total']*100:.1f}%)\n")
            f.write(f"- Errors: {stats['errors']}\n\n")
            
            f.write("Enhancement Categories:\n")
            for category, ids in sorted(categories.items(), key=lambda x: len(x[1]), reverse=True):
                f.write(f"- {category}: {len(ids)} entries\n")
            
            f.write("\n\nOutput Files:\n")
            f.write(f"- Excellent entries: {excellent_file}\n")
            f.write(f"- Salvageable entries: {salvageable_file}\n")
            
            f.write("\n\nRemoved Entries (first 20):\n")
            f.write("-" * 40 + "\n")
            for entry in removed[:20]:
                f.write(f"ID: {entry['id']}\n")
                f.write(f"Reason: {entry['reason']}\n")
                f.write(f"Score: {entry['current_score']}\n")
                f.write("-" * 20 + "\n")
            
            # Enhancement recommendations
            f.write("\n\nEnhancement Recommendations:\n")
            f.write("1. Major Empathy Enhancement: Add deeper emotional validation\n")
            f.write("2. Major Action Enhancement: Add specific numbered steps with ETAs\n")
            f.write("3. Deep Trauma Integration: Implement all 5 principles systematically\n")
            f.write("4. Cultural Enhancement: Add communication style variants\n")
            
            f.write(f"\n\nExpected Final Corpus Size: {stats['already_excellent'] + stats['salvageable']}\n")
            f.write(f"Expected Average Quality: 9.2+\n")
        
        print(f"\nAudit report saved: {report_file}")

if __name__ == "__main__":
    auditor = CorpusQualityAuditor()
    
    # Use the latest quality metrics corpus
    input_file = sys.argv[1] if len(sys.argv) > 1 else "willow_corpus_quality_metrics_20250624_022548.jsonl"
    
    results = auditor.process_corpus(input_file)
    
    print(f"\nAudit complete!")
    print(f"Excellent entries: {results['excellent_file']}")
    print(f"Salvageable entries: {results['salvageable_file']}")
    print(f"Total retained: {results['stats']['already_excellent'] + results['stats']['salvageable']}")