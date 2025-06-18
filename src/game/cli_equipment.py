from src.game.equipment_enhanced import EnhancedEquipmentManager, EnhancedEquipmentProfile
from src.game.equipment_integration import EquipmentIntegrationManager, LoadoutSlot
from src.game.equipment_system import EquipmentCategory

# Helper for clear screen
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def cli_equipment_menu(equipment_manager: EnhancedEquipmentManager, integration_manager: EquipmentIntegrationManager, agents: list):
    """Main CLI menu for equipment management."""
    while True:
        clear_screen()
        print("=== Equipment Management ===")
        print("[1] View All Equipment")
        print("[2] Inspect Equipment Item")
        print("[3] Assign Equipment to Agent")
        print("[4] Remove Equipment from Agent")
        print("[5] Show Agent Loadouts")
        print("[H] Help   [Q] Quit Equipment Menu")
        choice = input("Select an option: ").strip().lower()
        if choice == '1':
            cli_view_all_equipment(equipment_manager)
        elif choice == '2':
            cli_inspect_equipment(equipment_manager)
        elif choice == '3':
            cli_assign_equipment(equipment_manager, integration_manager, agents)
        elif choice == '4':
            cli_remove_equipment(integration_manager, agents)
        elif choice == '5':
            cli_show_agent_loadouts(integration_manager, agents)
        elif choice == 'h':
            cli_equipment_help()
        elif choice == 'q':
            break
        else:
            print("Invalid option. Press Enter to continue.")
            input()

def cli_view_all_equipment(equipment_manager: EnhancedEquipmentManager):
    clear_screen()
    print("--- All Equipment ---")
    equipment_list = list(equipment_manager.equipment_registry.values())
    if not equipment_list:
        print("No equipment available.")
    else:
        for idx, eq in enumerate(equipment_list):
            print(f"[{idx+1}] {eq.name} (Category: {eq.category.value}, Condition: {eq.durability.condition:.2f})")
    input("\nPress Enter to return.")

def cli_inspect_equipment(equipment_manager: EnhancedEquipmentManager):
    clear_screen()
    print("--- Inspect Equipment ---")
    equipment_list = list(equipment_manager.equipment_registry.values())
    if not equipment_list:
        print("No equipment available.")
        input("Press Enter to return.")
        return
    for idx, eq in enumerate(equipment_list):
        print(f"[{idx+1}] {eq.name}")
    choice = input("Enter number to inspect: ").strip()
    if not choice.isdigit() or not (1 <= int(choice) <= len(equipment_list)):
        print("Invalid selection.")
        input("Press Enter to return.")
        return
    eq = equipment_list[int(choice)-1]
    clear_screen()
    print(f"--- {eq.name} ---")
    print(f"Category: {eq.category.value}")
    print(f"Condition: {eq.durability.condition:.2f}")
    print(f"Legal Status: {eq.legal_status.value}")
    print(f"Rarity: {eq.rarity:.2f}")
    print(f"Weight: {eq.weight} kg  Bulk: {eq.bulk}")
    print(f"Skill Bonuses: {eq.effects.skill_bonuses}")
    print(f"Mission Modifiers: {eq.effects.mission_modifiers}")
    print(f"Description: {eq.description}")
    input("\nPress Enter to return.")

def cli_assign_equipment(equipment_manager: EnhancedEquipmentManager, integration_manager: EquipmentIntegrationManager, agents: list):
    clear_screen()
    print("--- Assign Equipment to Agent ---")
    equipment_list = list(equipment_manager.equipment_registry.values())
    if not equipment_list:
        print("No equipment available.")
        input("Press Enter to return.")
        return
    for idx, eq in enumerate(equipment_list):
        print(f"[{idx+1}] {eq.name}")
    eq_choice = input("Enter equipment number to assign: ").strip()
    if not eq_choice.isdigit() or not (1 <= int(eq_choice) <= len(equipment_list)):
        print("Invalid selection.")
        input("Press Enter to return.")
        return
    eq = equipment_list[int(eq_choice)-1]
    print("Available agents:")
    for idx, agent in enumerate(agents):
        print(f"[{idx+1}] {agent['name']}")
    agent_choice = input("Enter agent number: ").strip()
    if not agent_choice.isdigit() or not (1 <= int(agent_choice) <= len(agents)):
        print("Invalid selection.")
        input("Press Enter to return.")
        return
    agent = agents[int(agent_choice)-1]
    loadout = integration_manager.get_agent_loadout(agent['id'])
    print("Available slots:")
    for idx, slot in enumerate(LoadoutSlot):
        print(f"[{idx+1}] {slot.value}")
    slot_choice = input("Enter slot number: ").strip()
    if not slot_choice.isdigit() or not (1 <= int(slot_choice) <= len(LoadoutSlot)):
        print("Invalid selection.")
        input("Press Enter to return.")
        return
    slot = list(LoadoutSlot)[int(slot_choice)-1]
    if loadout.add_equipment(slot, eq):
        print(f"✅ Assigned {eq.name} to {agent['name']} in slot {slot.value}.")
    else:
        print(f"❌ Slot {slot.value} already occupied for {agent['name']}.")
    input("Press Enter to return.")

def cli_remove_equipment(integration_manager: EquipmentIntegrationManager, agents: list):
    clear_screen()
    print("--- Remove Equipment from Agent ---")
    for idx, agent in enumerate(agents):
        print(f"[{idx+1}] {agent['name']}")
    agent_choice = input("Enter agent number: ").strip()
    if not agent_choice.isdigit() or not (1 <= int(agent_choice) <= len(agents)):
        print("Invalid selection.")
        input("Press Enter to return.")
        return
    agent = agents[int(agent_choice)-1]
    loadout = integration_manager.get_agent_loadout(agent['id'])
    if not loadout or not loadout.equipment:
        print(f"No equipment assigned to {agent['name']}.")
        input("Press Enter to return.")
        return
    print(f"Equipment for {agent['name']}:")
    slots = list(loadout.equipment.keys())
    for idx, slot in enumerate(slots):
        eq = loadout.equipment[slot]
        print(f"[{idx+1}] {slot.value}: {eq.name}")
    slot_choice = input("Enter slot number to remove: ").strip()
    if not slot_choice.isdigit() or not (1 <= int(slot_choice) <= len(slots)):
        print("Invalid selection.")
        input("Press Enter to return.")
        return
    slot = slots[int(slot_choice)-1]
    removed = loadout.remove_equipment(slot)
    if removed:
        print(f"✅ Removed {removed.name} from {agent['name']}.")
    else:
        print(f"❌ Failed to remove equipment from slot {slot.value}.")
    input("Press Enter to return.")

def cli_show_agent_loadouts(integration_manager: EquipmentIntegrationManager, agents: list):
    clear_screen()
    print("--- Agent Loadouts ---")
    for agent in agents:
        loadout = integration_manager.get_agent_loadout(agent['id'])
        print(f"\n{agent['name']}:")
        if not loadout or not loadout.equipment:
            print("  (No equipment assigned)")
        else:
            for slot, eq in loadout.equipment.items():
                print(f"  {slot.value}: {eq.name} (Condition: {eq.durability.condition:.2f})")
        print(f"  Total Weight: {loadout.total_weight:.1f} kg  Bulk: {loadout.total_bulk:.1f}")
        print(f"  Concealment: {loadout.concealment_rating:.2f}  Legal Risk: {loadout.legal_risk:.2f}")
        print(f"  Skill Bonuses: {loadout.equipment_bonuses}")
        print(f"  Mission Modifiers: {loadout.mission_modifiers}")
    input("\nPress Enter to return.")

def cli_equipment_help():
    clear_screen()
    print("--- Equipment Management Help ---")
    print("1: View all equipment in your inventory.")
    print("2: Inspect detailed stats and effects of an equipment item.")
    print("3: Assign equipment to an agent and slot.")
    print("4: Remove equipment from an agent's slot.")
    print("5: Show all agent loadouts and bonuses.")
    print("H: Show this help screen.")
    print("Q: Quit equipment management menu.")
    input("\nPress Enter to return.") 