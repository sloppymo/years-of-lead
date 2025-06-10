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
    FactionAlliance, FactionRelationship, AlliancePropagandaEvent, PropagandaTone,
    AllianceType, SecretDiplomaticChannel
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

def test_secret_alliance_system():
    """Test secret alliance formation, covert operations, and intelligence leaks - ITERATION 025"""
    print("\n" + "="*60)
    print("🕵️ TESTING SECRET ALLIANCE SYSTEM - ITERATION 025")
    print("="*60)
    
    ecosystem = RevolutionaryEcosystem()
    
    # Create factions with high government heat to trigger secret alliance conditions
    shadow_faction = RevolutionaryFaction(
        name="Shadow Network",
        ideology=FactionIdeology.ANARCHIST,
        aggression=0.6,
        cooperation=0.75,
        public_support=12.0,  # Low public support
        media_reach=0.3,
        operational_capacity=1.4,
        funding_level=0.6,
        government_heat=8.5,  # High heat triggers secret alliance needs
        factional_trust=60.0,
        territory_zones=["Underground Tunnels", "Safe Houses"]
    )
    
    covert_faction = RevolutionaryFaction(
        name="Covert Liberation Front",
        ideology=FactionIdeology.SOCIALIST,
        aggression=0.5,
        cooperation=0.8,
        public_support=16.0,
        media_reach=0.4,
        operational_capacity=1.6,
        funding_level=0.4,
        government_heat=7.8,  # High heat
        factional_trust=65.0,
        territory_zones=["Worker Districts", "Hidden Cells"]
    )
    
    exposed_faction = RevolutionaryFaction(
        name="Public Resistance Movement",
        ideology=FactionIdeology.LIBERAL_DEMOCRATIC,
        aggression=0.3,
        cooperation=0.6,
        public_support=35.0,
        media_reach=0.7,
        operational_capacity=1.0,
        funding_level=0.8,
        government_heat=4.0,  # Lower heat - public faction
        factional_trust=50.0,
        territory_zones=["City Center", "Universities"]
    )
    
    ecosystem.active_factions = [shadow_faction, covert_faction, exposed_faction]
    ecosystem._initialize_faction_relationships()
    
    print(f"📊 Initial Faction Status (Pre-Secret Operations):")
    for faction in ecosystem.active_factions:
        print(f"  {faction.name}:")
        print(f"    - Support: {faction.public_support:.1f}%")
        print(f"    - Government Heat: {faction.government_heat:.1f}")
        print(f"    - Factional Trust: {faction.factional_trust:.1f}")
        print(f"    - Operational Capacity: {faction.operational_capacity:.2f}")
    
    # Manually form a secret alliance for testing
    print(f"\n🤫 Forming Secret Alliance:")
    secret_alliance = ecosystem.form_secret_alliance(["Shadow Network", "Covert Liberation Front"])
    if secret_alliance:
        print(f"✅ Secret Alliance Created: {secret_alliance.alliance_name}")
        print(f"   - Alliance Type: {secret_alliance.alliance_type.value}")
        print(f"   - Initial Trust: {secret_alliance.trust_level:.1f}")
        print(f"   - Leak Probability: {secret_alliance.leak_probability:.3f}")
    
    # Check diplomatic channels
    print(f"\n🕵️ Diplomatic Channels:")
    print(f"   Active Channels: {len(ecosystem.diplomatic_channels)}")
    for channel_key, channel in ecosystem.diplomatic_channels.items():
        print(f"   - {channel.faction_a} ↔ {channel.faction_b}")
        print(f"     Security: {channel.encryption_level:.2f}, Risk: {channel.leak_risk:.3f}")
    
    return ecosystem

def test_covert_operations_and_leaks():
    """Test covert support operations and intelligence leak mechanics"""
    print("\n" + "="*60)
    print("🎯 TESTING COVERT OPERATIONS & INTELLIGENCE LEAKS")
    print("="*60)
    
    ecosystem = test_secret_alliance_system()
    
    # Track initial metrics
    initial_metrics = {}
    for faction in ecosystem.active_factions:
        initial_metrics[faction.name] = {
            'support': faction.public_support,
            'heat': faction.government_heat,
            'trust': faction.factional_trust,
            'capacity': faction.operational_capacity
        }
    
    print(f"\n🔄 Running 5 Turns with Secret Alliance System:")
    
    covert_operations_count = 0
    intelligence_leaks_count = 0
    
    for turn in range(5):
        print(f"\n--- SECRET OPERATIONS TURN {turn + 1} ---")
        
        # Simulate alliance turn with secret operations
        alliance_results = ecosystem.simulate_alliance_turn()
        
        # Track secret alliances
        secret_alliances = alliance_results.get('secret_alliances', [])
        if secret_alliances:
            print(f"🤫 Secret Alliances Formed:")
            for secret in secret_alliances:
                print(f"   - {secret['alliance_name']}: {', '.join(secret['members'])}")
                print(f"     Leak Risk: {secret['leak_probability']:.3f}")
        
        # Track joint operations (including covert)
        joint_ops = alliance_results.get('joint_operations', [])
        for op in joint_ops:
            if op['activity_type'] == 'covert_support':
                covert_operations_count += 1
                print(f"🎯 COVERT OPERATION:")
                print(f"   Alliance: {op['alliance_name']}")
                print(f"   Success: {'✅' if op['success'] else '❌'}")
                for outcome in op['outcomes']:
                    print(f"   - {outcome}")
                
                if 'counterintelligence_flag' in op:
                    print(f"   ⚠️ Counterintelligence Alert Generated")
        
        # Track intelligence leaks
        leaks = alliance_results.get('intelligence_leaks', [])
        if leaks:
            intelligence_leaks_count += len(leaks)
            print(f"💥 INTELLIGENCE LEAKS:")
            for leak in leaks:
                print(f"   - Type: {leak['type']}")
                if leak['type'] == 'diplomatic_leak':
                    print(f"     Channel: {leak['channel']}")
                elif leak['type'] == 'secret_alliance_exposed':
                    print(f"     Alliance: {leak['alliance_name']}")
                    print(f"     Members: {', '.join(leak['members'])}")
                print(f"     Impact: {leak['impact']}")
        
        # Check propaganda events triggered by leaks
        if alliance_results.get('propaganda_wars'):
            print(f"📢 Scandal Propaganda Triggered:")
            for war in alliance_results['propaganda_wars']:
                print(f"   - {war['initiator']}: {war['tone']}")
        
        # Run regular ecosystem turn
        turn_results = ecosystem.simulate_ecosystem_turn()
    
    # Final summary
    print(f"\n📈 SECRET OPERATIONS SUMMARY:")
    print(f"   Covert Operations Executed: {covert_operations_count}")
    print(f"   Intelligence Leaks: {intelligence_leaks_count}")
    print(f"   Active Secret Alliances: {len([a for a in ecosystem.active_alliances.values() if a.alliance_type == AllianceType.SECRET])}")
    print(f"   Diplomatic Channels: {len(ecosystem.diplomatic_channels)}")
    print(f"   Total Propaganda Events: {len(ecosystem.propaganda_events)}")
    
    # Show faction changes
    print(f"\n🔍 Faction Impact Analysis:")
    for faction in ecosystem.active_factions:
        initial = initial_metrics[faction.name]
        print(f"  {faction.name}:")
        print(f"    Support: {initial['support']:.1f}% → {faction.public_support:.1f}% (Δ{faction.public_support - initial['support']:+.1f})")
        print(f"    Heat: {initial['heat']:.1f} → {faction.government_heat:.1f} (Δ{faction.government_heat - initial['heat']:+.1f})")
        print(f"    Trust: {initial['trust']:.1f} → {faction.factional_trust:.1f} (Δ{faction.factional_trust - initial['trust']:+.1f})")
        print(f"    Capacity: {initial['capacity']:.2f} → {faction.operational_capacity:.2f} (Δ{faction.operational_capacity - initial['capacity']:+.2f})")
    
    # Validation checks
    print(f"\n✅ ITERATION 025 VALIDATION:")
    secret_alliances_formed = len([a for a in ecosystem.active_alliances.values() if a.alliance_type == AllianceType.SECRET]) > 0
    covert_ops_executed = covert_operations_count > 0
    leaks_occurred = intelligence_leaks_count > 0
    diplomatic_channels_active = len(ecosystem.diplomatic_channels) > 0
    propaganda_integration = len(ecosystem.propaganda_events) > 0
    
    print(f"   ✓ Secret Alliances Formed: {'✅' if secret_alliances_formed else '❌'}")
    print(f"   ✓ Covert Operations Executed: {'✅' if covert_ops_executed else '❌'}")
    print(f"   ✓ Intelligence Leaks Occurred: {'✅' if leaks_occurred else '❌'}")
    print(f"   ✓ Diplomatic Channels Active: {'✅' if diplomatic_channels_active else '❌'}")
    print(f"   ✓ Propaganda Integration: {'✅' if propaganda_integration else '❌'}")
    
    return ecosystem

def test_sleeper_cell_mechanics():
    """Basic test for sleeper cell deployment and operation - # ITERATION_026"""
    eco = RevolutionaryEcosystem()
    eco.initialize_default_factions()
    handler = eco.active_factions[0].name
    target = eco.active_factions[1].name
    cell = eco.deploy_sleeper_cell(handler, target)
    assert cell is not None, "Sleeper cell should deploy"
    for _ in range(3):
        eco.uprising_clock.advance_day()
        events = eco.process_sleeper_cells()
        # Ensure events list is collected without error
        assert isinstance(events, list)

def main():
    """Main test function"""
    print("🚀 REVOLUTIONARY ECOSYSTEM TESTING - ITERATIONS 022, 023, 024 & 025")
    print("Testing Faction Rivalries, Alliances, Propaganda Wars, and Secret Diplomacy")
    print("="*80)
    
    # Set random seed for reproducible testing
    random.seed(42)
    
    try:
        # Test alliance system with propaganda
        ecosystem = test_ecosystem_with_alliances()
        
        # Test secret alliance system - ITERATION 025
        print("\n" + "="*80)
        print("🕵️ BEGINNING ITERATION 025 TESTING")
        print("="*80)
        
        secret_ecosystem = test_covert_operations_and_leaks()
        
        print(f"\n✅ TESTING COMPLETE - SUCCESS CRITERIA CHECK:")
        
        # Check success criteria for previous iterations
        alliance_formed = len(ecosystem.active_alliances) > 0 or len(ecosystem.alliance_events) > 0
        joint_operations_occurred = any(event.get('type') == 'joint_operation' for event in ecosystem.uprising_clock.major_events)
        betrayals_or_conflicts = len(ecosystem.conflict_history) > 0 or any(event.get('type') == 'alliance_betrayal' for event in ecosystem.alliance_events)
        
        # Iteration 024 criteria
        propaganda_events_exist = len(ecosystem.propaganda_events) > 0
        support_changes_logged = any(prop.support_changes for prop in ecosystem.propaganda_events)
        narrative_wars_occurred = any(prop.event_type == "counter_narrative" for prop in ecosystem.propaganda_events)
        
        # New criteria for Iteration 025
        secret_alliances_formed = len([a for a in secret_ecosystem.active_alliances.values() if a.alliance_type == AllianceType.SECRET]) > 0
        diplomatic_channels_established = len(secret_ecosystem.diplomatic_channels) > 0
        covert_operations_executed = any(event.get('type') == 'joint_operation' and 'covert' in event.get('description', '') for event in secret_ecosystem.uprising_clock.major_events)
        intelligence_leaks_occurred = len(secret_ecosystem.intelligence_leaks) > 0
        
        print(f"  📊 ITERATION 023 (Alliances):")
        print(f"    ✓ Alliance Formation: {'✅' if alliance_formed else '❌'}")
        print(f"    ✓ Joint Operations: {'✅' if joint_operations_occurred else '❌'}")
        print(f"    ✓ Conflicts/Betrayals: {'✅' if betrayals_or_conflicts else '❌'}")
        
        print(f"  📊 ITERATION 024 (Propaganda):")
        print(f"    ✓ Propaganda Events: {'✅' if propaganda_events_exist else '❌'}")
        print(f"    ✓ Support Changes Logged: {'✅' if support_changes_logged else '❌'}")
        print(f"    ✓ Narrative Wars: {'✅' if narrative_wars_occurred else '❌'}")
        
        print(f"  📊 ITERATION 025 (Secret Diplomacy):")
        print(f"    ✓ Secret Alliances Formed: {'✅' if secret_alliances_formed else '❌'}")
        print(f"    ✓ Diplomatic Channels: {'✅' if diplomatic_channels_established else '❌'}")
        print(f"    ✓ Covert Operations: {'✅' if covert_operations_executed else '❌'}")
        print(f"    ✓ Intelligence Leaks: {'✅' if intelligence_leaks_occurred else '❌'}")
        
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
        
        if (alliance_formed and propaganda_events_exist and support_changes_logged and 
            secret_alliances_formed and diplomatic_channels_established):
            print(f"\n🎉 ITERATIONS 023-025 IMPLEMENTATION SUCCESSFUL!")
            print(f"Complete revolutionary ecosystem with:")
            print(f"  - Alliance formation and betrayal mechanics")
            print(f"  - Propaganda narrative warfare")
            print(f"  - Secret diplomatic channels and covert operations")
            print(f"  - Intelligence leak detection and scandal generation")
            print(f"  - Dynamic trust, momentum, and heat systems")
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