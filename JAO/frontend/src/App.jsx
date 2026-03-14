import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Play, Activity, CheckCircle, FileText, Bot, Github } from 'lucide-react';

const API_BASE = 'http://localhost:8000/api/v1';

function App() {
  const [agents, setAgents] = useState([]);
  const [selectedAgent, setSelectedAgent] = useState(null);
  const [task, setTask] = useState('');
  const [repoId, setRepoId] = useState('sources/github/YOUR_USERNAME/repo-name');
  
  // Run tracking
  const [activeRunId, setActiveRunId] = useState(null);
  const [runState, setRunState] = useState(null);

  useEffect(() => {
    // Fetch available agents
    axios.get(`${API_BASE}/agents/`).then(res => {
      setAgents(res.data);
      if(res.data.length > 0) setSelectedAgent(res.data[0]);
    }).catch(err => console.error("Failed to fetch agents", err));
  }, []);

  useEffect(() => {
    // Poll for workflow status
    let interval;
    if (activeRunId && runState?.status !== 'COMPLETED') {
      interval = setInterval(() => {
        axios.get(`${API_BASE}/workflows/${activeRunId}`).then(res => {
          setRunState(res.data);
        });
      }, 2000);
    }
    return () => clearInterval(interval);
  }, [activeRunId, runState]);

  const startWorkflow = async () => {
    if (!task || !selectedAgent) return;
    
    try {
      const res = await axios.post(`${API_BASE}/workflows/run`, {
        task,
        starting_agent: selectedAgent.id,
        github_repo_id: repoId,
        interactive: true
      });
      setActiveRunId(res.data.session_id);
      setRunState({ status: 'STARTING', history: [] });
    } catch (error) {
      console.error("Failed to start workflow", error);
      alert("Error starting workflow check console");
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
              <label><Github size={16} style={{verticalAlign: 'middle', marginRight: '5px'}}/> GitHub Source ID</label>
              <input 
                type="text" 
                value={repoId} 
                onChange={e => setRepoId(e.target.value)}
                placeholder="sources/github/userName/repo"
              />
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

            <button onClick={startWorkflow} disabled={!task || !selectedAgent || activeRunId}>
              <Play size={16} style={{verticalAlign: 'middle', marginRight: '5px'}}/>
              {activeRunId ? 'Workflow Running...' : 'Start Workflow'}
            </button>
            
            {activeRunId && (
              <button className="secondary" style={{marginLeft: '10px'}} onClick={() => {setActiveRunId(null); setRunState(null);}}>
                Clear Run
              </button>
            )}
          </div>

          {/* Right Column: Live Monitor */}
          <div className="panel monitor-panel" style={{display: 'flex', flexDirection: 'column'}}>
            <h2><Activity size={18} style={{verticalAlign: 'middle'}}/> Live Monitor</h2>
            
            {!activeRunId ? (
              <div style={{color: 'var(--text-muted)', textAlign: 'center', marginTop: '40px'}}>
                <FileText size={48} opacity={0.2} style={{marginBottom: '10px'}}/>
                <p>No active workflow. Start one to see live progress.</p>
              </div>
            ) : (
              <div style={{display: 'flex', flexDirection: 'column', height: '100%'}}>
                 <div style={{marginBottom: '20px'}}>
                    <strong>Status: </strong>
                    <span className={`status-badge ${runState?.status?.includes('COMPLETED') ? 'COMPLETED' : 'RUNNING'}`}>
                      {runState?.status || 'INITIALIZING'}
                    </span>
                 </div>
                 
                 <div style={{flex: 1, overflowY: 'auto', paddingRight: '10px'}}>
                    {runState?.history?.map((step, idx) => (
                      <div key={idx} className="history-item">
                        <div className="history-agent">@{step.agent}</div>
                        <div className="history-output">{step.output.trim()}</div>
                      </div>
                    ))}
                    
                    {runState?.status !== 'COMPLETED' && (
                        <div className="history-item" style={{opacity: 0.6}}>
                          <div className="history-agent">Waiting for {runState?.current_agent || 'agent'}...</div>
                        </div>
                    )}
                    
                    {runState?.status === 'COMPLETED' && (
                        <div style={{color: 'var(--success)', display: 'flex', alignItems: 'center', gap: '5px', marginTop: '20px'}}>
                           <CheckCircle size={18} /> Workflow Reached Completion
                        </div>
                    )}
                 </div>
              </div>
            )}
          </div>

        </div>
      </div>
    </div>
  );
}

export default App;
