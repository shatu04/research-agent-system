"""
Intelligent Research Assistant Agent System
A multi-agent system for autonomous research with memory and observability

Features:
- Multi-agent architecture (Coordinator, Researcher, Synthesizer)
- Web search tool integration
- Session memory for context retention
- Comprehensive logging and tracing
- Agent evaluation framework
"""

import json
import logging
import time
from datetime import datetime
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum


# ==================== OBSERVABILITY ====================

class LogLevel(Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    DEBUG = "DEBUG"


class AgentLogger:
    """Centralized logging and tracing for all agents"""
    
    def __init__(self, log_file: str = "agent_traces.log"):
        self.log_file = log_file
        self.traces = []
        
        # Setup file logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger("ResearchAgent")
    
    def log(self, agent_name: str, action: str, details: Dict[str, Any], level: LogLevel = LogLevel.INFO):
        """Log agent actions with full tracing"""
        trace_entry = {
            "timestamp": datetime.now().isoformat(),
            "agent": agent_name,
            "action": action,
            "details": details
        }
        self.traces.append(trace_entry)
        
        log_message = f"[{agent_name}] {action}: {json.dumps(details)}"
        
        if level == LogLevel.INFO:
            self.logger.info(log_message)
        elif level == LogLevel.WARNING:
            self.logger.warning(log_message)
        elif level == LogLevel.ERROR:
            self.logger.error(log_message)
        elif level == LogLevel.DEBUG:
            self.logger.debug(log_message)
    
    def get_traces(self) -> List[Dict[str, Any]]:
        """Retrieve all traces for analysis"""
        return self.traces
    
    def export_traces(self, filename: str = "trace_export.json"):
        """Export traces to JSON file"""
        with open(filename, 'w') as f:
            json.dump(self.traces, f, indent=2)


# ==================== MEMORY & SESSIONS ====================

@dataclass
class ResearchContext:
    """Context object for research sessions"""
    query: str
    sources: List[str]
    findings: List[str]
    synthesis: str
    timestamp: str


class InMemorySessionService:
    """Session management with context retention"""
    
    def __init__(self):
        self.sessions: Dict[str, List[ResearchContext]] = {}
        self.current_session_id: Optional[str] = None
    
    def create_session(self, session_id: str) -> str:
        """Create a new research session"""
        self.sessions[session_id] = []
        self.current_session_id = session_id
        return session_id
    
    def add_to_session(self, session_id: str, context: ResearchContext):
        """Add research context to session"""
        if session_id not in self.sessions:
            self.create_session(session_id)
        self.sessions[session_id].append(context)
    
    def get_session_history(self, session_id: str) -> List[ResearchContext]:
        """Retrieve full session history"""
        return self.sessions.get(session_id, [])
    
    def get_context_summary(self, session_id: str) -> str:
        """Generate summary of session for context compaction"""
        history = self.get_session_history(session_id)
        if not history:
            return "No previous research in this session."
        
        summary = f"Previous research in this session ({len(history)} queries):\n"
        for i, ctx in enumerate(history[-3:], 1):  # Last 3 for context compaction
            summary += f"{i}. {ctx.query}: {ctx.synthesis[:100]}...\n"
        return summary


class MemoryBank:
    """Long-term memory across sessions"""
    
    def __init__(self):
        self.knowledge_base: Dict[str, Any] = {}
        self.research_patterns: List[str] = []
    
    def store_insight(self, topic: str, insight: str):
        """Store insights for long-term retrieval"""
        if topic not in self.knowledge_base:
            self.knowledge_base[topic] = []
        self.knowledge_base[topic].append({
            "insight": insight,
            "timestamp": datetime.now().isoformat()
        })
    
    def retrieve_insights(self, topic: str) -> List[str]:
        """Retrieve relevant insights from memory"""
        return [item["insight"] for item in self.knowledge_base.get(topic, [])]
    
    def add_research_pattern(self, pattern: str):
        """Learn from research patterns"""
        self.research_patterns.append(pattern)


# ==================== TOOLS ====================

class WebSearchTool:
    """Custom web search tool (simulated for demo)"""
    
    def __init__(self, logger: AgentLogger):
        self.logger = logger
    
    def search(self, query: str, num_results: int = 5) -> List[Dict[str, str]]:
        """Perform web search and return results"""
        self.logger.log("WebSearchTool", "search_initiated", {
            "query": query,
            "num_results": num_results
        })
        
        # In production, integrate with real search API
        # For demo, return structured mock results
        results = [
            {
                "title": f"Research Result {i+1} for: {query}",
                "url": f"https://example.com/result{i+1}",
                "snippet": f"This source provides information about {query}. Key findings include relevant data points and analysis."
            }
            for i in range(num_results)
        ]
        
        self.logger.log("WebSearchTool", "search_completed", {
            "results_count": len(results)
        })
        
        return results


class SynthesisTool:
    """Custom tool for synthesizing information"""
    
    def __init__(self, logger: AgentLogger):
        self.logger = logger
    
    def synthesize(self, findings: List[str]) -> str:
        """Synthesize multiple findings into coherent summary"""
        self.logger.log("SynthesisTool", "synthesis_started", {
            "findings_count": len(findings)
        })
        
        # In production, use LLM for synthesis
        synthesis = f"Based on {len(findings)} sources, the key insights are:\n"
        for i, finding in enumerate(findings[:3], 1):
            synthesis += f"{i}. {finding}\n"
        
        return synthesis


# ==================== AGENTS ====================

class BaseAgent:
    """Base agent class with common functionality"""
    
    def __init__(self, name: str, logger: AgentLogger):
        self.name = name
        self.logger = logger
        self.start_time = None
        self.end_time = None
    
    def _start_task(self, task_name: str):
        """Track task start"""
        self.start_time = time.time()
        self.logger.log(self.name, "task_started", {"task": task_name})
    
    def _end_task(self, task_name: str):
        """Track task completion"""
        self.end_time = time.time()
        duration = self.end_time - self.start_time
        self.logger.log(self.name, "task_completed", {
            "task": task_name,
            "duration_seconds": round(duration, 2)
        })


class CoordinatorAgent(BaseAgent):
    """Coordinates the research workflow"""
    
    def __init__(self, logger: AgentLogger, session_service: InMemorySessionService):
        super().__init__("CoordinatorAgent", logger)
        self.session_service = session_service
    
    def plan_research(self, query: str, session_id: str) -> Dict[str, Any]:
        """Plan the research strategy"""
        self._start_task("research_planning")
        
        # Get session context for informed planning
        context_summary = self.session_service.get_context_summary(session_id)
        
        plan = {
            "query": query,
            "search_queries": self._generate_search_queries(query),
            "num_sources": 5,
            "synthesis_required": True,
            "context": context_summary
        }
        
        self.logger.log(self.name, "research_plan_created", plan)
        self._end_task("research_planning")
        
        return plan
    
    def _generate_search_queries(self, query: str) -> List[str]:
        """Generate multiple search queries for comprehensive research"""
        # In production, use LLM to generate diverse queries
        return [
            query,
            f"{query} latest developments",
            f"{query} expert analysis"
        ]


class ResearcherAgent(BaseAgent):
    """Conducts research using tools"""
    
    def __init__(self, logger: AgentLogger, search_tool: WebSearchTool):
        super().__init__("ResearcherAgent", logger)
        self.search_tool = search_tool
    
    def conduct_research(self, plan: Dict[str, Any]) -> List[str]:
        """Execute research plan"""
        self._start_task("research_execution")
        
        findings = []
        for search_query in plan["search_queries"]:
            results = self.search_tool.search(search_query, plan["num_sources"])
            for result in results:
                findings.append(f"{result['title']}: {result['snippet']}")
        
        self.logger.log(self.name, "research_completed", {
            "findings_count": len(findings)
        })
        
        self._end_task("research_execution")
        return findings


class SynthesizerAgent(BaseAgent):
    """Synthesizes research findings"""
    
    def __init__(self, logger: AgentLogger, synthesis_tool: SynthesisTool, memory_bank: MemoryBank):
        super().__init__("SynthesizerAgent", logger)
        self.synthesis_tool = synthesis_tool
        self.memory_bank = memory_bank
    
    def synthesize(self, findings: List[str], query: str) -> str:
        """Synthesize findings into final output"""
        self._start_task("synthesis")
        
        # Retrieve relevant insights from memory
        past_insights = self.memory_bank.retrieve_insights(query)
        
        synthesis = self.synthesis_tool.synthesize(findings)
        
        if past_insights:
            synthesis += f"\nPrevious insights: {past_insights[0]}"
        
        # Store new insight
        self.memory_bank.store_insight(query, synthesis[:200])
        
        self.logger.log(self.name, "synthesis_completed", {
            "output_length": len(synthesis)
        })
        
        self._end_task("synthesis")
        return synthesis


# ==================== MULTI-AGENT ORCHESTRATION ====================

class ResearchAgentSystem:
    """Main system orchestrating all agents"""
    
    def __init__(self):
        self.logger = AgentLogger()
        self.session_service = InMemorySessionService()
        self.memory_bank = MemoryBank()
        
        # Initialize tools
        self.search_tool = WebSearchTool(self.logger)
        self.synthesis_tool = SynthesisTool(self.logger)
        
        # Initialize agents
        self.coordinator = CoordinatorAgent(self.logger, self.session_service)
        self.researcher = ResearcherAgent(self.logger, self.search_tool)
        self.synthesizer = SynthesizerAgent(self.logger, self.synthesis_tool, self.memory_bank)
    
    def research(self, query: str, session_id: str = None) -> Dict[str, Any]:
        """Execute full research workflow (Sequential agents)"""
        if not session_id:
            session_id = f"session_{int(time.time())}"
            self.session_service.create_session(session_id)
        
        self.logger.log("ResearchAgentSystem", "research_started", {
            "query": query,
            "session_id": session_id
        })
        
        # Sequential execution
        # 1. Coordinator plans
        plan = self.coordinator.plan_research(query, session_id)
        
        # 2. Researcher executes
        findings = self.researcher.conduct_research(plan)
        
        # 3. Synthesizer produces output
        synthesis = self.synthesizer.synthesize(findings, query)
        
        # Store in session
        context = ResearchContext(
            query=query,
            sources=[f["url"] for f in self.search_tool.search(query, 3)],
            findings=findings[:5],
            synthesis=synthesis,
            timestamp=datetime.now().isoformat()
        )
        self.session_service.add_to_session(session_id, context)
        
        result = {
            "query": query,
            "synthesis": synthesis,
            "sources_count": len(findings),
            "session_id": session_id
        }
        
        self.logger.log("ResearchAgentSystem", "research_completed", result)
        
        return result


# ==================== EVALUATION FRAMEWORK ====================

class AgentEvaluator:
    """Evaluate agent performance"""
    
    def __init__(self, logger: AgentLogger):
        self.logger = logger
    
    def evaluate_session(self, system: ResearchAgentSystem, session_id: str) -> Dict[str, Any]:
        """Evaluate agent performance for a session"""
        traces = self.logger.get_traces()
        session_traces = [t for t in traces if session_id in str(t.get("details", {}))]
        
        # Calculate metrics
        total_tasks = len([t for t in session_traces if t["action"].endswith("_completed")])
        total_time = sum([
            t["details"].get("duration_seconds", 0) 
            for t in session_traces 
            if "duration_seconds" in t["details"]
        ])
        
        history = system.session_service.get_session_history(session_id)
        
        metrics = {
            "session_id": session_id,
            "total_queries": len(history),
            "total_tasks_completed": total_tasks,
            "total_time_seconds": round(total_time, 2),
            "avg_time_per_query": round(total_time / max(len(history), 1), 2),
            "memory_entries": len(system.memory_bank.knowledge_base)
        }
        
        self.logger.log("AgentEvaluator", "evaluation_completed", metrics)
        
        return metrics


# ==================== DEMO & USAGE ====================

def main():
    """Demo the research agent system"""
    print("=" * 60)
    print("INTELLIGENT RESEARCH ASSISTANT AGENT SYSTEM")
    print("=" * 60)
    
    # Initialize system
    system = ResearchAgentSystem()
    evaluator = AgentEvaluator(system.logger)
    
    # Create session
    session_id = system.session_service.create_session("demo_session_001")
    
    # Example research queries
    queries = [
        "artificial intelligence latest trends 2024",
        "climate change mitigation strategies",
        "quantum computing applications"
    ]
    
    print("\n🔍 Starting research queries...\n")
    
    for query in queries:
        print(f"Query: {query}")
        result = system.research(query, session_id)
        print(f"✓ Synthesis: {result['synthesis'][:150]}...")
        print(f"  Sources: {result['sources_count']}")
        print("-" * 60)
    
    # Evaluate performance
    print("\n📊 Performance Evaluation:\n")
    metrics = evaluator.evaluate_session(system, session_id)
    for key, value in metrics.items():
        print(f"  {key}: {value}")
    
    # Export traces
    system.logger.export_traces("research_agent_traces.json")
    print("\n✓ Traces exported to: research_agent_traces.json")
    
    print("\n" + "=" * 60)
    print("Demo completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()