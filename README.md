# -edunet-ibm-AICTE--batch-6-ALML-

# 🤖 AI Health Companion - Nutrition & Wellness App

A Streamlit-based AI-powered nutritionist and health advisor that uses Google's Gemini AI to provide personalized meal planning, food analysis, and health guidance.

## ✨ Features

### 🍽️ Meal Planning
- Personalized 7-day meal plans based on your health goals
- Nutritional breakdown (calories, macros, micros)
- Shopping lists with quantities and cost estimates
- Meal prep tips and time-saving suggestions

### 🔍 Food Analysis
- Upload food images for instant nutritional analysis
- Calorie estimation
- Macronutrient breakdown
- Dietary restriction compatibility checking
- Portion size recommendations

### 💡 Health Insights
- Ask nutrition and health questions
- Science-backed answers tailored to your profile
- Evidence-based recommendations
- Study references and credible sources

### 🥗 Recipe Suggestions
- Pre-loaded recipes matching your dietary needs
- Filter by diet type (vegetarian, gluten-free, low-carb, etc.)
- One-click meal logging
- Calorie tracking

### 📈 Progress Tracking
- Daily calorie counter
- Meal logging history
- Daily nutrition statistics
- Progress visualization

### 💾 Data Persistence
- SQLite database for saving health profiles
- Meal history tracking
- Food analysis history

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation

1. **Clone or download the project**
```bash
cd AICTE-BATCH6-NUTRITION-main
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Get your API Key**
   - Visit [Google AI Studio](https://aistudio.google.com/apikey)
   - Click "Create API Key"
   - Copy your API key

4. **Configure API Key**
   - Open `.env` file in the project folder
   - Replace the placeholder with your actual API key
   - Save the file

   Example `.env`:
   ```
   GOOGLE_API_KEY=your_actual_api_key_here
   ```

5. **Run the app**
```bash
streamlit run Nutrition1.py
```

The app will open in your browser at `http://localhost:8501`

## 📖 Usage Guide

### Setting Up Your Health Profile
1. In the left sidebar, fill in your health information:
   - **Health Goals**: Weight loss, fitness, health improvements
   - **Medical Conditions**: Any relevant conditions
   - **Fitness Routines**: Your current exercise habits
   - **Food Preferences**: Cuisine styles, cooking methods
   - **Dietary Restrictions**: Allergies, intolerances, ethical choices
2. Click **"Update Profile"** to save

### Generating Meal Plans
1. Go to **"Meal Planning"** tab
2. Optionally specify additional requirements
3. Click **"Generate Personalized Meal Plan"**
4. Review the 7-day plan, nutritional info, and shopping list
5. Download the plan if desired

### Analyzing Food
1. Go to **"Food Analysis"** tab
2. Upload a photo of your food
3. Click **"Analyze Food"**
4. View nutritional information and dietary compatibility
5. Optionally add to your meal log

### Getting Health Insights
1. Go to **"Health Insights"** tab
2. Ask any nutrition or health question
3. Receive science-backed, personalized answers

### Using Recipes
1. Go to **"Recipes"** tab
2. Browse pre-loaded recipe suggestions
3. Click on a recipe to see ingredients and nutritional info
4. Click **"Add to Meal Log"** to track it

### Tracking Progress
1. Go to **"Progress"** tab
2. View daily calorie intake and goals
3. Check your meal history
4. Reset daily log as needed

## 🎯 Demo Mode

If you don't have an API key configured yet, you can still explore all features using **Demo Mode**:

1. In the sidebar, check the **"Demo Mode (No API needed)"** checkbox
2. All features will use sample data and responses
3. No API calls will be made
4. Perfect for testing and learning the app

## 🔒 API Key Security

### ⚠️ IMPORTANT: Never share your API key!

Your API key in `.env` file:
- Is automatically loaded and never shown in code
- Should never be committed to version control
- Should be treated like a password

**To keep it safe:**
1. Add `.env` to `.gitignore` if using Git
2. Don't share your `.env` file
3. If compromised, regenerate your key at [Google AI Studio](https://aistudio.google.com/apikey)
4. Use environment variables for deployment

## 📊 Database

The app stores data in `nutrition_app.db` (SQLite) with tables for:
- **health_profiles**: Your health and dietary information
- **meal_logs**: Daily meal entries with calories
- **food_analysis_history**: Previous food analyses

## 🛠️ Troubleshooting

### "API key not valid" Error
**Solution:** 
1. Make sure your `.env` file exists in the project folder
2. Verify you copied the entire API key correctly
3. Check that `GOOGLE_API_KEY=` line has no extra spaces
4. Restart the Streamlit app after updating `.env`
5. Use Demo Mode to test if the issue is API-related

### "Import not found" Error
**Solution:**
```bash
pip install -r requirements.txt
```

### App won't start
**Solution:**
1. Make sure Streamlit is installed: `pip install streamlit`
2. Use: `streamlit run Nutrition1.py`
3. Check terminal for detailed error messages

### Demo Mode isn't working
**Solution:** 
Enable Demo Mode in the sidebar checkbox at the top of the left panel

## 📚 Pre-loaded Sample Data

The app includes sample health profiles and recipes to demonstrate features:

### Sample Recipes
- Quinoa Buddha Bowl (450 cal)
- Grilled Salmon with Asparagus (520 cal)
- Chickpea Curry (380 cal)
- Zucchini Noodles with Pesto (320 cal)
- Lentil Soup (280 cal)

### Sample Health Profile
- **Goals**: Weight loss, cardiovascular health, energy
- **Routines**: Walking 3x/week, yoga 2x/week
- **Preferences**: Vegetarian, low carb
- **Restrictions**: No dairy, no nuts, gluten-free

## 🔄 Updates & Improvements

### Planned Features
- [ ] Workout recommendations based on health goals
- [ ] Integration with fitness apps (Apple Health, Fitbit)
- [ ] Multi-language support
- [ ] Voice input for hands-free operation
- [ ] Mobile app version
- [ ] Community recipe sharing
- [ ] Nutritionist consultation booking
- [ ] Progress photos and body measurements

### Recent Improvements
✅ Secure API key handling with environment variables
✅ Demo Mode for testing without API key
✅ Data persistence with SQLite
✅ Daily calorie tracking
✅ Recipe suggestions and meal logging
✅ Better error messages and guidance
✅ Expanded health insights with science-backed recommendations
✅ Pre-loaded sample data

## 📝 Disclaimer

This app is for **educational and informational purposes only**. It should not replace professional medical or nutritional advice.

**Always consult a healthcare professional before:**
- Making significant dietary changes
- Starting a new exercise program
- If you have medical conditions
- If you have allergies or intolerances

## 🤝 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review error messages in the Streamlit sidebar
3. Ensure your API key is valid at [Google AI Studio](https://aistudio.google.com/apikey)
4. Try Demo Mode to verify the app works

## 📄 License

This project is created for educational purposes.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io)
- Powered by [Google Gemini AI](https://ai.google.dev)
- Community health and nutrition best practices

---

**Version**: 2.0 (Enhanced with API security, Demo Mode, and data persistence)
**Last Updated**: January 2026
<<<<<<< HEAD
# -edunet-ibm-AICTE--batch-6-ALML-
=======
# 🤖 AI Health Companion - Nutrition & Wellness App

A Streamlit-based AI-powered nutritionist and health advisor that uses Google's Gemini AI to provide personalized meal planning, food analysis, and health guidance.

## ✨ Features

### 🍽️ Meal Planning
- Personalized 7-day meal plans based on your health goals
- Nutritional breakdown (calories, macros, micros)
- Shopping lists with quantities and cost estimates
- Meal prep tips and time-saving suggestions

### 🔍 Food Analysis
- Upload food images for instant nutritional analysis
- Calorie estimation
- Macronutrient breakdown
- Dietary restriction compatibility checking
- Portion size recommendations

### 💡 Health Insights
- Ask nutrition and health questions
- Science-backed answers tailored to your profile
- Evidence-based recommendations
- Study references and credible sources

### 🥗 Recipe Suggestions
- Pre-loaded recipes matching your dietary needs
- Filter by diet type (vegetarian, gluten-free, low-carb, etc.)
- One-click meal logging
- Calorie tracking

### 📈 Progress Tracking
- Daily calorie counter
- Meal logging history
- Daily nutrition statistics
- Progress visualization

### 💾 Data Persistence
- SQLite database for saving health profiles
- Meal history tracking
- Food analysis history

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation

1. **Clone or download the project**
```bash
cd AICTE-BATCH6-NUTRITION-main
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Get your API Key**
   - Visit [Google AI Studio](https://aistudio.google.com/apikey)
   - Click "Create API Key"
   - Copy your API key

4. **Configure API Key**
   - Open `.env` file in the project folder
   - Replace `your_actual_api_key_here_replace_this` with your actual API key
   - Save the file

   Example `.env`:
   ```
   GOOGLE_API_KEY=AIzaSyDqj69aWzAYeuAcMIcfJLgWBJ1234567890
   ```

5. **Run the app**
```bash
streamlit run Nutrition1.py
```

The app will open in your browser at `http://localhost:8501`

## 📖 Usage Guide

### Setting Up Your Health Profile
1. In the left sidebar, fill in your health information:
   - **Health Goals**: Weight loss, fitness, health improvements
   - **Medical Conditions**: Any relevant conditions
   - **Fitness Routines**: Your current exercise habits
   - **Food Preferences**: Cuisine styles, cooking methods
   - **Dietary Restrictions**: Allergies, intolerances, ethical choices
2. Click **"Update Profile"** to save

### Generating Meal Plans
1. Go to **"Meal Planning"** tab
2. Optionally specify additional requirements
3. Click **"Generate Personalized Meal Plan"**
4. Review the 7-day plan, nutritional info, and shopping list
5. Download the plan if desired

### Analyzing Food
1. Go to **"Food Analysis"** tab
2. Upload a photo of your food
3. Click **"Analyze Food"**
4. View nutritional information and dietary compatibility
5. Optionally add to your meal log

### Getting Health Insights
1. Go to **"Health Insights"** tab
2. Ask any nutrition or health question
3. Receive science-backed, personalized answers

### Using Recipes
1. Go to **"Recipes"** tab
2. Browse pre-loaded recipe suggestions
3. Click on a recipe to see ingredients and nutritional info
4. Click **"Add to Meal Log"** to track it

### Tracking Progress
1. Go to **"Progress"** tab
2. View daily calorie intake and goals
3. Check your meal history
4. Reset daily log as needed

## 🎯 Demo Mode

If you don't have an API key configured yet, you can still explore all features using **Demo Mode**:

1. In the sidebar, check the **"Demo Mode (No API needed)"** checkbox
2. All features will use sample data and responses
3. No API calls will be made
4. Perfect for testing and learning the app

## 🔒 API Key Security

### ⚠️ IMPORTANT: Never share your API key!

Your API key in `.env` file:
- Is automatically loaded and never shown in code
- Should never be committed to version control
- Should be treated like a password

**To keep it safe:**
1. Add `.env` to `.gitignore` if using Git
2. Don't share your `.env` file
3. If compromised, regenerate your key at [Google AI Studio](https://aistudio.google.com/apikey)
4. Use environment variables for deployment

## 📊 Database

The app stores data in `nutrition_app.db` (SQLite) with tables for:
- **health_profiles**: Your health and dietary information
- **meal_logs**: Daily meal entries with calories
- **food_analysis_history**: Previous food analyses

## 🛠️ Troubleshooting

### "API key not valid" Error
**Solution:** 
1. Make sure your `.env` file exists in the project folder
2. Verify you copied the entire API key correctly
3. Check that `GOOGLE_API_KEY=` line has no extra spaces
4. Restart the Streamlit app after updating `.env`
5. Use Demo Mode to test if the issue is API-related

### "Import not found" Error
**Solution:**
```bash
pip install -r requirements.txt
```

### App won't start
**Solution:**
1. Make sure Streamlit is installed: `pip install streamlit`
2. Use: `streamlit run Nutrition1.py`
3. Check terminal for detailed error messages

### Demo Mode isn't working
**Solution:** 
Enable Demo Mode in the sidebar checkbox at the top of the left panel

## 📚 Pre-loaded Sample Data

The app includes sample health profiles and recipes to demonstrate features:

### Sample Recipes
- Quinoa Buddha Bowl (450 cal)
- Grilled Salmon with Asparagus (520 cal)
- Chickpea Curry (380 cal)
- Zucchini Noodles with Pesto (320 cal)
- Lentil Soup (280 cal)

### Sample Health Profile
- **Goals**: Weight loss, cardiovascular health, energy
- **Routines**: Walking 3x/week, yoga 2x/week
- **Preferences**: Vegetarian, low carb
- **Restrictions**: No dairy, no nuts, gluten-free

## 🔄 Updates & Improvements

### Planned Features
- [ ] Workout recommendations based on health goals
- [ ] Integration with fitness apps (Apple Health, Fitbit)
- [ ] Multi-language support
- [ ] Voice input for hands-free operation
- [ ] Mobile app version
- [ ] Community recipe sharing
- [ ] Nutritionist consultation booking
- [ ] Progress photos and body measurements

### Recent Improvements
✅ Secure API key handling with environment variables
✅ Demo Mode for testing without API key
✅ Data persistence with SQLite
✅ Daily calorie tracking
✅ Recipe suggestions and meal logging
✅ Better error messages and guidance
✅ Expanded health insights with science-backed recommendations
✅ Pre-loaded sample data

## 📝 Disclaimer

This app is for **educational and informational purposes only**. It should not replace professional medical or nutritional advice.

**Always consult a healthcare professional before:**
- Making significant dietary changes
- Starting a new exercise program
- If you have medical conditions
- If you have allergies or intolerances

## 🤝 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review error messages in the Streamlit sidebar
3. Ensure your API key is valid at [Google AI Studio](https://aistudio.google.com/apikey)
4. Try Demo Mode to verify the app works

## 📄 License

This project is created for educational purposes.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io)
- Powered by [Google Gemini AI](https://ai.google.dev)
- Community health and nutrition best practices

---

**Version**: 2.0 (Enhanced with API security, Demo Mode, and data persistence)
**Last Updated**: January 2026
>>>>>>> cd59082 (Initial commit: AICTE Batch 6 Nutrition App)
