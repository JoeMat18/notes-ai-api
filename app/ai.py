import openai
import os
from dotenv import load_dotenv
from transformers import pipeline


load_dotenv()

summarizer = pipeline("summarization", model="google/pegasus-xsum")


def summarize_text(text: str) -> str:
    # The model has a limit of ~1024 tokens, so we will trim the text if necessary
    if len(text) > 1000:
        text = text[:1000]

    prompt = "Summarize the following user note:\n" + text

    summary = summarizer(prompt, max_length=100, min_length=30, do_sample=False)
    return summary[0]['summary_text']
