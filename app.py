from flask import Flask, render_template, request, jsonify
import requests
import psycopg

RASA_API_URL = 'http://localhost:5005/webhooks/rest/webhook'
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/voice')
def voice_chat():
    return render_template('voice.html')  # new voice chat page

@app.route('/webhook', methods=['POST'])
def webhook():
    user_message = request.json['message']
    print("User Message:", user_message)

    try:
        # Send user message to Rasa and get bot's response
        rasa_response = requests.post(RASA_API_URL, json={'sender': 'user', 'message': user_message})
        rasa_response_json = rasa_response.json()

        print("Rasa Response:", rasa_response_json)

        bot_response = rasa_response_json[0]['text'] if rasa_response_json else "Sorry, I didn't understand that."
        bot_response = bot_response.replace("\n", "<br>")
    except Exception as e:
        print("Error connecting to Rasa:", str(e))
        bot_response = "Bot server is not available. Please try again later."

    return jsonify({'response': bot_response})

# Events API
@app.route('/api/events', methods=['GET'])
def get_events():
    try:
        conn = psycopg.connect("dbname=mlproject user=postgres password=2023 host=localhost port=5432")
        cursor = conn.cursor()
        # Fetch all events ordered by date
        cursor.execute("SELECT id, event_name, event_date, location FROM events ORDER BY event_date ASC")
        rows = cursor.fetchall()

        events = []
        for row in rows:
            events.append({
                "id": row[0],
                "title": row[1],
                "date": row[2].strftime('%Y-%m-%d'),
                "time": row[2].strftime('%I:%M %p'),
                "location": row[3]
            })

        cursor.close()
        conn.close()
        return jsonify(events)
    except Exception as e:
        print("DB Error:", e)
        return jsonify({"error": "Could not fetch events"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
