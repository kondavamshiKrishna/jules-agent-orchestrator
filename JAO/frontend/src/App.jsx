import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Play, Activity, CheckCircle, FileText, Bot, Github } from 'lucide-react';

const API_BASE = 'http://localhost:8000/api/v1';

function App() {
  const [agents, setAgents] = useState([]);
  const [selectedAgent, setSelectedAgent] = useState(null);
  const [task, setTask] = useState('');
  const [repoId, setRepoId] = useState('sources/github/YOUR_USERNAME/repo-name');
  

  const [sources, setSources] = useState([]);
  const [subscriptionPlan, setSubscriptionPlan] = useState('free');
  const [activeRuns, setActiveRuns] = useState([]);

  // Run tracking
  const [activeRunId, setActiveRunId] = useState(null);
  const [runState, setRunState] = useState(null);



  useEffect(() => {
    // Fetch available sources
    axios.get(`${API_BASE}/sources/`).then(res => {
      setSources(res.data);
      if(res.data.length > 0) setRepoId(res.data[0].id);
    }).catch(err => console.error("Failed to fetch sources", err));

    // Fetch available agents

    axios.get(`${API_BASE}/agents/`).then(res => {
      setAgents(res.data);
      if(res.data.length > 0) setSelectedAgent(res.data[0]);
    }).catch(err => console.error("Failed to fetch agents", err));
  }, []);

  useEffect(() => {
    // Poll for active workflows
    const interval = setInterval(() => {
        axios.get(`${API_BASE}/workflows/`).then(res => {
          setActiveRuns(res.data);
        }).catch(err => console.error("Failed to fetch active workflows", err));
    }, 2000);
    return () => clearInterval(interval);
  }, []);

  const startWorkflow = async () => {
    if (!task || !selectedAgent) return;
    
    try {
      const res = await axios.post(`${API_BASE}/workflows/run`, {
        task,
        starting_agent: selectedAgent.id,
        github_repo_id: repoId,
        interactive: true,
        plan: subscriptionPlan
      });
      setTask(''); // Clear task after starting
    } catch (error) {
      console.error("Failed to start workflow", error);
      alert(error.response?.data?.detail || "Error starting workflow check console");
    }
  };

  return (
    <div className="app-container">
      {/* Sidebar - Agent Roster */}
      <div className="sidebar">
        <div className="sidebar-header">
          <h1><Bot size={20} /> JAO Agents</h1>
        </div>
        <div className="agent-list">
          {agents.map(agent => (
            <div 
              key={agent.id} 
              className={`agent-item ${selectedAgent?.id === agent.id ? 'active' : ''}`}
              onClick={() => setSelectedAgent(agent)}
            >
              <div className="agent-name">{agent.name}</div>
              <div className="agent-desc" title={agent.description}>{agent.description}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Main Content Area */}
      <div className="main-content">
        <div className="topbar">
          <h2 style={{border: 'none', margin: 0, padding: 0}}>
            Jules Agent Orchestrator <span style={{fontSize: '0.8rem', color: 'var(--text-muted)'}}>Alpha</span>
          </h2>
        </div>
        
        <div className="dashboard">
          
          {/* Left Column: Launcher */}
          <div className="panel launcher-panel">
            <h2>Launch Workflow</h2>
            
            <div className="form-group">
              <label>Starting Agent</label>
              <div style={{padding: '10px', backgroundColor: 'var(--bg-color)', borderRadius: '6px', border: '1px solid var(--border)', display: 'flex', alignItems: 'center', gap: '10px'}}>
                <Bot size={18} color="var(--accent)" />
                <strong>{selectedAgent?.name || 'Select an agent from the sidebar'}</strong>
              </div>
            </div>


            <div className="form-group">
              <label>Subscription Plan Limit</label>
              <select value={subscriptionPlan} onChange={e => setSubscriptionPlan(e.target.value)}>
                <option value="free">Free (5 Concurrent Tasks)</option>
                <option value="pro">Pro (15 Concurrent Tasks)</option>
                <option value="ultra">Ultra (60 Concurrent Tasks)</option>
              </select>
            </div>

            <div className="form-group">
              <label><Github size={16} style={{verticalAlign: 'middle', marginRight: '5px'}}/> Source Repository</label>
              <select value={repoId} onChange={e => setRepoId(e.target.value)}>
                {sources.map(source => (
                  <option key={source.id} value={source.id}>{source.name}</option>
                ))}
              </select>
            </div>


            <div className="form-group">
              <label>Objective / Task</label>
              <textarea 
                rows={5} 
                value={task} 
                onChange={e => setTask(e.target.value)}
                placeholder="e.g. Audit the Stock Advisor module for background task bugs..."
              />
            </div>

            <button onClick={startWorkflow} disabled={!task || !selectedAgent}>
              <Play size={16} style={{verticalAlign: 'middle', marginRight: '5px'}}/>
              Start Workflow
            </button>
            

          </div>


          {/* Right Column: Live Monitor */}
          <div className="panel monitor-panel" style={{display: 'flex', flexDirection: 'column'}}>
            <h2><Activity size={18} style={{verticalAlign: 'middle'}}/> Live Monitor ({activeRuns.length} Active Tasks)</h2>
            
            {activeRuns.length === 0 ? (
              <div style={{color: 'var(--text-muted)', textAlign: 'center', marginTop: '40px'}}>
                <FileText size={48} opacity={0.2} style={{marginBottom: '10px'}}/>
                <p>No active workflows. Start one to see live progress.</p>
              </div>
            ) : (
              <div style={{flex: 1, overflowY: 'auto', paddingRight: '10px'}}>
                {activeRuns.map(run => (
                  <div key={run.run_id} className="history-item" style={{marginBottom: '15px', padding: '10px', backgroundColor: 'var(--bg-color)', borderRadius: '6px', border: '1px solid var(--border)'}}>
                    <div style={{marginBottom: '5px', display: 'flex', justifyContent: 'space-between'}}>
                      <span className={`status-badge RUNNING`}>{run.status}</span>
                      <span style={{fontSize: '0.8rem', color: 'var(--text-muted)'}}>Run ID: {run.run_id.substring(0,8)}...</span>
                    </div>
                    <div className="history-agent">Current Agent: @{run.current_agent || 'None'}</div>
                    <div style={{fontSize: '0.85rem', marginTop: '5px', color: 'var(--text-main)'}}>Task: {run.task}</div>
                  </div>
                ))}
              </div>
            )}
          </div>


        </div>
      </div>
    </div>
  );
}

export default App;
