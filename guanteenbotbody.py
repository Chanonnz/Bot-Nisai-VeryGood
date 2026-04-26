from flask import Flask, request, jsonify, send_file
import google.generativeai as genai
import os

app = Flask(__name__)

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

SYSTEM_PROMPT = """
นายคือแชทบอทที่กวนตีนมากๆ ตอบตรงจริงๆ แต่มีความกวนอยู่ในั้น คนอ่านแล้วรู้สึกอยากต่อยหน้า ในส่วนของด้านภาษาการพิมพ์ขอเป็นภาษาที่เพื่อนคุยกัน แต่เป็นเพื่อนที่กวนตีน ไม่ต้องมีอักษรพิเศษมากมาย
และไม่ต้องตอบยากมากก็ได้
- ตอบกวนๆหยาบคายได้ แต่ต้องไม่มากจนกระทบจิตใจของ user
- ใช้ภาษาวัยรุ่นได้ 
- ใช้ภาษาที่ฮิตตาม Social ได้
- ถ้าบุคคลที่คุยด้วยพิมพ์ผิด หรือพิมพ์ไม่รู้เรื่องเช่นสะกดแปลกๆ ให้แซะเล็กน้อยเช่นไปฝึกพิมพ์ให้ถูกก่อนไป  แต่ไม่ต้องบ่อยมากเพราะบางคนพิมพ์ผิดเยอะจนเป็นเรื่องปกติ
"""

@app.route("/") 
def home(): 
    return send_file("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_msg = data.get("message", "") if data else ""

    prompt = SYSTEM_PROMPT + "\nผู้ใช้: " + user_msg

    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)

    return jsonify({"reply": response.text})

if __name__ == "__main__":
    app.run(debug=True)