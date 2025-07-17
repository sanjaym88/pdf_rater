from langchain_community.document_loaders import PyMuPDFLoader
from langchain_core.prompts import PromptTemplate
from groq import Groq

def read_text_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

resume_path = r"C:\Users\ADMIN\Desktop\codes\resume1.pdf"
jd_path = r"C:\Users\ADMIN\Desktop\codes\jd.txt"
prompt_path = r"C:\Users\ADMIN\Desktop\codes\prompt.txt"

loader = PyMuPDFLoader(resume_path)
documents = loader.load()
resume_text = "\n".join(doc.page_content for doc in documents)

jd_text = read_text_file(jd_path)
prompt_template = PromptTemplate.from_template(read_text_file(prompt_path))
initial_prompt = prompt_template.format(jd=jd_text, resume=resume_text)

client = Groq()

messages = [
    {"role": "user", "content": initial_prompt}
]

while True:
    user_input = input("You: ")
    if user_input.strip().lower() == "exit":
        break

    messages.append({"role": "user", "content": user_input})
    print("AI:", end=" ", flush=True)
    reply = ""

    try:
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=messages,
            temperature=0.3,
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
