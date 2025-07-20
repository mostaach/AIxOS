#!/bin/bash

# AIxOS Setup Script
# This script helps you set up AIxOS with Docker for safety, isolation, portability, and resource management

set -e  # Exit on any error

echo "🚀 AIxOS Setup Script"
echo "==================="
echo "Setting up AI-Powered Operating System with Docker..."
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first:"
    echo "   https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is available
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose is not available. Please install Docker Compose:"
    echo "   https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✅ Docker and Docker Compose are available"
echo ""

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p data logs config
echo "✅ Directories created"
echo ""

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "✅ .env file created. Please edit it with your configuration."
    echo ""
    echo "⚠️  IMPORTANT: You need to add your OpenAI API key to the .env file!"
    echo "   Edit .env and set OPENAI_API_KEY=your_actual_api_key"
    echo ""
else
    echo "✅ .env file already exists"
fi

# Function to prompt for API key
prompt_api_key() {
    echo "🔑 OpenAI API Key Setup"
    echo "To use AIxOS, you need an OpenAI API key."
    echo "You can get one from: https://platform.openai.com/api-keys"
    echo ""
    read -p "Enter your OpenAI API key (or press Enter to skip): " api_key
    
    if [ ! -z "$api_key" ]; then
        # Update the .env file with the API key
        if [[ "$OSTYPE" == "darwin"* ]]; then
            # macOS
            sed -i '' "s/OPENAI_API_KEY=.*/OPENAI_API_KEY=$api_key/" .env
        else
            # Linux
            sed -i "s/OPENAI_API_KEY=.*/OPENAI_API_KEY=$api_key/" .env
        fi
        echo "✅ API key added to .env file"
    else
        echo "⚠️  Skipped API key setup. You can add it later to the .env file."
    fi
    echo ""
}

# Check if API key is set
if grep -q "OPENAI_API_KEY=your_openai_api_key_here" .env || grep -q "OPENAI_API_KEY=$" .env; then
    prompt_api_key
fi

# Build the Docker image
echo "🔨 Building AIxOS Docker image..."
docker build -t aixos:latest --target production .
echo "✅ Docker image built successfully"
echo ""

# Create a simple start script
echo "📜 Creating start script..."
cat > start-aixos.sh << 'EOF'
#!/bin/bash
# AIxOS Start Script

echo "🚀 Starting AIxOS..."
echo "Press Ctrl+C to exit"
echo ""

# Start AIxOS with Docker Compose
docker-compose up aixos
EOF

chmod +x start-aixos.sh
echo "✅ Start script created (start-aixos.sh)"
echo ""

# Create a development start script
echo "📜 Creating development start script..."
cat > start-aixos-dev.sh << 'EOF'
#!/bin/bash
# AIxOS Development Start Script

echo "🛠️  Starting AIxOS in development mode..."
echo "This will give you a bash shell inside the container"
echo ""

# Build development image
docker build -t aixos:dev --target development .

# Start development environment
docker-compose --profile dev up -d aixos-dev
docker-compose exec aixos-dev /bin/bash
EOF

chmod +x start-aixos-dev.sh
echo "✅ Development start script created (start-aixos-dev.sh)"
echo ""

echo "🎉 AIxOS Setup Complete!"
echo "======================"
echo ""
echo "Next steps:"
echo "1. Make sure your OpenAI API key is set in the .env file"
echo "2. Run './start-aixos.sh' to start AIxOS"
echo "3. Or run './start-aixos-dev.sh' for development mode"
echo ""
echo "Available commands:"
echo "  ./start-aixos.sh          - Start AIxOS in production mode"
echo "  ./start-aixos-dev.sh      - Start AIxOS in development mode"
echo "  docker-compose up         - Start all services"
echo "  docker-compose down       - Stop all services"
echo "  docker-compose logs       - View logs"
echo ""
echo "For more information, see the README.md file."
echo ""
echo "🐳 Docker benefits for AIxOS:"
echo "  ✅ Safety: Isolated environment prevents system damage"
echo "  ✅ Isolation: Commands run in contained environment"
echo "  ✅ Portability: Works the same on any system with Docker"
echo "  ✅ Reproducibility: Consistent environment every time"
echo "  ✅ Resource Management: CPU and memory limits enforced"
echo ""
echo "Happy coding with AIxOS! 🤖"