import requests
from huggingface_hub import InferenceClient
print("pre fastapi")
from fastapi import FastAPI
print("post fastapi")


def getText(path):
    API_KEY = "K84037285688957"  # Use your API key here
    OCR_URL = "https://api.ocr.space/parse/image"

    # Open an image file
    with open(path, "rb") as image_file:
        payload = {
            "apikey": API_KEY,
            "language": "eng",  # Set language (e.g., "eng" for English, "spa" for Spanish)
            "isOverlayRequired": True  # Get bounding box data
        }
        files = {"file": image_file}

        # Send API request
        response = requests.post(OCR_URL, files=files, data=payload)

    # Parse JSON response
    result = response.json()
    text = result["ParsedResults"][0]["ParsedText"]

    print("Extracted Text:", text)
    return text


def isToxic(ingredients):
    messages = [
        {
            "role": "user",
            "content": f"My sunscreen contains the following ingredients: {ingredients}. \n\n Tell me if it is toxic to aquatic and marine life. Give a concise response as an informatory chatbot instead of a conversational Large Language Model."
        }
    ]

    client = InferenceClient(api_key="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")

    completion = client.chat.completions.create(
        model="Qwen/Qwen2.5-Coder-32B-Instruct",
        messages=messages,
        max_tokens=10000
    )

    return completion.choices[0].message['content']

app = FastAPI()

@app.post("/")
def getResponse(path: str):
    text = getText(path)
    response = isToxic(text)
    print(response)
    return {
        "response": response
    }