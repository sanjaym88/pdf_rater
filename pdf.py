import fitz
from groq import Groq


def textextractor(pdfpath):
    doc = fitz.open(pdfpath)
    text = " "
    for page in doc:
        text += page.get_text()
    return text

client = Groq()

pdfpath = r"C:\Users\ADMIN\Desktop\sanjay resume2.pdf"
resumetext = textextractor(pdfpath)

messages = [
    {"role": "system", "content": "You are a seasoned hiring recruiter. Rate the following resume, only giving the score"},
    {"role": "user", "content": resumetext}
]


while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break

    messages.append({"role": "user", "content": user_input})
    print("ChatBot:", end=" ", flush=True)
    reply = ""

    try:
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=messages,
            temperature=0.2,
            max_tokens=1024,
            stream=True,
        )

        for chunk in completion:
            delta = chunk.choices[0].delta.content
            if delta:
                print(delta, end="", flush=True)
                reply += delta

        print()
        if reply.strip():
            messages.append({"role": "assistant", "content": reply.strip()})

    except Exception as e:
        print("\n[Error occurred]", e)