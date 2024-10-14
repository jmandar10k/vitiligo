import streamlit as st
import pickle
import numpy as np
import pandas as pd
import joblib
from fpdf import FPDF
import datetime

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

# Mock-up function for generating the Vitiligo report as a PDF
def generate_vitiligo_report(patient_name, age, gender, date, diet_score, environmental_score, lifestyle_score, psychological_score, family_score, combined_score, prediction):
    pdf = FPDF()
    pdf.add_page()

    # Header
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "Vitiligo Assessment Report", ln=True, align='C')

    # Patient Info
    pdf.set_font("Arial", '', 12)
    pdf.cell(200, 10, f"Patient Name: {patient_name}", ln=True)
    pdf.cell(200, 10, f"Age: {age}", ln=True)
    pdf.cell(200, 10, f"Gender: {gender}", ln=True)
    pdf.cell(200, 10, f"Date: {date}", ln=True)
    
    pdf.ln(10)  # Space before diagnostics

    # Diagnostics Section
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, "Diagnostic Report", ln=True)

    # Family History Section
    responses = {}

    pdf.set_font("Arial", '', 12)


# Checking conditions for family history and personal history based on the new questions
    pdf.set_font("Arial", '', 12)
    if family_score >= 10:
        pdf.cell(200, 10, "Family History: High Risk", ln=True)
    elif 5 <= family_score < 10:
        pdf.cell(200, 10, "Family History: Moderate Risk", ln=True)
    else:
        pdf.cell(200, 10, "Family History: Low Risk", ln=True)

    pdf.ln(10) 
    
    # Dietary Section
    if 0 <= diet_score < 28:
        pdf.cell(200, 10, "Dietary Section: Low Risk", ln=True)
        pdf.cell(200, 10, "Description: Minimal dietary exposure related to vitiligo risk.", ln=True)
    elif 29 <= diet_score < 56:
        pdf.cell(200, 10, "Dietary Section: Moderate Risk", ln=True)
        pdf.cell(200, 10, "Description: Moderate dietary exposure; review of eating habits recommended.", ln=True)
    elif 57 <= diet_score < 84:
        pdf.cell(200, 10, "Dietary Section: High Risk", ln=True)
        pdf.cell(200, 10, "Description: Significant dietary influence linked to vitiligo; dietary changes advised.", ln=True)
    else:
        pdf.cell(200, 10, "Dietary Section: Very High Risk", ln=True)
        pdf.cell(200, 10, "Description: Strong dietary factors likely causing or exacerbating vitiligo; immediate action required.", ln=True)
        
    pdf.ln(10) 
    
    # Lifestyle Section
    if 0 <= lifestyle_score < 15:
        pdf.cell(200, 10, "Lifestyle Section: Low Risk", ln=True)
        pdf.cell(200, 10, "Description: Minimal lifestyle-related issues.", ln=True)
    elif 16 <= lifestyle_score < 30:
        pdf.cell(200, 10, "Lifestyle Section: Moderate Risk", ln=True)
        pdf.cell(200, 10, "Description: Moderate lifestyle-related issues; attention recommended", ln=True)
    else:
        pdf.cell(200, 10, "Lifestyle Section: High Risk", ln=True)
        pdf.cell(200, 10, "Description: High levels of lifestyle-related issues; action advised.", ln=True)
    
    pdf.ln(10) 

    # Psychological Section
    if 0 <= psychological_score < 10:
        pdf.cell(200, 10, "Psychological Section: Low Risk", ln=True)
        pdf.cell(200, 10, "Description: Minimal stress and anxiety-related experiences.", ln=True)
    elif 11 <= psychological_score < 25:
        pdf.cell(200, 10, "Psychological Section: Moderate Risk", ln=True)
        pdf.cell(200, 10, "Description: Moderate levels of stress and anxiety; attention recommended.", ln=True)
    else:
        pdf.cell(200, 10, "Psychological Section: High Risk", ln=True)
        pdf.cell(200, 10, "Description: High levels of stress, anxiety, and moral distress; action advised", ln=True)
    
    pdf.ln(10) 

    # Environmental Section
    if 0 <= environmental_score < 5:
        pdf.cell(200, 10, "Environmental Section: Low Risk", ln=True)
        pdf.cell(200, 10, "Description: Minimal exposure to environmental factors; low health risk.", ln=True)

    elif 6 <= environmental_score < 10:
        pdf.cell(200, 10, "Environmental Section: Moderate Risk", ln=True)
        pdf.cell(200, 10, "Description: Moderate exposure to environmental factors; some concern.", ln=True)
    else:
        pdf.cell(200, 10, "Environmental Section: High Risk", ln=True)
        pdf.cell(200, 10, "Description: High levels of exposure to environmental factors; urgent action needed.", ln=True)

    # Overall Diagnosis
    # Overall Diagnosis
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, "Overall Diagnosis", ln=True)

# Adjust font for the description
    pdf.set_font("Arial", '', 12)

# Add descriptive text based on the prediction value
    # Overall Diagnosis
    #pdf.ln(10)  # Add a new line before the diagnosis section
    pdf.set_font("Arial", 'B', 12)

# Determine risk levels based on prediction
    if prediction == "Low Risk":
        pdf.cell(200, 10, "Overall Risk: Low Risk", ln=True)
        pdf.multi_cell(0, 10, "The assessment indicates that there is a low likelihood of vitiligo based on "
                          "the provided information. While maintaining a healthy lifestyle is important, "
                          "there are no significant risk factors present at this time.")

    elif prediction == "Moderate Risk":
        pdf.cell(200, 10, "Overall Risk: Moderate Risk", ln=True)
        pdf.multi_cell(0, 10, "The assessment suggests a moderate risk of vitiligo. While there are some risk factors "
                          "present, the likelihood is not high. It is advisable to monitor any changes and "
                          "consider consulting a healthcare professional for further evaluation.")

    else:  # High Risk case
        pdf.cell(200, 10, "Overall Risk: High Risk", ln=True)
        pdf.multi_cell(0, 10, "The assessment points to a high risk of vitiligo based on significant risk factors, "
                          "including personal or family history. Immediate medical consultation is recommended "
                          "for early intervention and management.")



    # Disclaimer
    pdf.ln(10)
    pdf.cell(200, 10, "Disclaimer: This report is generated by AI-based software. Please consult a doctor.", ln=True)

    # Save the report
    report_path = f"{patient_name}_vitiligo_report.pdf"
    pdf.output(report_path)

    return report_path

# Function to predict vitiligo risk (replace with your actual model)
def predict_vitiligo_risk(diet_score, environmental_score, lifestyle_score, psychological_score, family_score, combined_score):
    # Reshape the scores into the format your model expects (e.g., 2D array for scikit-learn)
    scores_input = np.array([[diet_score, environmental_score, lifestyle_score, psychological_score, family_score, combined_score]])
    
    # Make a prediction using the trained model
    prediction = model.predict( scores_input)

    # Map the prediction to the risk level (customize this based on your model output)
    #risk_levels = {0: "Low Risk", 1: "Moderate Risk", 2: "High Risk"}  # Example mapping
    #predicted_risk_level = risk_levels.get(prediction[0], "Unknown")

    return prediction

# Main code that calculates section scores (replace with actual section score calculation logic)
def calculate_scores():
    
    return diet_score, environmental_score, lifestyle_score, psychological_score, family_score, combined_score

# Streamlit app code
st.title("Vitiligo Assessment Tool")

# Collect Patient Information
st.header("Patient Information")
patient_name = st.text_input("Patient Name")
age = st.number_input("Age", min_value=0, max_value=120, value=30)
gender = st.selectbox("Gender", ("Male", "Female", "Other"))
date = st.date_input("Date")

# Fetch the calculated section scores from the main code
diet_score, environmental_score, lifestyle_score, psychological_score, family_score, combined_score = calculate_scores()

# Display section scores
st.header("Calculated Scores")
st.write(f"Diet Score: {diet_score}")
st.write(f"Environmental Score: {environmental_score}")
st.write(f"Lifestyle Score: {lifestyle_score}")
st.write(f"Psychological Score: {psychological_score}")
st.write(f"Family Score: {family_score}")
st.write(f"Combined Score: {combined_score}")

# Predict button and result
if st.button("Predict Risk Level"):
    prediction = predict_vitiligo_risk(diet_score, environmental_score, lifestyle_score, psychological_score, family_score, combined_score)

    # Save the prediction in session state
    st.session_state.prediction = prediction

    # Show the predicted risk level
    st.header("Predicted Vitiligo Risk Level")
    st.write(f"The predicted risk level is: {prediction}")

# Button to generate and download the PDF report
if st.button("Download Report"):
    # Ensure prediction is available in session state
    
    if "prediction" in st.session_state:
        prediction = st.session_state.prediction
         # This will display the dictionary content
        report_path = generate_vitiligo_report(
        patient_name,
        age,
        gender,
        date,
        diet_score,
        environmental_score,
        lifestyle_score,
        psychological_score,
        family_score,
        combined_score,
        prediction
    )

    
        
        # Provide download link
        with open(report_path, "rb") as file:
            pdf_data = file.read()  # Read the file content as binary data
            btn = st.download_button(label="Download Vitiligo Report", data=pdf_data, file_name=report_path, mime="application/pdf")
    else:
        st.error("Please click on 'Predict Risk Level' before downloading the report.")
