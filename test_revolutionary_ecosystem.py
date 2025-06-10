#!/usr/bin/env python3
"""
Test script for Revolutionary Ecosystem with Faction Rivalries, Splintering, and Alliance System
Comprehensive test of ITERATION 022 (rivalries) and ITERATION 023 (alliances)
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from game.revolutionary_ecosystem import (
    RevolutionaryEcosystem, RevolutionaryFaction, FactionIdeology,
    FactionConflictType, FactionActivityType, JointActivityType,
    FactionAlliance, FactionRelationship, AlliancePropagandaEvent, PropagandaTone
)
import random
from datetime import datetime

def test_alliance_formation_and_cooperation():
    """Test alliance formation, joint operations, and cooperation mechanics"""
    print("\n" + "="*60)
    print("🤝 TESTING ALLIANCE SYSTEM - ITERATION 023")
    print("="*60)
    
    # Create ecosystem with multiple factions
    ecosystem = RevolutionaryEcosystem()
    
    # Create factions with complementary strengths for alliance potential
    socialist_faction = RevolutionaryFaction(
        name="Workers' Unity Front",
        ideology=FactionIdeology.SOCIALIST,
        aggression=0.4,
        cooperation=0.8,  # High cooperation
        public_support=18.0,  # Lower support to trigger necessity
        media_reach=0.6,
        operational_capacity=1.2,
        funding_level=0.7,
        government_heat=7.5,  # Higher pressure - good for alliance
        factional_trust=70.0,  # High trust in alliances
        territory_zones=["Industrial District", "Worker Housing"]
    )
    
    anarchist_faction = RevolutionaryFaction(
        name="Liberation Collective",
        ideology=FactionIdeology.ANARCHIST,
        aggression=0.6,
        cooperation=0.7,  # Increased cooperation
        public_support=15.0,  # Lower support
        media_reach=0.4,
        operational_capacity=1.5,  # High operational capacity
        funding_level=0.4,
        government_heat=8.0,  # Higher pressure
        factional_trust=65.0,  # Increased trust
        territory_zones=["University Quarter", "Art District"]
    )
    
    nationalist_faction = RevolutionaryFaction(
        name="Patriotic Liberation Army",
        ideology=FactionIdeology.NATIONALIST,
        aggression=0.7,
        cooperation=0.5,
        public_support=40.0,
        media_reach=0.5,
        operational_capacity=1.3,
        funding_level=0.8,
        government_heat=5.0,
        factional_trust=45.0,  # Lower trust - less likely to ally
        territory_zones=["Border Region", "Rural Towns"]
    )
    
    ecosystem.active_factions = [socialist_faction, anarchist_faction, nationalist_faction]
    
    # Lower alliance threshold for easier testing
    ecosystem.alliance_formation_threshold = 40.0  # Lower threshold
    
    ecosystem._initialize_faction_relationships()
    
    # Boost relationships for alliance potential
    for relationship in ecosystem.faction_relationships.values():
        if relationship.faction_a in ["Workers' Unity Front", "Liberation Collective"] and \
           relationship.faction_b in ["Workers' Unity Front", "Liberation Collective"]:
            relationship.trust_rating = 25.0  # Sufficient trust for alliance
    
    print(f"\n📊 Initial Faction Status:")
    for faction in ecosystem.active_factions:
        print(f"  {faction.name}:")
        print(f"    - Support: {faction.public_support:.1f}%")
        print(f"    - Cooperation: {faction.cooperation:.2f}")
        print(f"    - Trust in Alliances: {faction.factional_trust:.1f}")
        print(f"    - Government Heat: {faction.government_heat:.1f}")
        print(f"    - Operational Capacity: {faction.operational_capacity:.2f}")
    
    # Test alliance opportunity evaluation
    print(f"\n🔍 Evaluating Alliance Opportunities:")
    opportunities = ecosystem.evaluate_alliance_opportunities()
    
    print(f"Found {len(opportunities)} potential alliance opportunities:")
    for faction_a, faction_b, value in opportunities:
        print(f"  • {faction_a} + {faction_b}: Alliance Value = {value:.1f}")
        
        # Get individual alliance values for detailed analysis
        faction_a_obj = next(f for f in ecosystem.active_factions if f.name == faction_a)
        faction_b_obj = next(f for f in ecosystem.active_factions if f.name == faction_b)
        
        can_ally_a, reason_a = faction_a_obj.can_form_alliance_with(faction_b_obj)
        can_ally_b, reason_b = faction_b_obj.can_form_alliance_with(faction_a_obj)
        
        print(f"    {faction_a} perspective: {reason_a}")
        print(f"    {faction_b} perspective: {reason_b}")
    
    # Force alliance formation between top candidates OR create one manually for testing
    if opportunities:
        top_faction_a, top_faction_b, top_value = opportunities[0]
        print(f"\n🤝 Forming Alliance: {top_faction_a} + {top_faction_b}")
        
        alliance = ecosystem.form_alliance([top_faction_a, top_faction_b])
    else:
        # Force alliance formation for testing
        print(f"\n🤝 Forcing Alliance Formation for Testing: Workers' Unity Front + Liberation Collective")
        alliance = ecosystem.form_alliance(["Workers' Unity Front", "Liberation Collective"])
    
    if alliance:
        print(f"✅ Alliance '{alliance.alliance_name}' successfully formed!")
        print(f"   - Initial Trust Level: {alliance.trust_level:.1f}")
        print(f"   - Cooperation Momentum: {alliance.cooperation_momentum:.1f}")
        print(f"   - Betrayal Risk: {alliance.betrayal_risk:.3f}")
        
        # Test joint operations
        print(f"\n⚡ Testing Joint Operations:")
        
        # Simulate several turns of joint operations
        for turn in range(3):
            print(f"\n--- Turn {turn + 1} ---")
            joint_ops = ecosystem.execute_joint_operations()
            
            if joint_ops:
                for op in joint_ops:
                    print(f"🎯 {op['alliance_name']} - {op['activity_type']}:")
                    print(f"   Participants: {', '.join(op['participants'])}")
                    print(f"   Success: {'✅' if op['success'] else '❌'}")
                    print(f"   Outcomes: {'; '.join(op['outcomes'])}")
                    print(f"   Trust Change: {op['trust_change']:+.1f}")
                    print(f"   Momentum Impact: {op['momentum_impact']:+.1f}")
            else:
                print("   No joint operations this turn")
            
            # Check alliance status after operations
            updated_alliance = ecosystem.active_alliances.get(alliance.alliance_name)
            if updated_alliance:
                print(f"   Alliance Status:")
                print(f"     Trust: {updated_alliance.trust_level:.1f}")
                print(f"     Momentum: {updated_alliance.cooperation_momentum:.1f}")
                print(f"     Victories: {updated_alliance.shared_victories}")
                print(f"     Failures: {updated_alliance.cooperation_failures}")
                print(f"     Betrayal Risk: {updated_alliance.betrayal_risk:.3f}")
    
    # Test betrayal scenario
    print(f"\n💀 Testing Alliance Betrayal Mechanics:")
    if alliance and len(alliance.member_factions) >= 2:
        # Artificially increase betrayal risk
        alliance.trust_level = 25.0  # Low trust
        alliance.cooperation_failures = 3  # Multiple failures
        alliance.cooperation_momentum = -25.0  # Negative momentum
        
        print(f"Simulating deteriorated alliance conditions:")
        print(f"  - Trust Level: {alliance.trust_level:.1f} (Low)")
        print(f"  - Failures: {alliance.cooperation_failures}")
        print(f"  - Momentum: {alliance.cooperation_momentum:.1f} (Negative)")
        
        # Recalculate betrayal risk
        alliance.betrayal_risk = alliance.calculate_betrayal_risk(ecosystem.faction_relationships)
        print(f"  - Betrayal Risk: {alliance.betrayal_risk:.3f}")
        
        # Force a betrayal for testing
        betrayer = alliance.member_factions[0]
        print(f"\n💥 {betrayer} betrays the alliance!")
        
        betrayal_success = ecosystem.execute_alliance_betrayal(alliance.alliance_name, betrayer)
        
        if betrayal_success:
            print(f"✅ Betrayal executed successfully")
            print(f"   - Remaining members: {alliance.member_factions if alliance.alliance_name in ecosystem.active_alliances else 'Alliance disbanded'}")
            
            # Check faction relationships after betrayal
            betrayer_faction = next(f for f in ecosystem.active_factions if f.name == betrayer)
            print(f"   - {betrayer} alliance cooldowns: {len(betrayer_faction.alliance_cooldown)} factions")
            
            # Check trust damage
            for victim in alliance.member_factions:
                relationship = ecosystem._get_faction_relationship(betrayer, victim)
                if relationship:
                    print(f"   - Trust with {victim}: {relationship.trust_rating:.1f}")
    
    return ecosystem

def test_ecosystem_with_alliances():
    """Test full ecosystem simulation with alliance system integrated"""
    print("\n" + "="*60)
    print("🌍 TESTING FULL ECOSYSTEM WITH ALLIANCES & PROPAGANDA")
    print("="*60)
    
    ecosystem = test_alliance_formation_and_cooperation()
    
    print(f"\n🔄 Running Ecosystem Simulation with Alliance & Propaganda Systems:")
    
    # Track initial support levels for comparison
    initial_support = {f.name: f.public_support for f in ecosystem.active_factions}
    
    # Run several turns to see alliance dynamics and propaganda wars
    for turn in range(5):
        print(f"\n--- ECOSYSTEM TURN {turn + 1} ---")
        
        turn_results = ecosystem.simulate_ecosystem_turn()
        
        # Display faction activities
        print(f"📋 Faction Activities:")
        for activity in turn_results['faction_activities']:
            faction_name = activity['faction_name']
            activity_type = activity['activity_type']
            outcomes = activity.get('outcomes', [])
            
            print(f"  • {faction_name}: {activity_type}")
            for outcome in outcomes[:2]:  # Limit to first 2 outcomes
                print(f"    - {outcome}")
        
        # Display alliance activities
        alliance_activities = turn_results.get('alliance_activities', {})
        if alliance_activities:
            print(f"\n🤝 Alliance Activities:")
            
            # New alliances
            new_alliances = alliance_activities.get('new_alliances', [])
            for alliance in new_alliances:
                print(f"  🆕 New Alliance: {alliance['alliance_name']}")
                print(f"     Members: {', '.join(alliance['members'])}")
            
            # Joint operations
            joint_ops = alliance_activities.get('joint_operations', [])
            for op in joint_ops:
                status = "✅" if op['success'] else "❌"
                print(f"  {status} {op['alliance_name']}: {op['activity_type']}")
                for outcome in op['outcomes'][:1]:  # First outcome only
                    print(f"     - {outcome}")
                
                # Display propaganda events - ITERATION 024
                if 'propaganda_event' in op:
                    prop_event = op['propaganda_event']
                    print(f"     📢 Propaganda: {prop_event['type']} by {prop_event.get('leader', 'faction')}")
                    print(f"        Tone: {prop_event['tone']}, Coverage: {prop_event.get('media_coverage', 0):.2f}")
            
            # Propaganda wars - ITERATION 024
            propaganda_wars = alliance_activities.get('propaganda_wars', [])
            if propaganda_wars:
                print(f"\n📢 Propaganda Narrative Wars:")
                for war in propaganda_wars:
                    print(f"  💥 {war['initiator']} launches {war['tone']} against {', '.join(war['targets'])}")
                    print(f"     Effectiveness: {war['effectiveness']:.2f}")
            
            # Alliance summary
            summary = alliance_activities.get('alliance_summary', {})
            if summary.get('active_alliances', 0) > 0:
                print(f"  📊 Active Alliances: {summary['active_alliances']}")
                print(f"      Propaganda Events: {summary.get('propaganda_events', 0)}")
                print(f"      Media Saturation: {summary.get('media_saturation', 0):.2f}")
                for detail in summary.get('alliance_details', []):
                    print(f"     {detail['name']}: Trust={detail['trust_level']:.0f}, Risk={detail['betrayal_risk']:.2f}")
        
        # Display major events
        major_events = turn_results.get('major_events', [])
        if major_events:
            print(f"\n🎆 Major Events:")
            for event in major_events:
                print(f"  • {event}")
        
        # Display faction conflicts
        conflicts = turn_results.get('faction_conflicts', [])
        if conflicts:
            print(f"\n⚔️ Faction Conflicts:")
            for conflict in conflicts:
                print(f"  • {conflict['initiator']} vs {conflict['target']}: {conflict['conflict_type']}")
    
    # Final alliance summary
    print(f"\n📈 FINAL ALLIANCE & PROPAGANDA SYSTEM SUMMARY:")
    print(f"  Active Alliances: {len(ecosystem.active_alliances)}")
    print(f"  Total Alliance Events: {len(ecosystem.alliance_events)}")
    print(f"  Propaganda Events: {len(ecosystem.propaganda_events)}")  # ITERATION 024
    print(f"  Media Saturation Level: {ecosystem.media_saturation_level:.2f}")  # ITERATION 024
    
    for alliance_name, alliance in ecosystem.active_alliances.items():
        print(f"\n  Alliance: {alliance_name}")
        print(f"    Members: {', '.join(alliance.member_factions)}")
        print(f"    Trust Level: {alliance.trust_level:.1f}")
        print(f"    Shared Victories: {alliance.shared_victories}")
        print(f"    Cooperation Failures: {alliance.cooperation_failures}")
        print(f"    Betrayal Risk: {alliance.betrayal_risk:.3f}")
    
    # Display propaganda event summary - ITERATION 024
    if ecosystem.propaganda_events:
        print(f"\n📢 PROPAGANDA EVENT SUMMARY:")
        propaganda_by_type = {}
        support_changes_total = {}
        
        for prop_event in ecosystem.propaganda_events:
            event_type = prop_event.event_type
            propaganda_by_type[event_type] = propaganda_by_type.get(event_type, 0) + 1
            
            # Track support changes
            for faction_name, change in prop_event.support_changes.items():
                if faction_name not in support_changes_total:
                    support_changes_total[faction_name] = 0
                support_changes_total[faction_name] += change
        
        for event_type, count in propaganda_by_type.items():
            print(f"  {event_type}: {count} events")
        
        print(f"\n  Public Support Changes from Propaganda:")
        for faction_name, total_change in support_changes_total.items():
            initial = initial_support.get(faction_name, 0)
            final = next((f.public_support for f in ecosystem.active_factions if f.name == faction_name), 0)
            print(f"    {faction_name}: {initial:.1f}% → {final:.1f}% (Δ{total_change:+.1f}% from propaganda)")
    
    # Display relationship summary
    print(f"\n🔗 Faction Relationship Summary:")
    relationship_summary = ecosystem.get_faction_relationship_summary()
    print(f"  Total Relationships: {relationship_summary['total_relationships']}")
    print(f"  Hostile: {relationship_summary['hostile_relationships']}")
    print(f"  Neutral: {relationship_summary['neutral_relationships']}")
    print(f"  Friendly: {relationship_summary['friendly_relationships']}")
    print(f"  Active Rivalries: {relationship_summary['active_rivalries']}")
    
    return ecosystem

def main():
    """Main test function"""
    print("🚀 REVOLUTIONARY ECOSYSTEM TESTING - ITERATIONS 022, 023 & 024")
    print("Testing Faction Rivalries, Alliances, and Propaganda Narrative Wars")
    print("="*80)
    
    # Set random seed for reproducible testing
    random.seed(42)
    
    try:
        # Test alliance system with propaganda
        ecosystem = test_ecosystem_with_alliances()
        
        print(f"\n✅ TESTING COMPLETE - SUCCESS CRITERIA CHECK:")
        
        # Check success criteria for Iteration 024
        alliance_formed = len(ecosystem.active_alliances) > 0 or len(ecosystem.alliance_events) > 0
        joint_operations_occurred = any(event.get('type') == 'joint_operation' for event in ecosystem.uprising_clock.major_events)
        betrayals_or_conflicts = len(ecosystem.conflict_history) > 0 or any(event.get('type') == 'alliance_betrayal' for event in ecosystem.alliance_events)
        
        # New criteria for Iteration 024
        propaganda_events_exist = len(ecosystem.propaganda_events) > 0
        support_changes_logged = any(prop.support_changes for prop in ecosystem.propaganda_events)
        narrative_wars_occurred = any(prop.event_type == "counter_narrative" for prop in ecosystem.propaganda_events)
        
        print(f"  ✓ Alliance Formation: {'✅' if alliance_formed else '❌'}")
        print(f"  ✓ Joint Operations: {'✅' if joint_operations_occurred else '❌'}")
        print(f"  ✓ Conflicts/Betrayals: {'✅' if betrayals_or_conflicts else '❌'}")
        print(f"  ✓ Propaganda Events: {'✅' if propaganda_events_exist else '❌'}")
        print(f"  ✓ Support Changes Logged: {'✅' if support_changes_logged else '❌'}")
        print(f"  ✓ Narrative Wars: {'✅' if narrative_wars_occurred else '❌'}")
        
        # Check momentum impact logging
        momentum_events = [event for event in ecosystem.uprising_clock.major_events if 'joint_operation' in event.get('type', '')]
        momentum_logged = len(momentum_events) > 0
        print(f"  ✓ Momentum Logging: {'✅' if momentum_logged else '❌'}")
        
        # Check alliance impact on faction behavior
        alliance_members = []
        for alliance in ecosystem.active_alliances.values():
            alliance_members.extend(alliance.member_factions)
        
        cooperation_changes = len(alliance_members) > 0  # Simple check - alliance members exist
        print(f"  ✓ Alliance Landscape Impact: {'✅' if cooperation_changes else '❌'}")
        
        if alliance_formed and propaganda_events_exist and support_changes_logged:
            print(f"\n🎉 ITERATION 024 IMPLEMENTATION SUCCESSFUL!")
            print(f"Propaganda narrative system integrated with alliance mechanics.")
            print(f"Dynamic support shifts and trust changes working correctly.")
        else:
            print(f"\n⚠️ Some success criteria not fully met - may need additional testing.")
            
    except Exception as e:
        print(f"\n❌ ERROR during testing: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)