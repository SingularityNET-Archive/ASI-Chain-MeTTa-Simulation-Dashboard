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
    if 'graph_update_interval' not in st.session_state:
        st.session_state.graph_update_interval = 3  # Update graph every N steps
    if 'agent_states_history' not in st.session_state:
        st.session_state.agent_states_history = []  # Store full agent states at each step
    if 'current_view_step' not in st.session_state:
        st.session_state.current_view_step = 0  # Which step we're viewing


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
    
    graph_update_freq = st.sidebar.slider(
        "Graph Update Frequency",
        min_value=1,
        max_value=10,
        value=3,
        step=1,
        help="Update graph every N steps (higher = smoother)"
    )
    st.session_state.graph_update_interval = graph_update_freq
    
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
    st.session_state.agent_states_history = []
    st.session_state.current_view_step = 0


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
    st.session_state.agent_states_history = []
    st.session_state.current_view_step = 0
    
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
        
        # Store full agent states for replay
        agent_states = st.session_state.simulation.get_agent_states()
        st.session_state.agent_states_history.append(agent_states.copy())
        st.session_state.current_view_step = step + 1  # Update to latest step
        
        # Update status
        with status_placeholder.container():
            # Action indicator bar
            action_emoji = {
                'contribute': '🤝',
                'share': '📤',
                'trade': '💱',
                'idle': '😴'
            }
            emoji = action_emoji.get(step_info['action'], '⚡')
            
            col1, col2 = st.columns([1, 3])
            with col1:
                st.markdown(f"**Step {step + 1}/{num_steps}**")
            with col2:
                action_display = f"{emoji} **{step_info['agent']}** performed **{step_info['action'].upper()}** (Change: {step_info['reputation_change']:+.1f})"
                st.markdown(action_display)
        
        # Get current agent states
        agent_states = st.session_state.simulation.get_agent_states()
        health_score = st.session_state.simulation.get_health_score()
        rep_dist = st.session_state.simulation.get_reputation_distribution()
        
        # Update graph visualization (only every N steps to reduce flicker)
        update_interval = st.session_state.graph_update_interval
        if step % update_interval == 0 or step == num_steps - 1:
            with graph_placeholder.container():
                st.subheader("🕸️ Agent Network Visualization")
                
                # Display current action indicator
                action_emoji = {
                    'contribute': '🤝',
                    'share': '📤',
                    'trade': '💱',
                    'idle': '😴'
                }
                emoji = action_emoji.get(step_info['action'], '⚡')
                action_color = {
                    'contribute': '#27AE60',
                    'share': '#3498DB',
                    'trade': '#F39C12',
                    'idle': '#E74C3C'
                }
                color = action_color.get(step_info['action'], '#95A5A6')
                
                st.markdown(f"""
                <div style="background-color: {color}; padding: 10px; border-radius: 5px; margin-bottom: 10px; text-align: center;">
                    <span style="font-size: 1.2em; color: white; font-weight: bold;">
                        {emoji} {step_info['agent']} performed <u>{step_info['action'].upper()}</u> 
                        (Rep: {step_info['old_reputation']:.1f} → {step_info['new_reputation']:.1f}, 
                        Change: {step_info['reputation_change']:+.1f})
                    </span>
                </div>
                """, unsafe_allow_html=True)
                
                nx_graph = create_agent_graph(agent_states)
                # Use faster rendering during simulation (less stabilization)
                pyvis_html = render_pyvis_graph(nx_graph, height="600px", stabilize=False)
                
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
    """)
    
    st.markdown("---")
    
    # Graph visualization explanation
    st.markdown("### 🕸️ Understanding the Network Visualization")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Nodes (Circles):**
        - Each node = one agent
        - **Size**: Larger = higher reputation
        - **Color**: Indicates reputation level
          - 🟢 Green: High (150-200)
          - 🟡 Yellow: Good (100-150)
          - 🟠 Orange: Medium (50-100)
          - 🔴 Red: Low (0-50)
        """)
    
    with col2:
        st.markdown("""
        **Edges (Lines):**
        - Connect agents with **similar reputations**
        - Each agent links to 2-3 nearest reputation peers
        - Creates **visual clustering** by reputation tier
        - **Not** direct interactions or trades
        - Shows reputation-based social structure
        """)
    
    st.info("💡 **Tip**: Watch how agents migrate between clusters as their reputation changes through actions!")
    
    st.markdown("---")
    
    st.markdown("""
    **Graph Dynamics:**
    - High-rep agents naturally cluster in the center
    - Similar-reputation agents form cohesive groups
    - Edge thickness reflects combined reputation strength
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
        # Show results after simulation completes with step navigation
        st.markdown("<div class='main-header'>📊 Simulation Complete - Replay Mode</div>", 
                    unsafe_allow_html=True)
        
        # Step navigation controls
        if st.session_state.agent_states_history:
            st.markdown("### ⏪ Navigate Through Simulation ⏩")
            
            col1, col2, col3 = st.columns([1, 6, 1])
            
            with col1:
                if st.button("⏮️ First", use_container_width=True):
                    st.session_state.current_view_step = 0
                    st.rerun()
            
            with col2:
                # Slider to jump to any step
                total_steps = len(st.session_state.agent_states_history)
                view_step = st.slider(
                    "Step",
                    min_value=0,
                    max_value=total_steps - 1,
                    value=st.session_state.current_view_step,
                    step=1,
                    format="Step %d",
                    key="step_slider"
                )
                st.session_state.current_view_step = view_step
            
            with col3:
                if st.button("⏭️ Last", use_container_width=True):
                    st.session_state.current_view_step = len(st.session_state.agent_states_history) - 1
                    st.rerun()
            
            # Navigation buttons
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                if st.button("⏪ Previous", use_container_width=True, 
                            disabled=st.session_state.current_view_step == 0):
                    st.session_state.current_view_step = max(0, st.session_state.current_view_step - 1)
                    st.rerun()
            
            with col4:
                if st.button("Next ⏩", use_container_width=True,
                            disabled=st.session_state.current_view_step >= len(st.session_state.agent_states_history) - 1):
                    st.session_state.current_view_step = min(
                        len(st.session_state.agent_states_history) - 1,
                        st.session_state.current_view_step + 1
                    )
                    st.rerun()
            
            st.markdown("---")
            
            # Get the agent states for the selected step
            agent_states = st.session_state.agent_states_history[st.session_state.current_view_step]
            step_info = st.session_state.history[st.session_state.current_view_step]
            
            # Show action that occurred at this step
            action_emoji = {
                'contribute': '🤝',
                'share': '📤',
                'trade': '💱',
                'idle': '😴'
            }
            emoji = action_emoji.get(step_info['action'], '⚡')
            action_color = {
                'contribute': '#27AE60',
                'share': '#3498DB',
                'trade': '#F39C12',
                'idle': '#E74C3C'
            }
            color = action_color.get(step_info['action'], '#95A5A6')
            
            st.markdown(f"""
            <div style="background-color: {color}; padding: 15px; border-radius: 5px; margin-bottom: 15px; text-align: center;">
                <span style="font-size: 1.3em; color: white; font-weight: bold;">
                    Step {st.session_state.current_view_step + 1}: {emoji} {step_info['agent']} performed <u>{step_info['action'].upper()}</u>
                    <br>
                    <span style="font-size: 0.9em;">
                    Reputation: {step_info['old_reputation']:.1f} → {step_info['new_reputation']:.1f} 
                    (Change: {step_info['reputation_change']:+.1f})
                    </span>
                </span>
            </div>
            """, unsafe_allow_html=True)
            
            # Calculate metrics for this step
            health_score = sum(agent_states.values()) / len(agent_states) if agent_states else 0
            rep_dist = {'high': 0, 'medium': 0, 'low': 0}
            for reputation in agent_states.values():
                if reputation >= 100:
                    rep_dist['high'] += 1
                elif reputation >= 50:
                    rep_dist['medium'] += 1
                else:
                    rep_dist['low'] += 1
            
            # Graph visualization (main focus)
            st.subheader("🕸️ Agent Network at This Step")
            nx_graph = create_agent_graph(agent_states)
            # Use full stabilization for replay (better layout)
            pyvis_html = render_pyvis_graph(nx_graph, height="600px", stabilize=True)
            components.html(pyvis_html, height=620, scrolling=False)
            
            st.markdown("---")
            
            # Metrics below graph
            st.subheader(f"📊 Metrics at Step {st.session_state.current_view_step + 1}")
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


