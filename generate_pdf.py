from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib import colors
from datetime import datetime
import os

# Create PDF
pdf_filename = "AI_Health_Companion_Project_Documentation.pdf"
doc = SimpleDocTemplate(pdf_filename, pagesize=A4, topMargin=0.5*inch, bottomMargin=0.5*inch)

# Styles
styles = getSampleStyleSheet()
title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Heading1'],
    fontSize=24,
    textColor=colors.HexColor('#2C3E50'),
    spaceAfter=10,
    alignment=1
)

heading_style = ParagraphStyle(
    'CustomHeading',
    parent=styles['Heading2'],
    fontSize=14,
    textColor=colors.HexColor('#34495E'),
    spaceAfter=8,
    spaceBefore=8
)

body_style = ParagraphStyle(
    'CustomBody',
    parent=styles['BodyText'],
    fontSize=10,
    spaceAfter=6
)

# Content
story = []

# Title Page
story.append(Spacer(1, 0.5*inch))
story.append(Paragraph("🤖 AI HEALTH COMPANION", title_style))
story.append(Paragraph("Complete Nutrition & Fitness Suite", styles['Heading2']))
story.append(Spacer(1, 0.3*inch))
story.append(Paragraph(f"<b>Project Documentation</b><br/>Generated: {datetime.now().strftime('%B %d, %Y')}", body_style))
story.append(Spacer(1, 0.5*inch))

# Project Overview
story.append(Paragraph("PROJECT OVERVIEW", heading_style))
story.append(Paragraph("""
<b>Project Name:</b> AI Health Companion - Complete Nutrition & Fitness Suite<br/>
<b>Type:</b> Web Application | Health & Wellness | AI-Powered Platform<br/>
<b>Technology Stack:</b> Python, Streamlit, SQLite, Google Gemini AI<br/>
<b>Target Users:</b> Fitness enthusiasts, Weight loss seekers, Health-conscious individuals<br/>
<b>Status:</b> Fully Functional (v1.0)
""", body_style))
story.append(Spacer(1, 0.2*inch))

# Key Objectives
story.append(Paragraph("KEY OBJECTIVES", heading_style))
objectives = [
    "Provide AI-powered personalized meal planning",
    "Enable comprehensive nutrition tracking (calories, macros, water intake)",
    "Facilitate workout logging and progress monitoring",
    "Calculate advanced health metrics (BMI, BMR, TDEE, body fat %)",
    "Generate smart shopping lists with budget planning",
    "Deliver nutritional education content",
    "Support multi-user accounts with data persistence",
    "Visualize progress with interactive charts"
]
for obj in objectives:
    story.append(Paragraph(f"✓ {obj}", body_style))
story.append(Spacer(1, 0.2*inch))

# Features Overview Table
story.append(Paragraph("FEATURES OVERVIEW", heading_style))
features_data = [
    ['Feature Module', 'Functionality', 'Status'],
    ['User Management', 'Login, signup, secure authentication', 'ACTIVE'],
    ['Meal Planning', 'Quick recipes, manual entry, AI generation', 'ACTIVE'],
    ['Water Tracking', 'Daily intake logging, 8-cup goal', 'ACTIVE'],
    ['Workouts', '7 templates, calorie tracking, 30-day history', 'ACTIVE'],
    ['Progress', 'Weight & measurements, 90-day charts', 'ACTIVE'],
    ['Health Metrics', 'BMI, BMR, TDEE, macro calculator', 'ACTIVE'],
    ['Education', '5 nutrition articles, AI insights', 'ACTIVE'],
    ['Shopping', 'List generator, budget planner', 'ACTIVE'],
    ['Favorites', 'Save recipes & workouts', 'ACTIVE'],
    ['Dashboard', '7-day summary, macro pie chart', 'ACTIVE'],
]

features_table = Table(features_data, colWidths=[1.5*inch, 2.5*inch, 0.7*inch])
features_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495E')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 10),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ('FONTSIZE', (0, 1), (-1, -1), 9),
]))
story.append(features_table)
story.append(Spacer(1, 0.2*inch))

# Page Break
story.append(PageBreak())

# Technical Stack
story.append(Paragraph("TECHNICAL STACK", heading_style))
tech_data = [
    ['Component', 'Technology', 'Version'],
    ['Frontend', 'Streamlit', '1.28+'],
    ['Backend', 'Python', '3.8+'],
    ['Database', 'SQLite3', 'Built-in'],
    ['AI/ML Engine', 'Google Gemini 2.5 Flash', 'Latest'],
    ['Data Visualization', 'Plotly, Pandas', 'Latest'],
    ['Security', 'SHA256 Hashing', 'Standard'],
    ['Configuration', 'Python-dotenv', 'Latest'],
]

tech_table = Table(tech_data, colWidths=[1.5*inch, 2*inch, 1.5*inch])
tech_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2980B9')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 10),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
    ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ('FONTSIZE', (0, 1), (-1, -1), 9),
]))
story.append(tech_table)
story.append(Spacer(1, 0.2*inch))

# Database Schema
story.append(Paragraph("DATABASE SCHEMA", heading_style))
story.append(Paragraph("""
<b>8 Main Tables:</b><br/>
✓ <b>users</b> - User authentication & credentials<br/>
✓ <b>health_profiles</b> - User health data & goals<br/>
✓ <b>meal_logs</b> - Daily meal tracking (calories, macros)<br/>
✓ <b>water_logs</b> - Hydration tracking<br/>
✓ <b>workout_logs</b> - Exercise history & calories burned<br/>
✓ <b>progress_tracking</b> - Body measurements & weight history<br/>
✓ <b>favorites</b> - Saved recipes & workouts<br/>
✓ <b>goals</b> - User goals & achievement tracking
""", body_style))
story.append(Spacer(1, 0.2*inch))

# Key Formulas
story.append(Paragraph("KEY FORMULAS & CALCULATIONS", heading_style))
story.append(Paragraph("""
<b>BMI:</b> Weight (kg) / Height (m) squared<br/>
Categories: Less than 18.5 (Underweight), 18.5-25 (Normal), 25-30 (Overweight), Over 30 (Obese)<br/><br/>

<b>BMR (Mifflin-St Jeor):</b><br/>
Male: 10*Weight + 6.25*Height - 5*Age + 5<br/>
Female: 10*Weight + 6.25*Height - 5*Age - 161<br/><br/>

<b>TDEE:</b> BMR * Activity Multiplier<br/>
(Sedentary: 1.2, Light: 1.375, Moderate: 1.55, Active: 1.725, Very Active: 1.9)<br/><br/>

<b>Body Fat Percentage:</b><br/>
Male: (1.20 * BMI) + (0.23 * Age) - 16.2<br/>
Female: (1.20 * BMI) + (0.23 * Age) - 5.4<br/><br/>

<b>Macro Breakdown:</b><br/>
Protein (g) = (Calories * Protein %) / 4<br/>
Carbs (g) = (Calories * Carbs %) / 4<br/>
Fats (g) = (Calories * Fats %) / 9
""", body_style))
story.append(Spacer(1, 0.2*inch))

# Page Break
story.append(PageBreak())

# Sample Data
story.append(Paragraph("SAMPLE DATA INCLUDED", heading_style))

story.append(Paragraph("<b>5 Pre-loaded Recipes:</b>", body_style))
recipes_data = [
    ['Recipe', 'Calories', 'Prep Time', 'Protein', 'Carbs', 'Fats'],
    ['Quinoa Buddha Bowl', '450', '15 min', '18g', '52g', '16g'],
    ['Grilled Salmon', '520', '20 min', '45g', '8g', '28g'],
    ['Chickpea Curry', '380', '25 min', '14g', '48g', '12g'],
    ['Zucchini Noodles', '320', '10 min', '12g', '18g', '18g'],
    ['Lentil Soup', '280', '30 min', '16g', '42g', '4g'],
]
recipes_table = Table(recipes_data, colWidths=[1.3*inch, 0.9*inch, 0.9*inch, 0.8*inch, 0.8*inch, 0.8*inch])
recipes_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#27AE60')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 9),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
    ('BACKGROUND', (0, 1), (-1, -1), colors.lightgreen),
    ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ('FONTSIZE', (0, 1), (-1, -1), 8),
]))
story.append(recipes_table)
story.append(Spacer(1, 0.15*inch))

story.append(Paragraph("<b>7 Workout Templates:</b>", body_style))
workouts_data = [
    ['Workout', 'Duration', 'Calories', 'Intensity'],
    ['HIIT Training', '30 min', '400 cal', 'High'],
    ['Running', '45 min', '450 cal', 'Moderate'],
    ['Yoga', '60 min', '200 cal', 'Low'],
    ['Weight Training', '60 min', '300 cal', 'High'],
    ['Swimming', '45 min', '500 cal', 'Moderate'],
    ['Cycling', '60 min', '550 cal', 'Moderate'],
    ['Walking', '30 min', '150 cal', 'Low'],
]
workouts_table = Table(workouts_data, colWidths=[1.5*inch, 1.2*inch, 1.2*inch, 1.1*inch])
workouts_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E74C3C')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 9),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
    ('BACKGROUND', (0, 1), (-1, -1), colors.lightsalmon),
    ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ('FONTSIZE', (0, 1), (-1, -1), 8),
]))
story.append(workouts_table)
story.append(Spacer(1, 0.15*inch))

story.append(Paragraph("<b>5 Educational Articles:</b>", body_style))
articles = [
    "Complete Guide to Macronutrients",
    "Benefits of Intermittent Fasting",
    "Hydration & Performance",
    "Healthy Eating on a Budget",
    "Superfoods You Should Know About"
]
for i, article in enumerate(articles, 1):
    story.append(Paragraph(f"{i}. {article}", body_style))
story.append(Spacer(1, 0.2*inch))

# Page Break
story.append(PageBreak())

# Security Features
story.append(Paragraph("SECURITY FEATURES", heading_style))
story.append(Paragraph("""
✓ SHA256 password hashing<br/>
✓ Environment variable API key storage (.env file)<br/>
✓ Per-user data isolation & authentication<br/>
✓ Secure session management (Streamlit sessions)<br/>
✓ Input validation on all user entries<br/>
✓ No hardcoded sensitive information<br/>
✓ Safe database queries with parameterization
""", body_style))
story.append(Spacer(1, 0.2*inch))

# Installation & Setup
story.append(Paragraph("INSTALLATION & SETUP", heading_style))
story.append(Paragraph("""
<b>System Requirements:</b><br/>
• Python 3.8+<br/>
• 2GB+ RAM<br/>
• 500MB free disk space<br/>
• Modern web browser<br/><br/>

<b>Installation Steps:</b><br/>
1. Clone repository<br/>
2. Navigate to folder<br/>
3. Create virtual environment: python -m venv venv<br/>
4. Activate venv<br/>
5. Install packages: pip install -r requirements.txt<br/>
6. Create .env file with GOOGLE_API_KEY<br/>
7. Run app: streamlit run Nutrition1.py<br/>
8. Access at: http://localhost:8501<br/>
""", body_style))
story.append(Spacer(1, 0.2*inch))

# Testing Checklist
story.append(Paragraph("TESTING CHECKLIST", heading_style))
tests = [
    "User registration & login functionality",
    "Health profile creation & updates",
    "Meal logging (quick add & manual entry)",
    "Water intake tracking",
    "Workout logging & history",
    "Progress measurements & charts",
    "Health metrics calculations",
    "AI meal plan generation",
    "Shopping list generation",
    "Dashboard visualizations",
    "Data export to CSV",
    "Multi-user data isolation"
]
for test in tests:
    story.append(Paragraph(f"☐ {test}", body_style))
story.append(Spacer(1, 0.2*inch))

# Page Break
story.append(PageBreak())

# Future Enhancements
story.append(Paragraph("FUTURE ENHANCEMENTS", heading_style))

story.append(Paragraph("<b>Phase 2 - Advanced Features:</b>", body_style))
phase2 = [
    "Mobile app version (React Native)",
    "Fitness tracker integrations (Google Fit, Apple Health)",
    "Barcode scanner for packaged foods",
    "Recipe video tutorials"
]
for p in phase2:
    story.append(Paragraph(f"→ {p}", body_style))
story.append(Spacer(1, 0.1*inch))

story.append(Paragraph("<b>Phase 3 - Social & AI:</b>", body_style))
phase3 = [
    "Social features (recipe sharing, leaderboards)",
    "Nutritionist consultation booking",
    "Voice assistant integration",
    "Advanced ML-based recommendations"
]
for p in phase3:
    story.append(Paragraph(f"→ {p}", body_style))
story.append(Spacer(1, 0.1*inch))

story.append(Paragraph("<b>Phase 4 - Enterprise:</b>", body_style))
phase4 = [
    "Machine learning personalization engine",
    "Restaurant integration with menu analysis",
    "Offline mode support",
    "Cloud sync across devices"
]
for p in phase4:
    story.append(Paragraph(f"→ {p}", body_style))
story.append(Spacer(1, 0.2*inch))

# Project Metrics
story.append(Paragraph("PROJECT METRICS", heading_style))
metrics_data = [
    ['Metric', 'Value'],
    ['Total Feature Modules', '10+'],
    ['Database Tables', '8'],
    ['Pre-loaded Recipes', '5'],
    ['Workout Templates', '7'],
    ['Educational Articles', '5'],
    ['Supported Users', 'Unlimited'],
    ['Data History Tracked', 'Up to 90 days'],
    ['Health Formulas', '6 advanced'],
    ['API Integrations', 'Google Gemini AI'],
]
metrics_table = Table(metrics_data, colWidths=[3*inch, 2*inch])
metrics_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#8E44AD')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 10),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), colors.plum),
    ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ('FONTSIZE', (0, 1), (-1, -1), 9),
]))
story.append(metrics_table)
story.append(Spacer(1, 0.3*inch))

# Footer
story.append(Paragraph("""
<b>AI Health Companion - Complete Nutrition & Fitness Suite</b><br/>
<i>Powered by Google Gemini AI | Built with Streamlit | Python Backend</i><br/>
Generated: """ + datetime.now().strftime('%B %d, %Y at %H:%M:%S') + """
""", body_style))

# Build PDF
doc.build(story)
print(f"SUCCESS: PDF created - {pdf_filename}")
print(f"Location: {os.path.abspath(pdf_filename)}")
