import os

import re

from datetime import datetime
from dotenv import load_dotenv
from google import genai

load_dotenv()

client=genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

def ask_ai_for_manim_code(user_prompt):  # Define a function that takes one argument

    system_instruction = (  # Start a multi-line string (using brackets for readability)

        "You are an expert in Python and the Manim animation library. "  # Role assignment

        "When given a request, generate ONLY valid Python code using Manim. "  # Output constraint

        "CRITICAL FONT RULES: You must NEVER use Tex() or MathTex(). "  # Crash prevention rule

        "You must ONLY use the standard Text() class for all text. "  # Crash prevention rule

        "Never use Unicode superscripts such as ². Use a^2, b^2 and c^2 instead. "

        "Do not include any explanations or additional text. "  # No chatty output

        "Just output the raw code block."  # Pure code output only

    )  # End of system_instruction string

    full_prompt = f"{system_instruction}\n\nUser Request: {user_prompt}"  # Combine both strings

    print(f"Sending prompt to Gemini, please wait...")  # Show feedback to the user

    response = client.models.generate_content(  # Call the Gemini API
        model='gemini-2.5-flash',  # Specify which AI model to use
        contents=full_prompt,      # Send our combined prompt
    )  # End of API call

    return response.text  # Return just the text part of the response

def extract_python_code(raw_text):  # Define function, takes raw AI response as input

    backticks = chr(96) * 3  # Create the ``` string safely using character code

    pattern = rf"{backticks}(?:python)?\n(.*?)\n{backticks}"  # Define the regex search pattern

    match = re.search(pattern, raw_text, re.DOTALL)  # Run the search

    if match:  # If a code block was found...
        return match.group(1).strip()  # Return ONLY the captured code, trimmed

    return raw_text.strip()  # Fallback: if no fences found, return as-is

if __name__ == '__main__':  # Only run this block when executed directly

    print('\n' + '=' * 50)  # Print a separator line (= repeated 50 times)

    print('Welcome to the AI Animation Generator!')  # Print welcome message

    print("Type your idea, or type 'quit' to exit.")  # Print instructions

    print('=' * 50)  # Print closing separator

    while True:  # Start an infinite loop - runs forever until broken

        user_request = input('\nEnter your animation idea: ')  # Wait for user input

        if user_request.lower() in ['quit', 'exit']:  # Check for exit commands
            print('Shutting down. Goodbye!')  # Print goodbye message
            break  # Exit the while loop entirely

        if user_request.strip() == '':  # Check if user pressed Enter with no text
            continue  # Skip to next loop iteration (ignore blank input)

        result = ask_ai_for_manim_code(user_request)  # STEP 1: Call AI, get raw response

        cleaned_code = extract_python_code(result)  # STEP 2: Clean the response

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')  # STEP 3: Create timestamp
        
        output_filename = f'animation_{timestamp}.py'

        with open(output_filename, 'w') as f:
            f.write(cleaned_code)

        print(f'Success! Saved as -> {output_filename}')
