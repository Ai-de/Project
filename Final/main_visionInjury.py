import pyttsx3

# Initialize the Text-to-Speech engine
engine = pyttsx3.init()

# Set properties like voice and speech rate (optional)
engine.setProperty('rate', 150)  # Speed of speech
engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)


# from groq import Groq
# import base64


# # Function to encode the image
# def encode_image(image_path):
#   with open(image_path, "rb") as image_file:
#     return base64.b64encode(image_file.read()).decode('utf-8')

# # Path to your image
# image_path = "C:/Users/phamc/Downloads/a2e7c170-79ba-11ef-8547-c93707d8f8aa.png"

# # Getting the base64 string
# base64_image = encode_image(image_path)

# client = Groq(
#     api_key="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",
# )

# chat_completion = client.chat.completions.create(
#     messages=[
#         {
#             "role": "user",
#             "content": [
#                 {"type": "text", "text": "Provide advice to the image as if a 911 responder and suggest 911 only if urgent and very severe"},
#                 {
#                     "type": "image_url",
#                     "image_url": {
#                         "url": f"data:image/jpeg;base64,{base64_image}",
#                     },
#                 },
#             ],
#         }
#     ],
#     model="llama-3.2-11b-vision-preview",
# )

# print(chat_completion.choices[0].message.content)


from groq import Groq

client = Groq(
     api_key="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",
)
def process_image(image_url):
    completion = client.chat.completions.create(
    model="llama-3.2-11b-vision-preview",
    messages=[
        {
            "role": "system",
            "content": f"Scan for possible problems in {image_url}. Research emergency solution to problems as if a 911 operator, because people might be in danger because of that. Determine whether problem's severity needs 911 or not. keep response concise"
                    "If problem given is severe and requires 911, output content must start '911 dialling...' first. If not a severe emergency, output content can be 'consider calling 311' . Then provide numbered steps and solutions, limited to below 50 words and upper 30 words."
                    "Events that needs 911 are those that can make human bleed, can injure human, related to internal organ of a human, animal abuse, can cause small to catastrophic event"
                    "Events like a small bleeding cut on body or depression will need 113 instead of 911. Any illegal event like burglar, gun fight, thief, robbery, adult fights must call 911"
                    "Else do not mention 911 or 311 in the output content, just give the instructions, limit to below 50 words and upper 20 words"
                    
        },
         {
        "role": "user",
        "content": f"Here is the image URL: {image_url}. Please analyze and respond accordingly."
    }
    ],
    temperature=1,
    max_completion_tokens=1024,
    top_p=1,
    stream=False,
    stop=None,
    )
    engine.say(completion.choices[0].message.content.strip())
    engine.runAndWait() #wait for speech to run

    return completion.choices[0].message.content

