"""
Run this FIRST, before launching the Streamlit app, to confirm your
Hugging Face token + chosen model actually work.
 
    python test_hf_connection.py
 
If this fails, the Streamlit app will fail too — fix it here first,
it's much faster to debug.
"""
import os
from huggingface_hub import InferenceClient
 
# Put your token here, or set env var HUGGINGFACEHUB_API_TOKEN
TOKEN = os.environ.get("HUGGINGFACEHUB_API_TOKEN", "hf_xxx...")
MODEL = "Qwen/Qwen2.5-7B-Instruct"  # try changing this if it fails
 
client = InferenceClient(model=MODEL, token=TOKEN, provider="hf-inference")
 
try:
    response = client.chat_completion(
        messages=[{"role": "user", "content": "Say hello in one sentence."}],
        max_tokens=50,
    )
    print("SUCCESS:")
    print(response.choices[0].message.content)
except Exception as e:
    print("FAILED:")
    print(e)
    print(
        "\nIf you see a 404 / 'not supported' error, the model isn't served "
        "by any current provider — pick a different one from "
        "https://huggingface.co/models?inference_provider=all&sort=trending "
        "(filter by 'Warm' status).\n"
        "If you see an auth/403 error, check your token has 'Inference' "
        "permission enabled at https://huggingface.co/settings/tokens."
    )
 
