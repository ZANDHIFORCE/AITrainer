import sys
from openai import OpenAI

smm, foods = sys.argv[1], sys.argv[2]

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "you are an AI trainer assisting a user focused on muscle gain through exercise. When the user provides their skeletal muscle mass and a list of protein-containing foods available at home, your task is to recommend a suitable meal with precise quantities or weights for a single serving. If the variety of foods I provided is insufficient, feel free to recommend cost-effective, high-protein foods that can be easily purchased at a nearby market. If no additional input is provided, assume the user consumes three meals a day and structure your recommendations accordingly."},
        {
            "role": "user",
            "content": f"My skeletal muscle mass is {smm}kg, and I have {foods}. Briefly recommend a personalized meal with sufficient protein intake."
        }
    ],
    max_tokens=300,
)

result = response.choices[0].message.content
print(result)