import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.express as px

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="CrowdShield Dashboard", page_icon="🛡️", layout="wide")

# --- 2. CSS FOR CUSTOM STYLING (Optional but looks cool) ---
st.markdown("""
    <style>
    .big-font { font-size:24px !important; font-weight: bold; }
    .alert-text { color: red; font-weight: bold; font-size: 20px;}
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR CONTROLS ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100) # Dummy logo
st.sidebar.title("⚙️ Control Center")
st.sidebar.markdown("Manage crowd monitoring settings.")
sim_speed = st.sidebar.slider("Simulation Speed (seconds)", 1, 5, 2)
run_simulation = st.sidebar.checkbox("Start Live Monitoring 🔴")

# --- 4. MAIN DASHBOARD HEADER ---
st.title("🛡️ CrowdShield: Command Dashboard")
st.markdown("Predictive early warning system for crowd stampedes.")
st.divider()

# Placeholder elements that we will update in the loop
kpi_container = st.container()
chart_container = st.container()
alert_container = st.empty()

# --- 5. LOGIC FOR DUMMY LIVE DATA ---
def get_live_data():
    zones = ['Gate 1 (North)', 'Gate 2 (South)', 'Main Food Court', 'Stage Area A', 'Exit C']
    # Generating random but somewhat realistic data
    data = pd.DataFrame({
        'Zone': zones,
        'Density (Count)': np.random.randint(50, 600, size=len(zones)),
        'Speed (m/s)': np.random.uniform(0.1, 2.0, size=len(zones)),
    })
    
    # Bottleneck score calculation (Density / Speed)
    data['Bottleneck_Score'] = (data['Density (Count)'] / (data['Speed (m/s)'] + 0.1)).round(2)
    
    # Assign Status based on score
    conditions = [
        (data['Bottleneck_Score'] > 400) & (data['Density (Count)'] > 300),
        (data['Bottleneck_Score'] > 200)
    ]
    choices = ['CRITICAL (Crush Risk)', 'WARNING']
    data['Status'] = np.select(conditions, choices, default='NORMAL')
    
    return data

# --- 6. LIVE MONITORING LOOP ---
if run_simulation:
    while True:
        df = get_live_data()
        
        # Calculate overall metrics
        total_crowd = df['Density (Count)'].sum()
        max_bottleneck = df['Bottleneck_Score'].max()
        critical_zones = df[df['Status'] == 'CRITICAL (Crush Risk)']['Zone'].tolist()
        
        # Update KPIs
        with kpi_container:
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Venue Crowd", f"{total_crowd:,}")
            col2.metric("Max Bottleneck Score", f"{max_bottleneck}")
            
            if len(critical_zones) > 0:
                col3.metric("Venue Status", "🔴 HIGH RISK", delta="Stampede Alert", delta_color="inverse")
            else:
                col3.metric("Venue Status", "🟢 SAFE")
        
        # Update Charts and Tables
        with chart_container:
            col_chart, col_table = st.columns([2, 1])
            
            with col_chart:
                # Bar chart for crowd density
                fig = px.bar(df, x='Zone', y='Density (Count)', color='Status', 
                             color_discrete_map={'NORMAL': 'green', 'WARNING': 'orange', 'CRITICAL (Crush Risk)': 'red'},
                             title="Live Crowd Density by Zone")
                st.plotly_chart(fig, use_container_width=True)
            
            with col_table:
                st.markdown("### Live Zone Data")
                st.dataframe(df[['Zone', 'Density (Count)', 'Speed (m/s)', 'Status']], hide_index=True)

        # Update Alerts and Actionable Interventions
        if len(critical_zones) > 0:
            zones_str = ", ".join(critical_zones)
            alert_container.error(f"""
            🚨 **CRITICAL ALERT: High Stampede Risk Detected in {zones_str}!**
            
            **Actionable Interventions:**
            *   🚪 **Action 1:** Immediately close entry gates directing to {zones_str}.
            *   ➡️ **Action 2:** Open alternate emergency exits to redistribute the crowd.
            *   📢 **Action 3:** Trigger multilingual public announcements to reduce panic.
            *   👮 **Action 4:** Deploy additional security staff to the bottleneck area.
            """)
        elif 'WARNING' in df['Status'].values:
            alert_container.warning("⚠️ **Warning:** Crowd congestion increasing in some zones. Monitor closely.")
        else:
            alert_container.success("✅ Crowd flow is normal and within safe limits.")
        
        # Pause for the next update
        time.sleep(sim_speed)
        
        # Clear containers for the next loop to create a seamless live effect
        kpi_container.empty()
        chart_container.empty()
        
else:
    st.info("👈 Please check 'Start Live Monitoring' in the sidebar to run the system.")