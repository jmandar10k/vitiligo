import streamlit as st
import pickle
import numpy as np
import pandas as pd
import joblib
from fpdf import FPDF
import datetime
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
 
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





# Function to determine the type of vitiligo based on user input
def determine_vitiligo_type(responses):
    vitiligo_types = set()

    # Logic for location of spot on face
    if 'at the openings(lips/nostrils/ears)' in responses['face']:
        vitiligo_types.add('Acrofacial vitiligo (due to spots on the face openings).')
    if 'on one side of the face' in responses['face']:
        vitiligo_types.add('Segmental vitiligo (due to spots on one side of the face).')
    if 'on both sides of the face' in responses['face']:
        vitiligo_types.add('Non-segmental vitiligo (due to spots on both sides of the face).')
    if 'just one spot on face' in responses['face']:
        vitiligo_types.add('Focal vitiligo (due to a single spot on the face).')

    # Logic for location of spot on hands and feet
    if 'at the ends of limbs(fingers / toes)' in responses['hands_feet']:
        vitiligo_types.add('Acrofacial vitiligo (due to spots on the fingers).')
    if 'on both hands or feet' in responses['hands_feet']:
        vitiligo_types.add('Non-segmental vitiligo (due to spots on both hands or feet).')
    if 'on only one hand or feet' in responses['hands_feet']:
        vitiligo_types.add('Segmental vitiligo (due to spots on only one hand or foot).')

    # Logic for location of spot on arms and legs
    if 'on both arms or legs' in responses['arms_legs']:
        vitiligo_types.add('Non-segmental vitiligo (due to spots on both arms or legs).')
    if 'on only one arm or leg' in responses['arms_legs']:
        vitiligo_types.add('Segmental vitiligo (due to spots on only one arm or leg).')

    # Logic for depigmentation over 80% of the body
    if 'yes' in responses['whole_body']:
        vitiligo_types.add('Universal vitiligo (due to depigmentation affecting over 80% of the body).')

    # Return the vitiligo type(s)
    if vitiligo_types:
        return ', '.join(vitiligo_types)
    else:
        return 'Unknown type'

# function to determine the health of disease 
# Function to generate insights and conclusion based on user responses
def generate_insights_and_conclusion(white_patches, patch_shape, expanding_patches, patch_duration, sensations, color_change, new_patches, visibility_in_sunlight):
    insights = []
    
    # Insights for white patches
    if white_patches == 'Yes':
        insights.append("1) The patient has white patches, which can suggest depigmentation-related conditions like vitiligo.")
        
        # Shape of patches
        if patch_shape == 'Irregular':
            insights.append(" 2) Irregular shapes can indicate an active, progressive phase of vitiligo, compared to round/oval shapes, which might signify more stable patches.")
        elif patch_shape in ['Round', 'Oval']:
            insights.append(" 2) Round/oval shapes may indicate more stable vitiligo patches.")
        else:
            insights.append(" 2) Uncertain shape may require further observation.")

        # Expansion over time
        if expanding_patches == 'Yes, they are growing':
            insights.append(" 3) The condition is still progressing, and the patches are likely spreading, which could require more aggressive treatment.")
        elif expanding_patches == 'No, they have remained the same size':
            insights.append(" 3) The vitiligo appears stable without active spreading.")
        else:
            insights.append(" 3) Uncertainty about patch expansion may require monitoring.")
        
        # Duration of condition
        if patch_duration in ['6-12 months', 'More than 1 year']:
            insights.append("4) The patient has been experiencing symptoms for a significant period, suggesting chronic vitiligo.")
        elif patch_duration in ['Less than 3 months', '3-6 months']:
            insights.append("4) A relatively recent onset, which may indicate early-stage vitiligo.")

        # Sensations
        if sensations == 'No, no sensations':
            insights.append("5) Lack of sensations like itching or pain can rule out inflammatory skin conditions, as vitiligo typically doesn’t involve sensory symptoms.")
        else:
            insights.append(f"5) The presence of {sensations} might require additional investigation for other skin conditions.")

        # Color change over time
        if color_change == 'Yes, they have lightened over time':
            insights.append("6) Depigmentation has progressed from partial loss of skin color to complete depigmentation, a hallmark of vitiligo progression.")
        else:
            insights.append("6) The patches have remained stable in color.")
        
        # New patches
        if new_patches == 'Yes, within the last 3 months':
            insights.append("7) New patches indicate active vitiligo, suggesting the disease is still spreading.")
        else:
            insights.append("7) No new patches suggest stability.")

        # Visibility in sunlight
        if visibility_in_sunlight == 'Yes, they are more noticeable':
            insights.append("8) The contrast between normal skin and depigmented patches increases when the skin tans, often seen in vitiligo.")
        else:
            insights.append("8) No change in visibility suggests the patches may blend more with the skin tone.")
    
    else:
        insights.append("Insight: No white patches indicate vitiligo may not be present.")

    # Conclusion based on the responses
    conclusion = "From these responses, we gather that the patient is "
    
    if expanding_patches == 'Yes, they are growing' or new_patches == 'Yes, within the last 3 months':
        conclusion += "likely dealing with progressive vitiligo. The condition is still spreading, as "
        if expanding_patches == 'Yes, they are growing':
            conclusion += "existing patches have grown larger, "
        if new_patches == 'Yes, within the last 3 months':
            conclusion += "new patches have appeared recently, "
        conclusion = conclusion.rstrip(", ") + ". "
    else:
        conclusion += "likely dealing with stable vitiligo, as there has been no significant spread of the patches. "

    if sensations == 'No, no sensations':
        conclusion += "The lack of pain or itching helps distinguish it from other skin conditions like eczema or psoriasis, which often involve these symptoms. "

    if visibility_in_sunlight == 'Yes, they are more noticeable':
        conclusion += "The increased visibility of the patches in sunlight supports the diagnosis of vitiligo, as tanning makes the depigmentation more apparent. "

    conclusion += "Overall, the responses suggest that "
    if expanding_patches == 'Yes, they are growing' or new_patches == 'Yes, within the last 3 months':
        conclusion += "the condition is still active and progressing."
    else:
        conclusion += "the condition is stable and not actively spreading."

    return insights, conclusion

# pie chart 

import matplotlib.pyplot as plt

def create_pie_chart(family_score, diet_score, lifestyle_score, psychological_score, environmental_score):
    # Create a dictionary of scores
    scores = {
        'Family Score': family_score,
        'Diet Score': diet_score,
        'Lifestyle Score': lifestyle_score,
        'Psychological Score': psychological_score,
        'Environmental Score': environmental_score,
    }

    # Create a pie chart
    labels = scores.keys()
    sizes = scores.values()
    colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0']

    plt.figure(figsize=(8, 8))
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')  # Equal aspect ratio ensures that pie chart is a circle.

    # Save the pie chart as an image
    chart_path = "pie_chart.png"
    plt.savefig(chart_path)
    plt.close()  # Close the figure

    return chart_path



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



# Section for Vitiligo Lesion Questionnaire
# Header for the questionnaire
st.header("Vitiligo Lesion Questionnaire")
report_text = ""
vitiligo_type = ""

# Main questions with subquestions and options
responses = {}

# Location of spots on the face
responses['face'] = st.multiselect(
    'Location of spot on face?',
    ['at the openings(lips/nostrils/ears)',
     'on one side of the face',
     'on both sides of the face',
     'just one spot on face'],
    key='face_multiselect'  # Unique key for this multiselect
)

# Location of spots on hands and feet
responses['hands_feet'] = st.multiselect(
    'Location of spot on hands and feet?',
    ['at the ends of limbs(fingers / toes)',
     'on both hands or feet',
     'on only one hand or feet'],
    key='hands_feet_multiselect'  # Unique key for this multiselect
)

# Location of spots on arms and legs
responses['arms_legs'] = st.multiselect(
    'Location of spot on arms and legs?',
    ['on both arms or legs',
     'on only one arm or leg'],
    key='arms_legs_multiselect'  # Unique key for this multiselect
)

# Whole body depigmentation question
responses['whole_body'] = st.multiselect(
    'Do you have around 80 to more than 80% body depigmentation?',
    ['yes', 'no'],
    key='whole_body_multiselect'  # Unique key for this multiselect
)
# Button to submit the questionnaire

# Button to submit the questionnaire
if st.button('Submit', key='submit_button'):  # Unique key for this button
    # Determine vitiligo type based on responses
    vitiligo_type = determine_vitiligo_type(responses)
    
    # Display the result
    st.subheader(f"Based on your responses, the type of vitiligo is: {vitiligo_type}")

    # Adding vitiligo type to the PDF report
    report_text += f"Vitiligo Assessment:\nType of Vitiligo: {vitiligo_type}\n"

#new

st.title("Vitiligo Progression Questionnaire")

# Questions
white_patches = st.radio("Do you have any white patches on your skin?", ['Yes', 'No'])

if white_patches == 'Yes':
    patch_shape = st.radio("What is the shape of the white patches?", ['Round', 'Oval', 'Irregular', 'Not sure'])
    expanding_patches = st.radio("Are the white patches expanding over time?", 
                                 ['Yes, they are growing', 'No, they have remained the same size', 'Not sure'])
    patch_duration = st.radio("How long have you had the white patches on your body?", 
                              ['Less than 3 months', '3-6 months', '6-12 months', 'More than 1 year'])
    sensations = st.radio("Do you experience any sensations (e.g., itching, pain) in or around the white patches?", 
                          ['Yes, itching', 'Yes, pain', 'No, no sensations', 'Not sure'])
    color_change = st.radio("Have the patches changed in color over time (e.g., from light to completely white)?", 
                            ['Yes, they have lightened over time', 'No, they have remained the same color', 'Not sure'])
    new_patches = st.radio("Have you noticed any new white patches appearing recently?", 
                           ['Yes, within the last 3 months', 'No, no new patches', 'Not sure'])
    visibility_in_sunlight = st.radio("Do the patches become more noticeable in sunlight or when your skin tans?", 
                                      ['Yes, they are more noticeable', 'No, there’s no change', 'Not sure'])
else:
    # If the user answers 'No', you can assign default values to the other variables.
    patch_shape =expanding_patches= patch_duration = sensations = color_change = new_patches = visibility_in_sunlight = None

# Submit button


# if st.button("Submit"):
#     # Ensure all necessary variables are defined
#     if white_patches == 'Yes':
#         # Generate insights and conclusion
#         insights, conclusion = generate_insights_and_conclusion(
#             white_patches, patch_shape, expanding_patches, patch_duration, sensations, color_change, new_patches, visibility_in_sunlight
#         )

#         # Insights Section
#         st.subheader("Insights:")
#         for insight in insights:
#             st.write(insight)

#         # Conclusion Section
#         st.subheader("Conclusion:")
#         st.write(conclusion)
#     else:
#         # If no white patches, you might want to display a different message
#         st.subheader("Conclusion:")
#         st.write("No white patches indicate vitiligo may not be present.")


# Submit button
if st.button("Submit"):
    # Ensure all necessary variables are defined
    if white_patches == 'Yes':
        # Generate insights and conclusion
        insights, conclusion = generate_insights_and_conclusion(
            white_patches, patch_shape, expanding_patches, patch_duration, sensations, color_change, new_patches, visibility_in_sunlight
        )
        
        # Store insights and conclusion without displaying them
        st.session_state.insights = insights
        st.session_state.conclusion = conclusion
        
    else:
        # If no white patches, you might want to display a different message
        st.session_state.insights = []
        st.session_state.conclusion = "No white patches indicate vitiligo may not be present."






# Calculate combined score
combined_score = calculate_combined_score(family_score, diet_score, lifestyle_score, psychological_score, environmental_score)
st.write(f"Combined Score: {combined_score}")

#pie streamlit


# Button to generate pie chart
# Initialize session state for the pie chart path
if 'chart_path' not in st.session_state:
    st.session_state.chart_path = None

# Generate and save the Score Pie Chart when button is clicked
if st.button("Generate Score Pie Chart"):
    st.session_state.chart_path = create_pie_chart(family_score, diet_score, lifestyle_score, psychological_score, environmental_score)

# # Display the pie chart if it exists in session state
# if st.session_state.chart_path:
#     st.image(st.session_state.chart_path, caption="Score Distribution Pie Chart", use_column_width=True)






# Mock-up function for generating the Vitiligo report as a PDF
from fpdf import FPDF

def generate_vitiligo_report(patient_name, age, gender, date, diet_score, environmental_score, lifestyle_score, 
                              psychological_score, family_score, combined_score, prediction, insights, conclusion):
    pdf = FPDF()
    pdf.add_page()

       # Header
    pdf.set_font("Arial", 'B', 16)
    pdf.set_text_color(0, 102, 204)  # Blue color
    pdf.cell(200, 10, "Vitiligo Assessment Report", ln=True, align='C')

    # Reset text color to black for patient info
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", '', 12)
    pdf.cell(200, 10, f"Patient Name: {patient_name}", ln=True)
    pdf.cell(200, 10, f"Age: {age}", ln=True)
    pdf.cell(200, 10, f"Gender: {gender}", ln=True)
    pdf.cell(200, 10, f"Date: {date}", ln=True)

    pdf.ln(20)  # Space before diagnostics

    # Diagnostics Section
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(0, 102, 204)  # Blue color
    pdf.cell(200, 10, "Diagnostic Report", ln=True)

    # Family History Section
    pdf.set_font("Arial", '', 12)
    pdf.set_text_color(0, 0, 0)  # Black color
    if family_score >= 10:
        pdf.cell(200, 10, "1)Family History: High Risk", ln=True)
    elif 5 <= family_score < 10:
        pdf.cell(200, 10, "1)Family History: Moderate Risk", ln=True)
    else:
        pdf.cell(200, 10, "1)Family History: Low Risk", ln=True)

    pdf.ln(5)

    # Dietary Section
    pdf.set_text_color(0, 0, 0)  # Black color
    if 0 <= diet_score < 28:
        pdf.cell(200, 10, "2)Dietary Section: Low Risk", ln=True)
        pdf.cell(200, 10, "Description: Minimal dietary exposure related to vitiligo risk.", ln=True)
    elif 29 <= diet_score < 56:
        pdf.cell(200, 10, "2)Dietary Section: Moderate Risk", ln=True)
        pdf.cell(200, 10, "Description: Moderate dietary exposure; review of eating habits recommended.", ln=True)
    elif 57 <= diet_score < 84:
        pdf.cell(200, 10, "2)Dietary Section: High Risk", ln=True)
        pdf.cell(200, 10, "Description: Significant dietary influence linked to vitiligo; dietary changes advised.", ln=True)
    else:
        pdf.cell(200, 10, "Dietary Section: Very High Risk", ln=True)
        pdf.cell(200, 10, "Description: Strong dietary factors likely causing or exacerbating vitiligo; immediate action required.", ln=True)

    pdf.ln(5)

    # Lifestyle Section
    if 0 <= lifestyle_score < 15:
        pdf.cell(200, 10, "3)Lifestyle Section: Low Risk", ln=True)
        pdf.cell(200, 10, "Description: Minimal lifestyle-related issues.", ln=True)
    elif 16 <= lifestyle_score < 30:
        pdf.cell(200, 10, "3)Lifestyle Section: Moderate Risk", ln=True)
        pdf.cell(200, 10, "Description: Moderate lifestyle-related issues; attention recommended", ln=True)
    else:
        pdf.cell(200, 10, "3)Lifestyle Section: High Risk", ln=True)
        pdf.cell(200, 10, "Description: High levels of lifestyle-related issues; action advised.", ln=True)

    pdf.ln(5)

    # Psychological Section
    if 0 <= psychological_score < 10:
        pdf.cell(200, 10, "4)Psychological Section: Low Risk", ln=True)
        pdf.cell(200, 10, "Description: Minimal stress and anxiety-related experiences.", ln=True)
    elif 11 <= psychological_score < 25:
        pdf.cell(200, 10, "4)Psychological Section: Moderate Risk", ln=True)
        pdf.cell(200, 10, "Description: Moderate levels of stress and anxiety; attention recommended.", ln=True)
    else:
        pdf.cell(200, 10, "4)Psychological Section: High Risk", ln=True)
        pdf.cell(200, 10, "Description: High levels of stress, anxiety, and moral distress; action advised", ln=True)

    pdf.ln(5)

    # Environmental Section
    if 0 <= environmental_score < 5:
        pdf.cell(200, 10, "5)Environmental Section: Low Risk", ln=True)
        pdf.cell(200, 10, "Description: Minimal exposure to environmental factors; low health risk.", ln=True)
    elif 6 <= environmental_score < 10:
        pdf.cell(200, 10, "5)Environmental Section: Moderate Risk", ln=True)
        pdf.cell(200, 10, "Description: Moderate exposure to environmental factors; some concern.", ln=True)
    else:
        pdf.cell(200, 10, "5)Environmental Section: High Risk", ln=True)
        pdf.cell(200, 10, "Description: High levels of exposure to environmental factors; urgent action needed.", ln=True)

    pdf.ln(20)

    # Vitiligo Assessment Section
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(0, 102, 204)  # Blue color
    pdf.cell(200, 10, "Vitiligo Assessment Section", ln=True)

    # Assuming you have a variable vitiligo_type defined somewhere
    vitiligo_type = determine_vitiligo_type(responses)  # Replace with actual logic to determine vitiligo type
    pdf.set_font("Arial", '', 12)
    pdf.set_text_color(0, 0, 0)  # Black color
    if vitiligo_type:
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(200, 10, "Type of Vitiligo:", ln=True)
        pdf.cell(200, 10, f"Type of Vitiligo: {vitiligo_type}", ln=True)
    else:
        pdf.cell(200, 10, "Type of Vitiligo: Unknown", ln=True)

    pdf.ln(20)  # Space before insights

    # Insights Section
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(0, 102, 204)  # Blue color
    pdf.cell(200, 10, "Insights:", ln=True)
    pdf.set_font("Arial", '', 12)
    pdf.set_text_color(0, 0, 0)  # Black color
    for insight in insights:
        pdf.multi_cell(0, 10, insight)

    pdf.ln(20)  # Space before conclusion

    # Conclusion Section
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(0, 102, 204)  # Blue color
    pdf.cell(200, 10, "Conclusion:", ln=True)
    pdf.set_font("Arial", '', 12)
    pdf.set_text_color(0, 0, 0)  # Black color
    pdf.multi_cell(0, 10, conclusion)

    pdf.ln(20)  # Space before conclusion

    # Add Pie Chart
    
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(0, 102, 204)  # Blue color
    pdf.cell(200, 10, "Risk Distribution:", ln=True)
    pdf.multi_cell(0, 10, "The following Pie chart narrate the information about contribution of each sections"
                    "if a person having vitiligo,so we get the actual cause of disease. ")

    chart_path = create_pie_chart(family_score, diet_score, lifestyle_score, psychological_score, environmental_score)

    # Insert the pie chart image
    pdf.image(chart_path, x=50, y=None, w=100, h=100)

    # Overall Diagnosis
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(0, 102, 204)  # Blue color
    pdf.cell(200, 10, "Overall Diagnosis", ln=True)

    # Adjust font for the description
    pdf.set_font("Arial", '', 12)
    pdf.set_text_color(0, 0, 0)  # Black color

    # Add descriptive text based on the prediction value
    pdf.set_font("Arial", 'B', 12)
    pdf.set_text_color(0, 0, 0)  # Black color

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
    pdf.multi_cell(200, 10, "Disclaimer: This report is generated by AI-based software and is for informational purposes only. "
                    "It is not a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice "
                    "of your physician or other qualified health provider with any questions you may have regarding a medical condition.")
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



if st.button("Download Report"):
    
    # Ensure prediction is available
    if "prediction" in st.session_state:
        prediction = st.session_state.prediction
        
        # Generate insights and conclusion directly here
        insights, conclusion = generate_insights_and_conclusion(
            white_patches, patch_shape, expanding_patches, patch_duration, sensations, color_change, new_patches, visibility_in_sunlight
        )

        # Generate the vitiligo report with insights and conclusion
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
            prediction,
            insights,
            conclusion
        )

        st.success(f"Report generated: {report_path}")

        # Provide download link
        with open(report_path, "rb") as file:
            pdf_data = file.read()  # Read the file content as binary data
            btn = st.download_button(label="Download Vitiligo Report", data=pdf_data, file_name=report_path, mime="application/pdf")
    
    else:
        st.error("Please click on 'Predict Risk Level' before downloading the report.")



# Function to send the email
def send_email(receiver_email, pdf_file):
    sender_email = "jmandar1322@gmail.com"
    EMAIL_PASSWORD = "rsai nmjq hsvo zqrm"  # Replace with your app-specific password

    # Create email header
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "Your Vitiligo Assessment Report"

    # Email body
    body = f"Hey {patient_name}  Please find your Attached Vitiligo Assessment Report."
    msg.attach(MIMEText(body, 'plain'))

    # Attach the existing PDF
    with open(pdf_file, "rb") as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename= {os.path.basename(pdf_file)}")
        msg.attach(part)

    # Create the SMTP session for sending the email
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, EMAIL_PASSWORD)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        st.success("Email sent successfully!")
    except Exception as e:
        st.error(f"Error: {e}")

# Streamlit app
st.title("Vitiligo Assessment Report Sender")

# Input for recipient email
receiver_email = st.text_input("Enter the recipient's email address")

# Specify the path to the existing PDF file
pdf_file = f"{patient_name}_vitiligo_report.pdf" # Make sure this file exists in the working directory

if st.button("Send Report"):
    if receiver_email:
        send_email(receiver_email, pdf_file)
    else:
        st.error("Please enter a recipient email address.")
