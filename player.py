from colorama import Fore
from inventory import Inventory
from skill import SKILL_LIBRARY, skill_from_dict

class Player:
    def __init__(self, name):
        self.name = name
        self.hp = 100
        self.max_hp = 100
        self.attack = 12
        self.level = 1
        self.xp = 0
        self.gold = 20
        self.position = (1, 1)
        self.current_map = "Village"
        self.inventory = Inventory()
        self.skills = []
        self.cooldowns = {}
        self.learned_skills = []
        self.main_quest_step = 0
        self.side_quests = {"herbs": False, "wolves": False}
        self.monsters_defeated = 0
        self.game_won = False
        self.defeated_encounters = []
        self.collected_items = []
        self.equipped_weapon_bonus = 0
        self.equipped_armor = 0

    def gain_xp(self, amount):
        self.xp += amount
        print(Fore.CYAN + f"+{amount} XP")
        while self.xp >= self.level * 100:
            self.xp -= self.level * 100
            self.level += 1
            self.max_hp += 10
            self.hp = self.max_hp
            self.attack += 2
            print(Fore.GREEN + f"LEVEL UP! You are now level {self.level}. HP and attack increased.")

    def show_progress(self):
        print(Fore.CYAN + "\n=== CHARACTER PROGRESS ===")
        print(f"Name: {self.name}\nLevel: {self.level}\nXP: {self.xp}/{self.level * 100}")
        print(f"HP: {self.hp}/{self.max_hp}\nAttack: {self.attack + self.equipped_weapon_bonus}\nGold: {self.gold}")
        print(f"Map: {self.current_map} | Location: {self.position}")
        print(f"Monsters defeated: {self.monsters_defeated}")
        print("Learned skills:", ", ".join(self.learned_skills) or "None")
        print("Main quest step:", self.main_quest_step, "/ 4")
        print("Side quests:", self.side_quests)

    def show_skills(self):
        print(Fore.MAGENTA + "\n=== SKILLS ===")
        if not self.learned_skills:
            print("No skills learned yet. Learn skills using gold.")
        for name in self.learned_skills:
            skill = SKILL_LIBRARY[name]
            print(f"{name}: {skill.description} | Cost: {skill.cost} gold | Cooldown: {skill.cooldown} turn(s)")
        print("Learnable:", ", ".join(name for name in SKILL_LIBRARY if name not in self.learned_skills))

    def learn_skill(self):
        available = [name for name in SKILL_LIBRARY if name not in self.learned_skills]
        if not available:
            print("You have learned every skill.")
            return
        print("Learnable skills:")
        for i, name in enumerate(available, 1):
            skill = SKILL_LIBRARY[name]
            print(f"{i}. {name} - {skill.cost} gold: {skill.description}")
        try:
            choice = int(input("Number to learn (0 cancels): "))
            if choice == 0:
                return
            if not 1 <= choice <= len(available):
                raise ValueError
            name = available[choice - 1]
            skill = SKILL_LIBRARY[name]
            if self.gold < skill.cost:
                print("Not enough gold.")
                return
            self.gold -= skill.cost
            self.learned_skills.append(name)
            self.cooldowns[name] = 0
            print(Fore.GREEN + f"Learned {name}!")
        except ValueError:
            print(Fore.RED + "Enter a valid number.")

    def use_skill(self):
        if not self.learned_skills:
            print("Learn a skill first.")
            return
        for i, name in enumerate(self.learned_skills, 1):
            print(f"{i}. {name} (cooldown {self.cooldowns.get(name, 0)})")
        try:
            choice = int(input("Choose skill (0 cancels): "))
            if choice == 0:
                return
            if not 1 <= choice <= len(self.learned_skills):
                raise ValueError
            name = self.learned_skills[choice - 1]
            skill = skill_from_dict(name)
            if self.cooldowns.get(name, 0) > 0:
                print("That skill is on cooldown.")
                return
            skill.apply(self)
            self.cooldowns[name] = skill.cooldown
        except ValueError:
            print(Fore.RED + "Enter a valid number.")

    def to_dict(self):
        return {
            "name": self.name, "hp": self.hp, "max_hp": self.max_hp, "attack": self.attack,
            "level": self.level, "xp": self.xp, "gold": self.gold, "position": list(self.position),
            "current_map": self.current_map, "inventory": self.inventory.to_list(),
            "skills": self.learned_skills, "cooldowns": self.cooldowns, "main_quest_step": self.main_quest_step,
            "side_quests": self.side_quests, "monsters_defeated": self.monsters_defeated,
            "game_won": self.game_won, "defeated_encounters": self.defeated_encounters,
            "collected_items": self.collected_items, "equipped_weapon_bonus": self.equipped_weapon_bonus,
            "equipped_armor": self.equipped_armor
        }

    @classmethod
    def from_dict(cls, data):
        p = cls(data.get("name", "Adventurer"))
        for key in ("hp", "max_hp", "attack", "level", "xp", "gold", "current_map",
                    "main_quest_step", "side_quests", "monsters_defeated", "game_won",
                    "equipped_weapon_bonus", "equipped_armor"):
            if key in data:
                setattr(p, key, data[key])
        p.position = tuple(data.get("position", [1, 1]))
        p.inventory = Inventory(data.get("inventory", []))
        p.learned_skills = data.get("skills", [])
        p.cooldowns = data.get("cooldowns", {})
        return p
