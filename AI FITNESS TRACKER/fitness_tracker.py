import cv2
import mediapipe as mp
import numpy as np
import streamlit as st
import pandas as pd
from datetime import date
from PIL import Image
import io
import time

# Initialize mediapipe and drawing utilities
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
# Page configuration
st.set_page_config(page_title="Fitness Tracker", layout="centered", page_icon="🏋")

st.markdown("""
    <style>
    /* Adjust font size for headers */
    h1, h2, h3, h4, h5, h6 {
        font-size: 24px !important;
    }
    /* Adjust font size for all body text */
    .streamlit-expanderHeader, .big-font, p, li, div, span {
        font-size: 18px !important;
    }
    /* Adjust button text size */
    .stButton > button {
        font-size: 18px !important;
    }
    /* Adjust sidebar title */
    .css-1p4r0a6 {
        font-size: 20px !important;
    }
    </style>
""", unsafe_allow_html=True)


    # Initialize session state for navigation and user profile
if 'page' not in st.session_state:
    st.session_state.page = "Dashboard"
if 'user_profile' not in st.session_state:
    st.session_state.user_profile = {"Name": "", "Age": 0, "Weight": 0, "Goal": ""}

def navigate_to(page_name):
    st.session_state.page = page_name


# Sidebar navigation with user profile input
with st.sidebar:
    st.header("🌟 Fitness Tracker")
    st.button("🏋 Dashboard", on_click=navigate_to, args=("Dashboard",))
    st.button("📝 Log Workout", on_click=navigate_to, args=("Log Workout",))
    st.button("🍽 Log Food Intake", on_click=navigate_to, args=("Log Food",))
    st.button("💤 Log Sleep Routine", on_click=navigate_to, args=("Log Sleep",))
    st.button("💪 Rep Calculator", on_click=navigate_to, args=("Rep Calculator",))
    st.button("📜 View History", on_click=navigate_to, args=("History",))
    st.button("📊 Summary Analysis", on_click=navigate_to, args=("Summary",))

    # User Profile Section
    st.header("👤 User Profile")

    # User Profile Form
    with st.form("user_profile_form"):
        name = st.text_input("Name", st.session_state.user_profile["Name"])
        age = st.number_input("Age", min_value=0, max_value=100, value=st.session_state.user_profile["Age"], step=1)
        weight = st.number_input("Weight (kg)", min_value=0, max_value=300, value=st.session_state.user_profile["Weight"], step=1)
        goal = st.text_input("Fitness Goal", st.session_state.user_profile["Goal"])
        submitted = st.form_submit_button("Update Profile")

    # Update profile information
    if submitted:
        st.session_state.user_profile = {"Name": name, "Age": age, "Weight": weight, "Goal": goal}
        st.success("Profile updated successfully!")

    # Display user profile
    st.write("### Profile Summary")
    st.write(f"*Name*: {st.session_state.user_profile['Name']}")
    st.write(f"*Age*: {st.session_state.user_profile['Age']} years")
    st.write(f"*Weight*: {st.session_state.user_profile['Weight']} kg")
    st.write(f"*Goal*: {st.session_state.user_profile['Goal']}")


# Define functions to save and load data
def save_data(filename, new_data):
    try:
        data = pd.read_csv(filename)
        data = pd.concat([data, new_data], ignore_index=True)
    except FileNotFoundError:
        data = new_data
    data.to_csv(filename, index=False)

def load_data(filename):
    try:
        data = pd.read_csv(filename)
    except FileNotFoundError:
        data = pd.DataFrame()
    return data

    # User Profile Section
    st.header("👤 User Profile")
    with st.form("user_profile_form"):
        name = st.text_input("Name", st.session_state.user_profile["Name"])
        age = st.number_input("Age", min_value=0, max_value=100, value=st.session_state.user_profile["Age"], step=1)
        weight = st.number_input("Weight (kg)", min_value=0, max_value=300, value=st.session_state.user_profile["Weight"], step=1)
        goal = st.text_input("Fitness Goal", st.session_state.user_profile["Goal"])
        submitted = st.form_submit_button("Update Profile")

    # Update profile information
    if submitted:
        st.session_state.user_profile = {"Name": name, "Age": age, "Weight": weight, "Goal": goal}
        st.success("Profile updated successfully!")

    # Display user profile
    st.write("### Profile Summary")
    st.write(f"*Name*: {st.session_state.user_profile['Name']}")
    st.write(f"*Age*: {st.session_state.user_profile['Age']} years")
    st.write(f"*Weight*: {st.session_state.user_profile['Weight']} kg")
    st.write(f"*Goal*: {st.session_state.user_profile['Goal']}")

# Define functions to save and load data
def save_data(filename, new_data):
    try:
        data = pd.read_csv(filename)
        data = pd.concat([data, new_data], ignore_index=True)
    except FileNotFoundError:
        data = new_data
    data.to_csv(filename, index=False)

def load_data(filename):
    try:
        data = pd.read_csv(filename)
    except FileNotFoundError:
        data = pd.DataFrame()
    return data
# Dashboard Page
if st.session_state.page == "Dashboard":
    st.title("🏃 Welcome to Your Fitness Dashboard")
    st.subheader("Track your progress, reach your goals, and stay motivated!")
    st.markdown("'The only bad workout is the one you didn't do.'", unsafe_allow_html=True)

    # Quick Stats Summary
    st.write("### 💪 Quick Stats")
    workout_data = pd.DataFrame({"Date": [date.today()], "Workout": ["Running"], "Duration (min)": [30], "Calories Burned": [300]})
    food_data = pd.DataFrame({"Date": [date.today()], "Calories Intake": [2000]})
    sleep_data = pd.DataFrame({"Date": [date.today()], "Sleep Duration (hours)": [7]})

    total_workouts = workout_data.shape[0]
    total_calories_burned = workout_data["Calories Burned"].sum()
    total_calories_intake = food_data["Calories Intake"].sum()
    avg_sleep = sleep_data["Sleep Duration (hours)"].mean()

    st.write(f"- *Total Workouts Logged*: {total_workouts}")
    st.write(f"- *Total Calories Burned*: {total_calories_burned} kcal 🔥")
    st.write(f"- *Average Daily Sleep*: {avg_sleep:.1f} hours 🌙")
    
    # Motivational Message
    st.write("### 🌟 Stay Motivated")
    st.info("Remember, progress is progress, no matter how small. Keep pushing toward your goals every day!")

    # Goals & Achievements
    st.write("### 🎯 Goals & Achievements")
    st.write("Set and monitor your daily fitness, diet, and sleep goals. Celebrate your milestones along the way!")
    
    # Achievements Display
    if total_calories_burned > 5000:
        st.success("🎉 Milestone Achieved: Burned 5000 calories! Amazing job!")
    elif total_workouts >= 10:
        st.success("🏆 Milestone Achieved: Logged 10 workouts! Keep up the consistency!")

    # Tips and Recommendations
    st.write("### 📈 Tips for Improved Fitness")
    st.markdown(
        """
        - *Stay Hydrated*: Drinking water helps regulate body temperature and keeps you energized.
        - *Focus on Nutrition*: Balanced meals help you recover faster and improve workout results.
        - *Get Enough Rest*: Quality sleep is essential for muscle recovery and mental well-being.
        - *Stay Consistent*: Consistency over intensity brings sustainable results.
        """
    )

    # Visual Progress Indicator (Example Data)
    st.write("### 📊 Weekly Progress")
    sample_data = pd.DataFrame({
        "Date": pd.date_range(end=date.today(), periods=7),
        "Calories Burned": [300, 400, 450, 500, 350, 600, 700]
    })
    sample_data.set_index("Date", inplace=True)
    st.line_chart(sample_data["Calories Burned"])

# Log Workout Page
if st.session_state.page == "Log Workout":
    st.title("📝 Log Your Workout")
    with st.form("workout_form"):
        workout_type = st.selectbox("Select Workout Type", ["Running", "Cycling", "Weight Lifting", "Yoga", "Other"])
        duration = st.number_input("Duration (minutes)", min_value=1, step=1)
        calories_burned = st.number_input("Calories Burned", min_value=1, step=1)
        workout_date = st.date_input("Workout Date", value=date.today())
        submitted = st.form_submit_button("Add Workout")

    if submitted:
        new_data = pd.DataFrame({"Date": [workout_date], "Workout": [workout_type], "Duration (min)": [duration], "Calories Burned": [calories_burned]})
        save_data("workout_history.csv", new_data)
        st.success("Workout logged successfully!")

# Log Food Intake Page
if st.session_state.page == "Log Food":
    st.title("🍽 Log Your Food Intake")
    with st.form("food_form"):
        food_item = st.text_input("Food Item")
        calories_intake = st.number_input("Calories Intake", min_value=1, step=1)
        food_date = st.date_input("Food Date", value=date.today())
        submitted = st.form_submit_button("Add Food Intake")

    if submitted:
        new_data = pd.DataFrame({"Date": [food_date], "Food Item": [food_item], "Calories Intake": [calories_intake]})
        save_data("food_history.csv", new_data)
        st.success("Food intake logged successfully!")

# Log Sleep Routine Page
if st.session_state.page == "Log Sleep":
    st.title("💤 Log Your Sleep Routine")
    with st.form("sleep_form"):
        sleep_hours = st.number_input("Sleep Duration (hours)", min_value=1, max_value=12, step=1)
        sleep_date = st.date_input("Sleep Date", value=date.today())
        submitted = st.form_submit_button("Add Sleep Record")

    if submitted:
        new_data = pd.DataFrame({"Date": [sleep_date], "Sleep Duration (hours)": [sleep_hours]})
        save_data("sleep_history.csv", new_data)
        st.success("Sleep record logged successfully!")


# Rep Calculator Page
if st.session_state.page == "Rep Calculator":
    st.title("💪 Rep Calculator")
    st.subheader("Use your webcam to calculate the number of reps during your exercise.")

    # Initialize webcam video capture
    video_capture = cv2.VideoCapture(0)

    # Define a placeholder for the video frames
    frame_placeholder = st.empty()

    # Initialize Mediapipe Pose detection
    mp_pose = mp.solutions.pose
    mp_drawing = mp.solutions.drawing_utils
    pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

    # Rep counting variables
    stage = "down"
    counter = 0

    # Placeholder model function (to calculate reps)
    def calculate_angle(a, b, c):
        # Calculate angle between three points
        angle = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
        angle = np.abs(angle)
        if angle > np.pi:
            angle = 2 * np.pi - angle
        return np.degrees(angle)

    # Check if the webcam opened successfully
    if not video_capture.isOpened():
        st.error("Error: Could not open video.")
    else:
        st.write("Webcam feed is live. Press 'Stop' to end.")
        var=st.button("stop")
        # Stream and process frames
        while video_capture.isOpened():
            ret, frame = video_capture.read()  # Capture frame-by-frame
            if not ret:
                st.error("Failed to capture video frame.")
                break

            # Convert frame to RGB for Mediapipe processing
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(frame_rgb)

            try:
                if results.pose_landmarks:
                    landmarks = results.pose_landmarks.landmark
                    shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                    elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                    wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

                    # Calculate angle between shoulder, elbow, wrist
                    angle = calculate_angle(shoulder, elbow, wrist)

                    # Update rep count
                    if angle > 160:
                        stage = "down"
                    if angle < 30 and stage == 'down':
                        stage = "up"
                        counter += 1
                        st.write(f"Reps: {counter}")

                    # Visualize angle on the frame
                    cv2.putText(frame, str(int(angle)), tuple(np.multiply(elbow, [640, 480]).astype(int)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

                # Draw pose landmarks on the frame
                mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                          mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                          mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2))

            except Exception as e:
                st.error(f"Error during rep calculation: {e}")

            # Display processed frame in Streamlit
            frame_placeholder.image(frame, channels="BGR")

            # Control frame rate to limit Streamlit update frequency
           # time.sleep(0.1)

            # Stop button to end the loop
            if var:
                break
            
        #st.write(f"Reps: {counter}")

        # Release the video capture object
        video_capture.release()
        st.write("Video capture ended.")


# History Page
if st.session_state.page == "History":
    st.title("📜 View History")
    st.subheader("Workout History")
    workout_data = load_data("workout_history.csv")
    if not workout_data.empty:
        st.dataframe(workout_data)
    else:
        st.info("No workouts logged yet.")

    st.subheader("Food Intake History")
    food_data = load_data("food_history.csv")
    if not food_data.empty:
        st.dataframe(food_data)
    else:
        st.info("No food intake records found.")

    st.subheader("Sleep Routine History")
    sleep_data = load_data("sleep_history.csv")
    if not sleep_data.empty:
        st.dataframe(sleep_data)
    else:
        st.info("No sleep records found.")

# Summary Analysis Page
if st.session_state.page == "Summary":
    st.title("📊 Summary Analysis")
    workout_data = load_data("workout_history.csv")
    food_data = load_data("food_history.csv")
    sleep_data = load_data("sleep_history.csv")

    if not workout_data.empty:
        st.subheader("Workout Analysis")
        total_calories = workout_data["Calories Burned"].sum()
        st.write(f"*Total Calories Burned:* {total_calories} kcal")
        st.line_chart(workout_data.set_index("Date")["Calories Burned"])

    if not food_data.empty:
        st.subheader("Food Intake Analysis")
        total_calories_intake = food_data["Calories Intake"].sum()
        st.write(f"*Total Calories Intake:* {total_calories_intake} kcal")
        st.line_chart(food_data.set_index("Date")["Calories Intake"])

    if not sleep_data.empty:
        st.subheader("Sleep Analysis")
        avg_sleep = sleep_data["Sleep Duration (hours)"].mean()
        st.write(f"*Average Sleep Duration:* {avg_sleep:.1f} hours")
        st.line_chart(sleep_data.set_index("Date")["Sleep Duration (hours)"])