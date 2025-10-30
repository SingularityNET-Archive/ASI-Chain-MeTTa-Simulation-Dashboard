# 🧠 ASI Chain Agent Simulation Dashboard

An interactive **Streamlit** web application that simulates an **Artificial Superintelligence (ASI) Chain** agent network using the **hyperon** (MeTTa) Python API for cognitive reasoning.

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/streamlit-1.28%2B-FF4B4B)
![MeTTa](https://img.shields.io/badge/hyperon-MeTTa-purple)
![License](https://img.shields.io/badge/license-MIT-green)

## 🎯 Overview

This dashboard visualizes a multi-agent system where autonomous agents:

- 🧠 **Think** using MeTTa symbolic reasoning
- 🤝 **Collaborate** in a shared hypergraph memory space  
- 📊 **Evolve** reputations based on their actions
- 🌐 **Form** a dynamic network of relationships

The simulation demonstrates how cognitive rules defined in MeTTa can govern agent behavior, reputation dynamics, and emergent network properties in a distributed AI system.

## ✨ Features

### Core Simulation
- **MeTTa Runtime**: Uses the `hyperon` package to create a shared hypergraph memory space
- **Agent Actions**: Contribute, share, trade, and idle actions with reputation consequences
- **Cognitive Rules**: Symbolic logic in MeTTa defines how actions affect reputation
- **Health Score**: System-level metric tracking average agent reputation

### Visualization
- **Interactive Graph**: Real-time NetworkX + PyVis visualization of agent network
- **Color-Coded Nodes**: Visual representation of reputation levels
- **Dynamic Updates**: Graph evolves as agents take actions
- **Network Statistics**: Metrics like density, average degree, and path length

### Streamlit Interface
- **Sidebar Controls**: Configure number of agents, simulation steps, and speed
- **Real-Time Metrics**: Live health score, reputation distribution, and status
- **Action History**: Complete log of all agent actions and reputation changes
- **Responsive Design**: Clean, modern UI with custom styling

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ASI-Chain-MeTTa-Simulation-Dashboard.git
   cd ASI-Chain-MeTTa-Simulation-Dashboard
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Open your browser**
   
   The app will automatically open at `http://localhost:8501`

## 📖 How to Use

### Basic Workflow

1. **Configure Parameters** in the sidebar:
   - Number of Agents (3-20)
   - Simulation Steps (10-100)
   - Step Delay (0.1-2.0 seconds)

2. **Click ▶️ Run** to start the simulation

3. **Watch the simulation** as:
   - Agents take actions (contribute, share, trade, idle)
   - Reputations change based on MeTTa rules
   - The network graph updates in real-time
   - Health score evolves

4. **Stop** the simulation anytime with the ⏹️ Stop button

5. **Reset** to start fresh with new parameters

### Understanding the Visualization

**Node Colors** indicate reputation levels:
- 🟢 **Green** (150-200): Excellent reputation
- 🟡 **Yellow** (100-150): Good reputation  
- 🟠 **Orange** (50-100): Average reputation
- 🔴 **Red** (0-50): Low reputation

**Node Size** is proportional to reputation value.

**Edges** connect agents with similar reputations, showing network clustering.

## 🔬 How It Works

### Architecture

The project is organized into three main modules:

```
ASI-Chain-MeTTa-Simulation-Dashboard/
├── app.py              # Streamlit UI and control flow
├── agent_sim.py        # Core simulation logic with MeTTa
├── visualizer.py       # Graph rendering (NetworkX + PyVis)
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

### MeTTa Integration

**MeTTa (Meta Type Talk)** is a programming language for AGI that operates on hypergraphs. In this simulation:

1. **Shared Space**: A `hypergraph` memory where all agents coexist
2. **Symbolic Rules**: Logic defining reputation changes based on actions
3. **Grounded Functions**: Python functions callable from MeTTa for dynamic updates

#### Agent Actions in MeTTa

The simulation defines cognitive rules in MeTTa:

```metta
; Contribute action increases reputation significantly
(= (action-contribute $agent)
   (update-reputation $agent 15))

; Share action increases reputation moderately
(= (action-share $agent)
   (update-reputation $agent 8))

; Idle decreases reputation (encouraging activity)
(= (action-idle $agent)
   (update-reputation $agent -2))
```

#### Grounded Functions

Python functions are registered with MeTTa using the `@operation` decorator:

```python
def update_reputation(agent_name: Atom, delta: Atom) -> Atom:
    """Update an agent's reputation by a delta value."""
    # ... implementation
    return ValueAtom(new_reputation)

metta.register_atom('update-reputation', 
                    OperationAtom('update-reputation', update_reputation))
```

### Reputation Dynamics

**Agent Actions:**
- **Contribute** (+15): Major contribution to the network
- **Share** (+8): Moderate positive action
- **Trade**: Reputation transfer with 1.1x multiplier (positive-sum)
- **Idle** (-2): Penalty for inactivity

**Health Score** = Average reputation across all agents (0-200 scale)

### Network Topology

The graph visualization uses NetworkX to create connections between agents:

- Agents with similar reputations form clusters
- High-reputation agents become more central in the network
- Edge weights reflect combined reputation of connected agents
- The graph is guaranteed to be connected (no isolated agents)

## 🎓 Educational Use Cases

This dashboard is ideal for:

- **AI Research**: Studying multi-agent dynamics and emergent behavior
- **MeTTa Learning**: Exploring hypergraph-based cognitive architectures  
- **Network Science**: Analyzing how reputation affects network topology
- **System Design**: Understanding health metrics in distributed systems
- **Demonstrations**: Showcasing ASI Chain concepts and MeTTa capabilities

## 🛠️ Technical Details

### Dependencies

- **streamlit** (≥1.28.0): Web application framework
- **hyperon** (≥0.1.12): MeTTa runtime for cognitive logic
- **networkx** (≥3.1): Graph structure manipulation
- **pyvis** (≥0.3.2): Interactive network visualization
- **matplotlib** (≥3.7.0): Color mapping and utilities
- **pandas** (≥2.0.0): Data handling and tables

### Performance

- Lightweight MeTTa rules ensure fast execution
- Non-blocking UI with async patterns (`st.empty()`)
- Smooth updates with configurable step delays
- Handles 3-20 agents efficiently

### Browser Compatibility

Tested on:
- Chrome/Edge (recommended)
- Firefox
- Safari

## 🔧 Customization

### Adding New Actions

1. Define a new action rule in `agent_sim.py`:
   ```python
   metta_rules += """
   (= (action-collaborate $agent)
      (update-reputation $agent 20))
   """
   ```

2. Add it to the action dispatcher in the `step()` method

3. Update the UI info in `app.py` sidebar

### Modifying Reputation Logic

Edit the MeTTa rules in `_load_metta_rules()` method:

```python
; Custom rule example: bonus for high reputation
(= (bonus-high-rep $agent $rep)
   (if (> $rep 150) 
       (update-reputation $agent 5)
       (update-reputation $agent 0)))
```

### Changing Visualization

Customize graph appearance in `visualizer.py`:

```python
def _get_reputation_color(reputation: float) -> str:
    # Modify color scheme here
    if reputation > 100:
        return '#YOUR_COLOR_CODE'
```

## 🚧 Future Enhancements

Potential extensions (from original spec):

- **Multi-Shard Simulation**: Separate `Space` instances for reputation, data, compute
- **Export Functionality**: Save hypergraph snapshots as JSON
- **AI Reasoning Log**: Panel showing MeTTa query results and decision traces
- **Advanced Metrics**: Clustering coefficients, betweenness centrality
- **Agent Profiles**: Individual agent dashboards with action history
- **Deployment**: One-click deploy to Streamlit Cloud or Hugging Face Spaces

## 📝 License

MIT License - feel free to use, modify, and distribute.

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📧 Contact

For questions, suggestions, or collaboration:

- GitHub Issues: [Report a bug or request a feature](https://github.com/yourusername/ASI-Chain-MeTTa-Simulation-Dashboard/issues)
- Email: your.email@example.com

## 🙏 Acknowledgments

- **OpenCog Hyperon** team for the MeTTa language and hyperon package
- **Streamlit** team for the amazing web framework
- **NetworkX** and **PyVis** communities for visualization tools
- **ASI Chain** concept and inspiration

---

**Built with ❤️ using MeTTa, Streamlit, and Python**

*Exploring the future of cognitive AI architectures, one agent at a time.*





