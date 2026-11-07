from dataclasses import dataclass

@dataclass
class NPC:
    key: str
    name: str
    dialogue: str
    position: tuple
    map_name: str

NPCS = [
    NPC("elder", "Elder Rowan", "The ward stones are dimming. Find the Sunstone and stop the Ashen Dragon.", (2, 1), "Village"),
    NPC("herbalist", "Mira the Herbalist", "Wraiths carry mana crystals. Bring one to me, and I will reward you.", (6, 4), "Forest"),
    NPC("guard", "Captain Brann", "The roads are unsafe. Defeat two monsters and I will pay you for protecting travelers.", (2, 5), "Village"),
    NPC("merchant", "Pip the Merchant", "Coins buy supplies, but preparation is worth more than treasure.", (4, 2), "Village"),
    NPC("scholar", "Professor Elowen", "A skill used at the right moment can turn a battle. Watch your cooldowns.", (6, 2), "Ruins"),
]
