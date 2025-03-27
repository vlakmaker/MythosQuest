from memory_manager import MemoryManager

memory = MemoryManager()

# Test saving some memories
memory.save_memory('choice', 'Sided with commoners')
memory.save_memory('npc', 'Robespierre', {"attitude": "friendly"})

# Test retrieving memories
print("Recent Memories:")
print(memory.get_recent_memories())

memory.close()
