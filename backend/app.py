from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from rr2 import get_resume_score, continue_conversation

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/evaluate")
async def evaluate(
    resume: UploadFile = File(...),
    jd: UploadFile = File(...),
    prompt: UploadFile = File(...),
    session_id: str = Form("default")
):
    resume_bytes = await resume.read()
    jd_text = (await jd.read()).decode("utf-8")
    prompt_text = (await prompt.read()).decode("utf-8")

    score, reason = get_resume_score(resume_bytes, jd_text, prompt_text, session_id)
    return JSONResponse(content={"score": score, "reason": reason})

@app.post("/chat")
async def chat(user_input: str = Form(...), session_id: str = Form("default")):
    reply = continue_conversation(user_input, session_id)
    return JSONResponse(content={"response": reply})


app.mount("/", StaticFiles(directory="../frontend", html=True), name="static")
