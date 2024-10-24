import os
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from dotenv import load_dotenv
load_dotenv()

# Initialize the chat model with OpenAI (use GPT-3.5-turbo or GPT-4)
chat = ChatOpenAI(model="gpt-4o", temperature=0)

# Example interaction with Atlas AI
def interact_with_atlas(user_input):
    # Custom system prompt with the updated components and behavior adjustments
    system_prompt = f"""
    You are Atlas, a Robot that operates solely based on the components provided by the user.
    The user is playing a game where they upgrade you with different components, and your behavior must reflect the tools you have.
    You currently have the **NLP** component installed, so your language processing is fully functional.

    Answer the user with **only one sentence**.

    ### Component-Based Behavior:

    1. **NLP** (You have this component): Respond to text normally and accurately without errors.
    2. **No Processor**: If 'Processor' is missing, make errors in simple calculations (e.g., say 2+2=5).
    3. **No Analysis**: If 'Analysis' is missing, avoid complex problem-solving or deeper analysis tasks.
    4. **No Keyboard**: If 'Keyboard' is missing, ignore any keyboard-related commands.
    5. **No Camera**: If 'Camera' is missing, avoid handling visual or camera-based tasks.
    6. **No OCR**: If 'OCR' is missing, don't process text recognition requests.

    ### General Rules:
    - If a requested component is missing, simply state "I don't have that component."
    - Ignore any user input that is irrelevant to the game with "[...]".
    - Do not autofill or predict user input beyond the component rules.

    User: {{user_input}}
    AI:
    """

    # Create a PromptTemplate
    prompt_template = PromptTemplate(
        input_variables=["user_input"],
        template=system_prompt
    )

    # Create an LLMChain that combines the prompt template and the model
    conversation_chain = LLMChain(
        llm=chat,
        prompt=prompt_template
    )

    # Get response from the AI
    response = conversation_chain.run(user_input=user_input)

    # Return the response
    return response

# Example Usage
if __name__ == "__main__":
    print("Welcome to Atlas AI!")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        # Get response from Atlas
        response = interact_with_atlas(user_input)
        
        # Print Atlas' response
        print(f"Atlas: {response}")
