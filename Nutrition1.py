from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image
import json
from datetime import datetime, timedelta
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO
import hashlib

# Configure Gemini
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    st.error("❌ API Key not found!")
    st.stop()

try:
    genai.configure(api_key=GOOGLE_API_KEY)
except Exception as e:
    st.error(f"❌ Failed to configure API: {str(e)}")
    st.stop()

# Database initialization
def init_database():
    conn = sqlite3.connect('nutrition_app.db')
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password_hash TEXT, created_at TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS health_profiles
                 (id INTEGER PRIMARY KEY, user_id INTEGER, profile_data TEXT, created_at TEXT, updated_at TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS meal_logs
                 (id INTEGER PRIMARY KEY, user_id INTEGER, date TEXT, meal_type TEXT, food_name TEXT, 
                  calories INTEGER, protein REAL, carbs REAL, fats REAL, created_at TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS water_logs
                 (id INTEGER PRIMARY KEY, user_id INTEGER, date TEXT, cups REAL, created_at TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS workout_logs
                 (id INTEGER PRIMARY KEY, user_id INTEGER, date TEXT, exercise TEXT, duration INTEGER, 
                  calories_burned INTEGER, intensity TEXT, created_at TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS progress_tracking
                 (id INTEGER PRIMARY KEY, user_id INTEGER, date TEXT, weight REAL, waist REAL, 
                  hip REAL, chest REAL, notes TEXT, created_at TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS favorites
                 (id INTEGER PRIMARY KEY, user_id INTEGER, item_type TEXT, item_data TEXT, created_at TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS goals
                 (id INTEGER PRIMARY KEY, user_id INTEGER, goal_text TEXT, target_value REAL, 
                  target_date TEXT, achieved INTEGER, created_at TEXT)''')
    
    conn.commit()
    conn.close()

init_database()

# Utility Functions
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate_user(username, password):
    conn = sqlite3.connect('nutrition_app.db')
    c = conn.cursor()
    c.execute('SELECT id FROM users WHERE username=? AND password_hash=?', 
              (username, hash_password(password)))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

def create_user(username, password):
    conn = sqlite3.connect('nutrition_app.db')
    c = conn.cursor()
    try:
        c.execute('INSERT INTO users (username, password_hash, created_at) VALUES (?, ?, ?)',
                 (username, hash_password(password), datetime.now().isoformat()))
        conn.commit()
        conn.close()
        return True
    except:
        conn.close()
        return False

def calculate_bmi(weight_kg, height_m):
    return round(weight_kg / (height_m ** 2), 1)

def get_bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight", "🟡"
    elif 18.5 <= bmi < 25:
        return "Normal", "🟢"
    elif 25 <= bmi < 30:
        return "Overweight", "🟠"
    else:
        return "Obese", "🔴"

def calculate_tdee(weight_kg, height_cm, age, gender, activity_level):
    if gender.lower() == 'male':
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    else:
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161
    
    activity_multipliers = {
        'sedentary': 1.2,
        'light': 1.375,
        'moderate': 1.55,
        'active': 1.725,
        'very_active': 1.9
    }
    tdee = bmr * activity_multipliers.get(activity_level, 1.55)
    return round(tdee), round(bmr)

def get_macro_breakdown(calories, protein_percent=30, carb_percent=50, fat_percent=20):
    return {
        'protein_g': round((calories * protein_percent / 100) / 4, 1),
        'carbs_g': round((calories * carb_percent / 100) / 4, 1),
        'fat_g': round((calories * fat_percent / 100) / 9, 1)
    }

def calculate_whr(waist_cm, hip_cm):
    return round(waist_cm / hip_cm, 2)

def calculate_body_fat_estimate(bmi, age, gender):
    if gender.lower() == 'male':
        body_fat = (1.20 * bmi) + (0.23 * age) - 16.2
    else:
        body_fat = (1.20 * bmi) + (0.23 * age) - 5.4
    return round(max(0, body_fat), 1)

def get_calorie_deficit(tdee, weight_loss_goal_weeks):
    weekly_deficit = 7000 / weight_loss_goal_weeks
    daily_deficit = weekly_deficit / 7
    return round(tdee - daily_deficit)

def save_meal_log(user_id, meal_data):
    conn = sqlite3.connect('nutrition_app.db')
    c = conn.cursor()
    c.execute('''INSERT INTO meal_logs (user_id, date, meal_type, food_name, calories, protein, carbs, fats, created_at)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
             (user_id, meal_data['date'], meal_data['meal_type'], meal_data['food_name'],
              meal_data['calories'], meal_data.get('protein', 0), meal_data.get('carbs', 0), 
              meal_data.get('fats', 0), datetime.now().isoformat()))
    conn.commit()
    conn.close()

def save_water_log(user_id, cups, date=None):
    if date is None:
        date = datetime.now().strftime('%Y-%m-%d')
    conn = sqlite3.connect('nutrition_app.db')
    c = conn.cursor()
    c.execute('INSERT INTO water_logs (user_id, date, cups, created_at) VALUES (?, ?, ?, ?)',
             (user_id, date, cups, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def save_workout(user_id, workout_data):
    conn = sqlite3.connect('nutrition_app.db')
    c = conn.cursor()
    c.execute('''INSERT INTO workout_logs (user_id, date, exercise, duration, calories_burned, intensity, created_at)
                 VALUES (?, ?, ?, ?, ?, ?, ?)''',
             (user_id, workout_data['date'], workout_data['exercise'], workout_data['duration'],
              workout_data['calories_burned'], workout_data['intensity'], datetime.now().isoformat()))
    conn.commit()
    conn.close()

def save_progress(user_id, progress_data):
    conn = sqlite3.connect('nutrition_app.db')
    c = conn.cursor()
    c.execute('''INSERT INTO progress_tracking (user_id, date, weight, waist, hip, chest, notes, created_at)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
             (user_id, progress_data['date'], progress_data.get('weight'), progress_data.get('waist'),
              progress_data.get('hip'), progress_data.get('chest'), progress_data.get('notes', ''),
              datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_meal_logs(user_id, date=None):
    if date is None:
        date = datetime.now().strftime('%Y-%m-%d')
    conn = sqlite3.connect('nutrition_app.db')
    c = conn.cursor()
    c.execute('SELECT * FROM meal_logs WHERE user_id=? AND date=? ORDER BY created_at DESC', (user_id, date))
    meals = c.fetchall()
    conn.close()
    return meals

def get_daily_totals(user_id, date=None):
    if date is None:
        date = datetime.now().strftime('%Y-%m-%d')
    conn = sqlite3.connect('nutrition_app.db')
    c = conn.cursor()
    c.execute('''SELECT SUM(calories) as calories, SUM(protein) as protein, SUM(carbs) as carbs, SUM(fats) as fats
                 FROM meal_logs WHERE user_id=? AND date=?''', (user_id, date))
    result = c.fetchone()
    conn.close()
    return {
        'calories': int(result[0]) if result[0] else 0,
        'protein': float(result[1]) if result[1] else 0,
        'carbs': float(result[2]) if result[2] else 0,
        'fats': float(result[3]) if result[3] else 0
    }

def get_water_intake(user_id, date=None):
    if date is None:
        date = datetime.now().strftime('%Y-%m-%d')
    conn = sqlite3.connect('nutrition_app.db')
    c = conn.cursor()
    c.execute('SELECT SUM(cups) FROM water_logs WHERE user_id=? AND date=?', (user_id, date))
    result = c.fetchone()
    conn.close()
    return result[0] or 0

def get_progress_history(user_id, days=30):
    conn = sqlite3.connect('nutrition_app.db')
    c = conn.cursor()
    start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
    c.execute('SELECT date, weight FROM progress_tracking WHERE user_id=? AND date>=? ORDER BY date',
             (user_id, start_date))
    data = c.fetchall()
    conn.close()
    return data

def get_workout_history(user_id, days=30):
    conn = sqlite3.connect('nutrition_app.db')
    c = conn.cursor()
    start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
    c.execute('SELECT date, exercise, duration, calories_burned FROM workout_logs WHERE user_id=? AND date>=? ORDER BY date',
             (user_id, start_date))
    data = c.fetchall()
    conn.close()
    return data

def export_to_csv(user_id):
    conn = sqlite3.connect('nutrition_app.db')
    df = pd.read_sql_query('SELECT * FROM meal_logs WHERE user_id=? ORDER BY date DESC LIMIT 100', conn, params=(user_id,))
    conn.close()
    return df.to_csv(index=False).encode()

def get_gemini_response(input_prompt, image_data=None):
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        content = [input_prompt]
        if image_data:
            content.extend(image_data)
        response = model.generate_content(content)
        return response.text
    except Exception as e:
        return f"❌ Error: {str(e)}"

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [{"mime_type": uploaded_file.type, "data": bytes_data}]
        return image_parts
    return None

# Load CSV Data
def load_meals_from_csv():
    """Load meals from CSV file"""
    try:
        df = pd.read_csv('meals.csv')
        meals = []
        for _, row in df.iterrows():
            meal = {
                'name': row['name'],
                'calories': int(row['calories']),
                'prep_time': row['prep_time'],
                'protein': float(row['protein']),
                'carbs': float(row['carbs']),
                'fats': float(row['fats']),
                'ingredients': row['ingredients'].split(',')
            }
            meals.append(meal)
        return meals
    except FileNotFoundError:
        return None

def load_workouts_from_csv():
    """Load workouts from CSV file"""
    try:
        df = pd.read_csv('workouts.csv')
        workouts = []
        for _, row in df.iterrows():
            workout = {
                'name': row['name'],
                'duration': int(row['duration_mins']),
                'calories': int(row['calories_burned']),
                'intensity': row['intensity'].lower()
            }
            workouts.append(workout)
        return workouts
    except FileNotFoundError:
        return None

# Sample Data (fallback if CSV files not found)
SAMPLE_RECIPES = [
    {'name': 'Quinoa Buddha Bowl', 'calories': 450, 'prep_time': '15 mins', 
     'ingredients': ['Quinoa', 'Spinach', 'Chickpeas', 'Avocado', 'Tahini'],
     'protein': 18, 'carbs': 52, 'fats': 16},
    {'name': 'Grilled Salmon with Asparagus', 'calories': 520, 'prep_time': '20 mins',
     'ingredients': ['Salmon', 'Asparagus', 'Olive Oil', 'Lemon'],
     'protein': 45, 'carbs': 8, 'fats': 28},
    {'name': 'Chickpea Curry', 'calories': 380, 'prep_time': '25 mins',
     'ingredients': ['Chickpeas', 'Coconut Milk', 'Curry Spice', 'Spinach', 'Tomatoes'],
     'protein': 14, 'carbs': 48, 'fats': 12},
    {'name': 'Zucchini Noodles with Pesto', 'calories': 320, 'prep_time': '10 mins',
     'ingredients': ['Zucchini', 'Basil', 'Olive Oil', 'Garlic', 'Seeds'],
     'protein': 12, 'carbs': 18, 'fats': 18},
    {'name': 'Lentil Soup', 'calories': 280, 'prep_time': '30 mins',
     'ingredients': ['Red Lentils', 'Vegetables', 'Vegetable Broth', 'Spices'],
     'protein': 16, 'carbs': 42, 'fats': 4},
]

WORKOUT_TEMPLATES = [
    {'name': 'HIIT Training', 'duration': 30, 'calories': 400, 'intensity': 'high'},
    {'name': 'Running', 'duration': 45, 'calories': 450, 'intensity': 'moderate'},
    {'name': 'Yoga', 'duration': 60, 'calories': 200, 'intensity': 'low'},
    {'name': 'Weight Training', 'duration': 60, 'calories': 300, 'intensity': 'high'},
    {'name': 'Swimming', 'duration': 45, 'calories': 500, 'intensity': 'moderate'},
    {'name': 'Cycling', 'duration': 60, 'calories': 550, 'intensity': 'moderate'},
    {'name': 'Walking', 'duration': 30, 'calories': 150, 'intensity': 'low'},
]

NUTRITION_ARTICLES = [
    {'title': 'Complete Guide to Macronutrients', 'preview': 'Understanding protein, carbs, and fats and their roles in your body...'},
    {'title': 'Benefits of Intermittent Fasting', 'preview': 'How intermittent fasting works and who should consider it...'},
    {'title': 'Hydration & Performance', 'preview': 'Why water intake matters for fitness and overall health...'},
    {'title': 'Healthy Eating on a Budget', 'preview': 'Tips for nutritious meals without breaking the bank...'},
    {'title': 'Superfoods You Should Know About', 'preview': 'Nutrient-dense foods to add to your diet for better health...'},
]

# PAGE CONFIG
st.set_page_config(page_title="AI Health Companion", layout="wide", initial_sidebar_state="expanded")

# Initialize session state
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'current_date' not in st.session_state:
    st.session_state.current_date = datetime.now().strftime('%Y-%m-%d')

# Load CSV data at startup
csv_recipes = load_meals_from_csv()
csv_workouts = load_workouts_from_csv()

# Use CSV data if available, otherwise use sample data
if csv_recipes:
    SAMPLE_RECIPES = csv_recipes
if csv_workouts:
    WORKOUT_TEMPLATES = csv_workouts


# LOGIN/SIGNUP PAGE
def show_login_page():
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("## 👤 Login")
        login_username = st.text_input("Username", key="login_user")
        login_password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login", key="login_btn"):
            user_id = authenticate_user(login_username, login_password)
            if user_id:
                st.session_state.user_id = user_id
                st.success("✅ Logged in successfully!")
                st.rerun()
            else:
                st.error("❌ Invalid credentials")
    
    with col2:
        st.markdown("## 📝 Sign Up")
        signup_username = st.text_input("New Username", key="signup_user")
        signup_password = st.text_input("New Password", type="password", key="signup_pass")
        signup_confirm = st.text_input("Confirm Password", type="password", key="signup_confirm")
        
        if st.button("Create Account", key="signup_btn"):
            if signup_password != signup_confirm:
                st.error("❌ Passwords don't match")
            elif len(signup_password) < 6:
                st.error("❌ Password must be at least 6 characters")
            elif create_user(signup_username, signup_password):
                st.success("✅ Account created! Please login.")
            else:
                st.error("❌ Username already exists")

# MAIN APP
def show_main_app():
    user_id = st.session_state.user_id
    
    # Header
    st.markdown("# 🤖 AI Health Companion - Complete Nutrition & Fitness Suite")
    
    col1, col2, col3 = st.columns([3, 1, 1])
    with col3:
        if st.button("🚪 Logout"):
            st.session_state.user_id = None
            st.rerun()
    
    # Sidebar - Health Profile & Quick Stats
    with st.sidebar:
        st.subheader("👤 Your Profile")
        
        col_a, col_b = st.columns(2)
        with col_a:
            weight = st.number_input("Weight (kg)", 0.0, 500.0, 70.0, key="weight_input")
            height_m = st.number_input("Height (m)", 1.0, 2.5, 1.75, key="height_input")
            age = st.number_input("Age", 13, 120, 30, key="age_input")
        
        with col_b:
            gender = st.selectbox("Gender", ["Male", "Female"], key="gender_select")
            activity = st.selectbox("Activity Level", 
                                   ["sedentary", "light", "moderate", "active", "very_active"],
                                   key="activity_select")
        
        # Quick metrics
        st.markdown("---")
        st.subheader("📊 Quick Metrics")
        
        bmi = calculate_bmi(weight, height_m)
        bmi_cat, bmi_emoji = get_bmi_category(bmi)
        tdee, bmr = calculate_tdee(weight, height_m * 100, age, gender, activity)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("BMI", f"{bmi} {bmi_emoji}", bmi_cat)
            st.metric("BMR", f"{bmr} cal")
        with col2:
            st.metric("TDEE", f"{tdee} cal")
            body_fat = calculate_body_fat_estimate(bmi, age, gender)
            st.metric("Body Fat %", f"{body_fat}%")
        
        # Daily totals
        st.markdown("---")
        daily_totals = get_daily_totals(user_id, st.session_state.current_date)
        st.subheader("📈 Today's Summary")
        
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            st.metric("Calories", f"{daily_totals['calories']} / {tdee}")
            st.metric("Protein", f"{daily_totals['protein']:.0f}g")
        with col_t2:
            st.metric("Carbs", f"{daily_totals['carbs']:.0f}g")
            st.metric("Fats", f"{daily_totals['fats']:.0f}g")
        
        water_intake = get_water_intake(user_id, st.session_state.current_date)
        st.metric("Water", f"{water_intake:.1f} / 8 cups")
    
    # TABS
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
        "🍽️ Meals", "💧 Water", "🏋️ Workouts", "⚖️ Progress", 
        "🏥 Health Metrics", "🎓 Education", "🛒 Shopping", "⭐ Favorites", "📊 Dashboard"
    ])
    
    # TAB 1: MEAL PLANNING & LOGGING
    with tab1:
        st.subheader("🍽️ Meal Management")
        col_m1, col_m2 = st.columns([2, 1])
        
        with col_m2:
            st.session_state.current_date = st.date_input("Select Date", 
                                                           datetime.now()).strftime('%Y-%m-%d')
        
        col_ma, col_mb = st.columns(2)
        
        with col_ma:
            st.write("### Quick Add Recipe")
            selected_recipe = st.selectbox("Choose Recipe", [r['name'] for r in SAMPLE_RECIPES])
            if st.button("➕ Add Recipe to Meal Log"):
                recipe = next(r for r in SAMPLE_RECIPES if r['name'] == selected_recipe)
                meal_data = {
                    'date': st.session_state.current_date,
                    'meal_type': 'recipe',
                    'food_name': recipe['name'],
                    'calories': recipe['calories'],
                    'protein': recipe['protein'],
                    'carbs': recipe['carbs'],
                    'fats': recipe['fats']
                }
                save_meal_log(user_id, meal_data)
                st.success(f"✅ Added {recipe['name']}")
                st.rerun()
        
        with col_mb:
            st.write("### Manual Entry")
            food_name = st.text_input("Food Name")
            cal_input = st.number_input("Calories", 0, 2000, 500)
            protein_input = st.number_input("Protein (g)", 0.0, 200.0, 25.0)
            carbs_input = st.number_input("Carbs (g)", 0.0, 300.0, 50.0)
            fats_input = st.number_input("Fats (g)", 0.0, 100.0, 20.0)
            
            if st.button("➕ Add Meal"):
                if food_name:
                    meal_data = {
                        'date': st.session_state.current_date,
                        'meal_type': 'manual',
                        'food_name': food_name,
                        'calories': cal_input,
                        'protein': protein_input,
                        'carbs': carbs_input,
                        'fats': fats_input
                    }
                    save_meal_log(user_id, meal_data)
                    st.success("✅ Meal added!")
                    st.rerun()
        
        st.markdown("---")
        st.write("### Today's Meals")
        meals = get_meal_logs(user_id, st.session_state.current_date)
        if meals:
            meal_df = pd.DataFrame(meals, columns=['ID', 'User', 'Date', 'Type', 'Food', 'Cal', 'P', 'C', 'F', 'Created'])
            st.dataframe(meal_df[['Food', 'Cal', 'P', 'C', 'F']], use_container_width=True)
        else:
            st.info("No meals logged yet")
        
        # AI Meal Planning
        st.markdown("---")
        st.write("### 🤖 AI Meal Plan Generator")
        goal = st.text_area("Describe your meal plan goals",
                           placeholder="e.g., Vegetarian weight loss plan for 1500 calories")
        if st.button("🚀 Generate AI Meal Plan"):
            if goal:
                with st.spinner("Generating personalized meal plan..."):
                    prompt = f"""Create a detailed meal plan for: {goal}
                    Include:
                    1. 7-day meal schedule
                    2. Calorie targets and macros
                    3. Shopping list
                    4. Prep tips
                    Format with clear sections."""
                    response = get_gemini_response(prompt)
                    st.markdown(response)
                    st.download_button("📥 Download Plan", response, "meal_plan.txt", "text/plain")
    
    # TAB 2: WATER TRACKING
    with tab2:
        st.subheader("💧 Hydration Tracker")
        
        col_w1, col_w2, col_w3 = st.columns(3)
        with col_w1:
            cups_to_add = st.number_input("Cups to add", 0.0, 10.0, 1.0, key="water_cups")
            if st.button("➕ Add Water"):
                save_water_log(user_id, cups_to_add, st.session_state.current_date)
                st.success("✅ Water logged!")
                st.rerun()
        
        with col_w2:
            st.metric("Daily Goal", "8 cups")
            current_water = get_water_intake(user_id, st.session_state.current_date)
            st.metric("Current", f"{current_water:.1f} cups")
        
        with col_w3:
            remaining = max(0, 8 - current_water)
            st.metric("Remaining", f"{remaining:.1f} cups")
        
        # Progress bar
        st.progress(min(current_water / 8, 1.0))
        
        # Tips
        st.info("""
        💧 **Hydration Tips:**
        - Drink water with every meal
        - Start your day with a glass of water
        - Keep a water bottle with you
        - Drink before, during, and after workouts
        """)
    
    # TAB 3: WORKOUTS
    with tab3:
        st.subheader("🏋️ Workout Tracking")
        
        col_w1, col_w2 = st.columns(2)
        
        with col_w1:
            st.write("### Quick Log Workout")
            workout_name = st.selectbox("Select Workout", [w['name'] for w in WORKOUT_TEMPLATES])
            selected_workout = next(w for w in WORKOUT_TEMPLATES if w['name'] == workout_name)
            
            duration = st.number_input("Duration (minutes)", 0, 300, selected_workout['duration'])
            
            if st.button("➕ Log Workout"):
                workout_data = {
                    'date': st.session_state.current_date,
                    'exercise': selected_workout['name'],
                    'duration': duration,
                    'calories_burned': int(selected_workout['calories'] * duration / selected_workout['duration']),
                    'intensity': selected_workout['intensity']
                }
                save_workout(user_id, workout_data)
                st.success("✅ Workout logged!")
                st.rerun()
        
        with col_w2:
            st.write("### Workout Templates")
            for w in WORKOUT_TEMPLATES:
                st.write(f"**{w['name']}** - {w['duration']}min, {w['calories']}cal, {w['intensity']} intensity")
        
        # Workout history chart
        st.markdown("---")
        workout_hist = get_workout_history(user_id, 30)
        if workout_hist:
            workout_df = pd.DataFrame(workout_hist, columns=['Date', 'Exercise', 'Duration', 'Calories'])
            st.write("### Last 30 Days Workouts")
            st.dataframe(workout_df, use_container_width=True)
            
            # Chart
            fig = px.bar(workout_df, x='Date', y='Calories', title='Calories Burned by Workout',
                        labels={'Calories': 'Calories Burned'})
            st.plotly_chart(fig, use_container_width=True)
    
    # TAB 4: PROGRESS TRACKING
    with tab4:
        st.subheader("⚖️ Body Measurements")
        
        col_p1, col_p2 = st.columns(2)
        
        with col_p1:
            st.write("### Log Measurements")
            meas_weight = st.number_input("Weight (kg)", 0.0, 500.0, 70.0, key="meas_weight")
            meas_waist = st.number_input("Waist (cm)", 0.0, 200.0, 80.0, key="meas_waist")
            meas_hip = st.number_input("Hip (cm)", 0.0, 200.0, 90.0, key="meas_hip")
            meas_chest = st.number_input("Chest (cm)", 0.0, 200.0, 95.0, key="meas_chest")
            notes = st.text_area("Notes", key="meas_notes")
            
            if st.button("💾 Save Measurements"):
                progress_data = {
                    'date': st.session_state.current_date,
                    'weight': meas_weight,
                    'waist': meas_waist,
                    'hip': meas_hip,
                    'chest': meas_chest,
                    'notes': notes
                }
                save_progress(user_id, progress_data)
                st.success("✅ Measurements saved!")
                st.rerun()
        
        with col_p2:
            # Progress history
            progress_hist = get_progress_history(user_id, 90)
            if progress_hist:
                prog_df = pd.DataFrame(progress_hist, columns=['Date', 'Weight'])
                st.write("### Weight History (90 days)")
                st.dataframe(prog_df, use_container_width=True)
                
                # Weight chart
                fig = px.line(prog_df, x='Date', y='Weight', title='Weight Progress',
                             markers=True)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No measurements yet. Start logging today!")
    
    # TAB 5: HEALTH METRICS
    with tab5:
        st.subheader("🏥 Health Metrics Calculator")
        
        col_h1, col_h2 = st.columns(2)
        
        with col_h1:
            st.write("### Health Status")
            st.metric("BMI", f"{calculate_bmi(weight, height_m)}")
            st.metric("BMR", f"{calculate_tdee(weight, height_m * 100, age, gender, activity)[1]} cal/day")
            st.metric("Body Fat Est.", f"{calculate_body_fat_estimate(calculate_bmi(weight, height_m), age, gender)}%")
        
        with col_h2:
            st.write("### Goal Calculations")
            target_weight = st.number_input("Target Weight (kg)", 0.0, 500.0, 65.0)
            weeks_to_goal = st.number_input("Weeks to Goal", 1, 104, 12)
            
            calorie_deficit = get_calorie_deficit(calculate_tdee(weight, height_m * 100, age, gender, activity)[0], weeks_to_goal)
            weekly_loss = (weight - target_weight) / weeks_to_goal
            
            st.metric("Daily Calorie Target", f"{calorie_deficit} cal")
            st.metric("Weekly Loss", f"{weekly_loss:.2f} kg/week")
            st.metric("Total Loss Needed", f"{weight - target_weight:.1f} kg")
        
        # Macros breakdown
        st.markdown("---")
        st.write("### Macro Breakdown")
        protein_pct = st.slider("Protein %", 10, 50, 30)
        carb_pct = st.slider("Carbs %", 20, 60, 50)
        fat_pct = 100 - protein_pct - carb_pct
        
        macros = get_macro_breakdown(calculate_tdee(weight, height_m * 100, age, gender, activity)[0], 
                                    protein_pct, carb_pct, fat_pct)
        
        col_macro1, col_macro2, col_macro3 = st.columns(3)
        with col_macro1:
            st.metric("Protein", f"{macros['protein_g']:.0f}g ({protein_pct}%)")
        with col_macro2:
            st.metric("Carbs", f"{macros['carbs_g']:.0f}g ({carb_pct}%)")
        with col_macro3:
            st.metric("Fats", f"{macros['fat_g']:.0f}g ({fat_pct}%)")
    
    # TAB 6: EDUCATION
    with tab6:
        st.subheader("🎓 Nutrition & Health Education")
        
        for article in NUTRITION_ARTICLES:
            with st.expander(f"📚 {article['title']}"):
                st.write(article['preview'])
                
                if st.button(f"Read more: {article['title']}", key=article['title']):
                    prompt = f"Provide detailed information about: {article['title']}"
                    response = get_gemini_response(prompt)
                    st.markdown(response)
    
    # TAB 7: SHOPPING LIST
    with tab7:
        st.subheader("🛒 Smart Shopping List")
        
        col_s1, col_s2 = st.columns(2)
        
        with col_s1:
            st.write("### Generate Shopping List")
            meals_for_week = st.multiselect("Select meals for the week", [r['name'] for r in SAMPLE_RECIPES])
            
            if st.button("📋 Generate Shopping List"):
                selected_meals = [r for r in SAMPLE_RECIPES if r['name'] in meals_for_week]
                ingredients = []
                for meal in selected_meals:
                    ingredients.extend(meal['ingredients'])
                
                st.write("### Shopping List")
                for ing in sorted(set(ingredients)):
                    st.write(f"☐ {ing}")
        
        with col_s2:
            st.write("### Budget Planner")
            budget = st.number_input("Weekly Budget ($)", 0, 500, 100)
            servings = st.number_input("Number of People", 1, 10, 1)
            
            daily_budget = budget / 7 / servings
            st.metric("Daily Budget per Person", f"${daily_budget:.2f}")
            
            st.info(f"💰 Estimated cost per meal: ${daily_budget:.2f}")
    
    # TAB 8: FAVORITES
    with tab8:
        st.subheader("⭐ Saved Favorites")
        
        st.write("### Favorite Recipes")
        for recipe in SAMPLE_RECIPES[:3]:
            col_f1, col_f2 = st.columns([3, 1])
            with col_f1:
                st.write(f"**{recipe['name']}** - {recipe['calories']} cal")
            with col_f2:
                if st.button("❤️", key=f"fav_{recipe['name']}"):
                    st.success("Added to favorites!")
    
    # TAB 9: DASHBOARD
    with tab9:
        st.subheader("📊 Weekly Summary Dashboard")
        
        # Get 7-day data
        week_data = []
        for i in range(7):
            date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
            totals = get_daily_totals(user_id, date)
            week_data.append({'Date': date, **totals})
        
        week_df = pd.DataFrame(week_data)
        
        col_d1, col_d2 = st.columns(2)
        
        with col_d1:
            st.write("### Calorie Intake (7 days)")
            fig_cal = px.bar(week_df, x='Date', y='calories', title='Daily Calories')
            st.plotly_chart(fig_cal, use_container_width=True)
        
        with col_d2:
            st.write("### Macro Distribution (Today)")
            daily = get_daily_totals(user_id)
            macro_data = {'Protein': daily['protein'], 'Carbs': daily['carbs'], 'Fats': daily['fats']}
            fig_macro = px.pie(values=macro_data.values(), names=macro_data.keys(), title='Macros')
            st.plotly_chart(fig_macro, use_container_width=True)
        
        st.markdown("---")
        st.write("### Export Data")
        csv_data = export_to_csv(user_id)
        st.download_button("📥 Download CSV", csv_data, "nutrition_data.csv", "text/csv")

# MAIN LOGIC
if st.session_state.user_id:
    show_main_app()
else:
    st.title("🤖 AI Health Companion")
    st.markdown("### Your Personal Nutrition & Fitness Coach")
    show_login_page()
