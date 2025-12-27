# import sys
# import subprocess
# # The '--user' flag ensures it installs locally for you without needing admin rights
# subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--user', 'google-generativeai'])

# restart kernel

import google.generativeai as genai
import os
import warnings
from dotenv import load_dotenv
warnings.filterwarnings("ignore")

load_dotenv()

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

print("Checking available models...")
print("="*30)

available_models = [] 

try:
    # Fetch models
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            available_models.append(m.name)

    if not available_models:
        print("No available models found.")
    else:
        while True:
            # --- MODEL SELECTION MENU ---
            print("\n" + "="*30)
            print("AVAILABLE MODELS:")
            for i, name in enumerate(available_models):
                print(f"[{i+1}] {name}")
            print("="*30)

            selection = input("Type model number (or 'exit'): ")

            if selection.lower() in ['exit', 'quit']:
                print("Program finished.")
                break

            try:
                index = int(selection) - 1
                if 0 <= index < len(available_models):
                    selected_model_name = available_models[index]
                    print(f"\n---> Selected: {selected_model_name}")
                    
                    try:
                        model = genai.GenerativeModel(selected_model_name)
                        chat = model.start_chat(history=[])
                        
                        print(f"Chat ready! (Type 'back' to change model)")
                        print("-" * 30)

                        # --- CHAT LOOP ---
                        while True:
                            user_input = input("You: ")
                            
                            if user_input.lower() in ['back', 'quit', 'exit']:
                                print("Returning to menu...")
                                break
                            
                            if not user_input.strip():
                                continue

                            try:
                                response = chat.send_message(user_input)
                                print(f"Gemini: {response.text}")
                                print("-" * 30)
                            except Exception as e:
                                # AUTOMATICALLY GO BACK TO MENU ON ERROR
                                print(f"\n[!] Error with this model: {e}")
                                print("[!] Returning to model selection automatically...")
                                break 
                        # -----------------

                    except Exception as e:
                        print(f"Could not initialize model: {e}")

                else:
                    print("Invalid number.")
            except ValueError:
                print("Please enter a valid number.")
    
except Exception as e:
    print(f"Critical Error: {e}")