from colorama import Fore, Style, init
from auth import Auth
from database import GameDatabase
from player import Player
from world_map import WorldMap
from npc import NPCS
from quest import QuestManager
from shop import Shop
from combat import Combat
from monster import create_monster
from item import make_item

init(autoreset=True)

class Game:
    def __init__(self):
        self.db = GameDatabase()
        self.auth = Auth(self.db)
        self.username = None
        self.player = None
        self.map = None
        self.quests = None
        self.shop = Shop()
        self.combat = None

    def run(self):
        print(Fore.CYAN + Style.BRIGHT + """
╔══════════════════════════════════════════════╗
║                 EMBERFALL                   ║
╚══════════════════════════════════════════════╝
The kingdom of Emberfall is fading. The Ember Crown has been stolen,
and the ancient wards protecting the realm are breaking.
You are a new adventurer summoned to restore the wards, help its people,
and face the Ashen Dragon before darkness claims the kingdom.
""")
        while True:
            print(Fore.YELLOW + "\n1. Log in\n2. Register\n3. Exit")
            choice = input("Choose: ").strip()
            if choice == "1":
                username = self.auth.login()
                if username:
                    self.start_session(username)
                    return
            elif choice == "2":
                self.auth.register()
            elif choice == "3":
                print("May your road be bright.")
                return
            else:
                print(Fore.RED + "Please enter 1, 2, or 3.")

    def start_session(self, username):
        self.username = username
        saved = self.db.load_progress(username)
        self.player = Player.from_dict(saved) if saved else Player(username)
        self.map = WorldMap(self.player.current_map, self.player)
        self.quests = QuestManager(self.player)
        self.combat = Combat(self.player, self.save)
        self.main_loop()

    def save(self):
        self.player.current_map = self.map.name
        self.db.save_progress(self.username, self.player.to_dict())

    def main_loop(self):
        while self.player.hp > 0:
            self.map = WorldMap(self.player.current_map, self.player)
            self.map.draw(self.player.position, self.player)
            print(Fore.CYAN + f"\n{self.player.name} | Lv {self.player.level} | HP {self.player.hp}/{self.player.max_hp} | XP {self.player.xp} | Gold {self.player.gold}")
            print("1 Move  2 Talk  3 Quests  4 Inventory  5 Skills  6 Character  7 Shop  8 Save  9 Logout")
            choice = input("> ").strip()
            if choice == "1":
                self.move()
            elif choice == "2":
                self.talk()
            elif choice == "3":
                self.quests.show()
            elif choice == "4":
                self.inventory_menu()
            elif choice == "5":
                self.skill_menu()
            elif choice == "6":
                self.player.show_progress()
            elif choice == "7":
                self.shop_menu()
            elif choice == "8":
                self.save()
                print(Fore.GREEN + "Progress saved.")
            elif choice == "9":
                self.save()
                print(Fore.GREEN + "Saved. You are logged out.")
                return
            else:
                print(Fore.RED + "Invalid choice. Enter a number from 1 to 9.")
        self.save()
        print(Fore.RED + "You have fallen. Your progress has been saved.")

    def move(self):
        direction = input("Move (W/A/S/D), or X to cancel: ").strip().lower()
        if direction == "x":
            return
        deltas = {"w": (0, -1), "s": (0, 1), "a": (-1, 0), "d": (1, 0)}
        if direction not in deltas:
            print(Fore.RED + "Use W, A, S, D, or X.")
            return
        dx, dy = deltas[direction]
        nx, ny = self.player.position[0] + dx, self.player.position[1] + dy
        if not self.map.walkable(nx, ny):
            print(Fore.RED + "A wall blocks the way.")
            return
        self.player.position = (nx, ny)
        self.map.name = self.player.current_map
        item_key = self.map.ground_items.get(self.player.position)
        if item_key:
            self.collect_ground_item(item_key)
            self.player.collected_items.append(f"{self.map.name}:{self.player.position[0]}:{self.player.position[1]}")
            self.map.ground_items.pop(self.player.position, None)
        encounter = self.map.encounters.get(self.player.position)
        if encounter:
            if encounter == "ashen_dragon" and self.player.main_quest_step < 3:
                print(Fore.YELLOW + "The Ashen Dragon's ward blocks you. Complete the main quest steps first.")
                self.player.position = (self.player.position[0] - dx, self.player.position[1] - dy)
                return
            self.handle_encounter(encounter)
        if self.player.position in self.map.portals:
            next_map, spawn = self.map.portals[self.player.position]
            self.player.current_map = next_map
            self.player.position = spawn
            self.map = WorldMap(next_map, self.player)
            print(Fore.MAGENTA + f"You travel to {next_map}.")
        self.save()

    def collect_ground_item(self, item_key):
        if item_key == "sunstone":
            item = {"name": "Sunstone", "type": "quest", "price": 0,
                    "description": "The glowing relic needed to restore Emberfall's ward."}
        else:
            item = make_item(item_key)
        self.player.inventory.add(item)
        print(Fore.YELLOW + f"You collected {item['name']}.")

    def handle_encounter(self, monster_key):
        monster = create_monster(monster_key)
        won = self.combat.fight(monster)
        if won:
            self.map.encounters.pop(self.player.position, None)
            self.player.defeated_encounters.append(f"{self.map.name}:{self.player.position[0]}:{self.player.position[1]}")
            self.player.monsters_defeated += 1
            self.quests.on_monster_defeated(monster_key)
            for drop in monster.drops:
                if drop == "gold":
                    self.player.gold += monster.gold_drop
                    print(Fore.YELLOW + f"You collect {monster.gold_drop} gold.")
                else:
                    self.player.inventory.add(make_item(drop))
            if monster_key == "ashen_dragon":
                self.quests.complete_main_quest()
                self.player.game_won = True
                print(Fore.GREEN + Style.BRIGHT + "THE ASHEN DRAGON IS DEFEATED. EMBERFALL IS SAVED! YOU WIN!")
        self.save()

    def talk(self):
        npc = self.map.npc_at(self.player.position)
        if not npc:
            print(Fore.YELLOW + "Nobody is here to talk to.")
            return
        print(Fore.GREEN + f'{npc.name}: "{npc.dialogue}"')
        self.quests.interact(npc.key)
        if npc.key == "merchant":
            print("The merchant can also be visited from the Shop menu.")

    def inventory_menu(self):
        self.player.inventory.show()
        if not self.player.inventory.items:
            return
        print("Use a potion or equip gear? (U/E, Enter to cancel)")
        action = input("> ").strip().lower()
        if action == "u":
            self.player.inventory.use_item(self.player)
        elif action == "e":
            self.player.inventory.equip_item(self.player)
        elif action:
            print(Fore.RED + "Choose U, E, or Enter.")
        self.save()

    def skill_menu(self):
        self.player.show_skills()
        print("Learn a skill? (L), or use a skill? (U), Enter to cancel")
        action = input("> ").strip().lower()
        if action == "l":
            self.player.learn_skill()
        elif action == "u":
            self.player.use_skill()
        elif action:
            print(Fore.RED + "Choose L, U, or Enter.")
        self.save()

    def shop_menu(self):
        self.shop.visit(self.player)
        self.save()
