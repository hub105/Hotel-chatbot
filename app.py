from flask import Flask, request, jsonify, render_template_string
from groq import Groq

app = Flask(__name__)

API_KEY = "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"
client = Groq(api_key=API_KEY)

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Grand Atlas Hotel</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Arial, sans-serif; background: #f0f0f0; display: flex; flex-direction: column; height: 100vh; }
        .header { background: #1a1200; color: white; padding: 12px 16px; display: flex; align-items: center; gap: 12px; box-shadow: 0 2px 5px rgba(0,0,0,0.3); }
        .header-avatar { background: #2a2000; border-radius: 50%; width: 45px; height: 45px; display: flex; align-items: center; justify-content: center; font-size: 22px; border: 2px solid #c9a84c; }
        .header-info h2 { font-size: 17px; color: #e8cc85; }
        .header-info p { font-size: 12px; opacity: 0.8; }
        .hero { background: linear-gradient(rgba(0,0,0,0.55), rgba(0,0,0,0.55)), url('https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=800') center/cover; padding: 28px 20px; color: white; text-align: center; }
        .hero h3 { font-size: 20px; margin-bottom: 6px; color: #e8cc85; }
        .hero p { font-size: 13px; opacity: 0.9; margin-bottom: 16px; }
        .hero-buttons { display: flex; gap: 10px; justify-content: center; flex-wrap: wrap; }
        .hero-btn { background: rgba(201,168,76,0.15); border: 2px solid #c9a84c; color: #e8cc85; padding: 8px 18px; border-radius: 20px; font-size: 13px; cursor: pointer; backdrop-filter: blur(4px); }
        .hero-btn:hover { background: #c9a84c; color: #1a1200; }
        .chat-box { flex: 1; overflow-y: auto; padding: 12px 16px; background: #0f0f18; }
        .message { margin: 6px 0; display: flex; flex-direction: column; }
        .message.user { align-items: flex-end; }
        .message.bot { align-items: flex-start; }
        .bubble { max-width: 78%; padding: 10px 14px; border-radius: 18px; font-size: 14px; line-height: 1.6; position: relative; box-shadow: 0 1px 2px rgba(0,0,0,0.3); }
        .user .bubble { background: #2a2010; border: 1px solid #c9a84c; color: #e8cc85; border-bottom-right-radius: 4px; }
        .bot .bubble { background: #1a1a25; border: 1px solid rgba(201,168,76,0.2); color: #e8e0d0; border-bottom-left-radius: 4px; }
        .time { font-size: 10px; color: #666; margin-top: 3px; padding: 0 4px; }
        .input-area { display: flex; padding: 10px 12px; background: #0a0a12; gap: 8px; align-items: center; border-top: 1px solid rgba(201,168,76,0.2); }
        .input-area input { flex: 1; padding: 11px 16px; border: 1px solid rgba(201,168,76,0.3); border-radius: 24px; background: #1a1a25; color: #e8e0d0; font-size: 14px; outline: none; }
        .input-area input::placeholder { color: #666; }
        .input-area input:focus { border-color: #c9a84c; }
        .input-area button { background: linear-gradient(135deg, #c9a84c, #a07830); color: #0a0a12; border: none; border-radius: 50%; width: 44px; height: 44px; font-size: 18px; cursor: pointer; box-shadow: 0 2px 5px rgba(201,168,76,0.3); font-weight: bold; }
        .footer { text-align: center; font-size: 11px; color: #c9a84c; padding: 6px; background: #0a0a12; letter-spacing: 1px; }
    </style>
</head>
<body>
    <div class="header">
        <div class="header-avatar">♛</div>
        <div class="header-info">
            <h2>Grand Atlas Hotel</h2>
            <p>🟢 AI Concierge • Available 24/7</p>
        </div>
    </div>

    <div class="hero">
        <h3>Welcome to Grand Atlas Hotel</h3>
        <p>Luxury Stays • Fine Dining • Spa & Wellness</p>
        <div class="hero-buttons">
            <button class="hero-btn" onclick="quickSend('I want to book a room')">🛏 Rooms</button>
            <button class="hero-btn" onclick="quickSend('Show me dining options')">🍽 Dining</button>
            <button class="hero-btn" onclick="quickSend('Tell me about the spa')">💆 Spa</button>
            <button class="hero-btn" onclick="quickSend('I need airport transfer')">🚗 Transfer</button>
        </div>
    </div>

    <div class="chat-box" id="chat">
        <div class="message bot">
            <div class="bubble">Good evening. I am Aurelius, your personal concierge at The Grand Atlas Hotel powered by Atlas Automations. Whether you wish to reserve a suite, book a dining experience, or explore our world-class amenities — I am entirely at your service. How may I assist you today?</div>
            <div class="time">Now</div>
        </div>
    </div>

    <div class="footer">♛ Powered by Atlas Automations AI</div>

    <div class="input-area">
        <input type="text" id="msg" placeholder="Ask your concierge anything..." />
        <button onclick="send()">➤</button>
    </div>

    <script>
        let messages = [{role:"system", content:"You are Aurelius, an elite luxury hotel AI concierge for The Grand Atlas Hotel by Atlas Automations. Help guests with: room bookings (Deluxe Room 85000 Naira per night, Junior Suite 150000 Naira per night, Presidential Suite 250000 Naira per night), restaurant reservations, spa appointments (massage 25000 Naira, facial 18000 Naira, full package 55000 Naira), airport transfers (15000 Naira one way), check-in time 2pm and check-out time 12pm, swimming pool, gym and all hotel amenities. Collect guest name and preferred dates. Use elegant refined language. Keep responses 2 to 4 sentences. Always end with a warm offer to assist further."}];

        function getTime() {
            return new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
        }

        function addMessage(text, sender) {
            const chat = document.getElementById("chat");
            const div = document.createElement("div");
            div.className = "message " + sender;
            div.innerHTML = '<div class="bubble">' + text + '</div><div class="time">' + getTime() + '</div>';
            chat.appendChild(div);
            chat.scrollTop = chat.scrollHeight;
        }

        async function send() {
            const input = document.getElementById("msg");
            const text = input.value.trim();
            if (!text) return;
            addMessage(text, "user");
            input.value = "";
            messages.push({role: "user", content: text});
            addMessage("typing...", "bot");
            const res = await fetch("/chat", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({messages: messages})
            });
            const data = await res.json();
            const chat = document.getElementById("chat");
            chat.removeChild(chat.lastChild);
            addMessage(data.reply, "bot");
            messages.push({role: "assistant", content: data.reply});
        }

        function quickSend(text) {
            document.getElementById("msg").value = text;
            send();
        }

        document.getElementById("msg").addEventListener("keypress", function(e) {
            if (e.key === "Enter") send();
        });
    </script>
</body>
</html>
'''

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    messages = data["messages"]
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages
    )
    reply = response.choices[0].message.content
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
