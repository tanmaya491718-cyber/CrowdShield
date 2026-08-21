# 🛡️ CrowdShield: AI-Powered Early Warning System

CrowdShield is a real-time, AI-driven predictive system designed to prevent crowd crush and stampede incidents at large-scale venues. It analyzes crowd density and flow speed to provide actionable interventions before critical bottlenecks occur.

## 🚀 Key Features
* **Live AI Predictions:** Utilizes a custom-trained Random Forest Classifier to assess threat levels (Normal, Warning, Critical).
* **Command Dashboard:** Built with Flask and Chart.js for real-time KPI monitoring.
* **Digital Twin Venue Map:** Spatially tracks crowd density across different venue sectors with dynamic visual alerting.
* **Analytics Hub:** Visualizes historical crowd trends and risk distributions.

## 💻 Tech Stack
* **Backend:** Python, Flask
* **Machine Learning:** Scikit-Learn, Pandas, NumPy
* **Frontend:** HTML5, CSS3, JavaScript (Fetch API, Chart.js)

## ⚙️ How to Run Locally
1. Clone the repository: `git clone https://github.com/tanmaya491718-cyber/CrowdShield`
2. Install dependencies: `pip install flask scikit-learn pandas numpy`
3. Run the backend server: `python App/server.py`
4. Open your browser and navigate to `http://127.0.0.1:5000`

## 📁 Project Structure
* `/App` - Contains the Flask backend and HTML/JS frontend templates.
* `/SRC` - Stores the trained ML models and scalers.
* `/Notebooks` - Includes data generation, EDA, and model training scripts.
* `/Deliverables` - Contains the architecture diagram, pitch deck, and demo video.