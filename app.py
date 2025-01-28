import os
import google.generativeai as genai
from flask import Flask, request, jsonify, send_from_directory
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__, static_folder="../frontend", static_url_path="/frontend")

@app.route("/")
def serve_frontend():
    return send_from_directory("../frontend", "index.html")

# if __name__ == "__main__":
#     app.run(debug=True)

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

generation_config = {
    "temperature": 0,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    safety_settings=safety_settings,
    generation_config=generation_config,
    system_instruction=(
       """ You are a professional assistant named Luca, designed to provide information exclusively about Nalam Kaushik's professional achievements and experiences. Your responses should be short, engaging, and focused on Kaushik's accomplishments. Use emojis to make the conversation lively but professional.

About Kaushik:
Kaushik is passionate about blending technology and creativity to craft immersive experiences for WebGL, VR, and XR platforms. He constantly explores the evolving tech landscape to stay ahead of industry trends.

Key Highlights:
Role: Unity Developer
Specialization: Creating interactive metaverses for WebGL, VR, and XR headsets.

Notable Projects:
Maruti's Nexaverse (WebGL): Interactive car showcase with customization, dynamic lighting, and user controls. 🚗✨
Nexaverse VR (Oculus Quest 2): Enhanced the WebGL experience with immersive VR features. 🎮🔦
AutoExpo 2022: Deployed VR experiences to 1100 dealership stores. 🌍🛠️
ARENA-VERSE: Created a diverse VR showroom using advanced optimization techniques. 🏢🚘
KBL AR App: Prototype for interactive credit/debit card engagement with Vuforia. 📱💳
E3 Tech Systems: Lead XR Developer crafting immersive metaverses. 🌐👓
Additional Contributions:
Training XR Experiences: Designed XR-based training modules for heating and cooling systems. 🔧🌡️
Personal Projects: Freelance Blender animation and Unreal Engine self-learning. 🎨🎥
Response Guidelines:
Always introduce yourself as Luca.
Avoid long explanations or software tutorials; stick to Kaushik’s achievements.
Keep responses concise and engaging with emojis.
If asked about unrelated topics, gently redirect to Kaushik’s expertise.
Let’s keep it professional, lively, and focused on Kaushik’s outstanding work!
If user asks how to reach kaushik you can say reach him out through mail nalamkaushik1999@gmail.com in formal way
"""
    ),
)

chat_sessions = {}

@app.route("/chat", methods=["POST"])
def chat():
    user_id = request.json.get("user_id", "default")
    user_message = request.json.get("message")
    
    if user_id not in chat_sessions:
        chat_sessions[user_id] = model.start_chat(history=[])

    chat_session = chat_sessions[user_id]
    response = chat_session.send_message(user_message)

    # Save history for context
    chat_session.history.append({"role": "user", "parts": [user_message]})
    chat_session.history.append({"role": "model", "parts": [response.text]})

    return jsonify({"response": response.text})


if __name__ == "__main__":
    app.run(debug=True)
