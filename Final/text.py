import os
from groq import Groq
from twilio.rest import Client

client = Groq(
    api_key="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",
)

def analyze_text(input_text):
    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": f"Scan for possible problems relating to {input_text}. Research solution to problems as if a 911 operator. Determine whether problem's severity needs 911 or not. keep response concise"
                    "If problem given is severe and requires 911, output content must start '911 dialling...' first. If not a severe emergency, output content can be 'consider calling 311' . Then provide numbered steps and solutions, limited to below 50 words and upper 30 words."
                    "Events that needs 911 are those that can make human bleed, can injure human, related to internal organ of a human, animal abuse, can cause small to catastrophic event"
                    "Events like a small bleeding cut on body or depression will need 113 instead of 911. Any illegal event like burglar, gun fight, thief, robbery, adult fights must call 911"
                    "Else do not mention 911 or 311 in the output content, just give the instructions, limit to below 50 words and upper 20 words"
                    
                },
                {
        "role": "user",
        "content": "Needs to be determined if wellbeing enough or not. Please analyze and respond accordingly."
    }
        ],
        model="llama-3.3-70b-versatile",
    )
    return response.choices[0].message.content
