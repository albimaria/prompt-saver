from flask import Flask, request, render_template_string
from google import genai
import requests

app = Flask(__name__)

# 🔑 Gemini API
client = genai.Client(api_key="AIzaSyC86tNyDqlPCyXLqLpRlaDmKo1ddtMlGFw")

# 🔑 Unsplash API
UNSPLASH_KEY = "8KZB0VgugEVUKixaQu1IWquA-O-t10N9gA7VP6T8A9E"

history = []

# 📸 Function to fetch image
def get_image(query):
    url = "https://api.unsplash.com/search/photos"
    params = {
        "query": query,
        "client_id": UNSPLASH_KEY,
        "per_page": 1
    }

    res = requests.get(url, params=params).json()

    if res.get("results"):
        return res["results"][0]["urls"]["small"]

    return None


HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>AI Prompt Tool</title>

    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
            background: #FFDAB9; /* 🍑 peach */
            margin: 0;
            color: black;
            overflow-y: auto; 
        }

        h2 {
            text-align: center;
            padding: 20px;
        }

        .chat-container {
            width: 60%;
            margin: auto;
            display: flex;
            flex-direction: column;
            gap: 10px;
            padding-bottom: 120px; 
        }

        .message {
            padding: 12px;
            border-radius: 10px;
            max-width: 70%;
        }

        .user {
            align-self: flex-end;
            background: #4CAF50;
        }

        .ai {
            align-self: flex-start;
            background: #444654;
        }

        img {
            margin-top: 10px;
            border-radius: 10px;
        }

        .input-box {
            position: fixed;
            bottom: 0;
            width: 100%;
            background: #008080; /* 🌊 teal */
            padding: 15px;
            text-align: center;
        }

        input {
            width: 40%;
            padding: 10px;
            border-radius: 8px;
            border: none;
            margin: 5px;
            color: black; /* 👈 important */
        }

        button {
            padding: 10px 20px;
            border: none;
            border-radius: 8px;
            background: #ff7a18;
            color: white;
            font-weight: bold;
            cursor: pointer;
        }

        button:hover {
            background: #16a46b;
        }

        .loader {
            border: 4px solid #ccc;
            border-top: 4px solid #19c37d;
            border-radius: 50%;
            width: 20px;
            height: 20px;
            animation: spin 1s linear infinite;
            margin: auto;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</head>

<body>

<h2>🤖 AI Prompt Chat</h2>

<div class="chat-container">

    {% for p in history %}
        <div class="message user">
            <b>Prompt:</b> {{ p.prompt }} <br>
            <b>Reason:</b> {{ p.reason }}
        </div>

        <div class="message ai">
            <b>AI:</b> {{ p.output }}

            {% if p.image_url %}
                <br><img src="{{ p.image_url }}" width="250">
            {% endif %}
        </div>
    {% endfor %}

</div>

<!-- Input -->
<div class="input-box">
    <form method="POST" onsubmit="showLoader()">
        <input type="text" name="prompt" placeholder="Enter prompt..." required>
        <input type="text" name="reason" placeholder="Reason..." required>
        <button type="submit">Send</button>
    </form>

    <div id="loading" style="display:none;">
        <div class="loader"></div>
    </div>
</div>

<script>
    // Auto scroll
    window.onload = function() {
        window.scrollTo({
            top: document.body.scrollHeight,
            behavior: "smooth"
        });
    };

    // Show loading animation
    function showLoader() {
        document.getElementById("loading").style.display = "block";
    }
</script>

</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def home():
    try:
        if request.method == "POST":
            prompt = request.form.get("prompt")
            reason = request.form.get("reason")

            if not prompt or not reason:
                return render_template_string(HTML, history=history)

            # 🔥 Gemini API with error handling
            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )
                output = response.text if response.text else "No response"

            except Exception:
                output = "⚠️ API limit reached. Please try again later."

            # 📸 Unsplash image
            image_url = get_image(prompt)
            bg_url = get_image(prompt)

            # Save history
            history.append({
                "prompt": prompt,
                "reason": reason,
                "output": output,
                "image_url": image_url
            })

        return render_template_string(HTML, history=history, bg_url=bg_url)

    except Exception as e:
        return f"<h2>Error:</h2><p>{str(e)}</p>"


if __name__ == "__main__":
    app.run(debug=True)