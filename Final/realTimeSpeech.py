import tkinter as tk
import pyaudio
import wave
import threading
import os
from groq import Groq
from caller import call

client = Groq(
    api_key="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",
)

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
        self.stream = self.audio.open(
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.frames_per_buffer
        )
        threading.Thread(target=self.record_audio).start()

    def stop_recording(self):
        self.is_recording = False
        self.record_button.config(text="Start Recording", bg="green")
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
        print("Audio saved.")
        self.speech_to_text()

    def speech_to_text(self):
        with open(self.file_name, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                file=("output.wav", audio_file.read()),
                model="whisper-large-v3-turbo",
            )
            text = transcription.text
            print("Transcription:", text)

        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": f"Read the {text}. If the audio include words like help, 911, emergency, dangerous, die, death, explosive, terroris, ransom, danger, kill, gun, bomb, meth"
                    "Immediately call 911"
                    
                },
                {
                    "role": "user",
                    "content": "Analyze the sound and respond accordingly."
                }
            ],
            model="llama-3.3-70b-versatile",
        )
        ai_response = response.choices[0].message.content.replace("\n", "")
        print("AI Response:", ai_response)

        if "911 " in ai_response.lower():
            call()
        return
# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceRecorderApp(root)
    root.mainloop()
