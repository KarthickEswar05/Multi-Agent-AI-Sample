# Multi-Agent AI System

A trendy agentic AI framework where multiple specialized agents collaborate autonomously to solve complex objectives.

## 🎯 Key Features

### Multi-Agent Architecture
- **Planner Agent**: Breaks down objectives into structured subtasks
- **Researcher Agent**: Gathers information and performs analysis
- **Executor Agent**: Executes tasks using available tools
- **Critic Agent**: Reviews results and provides constructive feedback

### Real-Time Trending Concepts
1. **Agent Collaboration** - Agents work together toward common goals
2. **Tool Calling** - Agents can invoke functions/tools (web search, calculations, summarization)
3. **Memory & Context** - Agents maintain conversation history and task state
4. **Orchestration** - Central orchestrator coordinates agent workflows
5. **Real-Time Monitoring** - Live UI showing agent status and messages

### Agent Communication Flow
```
Objective Input
    ↓
Planner (creates tasks)
    ↓
Researcher (gathers info)
    ↓
Executor (performs work)
    ↓
Critic (validates output)
    ↓
Results
```

## 🚀 Setup

1. Create virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set OpenAI API key:
```bash
export OPENAI_API_KEY="your_api_key_here"
```

4. Run the app:
```bash
python app.py
```

5. Open `http://127.0.0.1:5000`

## 💡 How It Works

1. **Submit an objective** in the UI (e.g., "Analyze trends and create summary")
2. **Planner** agent breaks it into tasks
3. **Researcher** agent gathers information
4. **Executor** agent performs tasks using tools
5. **Critic** agent reviews the work
6. **UI displays** real-time agent status, execution logs, and final results

## 🔧 Available Agent Tools

- `web_search` - Search for information (simulated)
- `calculate` - Perform mathematical operations
- `summarize` - Summarize text content
- `get_info` - Get current system information

## 📊 Why This Is Trending (2026)

- **Autonomous Agents** - AI systems that work independently with minimal supervision
- **Function Calling** - Agents can invoke tools and APIs dynamically
- **Multi-Agent Systems** - Collaborative AI solving complex problems
- **AI Orchestration** - Managing multiple AI models working together
- **Real-Time Reasoning** - Agents think, plan, and act in real-time
