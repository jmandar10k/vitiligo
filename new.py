import streamlit as st
import pickle
import numpy as np
import pandas as pd
import joblib

@st.cache_resource
def load_model():
    # Provide the full path to your model file here
    with open('svc.pkl', 'rb') as file:
        model = pickle.load(file)
    return model

model = load_model()

# Function to combine all section scores
def calculate_combined_score(family_score, diet_score, lifestyle_score, psychological_score, environmental_score):
    # Combine the scores here; you could do a weighted sum or a simple sum
    combined_score = family_score + diet_score + lifestyle_score + psychological_score + environmental_score
    return combined_score

# Each section's code (as given by you previously)
def family_history_section():
    # Initialize responses dictionary
    responses = {}

    # Section: Personal and Family History Assessment
    st.title("Personal and Family History Assessment")

    # Question 1: Family history of vitiligo or other skin disorders?
    responses['family_history_skin_disorders'] = st.radio(
        "Do you have a family history of vitiligo or other skin disorders?",
        options=[0, 10],  # No, Yes
        format_func=lambda x: {0: "No (0)", 10: "Yes (10)"}[x]
    )

    # Question 2: Family history of depigmentation?
    responses['family_history_depigmentation'] = st.radio(
        "Has anyone in your family experienced depigmentation (loss of skin colour)?",
        options=[0, 10],  # No, Yes
        format_func=lambda x: {0: "No (0)", 10: "Yes (10)"}[x]
    )

    # Question 3: Personal history of autoimmune diseases?
    responses['personal_history_autoimmune'] = st.radio(
        "Do you have a personal history of autoimmune diseases (e.g., thyroid disorders, diabetes)?",
        options=[0, 10],  # No, Yes
        format_func=lambda x: {0: "No (0)", 10: "Yes (10)"}[x]
    )

    # Calculate total score for the family section
    family_score = sum(responses.values())
    return family_score

    
   
    
food_categories = {
    "Sour Foods": [
        "Fermented products", "Pickles", "Bhelpuri", "Sour fruit juices",
        "Tomato sauce", "Excess intake of preserved foods", "Curd",
        "Buttermilk", "Lemon juice", "Vinegar", "Alcohol", "Cold drinks"
    ],
    "Salty Foods": [
        "Salt predominant foods", "Papad", "Chips", "Namkeen", "Salt while eating"
    ],
    "Processed or Fried Foods": [
        "Pizza", "Cheese mixed foods", "Bakery products", "Kidney beans", 
        "Paneer", "Dosa", "Idli", "Vada", "Beef", "Pork", 
        "Food prepared from flour", "Regular intake of meat products", 
        "Intake of milk shakes", "Kheer"
    ],
    "Incompatible Food Combinations": [
        "Sprouted vegetables/grains with meat", "Milk with meat", 
        "Jaggery with meat", "Milk or honey with leafy vegetables", 
        "Curd with chicken", "Honey + hot water", 
        "Seafood with milk", "Seafood with sweet", 
        "Banana or fruit with milk", "Fruit salad", 
        "Smoothies", "Milk with sour food", 
        "Alcohol with or after milk", "Milk + rice + salt", 
        "Curd + milk + rice"
    ],
    "Food Habits": [
        "Cold + hot food together", "Cold food soon after intake of hot food or vice versa", 
        "Cold water with hot lunch/dinner", "Dessert along with hot food", 
        "Using cold milk with hot samosa", "Spicy and pungent foods with more of red chili, pepper"
    ],
    "Oily Foods": [
        "Excessively oily foods", "Biriyani", "Meat soups", 
        "Sweets made of excess ghee, milk", "Food prepared with cheese & ghee"
    ]
}

def diet_section():
    # Initialize responses dictionary

    # Section: Diet Assessment
    st.title("Diet Section")

    
    responses = {
        'sour_foods': [],
        'salty_foods': [],
        'processed_foods': [],
        'incompatible_combinations': [],
        'food_habits': [],
        'oily_foods': [],
        'meals_before_digestion': None,
    }

    # User input for sour foods
    sour_foods_input = st.multiselect("Select Sour Foods", food_categories["Sour Foods"])
    for food in sour_foods_input:
        days = st.selectbox(f"Days consumed for {food}", ['1-3', '3-5', '5-7'], index=0)
        responses['sour_foods'].append({'name': food, 'days': days})

    # User input for salty foods
    salty_foods_input = st.multiselect("Select Salty Foods", food_categories["Salty Foods"])
    for food in salty_foods_input:
        days = st.selectbox(f"Days consumed for {food}", ['1-3', '3-5', '5-7'], index=0)
        responses['salty_foods'].append({'name': food, 'days': days})

    # User input for processed foods
    processed_foods_input = st.multiselect("Select Processed or Fried Foods", food_categories["Processed or Fried Foods"])
    for food in processed_foods_input:
        days = st.selectbox(f"Days consumed for {food}", ['1-3', '3-5', '5-7'], index=0)
        responses['processed_foods'].append({'name': food, 'days': days})

    # User input for incompatible combinations
    incompatible_input = st.multiselect("Select Incompatible Food Combinations", food_categories["Incompatible Food Combinations"])
    for combo in incompatible_input:
        days = st.selectbox(f"Days consumed for {combo}", ['1-3', '3-5', '5-7'], index=0)
        responses['incompatible_combinations'].append({'name': combo, 'days': days})

    # User input for food habits
    food_habits_input = st.multiselect("Select Food Habits", food_categories["Food Habits"])
    for habit in food_habits_input:
        days = st.selectbox(f"Days spent on {habit}", ['1-3', '3-5', '5-7'], index=0)
        responses['food_habits'].append({'name': habit, 'days': days})

    # User input for oily foods
    oily_foods_input = st.multiselect("Select Oily Foods", food_categories["Oily Foods"])
    for oily_food in oily_foods_input:
        days = st.selectbox(f"Days consumed for {oily_food}", ['1-3', '3-5', '5-7'], index=0)
        responses['oily_foods'].append({'name': oily_food, 'days': days})

    # User input for meals before digestion
    meals_before_digestion = st.radio("Have you consumed meals before digestion?", ("Yes", "No"))
    responses['meals_before_digestion'] = meals_before_digestion

    # Calculate score based on responses
    total_score = calculate_food_score(responses)

    diet_score=total_score
    
    return diet_score

# Function to calculate score based on responses
def calculate_food_score(responses):
    total_score = 0
    
    # Sour Foods
    sour_score = sum(2 * (1 if food['days'] == '1-3' else 2 if food['days'] == '3-5' else 3) for food in responses.get('sour_foods', []))
    total_score += sour_score

    # Salty Foods
    salty_score = sum(2 * (1 if food['days'] == '1-3' else 2 if food['days'] == '3-5' else 3) for food in responses.get('salty_foods', []))
    total_score += salty_score

    # Processed Foods
    processed_score = sum(2 * (1 if food['days'] == '1-3' else 2 if food['days'] == '3-5' else 3) for food in responses.get('processed_foods', []))
    total_score += processed_score

    # Incompatible Food Combinations
    incompatible_score = sum(3 * (2 if combo['days'] == '1-3' else 4 if combo['days'] == '3-5' else 6) for combo in responses.get('incompatible_combinations', []))
    total_score += incompatible_score

    # Food Habits
    habits_score = sum(1 * (1 if habit['days'] == '1-3' else 2 if habit['days'] == '3-5' else 3) for habit in responses.get('food_habits', []))
    total_score += habits_score

    # Oily Foods
    oily_score = sum(1 * (1 if oily_food['days'] == '1-3' else 2 if oily_food['days'] == '3-5' else 3) for oily_food in responses.get('oily_foods', []))
    total_score += oily_score

    # Meals Before Digestion
    if responses.get('meals_before_digestion') == 'Yes':
        total_score += 6

    return total_score

def lifestyle_section():
    # Initialize responses dictionary
    responses = {}

    # Section: Lifestyle Factor
    st.title("Lifestyle Factor Assessment")

    # Question 1: Do you often suppress natural urges (e.g., urination, defecation, sneezing)?
    responses['suppress_urges'] = st.radio(
        "Do you often suppress natural urges (e.g., urination, defecation, sneezing)?",
        options=[0, 1, 3, 4],  # Never, Rarely, Sometimes, Often
        format_func=lambda x: {0: "Never (0)", 1: "Rarely (1)", 3: "Sometimes (3)", 4: "Often (4)"}[x]
    )

    # Question 2: How often do you engage in heavy physical exercise (Ati Vyayama)?
    responses['heavy_exercise'] = st.radio(
        "How often do you engage in heavy physical exercise (Ati Vyayama)?",
        options=[0, 1, 2, 3],  # Never, Rarely, Sometimes, Often
        format_func=lambda x: {0: "Never (0)", 1: "Rarely (1)", 2: "Sometimes (2)", 3: "Often (3)"}[x]
    )

    # Question 3: Do you sleep immediately after having lunch/dinner?
    responses['sleep_after_meal'] = st.radio(
        "Do you sleep immediately after having lunch/dinner?",
        options=[0, 10],  # No, Yes
        format_func=lambda x: {0: "No (0)", 10: "Yes (10)"}[x]
    )

    # Question 4: Do you often sleep during the day (Diwaswapan)?
    responses['day_sleep'] = st.radio(
        "Do you often sleep during the day (Diwaswapan)?",
        options=[0, 2, 4, 5],  # Never, Rarely, Sometimes, Often
        format_func=lambda x: {0: "Never (0)", 2: "Rarely (2)", 4: "Sometimes (4)", 5: "Often (5)"}[x]
    )

    # Question 5: How often do you feel physically or mentally exhausted (Ati Santapa)?
    responses['exhausted'] = st.radio(
        "How often do you feel physically or mentally exhausted (Ati Santapa)?",
        options=[0, 1, 2, 3],  # Never, Rarely, Sometimes, Often
        format_func=lambda x: {0: "Never (0)", 1: "Rarely (1)", 2: "Sometimes (2)", 3: "Often (3)"}[x]
    )

    # Question 6: Do you suffer from insomnia or disturbed sleep at night?
    responses['insomnia'] = st.radio(
        "Do you suffer from insomnia or disturbed sleep at night?",
        options=[0, 1, 3, 4],  # Never, Rarely, Sometimes, Often
        format_func=lambda x: {0: "Never (0)", 1: "Rarely (1)", 3: "Sometimes (3)", 4: "Often (4)"}[x]
    )

    # Question 7: Do you engage in heavy workouts at the gym soon after a heavy meal?
    responses['workout_after_meal'] = st.radio(
        "Do you engage in heavy workouts at the gym soon after a heavy meal?",
        options=[0, 5],  # No, Yes
        format_func=lambda x: {0: "No (0)", 5: "Yes (5)"}[x]
    )

    # Question 8: Do you consume heavy and highly nutritive food soon after fasting?
    responses['heavy_food_after_fasting'] = st.radio(
        "Do you consume heavy and highly nutritive food soon after fasting?",
        options=[0, 5],  # No, Yes
        format_func=lambda x: {0: "No (0)", 5: "Yes (5)"}[x]
    )

    # Question 9: Do you bathe in cold water immediately after coming from a hot environment?
    responses['cold_bath'] = st.radio(
        "Do you bathe in cold water immediately after coming from a hot environment?",
        options=[0, 1, 2, 3],  # Never, Rarely, Sometimes, Often
        format_func=lambda x: {0: "Never (0)", 1: "Rarely (1)", 2: "Sometimes (2)", 3: "Often (3)"}[x]
    )

    # Question 10: Do you eat when your mind is agitated by fear?
    responses['eat_with_fear'] = st.radio(
        "Do you eat when your mind is agitated by fear?",
        options=[0, 2, 3, 4],  # Never, Rarely, Sometimes, Often
        format_func=lambda x: {0: "Never (0)", 2: "Rarely (2)", 3: "Sometimes (3)", 4: "Often (4)"}[x]
    )

    # Calculate total score for the lifestyle section
    lifestyle_score = sum(responses.values())
    return lifestyle_score

def psychological_section():
   
    
    # Dictionary to store responses
    responses = {}

    # Section: Diet Assessment
    st.title("psychological section")

    # Question 1: How often do you experience stress or anxiety?
    responses['stress_anxiety'] = st.radio(
        "How often do you experience stress or anxiety?",
        options=[0, 1, 2, 3, 4, 5],  # Scale from Never (0) to Always (5)
        format_func=lambda x: ["Never (0)", "Rarely (1)", "Sometimes (2)", "Often (3)", "Very Often (4)", "Always (5)"][x]
    )

    # Question 2: Have you experienced prolonged grief or sadness recently?
    responses['grief_sadness'] = st.radio(
        "Have you experienced prolonged grief or sadness recently?",
        options=[0, 5],  # No = 0, Yes = 5
        format_func=lambda x: "No (0)" if x == 0 else "Yes (5)"
    )

    # Question 3: How often do you feel anger or frustration?
    responses['anger_frustration'] = st.radio(
        "How often do you feel anger or frustration?",
        options=[0, 1, 2, 3, 4, 5],  # Scale from Never (0) to Always (5)
        format_func=lambda x: ["Never (0)", "Rarely (1)", "Sometimes (2)", "Often (3)", "Very Often (4)", "Always (5)"][x]
    )

    # Question 4: Do you often feel mentally exhausted or overwhelmed?
    responses['mental_exhaustion'] = st.radio(
        "Do you often feel mentally exhausted or overwhelmed?",
        options=[0, 1, 2, 3],  # Never, Rarely, Sometimes, Often
        format_func=lambda x: ["Never (0)", "Rarely (1)", "Sometimes (2)", "Often (3)"][x]
    )

    # Question 5: Have you experienced guilt or moral distress recently?
    responses['guilt_distress'] = st.radio(
        "Have you experienced guilt or moral distress recently?",
        options=[0, 10],  # No = 0, Yes = 10
        format_func=lambda x: "No (0)" if x == 0 else "Yes (10)"
    )

    # Question 6: Do you feel any pressure or unresolved conflicts in your family or work environment?
    responses['conflicts'] = st.radio(
        "Do you feel any pressure or unresolved conflicts in your family or work environment?",
        options=[0, 5],  # No = 0, Yes = 5
        format_func=lambda x: "No (0)" if x == 0 else "Yes (5)"
    )

    # Question 7: Do you ever find yourself speaking disrespectfully or acting rudely towards elders, teachers, or those in authority?
    responses['disrespect_authority'] = st.radio(
        "Do you ever find yourself speaking disrespectfully or acting rudely towards elders, teachers, or those in authority?",
        options=[0, 3, 5, 6],  # Never, Rarely, Sometimes, Often
        format_func=lambda x: {0: "Never (0)", 3: "Rarely (3)", 5: "Sometimes (5)", 6: "Often (6)"}[x]
    )

    # Question 8: Have you ever justified or engaged in unethical actions to achieve personal success or benefits?
    responses['unethical_actions'] = st.radio(
        "Have you ever justified or engaged in unethical actions to achieve personal success or benefits?",
        options=[0, 3, 5, 6],  # Never, Rarely, Sometimes, Often
        format_func=lambda x: {0: "Never (0)", 3: "Rarely (3)", 5: "Sometimes (5)", 6: "Often (6)"}[x]
    )

    # Question 9: Have you ever taken something from someone else for your own personal gain?
    responses['taken_something'] = st.radio(
        "Have you ever taken something from someone else for your own personal gain?",
        options=[0, 3, 5, 6],  # Never, Rarely, Sometimes, Often
        format_func=lambda x: {0: "Never (0)", 3: "Rarely (3)", 5: "Sometimes (5)", 6: "Often (6)"}[x]
    )

    # Question 10: Have you experienced any major stressful life events recently?
    responses['major_stress_events'] = st.radio(
        "Have you experienced any major stressful life events recently?",
        options=[0, 10],  # No = 0, Yes = 10
        format_func=lambda x: "No (0)" if x == 0 else "Yes (10)"
    )

    # Calculate total score
    psychological_score = sum(responses.values())

    return psychological_score


def environmental_section():
    # Initialize responses dictionary
    responses = {}

    # Section: Environmental Factors
    st.title("Environmental Factors Assessment")

    # Question 1: Are you exposed to chemicals or industrial pollutants at work?
    responses['chemical_exposure'] = st.radio(
        "Are you exposed to chemicals or industrial pollutants at work?",
        options=[0, 1, 2, 3],  # Never, Rarely, Sometimes, Often
        format_func=lambda x: {0: "Never (0)", 1: "Rarely (1)", 2: "Sometimes (2)", 3: "Often (3)"}[x]
    )

    # Question 2: Do you live or work in a highly polluted area?
    responses['polluted_area'] = st.radio(
        "Do you live or work in a highly polluted area?",
        options=[0, 5],  # No, Yes
        format_func=lambda x: {0: "No (0)", 5: "Yes (5)"}[x]
    )

    # Question 3: Have you used any harsh chemicals or skin products in recent months?
    responses['harsh_chemicals'] = st.radio(
        "Have you used any harsh chemicals or skin products in recent months?",
        options=[0, 2, 3, 4],  # Never, Rarely, Sometimes, Often
        format_func=lambda x: {0: "Never (0)", 2: "Rarely (2)", 3: "Sometimes (3)", 4: "Often (4)"}[x]
    )

    # Question 4: Do you frequently spend long hours in direct sunlight without skin protection?
    responses['sunlight_exposure'] = st.radio(
        "Do you frequently spend long hours in direct sunlight without skin protection?",
        options=[0, 2, 3, 4],  # Never, Rarely, Sometimes, Often
        format_func=lambda x: {0: "Never (0)", 2: "Rarely (2)", 3: "Sometimes (3)", 4: "Often (4)"}[x]
    )

    # Calculate total score
    environmental_score = sum(responses.values())

    return environmental_score

# Streamlit UI
st.title("Vitiligo Risk Prediction")

st.header("Questionnaire")
st.write("Please fill out the following sections to predict your vitiligo risk.")

# Family History Section
family_score = family_history_section()
st.write(f"Family History Score: {family_score}")

# Diet Section
diet_score = diet_section()
st.write(f"Diet Score: {diet_score}")

# Lifestyle Section
lifestyle_score = lifestyle_section()
st.write(f"Lifestyle Score: {lifestyle_score}")

# Psychological Section
psychological_score = psychological_section()
st.write(f"Psychological Health Score: {psychological_score}")

# Environmental Section
environmental_score = environmental_section()
st.write(f"Environmental Score: {environmental_score}")

# Calculate combined score
combined_score = calculate_combined_score(family_score, diet_score, lifestyle_score, psychological_score, environmental_score)
st.write(f"Combined Score: {combined_score}")



# Reshape combined score into the format your model expects (e.g., 2D array for scikit-learn)



# Calculate combined score
combined_score = calculate_combined_score(family_score, diet_score, lifestyle_score, psychological_score, environmental_score)
st.write(f"Combined Score: {combined_score}")

def predict_vitiligo_risk(diet_score, environmental_score, lifestyle_score, psychological_score, family_score, combined_score):
    # Reshape the scores into the format your model expects (e.g., 2D array for scikit-learn)
    scores_input = np.array([[diet_score, environmental_score, lifestyle_score, psychological_score, family_score, combined_score]])
    
    # Make a prediction using the trained model
    prediction = model.predict( scores_input)

    # Map the prediction to the risk level (customize this based on your model output)
    #risk_levels = {0: "Low Risk", 1: "Moderate Risk", 2: "High Risk"}  # Example mapping
    #predicted_risk_level = risk_levels.get(prediction[0], "Unknown")

    return prediction


# Initialize prediction result variable
prediction_result = None

# Prediction button
if st.button("Predict Risk Level"):
    # Call the prediction function with all relevant scores
    prediction_result = predict_vitiligo_risk(diet_score, environmental_score, lifestyle_score, psychological_score, family_score, combined_score)

# Display the prediction result only if it exists
if prediction_result is not None:
    st.header("Predicted Vitiligo Risk Level")
    st.write(f"The predicted risk level is: {prediction_result}")
