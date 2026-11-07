from colorama import Fore
from item import make_item

class Inventory:
    def __init__(self, items=None):
        self.items = items or []

    def add(self, item):
        self.items.append(item)
        print(Fore.GREEN + f'Added {item["name"]} to inventory.')

    def show(self):
        print(Fore.CYAN + "\n=== INVENTORY ===")
        if not self.items:
            print("(empty)")
        for i, item in enumerate(self.items, 1):
            print(f'{i}. {item["name"]} [{item["type"]}] — {item.get("description", "")}')

    def use_item(self, player, item_type=None):
        candidates = [(i, it) for i, it in enumerate(self.items) if item_type is None or it["type"] == item_type]
        if not candidates:
            print("No usable items of that type.")
            return False
        for i, it in candidates:
            print(f'{i + 1}. {it["name"]}')
        try:
            choice = int(input("Item number (0 cancels): "))
            if choice == 0:
                return False
            if not 1 <= choice <= len(self.items):
                raise ValueError
            item = self.items[choice - 1]
            if item_type and item["type"] != item_type:
                print("Choose a matching item.")
                return False
            if item["type"] == "potion":
                old = player.hp
                player.hp = min(player.max_hp, player.hp + item.get("heal", 35))
                print(Fore.GREEN + f"Restored {player.hp - old} HP.")
                self.items.pop(choice - 1)
                return True
            print("That item cannot be used here.")
            return False
        except ValueError:
            print(Fore.RED + "Enter a valid item number.")
            return False

    def equip_item(self, player):
        gear = [(i, it) for i, it in enumerate(self.items) if it["type"] in ("weapon", "armor")]
        if not gear:
            print("No equipment in inventory.")
            return
        for i, item in gear:
            print(f'{i + 1}. {item["name"]} [{item["type"]}]')
        try:
            choice = int(input("Choose equipment (0 cancels): "))
            if choice == 0:
                return
            item = self.items[choice - 1]
            if item["type"] == "weapon":
                player.equipped_weapon_bonus = item.get("attack_bonus", 0)
            elif item["type"] == "armor":
                player.equipped_armor = item.get("armor_bonus", 0)
            print(f'Equipped {item["name"]}.')
        except (ValueError, IndexError):
            print(Fore.RED + "Invalid equipment number.")

    def to_list(self):
        return self.items
