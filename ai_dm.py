import ollama
from memory_manager import MemoryManager

memory = MemoryManager()

def ai_dungeon_master(player_input):
    """
    Generates AI responses while considering past player choices and historical memory.
    """
    # Save player's action
    memory.save_memory('choice', player_input)

    # Retrieve recent memories for AI context
    recent_memories = memory.get_recent_memories()
    memory_context = "\n".join(
        [f"{mem['memory_type']}: {mem['description']}" for mem in recent_memories]
    )

    # Generate AI response with memory
    response = ollama.chat(
        model="mistral",
        messages=[
            {"role": "system", "content": f"You are a historical RPG Dungeon Master. Here are recent player decisions:\n{memory_context}"},
            {"role": "user", "content": player_input}
        ]
    )

    return response['message']['content']


def load_last_session():
    """
    Loads the most recent scenario and character from memory.
    """
    recent_memories = memory.get_recent_memories()

    last_scenario = None
    last_character = None

    for mem in recent_memories:
        if mem['memory_type'] == 'setting' and not last_scenario:
            last_scenario = mem['description']
        if mem['memory_type'] == 'character' and not last_character:
            last_character = mem['description']

    if last_scenario:
        print(f"\n🕰️ Resuming your last scenario: {last_scenario}\n")
    else:
        choose_historical_period()

    if last_character:
        print(f"\n🎭 Your character: {last_character}\n")
    else:
        create_character()


def create_character():
    """
    Asks the player to define their character if one is not already saved.
    """
    print("\n🛠️ Let's create your character!")

    name = input("🎭 What is your character's name? ")
    role = input("💼 What is your character's profession? (e.g., Noble Spy, Revolutionary, Soldier) ")
    personality = input("🧠 Describe your character in one sentence: ")

    character_info = f"{name}, a {role} - {personality}"
    memory.save_memory('character', character_info)

    print(f"\n🌟 Welcome, {name} the {role}! Your journey begins...\n")


def choose_historical_period():
    """
    Allows the player to select a historical period if not already saved.
    """
    print("\n📜 Choose a historical period:")
    print("1️⃣ The French Revolution (1789)")
    print("2️⃣ The Fall of Rome (476 AD)")
    print("3️⃣ The Samurai Era (Edo Japan, 1600s)")
    print("4️⃣ World War I Trenches (1914-1918)")
    print("5️⃣ The Age of Exploration (1492-1600)")

    choice = input("\nEnter the number of your chosen period: ")

    historical_scenarios = {
        "1": "The year is 1789, and France is on the brink of revolution. The monarchy trembles as unrest spreads through Paris.",
        "2": "The Western Roman Empire is crumbling. Barbarians press in from all sides, and Rome is a city of fading glory.",
        "3": "Edo Japan is a time of warlords, samurai, and shifting alliances. Honor is everything, but betrayal is common.",
        "4": "The Great War has begun, and trench warfare dominates the battlefield. Will you survive the horrors of the front lines?",
        "5": "The world is expanding. You are an explorer, sailing into the unknown in search of wealth, glory, or something more."
    }

    if choice in historical_scenarios:
        setting = historical_scenarios[choice]
        print(f"\n🌍 You have chosen: {setting}\n")
        memory.save_memory('setting', setting)
    else:
        print("\n⚠️ Invalid choice. Please restart and select a valid number.")


def present_action_choices():
    """
    Gives structured choices for major player decisions.
    """
    print("\n🔹 **Choose an Action:**")
    print("1️⃣ Gather Intelligence")
    print("2️⃣ Infiltrate the Nobility")
    print("3️⃣ Spread Revolutionary Propaganda")
    print("4️⃣ Sabotage Royal Operations")
    print("5️⃣ Build Alliances")
    print("6️⃣ Engage in Espionage")
    print("7️⃣ Assassination")
    print("8️⃣ Escape")


def process_player_choice(choice):
    """
    Converts player choice into a command for the AI.
    """
    actions = {
        "1": "I gather intelligence on the monarchy's movements.",
        "2": "I infiltrate the nobility to uncover secrets.",
        "3": "I spread revolutionary propaganda through pamphlets.",
        "4": "I sabotage the monarchy's operations to weaken their influence.",
        "5": "I form new alliances to strengthen my position.",
        "6": "I engage in espionage, collecting valuable information.",
        "7": "I consider assassinating a key noble figure to further the cause.",
        "8": "I prepare to escape Paris before the situation worsens."
    }
    return actions.get(choice, None)


if __name__ == "__main__":
    print("🎲 Welcome to **MythosQuest: The AI Dungeon Master!**")
    print("📝 Type 'exit' anytime to save and quit.\n")

    load_last_session()  # Load previous session data if available

    while True:
        present_action_choices()
        player_input = input("\n🗣️ **What do you want to do? (Type a number or write freely)** ")

        if player_input.lower() == 'exit':
            print("\n💾 Game saved. Come back soon!")
            break

        if player_input.isdigit() and player_input in "12345678":
            action_description = process_player_choice(player_input)
            response = ai_dungeon_master(action_description)
        else:
            response = ai_dungeon_master(player_input)  # Open-ended freeform text

        print("\n" + response + "\n")

    memory.close()
