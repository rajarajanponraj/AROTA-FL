import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import torch
import os

# Import the core simulation functions from your existing experiments script
from experiments.run_fl_sweeps import run_fl_simulation_seed, load_mnist_full

st.set_page_config(page_title="AROTA-FL Simulator", layout="wide")

st.title("Convergence-Aware Active RIS for AirComp-Based FL")
st.markdown("### Interactive Network and Training Simulator")

# Cache the dataset loading so it doesn't reload every time you click a button
@st.cache_data
def get_data():
    return load_mnist_full()

train_data, test_data = get_data()

# --- SIDEBAR CONTROLS ---
st.sidebar.header("Network Parameters")
num_clients = st.sidebar.slider("Number of Clients", 5, 50, 10)
num_rounds = st.sidebar.slider("Communication Rounds", 5, 100, 20)

st.sidebar.header("Optimization Schemes")
run_iid = st.sidebar.checkbox("Baseline: Ideal Channel (IID Data)", True)
run_mse = st.sidebar.checkbox("Baseline: Active RIS (MSE-Minimization)", True)
run_conv = st.sidebar.checkbox("Proposed: Active RIS (Convergence-Aware)", True)

# --- 1. NETWORK TOPOLOGY VISUALIZATION ---
st.header("1. Network Topology (Physical Layout)")
st.markdown("This map shows the spatial distribution of the wireless network components. The Edge Devices transmit their models over-the-air, which are reflected and amplified by the Active RIS towards the Server.")

# Generate coordinates based on the distances in the project
fig_net, ax_net = plt.subplots(figsize=(10, 4))
ax_net.scatter([0], [0], c='red', s=300, marker='^', label='Access Point (Global Server)')
ax_net.scatter([80], [0], c='green', s=300, marker='s', label='Active RIS')

# Distribute users around the RIS and AP
np.random.seed(42)
user_x = 80 + np.random.uniform(-40, 10, num_clients)
user_y = np.random.uniform(-40, 40, num_clients)
ax_net.scatter(user_x, user_y, c='blue', s=80, label='Edge Devices (FL Clients)')

ax_net.legend(loc='lower left')
ax_net.set_title("Simulated Wireless Network Layout (Top-Down View)")
ax_net.set_xlabel("Distance (meters)")
ax_net.set_ylabel("Distance (meters)")
ax_net.grid(True, linestyle='--', alpha=0.6)
st.pyplot(fig_net)

# --- 2. FEDERATED LEARNING SIMULATION ---
st.header("2. Federated Learning Convergence Simulation")

if st.button("Start Live Simulation 🚀", type="primary"):
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    results = {}
    total_tasks = sum([run_iid, run_mse, run_conv])
    current_task = 0
    
    if run_iid:
        status_text.info("Simulating Ideal Channel baseline (Training...)")
        acc = run_fl_simulation_seed(train_data, test_data, num_clients, num_rounds, "ideal", True, seed=42)
        results["Ideal Channel (Theoretical Max)"] = acc
        current_task += 1
        progress_bar.progress(int((current_task / total_tasks) * 100))
        
    if run_mse:
        status_text.info("Simulating Active RIS with MSE-Minimization (Training...)")
        acc = run_fl_simulation_seed(train_data, test_data, num_clients, num_rounds, "mse_min", False, seed=42)
        results["Active RIS: MSE-Min"] = acc
        current_task += 1
        progress_bar.progress(int((current_task / total_tasks) * 100))
        
    if run_conv:
        status_text.info("Simulating Active RIS with Proposed Convergence-Aware (Training...)")
        acc = run_fl_simulation_seed(train_data, test_data, num_clients, num_rounds, "conv_aware", False, seed=42)
        results["Active RIS: Proposed Conv-Aware"] = acc
        current_task += 1
        progress_bar.progress(int((current_task / total_tasks) * 100))
        
    status_text.success("Simulation Complete! Check the convergence graph below.")
    
    # Plotting the Results
    st.subheader("Model Accuracy over Time")
    fig_acc, ax_acc = plt.subplots(figsize=(10, 5))
    rounds_range = range(num_rounds + 1)
    
    colors = {"Ideal Channel (Theoretical Max)": "blue", "Active RIS: MSE-Min": "red", "Active RIS: Proposed Conv-Aware": "green"}
    styles = {"Ideal Channel (Theoretical Max)": "--", "Active RIS: MSE-Min": "-", "Active RIS: Proposed Conv-Aware": "-"}
    
    for label, acc_hist in results.items():
        ax_acc.plot(rounds_range, acc_hist, color=colors.get(label, 'black'), 
                    linestyle=styles.get(label, '-'), label=label, linewidth=2.5)
        
    ax_acc.set_xlabel("Communication Round")
    ax_acc.set_ylabel("Test Accuracy (MNIST)")
    ax_acc.legend()
    ax_acc.grid(True)
    
    st.pyplot(fig_acc)
