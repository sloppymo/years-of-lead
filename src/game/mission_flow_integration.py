"""
Integration code to connect enhanced mission flows with the existing PlayerInterface.
"""

from typing import Dict, List, Any
from .enhanced_mission_flows import (
    InfiltrationMissionFlow,
    MissionState,
    MissionPhase,
    MissionChoice,
)
from .entities import Mission, Agent


class EnhancedPlayerInterface:
    """Enhanced version of PlayerInterface with dramatic mission flows"""

    def __init__(self, game_state):
        self.game_state = game_state
        self.active_mission_flows = {}  # mission_id -> flow instance

    def execute_mission_with_choices(
        self, mission: Mission, agents: List[Agent]
    ) -> Dict[str, Any]:
        """
        Execute a mission with full choice-driven narrative flow.

        This replaces the basic mission resolution with dramatic, interactive sequences.
        """
        # Create mission state
        mission_state = MissionState(
            mission_id=mission.id,
            current_phase=MissionPhase.PREPARATION,
            agents=agents,
            success_probability=0.5,  # Will be modified by choices
            stress_accumulation={agent.id: 0.0 for agent in agents},
            relationship_changes={},
            narrative_log=[],
            crisis_points=[],
            player_choices=[],
        )

        # Route to appropriate mission flow based on type
        if mission.mission_type.value == "infiltration":
            flow = InfiltrationMissionFlow(mission_state)
            result = flow.execute_mission()

        elif mission.mission_type.value == "assassination":
            result = self._execute_assassination_mission(mission_state)

        elif mission.mission_type.value == "recruitment":
            result = self._execute_recruitment_mission(mission_state)

        else:
            # Fallback to basic mission resolution for other types
            result = self._execute_basic_mission(mission_state)

        # Apply results to game state
        self._apply_mission_results(result, agents)

        return result

    def _execute_assassination_mission(
        self, mission_state: MissionState
    ) -> Dict[str, Any]:
        """Execute assassination mission with moral complexity"""
        self._display_mission_header("ASSASSINATION MISSION")

        # Phase 1: Moral briefing
        print("\n📋 MISSION BRIEF: ASSASSINATION")
        print("Target: Colonel Martinez, Head of Anti-Terrorism Unit")
        print("Location: Private residence, suburban district")
        print("Intel: Lives alone, ex-wife has custody of children")
        print("Moral Weight: Responsible for disappearing 40+ activists")

        # Check team psychological readiness for killing
        moral_objections = []
        for agent in mission_state.agents:
            # Check agent's ideology and trauma flags
            if (
                hasattr(agent, "trauma_flags")
                and "pacifist_drift" in agent.trauma_flags
            ):
                moral_objections.append(
                    f"{agent.name} has developed pacifist tendencies"
                )
            if getattr(agent, "stress", 0) > 70:
                moral_objections.append(
                    f"{agent.name} may not be psychologically ready for killing"
                )

        if moral_objections:
            print("\n⚖️  PSYCHOLOGICAL ASSESSMENT:")
            for objection in moral_objections:
                print(f"   • {objection}")

        # Moral choice point
        choice = MissionChoice(
            id="assassination_approach",
            description="How do you proceed with this assassination?",
            options=[
                {
                    "text": "Proceed with assassination - Maximum operational impact",
                    "consequences": {
                        "lethality": "high",
                        "psychological_trauma": "severe",
                    },
                    "requirements": {},
                },
                {
                    "text": "Capture for interrogation - More intel, preserve conscience",
                    "consequences": {"complexity": "high", "moral_preservation": True},
                    "requirements": {"team_coordination": 70},
                },
                {
                    "text": "Public exposure - Safer but less certain results",
                    "consequences": {"safety": "high", "effectiveness": "uncertain"},
                    "requirements": {"social_skill": 60},
                },
                {
                    "text": "Abort - Preserve team psychological health",
                    "consequences": {"mission_failure": True, "morale": "preserved"},
                    "requirements": {},
                },
            ],
            context={"target": "Colonel Martinez", "moral_weight": "extreme"},
            moral_weight="extreme",
        )

        result = self._present_choice(choice)

        if result.get("consequences", {}).get("mission_failure"):
            return self._create_mission_result(
                "aborted", "Team chose to preserve moral integrity"
            )

        # Phase 2: The personal moment (if proceeding)
        if result.get("consequences", {}).get("lethality") != "high":
            return self._handle_capture_scenario(mission_state)
        else:
            return self._handle_assassination_scenario(mission_state)

    def _handle_capture_scenario(self, mission_state: MissionState) -> Dict[str, Any]:
        """Handle the more complex capture scenario"""
        print("\n🏠 8:30 PM - Surveillance Phase")
        print("Your team watches Martinez's house from across the street.")
        print(
            "Through the kitchen window: Martinez cooking dinner, checking his phone."
        )
        print("He looks... normal. Human.")

        # Create moral tension through humanization
        agent_reactions = []
        for agent in mission_state.agents:
            if hasattr(agent, "background"):
                if agent.background == "family_oriented":
                    agent_reactions.append(
                        f"{agent.name} whispers: 'He's just making pasta. Like anyone's dad would.'"
                    )
                elif agent.background == "vengeful":
                    agent_reactions.append(
                        f"{agent.name}'s jaw tightens: 'Don't make him human to me.'"
                    )

        if agent_reactions:
            print("\n💭 TEAM REACTIONS:")
            for reaction in agent_reactions:
                print(f"   {reaction}")

        # The intercepted phone call
        print("\n📞 9:15 PM - Intercepted Phone Call")
        print("Through the speakers, you hear:")
        print('"Hi daddy! I lost another tooth today!"')
        print('Martinez: "Really? Did you put it under your pillow?"')
        print('"Yes! Mommy says the tooth fairy might bring two dollars!"')
        print('Martinez laughs: "Two whole dollars? You\'re getting rich, mija."')

        print("\nSILENCE IN THE VAN.")

        # Critical moral choice
        choice = MissionChoice(
            id="moral_breaking_point",
            description="Hearing Martinez with his daughter changes everything. What now?",
            options=[
                {
                    "text": "Continue mission - 'Being a father doesn't erase his crimes'",
                    "consequences": {"moral_conflict": "high", "team_stress": +20},
                    "requirements": {"determination": 70},
                },
                {
                    "text": "Modify approach - 'Capture during commute, away from family'",
                    "consequences": {
                        "complexity": "medium",
                        "moral_preservation": "partial",
                    },
                    "requirements": {"tactical_flexibility": 60},
                },
                {
                    "text": "Abort mission - 'We're not killers of fathers'",
                    "consequences": {
                        "mission_failure": True,
                        "moral_high_ground": True,
                    },
                    "requirements": {},
                },
                {
                    "text": "Investigate further - 'Let's verify our intelligence first'",
                    "consequences": {"delay": True, "intelligence_gathering": True},
                    "requirements": {"patience": True},
                },
            ],
            context={"humanization_moment": True, "family_involvement": True},
            moral_weight="extreme",
        )

        result = self._present_choice(choice)

        # Handle the revelation twist if investigating
        if result.get("consequences", {}).get("intelligence_gathering"):
            return self._handle_intelligence_revelation(mission_state)

        return self._resolve_capture_mission(mission_state, result)

    def _handle_intelligence_revelation(
        self, mission_state: MissionState
    ) -> Dict[str, Any]:
        """Handle the twist where intelligence reveals moral complexity"""
        print("\n📄 7:30 AM - The Investigation")
        print("Your team decides to confront Martinez directly.")
        print("As you approach, Martinez looks up from his morning coffee.")
        print("Recognition flashes across his face.")

        print("\nMartinez: \"You're Miguel Santos's sister.\"")

        # Find Maria Santos if she exists in the team
        maria = next(
            (agent for agent in mission_state.agents if "Maria" in agent.name), None
        )
        if maria:
            print(f"\n{maria.name} freezes. He remembers her brother's name.")

        print('\nMartinez: "I\'m sorry about Miguel. I really am."')
        print('         "But he was planning to bomb a school."')

        if maria:
            print(f'\n{maria.name}: "LIAR!"')

        print('\nMartinez: "The evidence is in my car. See for yourself."')

        # The moral revelation
        choice = MissionChoice(
            id="evidence_revelation",
            description="Martinez claims your brother was planning to bomb a school. Do you look at his evidence?",
            options=[
                {
                    "text": "Examine the evidence - 'Show me'",
                    "consequences": {
                        "truth_revealed": True,
                        "worldview_shattered": True,
                    },
                    "requirements": {"courage": 70},
                },
                {
                    "text": "Refuse to look - 'Obvious trap'",
                    "consequences": {"denial": True, "mission_continues": True},
                    "requirements": {},
                },
                {
                    "text": "Capture him first, verify later - 'Evidence can be faked'",
                    "consequences": {"tactical_advantage": True, "truth_delayed": True},
                    "requirements": {"suspicion": 60},
                },
                {
                    "text": "Walk away - 'This is getting too complicated'",
                    "consequences": {"mission_abort": True, "questions_remain": True},
                    "requirements": {},
                },
            ],
            context={"personal_stakes": True, "truth_moment": True},
            moral_weight="extreme",
        )

        result = self._present_choice(choice)

        if result.get("consequences", {}).get("truth_revealed"):
            return self._handle_truth_revelation(mission_state, maria)

        return self._resolve_capture_mission(mission_state, result)

    def _handle_truth_revelation(
        self, mission_state: MissionState, maria_agent
    ) -> Dict[str, Any]:
        """Handle the devastating truth revelation"""
        print("\n📄 Evidence Review")
        print(
            "The documents are real. Photos of Miguel with explosive materials, school blueprints."
        )
        print(
            "But the photos also show he was coerced - threatening notes about Maria's safety."
        )

        print(
            '\nMartinez: "Your brother was a good man forced into an impossible choice."'
        )
        print('          "He came to me the night before, wanted to call it off."')
        print('          "That\'s when they killed him - his own people."')

        if maria_agent:
            print(
                f'\n{maria_agent.name} breaks down: "The resistance... killed Miguel?"'
            )

            # Apply massive psychological trauma
            if hasattr(maria_agent, "trauma_flags"):
                maria_agent.trauma_flags.extend(
                    ["worldview_collapse", "betrayal_by_allies", "brother_truth"]
                )

            # Relationship changes - trust in faction leadership plummets
            mission_state.relationship_changes[maria_agent.id] = {
                "faction_loyalty": -50
            }

        # New mission parameters
        choice = MissionChoice(
            id="truth_aftermath",
            description="Everything you believed was wrong. How do you proceed?",
            options=[
                {
                    "text": "Recruit Martinez - 'Help us find Miguel's real killers'",
                    "consequences": {"faction_changing": True, "enemy_to_ally": True},
                    "requirements": {"open_mindedness": 80},
                },
                {
                    "text": "Extract information - 'Tell us everything you know'",
                    "consequences": {"intelligence_gain": "major", "cooperation": True},
                    "requirements": {},
                },
                {
                    "text": "Walk away - 'This is too much to process'",
                    "consequences": {"overwhelmed": True, "opportunity_lost": True},
                    "requirements": {},
                },
                {
                    "text": "Protect Martinez - 'You're in danger too'",
                    "consequences": {
                        "ally_protection": True,
                        "faction_betrayal_risk": True,
                    },
                    "requirements": {"moral_courage": 90},
                },
            ],
            context={"truth_revealed": True, "worldview_changed": True},
            moral_weight="extreme",
        )

        result = self._present_choice(choice)

        return self._create_mission_result(
            "life_changing",
            "Mission outcome: Worldview shattered, new alliance forged, truth discovered",
        )

    def _execute_recruitment_mission(
        self, mission_state: MissionState
    ) -> Dict[str, Any]:
        """Execute recruitment mission with gradual trust building"""
        self._display_mission_header("RECRUITMENT MISSION")

        print("\n📋 MISSION BRIEF: RECRUITMENT")
        print("Target: Dr. Elena Vasquez, Medical Examiner")
        print("Location: City Hospital, night shift")
        print("Intel: Has access to 'suicide' reports that might be murders")
        print("Personal: Single mother, 8-year-old son, heavily in debt")

        # Approach selection
        choice = MissionChoice(
            id="recruitment_approach",
            description="How do you approach Dr. Vasquez?",
            options=[
                {
                    "text": "Ideological appeal - 'Help us expose the truth'",
                    "consequences": {
                        "approach": "ideological",
                        "time": "fast",
                        "loyalty": "high",
                    },
                    "requirements": {"social_skill": 70},
                },
                {
                    "text": "Financial incentive - 'We can help with your debts'",
                    "consequences": {
                        "approach": "financial",
                        "loyalty": "transactional",
                        "guilt": "medium",
                    },
                    "requirements": {},
                },
                {
                    "text": "Protection offer - 'We'll keep you and your son safe'",
                    "consequences": {
                        "approach": "protective",
                        "fear_based": True,
                        "compliance": "high",
                    },
                    "requirements": {},
                },
                {
                    "text": "Gradual friendship - 'Build trust over time'",
                    "consequences": {
                        "approach": "friendship",
                        "time": "slow",
                        "loyalty": "genuine",
                    },
                    "requirements": {"patience": True},
                },
            ],
            context={"target_vulnerable": True, "family_involved": True},
            moral_weight="medium",
        )

        result = self._present_choice(choice)

        if result.get("consequences", {}).get("approach") == "friendship":
            return self._handle_friendship_recruitment(mission_state)
        else:
            return self._handle_direct_recruitment(mission_state, result)

    def _handle_direct_recruitment(
        self, mission_state: MissionState, approach: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle direct recruitment approaches (ideological, financial, protective)"""
        approach_type = approach.get("consequences", {}).get("approach", "ideological")

        print("\n🚀 Direct Recruitment Approach")
        print("----------------------------")

        if approach_type == "ideological":
            print("You appeal to Dr. Vasquez's sense of justice and truth.")
            print(
                "You show her evidence of covered-up murders in the 'suicide' reports."
            )
            print("She's visibly shaken but intrigued by the truth.")

            # Add a choice for her response
            choice = MissionChoice(
                id="ideological_response",
                description="How does Dr. Vasquez respond?",
                options=[
                    {
                        "text": "'I had no idea... I want to help expose this!'",
                        "consequences": {
                            "success": True,
                            "loyalty": "high",
                            "motivation": "ideological",
                        },
                    },
                    {
                        "text": "'This is too dangerous for me and my son.'",
                        "consequences": {"success": False, "reason": "fear_for_safety"},
                    },
                    {
                        "text": "'I need time to think about this...'",
                        "consequences": {
                            "success": "delayed",
                            "next_step": "follow_up",
                        },
                    },
                ],
            )

        elif approach_type == "financial":
            print("You offer to help with Dr. Vasquez's crippling debts.")
            print("She's hesitant but clearly tempted by the financial relief.")

            choice = MissionChoice(
                id="financial_response",
                description="How does Dr. Vasquez respond?",
                options=[
                    {
                        "text": "I can't say no to this opportunity... I'm in.",
                        "consequences": {
                            "success": True,
                            "loyalty": "transactional",
                            "motivation": "financial",
                        },
                    },
                    {
                        "text": "I can't be bought! Get out!",
                        "consequences": {"success": False, "reason": "insulted"},
                    },
                    {
                        "text": "How do I know I can trust you?",
                        "consequences": {
                            "success": "delayed",
                            "next_step": "build_trust",
                        },
                    },
                ],
            )

        else:  # protective approach
            print("You emphasize the danger she and her son are in.")
            print("You show her evidence that the government is watching her.")
            print("She's clearly frightened but also angry at being manipulated.")

            choice = MissionChoice(
                id="protective_response",
                description="How does Dr. Vasquez respond?",
                options=[
                    {
                        "text": "'If you can protect us, I'll help.'",
                        "consequences": {
                            "success": True,
                            "loyalty": "fear_based",
                            "motivation": "protection",
                        },
                    },
                    {
                        "text": "'This sounds like a threat! I'm calling security!'",
                        "consequences": {"success": False, "reason": "backfired"},
                    },
                    {
                        "text": "'I need proof you can protect us...'",
                        "consequences": {
                            "success": "delayed",
                            "next_step": "demonstrate_protection",
                        },
                    },
                ],
            )

        # Present the choice and get the result
        result = self._present_choice(choice)

        # Process the result
        if result.get("success") is True:
            print("\n✅ Success! Dr. Vasquez has agreed to work with us.")
            return {
                "success": True,
                "message": f"Successfully recruited Dr. Vasquez using {approach_type} approach.",
                "new_asset": "Dr. Elena Vasquez - Medical Examiner",
                "intel_gained": ["Covered-up murders in suicide reports"],
                "mission_type": "RECRUITMENT",
            }
        elif result.get("success") is False:
            print(f"\n❌ Recruitment failed: {result.get('reason', 'Unknown reason')}")
            return {
                "success": False,
                "message": f"Failed to recruit Dr. Vasquez: {result.get('reason', 'Unknown reason')}",
                "mission_type": "RECRUITMENT",
            }
        else:  # Delayed response
            print("\n⏳ Dr. Vasquez needs time to consider your offer.")
            return {
                "success": "pending",
                "message": "Dr. Vasquez needs more time to decide.",
                "next_step": result.get("next_step", "follow_up"),
                "mission_type": "RECRUITMENT",
            }

    def _handle_friendship_recruitment(
        self, mission_state: MissionState
    ) -> Dict[str, Any]:
        """Handle the gradual friendship approach to recruitment"""
        print("\n🏥 Week 1 - Building Trust")
        print("Sofia has been working night shifts, establishing a presence.")
        print("Dr. Vasquez enters the cafeteria, exhausted after a difficult autopsy.")

        # Find Sofia or primary social agent
        social_agent = max(
            mission_state.agents, key=lambda a: getattr(a, "social_skill", 0)
        )

        print(
            f"\n{social_agent.name} notices Dr. Vasquez's medical bag has a child's drawing:"
        )
        print("A stick figure family: mom, son, and a cat.")

        # Trust building choice
        choice = MissionChoice(
            id="trust_building",
            description="How do you build rapport with Dr. Vasquez?",
            options=[
                {
                    "text": "Personal connection - Share your own family story",
                    "consequences": {
                        "trust_gain": +20,
                        "vulnerability": "mutual",
                        "bond": "deep",
                    },
                    "requirements": {"empathy": 60},
                },
                {
                    "text": "Professional interest - Ask about her work",
                    "consequences": {
                        "trust_gain": +10,
                        "information": "some",
                        "distance": "maintained",
                    },
                    "requirements": {},
                },
                {
                    "text": "Supportive - 'Single parenthood must be tough'",
                    "consequences": {
                        "trust_gain": +15,
                        "emotional_support": True,
                        "appreciation": "high",
                    },
                    "requirements": {"social_awareness": 50},
                },
                {
                    "text": "Casual - Keep conversation light",
                    "consequences": {
                        "trust_gain": +5,
                        "safe_approach": True,
                        "progress": "slow",
                    },
                    "requirements": {},
                },
            ],
            context={"building_friendship": True, "child_involved": True},
            moral_weight="low",
        )

        result = self._present_choice(choice)

        # Week 2 - Deepening relationship
        print("\n🌙 Week 2 - Rooftop Conversations")
        print(
            "Elena and Sofia have developed a routine - coffee breaks on the hospital roof."
        )
        print("Elena brings homemade sandwiches, Sofia brings good stories.")

        print(
            "\nElena: \"You know, you're the first person here who doesn't treat me like"
        )
        print(
            '       the weird death lady. Everyone else gets uncomfortable when I talk about work."'
        )

        print(f"\n{social_agent.name}: \"Death isn't weird - it's just part of life.")
        print(
            "                     Someone has to speak for people who can't speak for themselves.\""
        )

        print("\nElena looks thoughtful: \"That's... actually really beautiful.")
        print(
            "                        'Speaking for the dead.' I never thought of it that way.\""
        )

        # The opening
        print('\nElena: "Can I tell you something? Off the record?"')
        print("       \"Some of these 'suicide' cases I get... they don't add up.\"")
        print('       "Wrong angle on wounds, defensive marks, signs of struggle."')
        print(
            '       "But when I write it up, my supervisor just files it as depression."'
        )

        # Critical ethical moment
        choice = MissionChoice(
            id="recruitment_moment",
            description="Elena is sharing exactly what you need, but as a friend. How do you respond?",
            options=[
                {
                    "text": "Immediate recruitment - 'What if I told you about people who could help?'",
                    "consequences": {
                        "recruitment": "direct",
                        "betrayal_feeling": "high",
                        "success": "uncertain",
                    },
                    "requirements": {},
                },
                {
                    "text": "Gather more intel - 'That sounds frustrating. Tell me more?'",
                    "consequences": {
                        "information": "more",
                        "manipulation": "continued",
                        "guilt": "building",
                    },
                    "requirements": {},
                },
                {
                    "text": "Genuine support - Focus on Elena's emotional needs first",
                    "consequences": {
                        "friendship": "deepened",
                        "ethics": "preserved",
                        "delay": True,
                    },
                    "requirements": {"moral_integrity": 70},
                },
                {
                    "text": "Plant seeds - 'What would you do if you could expose it?'",
                    "consequences": {
                        "subtle_influence": True,
                        "manipulation": "light",
                        "preparation": True,
                    },
                    "requirements": {"social_skill": 80},
                },
            ],
            context={"genuine_friendship": True, "mission_objective": "available"},
            moral_weight="high",
        )

        result = self._present_choice(choice)

        return self._resolve_recruitment_mission(mission_state, result)

    def _resolve_recruitment_mission(
        self, mission_state: MissionState, choice_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Resolve the recruitment mission based on player choices"""
        consequences = choice_result.get("consequences", {})

        # Week 3 - Crisis moment
        print("\n💔 Week 3 - Personal Crisis")
        print("Elena calls Sofia at 1 AM, crying.")
        print("Elena's son Diego is sick, needs expensive treatment.")
        print("Insurance denied the claim. Elena can't afford the medicine.")

        print(
            '\nElena: "I keep thinking... if I just signed off on those suspicious deaths,'
        )
        print(
            "       maybe I'd get promoted, make more money. But then I couldn't live with myself.\""
        )

        # The moment of truth
        if consequences.get("friendship") == "deepened":
            return self._handle_honest_recruitment(mission_state)
        else:
            return self._handle_manipulative_recruitment(mission_state)

    def _handle_honest_recruitment(self, mission_state: MissionState) -> Dict[str, Any]:
        """Handle recruitment with full honesty about identity"""
        print('\nSofia: "Elena, I need to tell you something about who I really am..."')
        print("       \"I'm not really a physical therapist. I'm part of the group")
        print("       that's been investigating those suspicious deaths.\"")

        print("\nElena goes silent. Steps out of the car.")
        print('Elena: "You... you\'ve been lying to me this whole time?"')

        print("\nSofia: \"No! The friendship is real. Everything we've shared is real.")
        print("       I was supposed to recruit you, but... I care about you too much")
        print('       to keep lying."')

        # Final choice
        choice = MissionChoice(
            id="honest_recruitment_finale",
            description="Elena feels betrayed but sees Sofia's genuine care. What do you offer?",
            options=[
                {
                    "text": "Full transparency - 'Ask me anything. No more lies.'",
                    "consequences": {
                        "honesty": "complete",
                        "trust": "rebuilt",
                        "recruitment": "ethical",
                    },
                    "requirements": {"moral_courage": 80},
                },
                {
                    "text": "Practical help - 'We'll get Diego's treatment regardless'",
                    "consequences": {
                        "compassion": "shown",
                        "no_strings": True,
                        "loyalty": "earned",
                    },
                    "requirements": {"resources": 100},
                },
                {
                    "text": "Choice freedom - 'If you say no, I disappear. No consequences.'",
                    "consequences": {
                        "pressure": "none",
                        "respect": "maximum",
                        "agency": "preserved",
                    },
                    "requirements": {},
                },
                {
                    "text": "Friendship priority - 'Handler or not, I want you in my life'",
                    "consequences": {
                        "relationship": "prioritized",
                        "human_connection": True,
                    },
                    "requirements": {"emotional_intelligence": 70},
                },
            ],
            context={"honesty_moment": True, "friendship_tested": True},
            moral_weight="high",
        )

        result = self._present_choice(choice)

        # Elena's decision based on relationship strength and approach
        trust_level = 85  # High due to honesty
        desperation = 90  # High due to son's medical needs
        moral_conviction = 78  # Wants to expose truth

        recruitment_chance = (trust_level + desperation + moral_conviction) / 300

        if recruitment_chance > 0.7:
            print("\nElena: \"I'll do it. Not for the money, not for the cause.")
            print(
                '       For Diego. I want him to grow up in a world where the truth matters."'
            )

            return self._create_mission_result(
                "success",
                "Ethical recruitment successful - genuine friendship and loyalty established",
            )
        else:
            print('\nElena: "I need time to think about this."')
            return self._create_mission_result(
                "partial_success",
                "Recruitment pending - trust maintained, decision delayed",
            )

    def _execute_basic_mission(self, mission_state: MissionState) -> Dict[str, Any]:
        """Fallback mission execution with basic resolution"""
        print("\n⚠️  Using basic mission resolution (fallback)")
        return {
            "success": True,
            "narrative": "Mission completed with basic resolution (enhanced flows not implemented for this mission type)",
            "stress_changes": {},
            "relationship_changes": {},
        }

    def _handle_manipulative_recruitment(
        self, mission_state: MissionState
    ) -> Dict[str, Any]:
        """Handle recruitment using manipulation tactics"""
        return self._create_mission_result(
            "success", "Recruitment successful through manipulation, but at what cost?"
        )

    def _handle_assassination_scenario(
        self, mission_state: MissionState
    ) -> Dict[str, Any]:
        """Handle the assassination scenario"""
        return self._create_mission_result(
            "success", "Assassination completed, but the moral weight remains..."
        )

    def _resolve_capture_mission(
        self, mission_state: MissionState, result: Dict
    ) -> Dict[str, Any]:
        """Resolve a capture mission"""
        return self._create_mission_result(
            "success", "Target captured and extracted successfully"
        )

    def _present_choice(self, choice) -> Dict:
        """Present choice to player and get their selection"""
        print(f"\n{choice.description}")
        for i, option in enumerate(choice.options, 1):
            print(f"{i}. {option['text']}")

        while True:
            try:
                selection = int(input("Choose an option: ")) - 1
                if 0 <= selection < len(choice.options):
                    return choice.options[selection]
                print("Invalid selection. Try again.")
            except ValueError:
                print("Please enter a number.")

    def _display_mission_header(self, title: str):
        """Display mission header"""
        print("\n" + "=" * 60)
        print(f"   🎯 {title}")
        print("=" * 60)

    def _create_mission_result(self, outcome: str, description: str) -> Dict[str, Any]:
        """Create a standardized mission result dictionary"""
        return {
            "outcome": outcome,
            "description": description,
            "success": outcome == "success" or outcome == "life_changing",
            "narrative_impact": "high" if outcome == "life_changing" else "medium",
            "psychological_impact": "varies_by_choice",
            "relationship_changes": True,
        }

    def _apply_mission_results(
        self, result: Dict[str, Any], agents: List[Agent]
    ) -> None:
        """Apply mission results to game state and agents"""
        # This would be implemented to update agent states, relationships, etc.
        pass


def execute_enhanced_mission(
    game_state, mission, agents: List[Agent]
) -> Dict[str, Any]:
    """
    Main integration function to execute missions with enhanced flows.

    Call this instead of basic mission resolution to get the full
    dramatic, choice-driven experience.
    """
    enhanced_interface = EnhancedPlayerInterface(game_state)
    return enhanced_interface.execute_mission_with_choices(mission, agents)
