import openai

content = "In the light of the moon a little egg lay on a leaf. One Sunday morning the warm sun came up….and POP, out of the egg came a tiny, very hungry caterpillar. He started looking for some food. On Monday he ate through one apple. But he was still hungry. On Tuesday he ate through two pears, but he was still hungry. On Wednesday he ate through three plums, but he was still hungry. On Thursday he ate through four strawberries, but he was still hungry. On Friday he ate through five oranges, but he was still hungry. On Saturday he ate through one piece of chocolate cake, one icecream cone, one pickle, one slice of Swiss cheese, one slice of salami, one lollipop, one piece of cherry pie, one sausage, one cupcake, and one slice of watermelon. That night he had a stomach ache! The next day was Sunday again. The caterpillar ate through one nice leaf, and after that he felt better. Now he wasn't hungry anymore--and he wasn't a little caterpillar anymore. He was a big fat caterpillar. He built a small house, called a cocoon, around himself. He stayed inside for more than two weeks. Then he nibbled a hole in the cocoon, pushed his way out and...He became a beautiful butterfly!"

chat_history = [
    {
        "role": "system",
        "content": f"Instructions: Compose a comprehensive reply to the query using the following content ONLY. Make sure the answer is correct and don't output false content. Ignore outlier queries which have nothing to do with the question. Only answer what is asked. The answer should be short and concise.\n\nContent: {content}"
    },
]

from openai import OpenAI
client = OpenAI(api_key='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')

def ask(prompt):
    chat_history.append({"role": "user", "content": prompt})
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=chat_history,
    )
    chat_history.append({"role": "assistant", "content": response.choices[0].message.content})
    return chat_history[-1]["content"]

import os
while True:
    question = input("User>")
    if question == "!quit" or question == "!exit":
        break
    if question == "!clear":
        os.system("cls")
        continue
    response = ask(question)
    print(f"\n{response}\n")

