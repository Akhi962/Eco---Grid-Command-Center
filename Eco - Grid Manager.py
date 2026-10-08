# =====================================================================
# ⚙️ STEP 2: MAIN DASHBOARD VIEW (RUNS ONLY AFTER ACCESS IS GRANTED)
# =====================================================================
else:
    # MOVE THIS TO THE TOP: Load the grid dictionary into memory immediately!
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

    # Now define your helper loop function safely
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

    # Keep the rest of your Step 3 titles, metric banner, sidebar, and layout blocks exactly the same below...