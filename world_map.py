from colorama import Fore
from npc import NPCS

MAPS = {
    "Village": [
        "############",
        "#..........#",
        "#..........#",
        "#..##......#",
        "#..........#",
        "#..........#",
        "#.....##...#",
        "############",
    ],
    "Forest": [
        "##############",
        "#....#.......#",
        "#....#..##...#",
        "#.......#....#",
        "###..#.......#",
        "#....#..###..#",
        "#............#",
        "##############",
    ],
    "Ruins": [
        "################",
        "#....#.........#",
        "#....#..####...#",
        "#..............#",
        "####...#####...#",
        "#..............#",
        "#..####.....#..#",
        "#..............#",
        "################",
    ],
}

ENCOUNTERS = {
    "Village": {(8, 4): "goblin", (9, 5): "wolf"},
    "Forest": {(2, 2): "wolf", (8, 4): "skeleton", (10, 6): "wraith", (10, 4): "troll"},
    "Ruins": {(3, 3): "skeleton", (11, 5): "troll", (13, 6): "ashen_dragon"},
}

PORTALS = {
    "Village": {(10, 1): ("Forest", (1, 1))},
    "Forest": {(1, 6): ("Village", (9, 1)), (12, 1): ("Ruins", (1, 1))},
    "Ruins": {(1, 1): ("Forest", (11, 1))},
}

GROUND_ITEMS = {
    "Village": {(3, 2): "potion"},
    "Forest": {(6, 5): "sunstone"},
    "Ruins": {(7, 3): "leather_armor"},
}

class WorldMap:
    def __init__(self, name, player=None):
        self.name = name if name in MAPS else "Village"
        self.layout = MAPS[self.name]
        self.encounters = dict(ENCOUNTERS[self.name])
        self.portals = PORTALS[self.name]
        self.ground_items = dict(GROUND_ITEMS[self.name])
        if player is not None:
            self.encounters = {
                pos: key for pos, key in self.encounters.items()
                if f"{self.name}:{pos[0]}:{pos[1]}" not in player.defeated_encounters
            }
            self.ground_items = {
                pos: key for pos, key in self.ground_items.items()
                if f"{self.name}:{pos[0]}:{pos[1]}" not in player.collected_items
            }

    def walkable(self, x, y):
        return 0 <= y < len(self.layout) and 0 <= x < len(self.layout[y]) and self.layout[y][x] != "#"

    def npc_at(self, position):
        for npc in NPCS:
            if npc.map_name == self.name and npc.position == position:
                return npc
        return None

    def draw(self, player_pos, player):
        print(Fore.CYAN + f"\n=== {self.name.upper()} ===")
        print(Fore.WHITE + "Legend: @ you | V NPC | M monster | * item | > exit | # wall")
        for y, row in enumerate(self.layout):
            line = ""
            for x, char in enumerate(row):
                pos = (x, y)
                if pos == player_pos:
                    line += Fore.CYAN + "@"
                elif self.npc_at(pos):
                    line += Fore.GREEN + "V"
                elif pos in self.encounters:
                    line += Fore.RED + "M"
                elif pos in self.ground_items:
                    line += Fore.YELLOW + "*"
                elif pos in self.portals:
                    line += Fore.MAGENTA + ">"
                else:
                    line += Fore.WHITE + char
            print(line)
