import streamlit as st
from nltk.chat.util import Chat, reflections

# Expanded fitness-related patterns and responses
patterns = [
    # Greetings and introductory questions
    (r'hello|hi|hey', ['Hello! How can I assist you with your fitness goals?', 'Hi there! Need some fitness advice?']),
    (r'what is your name', ['I am FitBot, your fitness assistant!', 'I am FitBot. How can I help with your fitness?']),
    (r'how are you', ['I am FitBot, always ready to help you stay fit and healthy!', 'I am here to support your fitness journey!']),
    
    # Weight loss and muscle gain
    (r'can you help me lose weight', [
        'Of course! For weight loss, focus on a calorie deficit, regular exercise, and a balanced diet. Would you like advice on workouts or diet plans?']),
    (r'how can i build muscle', [
        'To build muscle, focus on strength training with exercises like squats, deadlifts, and bench presses. Aim for progressive overload and a high-protein diet.']),
    
    # Specific workout routines
    (r'give me a workout plan', [
        'Sure! Here’s a beginner plan: \n1. Monday: Full body workout\n2. Wednesday: Cardio and core\n3. Friday: Strength training\n'
        'Make sure to include warm-ups and cool-downs. Would you like details on any specific exercise?']),
    (r'(.*) abs workout(.*)', [
        'For abs, try exercises like planks, bicycle crunches, and leg raises. Consistency is key!']),
    (r'(.*) leg day workout(.*)', [
        'For leg day, try squats, lunges, and deadlifts. Remember to focus on proper form and warm up well.']),
    (r'(.*) cardio workout(.*)', [
        'Good cardio options include running, cycling, swimming, or HIIT. Aim for at least 30 minutes per session.']),
    (r'how often should i workout', [
        'A balanced plan would be 3-5 times a week, with rest days in between for recovery.']),
    
    # Diet and nutrition
    (r'what should i eat for muscle gain', [
        'For muscle gain, include protein-rich foods like chicken, eggs, legumes, and Greek yogurt. Eat balanced meals with carbs, fats, and proteins.']),
    (r'(.*) healthy diet', [
        'A healthy diet includes fruits, vegetables, lean proteins, whole grains, and healthy fats. Stay hydrated and limit processed foods.']),
    (r'how many calories should i eat', [
        'Caloric needs vary by individual. Generally, for weight loss, aim for a 500-calorie deficit. For muscle gain, aim for a slight surplus.']),
    (r'(.*) protein intake(.*)', [
        'A common recommendation is 1.6-2.2 grams of protein per kilogram of body weight for muscle gain. Need tips on protein sources?']),
    (r'(.*) supplements(.*)', [
        'Supplements like protein powder, creatine, and multivitamins can be beneficial, but it’s best to focus on whole foods first.']),
    
    # Recovery and injury prevention
    (r'how can i improve flexibility', [
        'To improve flexibility, try yoga and dynamic stretching. Stretch daily, especially after workouts.']),
    (r'(.*) recovery tips(.*)', [
        'For recovery, prioritize sleep, hydration, and balanced nutrition. Stretching and foam rolling can also help.']),
    (r'how to prevent injuries', [
        'Warm up properly, use correct form, and avoid overtraining. Listen to your body and allow time for recovery.']),
    
    # Exercise types and benefits
    (r'(.*) benefits of (.*) yoga', [
        'Yoga improves flexibility, reduces stress, and enhances mental focus. It’s a great addition to any fitness routine.']),
    (r'(.*) benefits of (.*) strength training', [
        'Strength training builds muscle, increases metabolism, and improves bone density. It’s beneficial for overall health.']),
    (r'(.*) HIIT workout(.*)', [
        'HIIT (High-Intensity Interval Training) is great for burning calories in a short time. It involves intense bursts of exercise followed by rest.']),
    (r'(.*) resistance training(.*)', [
        'Resistance training builds strength and muscle. It includes exercises with weights, resistance bands, or bodyweight.']),
    
    # Motivation and mindset
    (r'(.*) stay motivated(.*)', [
        'Set achievable goals, track your progress, and remember why you started. Small victories help you stay motivated!']),
    (r'how can i overcome a fitness plateau', [
        'Try changing your workout routine, increasing intensity, or reviewing your diet. Sometimes a small change can break a plateau.']),
    
    # Goodbye and closing statements
    (r'bye|exit|quit', ['Goodbye! Keep up the great work on your fitness journey!', 'See you next time! Stay active and healthy!']),
    (r'(.*)', ["I'm not sure I understand. Can you rephrase or ask me something else related to fitness?"])
]

# Initialize the Chatbot
chatbot = Chat(patterns, reflections)

# Streamlit UI
st.title("Fitness Chatbot - FitBot")
st.markdown("### Chat with FitBot and get fitness advice!")

# Display previous conversation
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Function to display chat history
def display_chat():
    for message in st.session_state.messages:
        if message['role'] == 'user':
            st.write(f"👤 {message['text']}")
        else:
            st.write(f"🤖 {message['text']}")

# User input and chatbot response
user_input = st.text_input("You: ", "")

if st.button("Send") or user_input:
    if user_input:
        st.session_state.messages.append({"role": "user", "text": user_input})
        bot_response = chatbot.respond(user_input)
        st.session_state.messages.append({"role": "bot", "text": bot_response})
    
    display_chat()

# Clear chat history
if st.button("Clear Chat"):
    st.session_state.messages.clear()
    display_chat()
