import os
from groq import Groq
import geocoder

topic = "8 restaurants of different originals with best ratio of quality/price and 2 fast food place"
topic2 = "7 women's shopping brand with ongoing promotions"
client = Groq(
    # This is the default and can be omitted
    api_key="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",
)
location = geocoder.ip('me')


#Agent 1
senior_research_analyst = client.chat.completions.create(
    messages=[
        {
            "role" : "system",
            "content" : "You are an experienced researchers who looks for related information"
                        f"about {topic}. Find information related to"
                        f"{location.latlng}, open time and estimated driving time"
                        f"Research, analyze and synthesis related information on {topic} from reliable sources"
        },
        {"role" : "user",
        "content": f"Information about {topic}"
                "includes name, open time and estimated driving time."
                f"tranform research findings at {location.latlng} into information"
                "In form of <location name: distance -> estimate driving time. -> best rated dish" 
                "Do not provide any other location information or messages than this"
        },
    ],
    model = "llama-3.3-70b-versatile",
)

#Agent 2 Content Writer
content_writer = client.chat.completions.create(
    messages=[
        {
            "role" : "system",
            "content": "You are an experienced researchers who looks for related information"
                        f"about {topic2}. Find information related to"
                        f"{location.latlng}, open time and estimated driving time"
                        f"Research, analyze and synthesis related information on {topic2} from reliable sources"
        },
        {
            "role": "user",
            "content": f"Information about {topic2}"
                "includes name, open time and estimated driving time."
                f"tranform research findings at {location.latlng} into information"
                "In form of <brand name: distance -> 2 featured promotions" 
                "Do not provide any other location information or messages than this",
        }
    ],
    model = "llama-3.3-70b-versatile",
)
print(senior_research_analyst.choices[0].message.content)
print("\n\n\n")
print(content_writer.choices[0].message.content)



