# Contributing to ASI Chain Dashboard

Thank you for your interest in contributing to the ASI Chain Agent Simulation Dashboard! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### Reporting Bugs

If you find a bug, please open an issue on GitHub with:

- A clear, descriptive title
- Steps to reproduce the issue
- Expected behavior vs actual behavior
- Your environment (Python version, OS, package versions)
- Screenshots if applicable

### Suggesting Enhancements

We welcome feature requests! Please open an issue with:

- A clear description of the enhancement
- Use cases and benefits
- Any implementation ideas you have

### Pull Requests

1. **Fork the repository** and create your branch from `main`
   ```bash
   git checkout -b feature/amazing-feature
   ```

2. **Make your changes**
   - Follow the existing code style
   - Add comments for complex logic
   - Update documentation if needed

3. **Test your changes**
   ```bash
   python test_installation.py
   streamlit run app.py
   ```

4. **Commit your changes**
   ```bash
   git commit -m "Add amazing feature"
   ```

5. **Push to your fork**
   ```bash
   git push origin feature/amazing-feature
   ```

6. **Open a Pull Request** on GitHub

## 📝 Code Style Guidelines

### Python Code

- Follow PEP 8 style guide
- Use type hints where appropriate
- Write docstrings for functions and classes
- Keep functions focused and modular
- Maximum line length: 100 characters

Example:
```python
def calculate_health_score(agents: Dict[str, float]) -> float:
    """
    Calculate the average reputation across all agents.
    
    Args:
        agents: Dictionary mapping agent names to reputation values
    
    Returns:
        Average reputation score (0-200 scale)
    """
    if not agents:
        return 0.0
    return sum(agents.values()) / len(agents)
```

### MeTTa Code

- Use clear variable names with `$` prefix
- Comment complex rules
- Keep rules focused on single concerns

Example:
```metta
; Rule: Contribute action increases reputation significantly
; Agents who contribute actively earn higher standing
(= (action-contribute $agent)
   (update-reputation $agent 15))
```

### Streamlit UI

- Use semantic HTML when possible
- Maintain consistent spacing and layout
- Add helpful tooltips and descriptions
- Test on different screen sizes

## 🧪 Testing

Before submitting a PR, ensure:

1. **Installation test passes**
   ```bash
   python test_installation.py
   ```

2. **App runs without errors**
   ```bash
   streamlit run app.py
   ```

3. **All features work**
   - Run simulation with various parameters
   - Test stop/reset functionality
   - Verify graph visualization renders

4. **No linter errors**
   ```bash
   pylint agent_sim.py visualizer.py app.py
   ```

## 🎯 Areas for Contribution

### Priority Areas

1. **Multi-Shard Simulation**
   - Implement separate spaces for reputation, data, compute
   - Add shard visualization and metrics

2. **Export Functionality**
   - Save/load simulation state
   - Export graphs as images
   - Generate reports

3. **Advanced Metrics**
   - Network centrality measures
   - Reputation dynamics analysis
   - Emergent pattern detection

4. **Agent Profiles**
   - Individual agent dashboards
   - Action history per agent
   - Personality traits

5. **Enhanced Visualization**
   - 3D graph rendering
   - Time-series animations
   - Comparative views

### Good First Issues

- Add new agent actions
- Improve UI styling
- Add more color schemes
- Write additional tests
- Improve documentation
- Add keyboard shortcuts

## 🐛 Known Issues

Check the [GitHub Issues](https://github.com/yourusername/ASI-Chain-MeTTa-Simulation-Dashboard/issues) page for current known issues and planned improvements.

## 📚 Resources

### MeTTa/Hyperon
- [Hyperon GitHub](https://github.com/trueagi-io/hyperon-experimental)
- [MeTTa Documentation](https://wiki.opencog.org/w/MeTTa)

### Streamlit
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Streamlit Community](https://discuss.streamlit.io/)

### NetworkX & PyVis
- [NetworkX Documentation](https://networkx.org/documentation/stable/)
- [PyVis Documentation](https://pyvis.readthedocs.io/)

## 💬 Community

- **GitHub Discussions**: Ask questions and share ideas
- **Issues**: Report bugs and request features
- **Pull Requests**: Submit your contributions

## 📜 Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inspiring community for all. Please be respectful and constructive in your interactions.

### Expected Behavior

- Be respectful and inclusive
- Welcome newcomers
- Accept constructive criticism gracefully
- Focus on what's best for the community
- Show empathy towards others

### Unacceptable Behavior

- Harassment or discriminatory language
- Trolling or insulting comments
- Personal or political attacks
- Publishing others' private information

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🙏 Recognition

Contributors will be acknowledged in the README and release notes. Thank you for helping make this project better!

---

Questions? Open an issue or reach out to the maintainers.

**Happy Contributing!** 🚀





