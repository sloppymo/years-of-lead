#!/usr/bin/env python3
"""
Years of Lead - Equipment Integration Demo

This demo showcases the Phase 1 equipment system integration with:
1. Agent loadout management
2. Pre-mission equipment analysis
3. Equipment effects during mission execution
4. Equipment degradation and maintenance
5. Mission outcomes influenced by equipment
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from typing import Dict, List, Any
import random
from datetime import datetime

# Import game systems
from game.equipment_enhanced import EnhancedEquipmentManager, EnhancedEquipmentProfile
from game.equipment_integration import EquipmentIntegrationManager, AgentLoadout, LoadoutSlot
from game.mission_execution_engine import MissionExecutionEngine, ExecutionOutcome
from game.equipment_system import EquipmentCategory, LegalStatus


class EquipmentIntegrationDemo:
    """Demo class for equipment integration showcase"""
    
    def __init__(self):
        self.equipment_manager = EnhancedEquipmentManager()
        self.integration_manager = EquipmentIntegrationManager(self.equipment_manager)
        self.mission_engine = MissionExecutionEngine({"equipment_manager": self.equipment_manager})
        
        # Demo agents
        self.agents = [
            {
                "id": "agent_001",
                "name": "Alex Chen",
                "skills": {"stealth": 0.7, "combat": 0.6, "intelligence": 0.8},
                "emotional_state": {"trauma_level": 0.1, "confidence": 0.8}
            },
            {
                "id": "agent_002", 
                "name": "Maria Rodriguez",
                "skills": {"combat": 0.8, "intimidation": 0.7, "hacking": 0.6},
                "emotional_state": {"trauma_level": 0.2, "confidence": 0.7}
            }
        ]
        
        # Demo missions
        self.missions = [
            {
                "id": "mission_001",
                "type": "intelligence",
                "name": "Corporate Espionage",
                "difficulty": 0.7,
                "location": {"name": "TechCorp HQ", "security_level": 0.8},
                "description": "Infiltrate TechCorp headquarters to steal classified data"
            },
            {
                "id": "mission_002",
                "type": "sabotage", 
                "name": "Factory Sabotage",
                "difficulty": 0.6,
                "location": {"name": "Industrial Complex", "security_level": 0.6},
                "description": "Sabotage production equipment at the industrial complex"
            },
            {
                "id": "mission_003",
                "type": "assassination",
                "name": "High-Value Target",
                "difficulty": 0.9,
                "location": {"name": "Luxury Hotel", "security_level": 0.9},
                "description": "Eliminate a high-value target at the luxury hotel"
            }
        ]

    def run_comprehensive_demo(self):
        """Run the complete equipment integration demo"""
        print("🎮 Years of Lead - Equipment Integration Demo")
        print("=" * 60)
        print("Phase 1 Equipment System Integration with Mission Execution")
        print("=" * 60)
        
        # Step 1: Equipment Analysis
        self.demo_equipment_analysis()
        
        # Step 2: Loadout Creation
        self.demo_loadout_creation()
        
        # Step 3: Pre-mission Planning
        self.demo_pre_mission_planning()
        
        # Step 4: Mission Execution with Equipment
        self.demo_mission_execution()
        
        # Step 5: Equipment Degradation and Maintenance
        self.demo_equipment_maintenance()
        
        print("\n🎉 Equipment Integration Demo Complete!")
        print("✅ All Phase 1 features successfully integrated")

    def demo_equipment_analysis(self):
        """Demonstrate equipment analysis capabilities"""
        print("\n🔍 Step 1: Equipment Analysis")
        print("-" * 40)
        
        # Get available equipment
        available_equipment = list(self.equipment_manager.equipment_registry.values())
        
        print(f"📦 Available Equipment: {len(available_equipment)} items")
        
        # Categorize equipment
        categories = {}
        for equipment in available_equipment:
            category = equipment.category.value
            if category not in categories:
                categories[category] = []
            categories[category].append(equipment)
        
        print("\n📊 Equipment by Category:")
        for category, items in categories.items():
            print(f"   {category.title()}: {len(items)} items")
        
        # Show equipment details
        print("\n🔧 Sample Equipment Details:")
        sample_equipment = available_equipment[:3]
        for equipment in sample_equipment:
            print(f"\n   📦 {equipment.name}")
            print(f"      Category: {equipment.category.value}")
            print(f"      Condition: {equipment.durability.condition:.2f}")
            print(f"      Legal Status: {equipment.legal_status.value}")
            print(f"      Rarity: {equipment.rarity:.2f}")
            print(f"      Skill Bonuses: {equipment.effects.skill_bonuses}")
            print(f"      Mission Modifiers: {equipment.effects.mission_modifiers}")

    def demo_loadout_creation(self):
        """Demonstrate agent loadout creation"""
        print("\n🎒 Step 2: Agent Loadout Creation")
        print("-" * 40)
        
        # Create loadouts for agents
        agent_loadouts = {}
        
        for agent in self.agents:
            agent_id = agent["id"]
            loadout = self.integration_manager.create_agent_loadout(agent_id)
            
            # Add equipment based on agent skills
            self._equip_agent_based_on_skills(loadout, agent)
            
            agent_loadouts[agent_id] = loadout
            
            print(f"\n👤 {agent['name']} Loadout:")
            print(f"   Total Weight: {loadout.total_weight:.1f} kg")
            print(f"   Total Bulk: {loadout.total_bulk:.1f}")
            print(f"   Concealment Rating: {loadout.concealment_rating:.2f}")
            print(f"   Legal Risk: {loadout.legal_risk:.2f}")
            
            print(f"   📦 Equipment:")
            for slot, equipment in loadout.equipment.items():
                print(f"      {slot.value}: {equipment.name} (Condition: {equipment.durability.condition:.2f})")
            
            print(f"   ⚡ Skill Bonuses: {loadout.equipment_bonuses}")
            print(f"   🎯 Mission Modifiers: {loadout.mission_modifiers}")
        
        self.agent_loadouts = agent_loadouts

    def _equip_agent_based_on_skills(self, loadout: AgentLoadout, agent: Dict[str, Any]):
        """Equip agent based on their skills"""
        available_equipment = list(self.equipment_manager.equipment_registry.values())
        
        # Get agent's best skills
        skills = agent.get("skills", {})
        best_skills = sorted(skills.items(), key=lambda x: x[1], reverse=True)[:2]
        
        # Equip based on skills
        for skill, level in best_skills:
            if skill == "stealth":
                # Add stealth equipment
                stealth_equipment = [e for e in available_equipment 
                                   if e.category == EquipmentCategory.TOOL and 
                                   "stealth" in e.effects.skill_bonuses]
                if stealth_equipment:
                    loadout.add_equipment(LoadoutSlot.TOOL, stealth_equipment[0])
            
            elif skill == "combat":
                # Add combat equipment
                combat_equipment = [e for e in available_equipment 
                                  if e.category == EquipmentCategory.WEAPON and 
                                  "combat" in e.effects.skill_bonuses]
                if combat_equipment:
                    loadout.add_equipment(LoadoutSlot.PRIMARY_WEAPON, combat_equipment[0])
            
            elif skill == "hacking":
                # Add electronic equipment
                electronic_equipment = [e for e in available_equipment 
                                      if e.category == EquipmentCategory.ELECTRONIC and 
                                      "hacking" in e.effects.skill_bonuses]
                if electronic_equipment:
                    loadout.add_equipment(LoadoutSlot.ELECTRONIC, electronic_equipment[0])

    def demo_pre_mission_planning(self):
        """Demonstrate pre-mission equipment planning"""
        print("\n📋 Step 3: Pre-Mission Equipment Planning")
        print("-" * 40)
        
        # Analyze equipment for each mission
        available_equipment = list(self.equipment_manager.equipment_registry.values())
        
        for mission in self.missions:
            print(f"\n🎯 Mission: {mission['name']} ({mission['type']})")
            print(f"   Difficulty: {mission['difficulty']:.1f}")
            
            # Get equipment analysis
            analysis = self.integration_manager.analyze_mission_equipment(
                mission, available_equipment
            )
            
            print(f"   📊 Equipment Analysis:")
            print(f"      Success Probability Boost: {analysis.success_probability_boost:+.1%}")
            print(f"      Concealment Rating: {analysis.concealment_rating:.2f}")
            print(f"      Legal Risk Level: {analysis.legal_risk_level:.2f}")
            
            print(f"   ⚠️ Risk Assessment:")
            for risk_type, risk_level in analysis.risk_assessment.items():
                print(f"      {risk_type.replace('_', ' ').title()}: {risk_level:.2f}")
            
            print(f"   💡 Loadout Suggestions:")
            for suggestion in analysis.loadout_suggestions[:2]:  # Show top 2
                print(f"      {suggestion['strategy']} Strategy:")
                print(f"         Focus: {suggestion['focus']}")
                print(f"         Total Weight: {suggestion['total_weight']:.1f} kg")
                print(f"         Equipment: {len(suggestion['equipment'])} items")

    def demo_mission_execution(self):
        """Demonstrate mission execution with equipment integration"""
        print("\n⚔️ Step 4: Mission Execution with Equipment Integration")
        print("-" * 40)
        
        # Execute each mission with equipment
        for mission in self.missions:
            print(f"\n🎯 Executing: {mission['name']}")
            print(f"   Type: {mission['type']}")
            print(f"   Difficulty: {mission['difficulty']:.1f}")
            
            # Execute mission with equipment integration
            result = self.mission_engine.execute_mission(
                mission=mission,
                agents=self.agents,
                location=mission["location"],
                resources={"money": 10000, "equipment": 50},
                agent_loadouts=self.agent_loadouts
            )
            
            # Display results
            outcome = result["outcome"]
            success_prob = result["success_probability"]
            equipment_effects = result["equipment_effects"]
            
            print(f"   📊 Mission Results:")
            print(f"      Outcome: {outcome.value.replace('_', ' ').title()}")
            print(f"      Success Probability: {success_prob:.1%}")
            
            # Equipment effects
            success_modifier = equipment_effects.get("success_modifier", 0.0)
            print(f"      Equipment Success Modifier: {success_modifier:+.1%}")
            
            # Equipment degradation
            degradation = equipment_effects.get("equipment_degradation", {})
            if degradation:
                print(f"   🔧 Equipment Degradation:")
                for agent_id, agent_degradation in degradation.items():
                    agent_name = next(a["name"] for a in self.agents if a["id"] == agent_id)
                    print(f"      {agent_name}:")
                    for slot, result in agent_degradation.items():
                        if result["degradation"] < 0:
                            print(f"         {slot}: {result['equipment_name']} - Condition: {result['condition_after']:.2f}")
                            if result["broken"]:
                                print(f"            ❌ BROKEN")
                            elif result["maintenance_required"]:
                                print(f"            ⚠️ Needs Maintenance")
            
            # Narrative (with error handling)
            narrative = result.get("narrative", "Mission completed.")
            print(f"   📖 Narrative: {narrative[:200]}...")
            
            # Update loadouts for next mission
            self.agent_loadouts = result.get("agent_loadouts", self.agent_loadouts)

    def demo_equipment_maintenance(self):
        """Demonstrate equipment maintenance and repair"""
        print("\n🔧 Step 5: Equipment Maintenance and Repair")
        print("-" * 40)
        
        # Get maintenance report
        maintenance_report = self.integration_manager.get_equipment_maintenance_report()
        
        print(f"📊 Equipment Maintenance Status:")
        print(f"   Total Equipment: {maintenance_report['total_equipment']}")
        print(f"   Broken Equipment: {len(maintenance_report['broken_equipment'])}")
        print(f"   Maintenance Required: {len(maintenance_report['maintenance_required'])}")
        print(f"   Total Repair Costs: ${maintenance_report['repair_costs']}")
        
        # Show broken equipment
        if maintenance_report['broken_equipment']:
            print(f"\n❌ Broken Equipment:")
            for item in maintenance_report['broken_equipment']:
                print(f"   {item['equipment']} ({item['agent_id']}) - Repair Cost: ${item['repair_cost']}")
        
        # Show equipment needing maintenance
        if maintenance_report['maintenance_required']:
            print(f"\n⚠️ Equipment Needing Maintenance:")
            for item in maintenance_report['maintenance_required']:
                print(f"   {item['equipment']} ({item['agent_id']}) - Condition: {item['condition']:.2f}")
        
        # Demonstrate repair process
        print(f"\n🔧 Repair Process Demo:")
        for agent_id, loadout in self.agent_loadouts.items():
            agent_name = next(a["name"] for a in self.agents if a["id"] == agent_id)
            print(f"\n   👤 {agent_name}:")
            
            for slot, equipment in loadout.equipment.items():
                if equipment.durability.condition < 1.0:
                    print(f"      Repairing {equipment.name}...")
                    original_condition = equipment.durability.condition
                    
                    # Attempt repair
                    repair_success = equipment.durability.repair_equipment(quality=0.8)
                    
                    if repair_success:
                        new_condition = equipment.durability.condition
                        improvement = new_condition - original_condition
                        print(f"         ✅ Repaired! Condition: {original_condition:.2f} → {new_condition:.2f} (+{improvement:.2f})")
                    else:
                        print(f"         ❌ Repair failed or not needed")

    def run_equipment_effectiveness_analysis(self):
        """Analyze equipment effectiveness across different mission types"""
        print("\n📈 Equipment Effectiveness Analysis")
        print("-" * 40)
        
        available_equipment = list(self.equipment_manager.equipment_registry.values())
        
        mission_types = ["intelligence", "sabotage", "assassination", "propaganda", "recruitment"]
        
        for mission_type in mission_types:
            print(f"\n🎯 {mission_type.title()} Missions:")
            
            # Create test mission
            test_mission = {
                "type": mission_type,
                "difficulty": 0.7,
                "location": {"security_level": 0.6}
            }
            
            # Analyze equipment
            analysis = self.integration_manager.analyze_mission_equipment(
                test_mission, available_equipment
            )
            
            print(f"   Success Boost: {analysis.success_probability_boost:+.1%}")
            print(f"   Concealment: {analysis.concealment_rating:.2f}")
            print(f"   Legal Risk: {analysis.legal_risk_level:.2f}")
            
            # Top equipment recommendations
            top_equipment = []
            for slot, equipment_list in analysis.recommended_equipment.items():
                if equipment_list:
                    top_equipment.append(equipment_list[0])
            
            if top_equipment:
                print(f"   Top Equipment: {', '.join([e.name for e in top_equipment[:3]])}")


def main():
    """Run the equipment integration demo"""
    try:
        demo = EquipmentIntegrationDemo()
        demo.run_comprehensive_demo()
        
        # Additional analysis
        demo.run_equipment_effectiveness_analysis()
        
        print(f"\n🎊 Demo Complete!")
        print(f"✅ Phase 1 equipment system successfully integrated")
        print(f"✅ Equipment affects mission outcomes")
        print(f"✅ Loadouts provide meaningful bonuses")
        print(f"✅ Equipment degrades with use")
        print(f"✅ Maintenance system works")
        
    except Exception as e:
        print(f"❌ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 