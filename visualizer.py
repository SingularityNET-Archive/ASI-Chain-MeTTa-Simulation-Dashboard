"""
Graph visualization module for ASI Chain agent network.

This module provides functions to:
- Create NetworkX graphs from agent data
- Render interactive PyVis visualizations
- Style nodes based on reputation scores
- Generate HTML output for Streamlit embedding
"""

import networkx as nx
from pyvis.network import Network
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from typing import Dict, Tuple
import tempfile
import os


def create_agent_graph(agents: Dict[str, float]) -> nx.Graph:
    """
    Create a NetworkX graph representing the agent network.
    
    Agents are represented as nodes with:
    - Size proportional to reputation
    - Color based on reputation level
    - Edges connecting agents with similar reputations
    
    Args:
        agents: Dictionary mapping agent names to reputation values
    
    Returns:
        NetworkX Graph object with styled nodes and edges
    """
    G = nx.Graph()
    
    # Add nodes for each agent
    for agent_name, reputation in agents.items():
        # Normalize reputation for sizing (0-200 scale -> 10-50 node size)
        node_size = 10 + (reputation / 200) * 40
        
        # Determine color based on reputation level
        color = _get_reputation_color(reputation)
        
        # Add node with attributes
        G.add_node(
            agent_name,
            reputation=reputation,
            size=node_size,
            color=color,
            title=f"{agent_name}<br>Reputation: {reputation:.1f}"  # Tooltip for PyVis
        )
    
    # Create edges between agents
    # Strategy: connect agents to form a network where highly reputed agents
    # are more central, and similar-reputation agents are clustered
    agent_list = list(agents.items())
    
    # Connect each agent to 2-4 others based on reputation similarity
    for i, (agent_name, reputation) in enumerate(agent_list):
        # Find agents with similar reputation
        similar_agents = []
        for j, (other_name, other_rep) in enumerate(agent_list):
            if i != j:
                rep_diff = abs(reputation - other_rep)
                similar_agents.append((other_name, rep_diff))
        
        # Sort by reputation similarity and connect to closest ones
        similar_agents.sort(key=lambda x: x[1])
        num_connections = min(3, len(similar_agents))
        
        for other_name, _ in similar_agents[:num_connections]:
            if not G.has_edge(agent_name, other_name):
                # Edge weight based on combined reputation
                weight = (reputation + agents[other_name]) / 200
                G.add_edge(agent_name, other_name, weight=weight)
    
    # Ensure graph is connected (add edges if needed)
    if len(agents) > 1 and not nx.is_connected(G):
        components = list(nx.connected_components(G))
        for i in range(len(components) - 1):
            node1 = list(components[i])[0]
            node2 = list(components[i + 1])[0]
            G.add_edge(node1, node2)
    
    return G


def _get_reputation_color(reputation: float) -> str:
    """
    Map reputation value to a color code.
    
    Args:
        reputation: Reputation value (0-200 scale)
    
    Returns:
        Hex color string
    """
    # Normalize reputation to 0-1 range
    normalized = max(0, min(1, reputation / 200))
    
    # Use a colormap (red -> yellow -> green)
    # Low reputation = red, medium = yellow, high = green
    if normalized < 0.25:
        # Red zone (0-50)
        return '#E74C3C'
    elif normalized < 0.5:
        # Orange zone (50-100)
        return '#E67E22'
    elif normalized < 0.75:
        # Yellow zone (100-150)
        return '#F39C12'
    else:
        # Green zone (150-200)
        return '#27AE60'


def render_pyvis_graph(nx_graph: nx.Graph, height: str = "600px", 
                       width: str = "100%", stabilize: bool = True) -> str:
    """
    Convert NetworkX graph to interactive PyVis visualization.
    
    Args:
        nx_graph: NetworkX graph object with agent nodes
        height: Height of the visualization
        width: Width of the visualization
        stabilize: Whether to enable physics stabilization (slower but smoother)
    
    Returns:
        HTML string containing the interactive graph
    """
    # Create PyVis network
    net = Network(
        height=height,
        width=width,
        bgcolor="#222222",
        font_color="white",
        notebook=False,
        directed=False
    )
    
    # Configure physics - reduced iterations for faster rendering during simulation
    stabilization_iterations = 100 if stabilize else 20
    physics_enabled = "true" if stabilize else "false"
    
    net.set_options(f"""
    {{
        "physics": {{
            "enabled": {physics_enabled},
            "barnesHut": {{
                "gravitationalConstant": -30000,
                "centralGravity": 0.3,
                "springLength": 150,
                "springConstant": 0.04,
                "damping": 0.15,
                "avoidOverlap": 0.5
            }},
            "maxVelocity": 50,
            "minVelocity": 0.75,
            "solver": "barnesHut",
            "stabilization": {{
                "enabled": true,
                "iterations": {stabilization_iterations},
                "updateInterval": 10,
                "fit": true
            }}
        }},
        "nodes": {{
            "font": {{
                "size": 16,
                "color": "white"
            }},
            "borderWidth": 2,
            "borderWidthSelected": 4
        }},
        "edges": {{
            "color": {{
                "color": "#848484",
                "highlight": "#00FF00"
            }},
            "smooth": {{
                "enabled": true,
                "type": "continuous"
            }}
        }},
        "interaction": {{
            "hover": true,
            "tooltipDelay": 100,
            "zoomView": true,
            "dragNodes": true
        }},
        "layout": {{
            "improvedLayout": true
        }}
    }}
    """)
    
    # Add nodes from NetworkX graph
    for node, attrs in nx_graph.nodes(data=True):
        net.add_node(
            node,
            label=node,
            color=attrs.get('color', '#3498DB'),
            size=attrs.get('size', 20),
            title=attrs.get('title', node),
            borderWidth=2
        )
    
    # Add edges from NetworkX graph
    for source, target, attrs in nx_graph.edges(data=True):
        weight = attrs.get('weight', 1)
        net.add_edge(source, target, value=weight)
    
    # Generate HTML
    try:
        # Create a temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.html') as f:
            temp_path = f.name
        
        # Save to temporary file
        net.save_graph(temp_path)
        
        # Read the HTML content
        with open(temp_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Clean up temporary file
        os.unlink(temp_path)
        
        return html_content
    
    except Exception as e:
        # Fallback: return basic HTML with error message
        return f"""
        <html>
        <body style="background-color: #222222; color: white; text-align: center; padding: 50px;">
            <h3>Error rendering graph</h3>
            <p>{str(e)}</p>
        </body>
        </html>
        """


def create_reputation_legend() -> str:
    """
    Create an HTML legend explaining reputation color coding.
    
    Returns:
        HTML string with color legend
    """
    legend_html = """
    <div style="background-color: #2C3E50; padding: 15px; border-radius: 8px; margin: 10px 0;">
        <h4 style="color: white; margin-top: 0;">Reputation Color Legend</h4>
        <div style="display: flex; flex-direction: column; gap: 8px;">
            <div style="display: flex; align-items: center;">
                <span style="display: inline-block; width: 20px; height: 20px; 
                             background-color: #27AE60; border-radius: 50%; margin-right: 10px;"></span>
                <span style="color: white;">High (150-200): Excellent reputation</span>
            </div>
            <div style="display: flex; align-items: center;">
                <span style="display: inline-block; width: 20px; height: 20px; 
                             background-color: #F39C12; border-radius: 50%; margin-right: 10px;"></span>
                <span style="color: white;">Good (100-150): Above average</span>
            </div>
            <div style="display: flex; align-items: center;">
                <span style="display: inline-block; width: 20px; height: 20px; 
                             background-color: #E67E22; border-radius: 50%; margin-right: 10px;"></span>
                <span style="color: white;">Medium (50-100): Average reputation</span>
            </div>
            <div style="display: flex; align-items: center;">
                <span style="display: inline-block; width: 20px; height: 20px; 
                             background-color: #E74C3C; border-radius: 50%; margin-right: 10px;"></span>
                <span style="color: white;">Low (0-50): Needs improvement</span>
            </div>
        </div>
    </div>
    """
    return legend_html


def get_network_statistics(nx_graph: nx.Graph) -> Dict[str, any]:
    """
    Calculate network topology statistics.
    
    Args:
        nx_graph: NetworkX graph object
    
    Returns:
        Dictionary with network metrics
    """
    stats = {}
    
    if len(nx_graph.nodes()) == 0:
        return stats
    
    stats['num_nodes'] = nx_graph.number_of_nodes()
    stats['num_edges'] = nx_graph.number_of_edges()
    
    if nx_graph.number_of_edges() > 0:
        stats['avg_degree'] = sum(dict(nx_graph.degree()).values()) / nx_graph.number_of_nodes()
        stats['density'] = nx.density(nx_graph)
        
        if nx.is_connected(nx_graph):
            stats['avg_path_length'] = nx.average_shortest_path_length(nx_graph)
            stats['diameter'] = nx.diameter(nx_graph)
        else:
            stats['avg_path_length'] = None
            stats['diameter'] = None
    
    return stats





