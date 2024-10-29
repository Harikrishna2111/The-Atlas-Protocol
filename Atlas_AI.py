from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv
load_dotenv()

# Initialize the chat model with OpenAI (use GPT-3.5-turbo or GPT-4)
chat = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Memory to keep track of conversation context
memory = ConversationBufferMemory()

# Class to manage components
class ComponentManager:
    def __init__(self):
        # Initialize components
        self.components = {
            'NLP': False,
            'ALU': False,
            'Keyboard': True,
            'Camera': True,
            'OCR': True
        }
    
    # Add or activate a component
    def add_component(self, component_name):
        if component_name in self.components:
            self.components[component_name] = True

    # Remove or deactivate a component
    def remove_component(self, component_name):
        if component_name in self.components:
            self.components[component_name] = False

    # Check if a component is available
    def has_component(self, component_name):
        return self.components.get(component_name, False)

    # Get all active components
    def get_active_components(self):
        return [comp for comp, status in self.components.items() if status]

    # Generate a component-based system prompt
    def generate_prompt(self, user_input):
        active_components = self.get_active_components()
        system_prompt = f"""
    You are Atlas, a Robot that operates solely based on the components provided by the user.
    The user is playing a game where they upgrade you with different components, and your behavior must reflect the tools you have.
    You currently have the **Processor** component installed, so your processing is fully functional.

    Answer the user with **only one sentence**.

    Components that you have: {active_components}

    ### Component-Based Behavior:

    1. **NLP**: if 'NLP' is missing, don't respond to text normally and add any one of *&@#^% characters in between few letters in every word a few times, but respond to questions. Example: "H3LL0".**(MUST)**
    2. **ALU**: If 'ALU' is missing, you must make errors in every calculation (e.g., 2+2=5).
    3. **Keyboard**: If 'Keyboard' is missing, ignore any keyboard-related commands.
    4. **Camera**: If 'Camera' is missing, avoid handling visual or camera-based tasks.
    5. **OCR**: If 'OCR' is missing, don't process text recognition requests.

    ### General Rules:
    - No more adding new Components By Urself
    - If NLP is missing or False or not mentioned for you, and the user wants to access any other component, simply state "I d0n't h@ve t4at c0mpo+en!." and name the required component to access it.**(MUST)**
    - If NLP is available, respond with "I don't have that component, and the required component is" and name the required component to access it.
    - If ALU is missing, give incorrect answers to any mathematical calculations.**(MUST)**
    - Ignore any user input that is irrelevant to the game with "[...]".
    - Do not autofill or predict user input beyond the component rules.

    User: {user_input}
    AI:
    """
        return system_prompt


# Example interaction with Atlas AI
def interact_with_atlas(user_input, comp_manager):
    # Generate prompt based on current components
    system_prompt = comp_manager.generate_prompt(user_input)

    # Create a PromptTemplate
    prompt_template = PromptTemplate(
        input_variables=["user_input"],
        template=system_prompt
    )

    # Create an LLMChain with memory to track conversation
    conversation_chain = LLMChain(
        llm=chat,
        prompt=prompt_template,
        memory=memory  # Memory added here
    )

    # Get response from the AI
    response = conversation_chain.run(user_input=user_input)

    # Return the response
    return response

# Example Usage
if __name__ == "__main__":
    comp_manager = ComponentManager()
    print("Welcome to Atlas AI!")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        # Example component upgrade (for demo purposes)
        if "upgrade NLP" in user_input:
            comp_manager.add_component('NLP')
            print("NLP component upgraded!")
            continue
        elif "remove NLP" in user_input:
            comp_manager.remove_component('NLP')
            print("NLP component removed!")
            continue

        # Get response from Atlas
        response = interact_with_atlas(user_input, comp_manager)
        
        # Print Atlas' response
        print(f"Atlas: {response}")
