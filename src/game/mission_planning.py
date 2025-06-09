"""
Years of Lead - Mission Planning System

Comprehensive mission planning with risk assessment, resource allocation,
and narrative consequences for the insurgency simulator.
"""

import random
import uuid
from enum import Enum
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from .character_creation import Character, SkillCategory
from .emotional_state import EmotionalState


class MissionType(Enum):
    """Types of missions available"""
    PROPAGANDA = "propaganda"
    SABOTAGE = "sabotage"
    RECRUITMENT = "recruitment"
    INTELLIGENCE = "intelligence"
    FINANCING = "financing"
    RESCUE = "rescue"
    ASSASSINATION = "assassination"
    INFILTRATION = "infiltration"


class MissionPhase(Enum):
    """Phases of mission planning and execution"""
    PLANNING = "planning"
    PREPARATION = "preparation"
    EXECUTION = "execution"
    EXTRACTION = "extraction"
    COMPLETED = "completed"
    FAILED = "failed"


class RiskLevel(Enum):
    """Risk levels for missions"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    EXTREME = "extreme"


@dataclass
class MissionObjective:
    """Specific objective for a mission"""
    type: str
    description: str
    difficulty: int  # 1-10
    success_criteria: List[str]
    failure_conditions: List[str]
    rewards: Dict[str, int]
    penalties: Dict[str, int]


@dataclass
class MissionLocation:
    """Location where mission takes place"""
    name: str
    description: str
    security_level: int  # 1-10
    heat_level: int  # 1-10
    population_density: int  # 1-10
    escape_routes: int  # Number of escape routes
    cover_opportunities: int  # 1-10
    surveillance_level: int  # 1-10
    local_support: int  # 1-10 (how much locals support resistance)
    
    def get_risk_assessment(self) -> Dict[str, Any]:
        """Get detailed risk assessment for this location"""
        risks = {
            "security_risk": self.security_level * 2,
            "detection_risk": (self.surveillance_level + self.population_density) // 2,
            "escape_risk": max(1, 10 - self.escape_routes),
            "support_risk": max(1, 10 - self.local_support),
            "overall_risk": (self.security_level + self.surveillance_level + 
                           (10 - self.escape_routes) + (10 - self.local_support)) // 4
        }
        
        # Determine risk level
        if risks["overall_risk"] <= 3:
            risks["risk_level"] = RiskLevel.LOW
        elif risks["overall_risk"] <= 5:
            risks["risk_level"] = RiskLevel.MEDIUM
        elif risks["overall_risk"] <= 7:
            risks["risk_level"] = RiskLevel.HIGH
        else:
            risks["risk_level"] = RiskLevel.EXTREME
            
        return risks


@dataclass
class MissionPlan:
    """Complete mission plan"""
    id: str
    mission_type: MissionType
    objective: MissionObjective
    location: MissionLocation
    participants: List[Character]
    phase: MissionPhase = MissionPhase.PLANNING
    
    # Planning details
    approach_method: str = ""
    escape_plan: str = ""
    contingency_plans: List[str] = field(default_factory=list)
    
    # Resource allocation
    equipment_needed: List[str] = field(default_factory=list)
    budget_allocated: int = 0
    time_estimate: int = 0  # in hours
    
    # Risk assessment
    calculated_risk: RiskLevel = RiskLevel.MEDIUM
    success_probability: float = 0.5
    
    # Narrative elements
    mission_story: str = ""
    potential_consequences: List[str] = field(default_factory=list)
    
    def calculate_success_probability(self) -> float:
        """Calculate probability of mission success"""
        base_probability = 0.5
        
        # Adjust based on objective difficulty
        difficulty_modifier = (10 - self.objective.difficulty) * 0.05
        base_probability += difficulty_modifier
        
        # Adjust based on participant skills
        skill_bonus = 0
        required_skills = self._get_required_skills()
        for skill, required_level in required_skills.items():
            team_skill = sum(getattr(char.skills, skill, 1) for char in self.participants)
            if team_skill >= required_level:
                skill_bonus += 0.1
            elif team_skill >= required_level * 0.7:
                skill_bonus += 0.05
        
        base_probability += skill_bonus
        
        # Adjust based on location risk
        location_risks = self.location.get_risk_assessment()
        risk_penalty = (location_risks["overall_risk"] - 5) * 0.05
        base_probability -= risk_penalty
        
        # Adjust based on planning quality
        planning_bonus = 0
        if self.approach_method:
            planning_bonus += 0.1
        if self.escape_plan:
            planning_bonus += 0.1
        if len(self.contingency_plans) > 0:
            planning_bonus += min(0.2, len(self.contingency_plans) * 0.05)
        
        base_probability += planning_bonus
        
        return max(0.1, min(0.95, base_probability))
    
    def _get_required_skills(self) -> Dict[str, int]:
        """Get skills required for this mission type"""
        skill_requirements = {
            MissionType.PROPAGANDA: {"social": 3, "intelligence": 2},
            MissionType.SABOTAGE: {"technical": 4, "stealth": 3},
            MissionType.RECRUITMENT: {"social": 4, "intelligence": 2},
            MissionType.INTELLIGENCE: {"intelligence": 4, "stealth": 3},
            MissionType.FINANCING: {"social": 3, "intelligence": 3},
            MissionType.RESCUE: {"combat": 4, "medical": 3, "stealth": 2},
            MissionType.ASSASSINATION: {"combat": 5, "stealth": 4},
            MissionType.INFILTRATION: {"stealth": 4, "social": 3, "intelligence": 2}
        }
        
        return skill_requirements.get(self.mission_type, {})
    
    def get_risk_assessment(self) -> Dict[str, Any]:
        """Get comprehensive risk assessment"""
        location_risks = self.location.get_risk_assessment()
        required_skills = self._get_required_skills()
        
        # Calculate skill gaps
        skill_gaps = {}
        for skill, required_level in required_skills.items():
            team_skill = sum(getattr(char.skills, skill, 1) for char in self.participants)
            skill_gaps[skill] = max(0, required_level - team_skill)
        
        # Calculate team stress level
        team_stress = sum(char.emotional_state.trauma_level for char in self.participants) / len(self.participants)
        
        # Calculate overall risk
        risk_factors = {
            "location_risk": location_risks["overall_risk"],
            "skill_gap_risk": sum(skill_gaps.values()) * 2,
            "team_stress_risk": team_stress * 10,
            "planning_risk": 0 if self.approach_method and self.escape_plan else 3
        }
        
        overall_risk = sum(risk_factors.values()) / len(risk_factors)
        
        # Determine risk level
        if overall_risk <= 3:
            risk_level = RiskLevel.LOW
        elif overall_risk <= 5:
            risk_level = RiskLevel.MEDIUM
        elif overall_risk <= 7:
            risk_level = RiskLevel.HIGH
        else:
            risk_level = RiskLevel.EXTREME
        
        return {
            "risk_level": risk_level,
            "overall_risk_score": overall_risk,
            "risk_factors": risk_factors,
            "location_risks": location_risks,
            "skill_gaps": skill_gaps,
            "team_stress": team_stress,
            "success_probability": self.calculate_success_probability()
        }
    
    def generate_mission_story(self) -> str:
        """Generate narrative description of the mission"""
        mission_stories = {
            MissionType.PROPAGANDA: f"The team will infiltrate {self.location.name} to spread revolutionary propaganda and sway public opinion. The {self.location.description.lower()} provides both opportunities and dangers for this delicate operation.",
            MissionType.SABOTAGE: f"A sabotage mission targeting {self.location.name}. The team must disable key infrastructure while avoiding detection in this high-security area.",
            MissionType.RECRUITMENT: f"Recruitment operation in {self.location.name}. The team will identify and approach potential recruits while maintaining operational security.",
            MissionType.INTELLIGENCE: f"Intelligence gathering mission at {self.location.name}. The team must extract sensitive information without alerting security forces.",
            MissionType.FINANCING: f"Fundraising operation in {self.location.name}. The team will secure financial resources for the resistance movement.",
            MissionType.RESCUE: f"Rescue mission to extract a captured comrade from {self.location.name}. This high-risk operation requires precise timing and coordination.",
            MissionType.ASSASSINATION: f"Elimination mission targeting a high-value target in {self.location.name}. This operation carries extreme risks and moral implications.",
            MissionType.INFILTRATION: f"Deep infiltration mission into {self.location.name}. The team must establish long-term presence while gathering intelligence."
        }
        
        base_story = mission_stories.get(self.mission_type, f"Mission in {self.location.name}")
        
        # Add location-specific details
        if self.location.local_support >= 7:
            base_story += " Local support is strong, which should aid the operation."
        elif self.location.local_support <= 3:
            base_story += " Local support is weak, requiring extra caution."
        
        if self.location.surveillance_level >= 7:
            base_story += " Heavy surveillance in the area increases detection risk."
        
        return base_story
    
    def get_potential_consequences(self) -> List[str]:
        """Get potential consequences of mission success or failure"""
        consequences = []
        
        # Success consequences
        if self.mission_type == MissionType.PROPAGANDA:
            consequences.extend([
                "Increased public support for the resistance",
                "Government propaganda counter-campaign",
                "Media attention and potential exposure"
            ])
        elif self.mission_type == MissionType.SABOTAGE:
            consequences.extend([
                "Infrastructure damage disrupts government operations",
                "Increased security measures in the area",
                "Potential civilian casualties and backlash"
            ])
        elif self.mission_type == MissionType.RECRUITMENT:
            consequences.extend([
                "New operatives join the resistance",
                "Potential informants or double agents",
                "Increased operational capacity"
            ])
        elif self.mission_type == MissionType.INTELLIGENCE:
            consequences.extend([
                "Valuable intelligence gathered",
                "Government security review and changes",
                "Potential counter-intelligence operations"
            ])
        elif self.mission_type == MissionType.FINANCING:
            consequences.extend([
                "Financial resources secured",
                "Increased government scrutiny of financial transactions",
                "Potential legal consequences for funding sources"
            ])
        elif self.mission_type == MissionType.RESCUE:
            consequences.extend([
                "Comrade rescued and returned to safety",
                "Increased government security measures",
                "Potential retaliation against other prisoners"
            ])
        elif self.mission_type == MissionType.ASSASSINATION:
            consequences.extend([
                "Target eliminated",
                "Massive government crackdown",
                "Potential civil war escalation",
                "Moral consequences for team members"
            ])
        elif self.mission_type == MissionType.INFILTRATION:
            consequences.extend([
                "Long-term intelligence gathering capability established",
                "Risk of discovery increases over time",
                "Potential for deep cover operations"
            ])
        
        # Add location-specific consequences
        if self.location.local_support >= 7:
            consequences.append("Strong local support may provide additional assistance")
        elif self.location.local_support <= 3:
            consequences.append("Weak local support may lead to betrayal")
        
        return consequences


class MissionPlanner:
    """Mission planning interface"""
    
    def __init__(self):
        self.available_locations = self._create_default_locations()
        self.available_objectives = self._create_default_objectives()
    
    def _create_default_locations(self) -> Dict[str, MissionLocation]:
        """Create default mission locations"""
        locations = {}
        
        locations["government_quarter"] = MissionLocation(
            name="Government Quarter",
            description="High-security government district with police presence",
            security_level=9,
            heat_level=8,
            population_density=6,
            escape_routes=2,
            cover_opportunities=3,
            surveillance_level=9,
            local_support=2
        )
        
        locations["university_district"] = MissionLocation(
            name="University District",
            description="Academic area with student population and research facilities",
            security_level=4,
            heat_level=3,
            population_density=8,
            escape_routes=6,
            cover_opportunities=7,
            surveillance_level=5,
            local_support=7
        )
        
        locations["industrial_zone"] = MissionLocation(
            name="Industrial Zone",
            description="Factory district with heavy machinery and worker population",
            security_level=6,
            heat_level=7,
            population_density=5,
            escape_routes=4,
            cover_opportunities=6,
            surveillance_level=4,
            local_support=6
        )
        
        locations["old_town"] = MissionLocation(
            name="Old Town Market",
            description="Historic district with markets and residential areas",
            security_level=5,
            heat_level=4,
            population_density=9,
            escape_routes=8,
            cover_opportunities=5,
            surveillance_level=3,
            local_support=8
        )
        
        locations["suburban_residential"] = MissionLocation(
            name="Suburban Residential",
            description="Middle-class residential area with families",
            security_level=3,
            heat_level=2,
            population_density=7,
            escape_routes=7,
            cover_opportunities=4,
            surveillance_level=2,
            local_support=5
        )
        
        locations["downtown_commercial"] = MissionLocation(
            name="Downtown Commercial",
            description="Business district with offices and shopping centers",
            security_level=7,
            heat_level=6,
            population_density=8,
            escape_routes=5,
            cover_opportunities=6,
            surveillance_level=7,
            local_support=4
        )
        
        return locations
    
    def _create_default_objectives(self) -> Dict[MissionType, MissionObjective]:
        """Create default mission objectives"""
        objectives = {}
        
        objectives[MissionType.PROPAGANDA] = MissionObjective(
            type="propaganda",
            description="Spread revolutionary propaganda to sway public opinion",
            difficulty=4,
            success_criteria=["Distribute propaganda materials", "Avoid detection", "Reach target audience"],
            failure_conditions=["Team members arrested", "Materials confiscated", "Public backlash"],
            rewards={"influence": 50, "money": 5000},
            penalties={"heat": 20, "influence": -10}
        )
        
        objectives[MissionType.SABOTAGE] = MissionObjective(
            type="sabotage",
            description="Disable key infrastructure or equipment",
            difficulty=7,
            success_criteria=["Target disabled", "Team escapes", "No casualties"],
            failure_conditions=["Team members killed", "Target not disabled", "Massive retaliation"],
            rewards={"influence": 30, "money": 10000},
            penalties={"heat": 40, "influence": -20}
        )
        
        objectives[MissionType.RECRUITMENT] = MissionObjective(
            type="recruitment",
            description="Recruit new operatives to the resistance",
            difficulty=5,
            success_criteria=["New recruits secured", "Background checks passed", "Safe extraction"],
            failure_conditions=["Informants recruited", "Team compromised", "Recruits arrested"],
            rewards={"personnel": 3, "influence": 20},
            penalties={"heat": 15, "influence": -15}
        )
        
        objectives[MissionType.INTELLIGENCE] = MissionObjective(
            type="intelligence",
            description="Gather sensitive information from target location",
            difficulty=6,
            success_criteria=["Information extracted", "Team escapes", "Source protected"],
            failure_conditions=["Information compromised", "Team captured", "Source killed"],
            rewards={"intelligence": 100, "influence": 25},
            penalties={"heat": 25, "intelligence": -50}
        )
        
        objectives[MissionType.FINANCING] = MissionObjective(
            type="financing",
            description="Secure financial resources for the resistance",
            difficulty=5,
            success_criteria=["Funds secured", "Clean extraction", "No trail left"],
            failure_conditions=["Funds lost", "Team arrested", "Financial trail exposed"],
            rewards={"money": 25000, "influence": 15},
            penalties={"heat": 20, "money": -5000}
        )
        
        objectives[MissionType.RESCUE] = MissionObjective(
            type="rescue",
            description="Rescue captured comrades from enemy custody",
            difficulty=8,
            success_criteria=["Comrades rescued", "Team escapes", "Minimal casualties"],
            failure_conditions=["Rescue failed", "Team killed", "Comrades executed"],
            rewards={"personnel": 2, "influence": 40, "morale": 50},
            penalties={"heat": 50, "morale": -30}
        )
        
        objectives[MissionType.ASSASSINATION] = MissionObjective(
            type="assassination",
            description="Eliminate high-value target",
            difficulty=9,
            success_criteria=["Target eliminated", "Team escapes", "No witnesses"],
            failure_conditions=["Target survives", "Team killed", "Massive retaliation"],
            rewards={"influence": 60, "money": 15000},
            penalties={"heat": 80, "influence": -40, "morale": -20}
        )
        
        objectives[MissionType.INFILTRATION] = MissionObjective(
            type="infiltration",
            description="Establish long-term presence in target location",
            difficulty=7,
            success_criteria=["Cover established", "Access gained", "Intelligence flowing"],
            failure_conditions=["Cover blown", "Team captured", "Operation compromised"],
            rewards={"intelligence": 200, "influence": 35},
            penalties={"heat": 30, "personnel": -1}
        )
        
        return objectives
    
    def create_mission_plan(self, mission_type: MissionType, location_name: str, 
                          participants: List[Character]) -> MissionPlan:
        """Create a new mission plan"""
        location = self.available_locations[location_name]
        objective = self.available_objectives[mission_type]
        
        plan = MissionPlan(
            id=str(uuid.uuid4()),
            mission_type=mission_type,
            objective=objective,
            location=location,
            participants=participants
        )
        
        # Generate mission story and consequences
        plan.mission_story = plan.generate_mission_story()
        plan.potential_consequences = plan.get_potential_consequences()
        
        # Calculate initial risk assessment
        risk_assessment = plan.get_risk_assessment()
        plan.calculated_risk = risk_assessment["risk_level"]
        plan.success_probability = risk_assessment["success_probability"]
        
        return plan
    
    def get_location_details(self, location_name: str) -> Dict[str, Any]:
        """Get detailed information about a location"""
        location = self.available_locations[location_name]
        risk_assessment = location.get_risk_assessment()
        
        return {
            "name": location.name,
            "description": location.description,
            "security_level": location.security_level,
            "heat_level": location.heat_level,
            "population_density": location.population_density,
            "escape_routes": location.escape_routes,
            "cover_opportunities": location.cover_opportunities,
            "surveillance_level": location.surveillance_level,
            "local_support": location.local_support,
            "risk_assessment": risk_assessment,
            "flavor_text": self._generate_location_flavor_text(location)
        }
    
    def _generate_location_flavor_text(self, location: MissionLocation) -> str:
        """Generate procedural flavor text for a location"""
        flavor_templates = {
            "government_quarter": [
                "The imposing government buildings loom over the district, their windows reflecting the cold light of authority. Police patrols are frequent and thorough, their presence a constant reminder of the state's reach.",
                "This is the heart of the regime's power, where decisions that affect millions are made behind closed doors. The security is tight, but so are the opportunities for those brave enough to strike at the center.",
                "Government workers hurry between buildings, their faces a mix of determination and resignation. The air crackles with the tension of bureaucracy and the weight of power."
            ],
            "university_district": [
                "Students fill the streets, their conversations ranging from academic debates to whispered discussions of politics. The energy of youth and idealism is palpable, but so is the watchful eye of campus security.",
                "The university's historic buildings stand as monuments to knowledge and progress, but also to the system that controls education. Young minds are shaped here, some for the regime, others against it.",
                "Research labs and libraries hold secrets both academic and political. The student population provides both cover and potential recruits, but also the risk of betrayal by those seeking to prove their loyalty."
            ],
            "industrial_zone": [
                "The constant hum of machinery fills the air, a symphony of industry that masks both opportunity and danger. Workers move between shifts, their faces marked by the physical toll of labor.",
                "Factories and warehouses provide both targets for sabotage and cover for operations. The working-class population here has suffered under the regime, making them potential allies or informants.",
                "Smokestacks rise against the skyline, symbols of both economic power and environmental destruction. The industrial complex is a vital part of the regime's infrastructure, but also its vulnerability."
            ],
            "old_town": [
                "Narrow streets wind between historic buildings, creating a maze that can hide both secrets and pursuers. The market square bustles with activity, providing both cover and witnesses.",
                "This district has seen generations come and go, its walls holding the memories of countless struggles. The local population is tight-knit, making infiltration difficult but loyalty valuable.",
                "Street vendors and shopkeepers know everyone's business, making this both a source of intelligence and a risk of exposure. The old ways still hold sway here, for better or worse."
            ],
            "suburban_residential": [
                "Neat rows of houses line quiet streets, where families try to maintain normalcy in abnormal times. The appearance of order masks the tensions that lie beneath the surface.",
                "This is the territory of the middle class, those who have something to lose and everything to fear. Their support could be crucial, but their caution could be deadly.",
                "Children play in yards while parents watch from windows, their eyes scanning for both threats and opportunities. The suburbs represent the regime's success and its potential failure."
            ],
            "downtown_commercial": [
                "Glass and steel towers reach toward the sky, symbols of corporate power and economic might. The streets are filled with people rushing between meetings, their attention focused on their own concerns.",
                "Business deals are made in coffee shops and conference rooms, while security cameras watch from every corner. The commercial district is the regime's economic engine, but also its soft underbelly.",
                "Shoppers and workers create a constant flow of humanity, providing both anonymity and the risk of being noticed. The pursuit of profit masks the pursuit of power."
            ]
        }
        
        templates = flavor_templates.get(location.name, [
            f"{location.description} The area presents both opportunities and dangers for resistance operations."
        ])
        
        return random.choice(templates) 