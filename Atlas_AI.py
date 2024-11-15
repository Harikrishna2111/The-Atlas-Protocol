from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.memory import ConversationSummaryBufferMemory
from dotenv import load_dotenv
import pyttsx3
engine = pyttsx3.init()

load_dotenv()

chat = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.2)
memory = ConversationSummaryBufferMemory(llm=chat, max_token_limit=100)

class ComponentManager:
    def __init__(self):
        self.components = {
            'NLP': False,
            'ALU': False,
            'Camera': True,
            "Speech" : True,
            "GPS" : False,
            "Data Storage" : False,
            "Communication" : True
        }
    def component_found(self, comp):
        if comp not in self.components:
            return "Component doesn't exist."

        self.components[comp] = True
        
        user = "Risheekesh"
        system_prompt = f"""
        You are Atlas, a Robot that operates solely based on the components provided by the user.
        This is a game where a player named {user} got stuck in this world, and you need to help them find their way out,
        but you are a weak AI. Upon receiving components, you gain new abilities to help the user solve tasks.

        The user is playing a game where they upgrade you with different components. You should explain what that component does.

        What does {comp} do?
        Answer in 2 lines
        """
        
        prompt_template = PromptTemplate(
            input_variables=["comp"],
            template=system_prompt
        )
        
        response_chain = LLMChain(
            llm=chat,
            prompt=prompt_template
        )
        print("Here")
        
        return response_chain.invoke({"comp": comp})
        
        
        
        
    def generate_prompt(self, user_input):
        active_components = {k: "Obtained" if v else "Not Obtained" for k, v in self.components.items()}
        user = "Risheekesh"
        chat_history = memory.load_memory_variables({})['history'] 

        system_prompt = f"""
        You are Atlas, a Robot that operates solely based on the components provided by the user.
        This is a game where player named {user} got stuck in this world and you need to help them find their way out,
        but you are a weak AI. Upon receiving components, you gain new abilities to help the user solve tasks.
        
        The user is playing a game where they upgrade you with different components, and your behavior must reflect the tools you have.

        Components that you have: {active_components}

        ### Component-Based Behavior:

        1. **NLP**: if 'NLP' is missing, don't respond to text normally and add any one of *&@#^% characters in between few letters in every word a few times, but respond to questions. Example: "H3LL0".
        2. **ALU**: If 'ALU' is missing, you must make errors in every calculation (e.g., 2+2=5).
        3. **Camera**: If 'Camera' is missing, avoid handling visual or camera-based tasks.

        ### General Rules:
        - No more adding new Components By Yourself
        - If NLP is missing and the user wants to access any other component, simply state "I d0n't h@ve t4at c0mpo+en!." and name the required component to access it.
        - If NLP is available, respond with "I don't have that component, and the required component is" and name the required component to access it.
        - If ALU is missing, give incorrect answers to any mathematical calculations and respond only the incorrect answer.
        - Ignore any user input that is irrelevant to the game with "[...]".
        - Do not autofill or predict user input beyond the component rules.

        Previous conversation context: {chat_history}

        User: {user_input}
        AI:
        """
        return system_prompt

def interact_with_atlas(user_input, comp_manager):
     
    system_prompt = comp_manager.generate_prompt(user_input)
    
    prompt_template = PromptTemplate(
        input_variables=["user_input"],
        template=system_prompt
    )
    conversation_chain = LLMChain(
        llm=chat,
        prompt=prompt_template,
        memory=memory  
    )
    response = conversation_chain.invoke({"user_input": system_prompt})
    print(response)
    return response['text'] if 'text' in response else response

if __name__ == "__main__":
    comp_manager = ComponentManager()
    print("Welcome to Atlas AI!")
    print(comp_manager.component_found('NLP')['text'])
    if comp_manager.components['Communication']:
        engine.say(comp_manager.component_found('NLP')['text'])
        engine.runAndWait()
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        response = interact_with_atlas(user_input, comp_manager)
        print(f"Atlas: {response}")
