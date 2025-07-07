import fitz
from groq import Groq


def textextractor(pdfpath):
    doc = fitz.open(pdfpath)
    text =""
    for page in doc:
        text += page.get_text()
    return text

client = Groq()

    pdfpath = ""
    resumetext = textextractor(pdf)

