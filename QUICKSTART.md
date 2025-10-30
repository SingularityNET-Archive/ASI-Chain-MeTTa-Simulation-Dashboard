# 🚀 Quick Start Guide

Get the ASI Chain Agent Simulation running in under 5 minutes!

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- Streamlit (web framework)
- Hyperon (MeTTa runtime)
- NetworkX & PyVis (visualization)
- Pandas & Matplotlib (data handling)

## Step 2: Run the Application

```bash
streamlit run app.py
```

The dashboard will automatically open in your browser at `http://localhost:8501`

## Step 3: Run Your First Simulation

1. **In the sidebar**, you'll see default parameters:
   - Number of Agents: 5
   - Simulation Steps: 20
   - Step Delay: 0.5 seconds

2. **Click the ▶️ Run button**

3. **Watch as**:
   - The agent network graph appears and updates
   - Agents take actions (contribute, share, trade, idle)
   - Reputations change dynamically
   - The health score evolves

4. **Explore the results**:
   - See the reputation rankings table
   - Review the health score chart
   - Expand the action history

## Understanding What You See

### The Graph
- **Nodes** = Agents
- **Colors**: 🟢 Green (high rep) → 🟡 Yellow → 🟠 Orange → 🔴 Red (low rep)
- **Size**: Bigger nodes = higher reputation
- **Edges**: Connections between similar agents

### The Metrics
- **Health Score**: Average reputation (higher is better)
- **High/Medium/Low Rep Agents**: Distribution across reputation levels

### The Actions
- **Contribute**: +15 reputation (productive work)
- **Share**: +8 reputation (knowledge sharing)
- **Trade**: Transfer reputation (positive-sum, +10% bonus)
- **Idle**: -2 reputation (penalty for inactivity)

## Try Different Scenarios

### Small Team (3 agents, 50 steps)
See how a small group evolves over time

### Large Network (15 agents, 20 steps)
Watch complex network dynamics emerge

### Fast Simulation (20 agents, 100 steps, 0.1s delay)
Quick overview of long-term trends

### Slow Motion (5 agents, 30 steps, 1.5s delay)
Carefully observe each action's effect

## Troubleshooting

### Port Already in Use
```bash
streamlit run app.py --server.port 8502
```

### Dependencies Not Found
Make sure you're in the project directory:
```bash
cd ASI-Chain-MeTTa-Simulation-Dashboard
pip install -r requirements.txt
```

### Hyperon Installation Issues
Try installing from source:
```bash
pip install git+https://github.com/trueagi-io/hyperon-experimental.git
```

## Next Steps

- Read the full [README.md](README.md) for technical details
- Explore `agent_sim.py` to see MeTTa rules
- Modify actions and reputation logic in the code
- Share your results and feedback!

---

**Need Help?** Open an issue on GitHub or check the README for more info.

**Enjoy exploring AGI agent dynamics!** 🧠✨





