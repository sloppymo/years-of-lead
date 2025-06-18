from src.game.equipment_enhanced import (
    EnhancedEquipmentManager,
)
from src.game.equipment_integration import EquipmentIntegrationManager, LoadoutSlot

import os


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def cli_inventory_menu(
    equipment_manager: EnhancedEquipmentManager,
    integration_manager: EquipmentIntegrationManager,
    agents: list,
    storage: dict,
    safehouses: dict = None,
):
    """Main CLI menu for inventory and storage management."""
    while True:
        clear_screen()
        print("=== Inventory & Storage ===")
        print("[1] View Storage Inventory")
        print("[2] Move Equipment: Storage <-> Agent")
        print("[3] View Agent Inventories")
        print("[4] View Safehouse Storage")
        print("[H] Help   [Q] Quit Inventory Menu")
        choice = input("Select an option: ").strip().lower()
        if choice == "1":
            cli_view_storage_inventory(storage)
        elif choice == "2":
            cli_move_equipment_storage_agent(
                equipment_manager, integration_manager, agents, storage
            )
        elif choice == "3":
            cli_view_agent_inventories(integration_manager, agents)
        elif choice == "4":
            cli_view_safehouse_storage(safehouses)
        elif choice == "h":
            cli_inventory_help()
        elif choice == "q":
            break
        else:
            print("Invalid option. Press Enter to continue.")
            input()


def cli_view_storage_inventory(storage: dict):
    clear_screen()
    print("--- Storage Inventory ---")
    items = storage.get("items", [])
    if not items:
        print("No items in storage.")
    else:
        for idx, eq in enumerate(items):
            print(f"[{idx+1}] {eq.name} (Condition: {eq.durability.condition:.2f})")
    input("\nPress Enter to return.")


def cli_move_equipment_storage_agent(
    equipment_manager, integration_manager, agents, storage
):
    clear_screen()
    print("--- Move Equipment: Storage <-> Agent ---")
    items = storage.get("items", [])
    print("[1] Move from Storage to Agent")
    print("[2] Move from Agent to Storage")
    choice = input("Select direction: ").strip()
    if choice == "1":
        if not items:
            print("No items in storage.")
            input("Press Enter to return.")
            return
        for idx, eq in enumerate(items):
            print(f"[{idx+1}] {eq.name}")
        eq_choice = input("Enter equipment number to move: ").strip()
        if not eq_choice.isdigit() or not (1 <= int(eq_choice) <= len(items)):
            print("Invalid selection.")
            input("Press Enter to return.")
            return
        eq = items[int(eq_choice) - 1]
        print("Available agents:")
        for idx, agent in enumerate(agents):
            print(f"[{idx+1}] {agent['name']}")
        agent_choice = input("Enter agent number: ").strip()
        if not agent_choice.isdigit() or not (1 <= int(agent_choice) <= len(agents)):
            print("Invalid selection.")
            input("Press Enter to return.")
            return
        agent = agents[int(agent_choice) - 1]
        loadout = integration_manager.get_agent_loadout(agent["id"])
        print("Available slots:")
        for idx, slot in enumerate(LoadoutSlot):
            print(f"[{idx+1}] {slot.value}")
        slot_choice = input("Enter slot number: ").strip()
        if not slot_choice.isdigit() or not (1 <= int(slot_choice) <= len(LoadoutSlot)):
            print("Invalid selection.")
            input("Press Enter to return.")
            return
        slot = list(LoadoutSlot)[int(slot_choice) - 1]
        if loadout.add_equipment(slot, eq):
            print(f"✅ Moved {eq.name} to {agent['name']} in slot {slot.value}.")
            items.remove(eq)
        else:
            print(f"❌ Slot {slot.value} already occupied for {agent['name']}.")
        input("Press Enter to return.")
    elif choice == "2":
        print("Available agents:")
        for idx, agent in enumerate(agents):
            print(f"[{idx+1}] {agent['name']}")
        agent_choice = input("Enter agent number: ").strip()
        if not agent_choice.isdigit() or not (1 <= int(agent_choice) <= len(agents)):
            print("Invalid selection.")
            input("Press Enter to return.")
            return
        agent = agents[int(agent_choice) - 1]
        loadout = integration_manager.get_agent_loadout(agent["id"])
        if not loadout or not loadout.equipment:
            print(f"No equipment assigned to {agent['name']}.")
            input("Press Enter to return.")
            return
        print(f"Equipment for {agent['name']}:")
        slots = list(loadout.equipment.keys())
        for idx, slot in enumerate(slots):
            eq = loadout.equipment[slot]
            print(f"[{idx+1}] {slot.value}: {eq.name}")
        slot_choice = input("Enter slot number to move to storage: ").strip()
        if not slot_choice.isdigit() or not (1 <= int(slot_choice) <= len(slots)):
            print("Invalid selection.")
            input("Press Enter to return.")
            return
        slot = slots[int(slot_choice) - 1]
        eq = loadout.remove_equipment(slot)
        if eq:
            print(f"✅ Moved {eq.name} from {agent['name']} to storage.")
            items.append(eq)
        else:
            print(f"❌ Failed to remove equipment from slot {slot.value}.")
        input("Press Enter to return.")
    else:
        print("Invalid option.")
        input("Press Enter to return.")


def cli_view_agent_inventories(
    integration_manager: EquipmentIntegrationManager, agents: list
):
    clear_screen()
    print("--- Agent Inventories ---")
    for agent in agents:
        loadout = integration_manager.get_agent_loadout(agent["id"])
        print(f"\n{agent['name']}:")
        if not loadout or not loadout.equipment:
            print("  (No equipment assigned)")
        else:
            for slot, eq in loadout.equipment.items():
                print(
                    f"  {slot.value}: {eq.name} (Condition: {eq.durability.condition:.2f})"
                )
    input("\nPress Enter to return.")


def cli_view_safehouse_storage(safehouses: dict):
    clear_screen()
    print("--- Safehouse Storage ---")
    if not safehouses:
        print("No safehouses available.")
        input("Press Enter to return.")
        return
    for name, storage in safehouses.items():
        print(f"\n{name}:")
        items = storage.get("items", [])
        if not items:
            print("  (No items in storage)")
        else:
            for eq in items:
                print(f"  {eq.name} (Condition: {eq.durability.condition:.2f})")
    input("\nPress Enter to return.")


def cli_inventory_help():
    clear_screen()
    print("--- Inventory & Storage Help ---")
    print("1: View all equipment in central storage.")
    print("2: Move equipment between storage and agents.")
    print("3: View all agent inventories.")
    print("4: View equipment in safehouses.")
    print("H: Show this help screen.")
    print("Q: Quit inventory menu.")
    input("\nPress Enter to return.")
