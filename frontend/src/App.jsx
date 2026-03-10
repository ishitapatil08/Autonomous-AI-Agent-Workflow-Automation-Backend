import { useState } from 'react';
import './index.css';

function App() {
  const [instruction, setInstruction] = useState('');
  const [status, setStatus] = useState('idle');
  const [result, setResult] = useState(null);
  const [trace, setTrace] = useState([]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!instruction.trim()) return;

    setStatus('running');
    setResult(null);
    setTrace([]);

    try {
      // Calling the backend API
      const response = await fetch('http://127.0.0.1:5000/agent/run', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ instruction }),
      });

      const data = await response.json();
      
      if (response.ok) {
        setStatus('success');
        setResult(data.result);
        setTrace(data.trace || []);
      } else {
        setStatus('error');
        setResult(data.error || 'An error occurred');
      }
    } catch (err) {
      setStatus('error');
      setResult('Failed to connect to the agent backend.');
    }
  };

  return (
    <div className="dashboard-container">
      <header className="glass-header">
        <h1>Autonomous Agent Workspace</h1>
      </header>
      <main className="dashboard-main">
        
        <div className="glass-panel input-panel">
          <h2>New Task Execution</h2>
          <form onSubmit={handleSubmit}>
            <textarea 
              rows="4" 
              placeholder="E.g., Summarize all customer complaints from this week and create Jira tickets..."
              value={instruction}
              onChange={(e) => setInstruction(e.target.value)}
              disabled={status === 'running'}
            />
            <div style={{ marginTop: '1rem', display: 'flex', justifyContent: 'flex-end' }}>
              <button 
                type="submit" 
                className="btn-primary"
                disabled={status === 'running' || !instruction.trim()}
              >
                {status === 'running' ? 'Agent Reasoning...' : 'Execute Task'}
              </button>
            </div>
          </form>
        </div>

        {status !== 'idle' && (
          <div className="glass-panel result-panel">
            <h2>Agent Trace & Output</h2>
            
            <div className="trace-container">
              {trace.map((step, index) => (
                <div key={index} className="trace-step">
                  {step.thought && <div className="step-thought">🤔 <strong>Thought:</strong> {step.thought}</div>}
                  {step.action && <div className="step-action">🛠️ <strong>Action:</strong> {step.action}</div>}
                  {step.observation && <div className="step-observation">👀 <strong>Observation:</strong> {step.observation}</div>}
                </div>
              ))}
            </div>

            {status === 'success' && (
              <div className="final-result success">
                <h3>Final Answer</h3>
                <p>{result}</p>
              </div>
            )}
            
            {status === 'error' && (
              <div className="final-result error">
                <h3>Error</h3>
                <p>{result}</p>
              </div>
            )}
          </div>
        )}

      </main>
    </div>
  );
}

export default App;
