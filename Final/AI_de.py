import importlib

def main():
    print("Select an input method for the AI agent:")
    print("1. Text")
    print("2. Voice")
    print("3. Image")
    choice = input("Enter your choice (1/2/3): ")

    if choice == "1":
        handle_text_input()
    elif choice == "2":
        handle_voice_input()
    elif choice == "3":
        handle_image_input()
    else:
        print("Invalid choice. Please select 1, 2, or 3.")
        main()

def handle_text_input():
    from text import analyze_text
    problem = input("Enter the problem description: ")
    response = analyze_text(problem)
    handle_response(response)

def handle_voice_input():
    from realTimeSpeech import VoiceRecorderApp
    import tkinter as tk

    print("Starting the voice recording application...")
    root = tk.Tk()
    app = VoiceRecorderApp(root)
    root.mainloop()

def handle_image_input():
    from main_visionInjury import process_image
    image_url = input("Enter the URL of the image to analyze: ")
    response = process_image(image_url)
    handle_response(response)

def handle_response(response):
    print("AI Response:", response)
    if "911" in response.lower():
        print("Invoking 911 call...")
        from caller import call
        call()
    else:
        print("No emergency detected. Follow the AI's instructions.")

if __name__ == "__main__":
    while True:
        main()
