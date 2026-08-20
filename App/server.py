from flask import Flask, render_template, jsonify
import random
import numpy as np
import joblib
import os

app = Flask(__name__)

# --- 1. LOAD THE AI MODEL & SCALER ---
# This ensures the model loads only once when the server starts
model_path = os.path.join('src', 'best_crowd_model.pkl')
scaler_path = os.path.join('src', 'scaler.pkl')

try:
    ai_model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    print("✅ AI Model and Scaler loaded successfully!")
except Exception as e:
    print(f"⚠️ Error loading model: {e}")
    print("Please ensure 'best_crowd_model.pkl' and 'scaler.pkl' are inside the 'src' folder.")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/live-data')
def live_data():
    zones = ['Gate 1 (North)', 'Gate 2 (South)', 'Food Court', 'Stage Area A', 'Exit C']
    zone_data = []
    total_crowd = 0
    
    # We will store the features here to predict all zones at once
    features_list = []
    
    for zone in zones:
        density = random.randint(50, 800)  # Simulated live head count
        speed = round(random.uniform(0.1, 2.5), 2)  # Simulated live speed
        total_crowd += density
        
        features_list.append([density, speed])
        zone_data.append({'zone': zone, 'density': density, 'speed': speed})
        
    # --- 2. AI PREDICTION LOGIC ---
    # Scale the features just like we did during training
    features_scaled = scaler.transform(features_list)
    
    # Predict the risk labels (0: Normal, 1: Warning, 2: Critical)
    predictions = ai_model.predict(features_scaled)
    
    # Map predictions back to the dashboard status
    for i, pred in enumerate(predictions):
        if pred == 2:
            zone_data[i]['status'] = 'CRITICAL'
        elif pred == 1:
            zone_data[i]['status'] = 'WARNING'
        else:
            zone_data[i]['status'] = 'NORMAL'

    # --- 3. OVERALL DASHBOARD METRICS ---
    avg_speed = round(np.mean([z['speed'] for z in zone_data]), 2)
    overall_status = "NORMAL"
    action = "Crowd flow is smooth. No interventions needed."
    
    # Trigger actionable interventions based on AI predictions
    if any(z['status'] == 'CRITICAL' for z in zone_data):
        overall_status = "CRITICAL"
        action = "🚨 CRITICAL ALERT: Immediately close entry gates and open alternate emergency exits to redistribute the crowd[cite: 2]."
    elif any(z['status'] == 'WARNING' for z in zone_data):
        overall_status = "WARNING"
        action = "⚠️ WARNING: Monitor crowd flow closely. Consider deploying additional security staff[cite: 2]."

    return jsonify({
        "crowd": f"{total_crowd:,}",
        "speed": f"{avg_speed} m/s",
        "status": overall_status,
        "action": action,
        "zone_data": zone_data
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)