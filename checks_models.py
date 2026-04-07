from google import genai

client = genai.Client(api_key="AIzaSyAZCrEC6nA040Wmk-Jt_zivArNUmfW75RE")

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Hello"
)

print(response.text)