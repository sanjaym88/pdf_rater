from langchain_community.document_loaders import PyMuPDFLoader
from langchain_core.prompts import PromptTemplate
from groq import Groq
import tempfile

client = Groq()
message_store = {} 

def get_resume_score(resume_bytes, jd_text, prompt_text, session_id="default"):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
        temp_pdf.write(resume_bytes)
        temp_pdf_path = temp_pdf.name

    loader = PyMuPDFLoader(temp_pdf_path)
    documents = loader.load()
    resume_text = "\n".join(doc.page_content for doc in documents)

    prompt_template = PromptTemplate.from_template(prompt_text)
    formatted_prompt = prompt_template.format(jd=jd_text, resume=resume_text)

    messages = [{"role": "user", "content": formatted_prompt}]
    reply = ""

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
            reply += delta

    messages.append({"role": "assistant", "content": reply.strip()})
    message_store[session_id] = messages
    score = extract_score(reply)
    return score, reply.strip()

def continue_conversation(user_input, session_id="default"):
    if session_id not in message_store:
        return "Session expired. Please re-upload your resume."

    messages = message_store[session_id]
    messages.append({"role": "user", "content": user_input})
    reply = ""

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
            reply += delta

    messages.append({"role": "assistant", "content": reply.strip()})
    return reply.strip()

def extract_score(text):
    import re
    match = re.search(r"\b([0-9]|10)\b", text)
    return int(match.group(1)) if match else -1
