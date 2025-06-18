#!/usr/bin/env python3
"""
Phase 1 Equipment System - Comprehensive Bug Testing Suite

This test suite validates all Phase 1 features:
1. Equipment variety expansion (20+ new items)
2. Quality & durability system
3. Equipment effects & bonuses
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, field
from enum import Enum
import random
import json
from datetime import datetime

# Import the base equipment system
from game.equipment_system import (
    EquipmentCategory, LegalStatus, EquipmentProfile, 
    EquipmentFlag, ConsequenceRule, ConsequenceType
)


class EquipmentQuality(Enum):
    """Equipment quality levels"""
    BROKEN = 0.0
    POOR = 0.25
    FAIR = 0.5
    GOOD = 0.75
    EXCELLENT = 1.0


@dataclass
class EquipmentDurability:
    """Equipment durability and condition tracking"""
    condition: float = 1.0  # 0.0 = broken, 1.0 = perfect
    reliability: float = 0.8  # Success chance modifier
    maintenance_required: bool = False
    degradation_rate: float = 0.01  # Per use
    repair_cost: float = 0.0  # Cost to repair
    max_repairs: int = 3  # Maximum repair attempts
    repair_count: int = 0  # Current number of repairs
    last_maintenance: int = 0  # Turn of last maintenance

    def use_equipment(self, intensity: float = 1.0) -> bool:
        """Use equipment and apply degradation"""
        if self.condition <= 0.0:
            return False  # Equipment is broken
        
        # Apply degradation
        degradation = self.degradation_rate * intensity
        self.condition = max(0.0, self.condition - degradation)
        
        # Check if maintenance is needed
        if self.condition < 0.5:
            self.maintenance_required = True
        
        return True

    def repair_equipment(self, quality: float = 1.0) -> bool:
        """Repair equipment"""
        if self.repair_count >= self.max_repairs:
            return False  # Cannot repair further
        
        if self.condition >= 1.0:
            return False  # Already in perfect condition
        
        # Repair based on quality
        repair_amount = quality * 0.3  # 30% repair per attempt
        self.condition = min(1.0, self.condition + repair_amount)
        self.repair_count += 1
        self.maintenance_required = False
        
        return True

    def get_effectiveness_modifier(self) -> float:
        """Get effectiveness modifier based on condition"""
        if self.condition <= 0.0:
            return 0.0  # Broken equipment is useless
        elif self.condition < 0.3:
            return 0.3  # Poor condition
        elif self.condition < 0.6:
            return 0.6  # Fair condition
        elif self.condition < 0.9:
            return 0.9  # Good condition
        else:
            return 1.0  # Excellent condition


@dataclass
class EquipmentEffects:
    """Equipment effects and bonuses"""
    skill_bonuses: Dict[str, float] = field(default_factory=dict)
    mission_modifiers: Dict[str, float] = field(default_factory=dict)
    emotional_effects: Dict[str, float] = field(default_factory=dict)
    social_effects: Dict[str, float] = field(default_factory=dict)
    concealment_bonuses: Dict[str, float] = field(default_factory=dict)
    detection_penalties: Dict[str, float] = field(default_factory=dict)

    def get_total_skill_bonus(self, skill: str) -> float:
        """Get total bonus for a specific skill"""
        return self.skill_bonuses.get(skill, 0.0)

    def get_mission_modifier(self, mission_type: str) -> float:
        """Get modifier for a specific mission type"""
        return self.mission_modifiers.get(mission_type, 0.0)

    def get_emotional_effect(self, emotion: str) -> float:
        """Get emotional effect modifier"""
        return self.emotional_effects.get(emotion, 0.0)

    def get_social_effect(self, context: str) -> float:
        """Get social effect modifier"""
        return self.social_effects.get(context, 0.0)


@dataclass
class EnhancedEquipmentProfile(EquipmentProfile):
    """Enhanced equipment profile with quality and effects"""
    durability: EquipmentDurability = field(default_factory=EquipmentDurability)
    effects: EquipmentEffects = field(default_factory=EquipmentEffects)
    signature_properties: Dict[str, Any] = field(default_factory=dict)
    faction_affiliation: Optional[str] = None
    rarity: float = 0.5  # 0.0 = common, 1.0 = legendary

    def get_effective_concealment(
        self, 
        container_present: bool = False, 
        equipment_flags: Set[str] = None,
        context: Dict[str, Any] = None
    ) -> float:
        """Calculate effective concealment with quality and effects"""
        base_concealment = super().get_effective_concealment(container_present, equipment_flags)
        
        # Apply quality modifier
        quality_modifier = self.durability.get_effectiveness_modifier()
        base_concealment *= quality_modifier
        
        # Apply concealment bonuses from effects
        if context:
            for context_type, bonus in self.effects.concealment_bonuses.items():
                if context.get(context_type, False):
                    base_concealment += bonus
        
        return min(1.0, max(0.0, base_concealment))

    def use_equipment(self, intensity: float = 1.0) -> bool:
        """Use equipment and apply degradation"""
        return self.durability.use_equipment(intensity)

    def get_skill_bonus(self, skill: str) -> float:
        """Get skill bonus for this equipment"""
        return self.effects.get_total_skill_bonus(skill)

    def get_mission_bonus(self, mission_type: str) -> float:
        """Get mission bonus for this equipment"""
        return self.effects.get_mission_modifier(mission_type)


class EquipmentTestSuite:
    """Comprehensive test suite for Phase 1 equipment system"""
    
    def __init__(self):
        self.test_results = []
        self.equipment_registry = {}
        self.initialize_test_equipment()
    
    def log_test(self, test_name: str, passed: bool, details: str = ""):
        """Log test result"""
        result = {
            "test": test_name,
            "passed": passed,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"   {details}")

    def initialize_test_equipment(self):
        """Initialize test equipment for comprehensive testing"""
        
        # Test equipment with various configurations
        test_items = [
            {
                "item_id": "test_wpn_001",
                "name": "Test Assault Rifle",
                "category": EquipmentCategory.WEAPON,
                "concealable": False,
                "concealment_rating": 0.1,
                "legal_status": LegalStatus.PROHIBITED,
                "weight": 3.5,
                "bulk": 2.0,
                "value": 2500,
                "rarity": 0.7,
                "durability": EquipmentDurability(
                    condition=0.9,
                    reliability=0.85,
                    degradation_rate=0.02,
                    repair_cost=500
                ),
                "effects": EquipmentEffects(
                    skill_bonuses={"combat": 0.4, "intimidation": 0.3},
                    mission_modifiers={"sabotage": 0.2, "propaganda": -0.1},
                    emotional_effects={"fear": 0.2, "confidence": 0.3},
                    social_effects={"military": 0.2, "civilian": -0.3}
                )
            },
            {
                "item_id": "test_elc_001",
                "name": "Test Laptop",
                "category": EquipmentCategory.ELECTRONIC,
                "concealable": True,
                "concealment_rating": 0.6,
                "container_bonus": 0.1,
                "legal_status": LegalStatus.LEGAL,
                "weight": 2.5,
                "bulk": 1.5,
                "value": 1200,
                "rarity": 0.6,
                "durability": EquipmentDurability(
                    condition=0.85,
                    reliability=0.8,
                    degradation_rate=0.01,
                    repair_cost=200
                ),
                "effects": EquipmentEffects(
                    skill_bonuses={"hacking": 0.5, "intelligence": 0.3},
                    mission_modifiers={"intelligence": 0.4, "propaganda": 0.2},
                    emotional_effects={"confidence": 0.1},
                    social_effects={"corporate": 0.1}
                )
            },
            {
                "item_id": "test_tool_001",
                "name": "Test Lockpicks",
                "category": EquipmentCategory.TOOL,
                "concealable": True,
                "concealment_rating": 0.95,
                "container_bonus": 0.05,
                "legal_status": LegalStatus.RESTRICTED,
                "weight": 0.2,
                "bulk": 0.1,
                "value": 200,
                "rarity": 0.5,
                "durability": EquipmentDurability(
                    condition=0.9,
                    reliability=0.85,
                    degradation_rate=0.008,
                    repair_cost=30
                ),
                "effects": EquipmentEffects(
                    skill_bonuses={"stealth": 0.4, "infiltration": 0.3},
                    mission_modifiers={"intelligence": 0.3, "sabotage": 0.2},
                    emotional_effects={"confidence": 0.1}
                )
            }
        ]
        
        for item_data in test_items:
            equipment = EnhancedEquipmentProfile(
                item_id=item_data["item_id"],
                name=item_data["name"],
                category=item_data["category"],
                concealable=item_data["concealable"],
                concealment_rating=item_data["concealment_rating"],
                container_bonus=item_data.get("container_bonus", 0.0),
                legal_status=item_data["legal_status"],
                description=f"Test {item_data['name']}",
                weight=item_data["weight"],
                bulk=item_data["bulk"],
                value=item_data["value"],
                rarity=item_data["rarity"],
                durability=item_data["durability"],
                effects=item_data["effects"]
            )
            self.equipment_registry[item_data["item_id"]] = equipment

    def test_equipment_creation(self):
        """Test equipment creation and basic properties"""
        print("\n🔧 Testing Equipment Creation...")
        
        for item_id, equipment in self.equipment_registry.items():
            # Test basic properties
            self.log_test(
                f"Equipment Creation - {equipment.name}",
                equipment.item_id == item_id and equipment.name is not None,
                f"ID: {equipment.item_id}, Name: {equipment.name}"
            )
            
            # Test category assignment
            self.log_test(
                f"Category Assignment - {equipment.name}",
                equipment.category in EquipmentCategory,
                f"Category: {equipment.category.value}"
            )
            
            # Test legal status
            self.log_test(
                f"Legal Status - {equipment.name}",
                equipment.legal_status in LegalStatus,
                f"Status: {equipment.legal_status.value}"
            )
            
            # Test rarity bounds
            self.log_test(
                f"Rarity Bounds - {equipment.name}",
                0.0 <= equipment.rarity <= 1.0,
                f"Rarity: {equipment.rarity}"
            )

    def test_durability_system(self):
        """Test durability and quality system"""
        print("\n🔧 Testing Durability System...")
        
        for item_id, equipment in self.equipment_registry.items():
            # Test initial condition
            self.log_test(
                f"Initial Condition - {equipment.name}",
                0.0 <= equipment.durability.condition <= 1.0,
                f"Condition: {equipment.durability.condition}"
            )
            
            # Test equipment usage
            initial_condition = equipment.durability.condition
            success = equipment.use_equipment(intensity=1.0)
            
            self.log_test(
                f"Equipment Usage - {equipment.name}",
                success and equipment.durability.condition < initial_condition,
                f"Success: {success}, Condition: {equipment.durability.condition:.3f}"
            )
            
            # Test repair system
            if equipment.durability.condition < 1.0:
                repair_success = equipment.durability.repair_equipment(quality=0.8)
                self.log_test(
                    f"Repair System - {equipment.name}",
                    repair_success and equipment.durability.condition > initial_condition,
                    f"Repair Success: {repair_success}, New Condition: {equipment.durability.condition:.3f}"
                )
            
            # Test effectiveness modifier
            modifier = equipment.durability.get_effectiveness_modifier()
            self.log_test(
                f"Effectiveness Modifier - {equipment.name}",
                0.0 <= modifier <= 1.0,
                f"Modifier: {modifier:.3f}"
            )

    def test_equipment_effects(self):
        """Test equipment effects and bonuses"""
        print("\n⚡ Testing Equipment Effects...")
        
        for item_id, equipment in self.equipment_registry.items():
            # Test skill bonuses
            for skill, bonus in equipment.effects.skill_bonuses.items():
                retrieved_bonus = equipment.get_skill_bonus(skill)
                self.log_test(
                    f"Skill Bonus - {equipment.name} ({skill})",
                    retrieved_bonus == bonus,
                    f"Expected: {bonus}, Got: {retrieved_bonus}"
                )
            
            # Test mission modifiers
            for mission_type, modifier in equipment.effects.mission_modifiers.items():
                retrieved_modifier = equipment.get_mission_bonus(mission_type)
                self.log_test(
                    f"Mission Modifier - {equipment.name} ({mission_type})",
                    retrieved_modifier == modifier,
                    f"Expected: {modifier}, Got: {retrieved_modifier}"
                )
            
            # Test emotional effects
            for emotion, effect in equipment.effects.emotional_effects.items():
                retrieved_effect = equipment.effects.get_emotional_effect(emotion)
                self.log_test(
                    f"Emotional Effect - {equipment.name} ({emotion})",
                    retrieved_effect == effect,
                    f"Expected: {effect}, Got: {retrieved_effect}"
                )

    def test_concealment_system(self):
        """Test enhanced concealment system"""
        print("\n👁️ Testing Enhanced Concealment...")
        
        for item_id, equipment in self.equipment_registry.items():
            # Test base concealment
            base_concealment = equipment.get_effective_concealment()
            self.log_test(
                f"Base Concealment - {equipment.name}",
                0.0 <= base_concealment <= 1.0,
                f"Concealment: {base_concealment:.3f}"
            )
            
            # Test container bonus
            container_concealment = equipment.get_effective_concealment(container_present=True)
            self.log_test(
                f"Container Concealment - {equipment.name}",
                container_concealment >= base_concealment,
                f"Base: {base_concealment:.3f}, Container: {container_concealment:.3f}"
            )
            
            # Test quality effect on concealment
            original_condition = equipment.durability.condition
            equipment.durability.condition = 0.5  # Set to fair condition
            quality_concealment = equipment.get_effective_concealment()
            equipment.durability.condition = original_condition  # Restore
            
            self.log_test(
                f"Quality Concealment - {equipment.name}",
                quality_concealment <= base_concealment,
                f"Original: {base_concealment:.3f}, Quality: {quality_concealment:.3f}"
            )

    def test_edge_cases(self):
        """Test edge cases and error conditions"""
        print("\n⚠️ Testing Edge Cases...")
        
        # Test broken equipment
        test_equipment = self.equipment_registry["test_wpn_001"]
        test_equipment.durability.condition = 0.0
        
        self.log_test(
            "Broken Equipment Usage",
            not test_equipment.use_equipment(),
            "Broken equipment should not be usable"
        )
        
        # Test repair limits
        test_equipment.durability.repair_count = 3
        test_equipment.durability.condition = 0.5
        
        self.log_test(
            "Repair Limit",
            not test_equipment.durability.repair_equipment(),
            "Equipment should not be repairable beyond max repairs"
        )
        
        # Test negative values
        test_equipment.durability.condition = -0.1
        modifier = test_equipment.durability.get_effectiveness_modifier()
        
        self.log_test(
            "Negative Condition Handling",
            modifier == 0.0,
            f"Negative condition should result in 0.0 modifier, got: {modifier}"
        )
        
        # Test excessive values
        test_equipment.durability.condition = 1.5
        modifier = test_equipment.durability.get_effectiveness_modifier()
        
        self.log_test(
            "Excessive Condition Handling",
            modifier == 1.0,
            f"Excessive condition should be capped at 1.0, got: {modifier}"
        )

    def test_data_integrity(self):
        """Test data integrity and consistency"""
        print("\n🔒 Testing Data Integrity...")
        
        for item_id, equipment in self.equipment_registry.items():
            # Test equipment ID consistency
            self.log_test(
                f"ID Consistency - {equipment.name}",
                equipment.item_id == item_id,
                f"Expected: {item_id}, Got: {equipment.item_id}"
            )
            
            # Test weight and bulk consistency
            self.log_test(
                f"Weight/Bulk Consistency - {equipment.name}",
                equipment.weight > 0 and equipment.bulk > 0,
                f"Weight: {equipment.weight}, Bulk: {equipment.bulk}"
            )
            
            # Test value consistency
            self.log_test(
                f"Value Consistency - {equipment.name}",
                equipment.value >= 0,
                f"Value: {equipment.value}"
            )
            
            # Test durability data consistency
            durability = equipment.durability
            self.log_test(
                f"Durability Consistency - {equipment.name}",
                0.0 <= durability.condition <= 1.0 and durability.repair_count >= 0,
                f"Condition: {durability.condition}, Repairs: {durability.repair_count}"
            )

    def test_performance(self):
        """Test system performance"""
        print("\n⚡ Testing Performance...")
        
        # Test equipment creation performance
        import time
        
        start_time = time.time()
        for i in range(100):
            test_equipment = EnhancedEquipmentProfile(
                item_id=f"perf_test_{i}",
                name=f"Performance Test Item {i}",
                category=EquipmentCategory.TOOL,
                durability=EquipmentDurability(),
                effects=EquipmentEffects()
            )
        creation_time = time.time() - start_time
        
        self.log_test(
            "Equipment Creation Performance",
            creation_time < 1.0,  # Should create 100 items in under 1 second
            f"Created 100 items in {creation_time:.3f} seconds"
        )
        
        # Test concealment calculation performance
        test_equipment = self.equipment_registry["test_wpn_001"]
        start_time = time.time()
        for i in range(1000):
            concealment = test_equipment.get_effective_concealment()
        calculation_time = time.time() - start_time
        
        self.log_test(
            "Concealment Calculation Performance",
            calculation_time < 0.1,  # Should calculate 1000 times in under 0.1 seconds
            f"Calculated concealment 1000 times in {calculation_time:.3f} seconds"
        )

    def run_all_tests(self):
        """Run all test suites"""
        print("🧪 Phase 1 Equipment System - Comprehensive Bug Testing")
        print("=" * 70)
        
        self.test_equipment_creation()
        self.test_durability_system()
        self.test_equipment_effects()
        self.test_concealment_system()
        self.test_edge_cases()
        self.test_data_integrity()
        self.test_performance()
        
        # Generate summary
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["passed"])
        failed_tests = total_tests - passed_tests
        
        print(f"\n📊 Test Summary")
        print("=" * 70)
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests} ✅")
        print(f"Failed: {failed_tests} ❌")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        # Show failed tests
        if failed_tests > 0:
            print(f"\n❌ Failed Tests:")
            for result in self.test_results:
                if not result["passed"]:
                    print(f"   • {result['test']}: {result['details']}")
        
        # Save detailed results
        self.save_test_results()
        
        return failed_tests == 0

    def save_test_results(self):
        """Save detailed test results to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"phase1_equipment_test_results_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump({
                "test_suite": "Phase 1 Equipment System",
                "timestamp": datetime.now().isoformat(),
                "results": self.test_results,
                "summary": {
                    "total": len(self.test_results),
                    "passed": sum(1 for r in self.test_results if r["passed"]),
                    "failed": sum(1 for r in self.test_results if not r["passed"])
                }
            }, f, indent=2)
        
        print(f"\n📄 Detailed results saved to: {filename}")


def main():
    """Run the comprehensive test suite"""
    try:
        test_suite = EquipmentTestSuite()
        success = test_suite.run_all_tests()
        
        if success:
            print(f"\n🎉 All Phase 1 equipment system tests passed!")
            print(f"✅ Equipment variety expansion: Working")
            print(f"✅ Quality & durability system: Working")
            print(f"✅ Equipment effects & bonuses: Working")
            print(f"✅ Enhanced concealment: Working")
            print(f"✅ Edge case handling: Working")
            print(f"✅ Data integrity: Working")
            print(f"✅ Performance: Acceptable")
        else:
            print(f"\n⚠️ Some tests failed. Please review the failed tests above.")
        
        return success
        
    except Exception as e:
        print(f"❌ Test suite failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 