import ollama
from memory_manager import MemoryManager

memory = MemoryManager()

def ai_dungeon_master(player_input):
    """
    Generates AI responses while considering past player choices and historical memory.
    Dynamically suggests next actions based on the historical context.
    """
    # Save player's action
    memory.save_memory('choice', player_input)

    # Retrieve recent memories for AI context
    recent_memories = memory.get_recent_memories(limit=10)
    last_scenario = memory.get_latest_memory_by_type('setting')
    last_character = memory.get_latest_memory_by_type('character')

    # Retrieve past player actions
    past_actions = "\n".join(
        [f"- {mem['description']}" for mem in recent_memories if mem['memory_type'] == 'choice']
    )

    # If no scenario or character exists, re-run setup
    if not last_scenario:
        return choose_historical_period()
    if not last_character:
        return create_character()

    # Filter out irrelevant past actions
    filtered_past_actions = [act for act in recent_memories if 'git' not in act['description'].lower()]

    # Format past actions into narrative context
    past_actions_summary = "\n".join(
        [f"- {mem['description']}" for mem in filtered_past_actions if mem['memory_type'] == 'choice']
    )

    response = ollama.chat(
        model="mistral",
        messages=[
            {"role": "system", "content": (
                "⚠️ YOU ARE A HISTORICAL RPG DUNGEON MASTER. You MUST remain immersive and engaging. "
                "Your responses should include **rich descriptions, emotional weight, and NPC dialogue**. "
                f"The setting is: {last_scenario}. "
                f"The player's character is: {last_character}. "
                f"Past events include:\n{past_actions_summary}. "
                "🎭 **You MUST follow this format:**\n\n"
                "**[🌆 Scene Description]**: (Describe the environment, mood, and current situation)\n"
                "**[💬 NPC Interaction]**: (Make an NPC interact with the player based on their past choices)\n"
                "**[🛠️ Action Consequences]**: (Describe what happens as a result of the player’s last action)\n"
                "**[📜 Choices]**: (Provide 3 roleplay-driven actions that move the story forward)\n\n"
                "🚨 **You MUST stay in character at all times and make the experience engaging!**"
            )},
            {"role": "user", "content": player_input},
        ]
    )

    return response['message']['content']


def load_last_session():
    """
    Loads the most recent scenario and character from memory. 
    If a scenario already exists, skip re-selection.
    """
    last_scenario = memory.get_latest_memory_by_type('setting')
    last_character = memory.get_latest_memory_by_type('character')

    if last_scenario and last_character:
        print(f"\n🕰️ Resuming your last scenario: {last_scenario}\n")
        print(f"\n🎭 Your character: {last_character}\n")
    else:
        if not last_scenario:
            choose_historical_period()
        if not last_character:
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


if __name__ == "__main__":
    print("🎲 Welcome to **MythosQuest: The AI Dungeon Master!**")
    print("📝 Type 'exit' anytime to save and quit.\n")

    load_last_session()  # Load previous session data if available

    while True:
        player_input = input("\n🗣️ **What do you want to do? (Write freely)** ")

        if player_input.lower() == 'exit':
            print("\n💾 Game saved. Come back soon!")
            break

        response = ai_dungeon_master(player_input)
        print("\n" + response + "\n")

    memory.close()
