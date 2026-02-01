# 🏥 AI-Driven Smart Pediatric Health Advisor

A simplified web-based application that provides intelligent health guidance and nutritional recommendations for children using basic AI logic.

## 📋 Project Overview

This project was developed as a Final Year Project (FYP) to demonstrate how technology can assist parents and healthcare providers in understanding pediatric health conditions. The system analyzes symptoms, provides health advice, and offers age-appropriate nutritional guidance.

### 🎯 Key Features

- **Symptom Analysis**: Input child symptoms and get matched health conditions with advice
- **Nutrition Guidance**: Age-specific meal plans and dietary recommendations
- **User-Friendly Interface**: Clean, modern web design that's easy to navigate
- **Educational Purpose**: Beginner-friendly code that's easy to understand and modify

## 🚀 Technologies Used

| Technology | Purpose | Why We Use It |
|-----------|---------|---------------|
| **Python 3.x** | Backend programming | Easy to learn, powerful for data processing |
| **Flask** | Web framework | Lightweight, simple to understand |
| **HTML/CSS** | Frontend design | Standard web technologies |
| **JavaScript** | Interactive features | Makes the website dynamic |
| **JSON** | Data format | Easy way to structure data |

## 📁 Project Structure

```
pediatric-health-advisor/
│
├── app.py                 # Main application file (Backend logic)
├── templates/
│   └── index.html        # Web interface (Frontend)
├── requirements.txt      # Python dependencies
├── README.md             # This file
└── docs/
    ├── SETUP_GUIDE.md    # Installation instructions
    ├── TECH_EXPLAINED.md # Technology explanations
    └── DEMO_GUIDE.md     # How to present the project
```

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)
- A web browser

### Step-by-Step Installation

1. **Clone or Download the Repository**
```bash
git clone https://github.com/yourusername/pediatric-health-advisor.git
cd pediatric-health-advisor
```

2. **Install Required Packages**
```bash
pip install -r requirements.txt
```

3. **Run the Application**
```bash
python app.py
```

4. **Open in Browser**
- Go to: `http://localhost:5000`
- The application should be running!

## 💡 How It Works

### 1. Symptom Analysis
- User enters symptoms (e.g., "fever, cough")
- System uses **keyword matching** to find related conditions
- Displays advice and warning signs

**Simple Example:**
```python
# When user types "fever"
# System searches for keyword "fever" in conditions database
# Returns: Fever condition with causes, advice, warning signs
```

### 2. Nutrition Plan
- User enters child's age in months
- System selects appropriate age group (0-6 months, 6-12 months, etc.)
- Returns customized meal plan

**Simple Example:**
```python
# When user enters age = 8 months
# System selects "6-12 months" category
# Returns: Foods to eat, foods to avoid, feeding tips
```

## 📊 Data Structure Example

The application uses simple Python dictionaries to store information:

```python
PEDIATRIC_CONDITIONS = {
    "fever": {
        "name": "Fever",
        "keywords": ["fever", "hot", "temperature"],
        "causes": ["Viral infection", "Bacterial infection"],
        "advice": "Keep child hydrated, monitor temperature",
        "warning_signs": ["Fever above 104°F", "Lasts more than 3 days"]
    }
}
```

## 🎓 Learning Outcomes

By studying this project, you will understand:

1. **Web Development Basics**: How websites work (frontend + backend)
2. **Python Programming**: Functions, data structures, API endpoints
3. **Flask Framework**: Routing, templates, JSON responses
4. **Simple AI Logic**: Keyword matching algorithms
5. **User Interface Design**: Creating clean, responsive layouts

## 🔍 Key Code Sections to Understand

### 1. Finding Matching Conditions (app.py)
```python
def find_conditions(symptoms):
    """Matches user symptoms with health conditions"""
    symptoms_lower = symptoms.lower()
    results = []
    
    for key, condition in PEDIATRIC_CONDITIONS.items():
        for keyword in condition["keywords"]:
            if keyword in symptoms_lower:
                results.append(condition)
                break
    
    return results
```

### 2. Getting Nutrition Plan (app.py)
```python
def get_nutrition(age_months):
    """Returns age-appropriate nutrition plan"""
    if age_months < 6:
        return NUTRITION_PLANS["0-6"]
    elif age_months < 12:
        return NUTRITION_PLANS["6-12"]
    else:
        return NUTRITION_PLANS["12-36"]
```

### 3. API Endpoints (app.py)
```python
@app.route('/analyze', methods=['POST'])
def analyze():
    """Handles symptom analysis requests"""
    data = request.json
    symptoms = data.get('symptoms', '')
    conditions = find_conditions(symptoms)
    return jsonify({"success": True, "conditions": conditions})
```

## 🎨 Customization Ideas

You can easily extend this project:

1. **Add More Conditions**: Edit `PEDIATRIC_CONDITIONS` dictionary
2. **Add More Age Groups**: Expand `NUTRITION_PLANS`
3. **Improve UI**: Modify CSS in `index.html`
4. **Add Database**: Store data in SQLite instead of dictionaries
5. **Add User Accounts**: Let parents save their children's information

## ⚠️ Important Disclaimer

This application is for **educational and informational purposes only**. It does not replace professional medical advice, diagnosis, or treatment. Always consult qualified healthcare providers for medical concerns.

## 📝 Future Enhancements

- [ ] Add database to store user data
- [ ] Implement real machine learning models
- [ ] Add multilingual support
- [ ] Include vaccination tracking
- [ ] Add growth chart visualization
- [ ] Mobile app version

## 👨‍💻 For Job Interviews

When presenting this project, emphasize:

1. **Problem Solving**: Identified healthcare access gap for parents
2. **Technology Skills**: Python, Flask, web development
3. **User-Centric Design**: Easy-to-use interface
4. **Scalability**: Can be expanded with real AI/ML models
5. **Real-World Application**: Addresses actual healthcare needs

## 📚 Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Python Official Tutorial](https://docs.python.org/3/tutorial/)
- [HTML/CSS Basics](https://www.w3schools.com/)
- [JSON Format Guide](https://www.json.org/)


## 📄 License

This project is open source and available for educational purposes.

---

**Built with ❤️ for learning and healthcare awareness**
