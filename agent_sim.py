"""
Core simulation logic for ASI Chain agent system using MeTTa (hyperon).

This module implements an agent-based simulation where:
- Agents exist in a shared hypergraph memory space
- Actions (contribute, share, trade) affect agent reputations
- MeTTa rules define the cognitive logic for reputation updates
- A health score tracks overall system performance
"""

import random
from typing import Dict, List, Tuple
from hyperon import MeTTa, OperationAtom, ValueAtom
from hyperon.atoms import Atom, E, S, V


class AgentSimulation:
    """
    Manages the ASI Chain agent simulation using MeTTa for cognitive logic.
    
    The simulation uses a shared hypergraph Space where:
    - Agents are represented as atoms with reputation values
    - Actions trigger MeTTa rules that update reputations
    - The system maintains a health_score (average reputation)
    """
    
    def __init__(self, num_agents: int = 5):
        """
        Initialize the simulation with a given number of agents.
        
        Args:
            num_agents: Number of agents to create in the simulation
        """
        self.num_agents = num_agents
        self.metta = MeTTa()
        self.agents: Dict[str, float] = {}
        self.action_history: List[Tuple[str, str, float]] = []
        self.step_count = 0
        
        # Initialize agents with random starting reputations
        self._initialize_agents()
        
        # Register Python grounded functions for reputation updates
        self._register_grounded_functions()
        
        # Load MeTTa rules for agent actions
        self._load_metta_rules()
    
    def _initialize_agents(self):
        """Create agents with initial reputation values."""
        for i in range(self.num_agents):
            agent_name = f"Agent_{i}"
            # Start with reputation between 50 and 100
            initial_reputation = random.uniform(50, 100)
            self.agents[agent_name] = initial_reputation
            
            # Add agent to MeTTa space as (agent <name> <reputation>)
            self.metta.run(f"!(bind! &space (agent {agent_name} {initial_reputation}))")
    
    def _register_grounded_functions(self):
        """
        Register Python functions that can be called from MeTTa.
        These bridge the Python simulation with MeTTa's symbolic reasoning.
        """
        
        # Function to update reputation based on action
        def update_reputation(agent_name: Atom, delta: Atom) -> Atom:
            """Update an agent's reputation by a delta value."""
            name = str(agent_name)
            change = float(str(delta))
            
            if name in self.agents:
                old_rep = self.agents[name]
                # Keep reputation between 0 and 200
                self.agents[name] = max(0, min(200, old_rep + change))
                return ValueAtom(self.agents[name])
            return ValueAtom(0)
        
        # Function to get current reputation
        def get_reputation(agent_name: Atom) -> Atom:
            """Retrieve an agent's current reputation."""
            name = str(agent_name)
            if name in self.agents:
                return ValueAtom(self.agents[name])
            return ValueAtom(0)
        
        # Function to transfer reputation between agents (for trade action)
        def transfer_reputation(from_agent: Atom, to_agent: Atom, amount: Atom) -> Atom:
            """Transfer reputation from one agent to another."""
            from_name = str(from_agent)
            to_name = str(to_agent)
            transfer_amount = float(str(amount))
            
            if from_name in self.agents and to_name in self.agents:
                if self.agents[from_name] >= transfer_amount:
                    self.agents[from_name] -= transfer_amount
                    # Positive-sum: receiver gets 1.1x the amount
                    self.agents[to_name] += transfer_amount * 1.1
                    return ValueAtom(1)  # Success
            return ValueAtom(0)  # Failure
        
        # Register the functions with MeTTa
        self.metta.register_atom('update-reputation', 
                                  OperationAtom('update-reputation', update_reputation))
        self.metta.register_atom('get-reputation', 
                                  OperationAtom('get-reputation', get_reputation))
        self.metta.register_atom('transfer-reputation', 
                                  OperationAtom('transfer-reputation', transfer_reputation))
    
    def _load_metta_rules(self):
        """
        Define MeTTa rules for agent actions and reputation logic.
        These rules specify how different actions affect reputation.
        """
        
        # Define action rules in MeTTa
        metta_rules = """
        ; Rule: contribute action increases reputation significantly
        (= (action-contribute $agent)
           (update-reputation $agent 15))
        
        ; Rule: share action increases reputation moderately
        (= (action-share $agent)
           (update-reputation $agent 8))
        
        ; Rule: idle action slightly decreases reputation (agents must stay active)
        (= (action-idle $agent)
           (update-reputation $agent -2))
        
        ; Helper to calculate positive/negative trend
        (= (reputation-trend $rep)
           (if (> $rep 100) positive 
               (if (> $rep 50) neutral negative)))
        """
        
        # Load the rules into MeTTa runtime
        self.metta.run(metta_rules)
    
    def step(self) -> Dict[str, any]:
        """
        Execute one simulation step:
        1. Select random agent and action
        2. Apply action through MeTTa rules
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
        
        # Execute action through MeTTa
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





