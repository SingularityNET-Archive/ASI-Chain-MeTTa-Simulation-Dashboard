"""
Simplified simulation logic for ASI Chain agent system (without hyperon dependency).

This version simulates MeTTa-like behavior using pure Python, making it easy to install and run.
The logic and concepts remain the same, but without requiring the complex hyperon/Conan build.
"""

import random
from typing import Dict, List, Tuple


class SimpleMeTTaRuntime:
    """
    Simple simulator that mimics MeTTa's behavior without requiring hyperon.
    This demonstrates the concepts while being easy to install.
    """
    
    def __init__(self):
        self.rules = {}
        self.grounded_functions = {}
    
    def register_function(self, name: str, func):
        """Register a grounded function."""
        self.grounded_functions[name] = func
    
    def add_rule(self, name: str, func):
        """Add a rule/action."""
        self.rules[name] = func
    
    def run(self, command: str):
        """Execute a command (simplified MeTTa-like interface)."""
        # Parse simple commands like !(action-contribute Agent_0)
        if command.startswith('!(') and command.endswith(')'):
            parts = command[2:-1].split()
            action = parts[0]
            args = parts[1:] if len(parts) > 1 else []
            
            if action in self.rules:
                return self.rules[action](*args)
        
        return None


class AgentSimulation:
    """
    Manages the ASI Chain agent simulation using simplified MeTTa-like logic.
    
    The simulation uses a rule-based system where:
    - Agents are represented with reputation values
    - Actions trigger rules that update reputations
    - The system maintains a health_score (average reputation)
    """
    
    def __init__(self, num_agents: int = 5):
        """
        Initialize the simulation with a given number of agents.
        
        Args:
            num_agents: Number of agents to create in the simulation
        """
        self.num_agents = num_agents
        self.metta = SimpleMeTTaRuntime()
        self.agents: Dict[str, float] = {}
        self.action_history: List[Tuple[str, str, float]] = []
        self.step_count = 0
        
        # Initialize agents with random starting reputations
        self._initialize_agents()
        
        # Register grounded functions for reputation updates
        self._register_grounded_functions()
        
        # Load rules for agent actions
        self._load_rules()
    
    def _initialize_agents(self):
        """Create agents with initial reputation values."""
        for i in range(self.num_agents):
            agent_name = f"Agent_{i}"
            # Start with reputation between 50 and 100
            initial_reputation = random.uniform(50, 100)
            self.agents[agent_name] = initial_reputation
    
    def _register_grounded_functions(self):
        """
        Register Python functions that can be called from the rule system.
        These bridge the Python simulation with MeTTa-like symbolic reasoning.
        """
        
        def update_reputation(agent_name: str, delta: str) -> float:
            """Update an agent's reputation by a delta value."""
            change = float(delta)
            
            if agent_name in self.agents:
                old_rep = self.agents[agent_name]
                # Keep reputation between 0 and 200
                self.agents[agent_name] = max(0, min(200, old_rep + change))
                return self.agents[agent_name]
            return 0
        
        def get_reputation(agent_name: str) -> float:
            """Retrieve an agent's current reputation."""
            if agent_name in self.agents:
                return self.agents[agent_name]
            return 0
        
        def transfer_reputation(from_agent: str, to_agent: str, amount: str) -> int:
            """Transfer reputation from one agent to another."""
            transfer_amount = float(amount)
            
            if from_agent in self.agents and to_agent in self.agents:
                if self.agents[from_agent] >= transfer_amount:
                    self.agents[from_agent] -= transfer_amount
                    # Positive-sum: receiver gets 1.1x the amount
                    self.agents[to_agent] += transfer_amount * 1.1
                    return 1  # Success
            return 0  # Failure
        
        # Register the functions
        self.metta.register_function('update-reputation', update_reputation)
        self.metta.register_function('get-reputation', get_reputation)
        self.metta.register_function('transfer-reputation', transfer_reputation)
    
    def _load_rules(self):
        """
        Define rules for agent actions and reputation logic.
        These rules specify how different actions affect reputation (MeTTa-like rules).
        """
        
        # Rule: contribute action increases reputation significantly
        def action_contribute(agent):
            return self.metta.grounded_functions['update-reputation'](agent, '15')
        
        # Rule: share action increases reputation moderately
        def action_share(agent):
            return self.metta.grounded_functions['update-reputation'](agent, '8')
        
        # Rule: idle action slightly decreases reputation
        def action_idle(agent):
            return self.metta.grounded_functions['update-reputation'](agent, '-2')
        
        def action_transfer(from_agent, to_agent, amount):
            return self.metta.grounded_functions['transfer-reputation'](from_agent, to_agent, amount)
        
        # Register the rules
        self.metta.add_rule('action-contribute', action_contribute)
        self.metta.add_rule('action-share', action_share)
        self.metta.add_rule('action-idle', action_idle)
        self.metta.add_rule('transfer-reputation', action_transfer)
    
    def step(self) -> Dict[str, any]:
        """
        Execute one simulation step:
        1. Select random agent and action
        2. Apply action through rule system
        3. Update reputation
        4. Return state information
        
        Returns:
            Dictionary with step information (agent, action, reputation change)
        """
        self.step_count += 1
        
        # Select random agent
        agent_name = random.choice(list(self.agents.keys()))
        
        # Select random action (weighted towards productive actions)
        actions = ['contribute', 'share', 'trade', 'idle']
        weights = [0.4, 0.3, 0.2, 0.1]  # Favor contribute and share
        action = random.choices(actions, weights=weights)[0]
        
        old_reputation = self.agents[agent_name]
        
        # Execute action through rule system
        if action == 'contribute':
            result = self.metta.run(f"!(action-contribute {agent_name})")
        elif action == 'share':
            result = self.metta.run(f"!(action-share {agent_name})")
        elif action == 'trade':
            # Select another agent to trade with
            other_agents = [a for a in self.agents.keys() if a != agent_name]
            if other_agents:
                partner = random.choice(other_agents)
                transfer_amount = random.uniform(5, 15)
                result = self.metta.run(
                    f"!(transfer-reputation {agent_name} {partner} {transfer_amount})"
                )
        else:  # idle
            result = self.metta.run(f"!(action-idle {agent_name})")
        
        new_reputation = self.agents[agent_name]
        reputation_change = new_reputation - old_reputation
        
        # Record action in history
        self.action_history.append((agent_name, action, reputation_change))
        
        return {
            'step': self.step_count,
            'agent': agent_name,
            'action': action,
            'old_reputation': old_reputation,
            'new_reputation': new_reputation,
            'reputation_change': reputation_change,
            'health_score': self.get_health_score()
        }
    
    def get_health_score(self) -> float:
        """
        Calculate system health score as average agent reputation.
        
        Returns:
            Average reputation across all agents (0-200 scale)
        """
        if not self.agents:
            return 0.0
        return sum(self.agents.values()) / len(self.agents)
    
    def get_agent_states(self) -> Dict[str, float]:
        """
        Get current state of all agents.
        
        Returns:
            Dictionary mapping agent names to reputation values
        """
        return self.agents.copy()
    
    def get_action_history(self) -> List[Tuple[str, str, float]]:
        """
        Get the history of all actions taken.
        
        Returns:
            List of tuples (agent_name, action, reputation_change)
        """
        return self.action_history.copy()
    
    def reset(self, num_agents: int = None):
        """
        Reset the simulation to initial state.
        
        Args:
            num_agents: Optional new number of agents (uses current if None)
        """
        if num_agents is not None:
            self.num_agents = num_agents
        
        self.agents.clear()
        self.action_history.clear()
        self.step_count = 0
        
        # Reinitialize
        self._initialize_agents()
    
    def get_reputation_distribution(self) -> Dict[str, int]:
        """
        Categorize agents by reputation level.
        
        Returns:
            Dictionary with counts for 'high', 'medium', 'low' reputation
        """
        distribution = {'high': 0, 'medium': 0, 'low': 0}
        
        for reputation in self.agents.values():
            if reputation >= 100:
                distribution['high'] += 1
            elif reputation >= 50:
                distribution['medium'] += 1
            else:
                distribution['low'] += 1
        
        return distribution




