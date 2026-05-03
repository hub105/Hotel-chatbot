from flask import Flask, request, jsonify, render_template_string
from groq import Groq

app = Flask(__name__)

# Replace with your actual Groq API key
API_KEY = "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"
client = Groq(api_key=API_KEY)

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Grand Horizon Hotel | AI Concierge</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Roboto, Arial, sans-serif;
            background: #e9eef3;
            display: flex;
            flex-direction: column;
            height: 100vh;
        }

        /* Header with luxury hotel vibe */
        .header {
            background: #0b2b3b;
            color: #f9e7c2;
            padding: 12px 16px;
            display: flex;
            align-items: center;
            gap: 12px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
            border-bottom: 1px solid #c6a15b;
        }

        .header-avatar {
            background: #1e4a62;
            border-radius: 50%;
            width: 48px;
            height: 48px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 26px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.2);
        }

        .header-info h2 {
            font-size: 18px;
            letter-spacing: 0.5px;
            color: #f5e2b0;
        }

        .header-info p {
            font-size: 12px;
            opacity: 0.85;
            display: flex;
            align-items: center;
            gap: 4px;
        }

        /* Hero section with hotel lobby background */
        .hero {
            background: linear-gradient(rgba(0, 0, 0, 0.55), rgba(0, 0, 0, 0.55)), url('https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800');
            background-size: cover;
            background-position: center 35%;
            padding: 32px 20px;
            color: white;
            text-align: center;
        }

        .hero h3 {
            font-size: 22px;
            margin-bottom: 6px;
            font-weight: 600;
            text-shadow: 1px 1px 3px black;
        }

        .hero p {
            font-size: 14px;
            opacity: 0.9;
            margin-bottom: 18px;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
        }

        .hero-buttons {
            display: flex;
            gap: 12px;
            justify-content: center;
            flex-wrap: wrap;
        }

        .hero-btn {
            background: rgba(255, 248, 225, 0.2);
            backdrop-filter: blur(6px);
            border: 1.5px solid #f5e2b0;
            color: #fff7e8;
            padding: 8px 18px;
            border-radius: 40px;
            font-size: 13px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s ease;
        }

        .hero-btn:hover {
            background: #f5e2b0;
            color: #1e3a4d;
            border-color: #f5e2b0;
        }

        /* Chat container */
        .chat-box {
            flex: 1;
            overflow-y: auto;
            padding: 16px 14px;
            background: #fefaf5;
            scroll-behavior: smooth;
        }

        .message {
            margin: 10px 0;
            display: flex;
            flex-direction: column;
        }

        .message.user {
            align-items: flex-end;
        }

        .message.bot {
            align-items: flex-start;
        }

        .bubble {
            max-width: 80%;
            padding: 10px 16px;
            border-radius: 22px;
            font-size: 14px;
            line-height: 1.5;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.08);
        }

        .user .bubble {
            background: #d9e6f2;
            border-bottom-right-radius: 5px;
            color: #0b2b3b;
        }

        .bot .bubble {
            background: white;
            border-bottom-left-radius: 5px;
            border: 1px solid #efe0c9;
            color: #2c3e2f;
        }

        .time {
            font-size: 10px;
            color: #a0a7ae;
            margin-top: 4px;
            padding: 0 6px;
        }

        /* Input area */
        .input-area {
            display: flex;
            padding: 12px 14px;
            background: #ffffff;
            gap: 12px;
            align-items: center;
            border-top: 1px solid #e2dcd2;
            box-shadow: 0 -2px 6px rgba(0, 0, 0, 0.02);
        }

        .input-area input {
            flex: 1;
            padding: 12px 18px;
            border: 1px solid #ddcfbc;
            border-radius: 40px;
            background: #fefcf8;
            font-size: 14px;
            outline: none;
            transition: 0.2s;
        }

        .input-area input:focus {
            border-color: #c6a15b;
            box-shadow: 0 0 0 2px rgba(198, 161, 91, 0.2);
        }

        .input-area button {
            background: #b88643;
            color: white;
            border: none;
            border-radius: 50%;
            width: 48px;
            height: 48px;
            font-size: 20px;
            cursor: pointer;
            transition: background 0.2s;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .input-area button:hover {
            background: #9b6e36;
        }

        .footer {
            text-align: center;
            font-size: 11px;
            color: #9aaebf;
            padding: 8px;
            background: #f3f0ea;
            border-top: 1px solid #e6dfd3;
        }

        /* small tweaks */
        ::-webkit-scrollbar {
            width: 5px;
        }

        ::-webkit-scrollbar-track {
            background: #f1ede7;
        }

        ::-webkit-scrollbar-thumb {
            background: #b9a577;
            border-radius: 10px;
        }
    </style>
</head>
<body>

<div class="header">
    <div class="header-avatar">🏨</div>
    <div class="header-info">
        <h2>Grand Horizon Hotel</h2>
        <p>🛎️ AI Concierge • 24/7 assistance</p>
    </div>
</div>

<div class="hero">
    <h3>Timeless Elegance & Comfort</h3>
    <p>Ocean views • Premium Suites • Rooftop infinity pool</p>
    <div class="hero-buttons">
        <button class="hero-btn" onclick="quickSend('I would like to book a room at Grand Horizon Hotel')">📅 Book a Room</button>
        <button class="hero-btn" onclick="quickSend('Show me room types and current rates')">🛏️ Rooms & Rates</button>
        <button class="hero-btn" onclick="quickSend('Tell me about your amenities and services')">✨ Amenities</button>
        <button class="hero-btn" onclick="quickSend('I need help planning an event or conference')">🎉 Events & Meetings</button>
    </div>
</div>

<div class="chat-box" id="chat">
    <div class="message bot">
        <div class="bubble">🌟 Welcome to Grand Horizon Hotel! I'm HotelBot, your AI concierge powered by Atlas Automations. 🌴 I can help with room reservations, suite upgrades, spa bookings, local tours, and more. How can I make your stay unforgettable?</div>
        <div class="time">Now</div>
    </div>
</div>

<div class="footer">🏨 Powered by Atlas Automations — Elevating hospitality</div>

<div class="input-area">
    <input type="text" id="msg" placeholder="Ask me about rooms, rates, or concierge..." autocomplete="off">
    <button onclick="send()">➤</button>
</div>

<script>
    // System prompt defines HotelBot's knowledge and tone
    let messages = [{
        role: "system",
        content: "You are HotelBot, a warm, professional AI concierge for Grand Horizon Hotel (operated by Atlas Automations). Help guests with: room reservations (ask for check-in/out dates, number of guests, room category, then provide booking reference like GH- followed by 4 digits), showcase room types: Standard (₦25,000/night), Deluxe (₦35,000/night, includes breakfast), Executive Suite (₦55,000/night), Presidential Suite (₦100,000/night). Amenities: free high-speed Wi-Fi, infinity pool, state-of-the-art gym, full-service spa, gourmet restaurant, 24/7 room service, business center. Check-in 2 PM, check-out 11 AM. Late checkout on request. Cancellation: free up to 24h before arrival. Also assist with local attractions like Lekki Beach, art galleries, city tours, and transport booking. Keep answers 2-4 concise but charming sentences, use polite and elegant tone. Add a personalized touch when possible."
    }];

    function getTime() {
        const now = new Date();
        return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }

    function addMessage(text, sender) {
        const chatDiv = document.getElementById("chat");
        const messageDiv = document.createElement("div");
        messageDiv.className = "message " + sender;
        messageDiv.innerHTML = `<div class="bubble">${escapeHtml(text)}</div><div class="time">${getTime()}</div>`;
        chatDiv.appendChild(messageDiv);
        chatDiv.scrollTop = chatDiv.scrollHeight;
    }

    // simple escape to prevent injection
    function escapeHtml(str) {
        return str.replace(/[&<>]/g, function(m) {
            if (m === '&') return '&amp;';
            if (m === '<') return '&lt;';
            if (m === '>') return '&gt;';
            return m;
        }).replace(/[\uD800-\uDBFF][\uDC00-\uDFFF]/g, function(c) {
            return c;
        });
    }

    async function send() {
        const inputField = document.getElementById("msg");
        const userMsg = inputField.value.trim();
        if (userMsg === "") return;

        addMessage(userMsg, "user");
        inputField.value = "";

        // store user message in conversation history
        messages.push({ role: "user", content: userMsg });

        // Show typing indicator
        const typingDiv = document.createElement("div");
        typingDiv.className = "message bot";
        typingDiv.innerHTML = `<div class="bubble"><em>typing...</em></div><div class="time">${getTime()}</div>`;
        const chatContainer = document.getElementById("chat");
        chatContainer.appendChild(typingDiv);
        chatContainer.scrollTop = chatContainer.scrollHeight;

        try {
            const response = await fetch("/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ messages: messages })
            });
            const data = await response.json();
            const botReply = data.reply || "I'm sorry, I'm having trouble connecting. Please try again.";

            // remove typing indicator
            chatContainer.removeChild(typingDiv);
            addMessage(botReply, "bot");

            // store assistant response
            messages.push({ role: "assistant", content: botReply });
        } catch (error) {
            chatContainer.removeChild(typingDiv);
            addMessage("⚠️ Service interruption. Please refresh or try later.", "bot");
            console.error(error);
        }
    }

    function quickSend(question) {
        const inputBox = document.getElementById("msg");
        inputBox.value = question;
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
    data = request.get_json()
    if not data or "messages" not in data:
        return jsonify({"reply": "Invalid request. Please provide conversation."}), 400
    
    conversation = data["messages"]
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=conversation,
            temperature=0.7,
            max_tokens=300,
        )
        reply = completion.choices[0].message.content
        return jsonify({"reply": reply})
    except Exception as e:
        print("Groq API error:", e)
        return jsonify({"reply": "I'm currently having system issues. Please contact front desk or try again in a moment."}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
