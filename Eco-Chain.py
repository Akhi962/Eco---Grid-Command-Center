import streamlit as st
import time
import pandas as pd

# =====================================================================
# ⚙️ 1. MASTER LIFECYCLE & ENGINE CONFIGURATION (ALWAY AT THE TOP)
# =====================================================================
st.set_page_config(layout="wide", page_title="EcoGrid Commander", page_icon="⚡")

# Initialize global login state session conditions
if "access_granted" not in st.session_state:
    st.session_state.access_granted = False

# Initialize data layout in memory dictionary map globally
if "grid" not in st.session_state:
    st.session_state.grid = {
        "head": "Solar Array Alpha",
        "sectors": {
            "Solar Array Alpha": {"generation_kw": 600, "demand_kw": 0, "status": "🟢 Healthy", "next": "Substation Block 1"},
            "Substation Block 1": {"generation_kw": 0, "demand_kw": 350, "status": "🟢 Healthy", "next": "Substation Block 2"},
            "Substation Block 2": {"generation_kw": 150, "demand_kw": 250, "status": "🟢 Healthy", "next": "Emergency Battery Storage"},
            "Emergency Battery Storage": {"generation_kw": 0, "demand_kw": 0, "capacity_kw": 1000, "status": "🟢 Healthy", "next": None}
        }
    }

# Sequential Logic Routing Engine Loop
def balance_grid_traffic():
    grid_data = st.session_state.grid
    sectors = grid_data["sectors"]
    current_key = grid_data["head"]
    net_reserve = 0
    reports = []
    
    for k, v in sectors.items():
        if v["status"] != "⚡ TRIPPED":
            v["status"] = "🟢 Healthy"

    while current_key is not None:
        node = sectors[current_key]
        
        if node["status"] == "⚡ TRIPPED":
            reports.append({"node": current_key, "msg": "💥 FLOW BROKEN - Breaker Tripped!", "type": "error"})
            while current_key is not None:
                sectors[current_key]["status"] = "🔴 Offline"
                current_key = sectors[current_key]["next"]
            return reports

        local_generation = node.get("generation_kw", 0)
        local_demand = node.get("demand_kw", 0)
        net_reserve += (local_generation - local_demand)
        
        if net_reserve < 0:
            if "capacity_kw" in node:
                node["status"] = "🔋 Using Battery Backup"
                reports.append({"node": current_key, "msg": f"Deficit covered by batteries: {-net_reserve} kW", "type": "warning"})
                net_reserve = 0  
            else:
                node["status"] = "❌ OVERLOADED"
                reports.append({"node": current_key, "msg": f"Critical Shortfall of {-net_reserve} kW.", "type": "error"})
        else:
            reports.append({"node": current_key, "msg": f"Grid Balanced. Surplus: +{net_reserve} kW", "type": "success"})
            
        current_key = node["next"]
    return reports


# =====================================================================
# 🏛️ 2. GATEWAY INTERFACE LAYOUT (RUNS ONLY IF NOT LOGGED IN)
# =====================================================================
if not st.session_state.access_granted:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; font-style: italic; color: #90A4AE; letter-spacing: 2px;'>\"Imperium Sine Fine\"</h2>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: #00E676; font-size: 3rem; font-weight: 800; text-shadow: 0px 0px 15px rgba(0, 230, 118, 0.3);'>⚡ ECOGRID COMMAND CENTER</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; font-size: 1.2rem; color: #CFD8DC;'>Welcome To Our App</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1rem; color: #CFD8DC;'>Tap the rotating globe to engage grid sequences.</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 🌍 Vector Blue & Green Rotating Globe Assembly 
    st.markdown(
        """
        <div class="universe-container">
            <div class="globe-assembly">
                <div class="globe-arm"></div>
                <div class="spinning-sphere">
                    <div class="map-track">
                        <svg class="continental-drift" viewBox="0 0 400 200">
                            <path fill="#2E7D32" d="M20,40 Q40,20 60,30 T100,20 T140,50 T120,90 T70,80 Z M180,60 Q220,30 260,50 T300,80 T280,120 T220,100 Z M50,120 Q90,140 110,170 T60,180 Z"/>
                            <path fill="#4CAF50" d="M80,50 Q100,30 120,60 T90,90 Z M220,80 Q240,60 270,90 T210,110 Z"/>
                        </svg>
                        <svg class="continental-drift" viewBox="0 0 400 200">
                            <path fill="#2E7D32" d="M20,40 Q40,20 60,30 T100,20 T140,50 T120,90 T70,80 Z M180,60 Q220,30 260,50 T300,80 T280,120 T220,100 Z M50,120 Q90,140 110,170 T60,180 Z"/>
                            <path fill="#4CAF50" d="M80,50 Q100,30 120,60 T90,90 Z M220,80 Q240,60 270,90 T210,110 Z"/>
                        </svg>
                    </div>
                </div>
                <div class="globe-base"></div>
            </div>
        </div>

        <style>
            .universe-container { display: flex; justify-content: center; align-items: center; height: 320px; margin-bottom: 20px; }
            .globe-assembly { position: relative; width: 260px; height: 320px; display: flex; flex-direction: column; align-items: center; }
            .spinning-sphere { position: absolute; top: 20px; width: 200px; height: 200px; border-radius: 50%; background: #1565C0; overflow: hidden; transform: rotate(23.5deg); box-shadow: inset -30px -30px 50px rgba(0,0,0,0.8), inset 10px 10px 25px rgba(255,255,255,0.2), 0 0 35px rgba(0, 230, 118, 0.4); z-index: 2; cursor: pointer; }
            .map-track { display: flex; width: 800px; height: 200px; animation: spinEarth 12s linear infinite; }
            .continental-drift { width: 400px; height: 200px; opacity: 0.95; }
            .globe-arm { position: absolute; top: 5px; width: 230px; height: 230px; border: 10px solid #cfd8dc; border-radius: 50%; border-left-color: transparent; border-bottom-color: transparent; transform: rotate(45deg); z-index: 1; filter: drop-shadow(0px 0px 8px rgba(255,255,255,0.1)); }
            .globe-base { position: absolute; bottom: 25px; width: 120px; height: 16px; background: linear-gradient(to right, #90a4ae, #cfd8dc, #78909c); border-radius: 8px 8px 4px 4px; box-shadow: 0px 5px 15px rgba(0,0,0,0.4); z-index: 1; }
            .globe-base::before { content: ''; position: absolute; top: -45px; left: 48px; width: 24px; height: 45px; background: #b0bec5; }
            @keyframes spinEarth { 0% { transform: translateX(0px); } 100% { transform: translateX(-400px); } }
            .spinning-sphere:hover { filter: brightness(1.08); box-shadow: inset -20px -20px 40px rgba(0,0,0,0.7), 0 0 50px #00E676; }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    _, col_btn, _ = st.columns(3)
    with col_btn:
        if st.button("🏛️ ENTER INDUSTRIAL SYSTEM", use_container_width=True, type="primary"):
            st.session_state.access_granted = True
            st.rerun()
            
    st.stop()


# =====================================================================
# 📊 3. THE COMMAND CENTER VISUALIZER VIEW (RUNS ONCE LOGGED IN)
# =====================================================================
st.markdown("<h1 style='text-align: center; color: #00E676;'>⚡ EcoGrid Command Center</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.1rem; color: #B0BEC5;'>Smart sequential power routing dashboard for sustainable micro-grids.</p>", unsafe_allow_html=True)
st.divider()

# Sidebar Setup
with st.sidebar:
    st.header("🛠️ Grid Configuration")
    st.subheader("➕ Deploy New Energy Sector")
    new_name = st.text_input("Sector Name", placeholder="e.g., Wind Farm Beta")
    new_gen = st.number_input("Power Generation (kW)", min_value=0, max_value=1000, value=0, step=50)
    new_dem = st.number_input("Power Demand (kW)", min_value=0, max_value=1000, value=0, step=50)
    
    if st.button("🔌 Connect to Grid Sequence", use_container_width=True):
        if new_name and new_name not in st.session_state.grid["sectors"]:
            sectors = st.session_state.grid["sectors"]
            tail = next(k for k, v in sectors.items() if v["next"] is None)
            sectors[tail]["next"] = new_name
            sectors[new_name] = {"generation_kw": new_gen, "demand_kw": new_dem, "status": "🟢 Healthy", "next": None}
            st.success(f"Linked '{new_name}' downstream!")
            time.sleep(0.5)
            st.rerun()

    st.divider()
    if st.button("🔒 Lock System Dashboard", type="secondary", use_container_width=True):
        st.session_state.access_granted = False
        st.rerun()

# Run Computations
sectors_dict = st.session_state.grid["sectors"]
ledger_reports = balance_grid_traffic()

# Executive Summary Metrics Card row
total_gen = sum(v.get("generation_kw", 0) for v in sectors_dict.values())
total_dem = sum(v.get("demand_kw", 0) for v in sectors_dict.values())
net_balance = total_gen - total_dem
net_efficiency = round((total_dem / total_gen) * 100, 1) if total_gen > 0 else 0

m_col1, m_col2, m_col3 = st.columns(3)
with m_col1:
    st.metric(label="🔌 Total Grid Generation", value=f"{total_gen} kW")
with m_col2:
    delta_color = "normal" if net_balance >= 0 else "inverse"
    st.metric(label="📉 Total Consumer Demand", value=f"{total_dem} kW", delta=f"{net_balance} kW Balance", delta_color=delta_color)
with m_col3:
    st.metric(label="📊 Grid Load Factor Efficiency", value=f"{net_efficiency}%")

st.divider()

# Draw Grid Color Layout blocks
cols = st.columns(len(sectors_dict))
current = st.session_state.grid["head"]
idx = 0

# =====================================================================
# FIXED BLOCK: VISUAL NETWORK MAP (NO MORE PY INDENTATION FLAWS)
# =====================================================================
st.subheader("🌐 Visual Network Flow Map")

# Generate the card layout items entirely into a single fluid HTML stream
html_cards = []
current = st.session_state.grid["head"]

while current is not None:
    node = sectors_dict[current]
    card_color = "#1B5E20" if "Healthy" in node["status"] else ("#E65100" if "Battery" in node["status"] else "#B71C1C")
    
    # Bundle the card look cleanly
    card_html = f"""
    <div style='background-color: {card_color}; padding: 12px; border-radius: 8px; min-width: 160px; max-width: 180px; text-align: center; box-shadow: 2px 2px 8px rgba(0,0,0,0.3); color: white; margin: 5px;'>
        <h5 style='margin: 0; font-size: 0.9rem;'>{current}</h5>
        <p style='margin: 4px 0; font-size: 0.75rem; opacity: 0.9;'>{node['status']}</p>
        <hr style='margin: 4px 0; border: 0; border-top: 1px solid rgba(255,255,255,0.2);'>
        <p style='margin: 0; font-size: 0.7rem;'>⚡ Gen: {node.get('generation_kw', 0)} kW</p>
        <p style='margin: 0; font-size: 0.7rem;'>📉 Dem: {node.get('demand_kw', 0)} kW</p>
    </div>
    """
    html_cards.append(card_html)
    current = node["next"]

# Render all generated list cards horizontally side-by-side cleanly
st.markdown(
    f"""
    <div style='display: flex; flex-direction: row; flex-wrap: wrap; justify-content: center; align-items: center; gap: 10px; width: 100%;'>
        {"".join(html_cards)}
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("<br>", unsafe_allow_html=True)

# Clean, unified emergency toggle setup down below the layout map
st.subheader("💥 Emergency System Relays")
t_cols = st.columns(len(sectors_dict))
current_t = st.session_state.grid["head"]
t_idx = 0

while current_t is not None:
    node_t = sectors_dict[current_t]
    if node_t["status"] != "🔴 Offline":
        with t_cols[t_idx]:
            if st.button(f"Trip {current_t.split()[-1]}", key=f"relay_{current_t}"):
                node_t["status"] = "⚡ TRIPPED"
                st.rerun()
    current_t = node_t["next"]
    t_idx += 1