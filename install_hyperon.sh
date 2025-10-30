#!/bin/bash

# Installation script for full hyperon/MeTTa support
# This script will:
# 1. Check if Conan is installed
# 2. Install Conan via Homebrew if needed
# 3. Create Conan profile
# 4. Install hyperon from GitHub

set -e  # Exit on error

echo "================================================"
echo "Hyperon Installation Script"
echo "================================================"
echo ""

# Check if we're in a virtual environment
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo "⚠️  Warning: Not in a virtual environment"
    echo "   Please activate your venv first:"
    echo "   source venv/bin/activate"
    echo ""
    exit 1
fi

echo "✓ Virtual environment detected: $VIRTUAL_ENV"
echo ""

# Check if Conan is installed
if ! command -v conan &> /dev/null; then
    echo "📦 Conan not found. Installing via Homebrew..."
    
    # Check if Homebrew is installed
    if ! command -v brew &> /dev/null; then
        echo "❌ Homebrew not found. Please install it first:"
        echo "   /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
        exit 1
    fi
    
    # Install Conan
    echo "Installing Conan..."
    brew install conan
    
    if [ $? -ne 0 ]; then
        echo ""
        echo "❌ Failed to install Conan via Homebrew"
        echo ""
        echo "This might be due to permission issues. Try running:"
        echo "sudo chown -R $(whoami) /opt/homebrew /Users/$(whoami)/Library/Caches/Homebrew /Users/$(whoami)/Library/Logs/Homebrew"
        echo ""
        exit 1
    fi
else
    echo "✓ Conan is already installed"
fi

echo ""

# Create Conan profile if it doesn't exist
if [ ! -f "$HOME/.conan2/profiles/default" ]; then
    echo "🔧 Creating Conan default profile..."
    conan profile detect
    echo "✓ Conan profile created"
else
    echo "✓ Conan profile already exists"
fi

echo ""
echo "📥 Installing hyperon from GitHub..."
echo "⏱️  This will take 5-10 minutes (compiling Rust/C++ components)..."
echo ""

# Install hyperon
pip install git+https://github.com/trueagi-io/hyperon-experimental.git#subdirectory=python

if [ $? -eq 0 ]; then
    echo ""
    echo "================================================"
    echo "✅ Hyperon installed successfully!"
    echo "================================================"
    echo ""
    echo "Next steps:"
    echo "1. Test installation: python test_installation.py"
    echo "2. Run the dashboard: streamlit run app.py"
    echo ""
else
    echo ""
    echo "================================================"
    echo "❌ Hyperon installation failed"
    echo "================================================"
    echo ""
    echo "The app can still run with the simplified version."
    echo "Just run: streamlit run app.py"
    echo ""
    echo "The app will automatically use agent_sim_simple.py"
    echo "which provides the same functionality without hyperon."
    echo ""
    exit 1
fi




