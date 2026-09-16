from chatbot_backend import create_initial_conversation, get_sampling_params, generate_response

def run_cli_bot():
    print("\n--- Starting your Custom Chatbot Loop ---")
    print("Type 'exit' or 'quit' at any point to end the session.\n")
    
    # Initialize stateful conversation tracker
    conversation = create_initial_conversation()
    
    # Setup generation boundaries
    sampling_params = get_sampling_params(temperature=0.7, max_tokens=200, top_p=0.9)
    
    while True:
        user_input = input("You: ")
        if user_input.lower().strip() in ["exit", "quit"]:
            print("Goodbye!")
            break
            
        if not user_input.strip():
            continue
            
        # 1. Append user statement to history tracking
        conversation.append({"role": "user", "content": user_input})
        
        # 2. Run Inference on backend cluster
        try:
            bot_reply = generate_response(conversation, sampling_params)
            
            # 3. Print structural output answer
            print(f"Bot: {bot_reply}\n")
            
            # 4. Save Bot feedback to sustain state logic context
            conversation.append({"role": "assistant", "content": bot_reply})
            
        except Exception as e:
            print(f"An inference error occurred: {e}")

if __name__ == "__main__":
    run_cli_bot()
