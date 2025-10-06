
import requests
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

class ActionHelloWorld(Action):

     def name(self) -> Text:
         return "action_hello_world"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

         dispatcher.utter_message(text="Hello World!")

         return []


class ActionEmergencyContact(Action):

    def name(self) -> Text:
        return "action_emergency_contact"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        emergency = next(tracker.get_latest_entity_values("emergency_type"), None)
        contacts = {
            "medical": "Call IIT Indore Health Centre: +91-731-243-8700",
            "security": "Campus Security Helpline: +91-731-243-8999",
            "fire": "Fire Station: 101 (or Campus Emergency Fire Line: +91-731-243-8888)",
            "ambulance": "Ambulance No. is 101 "
        }
        if emergency:
            emergency = emergency.lower()

        if emergency in contacts:
            dispatcher.utter_message(text=f"For {emergency} emergencies: {contacts[emergency]}")
        else:
            dispatcher.utter_message(text="Here are the main emergency contacts:\n" \
                       "🚑 Medical: +91-731-243-8700\n" \
                       "🛡 Security: +91-731-243-8999\n" \
                       "🔥 Fire: 101 or +91-731-243-8888")

        return []



    class ActionGetDirections(Action):
        def name(self) -> Text:
            return "action_get_directions"
        def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            location = next(tracker.get_latest_entity_values("location"), None)
            hostel_type = next(tracker.get_latest_entity_values("hostel_type"), None)

            directions = {
                "DA": ("Girls Hostel DA", "https://maps.app.goo.gl/xyz_da"),
                "CVR": ("Boys Hostel CVR", "https://maps.app.goo.gl/44gRUYCxb4491axk8"),
                "APJ": ("Boys Hostel APJ", "https://maps.app.goo.gl/U5zGRvyWMvcjZAEN6"),
                "VSB": ("Boys Hostel VSB", "https://maps.app.goo.gl/HkpA2yF3uLXmNqqJA"),
                "HJB": ("PhD/MTech Hostel HJB", "https://maps.app.goo.gl/K3pmGuReJu5WMhM6A"),
                "JPN": ("PhD/MTech Hostel JPN", "https://maps.app.goo.gl/xyz_jpn"),
                "Kshipra Complex": ("Faculty Housing", "https://maps.app.goo.gl/mLiC6Bhjwn1E8Gzp9"),
                "LHC": ("Lecture Hall Complex", "https://maps.app.goo.gl/qGaai5w4tKrxBX8u6"),
                "Nalanda Auditorium": ("Auditorium", "https://maps.app.goo.gl/RNFtHsCP7vZ5vjcy5"),
                "POD A": ("Lab POD A", "https://maps.app.goo.gl/zSrej9yJkCFyaTQG9"),
                "POD B": ("Lab POD B", "https://maps.app.goo.gl/xyz_pod_b"),
                "POD C": ("Lab POD C", "https://maps.app.goo.gl/xyz_pod_c"),
                "POD D": ("Lab POD D", "https://maps.app.goo.gl/xyz_pod_d"),
                "POD E": ("Lab POD E", "https://maps.app.goo.gl/xyz_pod_e"),
                "Abhinandan Bhavan": ("Admin/Security Office", "https://maps.app.goo.gl/xyz_abhinandan"),
                "Central Dining Facility": ("Mess", "https://maps.app.goo.gl/1qyjJHiJj1P9CEUu5"),
                "Health Centre": ("Campus Health Centre", "https://maps.app.goo.gl/xyz_health"),
                "Dominos": ("Dominos Outlet", "https://maps.app.goo.gl/xyz_dominos"),
                "Nescafe": ("Nescafe Stall", "https://maps.app.goo.gl/xyz_nescafe"),
                "AS Canteen": ("AS Canteen", "https://maps.app.goo.gl/xyz_as"),
                "Village Cafe": ("Village Cafe", "https://maps.app.goo.gl/xyz_village"),
                "Amul": ("Amul Outlet", "https://maps.app.goo.gl/xyz_amul"),
                "Jucilous": ("Juice Shop", "https://maps.app.goo.gl/xyz_jucilous"),
                "Yewale": ("Yewale Tea Stall", "https://maps.app.goo.gl/xyz_yewale"),
            }

            # Hostel categories
            hostel_categories = {
                "girls": ["DA"],
                "boys": ["CVR", "APJ", "VSB"],
                "phd": ["HJB", "JPN"],
                "mtech":["VSB", "JPN"],
                "hospital":["Health Centre"],
                "academic office":["Abhinandan Bhavan"]
            }

            if hostel_type:
                hostel_key = hostel_type.lower()
                if hostel_key in hostel_categories:
                    hostels = hostel_categories[hostel_key]
                    response = f"Here are the {hostel_key} hostels:\n"
                    for h in hostels:
                        response += f"- {h}: {directions[h]}\n"
                    dispatcher.utter_message(text=response)
                    return []

            if location:
                # Normalize: remove 'hostel', strip, and lower-case
                loc_key = location.replace(" hostel", "").replace("Hostel", "").strip()

                # Try exact key (original case)
                if loc_key in directions:
                    name, link = directions[loc_key]
                    dispatcher.utter_message(text=f"{name}\n📍 I've shared the Google Maps link — you can check it on your screen.\n👉 <a href='{link}' target='_blank'>{link}</a>")
                    return []

                # Try uppercase for abbreviations like 'DA'
                if loc_key.upper() in directions:
                    name, link = directions[loc_key.upper()]
                    dispatcher.utter_message(
                        text=f"{name}\n📍 I've shared the Google Maps link — you can check it on your screen.\n👉 <a href='{link}' target='_blank'>{link}</a>"
                    )
                    return []

                # Try title case
                if loc_key.title() in directions:
                    name, link = directions[loc_key.title()]
                    dispatcher.utter_message(
                        text=f"{name}\n📍 I've shared the Google Maps link — you can check it on your screen.\n👉 <a href='{link}' target='_blank'>{link}</a>"
                    )
                    return []

                # Try lowercase (in case keys are added that way)
                if loc_key.lower() in directions:
                    name, link = directions[loc_key.lower()]
                    dispatcher.utter_message(
                        text=f"{name}\n📍 I've shared the Google Maps link — you can check it on your screen.\n👉 <a href='{link}' target='_blank'>{link}</a>"
                    )
                    return []

            dispatcher.utter_message(
                text="Sorry, I couldn't find directions for that place. Try specific hostel/building names.")
            return []

class ActionFetchEvents(Action):
    def name(self):
        return "action_get_events"

    def run(self, dispatcher, tracker, domain):
        time_entity = next(tracker.get_latest_entity_values("time"), None)

        try:
            response = requests.get("http://localhost:5000/api/events")
            if response.status_code != 200:
                dispatcher.utter_message(text="Sorry, I couldn’t fetch event details.")
                return []

            events = response.json()

            if not events:
                dispatcher.utter_message(text="No upcoming events found.")
                return []

            if time_entity == "Latest Events happening in IIT Indore are:":
                # Pick only the first/upcoming event
                event = events[0]
                message = f"📅 Latest Event:\n{event['title']} on {event['date']} at {event['time']} at {event['location']}"
            else:
                # List all events
                message = "📅 Upcoming Events happening in IIT Indore are:\n"
                for event in events:
                    message += f"- {event['title']} on {event['date']} at {event['time']} at {event['location']}\n"

            dispatcher.utter_message(text=message)

        except Exception as e:
            dispatcher.utter_message(text=f"Error connecting to server: {str(e)}")

        return []


class ActionDistance(Action):

    def name(self) -> Text:
        return "action_get_distance"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        point = next(tracker.get_latest_entity_values("transport_type"), None)
        transport = {
            "bus": "Approximately 30-33 km.",
            "railway": "Approximately 24-27 km.",
            "airport": "Approximately 32-35 km. "
        }
        if point:
            point = point.lower()

        if point in transport:
            dispatcher.utter_message(text=(
                f"From {point} it is  {transport[point]}\n\n"
                "Here are the travel options:\n\n"
                "Public Bus: From Bhawarkuan Square, you can take city bus M-19, "
                "which runs at regular intervals, to the IIT Indore Gate.\n\n"
                "Taxi/Cab (Ola/Uber): This is a convenient option from both the railway "
                "station and the airport directly to the IIT campus.\n\n"
                "Local Transport to Bhawarkuan: You can take a bus, shared taxi, or auto-rickshaw "
                "from the railway station to Bhawarkuan Square, and then switch to bus M-19."
            ))
        else:
            dispatcher.utter_message(text="Here are the travel options \n" \
                       "Public Bus: From Bhawarkuan Square, you can take city bus M-19, which runs at regular intervals, to the IIT Indore Gate.\n" \
                       "Taxi/Cab (Ola/Uber): This is a convenient option from both the railway station and the airport directly to the IIT campus.\n" \
                       "Local Transport to Bhawarkuan: You can take a bus, shared taxi, or auto-rickshaw from the railway station to Bhawarkuan Square, and then switch to bus M-19.")

        return []

class ActionAskFeedback(Action):
    def name(self):
        return "action_ask_feedback"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(text="Sure! Please share your feedback.")
        return [SlotSet("waiting_for_feedback", True)]


class ActionSaveFeedback(Action):
    def name(self):
        return "action_save_feedback"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        feedback_text = tracker.latest_message.get("text")
        user_id = tracker.sender_id   # Optional if no authentication

        try:
            response = requests.post(
                "http://localhost:5000/api/feedback",
                json={"feedback": feedback_text, "user_id": user_id}
            )

            if response.status_code == 200:
                dispatcher.utter_message(text="✅ Thanks for your feedback! We appreciate your input.")
            else:
                dispatcher.utter_message(text="❌ Sorry, I couldn’t record your feedback right now.")
        except Exception as e:
            dispatcher.utter_message(text=f"⚠️ Error connecting to feedback server: {e}")

        return [SlotSet("waiting_for_feedback", False)]


directions_map = {
    ("Mess", "DA"): "Exit the mess, turn right, walk straight for 200m, Hostel 1 will be on your left.",
    ("Mess", "LHC"): "Exit the mess, take the main road straight for 500m, LHC is on your right.",
    ("Mess", "Health Centre"): "Walk straight from Mess for 300m, then turn left to reach Health Centre.",
    ("DA", "LHC"): "Exit the Hostel, take the main road straight for 500m, LHC is on your right.",
    ("Sports Complex", "Mess"): "Exit the Ground, take the main road straight for 500m, LHC is on your right.",
    ("Health Centre", "Mess"): "Exit the health centre, turn right, walk straight for 200m, Hostel 1 will be on your left.",
    ("Mess", "APJ"): "Exit the mess, turn right, walk straight for 200m, Hostel 1 will be on your left.",
}

class ActionProvideDirections(Action):

    def name(self) -> Text:
        return "action_provide_directions"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        source = tracker.get_slot("source")
        destination = tracker.get_slot("destination")

        key = (source, destination)
        if key in directions_map:
            dispatcher.utter_message(text=directions_map[key])
        else:
            dispatcher.utter_message(text=f"Sorry, I don't have directions from {source} to {destination} yet.")

        return []


