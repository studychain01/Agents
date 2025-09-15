# Installation Instructions

## System Dependencies

Before installing Python packages, you need to install system-level dependencies for graph visualization:

### macOS (using Homebrew)
```bash
brew install graphviz pkg-config
```

### Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install python3-dev libgraphviz-dev pkg-config graphviz
```

### CentOS/RHEL/Fedora
```bash
# For CentOS/RHEL
sudo yum install python3-devel graphviz-devel pkgconfig graphviz

# For Fedora
sudo dnf install python3-devel graphviz-devel pkgconfig graphviz
```

## Python Dependencies

After installing system dependencies, install Python packages:

```bash
# Create and activate virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt
```

## Environment Setup

Create a `.env` file in the project root with your API keys:

```bash
OPENAI_API_KEY=your_openai_api_key_here
```
