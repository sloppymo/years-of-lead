from src.game.equipment_enhanced import EnhancedEquipmentManager
from src.game.equipment_integration import EquipmentIntegrationManager, LoadoutSlot
from src.game.mission_execution_engine import MissionExecutionEngine

import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def cli_mission_briefing_menu(mission_engine: MissionExecutionEngine, integration_manager: EquipmentIntegrationManager, equipment_manager: EnhancedEquipmentManager, agents: list, missions: list):
    while True:
        clear_screen()
        print("=== Mission Briefing & Planning ===")
        print("[1] View Missions")
        print("[2] Briefing & Risk Analysis")
        print("[3] Change Agent Loadouts (Pre-Mission)")
        print("[4] Launch Mission")
        print("[H] Help   [Q] Quit Mission Menu")
        choice = input("Select an option: ").strip().lower()
        if choice == '1':
            cli_view_missions(missions)
        elif choice == '2':
            cli_briefing_risk_analysis(mission_engine, integration_manager, equipment_manager, agents, missions)
        elif choice == '3':
            cli_change_agent_loadouts(integration_manager, equipment_manager, agents)
        elif choice == '4':
            cli_launch_mission(mission_engine, integration_manager, agents, missions)
        elif choice == 'h':
            cli_mission_help()
        elif choice == 'q':
            break
        else:
            print("Invalid option. Press Enter to continue.")
            input()

def cli_view_missions(missions: list):
    clear_screen()
    print("--- Available Missions ---")
    if not missions:
        print("No missions available.")
    else:
        for idx, m in enumerate(missions):
            print(f"[{idx+1}] {m['name']} (Type: {m['type']}, Difficulty: {m['difficulty']})")
            print(f"   Location: {m['location'].get('name', 'Unknown')}")
            print(f"   Description: {m['description']}")
    input("\nPress Enter to return.")

def cli_briefing_risk_analysis(mission_engine, integration_manager, equipment_manager, agents, missions):
    clear_screen()
    print("--- Mission Briefing & Risk Analysis ---")
    if not missions:
        print("No missions available.")
        input("Press Enter to return.")
        return
    for idx, m in enumerate(missions):
        print(f"[{idx+1}] {m['name']} (Type: {m['type']})")
    choice = input("Enter mission number: ").strip()
    if not choice.isdigit() or not (1 <= int(choice) <= len(missions)):
        print("Invalid selection.")
        input("Press Enter to return.")
        return
    mission = missions[int(choice)-1]
    available_equipment = list(equipment_manager.equipment_registry.values())
    analysis = integration_manager.analyze_mission_equipment(mission, available_equipment)
    print(f"\nMission: {mission['name']}")
    print(f"Type: {mission['type']}  Difficulty: {mission['difficulty']}")
    print(f"Recommended Equipment:")
    for slot, eq_list in analysis.recommended_equipment.items():
        if eq_list:
            print(f"  {slot.value}: {', '.join([eq.name for eq in eq_list[:2]])}")
    print(f"Success Probability Boost: {analysis.success_probability_boost:+.1%}")
    print(f"Concealment: {analysis.concealment_rating:.2f}  Legal Risk: {analysis.legal_risk_level:.2f}")
    print(f"Risk Assessment:")
    for risk_type, risk_level in analysis.risk_assessment.items():
        print(f"  {risk_type.replace('_', ' ').title()}: {risk_level:.2f}")
    input("\nPress Enter to return.")

def cli_change_agent_loadouts(integration_manager, equipment_manager, agents):
    from src.game.cli_equipment import cli_equipment_menu
    cli_equipment_menu(equipment_manager, integration_manager, agents)

def cli_launch_mission(mission_engine, integration_manager, agents, missions):
    clear_screen()
    print("--- Launch Mission ---")
    if not missions:
        print("No missions available.")
        input("Press Enter to return.")
        return
    for idx, m in enumerate(missions):
        print(f"[{idx+1}] {m['name']} (Type: {m['type']})")
    choice = input("Enter mission number to launch: ").strip()
    if not choice.isdigit() or not (1 <= int(choice) <= len(missions)):
        print("Invalid selection.")
        input("Press Enter to return.")
        return
    mission = missions[int(choice)-1]
    confirm = input(f"Are you sure you want to launch '{mission['name']}'? (y/N): ").strip().lower()
    if confirm != 'y':
        print("Mission launch cancelled.")
        input("Press Enter to return.")
        return
    # Execute mission
    result = mission_engine.execute_mission(
        mission=mission,
        agents=agents,
        location=mission["location"],
        resources={"money": 10000, "equipment": 50},
        agent_loadouts={a['id']: integration_manager.get_agent_loadout(a['id']) for a in agents}
    )
    print(f"\nMission Outcome: {result['outcome'].value.replace('_', ' ').title()}")
    print(f"Success Probability: {result['success_probability']:.1%}")
    print(f"Narrative: {result.get('narrative', 'No narrative.')[:200]}...")
    print(f"Equipment Effects: {result['equipment_effects'].get('success_modifier', 0.0):+.1%}")
    input("\nPress Enter to return.")

def cli_mission_help():
    clear_screen()
    print("--- Mission Briefing & Planning Help ---")
    print("1: View all available missions.")
    print("2: See mission briefing, risk analysis, and recommended equipment.")
    print("3: Change agent loadouts before launching a mission.")
    print("4: Launch a mission with current loadouts.")
    print("H: Show this help screen.")
    print("Q: Quit mission menu.")
    input("\nPress Enter to return.") 