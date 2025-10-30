"""
Streamlit Dashboard for ASI Chain Agent Simulation.

This interactive web application visualizes a multi-agent system where:
- Agents operate in a shared hypergraph memory space (MeTTa)
- Actions dynamically update agent reputations
- Real-time graph visualization shows the agent network
- Cognitive rules defined in MeTTa govern agent behavior

Run with: streamlit run app.py
"""

import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import time
try:
    from agent_sim import AgentSimulation
except ImportError:
    # Fallback to simplified version if hyperon is not installed
    from agent_sim_simple import AgentSimulation
from visualizer import (
    create_agent_graph, 
    render_pyvis_graph, 
    create_reputation_legend,
    get_network_statistics
)


# Page configuration
st.set_page_config(
    page_title="ASI Chain Agent Simulation",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1E88E5;
    }
    .status-running {
        color: #27AE60;
        font-weight: bold;
    }
    .status-stopped {
        color: #E74C3C;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if 'simulation' not in st.session_state:
        st.session_state.simulation = None
    if 'is_running' not in st.session_state:
        st.session_state.is_running = False
    if 'stop_flag' not in st.session_state:
        st.session_state.stop_flag = False
    if 'history' not in st.session_state:
        st.session_state.history = []
    if 'health_score_history' not in st.session_state:
        st.session_state.health_score_history = []
    if 'start_simulation' not in st.session_state:
        st.session_state.start_simulation = False
    if 'sim_params' not in st.session_state:
        st.session_state.sim_params = {}


def render_sidebar():
    """Render the sidebar with simulation controls."""
    st.sidebar.title("🎮 Simulation Controls")
    
    st.sidebar.markdown("---")
    
    # Simulation parameters
    num_agents = st.sidebar.slider(
        "Number of Agents",
        min_value=3,
        max_value=20,
        value=5,
        step=1,
        help="Number of agents in the simulation"
    )
    
    num_steps = st.sidebar.slider(
        "Simulation Steps",
        min_value=10,
        max_value=100,
        value=20,
        step=5,
        help="Number of steps to run"
    )
    
    step_delay = st.sidebar.slider(
        "Step Delay (seconds)",
        min_value=0.1,
        max_value=2.0,
        value=0.5,
        step=0.1,
        help="Delay between simulation steps"
    )
    
    st.sidebar.markdown("---")
    
    # Control buttons
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        if st.sidebar.button("▶️ Run", use_container_width=True, 
                            disabled=st.session_state.is_running):
            st.session_state.stop_flag = False
            st.session_state.start_simulation = True
            st.session_state.sim_params = {
                'num_agents': num_agents,
                'num_steps': num_steps,
                'step_delay': step_delay
            }
    
    with col2:
        if st.sidebar.button("⏹️ Stop", use_container_width=True,
                            disabled=not st.session_state.is_running):
            st.session_state.stop_flag = True
    
    if st.sidebar.button("🔄 Reset", use_container_width=True):
        reset_simulation()
        st.rerun()
    
    return num_agents, num_steps, step_delay


def reset_simulation():
    """Reset the simulation to initial state."""
    st.session_state.simulation = None
    st.session_state.is_running = False
    st.session_state.stop_flag = False
    st.session_state.history = []
    st.session_state.health_score_history = []


def run_simulation(num_agents: int, num_steps: int, step_delay: float):
    """
    Run the simulation for a specified number of steps.
    
    Args:
        num_agents: Number of agents to simulate
        num_steps: Number of simulation steps
        step_delay: Delay between steps in seconds
    """
    # Initialize or reset simulation
    if st.session_state.simulation is None:
        st.session_state.simulation = AgentSimulation(num_agents=num_agents)
    else:
        st.session_state.simulation.reset(num_agents=num_agents)
    
    st.session_state.is_running = True
    st.session_state.history = []
    st.session_state.health_score_history = []
    
    # Create placeholders for dynamic updates
    status_placeholder = st.empty()
    graph_placeholder = st.empty()
    metrics_placeholder = st.empty()
    table_placeholder = st.empty()
    
    # Run simulation steps
    for step in range(num_steps):
        # Check if user pressed stop
        if st.session_state.stop_flag:
            st.session_state.is_running = False
            status_placeholder.warning("⏹️ Simulation stopped by user")
            break
        
        # Execute one simulation step
        step_info = st.session_state.simulation.step()
        st.session_state.history.append(step_info)
        st.session_state.health_score_history.append(step_info['health_score'])
        
        # Update status
        with status_placeholder.container():
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.markdown(f"**Step {step + 1}/{num_steps}** - "
                          f"<span class='status-running'>Running...</span>", 
                          unsafe_allow_html=True)
            with col2:
                st.write(f"**Action:** {step_info['action']}")
            with col3:
                st.write(f"**Agent:** {step_info['agent']}")
        
        # Get current agent states
        agent_states = st.session_state.simulation.get_agent_states()
        health_score = st.session_state.simulation.get_health_score()
        rep_dist = st.session_state.simulation.get_reputation_distribution()
        
        # Update graph visualization (main focus)
        with graph_placeholder.container():
            st.subheader("🕸️ Agent Network Visualization")
            
            nx_graph = create_agent_graph(agent_states)
            pyvis_html = render_pyvis_graph(nx_graph, height="600px")
            
            components.html(pyvis_html, height=620, scrolling=False)
        
        # Update metrics below graph
        with metrics_placeholder.container():
            st.subheader("📊 Simulation Metrics")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    label="🏥 Health Score",
                    value=f"{health_score:.1f}",
                    delta=f"{step_info['reputation_change']:.1f}"
                )
            
            with col2:
                st.metric(
                    label="🟢 High Rep Agents",
                    value=rep_dist['high']
                )
            
            with col3:
                st.metric(
                    label="🟡 Medium Rep Agents",
                    value=rep_dist['medium']
                )
            
            with col4:
                st.metric(
                    label="🔴 Low Rep Agents",
                    value=rep_dist['low']
                )
        
        # Update agent reputation table and chart side by side
        with table_placeholder.container():
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📋 Agent Rankings")
                # Create DataFrame
                df = pd.DataFrame([
                    {
                        'Agent': name,
                        'Reputation': f"{rep:.2f}",
                        'Status': get_status_emoji(rep)
                    }
                    for name, rep in sorted(agent_states.items(), 
                                           key=lambda x: x[1], 
                                           reverse=True)
                ])
                st.dataframe(df, use_container_width=True, hide_index=True)
            
            with col2:
                if len(st.session_state.health_score_history) > 1:
                    st.subheader("📈 Health Score Trend")
                    chart_data = pd.DataFrame({
                        'Step': range(1, len(st.session_state.health_score_history) + 1),
                        'Health Score': st.session_state.health_score_history
                    })
                    st.line_chart(chart_data.set_index('Step'), use_container_width=True)
        
        # Remove the separate chart placeholder since it's now combined with table
        
        # Delay before next step
        time.sleep(step_delay)
    
    # Simulation completed
    st.session_state.is_running = False
    
    if not st.session_state.stop_flag:
        status_placeholder.success(f"✅ Simulation completed! Ran {num_steps} steps.")


def get_status_emoji(reputation: float) -> str:
    """Get status emoji based on reputation level."""
    if reputation >= 150:
        return "🟢 Excellent"
    elif reputation >= 100:
        return "🟡 Good"
    elif reputation >= 50:
        return "🟠 Average"
    else:
        return "🔴 Low"


def render_main_content():
    """Render the main content area when simulation is not running."""
    st.markdown("<div class='main-header'>🧠 ASI Chain Agent Simulation</div>", 
                unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>Multi-Agent System with MeTTa Cognitive Logic</div>", 
                unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Simple welcome message
    st.info("👈 Configure parameters in the sidebar and click **▶️ Run** to start the simulation!")
    
    st.markdown("""
    ### 🎯 About This Simulation
    
    This dashboard simulates an **ASI Chain agent network** where:
    - 🧠 Agents use **MeTTa symbolic reasoning**
    - 🤝 Actions (contribute, share, trade, idle) affect **reputation**
    - 📊 The **health score** tracks overall system performance
    - 🌐 A **dynamic network graph** visualizes agent relationships
    """)
    
    st.markdown("---")
    
    # MeTTa symbolic language representation
    st.markdown("### 🔬 MeTTa Symbolic Rules")
    st.markdown("""
    Agent actions are defined using **MeTTa** (Meta Type Talk), a symbolic language for AGI.
    Here's how each action is represented:
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🤝 Contribute Action**")
        st.code("""
; Contribute: Major reputation boost
(= (action-contribute $agent)
   (update-reputation $agent 15))
        """, language="lisp")
        st.caption("Increases agent reputation by +15 points")
        
        st.markdown("**📤 Share Action**")
        st.code("""
; Share: Moderate reputation boost
(= (action-share $agent)
   (update-reputation $agent 8))
        """, language="lisp")
        st.caption("Increases agent reputation by +8 points")
    
    with col2:
        st.markdown("**💱 Trade Action**")
        st.code("""
; Trade: Positive-sum transfer
(= (action-trade $from $to $amount)
   (transfer-reputation $from $to $amount))
   
; Receiver gets 1.1x bonus
; Sender: -X, Receiver: +1.1X
        """, language="lisp")
        st.caption("Transfers reputation with 10% bonus")
        
        st.markdown("**😴 Idle Action**")
        st.code("""
; Idle: Slight reputation penalty
(= (action-idle $agent)
   (update-reputation $agent -2))
        """, language="lisp")
        st.caption("Decreases agent reputation by -2 points")
    
    st.markdown("---")
    
    st.markdown("""
    ### 📊 How It Works
    
    1. **Symbolic Rules**: Actions are defined as symbolic patterns in MeTTa
    2. **Grounded Functions**: Python functions (like `update-reputation`) bridge MeTTa and simulation
    3. **Pattern Matching**: When an agent acts, MeTTa matches the pattern and executes the rule
    4. **State Updates**: Reputation changes are applied to the shared hypergraph space
    
    **Color Coding:**
    - 🟢 Green: High reputation (150-200)
    - 🟡 Yellow: Good reputation (100-150)
    - 🟠 Orange: Medium reputation (50-100)
    - 🔴 Red: Low reputation (0-50)
    """)


def main():
    """Main application entry point."""
    initialize_session_state()
    
    # Render sidebar and get parameters
    num_agents, num_steps, step_delay = render_sidebar()
    
    # Check if simulation should start (triggered from sidebar)
    if st.session_state.start_simulation:
        st.session_state.start_simulation = False
        params = st.session_state.sim_params
        run_simulation(params['num_agents'], params['num_steps'], params['step_delay'])
    
    # Render main content
    if not st.session_state.is_running and not st.session_state.history:
        render_main_content()
    elif st.session_state.history and not st.session_state.is_running:
        # Show results after simulation completes
        st.markdown("<div class='main-header'>📊 Simulation Complete</div>", 
                    unsafe_allow_html=True)
        
        # Final metrics
        if st.session_state.simulation:
            agent_states = st.session_state.simulation.get_agent_states()
            health_score = st.session_state.simulation.get_health_score()
            rep_dist = st.session_state.simulation.get_reputation_distribution()
            
            # Graph visualization (main focus)
            st.subheader("🕸️ Final Agent Network")
            nx_graph = create_agent_graph(agent_states)
            pyvis_html = render_pyvis_graph(nx_graph, height="600px")
            components.html(pyvis_html, height=620, scrolling=False)
            
            st.markdown("---")
            
            # Metrics below graph
            st.subheader("📊 Final Metrics")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    label="🏥 Final Health Score",
                    value=f"{health_score:.1f}"
                )
            
            with col2:
                st.metric(
                    label="🟢 High Rep Agents",
                    value=rep_dist['high']
                )
            
            with col3:
                st.metric(
                    label="🟡 Medium Rep Agents",
                    value=rep_dist['medium']
                )
            
            with col4:
                st.metric(
                    label="🔴 Low Rep Agents",
                    value=rep_dist['low']
                )
            
            st.markdown("---")
            
            # Table and chart side by side
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📋 Final Rankings")
                df = pd.DataFrame([
                    {
                        'Rank': idx + 1,
                        'Agent': name,
                        'Reputation': f"{rep:.2f}",
                        'Status': get_status_emoji(rep)
                    }
                    for idx, (name, rep) in enumerate(sorted(agent_states.items(), 
                                                             key=lambda x: x[1], 
                                                             reverse=True))
                ])
                st.dataframe(df, use_container_width=True, hide_index=True)
            
            with col2:
                st.subheader("📈 Health Score Evolution")
                chart_data = pd.DataFrame({
                    'Step': range(1, len(st.session_state.health_score_history) + 1),
                    'Health Score': st.session_state.health_score_history
                })
                st.line_chart(chart_data.set_index('Step'), use_container_width=True)
            
            # Action history
            with st.expander("📜 View Complete Action History"):
                history_df = pd.DataFrame(st.session_state.history)
                st.dataframe(history_df, use_container_width=True)


if __name__ == "__main__":
    main()


