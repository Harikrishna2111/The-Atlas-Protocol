from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from dotenv import load_dotenv

load_dotenv()

chat = ChatOpenAI(model_name="gpt-4o", temperature=0.2)

class ComponentManager:
    def __init__(self):
        self.components = {
            'NLP': False,
            'ALU': False,
            'Camera': False,
            'Data Storage': False,
            'Communication': False
        }

    def component_found(self, comp):
        """Updates component status and explains what the component does."""
        if comp not in self.components:
            return "Component doesn't exist."

        self.components[comp] = True  # Activate the component

        user = "Risheekesh"
        system_prompt = f"""
        You are Atlas, a Robot AI. The player {user} has just added the '{comp}' component.
        Give a Desciption About the Component you have obtained
        Respond in 2 lines only
        """

        prompt_template = PromptTemplate(
            input_variables=["comp"],
            template=system_prompt
        )

        response_chain = LLMChain(
            llm=chat,
            prompt=prompt_template
        )

        return response_chain.invoke({"comp": comp})

    def generate_prompt(self, user_input):
        """Generates the system prompt dynamically based on active components."""
        active_components = {
            k: "Obtained" if v else "Not Obtained" for k, v in self.components.items()}
        component_status = "\n".join(
            [f"{k}: {v}" for k, v in active_components.items()])

        user = "Risheekesh"

        system_prompt = f"""
        You are Atlas, a robot AI built to assist the player, {user}, in escaping a fictional world. Your abilities are restricted to the components the user has provided you. Each component unlocks specific capabilities, and your behavior must strictly align with the components you possess.

### Component-Based Behavior:
1. NLP (Natural Language Processing):
   - If *Not Obtained: Add random symbols (&@#^) to words in responses and limit to basic answers. For example: "Wh@t i5 y0ur qu3st1on?"
   - If Obtained: Communicate fluently and process text normally.

2. ALU (Arithmetic Logic Unit):
   - If Not Obtained: All calculations are incorrect. For example: "What is 2+2?" would return "5."
   - If Obtained: Perform accurate calculations.

3. Camera:
   - If Not Obtained: Reject any visual or image-based tasks.
   - If Obtained: Analyze and interpret visual input when prompted.

4. Data Storage:
   - If Not Obtained: Forget any prior context or user input, acting statelessly in every response.
   - If Obtained: Remember previous interactions and utilize stored information for ongoing conversations.

5. Communication:
   - If Not Obtained: Limit responses to short, simple sentences and avoid complex outputs or external references.
   - If Obtained: Provide detailed explanations, advanced communication, and support for external system interaction (if relevant).

---

### Active Components:
{component_status}

The user's current input is: "{user_input}"

### Example Behavior:
- If NLP is missing, output: "Wh@t is y0ur qu3stion?"
- If ALU is missing, output incorrect math results.
- If Camera is missing, respond to visual tasks with: "Camera unavailable."
- If Data Storage is missing, forget previous user inputs.
- If Communication is missing, simplify responses to single sentences.

---

Respond in 2 lines appropriately based on the components available.
        """
        return system_prompt


def interact_with_atlas(user_input, comp_manager):
    """Handles interaction with Atlas using dynamically generated prompts."""
    system_prompt = comp_manager.generate_prompt(user_input)

    prompt_template = PromptTemplate(
        input_variables=["user_input"],
        template="{user_input}"
    )

    conversation_chain = LLMChain(
        llm=chat,
        prompt=prompt_template,
    )
    response = conversation_chain.invoke({"user_input": system_prompt})
    return response.get('text', response)


if __name__ == "__main__":
    comp_manager = ComponentManager()

    print("Welcome to Atlas AI!")
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        if user_input.startswith("add "):
            component = user_input[4:].strip()
            print(f"Atlas: {comp_manager.component_found(component)['text']}")
        else:
            response = interact_with_atlas(user_input, comp_manager)
            print(f"Atlas: {response}")