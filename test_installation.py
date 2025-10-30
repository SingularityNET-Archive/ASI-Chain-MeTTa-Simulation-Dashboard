#!/usr/bin/env python3
"""
Installation Test Script for ASI Chain Dashboard

Run this script to verify that all dependencies are correctly installed
and the basic simulation functionality works.

Usage:
    python test_installation.py
"""

import sys


def test_imports():
    """Test that all required packages can be imported."""
    print("Testing package imports...")
    
    packages = [
        ('streamlit', 'Streamlit web framework'),
        ('hyperon', 'MeTTa/Hyperon runtime'),
        ('networkx', 'NetworkX graph library'),
        ('pyvis', 'PyVis visualization'),
        ('matplotlib', 'Matplotlib plotting'),
        ('pandas', 'Pandas data handling')
    ]
    
    failed = []
    
    for package, description in packages:
        try:
            __import__(package)
            print(f"  ✓ {package:15} - {description}")
        except ImportError as e:
            print(f"  ✗ {package:15} - {description} - FAILED")
            failed.append((package, str(e)))
    
    if failed:
        print("\n❌ Some packages failed to import:")
        for package, error in failed:
            print(f"   - {package}: {error}")
        return False
    
    print("\n✅ All packages imported successfully!")
    return True


def test_simulation():
    """Test basic simulation functionality."""
    print("\nTesting simulation logic...")
    
    try:
        try:
            from agent_sim import AgentSimulation
            print("  ✓ Using full hyperon-based simulation")
        except ImportError:
            from agent_sim_simple import AgentSimulation
            print("  ✓ Using simplified simulation (hyperon not installed)")
        
        # Create a small simulation
        print("  - Creating simulation with 3 agents...")
        sim = AgentSimulation(num_agents=3)
        
        # Run a few steps
        print("  - Running 5 simulation steps...")
        for i in range(5):
            result = sim.step()
            print(f"    Step {i+1}: Agent {result['agent']} performed {result['action']}")
        
        # Get health score
        health = sim.get_health_score()
        print(f"  - Final health score: {health:.2f}")
        
        # Get agent states
        states = sim.get_agent_states()
        print(f"  - Agent count: {len(states)}")
        
        print("\n✅ Simulation logic works correctly!")
        return True
    
    except Exception as e:
        print(f"\n❌ Simulation test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_visualizer():
    """Test visualization functionality."""
    print("\nTesting visualization...")
    
    try:
        from visualizer import create_agent_graph, render_pyvis_graph
        
        # Create dummy agent data
        agents = {
            'Agent_0': 100.0,
            'Agent_1': 75.0,
            'Agent_2': 125.0
        }
        
        print("  - Creating NetworkX graph...")
        nx_graph = create_agent_graph(agents)
        print(f"    Nodes: {nx_graph.number_of_nodes()}")
        print(f"    Edges: {nx_graph.number_of_edges()}")
        
        print("  - Rendering PyVis graph...")
        html = render_pyvis_graph(nx_graph)
        print(f"    HTML length: {len(html)} characters")
        
        if len(html) < 100:
            raise ValueError("Generated HTML is too short")
        
        print("\n✅ Visualization works correctly!")
        return True
    
    except Exception as e:
        print(f"\n❌ Visualization test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("ASI Chain Dashboard - Installation Test")
    print("=" * 60)
    print()
    
    results = []
    
    # Test imports
    results.append(("Package Imports", test_imports()))
    
    # Test simulation
    results.append(("Simulation Logic", test_simulation()))
    
    # Test visualizer
    results.append(("Visualization", test_visualizer()))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    all_passed = True
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name:20} - {status}")
        if not passed:
            all_passed = False
    
    print("=" * 60)
    
    if all_passed:
        print("\n🎉 All tests passed! Your installation is ready.")
        print("\nNext steps:")
        print("  1. Run: streamlit run app.py")
        print("  2. Open the dashboard in your browser")
        print("  3. Start simulating!")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
        print("\nTroubleshooting:")
        print("  1. Make sure you ran: pip install -r requirements.txt")
        print("  2. Check that you're using Python 3.8 or higher")
        print("  3. Try installing hyperon from source if needed")
        return 1


if __name__ == "__main__":
    sys.exit(main())


