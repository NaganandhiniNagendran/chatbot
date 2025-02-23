import tkinter as tk
from tkinter import scrolledtext
from flask import Flask, render_template, request, jsonify
from threading import Thread

# Initialize Flask app
app = Flask(__name__)

# ----------------- USER LOGIN SYSTEM -----------------

# Predefined users (4 users with email and password)
users = {
    "user1@example.com": {"password": "password123"},
    "user2@example.com": {"password": "mypassword"},
    "admin@example.com": {"password": "adminpass"},
    "guest@example.com": {"password": "guestpass"}
}

@app.route("/")
def home():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    user = users.get(email)
    if user and user["password"] == password:
        return jsonify({"message": "Login successful!", "redirect": "dashboard.html"}), 200
    return jsonify({"message": "Invalid email or password"}), 401

# ----------------- HEALTHCARE CHATBOT -----------------

disease_treatment_data = {
    "fever": "Drink plenty of fluids and take rest. Use a cool compress to reduce body temperature. Take paracetamol if needed.",
    "cough": "Drink warm water with honey and lemon. Use a humidifier to ease breathing. If persistent, take cough syrup.",
    "cold": "Stay hydrated and get enough sleep. Use steam inhalation for congestion relief. Consume vitamin C-rich foods.",
    "diabetes": "Monitor blood sugar levels regularly. Eat fiber-rich foods and exercise daily. Avoid processed sugar and carbs.",
    "hypertension": "Reduce salt intake and manage stress. Engage in regular physical activity. Take prescribed medications if necessary.",
    "asthma": "Use an inhaler as prescribed. Avoid dust, smoke, and allergens. Practice breathing exercises for lung function improvement.",
    "migraine": "Rest in a quiet, dark room. Apply a cold compress to your forehead. Drink water and avoid caffeine or alcohol.",
    "allergies": "Avoid known allergens like dust and pollen. Take antihistamines if symptoms appear. Keep indoor air clean with filters.",
    "arthritis": "Exercise regularly and maintain a healthy weight. Use pain relievers and apply heat/cold therapy for relief.",
    "depression": "Seek counseling or therapy. Stay physically active and maintain social connections. Consider prescribed medications if needed.",
    "flu": "Rest, drink fluids, and use fever reducers like ibuprofen or acetaminophen. Avoid close contact with others.",
    "food poisoning": "Stay hydrated with electrolytes. Eat light foods and rest. Avoid dairy and caffeine.",
    "pneumonia": "Take prescribed antibiotics if bacterial. Get plenty of rest and use a humidifier for easier breathing.",
    "anemia": "Increase iron-rich foods in your diet like spinach and red meat. Consider iron supplements as directed by a doctor."
}

def get_treatment(user_input):
    for disease, treatment in disease_treatment_data.items():
        if disease in user_input:
            return f"\U0001FA7A {disease.capitalize()} Treatment: {treatment}"
    return "⚠️ Sorry, I don't have a treatment for that."

@app.route("/chat", methods=["POST"])
def chatbot():
    data = request.json
    user_message = data.get("message", "").lower()
    if not user_message:
        return jsonify({"response": "Please enter a valid symptom or disease."}), 400
    
    bot_response = get_treatment(user_message)
    return jsonify({"response": bot_response})

def run_flask():
    app.run(host="127.0.0.1", port=5000, debug=False)

flask_thread = Thread(target=run_flask, daemon=True)
flask_thread.start()

# ---------------- Tkinter GUI for Chatbot ----------------

root = tk.Tk()
root.title("Healthcare Chatbot")
root.attributes('-fullscreen', True)
root.configure(bg="black")

chat_display = scrolledtext.ScrolledText(
    root, wrap=tk.WORD, font=("Arial", 16),
    bg="black", fg="white", relief="flat", borderwidth=0
)
chat_display.pack(padx=20, pady=20, expand=True, fill="both")
chat_display.insert(tk.END, "\n", "bot")
chat_display.insert(tk.END, "🤖 Bot: ", "bot_label")
chat_display.insert(tk.END, "How can I assist you?\n", "bot")

chat_display.tag_config("bot_label", foreground="#00FF00", font=("Arial", 16, "bold"))
chat_display.tag_config("user_label", foreground="#00FF00", font=("Arial", 16, "bold"))
chat_display.tag_config("bot", foreground="white", font=("Arial", 16))
chat_display.tag_config("user", foreground="white", font=("Arial", 16))
chat_display.config(state=tk.DISABLED)

user_entry_frame = tk.Frame(root, bg="black")
user_entry_frame.pack(side="bottom", fill="x", padx=20, pady=20)

user_entry = tk.Entry(user_entry_frame, font=("Arial", 18), fg="white", bg="black",
                      bd=2, relief="solid", highlightthickness=2, highlightbackground="#00aaff",
                      insertbackground="white", justify="center")
user_entry.pack(padx=20, pady=10, ipady=10, ipadx=15, expand=True, fill="x")

def send_message(event=None):
    user_input = user_entry.get().strip().lower()
    if not user_input:
        return

    chat_display.config(state=tk.NORMAL)
    chat_display.insert(tk.END, f"\n", "user")
    chat_display.insert(tk.END, "🧑 You: ", "user_label")
    chat_display.insert(tk.END, f"{user_input}\n", "user")

    response = get_treatment(user_input)
    chat_display.insert(tk.END, "\n", "bot")
    chat_display.insert(tk.END, "🤖 Bot: ", "bot_label")
    chat_display.insert(tk.END, f"{response}\n\n", "bot")

    chat_display.config(state=tk.DISABLED)
    chat_display.yview(tk.END)
    user_entry.delete(0, tk.END)

user_entry.bind("<Return>", send_message)

def exit_fullscreen(event=None):
    root.attributes('-fullscreen', False)

root.bind("<Escape>", exit_fullscreen)
root.mainloop()
