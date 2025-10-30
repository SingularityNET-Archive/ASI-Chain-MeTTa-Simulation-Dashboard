# ASI Chain Dashboard - Project Overview

## 📦 Project Structure

```
ASI-Chain-MeTTa-Simulation-Dashboard/
│
├── 🎯 Core Application Files
│   ├── app.py                 # Streamlit web interface (main entry point)
│   ├── agent_sim.py          # MeTTa simulation engine and agent logic
│   └── visualizer.py         # NetworkX + PyVis graph visualization
│
├── 📚 Documentation
│   ├── README.md             # Comprehensive project documentation
│   ├── QUICKSTART.md         # 5-minute quick start guide
│   ├── CONTRIBUTING.md       # Contribution guidelines
│   └── PROJECT_OVERVIEW.md   # This file
│
├── 🛠️ Configuration & Setup
│   ├── requirements.txt      # Python package dependencies
│   ├── .gitignore           # Git ignore patterns
│   └── LICENSE              # MIT License
│
└── 🧪 Testing
    └── test_installation.py  # Installation verification script
```

## 🚀 Quick Start (3 Commands)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Test installation (optional but recommended)
python test_installation.py

# 3. Launch the dashboard
streamlit run app.py
```

Then open your browser to `http://localhost:8501`

## 🎨 What Does It Do?

This dashboard simulates an **ASI Chain agent network** where:

1. **Agents** exist in a shared MeTTa hypergraph memory space
2. **Actions** (contribute, share, trade, idle) dynamically update reputations
3. **MeTTa rules** define the cognitive logic governing behavior
4. **Real-time visualization** shows the evolving agent network
5. **Health metrics** track overall system performance

## 🧠 Key Technologies

| Technology | Purpose | Version |
|------------|---------|---------|
| **Streamlit** | Web interface framework | ≥1.28.0 |
| **Hyperon** | MeTTa runtime for AGI logic | ≥0.1.12 |
| **NetworkX** | Graph structure manipulation | ≥3.1 |
| **PyVis** | Interactive network visualization | ≥0.3.2 |
| **Pandas** | Data handling and tables | ≥2.0.0 |

## 🏗️ Architecture

### Three-Layer Design

```
┌─────────────────────────────────────────────┐
│         Streamlit UI Layer (app.py)         │
│  • Controls & Parameters                    │
│  • Real-time Metrics                        │
│  • Interactive Dashboard                    │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────┴──────────────────────────┐
│     Visualization Layer (visualizer.py)     │
│  • NetworkX graph creation                  │
│  • PyVis rendering                          │
│  • Color & size styling                     │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────┴──────────────────────────┐
│    Simulation Engine (agent_sim.py)         │
│  • MeTTa runtime initialization             │
│  • Agent action logic                       │
│  • Reputation dynamics                      │
│  • Grounded function bridge                 │
└─────────────────────────────────────────────┘
```

## 📊 Core Components

### AgentSimulation Class (`agent_sim.py`)

**Responsibilities:**
- Initialize MeTTa runtime and shared hypergraph space
- Create agents with random starting reputations
- Register Python grounded functions for MeTTa
- Define cognitive rules for agent actions
- Execute simulation steps
- Calculate health score metrics

**Key Methods:**
- `__init__(num_agents)` - Initialize simulation
- `step()` - Execute one simulation step
- `get_health_score()` - Calculate average reputation
- `get_agent_states()` - Retrieve current agent data
- `reset()` - Reset to initial state

### Visualizer Module (`visualizer.py`)

**Responsibilities:**
- Create NetworkX graph from agent data
- Style nodes by reputation (color, size)
- Generate edges based on similarity
- Render interactive PyVis visualization
- Produce HTML for Streamlit embedding

**Key Functions:**
- `create_agent_graph(agents)` - Build NetworkX graph
- `render_pyvis_graph(nx_graph)` - Generate PyVis HTML
- `create_reputation_legend()` - Color coding explanation
- `get_network_statistics(nx_graph)` - Topology metrics

### Streamlit App (`app.py`)

**Responsibilities:**
- Render UI controls and parameters
- Manage session state (simulation instance, history)
- Run simulation loop with dynamic updates
- Display graphs, tables, and metrics
- Handle user interactions (run, stop, reset)

**Key Functions:**
- `initialize_session_state()` - Setup state variables
- `render_sidebar()` - Create control panel
- `run_simulation()` - Execute simulation with updates
- `render_main_content()` - Display information when idle

## 🎮 User Interaction Flow

```
User opens dashboard
        ↓
Configures parameters (agents, steps, speed)
        ↓
Clicks "Run" button
        ↓
Simulation loop starts:
  1. Agent takes action
  2. MeTTa evaluates rules
  3. Reputation updates
  4. Graph re-renders
  5. Metrics update
  6. Repeat until complete or stopped
        ↓
User views results (graph, table, chart)
        ↓
User can reset and run again
```

## 🔬 MeTTa Integration Details

### Grounded Functions Bridge

Python functions are registered with MeTTa to enable bidirectional communication:

```python
# Python function
def update_reputation(agent_name: Atom, delta: Atom) -> Atom:
    # ... implementation
    return ValueAtom(new_reputation)

# Register with MeTTa
metta.register_atom('update-reputation', 
                    OperationAtom('update-reputation', update_reputation))
```

### MeTTa Rules

Symbolic rules define agent behavior:

```metta
(= (action-contribute $agent)
   (update-reputation $agent 15))
```

### Execution Flow

1. Python selects agent and action
2. MeTTa rule evaluates: `!(action-contribute Agent_0)`
3. Rule calls grounded function: `(update-reputation Agent_0 15)`
4. Python function updates agent state
5. Result returned to MeTTa
6. Simulation continues

## 📈 Metrics Explained

### Health Score
- **Definition**: Average reputation across all agents
- **Range**: 0-200 (typically 50-150 in practice)
- **Interpretation**: Higher = better overall network performance

### Reputation Distribution
- **High** (150-200): Elite agents with excellent standing
- **Medium** (50-100): Average agents maintaining baseline
- **Low** (0-50): Struggling agents needing improvement

### Network Statistics
- **Density**: How connected the network is
- **Average Degree**: Average number of connections per agent
- **Path Length**: Average distance between any two agents

## 🎨 Customization Guide

### Adding New Actions

1. Define MeTTa rule in `agent_sim.py`:
   ```python
   (= (action-innovate $agent)
      (update-reputation $agent 25))
   ```

2. Add to action dispatcher in `step()` method

3. Update UI documentation in `app.py`

### Changing Reputation Logic

Modify rules in `_load_metta_rules()`:
```python
; Example: Bonus for consecutive contributions
(= (bonus-streak $agent $count)
   (if (> $count 3)
       (update-reputation $agent 10)
       (update-reputation $agent 0)))
```

### Adjusting Visualization

Edit color mapping in `visualizer.py`:
```python
def _get_reputation_color(reputation: float) -> str:
    if reputation > 150:
        return '#YOUR_HEX_COLOR'
```

## 🐛 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| Hyperon import fails | Install from source: `pip install git+https://github.com/trueagi-io/hyperon-experimental.git` |
| Port 8501 in use | Run with different port: `streamlit run app.py --server.port 8502` |
| Graph doesn't render | Check browser console, try different browser (Chrome recommended) |
| Simulation freezes | Reduce number of agents or steps, increase step delay |

### Verification Steps

1. Run `python test_installation.py` - should pass all tests
2. Check Python version: `python --version` (should be ≥3.8)
3. Verify packages: `pip list | grep -E "streamlit|hyperon|networkx|pyvis"`

## 🚀 Deployment Options

### Local Development
```bash
streamlit run app.py
```

### Streamlit Cloud
1. Push to GitHub
2. Connect repository to Streamlit Cloud
3. Deploy with one click
4. Share public URL

### Docker (Future Enhancement)
```dockerfile
FROM python:3.10
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD streamlit run app.py
```

## 📚 Learning Resources

### Understand MeTTa
- Read `agent_sim.py` comments explaining MeTTa integration
- Experiment with new rules in the code
- Check OpenCog wiki for MeTTa language details

### Understand Multi-Agent Systems
- Run simulations with different parameters
- Observe how reputation dynamics emerge
- Analyze network topology changes

### Understand Streamlit
- Review `app.py` for UI patterns
- Try adding new visualizations
- Explore Streamlit documentation

## 🎯 Future Roadmap

Potential enhancements from original spec:

- [ ] Multi-shard simulation (reputation, data, compute spaces)
- [ ] Export/import functionality (JSON snapshots)
- [ ] AI reasoning log panel (MeTTa query traces)
- [ ] Agent personality traits
- [ ] Advanced network analysis
- [ ] Historical comparison tools
- [ ] Real-time collaboration features
- [ ] Integration with external AI services

## 📝 File Manifest

| File | Lines | Purpose |
|------|-------|---------|
| `app.py` | ~450 | Streamlit web interface |
| `agent_sim.py` | ~280 | MeTTa simulation engine |
| `visualizer.py` | ~260 | Graph visualization |
| `test_installation.py` | ~180 | Installation verification |
| `README.md` | ~400 | Main documentation |
| `QUICKSTART.md` | ~120 | Quick start guide |
| `CONTRIBUTING.md` | ~250 | Contribution guidelines |

**Total**: ~2,000 lines of code and documentation

## 🎉 Success Criteria Checklist

- ✅ Dashboard runs locally with `streamlit run app.py`
- ✅ Graph visualization updates smoothly
- ✅ Agent reputations change based on MeTTa rules
- ✅ Health score accurately reflects system state
- ✅ UI remains responsive with stop/reset controls
- ✅ Code is modular and well-documented
- ✅ MeTTa integration explained with inline comments
- ✅ Complete documentation provided
- ✅ Installation test script included
- ✅ No linter errors in code

## 🙏 Acknowledgments

Built with:
- **Hyperon/MeTTa** - OpenCog Foundation
- **Streamlit** - Streamlit Inc.
- **NetworkX** - NetworkX Developers
- **PyVis** - WestHealth Institute

---

**Project Status**: ✅ Complete and Ready for Use

**Last Updated**: October 2025

**Maintained by**: ASI Chain Dashboard Contributors





