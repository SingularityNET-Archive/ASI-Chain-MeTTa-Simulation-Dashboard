# 🧠 ASI Chain Agent Simulation Dashboard

An interactive **Streamlit** web application that simulates an **Artificial Superintelligence (ASI) Chain** agent network using the **hyperon** (MeTTa) Python API for cognitive reasoning.

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/streamlit-1.28%2B-FF4B4B)
![MeTTa](https://img.shields.io/badge/hyperon-MeTTa-purple)
![License](https://img.shields.io/badge/license-MIT-green)

---

## 📑 Table of Contents

- [Overview](#-overview)
- [Quick Start](#-quick-start)
- [Key Concepts & Terminology](#-key-concepts--terminology)
- [Design Choices](#-design-choices)
- [How to Use](#-how-to-use)
- [Architecture](#-architecture)
- [Deployment Guide](#-deployment-guide)
- [Customization](#-customization)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Overview

This dashboard visualizes a multi-agent system where autonomous agents:

- 🧠 **Think** using MeTTa symbolic reasoning
- 🤝 **Collaborate** in a shared hypergraph memory space  
- 📊 **Evolve** reputations based on their actions
- 🌐 **Form** a dynamic network of relationships

The simulation demonstrates how cognitive rules defined in MeTTa can govern agent behavior, reputation dynamics, and emergent network properties in a distributed AI system.

### ✨ Features

- **Real-time Agent Network Visualization** with step-by-step replay
- **MeTTa-powered cognitive logic** for symbolic reasoning
- **Interactive controls** for simulation parameters
- **Action indicators** showing what's happening at each step
- **Health score tracking** for system-level metrics
- **Anti-flicker optimizations** for smooth graph rendering

---

## 🚀 Quick Start

### Option 1: Try Online (Recommended)

**Live Demo**: [View on Streamlit Cloud](https://your-app-url.streamlit.app)

### Option 2: Run Locally

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/ASI-Chain-MeTTa-Simulation-Dashboard.git
cd ASI-Chain-MeTTa-Simulation-Dashboard

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the application
streamlit run app.py
```

The app will open at `http://localhost:8501`

### First Simulation

1. Keep default settings (5 agents, 20 steps)
2. Click **▶️ Run**
3. Watch agents take actions and reputations change
4. Use the replay controls to step through the simulation

---

## 📖 Key Concepts & Terminology

### 🤖 Agents

**What they are**: Autonomous entities in the simulation with individual reputation scores.

**Starting state**: Each agent begins with a random reputation between 50-100.

**Goal**: Maximize reputation through strategic actions.

### 📊 Reputation

**Definition**: A numerical score (0-200) representing an agent's standing in the network.

**Purpose**: The primary metric for agent success and network health.

**Dynamics**: 
- Increases through productive actions (contribute, share)
- Decreases through inactivity (idle)
- Transfers through trade (with bonus)

### 🎯 Actions

Agents can perform four types of actions:

| Action | Effect | Reputation Change | Meaning |
|--------|--------|-------------------|---------|
| **🤝 Contribute** | Major boost | +15 | Agent performs significant work benefiting the network |
| **📤 Share** | Moderate boost | +8 | Agent shares knowledge or resources |
| **💱 Trade** | Transfer | Variable | Agent transfers reputation to another (with 10% bonus) |
| **😴 Idle** | Penalty | -2 | Agent does nothing (discourages inactivity) |

### 💱 Trade (Positive-Sum Exchange)

**What it means**: One agent transfers reputation to another, but the system creates value.

**Example**:
- Agent_0 trades 10 reputation to Agent_2
- Agent_0 loses: -10
- Agent_2 gains: +11 (10 × 1.1)
- **Net system gain**: +1 reputation

**Why positive-sum?**: Represents the economic principle that voluntary exchange creates value. The 10% multiplier incentivizes cooperation and trading over hoarding.

### 🏥 Health Score

**Definition**: Average reputation across all agents.

**Formula**: `Health Score = Sum of all reputations / Number of agents`

**Purpose**: System-level metric showing overall network performance.

**Typical range**: 50-120 (starts at ~75, grows with productive actions)

### 🕸️ Network Graph

**Nodes (Circles)**: 
- Each node = one agent
- **Size**: Larger = higher reputation
- **Color**: Indicates reputation tier (red → orange → yellow → green)

**Edges (Lines)**:
- Connect agents with **similar reputations**
- Show reputation-based clustering
- **NOT** trade relationships or interactions
- Each agent links to 2-3 nearest reputation peers

**Why this design?**: Makes it easy to visually identify reputation tiers and watch agents migrate between clusters as their reputation changes.

### 🧠 MeTTa (Meta Type Talk)

**What it is**: A programming language for AGI that operates on hypergraphs.

**Role in simulation**: Defines the symbolic rules governing agent behavior.

**Example rule**:
```metta
; When an agent contributes, increase their reputation by 15
(= (action-contribute $agent)
   (update-reputation $agent 15))
```

### 🔗 Grounded Functions

**Definition**: Python functions that can be called from MeTTa code.

**Purpose**: Bridge between symbolic reasoning (MeTTa) and actual computation (Python).

**Example**: The `update-reputation` function is called from MeTTa but implemented in Python.

### 📈 Graph Update Frequency

**What it is**: How often the visualization updates (every N steps).

**Default**: Every 3 steps

**Purpose**: Reduces flicker while keeping visualization responsive.

**Trade-off**: 
- Lower (1-2): See every change, but more flicker
- Higher (5-10): Smoother, but less frequent updates

---

## 🎨 Design Choices

### Why These Agent Actions?

1. **Contribute (+15)**: Largest reward encourages productive behavior
2. **Share (+8)**: Moderate reward balances generosity with self-interest
3. **Trade (1.1x)**: Positive-sum incentivizes cooperation over isolation
4. **Idle (-2)**: Small penalty keeps agents active without being punitive

**Alternative considered**: Zero-sum trade (1.0x multiplier) - rejected because it doesn't incentivize trading.

### Why Reputation-Based Clustering?

**Chosen approach**: Edges connect similar-reputation agents

**Reasoning**:
- Creates intuitive visual tiers (high/medium/low reputation groups)
- Easy to see agents migrate between clusters
- Shows emergent social structure based on performance

**Alternative considered**: Random connections - rejected because it doesn't convey meaningful information.

**Alternative considered**: Trade-history connections - rejected because trades are rare and graph would be sparse.

### Why Start Agents at 50-100?

**Reasoning**:
- Gives room to grow (up to 200)
- Prevents immediate failure (floor at 0)
- Creates initial diversity in the network
- Allows for interesting early dynamics

**Alternative considered**: All start at 100 - rejected because it's less interesting visually.

### Why 0-200 Reputation Scale?

**Reasoning**:
- 100 = neutral midpoint (easy reference)
- Room for both growth and decline
- Clean divisions: 0-50 (red), 50-100 (orange), 100-150 (yellow), 150-200 (green)

### Why Simplified MeTTa Version by Default?

**Technical challenge**: Full `hyperon` package requires Conan (C++ build system) which:
- Takes 10-15 minutes to compile
- Requires additional system dependencies
- May fail on some platforms

**Solution**: Created `agent_sim_simple.py` that:
- Simulates MeTTa-like behavior using pure Python
- Installs in seconds
- Demonstrates the same concepts
- Falls back gracefully if hyperon isn't available

**For advanced users**: Instructions provided in `install_hyperon.sh` for full MeTTa support.

### Why Step-by-Step Replay?

**Purpose**: Educational tool for understanding simulation dynamics

**Use cases**:
- **Analysis**: Review specific actions and their impacts
- **Presentations**: Step through interesting moments
- **Debugging**: Understand unexpected behavior
- **Learning**: See how each action affects the network

**Implementation**: Stores complete agent state at every step (memory trade-off for functionality).

### Why These Colors?

Color psychology applied to reputation tiers:

- 🟢 **Green (150-200)**: Success, growth, positive
- 🟡 **Yellow (100-150)**: Caution, stable, adequate
- 🟠 **Orange (50-100)**: Warning, needs attention
- 🔴 **Red (0-50)**: Danger, failing, critical

Makes status immediately recognizable without reading numbers.

---

## 📖 How to Use

### Basic Workflow

1. **Configure Parameters** in the sidebar:
   - **Number of Agents** (3-20): More agents = complex dynamics
   - **Simulation Steps** (10-100): How long to run
   - **Step Delay** (0.1-2.0s): Speed of animation
   - **Graph Update Frequency** (1-10): Smoothness vs detail

2. **Click ▶️ Run** to start

3. **Observe**:
   - Status bar shows current action
   - Graph updates showing network changes
   - Metrics track health score and distribution

4. **Control**:
   - **⏹️ Stop**: Pause simulation anytime
   - **🔄 Reset**: Clear and start fresh

5. **Replay** (after completion):
   - Use slider to jump to any step
   - Click ⏪ Previous / Next ⏩ to step through
   - See exact action and reputation changes

### Understanding What You See

**During Simulation:**
- Colored banner shows current action
- Graph updates periodically (based on update frequency)
- Metrics update every step
- Nodes change color/size as reputations change

**In Replay Mode:**
- Navigate to any point in the simulation
- See the exact network state at that moment
- Review action details for each step

### Tips for Best Experience

**For Smooth Visualization:**
- Set Graph Update Frequency to 5-10
- Use 0.3-0.5 second step delay

**For Detailed Analysis:**
- Set Graph Update Frequency to 1-2
- Use 1.0+ second step delay
- Run fewer steps (10-20) for focused study

**For Quick Overview:**
- Set Graph Update Frequency to 10
- Use 0.1 second step delay
- Run many steps (50-100) to see long-term trends

---

## 🏗️ Architecture

### Project Structure

```
ASI-Chain-MeTTa-Simulation-Dashboard/
├── app.py                    # Streamlit UI and control flow
├── agent_sim_simple.py       # Core simulation (pure Python)
├── agent_sim.py             # Core simulation (full hyperon) [optional]
├── visualizer.py            # Graph rendering (NetworkX + PyVis)
├── requirements.txt         # Python dependencies
├── install_hyperon.sh       # Script for full hyperon installation
├── test_installation.py     # Verify dependencies
├── .streamlit/
│   └── config.toml          # Streamlit theme configuration
├── packages.txt             # System dependencies for cloud deployment
└── README.md               # This file
```

### Module Responsibilities

**app.py** (544 lines):
- Streamlit interface
- Session state management
- Simulation control flow
- Replay navigation
- Action indicators

**agent_sim_simple.py** (275 lines):
- Agent initialization
- MeTTa-like rule system
- Action execution
- Reputation management
- Health score calculation

**visualizer.py** (316 lines):
- NetworkX graph creation
- PyVis HTML generation
- Node styling (color, size)
- Edge creation (similarity-based)
- Network statistics

### Data Flow

```
┌──────────────┐
│   User Input │ (sidebar controls)
└──────┬───────┘
       ↓
┌──────────────┐
│  app.py      │ (orchestration)
└──────┬───────┘
       ↓
┌──────────────┐
│ agent_sim.py │ (simulation logic)
│  - MeTTa rules
│  - State updates
└──────┬───────┘
       ↓
┌──────────────┐
│visualizer.py │ (graph generation)
│  - NetworkX
│  - PyVis
└──────┬───────┘
       ↓
┌──────────────┐
│  Browser     │ (interactive display)
└──────────────┘
```

### MeTTa Integration

**Symbolic Rules** (in `agent_sim.py`):
```python
metta_rules = """
(= (action-contribute $agent)
   (update-reputation $agent 15))

(= (action-share $agent)
   (update-reputation $agent 8))
"""
self.metta.run(metta_rules)
```

**Grounded Functions**:
```python
def update_reputation(agent_name, delta):
    # Python implementation
    return new_reputation

# Register with MeTTa
metta.register_function('update-reputation', update_reputation)
```

**Execution**:
```python
# Call MeTTa rule from Python
result = metta.run("!(action-contribute Agent_0)")
```

---

## ☁️ Deployment Guide

### Deploy to Streamlit Cloud (Free!)

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git
   git push -u origin main
   ```

2. **Deploy**
   - Go to [share.streamlit.io](https://share.streamlit.io/)
   - Click "New app"
   - Select your repository
   - Main file: `app.py`
   - Click "Deploy"

3. **Wait 2-3 minutes**
   - App builds and deploys automatically
   - You'll get a URL like: `https://YOUR_APP.streamlit.app`

4. **Auto-redeploy**
   - Any push to GitHub triggers automatic redeployment
   - No manual intervention needed

### Streamlit Cloud Features

- ✅ **100% Free** for public apps
- ✅ **Auto-deploy** on GitHub push
- ✅ **HTTPS** included
- ✅ **Custom subdomain**
- ✅ **1 GB RAM** per app
- ✅ **Sleep after inactivity** (wakes on visit)

### Troubleshooting Deployment

**Build fails**:
- Check logs in Streamlit Cloud dashboard
- Verify `requirements.txt` is correct
- Ensure all files are committed to GitHub

**App is slow**:
- Reduce default number of agents in code
- Increase graph update frequency default
- Optimize PyVis rendering settings

**Import errors**:
- Make sure `agent_sim_simple.py` is in repository
- Check that all dependencies are in `requirements.txt`

---

## 🔧 Customization

### Adding New Actions

1. **Define MeTTa rule** in `agent_sim_simple.py`:
   ```python
   def action_innovate(agent):
       return self.metta.grounded_functions['update-reputation'](agent, '25')
   
   self.metta.add_rule('action-innovate', action_innovate)
   ```

2. **Add to action dispatcher**:
   ```python
   actions = ['contribute', 'share', 'trade', 'idle', 'innovate']
   weights = [0.3, 0.25, 0.15, 0.1, 0.2]
   ```

3. **Update UI**:
   - Add emoji to `action_emoji` dict
   - Add color to `action_color` dict
   - Update welcome screen documentation

### Modifying Reputation Rules

Change the values in `_load_rules()`:

```python
def action_contribute(agent):
    return self.metta.grounded_functions['update-reputation'](agent, '20')  # Was 15
```

### Adjusting Trade Multiplier

In `transfer_reputation()` function:

```python
self.agents[to_agent] += transfer_amount * 1.2  # Was 1.1 (20% bonus instead of 10%)
```

### Changing Visualization Colors

In `visualizer.py`:

```python
def _get_reputation_color(reputation: float) -> str:
    if normalized < 0.25:
        return '#YOUR_HEX_COLOR'  # Change red zone color
```

### Modifying Graph Clustering

In `create_agent_graph()`:

```python
num_connections = min(5, len(similar_agents))  # Was 3
```

---

## 🤝 Contributing

Contributions welcome! Here's how:

### Getting Started

1. **Fork** the repository
2. **Clone** your fork
3. **Create a branch**: `git checkout -b feature/amazing-feature`
4. **Make changes**
5. **Test**: Run `python test_installation.py`
6. **Commit**: `git commit -m "Add amazing feature"`
7. **Push**: `git push origin feature/amazing-feature`
8. **Open Pull Request** on GitHub

### Code Style

- Follow PEP 8
- Use type hints
- Write docstrings
- Add comments for complex logic
- Keep functions focused (< 50 lines)

### What to Contribute

**Ideas welcome**:
- New agent actions
- Different network topologies
- Alternative visualization styles
- Performance improvements
- Bug fixes
- Documentation improvements

**Priority areas**:
- Multi-shard simulation (separate reputation/data/compute spaces)
- Export/import functionality
- Advanced metrics (centrality, clustering coefficients)
- Agent personality traits
- Historical comparison tools

---

## 📝 License

MIT License - See [LICENSE](LICENSE) file for details.

Free to use, modify, and distribute with attribution.

---

## 🙏 Acknowledgments

- **OpenCog Hyperon** team for MeTTa language and hyperon package
- **Streamlit** team for the amazing web framework
- **NetworkX** and **PyVis** communities for visualization tools
- **ASI Chain** concept and inspiration from distributed AI research
- All contributors and users of this project

---

## 📧 Support

**Questions?**
- Open an [issue on GitHub](https://github.com/yourusername/ASI-Chain-MeTTa-Simulation-Dashboard/issues)
- Check existing issues for similar questions

**Bug Reports:**
- Include error message and full traceback
- Describe steps to reproduce
- Mention your environment (OS, Python version)

**Feature Requests:**
- Describe the feature and use case
- Explain why it would be valuable
- Consider submitting a PR!

---

**Built with ❤️ using MeTTa, Streamlit, and Python**

*Exploring the future of cognitive AI architectures, one agent at a time.*

---

**⭐ Star this repo if you find it useful!**

**🔗 Live Demo**: [Your App on Streamlit Cloud](https://your-app-url.streamlit.app)
