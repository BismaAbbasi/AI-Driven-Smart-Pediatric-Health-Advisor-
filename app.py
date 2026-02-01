"""
AI-Driven Smart Pediatric Health Advisor
Complete standalone version - HTML included in Python file
"""

from flask import Flask, request, jsonify

app = Flask(__name__)

# Knowledge base
PEDIATRIC_CONDITIONS = {
    "fever": {
        "name": "Fever",
        "keywords": ["fever", "hot", "temperature", "warm"],
        "causes": ["Viral infection", "Bacterial infection", "Teething"],
        "advice": "Keep child hydrated, monitor temperature, rest",
        "warning_signs": ["Fever above 104°F", "Lasts more than 3 days", "Child very sleepy"]
    },
    "cough": {
        "name": "Cough",
        "keywords": ["cough", "coughing"],
        "causes": ["Cold", "Allergies", "Asthma"],
        "advice": "Use humidifier, give warm fluids, honey (if over 1 year)",
        "warning_signs": ["Difficulty breathing", "Cough lasts 2+ weeks"]
    },
    "rash": {
        "name": "Rash",
        "keywords": ["rash", "spots", "skin", "red", "itchy"],
        "causes": ["Eczema", "Allergic reaction", "Viral infection"],
        "advice": "Keep skin moisturized, avoid irritants",
        "warning_signs": ["Rash spreads fast", "With high fever", "Breathing problems"]
    }
}

NUTRITION_PLANS = {
    "0-6": {
        "age": "0-6 months",
        "foods": ["Breast milk or formula only"],
        "avoid": ["Solid foods", "Honey", "Cow's milk"],
        "tips": ["Feed on demand 8-12 times per day"]
    },
    "6-12": {
        "age": "6-12 months",
        "foods": ["Breast milk/formula", "Pureed vegetables", "Soft fruits", "Iron cereal"],
        "avoid": ["Honey", "Whole nuts", "Added salt/sugar"],
        "tips": ["Introduce one food at a time", "Watch for allergies"]
    },
    "12-36": {
        "age": "1-3 years",
        "foods": ["Whole milk", "Soft fruits", "Cooked vegetables", "Eggs", "Chicken"],
        "avoid": ["Choking hazards", "Excessive juice"],
        "tips": ["3 meals + 2 snacks daily", "Small portions"]
    }
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Pediatric Health Advisor</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 900px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        
        header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }
        
        header h1 { font-size: 2.2em; margin-bottom: 10px; }
        header p { font-size: 1.1em; opacity: 0.9; }
        
        .tabs {
            display: flex;
            border-bottom: 2px solid #e0e0e0;
            background: #f5f5f5;
        }
        
        .tab {
            flex: 1;
            padding: 15px;
            text-align: center;
            cursor: pointer;
            border: none;
            background: none;
            font-size: 1.1em;
            color: #666;
            transition: all 0.3s;
        }
        
        .tab:hover { background: #fff; color: #667eea; }
        .tab.active { background: #fff; color: #667eea; border-bottom: 3px solid #667eea; }
        
        .content {
            padding: 40px;
        }
        
        .tab-panel {
            display: none;
        }
        
        .tab-panel.active {
            display: block;
            animation: fadeIn 0.5s;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        label {
            display: block;
            margin-bottom: 8px;
            color: #333;
            font-weight: 600;
        }
        
        input, textarea {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 1em;
        }
        
        input:focus, textarea:focus {
            outline: none;
            border-color: #667eea;
        }
        
        textarea {
            min-height: 100px;
            resize: vertical;
        }
        
        button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 12px 30px;
            border: none;
            border-radius: 8px;
            font-size: 1.1em;
            cursor: pointer;
            transition: transform 0.2s;
        }
        
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        
        .results {
            margin-top: 30px;
            display: none;
        }
        
        .results.show {
            display: block;
            animation: slideIn 0.5s;
        }
        
        @keyframes slideIn {
            from { opacity: 0; transform: translateX(-20px); }
            to { opacity: 1; transform: translateX(0); }
        }
        
        .card {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 15px;
            border-left: 4px solid #667eea;
        }
        
        .card h3 {
            color: #667eea;
            margin-bottom: 10px;
        }
        
        .card ul {
            margin-left: 20px;
        }
        
        .card li {
            margin-bottom: 5px;
        }
        
        .warning {
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 15px;
            border-radius: 5px;
            margin-top: 20px;
        }
        
        .loading {
            text-align: center;
            padding: 20px;
            display: none;
        }
        
        .loading.show { display: block; }
        
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🏥 AI Pediatric Health Advisor</h1>
            <p>Smart health guidance for children</p>
        </header>
        
        <div class="tabs">
            <button class="tab active" onclick="switchTab('symptoms')">Symptoms</button>
            <button class="tab" onclick="switchTab('nutrition')">Nutrition</button>
            <button class="tab" onclick="switchTab('about')">About</button>
        </div>
        
        <div class="content">
            <!-- Symptoms Tab -->
            <div id="symptoms" class="tab-panel active">
                <h2>Symptom Analysis</h2>
                <form id="symptom-form">
                    <div class="form-group">
                        <label>Describe symptoms:</label>
                        <textarea id="symptoms-input" placeholder="e.g., fever, cough, rash..."></textarea>
                    </div>
                    <button type="submit">Analyze Symptoms</button>
                </form>
                
                <div class="loading" id="symptoms-loading">
                    <div class="spinner"></div>
                    <p>Analyzing...</p>
                </div>
                
                <div class="results" id="symptoms-results"></div>
            </div>
            
            <!-- Nutrition Tab -->
            <div id="nutrition" class="tab-panel">
                <h2>Nutrition Plan</h2>
                <form id="nutrition-form">
                    <div class="form-group">
                        <label>Child's age (months):</label>
                        <input type="number" id="age-input" min="0" max="36" placeholder="e.g., 12">
                    </div>
                    <button type="submit">Get Nutrition Plan</button>
                </form>
                
                <div class="loading" id="nutrition-loading">
                    <div class="spinner"></div>
                    <p>Loading...</p>
                </div>
                
                <div class="results" id="nutrition-results"></div>
            </div>
            
            <!-- About Tab -->
            <div id="about" class="tab-panel">
                <h2>About This Project</h2>
                <div class="card">
                    <h3>📋 Project Overview</h3>
                    <p><strong>AI-Driven Smart Pediatric Health Advisor</strong></p>
                    <p>A web application that provides health guidance for children.</p>
                    <p style="margin-top:10px;"><strong>Technologies:</strong> Python, Flask, HTML, CSS, JavaScript</p>
                </div>
                
                <div class="card">
                    <h3>✨ Features</h3>
                    <ul>
                        <li>Symptom analysis with health advice</li>
                        <li>Age-appropriate nutrition guidance</li>
                        <li>User-friendly interface</li>
                        <li>Emergency warning indicators</li>
                    </ul>
                </div>
                
                <div class="warning">
                    <strong>⚠️ Disclaimer:</strong> This is for educational purposes only. 
                    Always consult healthcare professionals for medical advice.
                </div>
            </div>
        </div>
    </div>
    
    <script>
        function switchTab(tabName) {
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
            
            event.target.classList.add('active');
            document.getElementById(tabName).classList.add('active');
        }
        
        // Symptom Analysis
        document.getElementById('symptom-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const loading = document.getElementById('symptoms-loading');
            const results = document.getElementById('symptoms-results');
            
            loading.classList.add('show');
            results.classList.remove('show');
            
            const symptoms = document.getElementById('symptoms-input').value;
            
            const response = await fetch('/analyze', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({symptoms})
            });
            
            const data = await response.json();
            loading.classList.remove('show');
            
            if (data.success) {
                let html = '';
                data.conditions.forEach(c => {
                    html += `
                        <div class="card">
                            <h3>${c.name}</h3>
                            <p><strong>Common Causes:</strong> ${c.causes.join(', ')}</p>
                            <p><strong>Advice:</strong> ${c.advice}</p>
                            <p><strong>⚠️ Warning Signs:</strong></p>
                            <ul>${c.warning_signs.map(s => `<li>${s}</li>`).join('')}</ul>
                        </div>
                    `;
                });
                html += '<div class="warning">⚠️ This is for information only. Consult a doctor.</div>';
                results.innerHTML = html;
            } else {
                results.innerHTML = '<div class="card"><p>No conditions matched. Please consult a pediatrician.</p></div>';
            }
            
            results.classList.add('show');
        });
        
        // Nutrition Plan
        document.getElementById('nutrition-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const loading = document.getElementById('nutrition-loading');
            const results = document.getElementById('nutrition-results');
            
            loading.classList.add('show');
            results.classList.remove('show');
            
            const age = document.getElementById('age-input').value;
            
            const response = await fetch('/nutrition', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({age})
            });
            
            const data = await response.json();
            loading.classList.remove('show');
            
            if (data.success) {
                const plan = data.plan;
                let html = `
                    <div class="card">
                        <h3>Nutrition Plan: ${plan.age}</h3>
                        <p><strong>Recommended Foods:</strong></p>
                        <ul>${plan.foods.map(f => `<li>${f}</li>`).join('')}</ul>
                        <p><strong>Foods to Avoid:</strong></p>
                        <ul>${plan.avoid.map(f => `<li>${f}</li>`).join('')}</ul>
                        <p><strong>Tips:</strong></p>
                        <ul>${plan.tips.map(t => `<li>${t}</li>`).join('')}</ul>
                    </div>
                    <div class="warning">⚠️ Consult a pediatrician for personalized advice.</div>
                `;
                results.innerHTML = html;
            }
            
            results.classList.add('show');
        });
    </script>
</body>
</html>
"""

def find_conditions(symptoms):
    symptoms_lower = symptoms.lower()
    results = []
    
    for key, condition in PEDIATRIC_CONDITIONS.items():
        for keyword in condition["keywords"]:
            if keyword in symptoms_lower:
                results.append(condition)
                break
    
    return results

def get_nutrition(age_months):
    age = int(age_months)
    if age < 6:
        return NUTRITION_PLANS["0-6"]
    elif age < 12:
        return NUTRITION_PLANS["6-12"]
    else:
        return NUTRITION_PLANS["12-36"]

@app.route('/')
def home():
    return HTML_TEMPLATE

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    symptoms = data.get('symptoms', '')
    conditions = find_conditions(symptoms)
    
    if conditions:
        return jsonify({"success": True, "conditions": conditions})
    else:
        return jsonify({"success": False, "message": "No conditions matched"})

@app.route('/nutrition', methods=['POST'])
def nutrition():
    data = request.json
    age = data.get('age', 0)
    plan = get_nutrition(age)
    return jsonify({"success": True, "plan": plan})

if __name__ == '__main__':
    print("🏥 Starting Pediatric Health Advisor...")
    print("📱 Open: http://localhost:5001")
    app.run(debug=True, port=5001)
