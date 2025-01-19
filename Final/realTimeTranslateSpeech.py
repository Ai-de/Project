import tkinter as tk
import pyaudio
import wave
import threading
import os
from groq import Groq

class VoiceRecorderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Voice Recorder")
        self.is_recording = False
        self.rate = 44100
        self.frames_per_buffer = 1024
        self.channels = 1
        self.format = pyaudio.paInt16
        self.file_name = "output.wav"
        self.audio = pyaudio.PyAudio()
        self.frames = []
        self.stream = None

        # Button to toggle recording
        self.record_button = tk.Button(
            self.root, text="Start Recording", bg="green", fg="white", font=("Arial", 14),
            command=self.toggle_recording
        )
        self.record_button.pack(pady=20)

    def toggle_recording(self):
        if self.is_recording:
            self.stop_recording()
        else:
            self.start_recording()

    def start_recording(self):
        self.is_recording = True
        self.record_button.config(text="Stop Recording", bg="red")
        self.frames = []
        # Start the audio stream
        self.stream = self.audio.open(
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.frames_per_buffer
        )
        # Run the recording process in a separate thread
        self.recording_thread = threading.Thread(target=self.record_audio)
        self.recording_thread.start()

    def stop_recording(self):
        if self.is_recording:
            self.is_recording = False
            self.record_button.config(text="Start Recording", bg="green")

            # Close the audio stream
            self.stream.stop_stream()
            self.stream.close()
            self.save_audio()

    def record_audio(self):
        while self.is_recording:
            data = self.stream.read(self.frames_per_buffer)
            self.frames.append(data)

    def save_audio(self):
        with wave.open(self.file_name, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.audio.get_sample_size(self.format))
            wf.setframerate(self.rate)
            wf.writeframes(b''.join(self.frames))
        print(f"Audio saved to {self.file_name}")

        self.speech_to_text() # After recording it, revoke the function


    def speech_to_text(self):
        # Initialize the Groq client
        client = Groq(
            api_key="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",
        )

        # Specify the path to the audio file
        filename = os.path.dirname(__file__) + "/output.wav" # Replace with your audio file!

        # Open the audio file
        with open(filename, "rb") as file:
            # Create a transcription of the audio file
            transcription = client.audio.transcriptions.create(
              file=(filename, file.read()),
              model="whisper-large-v3-turbo",
              prompt="Specify context or spelling",  # Optional
              response_format="json",  # Optional
              temperature=0.0  # Optional
            )
            # Print the transcription text
            ai_translation = transcription.text
            print(ai_translation)

        response = client.chat.completions.create(
            messages=[
                {
                    "role" : "system",
                    "content" : f"Il se passe {ai_translation}. Que dois-je faire ? Aidez-moi à ce sujet."
                        f"Si c'est une affaire grave, appelez le 911 et c'est tout, pas besoin d'expliquer davantage. Et dites 'Appeler le 911'."
                        f"Ou si c'est une petite affaire, expliquez-moi ce que je dois faire."

                },
            ],
            model = "llama-3.3-70b-versatile",
        )

        ai_response = response.choices[0].message.content
        print(ai_response)

        def start_call():
            print("Vous appelez le 911!")

        if "Appeler le 911" in ai_response: # Condition: if matches output in "Calling 911"
            start_call() # Revoke the make calling function
        else:
            print("Aucune urgence détectée. Vous pouvez suivre les instructions fournies.")

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceRecorderApp(root)
    root.mainloop()
