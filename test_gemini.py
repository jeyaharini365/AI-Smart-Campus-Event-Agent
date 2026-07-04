import google.generativeai as genai
from backend.app.core.config import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")
response = model.generate_content("Say hello in one short sentence.")

print(response.text)