import random

class Soul:
    """Represents a soul's journey with a karma score."""

    def __init__(self):
        """Initializes a new soul with a starting karma of 0."""
        self.karma = 0

    def add_karma(self, amount):
        """Increases the soul's karma score."""
        self.karma += amount
        print(f"✨ Karma increased by {amount}! (Current: {self.karma})")

    def subtract_karma(self, amount):
        """Decreases the soul's karma score."""
        self.karma -= amount
        print(f"💀 Karma decreased by {amount}! (Current: {self.karma})")

    def check_balance(self):
        """Displays the soul's current karma balance."""
        print(f"🔮 Your current karma is: {self.karma}")

    def reset_karma(self):
        """Resets karma back to 0."""
        self.karma = 0
        print("🌱 Your karma has been reset to 0. A new journey begins!")

def random_event(soul):
    """Applies a random blessing or punishment event."""
    events = [
        ("🌈 A kind spirit blesses you unexpectedly.", 10),
        ("⚡ A shadow curses your soul.", -15),
        ("🌟 You find hidden wisdom in the stars.", 20),
        ("🕸️ A trickster spirit drains your energy.", -10)
    ]
    event, change = random.choice(events)
    print(f"\n[Random Event] {event}")
    if change > 0:
        soul.add_karma(change)
    else:
        soul.subtract_karma(abs(change))

def simulate_afterlife():
    """
    Guides the user through a simple afterlife simulation.
    Choices determine the final karma score and outcome.
    """
    print("🌅 Welcome, weary traveler, to the great unknown.")
    print("A final judgment awaits, based on the choices of your life.")

    my_soul = Soul()

    # --- Scenario 1: A Test of Generosity ---
    print("\n[Scenario 1] You encounter a river of despair. A ghost is unable to cross.")
    print("Do you offer your spiritual energy to help them across?")
    print("1. Yes, I offer my energy. (Risky but compassionate)")
    print("2. No, I must save my strength for my own journey. (Self-serving)")
    choice1 = input("Enter your choice (1 or 2): ")

    if choice1 == '1':
        my_soul.add_karma(20)
        print("A light appears in the river. The ghost thanks you and vanishes.")
    else:
        my_soul.subtract_karma(10)
        print("The ghost wails in sorrow and fades away.")

    # --- Scenario 2: A Test of Honesty ---
    print("\n[Scenario 2] You come across a memory of your past life. A lie you told years ago could be exposed.")
    print("Do you confess the truth to the cosmic scribe or keep it hidden?")
    print("1. Confess the truth. (Painful but honest)")
    print("2. Hide the truth forever. (Easy but deceitful)")
    choice2 = input("Enter your choice (1 or 2): ")

    if choice2 == '1':
        my_soul.add_karma(15)
        print("The scribe nods in approval. The memory brightens.")
    else:
        my_soul.subtract_karma(20)
        print("The memory shimmers and darkens with your deceit.")

    # --- Scenario 3: A Test of Compassion ---
    print("\n[Scenario 3] A child spirit cries alone in the void, afraid and lost.")
    print("Do you stay to comfort them, or continue your journey?")
    print("1. Stay and comfort the child (selfless)")
    print("2. Move on quickly (practical but cold)")
    choice3 = input("Enter your choice (1 or 2): ")

    if choice3 == '1':
        my_soul.add_karma(25)
        print("The child smiles, and your soul shines brighter.")
    else:
        my_soul.subtract_karma(5)
        print("The child fades into silence, and the void grows colder.")

    # --- Random Event ---
    random_event(my_soul)

    # --- Final Judgment ---
    print("\n🌟 Your journey concludes. The cosmic scales weigh your soul...")
    print(f"Your final karma score is: {my_soul.karma}")

    if my_soul.karma > 40:
        print("\n✨ Outcome: The Elysian Fields!")
        print("Your soul is pure and full of light. You have earned a place in the celestial fields of eternal peace.")
    elif 10 <= my_soul.karma <= 40:
        print("\n⚖️ Outcome: Reincarnation!")
        print("Your soul is balanced, with a mix of good and bad deeds. You will be given a new chance to live and learn.")
    else:
        print("\n🌑 Outcome: The Void!")
        print("Your soul is heavy with sorrow and selfishness. You are sent to the desolate void to reflect on your deeds.")

# This block ensures the simulation runs when the script is executed.
if __name__ == "__main__":
    simulate_afterlife()
