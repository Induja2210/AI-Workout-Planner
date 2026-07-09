import streamlit as st
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder

# ---------------------------------
# PAGE CONFIG
# ---------------------------------

st.set_page_config(
    page_title="AI Workout Planner",
    page_icon="🏋️",
    layout="centered"
)

# ---------------------------------
# BMI FUNCTIONS
# ---------------------------------

def calculate_bmi(height_cm, weight_kg):
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)
    return round(bmi, 2)

def bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal Weight"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"

# ---------------------------------
# LOAD DATASET
# ---------------------------------

df = pd.read_csv("workout_dataset.csv")
exercise_df = pd.read_csv("exercise_database.csv")




# ---------------------------------
# LABEL ENCODING
# ---------------------------------

gender_encoder = LabelEncoder()
activity_encoder = LabelEncoder()
goal_encoder = LabelEncoder()
workout_encoder = LabelEncoder()

df["Gender"] = gender_encoder.fit_transform(df["Gender"])
df["Activity_Level"] = activity_encoder.fit_transform(df["Activity_Level"])
df["Fitness_Goal"] = goal_encoder.fit_transform(df["Fitness_Goal"])
df["Workout_Category"] = workout_encoder.fit_transform(df["Workout_Category"])

# ---------------------------------
# FEATURES & TARGET
# ---------------------------------

X = df[["Age", "Gender", "BMI", "Activity_Level", "Fitness_Goal"]]
y = df["Workout_Category"]

# ---------------------------------
# TRAIN MODEL
# ---------------------------------

model = DecisionTreeClassifier(random_state=42)
model.fit(X, y)

# ---------------------------------
# TITLE
# ---------------------------------

st.title("🏋️ AI Workout Planner")
#st.error("THIS IS THE NEW VERSION")
st.write("Generate your personalized AI-powered workout plan!")

st.divider()

# ---------------------------------
# USER INPUTS
# ---------------------------------

st.header("👤 Enter Your Details")

name = st.text_input("Full Name")

age = st.number_input(
    "Age",
    min_value=15,
    max_value=80,
    value=20
)

gender = st.selectbox(
    "Gender",
    ["Male", "Female"]
)

height = st.number_input(
    "Height (cm)",
    min_value=100,
    max_value=250,
    value=160
)

weight = st.number_input(
    "Weight (kg)",
    min_value=30,
    max_value=200,
    value=65
)

activity_level = st.selectbox(
    "Activity Level",
    [
        "Sedentary",
        "Lightly Active",
        "Moderately Active",
        "Very Active"
    ]
)

fitness_goal = st.selectbox(
    "Fitness Goal",
    [
        "Weight Loss",
        "Muscle Gain",
        "Maintain Fitness",
        "Improve Endurance"
    ]
)

workout_days = 5
st.write("**Workout Days Per Week:** 5")
    


st.divider()

generate = st.button("🚀 Generate Workout Plan")

# ---------------------------------
# GENERATE RESULTS
# ---------------------------------

if generate:
    st.success("Button clicked!")

    bmi = calculate_bmi(height, weight)
    category = bmi_category(bmi)

    predicted_workout = None

    try:

        # Encode User Inputs
        user_gender = gender_encoder.transform([gender])[0]
        user_activity = activity_encoder.transform([activity_level])[0]
        user_goal = goal_encoder.transform([fitness_goal])[0]

        # Create DataFrame for Prediction
        user_data = pd.DataFrame({
            "Age": [age],
            "Gender": [user_gender],
            "BMI": [bmi],
            "Activity_Level": [user_activity],
            "Fitness_Goal": [user_goal]
        })
        
        
        prediction = model.predict(user_data)
        

        

        predicted_workout = workout_encoder.inverse_transform(prediction)[0]

        st.write("Predicted Workout:", predicted_workout)

    except Exception as e:
             
             import traceback
             st.exception(e)
             st.code(traceback.format_exc())

    

    # ---------------------------------
    # DISPLAY RESULTS
    # ---------------------------------

    st.success("Workout Plan Generated Successfully! 🎉")

    st.header(f"👋 Hello {name}")

    st.subheader("📊 BMI Analysis")

    st.metric("BMI", bmi)

    st.write(f"**BMI Category:** {category}")

    st.divider()

    st.subheader("🤖 AI Recommendation")

    if predicted_workout is not None:
        st.success(f"🏋️ Recommended Workout Category: **{predicted_workout}**")

        st.divider()

        st.header("🏋️ Weekly Workout Plan")

        plan = exercise_df[

            exercise_df["Workout_Category"] == predicted_workout

        ]
        plan = plan.head(workout_days)

        
        for _, row in plan.iterrows():

            st.subheader(f"📅 {row['Day']}")
            st.write(f"✅ {row['Exercise_1']}")
            st.write(f"✅ {row['Exercise_2']}")
            st.write(f"✅ {row['Exercise_3']}")
            st.write(f"🏃 Cardio: {row['Cardio']}")
            st.write(f"🧘 Stretching: {row['Stretching']}")
            st.divider()

    else:
        
        st.warning("Unable to generate workout recommendation.")
        st.subheader("📋 Your Information")
        st.write(f"**Name:** {name}")
        st.write(f"**Age:** {age}")
        st.write(f"**Gender:** {gender}")
        st.write(f"**Height:** {height} cm")
        st.write(f"**Weight:** {weight} kg")
        st.write(f"**Activity Level:** {activity_level}")
        st.write(f"**Fitness Goal:** {fitness_goal}")
        st.write(f"**Workout Days per Week:** {workout_days}")