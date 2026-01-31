from langchain.memory import ConversationBufferMemory

def get_conversation_memory():
    """Create and return conversation memory for the session."""
    return ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key="output"
    )
