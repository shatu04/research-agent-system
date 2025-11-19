# Setup & Deployment Guide

## Quick Start (5 Minutes)

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

```bash
# Clone or download the project
git clone <your-repo-url>
cd research-agent-system

# No external dependencies needed! Uses Python standard library
python research_agent.py
```

That's it! The system uses only Python's standard library, so no pip installs required.

---

## Project Files

### Core Files
```
research-agent-system/
├── research_agent.py          # Main agent system (all code)
├── README.md                  # Documentation
├── VALUE_ANALYSIS.md          # Impact & metrics writeup
├── requirements.txt           # Dependencies (empty - stdlib only!)
└── .gitignore                # Git ignore file
```

### Generated Files (after running)
```
├── agent_traces.log          # Execution logs
└── research_agent_traces.json # Exported trace data
```

---

## Running the Demo

### Basic Demo
```bash
python research_agent.py
```

**Expected Output:**
```
============================================================
INTELLIGENT RESEARCH ASSISTANT AGENT SYSTEM
============================================================

🔍 Starting research queries...

Query: artificial intelligence latest trends 2024
✓ Synthesis: Based on 15 sources, the key insights are:...
  Sources: 15
------------------------------------------------------------
Query: climate change mitigation strategies
✓ Synthesis: Based on 15 sources, the key insights are:...
  Sources: 15
------------------------------------------------------------
Query: quantum computing applications
✓ Synthesis: Based on 15 sources, the key insights are:...
  Sources: 15
------------------------------------------------------------

📊 Performance Evaluation:

  session_id: demo_session_001
  total_queries: 3
  total_tasks_completed: 9
  total_time_seconds: 7.5
  avg_time_per_query: 2.5
  memory_entries: 3

✓ Traces exported to: research_agent_traces.json

============================================================
Demo completed successfully!
============================================================
```

---

## Custom Usage

### Python Script
```python
from research_agent import ResearchAgentSystem, AgentEvaluator

# Initialize
system = ResearchAgentSystem()
session_id = system.session_service.create_session("my_session")

# Research
result = system.research("machine learning applications", session_id)
print(result["synthesis"])

# Evaluate
evaluator = AgentEvaluator(system.logger)
metrics = evaluator.evaluate_session(system, session_id)
print(metrics)
```

### Interactive Python Console
```python
>>> from research_agent import ResearchAgentSystem
>>> system = ResearchAgentSystem()
>>> session_id = "interactive_session"
>>> system.session_service.create_session(session_id)
'interactive_session'
>>> result = system.research("quantum computing", session_id)
>>> print(result["synthesis"])
```

---

## Integration Options

### 1. REST API (Flask)

```python
# api_server.py
from flask import Flask, request, jsonify
from research_agent import ResearchAgentSystem

app = Flask(__name__)
system = ResearchAgentSystem()

@app.route('/research', methods=['POST'])
def research_endpoint():
    data = request.json
    query = data.get('query')
    session_id = data.get('session_id', 'default')
    
    result = system.research(query, session_id)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
```

```bash
# Install Flask
pip install flask

# Run server
python api_server.py

# Make requests
curl -X POST http://localhost:5000/research \
  -H "Content-Type: application/json" \
  -d '{"query": "AI trends", "session_id": "user123"}'
```

### 2. CLI Tool

```python
# cli.py
import sys
from research_agent import ResearchAgentSystem

def main():
    if len(sys.argv) < 2:
        print("Usage: python cli.py 'your research query'")
        return
    
    query = sys.argv[1]
    system = ResearchAgentSystem()
    result = system.research(query)
    print(result["synthesis"])

if __name__ == "__main__":
    main()
```

```bash
python cli.py "machine learning trends 2024"
```

### 3. Jupyter Notebook

```python
# In Jupyter cell
from research_agent import ResearchAgentSystem

system = ResearchAgentSystem()
session_id = system.session_service.create_session("notebook_session")

queries = [
    "neural networks",
    "deep learning applications",
    "transformer models"
]

for query in queries:
    result = system.research(query, session_id)
    print(f"\n{'='*60}")
    print(f"Query: {query}")
    print(f"{'='*60}")
    print(result["synthesis"])
```

---

## Configuration

### Customize Search Results
```python
# In WebSearchTool.__init__
self.default_results = 10  # Change from 5 to 10
```

### Adjust Context Window
```python
# In InMemorySessionService.get_context_summary
for i, ctx in enumerate(history[-5:], 1):  # Change from -3 to -5
    summary += f"{i}. {ctx.query}: {ctx.synthesis[:200]}...\n"
```

### Enable Debug Logging
```python
# In AgentLogger.__init__
logging.basicConfig(
    level=logging.DEBUG,  # Change from INFO to DEBUG
    ...
)
```

---

## Testing

### Unit Tests (Optional)

```python
# tests/test_agents.py
import unittest
from research_agent import ResearchAgentSystem

class TestResearchAgent(unittest.TestCase):
    def setUp(self):
        self.system = ResearchAgentSystem()
        self.session_id = "test_session"
        self.system.session_service.create_session(self.session_id)
    
    def test_research_completion(self):
        result = self.system.research("test query", self.session_id)
        self.assertIn("synthesis", result)
        self.assertGreater(result["sources_count"], 0)
    
    def test_session_memory(self):
        self.system.research("first query", self.session_id)
        self.system.research("second query", self.session_id)
        history = self.system.session_service.get_session_history(self.session_id)
        self.assertEqual(len(history), 2)

if __name__ == '__main__':
    unittest.main()
```

```bash
python -m unittest tests/test_agents.py
```

---

## Production Deployment

### Docker Container

```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY research_agent.py .

CMD ["python", "research_agent.py"]
```

```bash
docker build -t research-agent .
docker run research-agent
```

### AWS Lambda

```python
# lambda_handler.py
import json
from research_agent import ResearchAgentSystem

system = ResearchAgentSystem()

def lambda_handler(event, context):
    query = event.get('query')
    session_id = event.get('session_id', 'lambda_session')
    
    result = system.research(query, session_id)
    
    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }
```

### Cloud Functions (GCP)

```python
# main.py
from research_agent import ResearchAgentSystem

system = ResearchAgentSystem()

def research_function(request):
    request_json = request.get_json()
    query = request_json.get('query')
    result = system.research(query)
    return result
```

---

## Troubleshooting

### Issue: Module not found
**Solution**: Ensure you're in the correct directory
```bash
cd research-agent-system
python research_agent.py
```

### Issue: Permission denied on log file
**Solution**: Run with appropriate permissions or change log location
```python
# In AgentLogger.__init__
self.log_file = "/tmp/agent_traces.log"  # Use temp directory
```

### Issue: Memory usage high
**Solution**: Implement session cleanup
```python
# Add to InMemorySessionService
def clear_old_sessions(self, max_age_hours=24):
    # Implementation to remove old sessions
    pass
```

---

## Performance Optimization

### For High-Volume Usage

```python
# Enable caching
class CachedSearchTool(WebSearchTool):
    def __init__(self, logger):
        super().__init__(logger)
        self.cache = {}
    
    def search(self, query, num_results=5):
        if query in self.cache:
            return self.cache[query]
        results = super().search(query, num_results)
        self.cache[query] = results
        return results
```

### Parallel Processing

```python
import asyncio

async def parallel_research(queries):
    system = ResearchAgentSystem()
    tasks = [system.research(q) for q in queries]
    return await asyncio.gather(*tasks)
```

---

## Monitoring & Metrics

### Export Metrics to JSON
```python
# After running research
system.logger.export_traces("metrics.json")

# Analyze with any JSON tool
import json
with open("metrics.json") as f:
    metrics = json.load(f)
    print(f"Total agent actions: {len(metrics)}")
```

### Visualize Performance
```python
import matplotlib.pyplot as plt

traces = system.logger.get_traces()
durations = [t["details"].get("duration_seconds", 0) for t in traces]

plt.hist(durations, bins=20)
plt.xlabel("Duration (seconds)")
plt.ylabel("Frequency")
plt.title("Agent Task Duration Distribution")
plt.show()
```

---

## Support & Contribution

### Reporting Issues
- Check existing logs: `agent_traces.log`
- Include trace exports: `research_agent_traces.json`
- Describe expected vs actual behavior

### Contributing
1. Fork the repository
2. Create feature branch
3. Add tests for new features
4. Submit pull request

---

## Next Steps

1. ✅ **Run the demo**: `python research_agent.py`
2. 📝 **Read the documentation**: Review README.md
3. 🔧 **Customize**: Modify for your use case
4. 🚀 **Deploy**: Choose deployment option
5. 📊 **Monitor**: Use built-in observability

---

## Quick Reference

| Command | Purpose |
|---------|---------|
| `python research_agent.py` | Run demo |
| `system.research(query, session_id)` | Execute research |
| `system.logger.get_traces()` | View all traces |
| `system.logger.export_traces()` | Export to JSON |
| `evaluator.evaluate_session()` | Get metrics |

---

**Ready to start?** Run `python research_agent.py` now! 🚀
