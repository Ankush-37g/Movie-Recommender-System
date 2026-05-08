#!/bin/bash

echo "🎬 Movie Recommender System - Setup"
echo "===================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"
echo ""

# Install requirements
echo "📦 Installing dependencies..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully!"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo ""
echo "📥 Downloading NLTK data..."
python3 -c "import nltk; nltk.download('punkt')"

echo ""
echo "✅ Setup complete!"
echo ""
echo "🚀 To run the app, use:"
echo "   streamlit run app.py"
echo ""
