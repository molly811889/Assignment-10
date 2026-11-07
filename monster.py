from colorama import Fore

class Monster:
    def __init__(self, name, hp, attack, xp_reward, gold_drop, drops=None):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        self.xp_reward = xp_reward
        self.gold_drop = gold_drop
        self.drops = drops or ["gold"]
        self.color = Fore.RED

    def special_move(self, player):
        return self.attack

class Goblin(Monster):
    def __init__(self):
        super().__init__("Goblin", 35, 9, 35, 8, ["gold", "potion"])

class Wolf(Monster):
    def __init__(self):
        super().__init__("Wolf", 28, 12, 30, 6, ["gold"])

    def special_move(self, player):
        return self.attack + 3

class Skeleton(Monster):
    def __init__(self):
        super().__init__("Skeleton", 45, 10, 45, 10, ["gold", "iron_sword"])

class Troll(Monster):
    def __init__(self):
        super().__init__("Troll", 70, 16, 70, 18, ["gold", "potion"])

    def special_move(self, player):
        return self.attack + 5

class Wraith(Monster):
    def __init__(self):
        super().__init__("Wraith", 55, 18, 60, 14, ["gold", "mana_crystal"])

class AshenDragon(Monster):
    def __init__(self):
        super().__init__("Ashen Dragon", 130, 20, 200, 100, ["gold", "dragon_scale"])
        self.color = Fore.MAGENTA

    def special_move(self, player):
        return self.attack + 8

def create_monster(key):
    monsters = {
        "goblin": Goblin, "wolf": Wolf, "skeleton": Skeleton,
        "troll": Troll, "wraith": Wraith, "ashen_dragon": AshenDragon
    }
    return monsters[key]()
