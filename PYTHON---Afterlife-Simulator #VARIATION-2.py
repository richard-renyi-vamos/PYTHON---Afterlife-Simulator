"""
afterlife_sim.py
A simple Afterlife Simulator (CLI) — extensible, single-file.

Run:
    python afterlife_sim.py

Features:
- Define realms (Heaven, Hell, Reincarnation, Spirit Realm).
- Souls have karma, personality, and memory.
- Each 'life' step evaluates karma + choices + randomness to decide next realm.
- Save/load simulation state to JSON.
- Configurable probabilities and rules (see REALMS config).
"""

import json
import random
import uuid
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional

# -------------------------
# Configuration & constants
# -------------------------

REALMS = {
    "Reincarnation": {
        "description": "Return to a new life on a random world.",
        "base_chance": 0.5
    },
    "Heaven": {
        "description": "Reward realm for high karma and good choices.",
        "base_chance": 0.15
    },
    "Hell": {
        "description": "Challenging realm for negative karma or harmful choices.",
        "base_chance": 0.15
    },
    "SpiritRealm": {
        "description": "A neutral realm for learning and reflection.",
        "base_chance": 0.2
    }
}

# Tune influence of karma and personality on probabilities
KARMA_INFLUENCE = 0.02  # how much one karma point shifts chances
PERSONALITY_INFLUENCE = 0.05  # how much personality trait biases certain realms

# Seed for reproducibility during development (set to None to use real randomness)
RANDOM_SEED = None

# -------------------------
# Models
# -------------------------

@dataclass
class Soul:
    name: str
    uid: str = field(default_factory=lambda: str(uuid.uuid4()))
    karma: int = 0
    personality: Dict[str, float] = field(default_factory=lambda: {"compassion": 0.5, "curiosity": 0.5, "temper": 0.5})
    history: List[Dict] = field(default_factory=list)
    current_realm: str = "Reincarnation"
    lives_left: int = 5  # simulation convenience

    def step_choices(self) -> Dict:
        """
        Simulate a life's choices. Returns a dict with 'action' and karma change.
        This is intentionally simple and random-ish; extend with rules as you like.
        """
        # Weighted choices influenced by personality
        actions = [
            ("help", 1 + int(self.personality["compassion"] * 2)),
            ("learn", 0 + int(self.personality["curiosity"] * 1)),
            ("harm", -2 - int((1 - self.personality["temper"]) * 1.5)),
            ("coast", 0)
        ]
        # Expand into weighted list
        weighted = []
        for name, kchange in actions:
            # base weight depends on personality: compassion -> help, curiosity -> learn, temper -> harm
            weight = 1.0
            if name == "help":
                weight += self.personality["compassion"]
            if name == "learn":
                weight += self.personality["curiosity"]
            if name == "harm":
                weight += (1 - self.personality["temper"])  # low temper -> more likely harm
            weighted.extend([ (name, kchange) ] * max(1, int(weight * 4)))

        choice = random.choice(weighted)
        action, karma_delta = choice
        # small random variation
        karma_delta += random.choice([-1, 0, 1])
        return {"action": action, "karma_delta": karma_delta}

    def to_dict(self):
        return asdict(self)

# -------------------------
# Simulator core
# -------------------------

class AfterlifeSimulator:
    def __init__(self, souls: Optional[List[Soul]] = None):
        if RANDOM_SEED is not None:
            random.seed(RANDOM_SEED)
        self.souls: List[Soul] = souls or []
        self.stats = {"steps": 0, "realm_visits": {r:0 for r in REALMS}}

    def add_soul(self, soul: Soul):
        self.souls.append(soul)

    def step_soul(self, soul: Soul):
        """Simulate one 'life' for a soul, update karma and choose next realm."""
        if soul.lives_left <= 0:
            return None

        # Simulate choices in life
        result = soul.step_choices()
        soul.karma += result["karma_delta"]
        soul.lives_left -= 1

        # Decide next realm based on karma and personality
        next_realm = self.decide_realm(soul)
        event = {
            "action": result["action"],
            "karma_delta": result["karma_delta"],
            "karma_total": soul.karma,
            "next_realm": next_realm
        }
        soul.history.append(event)
        soul.current_realm = next_realm

        # update stats
        self.stats["steps"] += 1
        self.stats["realm_visits"].setdefault(next_realm, 0)
        self.stats["realm_visits"][next_realm] += 1

        return event

    def decide_realm(self, soul: Soul) -> str:
        # Start from base chances
        choices = {}
        for realm, conf in REALMS.items():
            choices[realm] = conf["base_chance"]

        # Modify by karma: positive karma favors Heaven & SpiritRealm, negative favors Hell & Reincarnation
        for realm in choices:
            if realm == "Heaven":
                choices[realm] += soul.karma * KARMA_INFLUENCE
            elif realm == "SpiritRealm":
                choices[realm] += max(0, soul.karma) * (KARMA_INFLUENCE / 2)
            elif realm == "Hell":
                choices[realm] -= soul.karma * KARMA_INFLUENCE
