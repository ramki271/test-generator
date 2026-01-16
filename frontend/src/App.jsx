import { useState } from 'react';
import axios from 'axios';
import { FaRobot, FaSpinner, FaDownload, FaCheckCircle } from 'react-icons/fa';
import './App.css';

// Configure API base URL - update this after Railway deployment
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

function App() {
  const [mode, setMode] = useState('manual'); // 'manual' or 'jira'
  const [loading, setLoading] = useState(false);
  const [testCases, setTestCases] = useState(null);
  const [error, setError] = useState(null);

  // Manual input state
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [criteria, setCriteria] = useState(['']);

  // JIRA input state
  const [jiraIssue, setJiraIssue] = useState('');

  // Options
  const [testTypes, setTestTypes] = useState(['functional']);
  const [includeEdgeCases, setIncludeEdgeCases] = useState(true);
  const [includeNegativeTests, setIncludeNegativeTests] = useState(true);

  const addCriterion = () => {
    setCriteria([...criteria, '']);
  };

  const updateCriterion = (index, value) => {
    const newCriteria = [...criteria];
    newCriteria[index] = value;
    setCriteria(newCriteria);
  };

  const removeCriterion = (index) => {
    const newCriteria = criteria.filter((_, i) => i !== index);
    setCriteria(newCriteria.length === 0 ? [''] : newCriteria);
  };

  const handleGenerate = async () => {
    setLoading(true);
    setError(null);
    setTestCases(null);

    try {
      const payload = mode === 'manual'
        ? {
            manual_input: {
              title,
              description,
              acceptance_criteria: criteria.filter(c => c.trim() !== '')
            },
            test_types: testTypes,
            include_edge_cases: includeEdgeCases,
            include_negative_tests: includeNegativeTests
          }
        : {
            jira_issue: {
              issue_key: jiraIssue
            },
            test_types: testTypes,
            include_edge_cases: includeEdgeCases,
            include_negative_tests: includeNegativeTests
          };

      const response = await axios.post(`${API_BASE_URL}/api/v1/generate-test-cases`, payload, {
        timeout: 180000 // 3 minutes timeout for agent processing
      });

      setTestCases(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Failed to generate test cases');
    } finally {
      setLoading(false);
    }
  };

  const exportTestCases = () => {
    const dataStr = JSON.stringify(testCases, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `test-cases-${testCases.feature_title.replace(/\s+/g, '-')}.json`;
    link.click();
  };

  const toggleTestType = (type) => {
    setTestTypes(prev =>
      prev.includes(type)
        ? prev.filter(t => t !== type)
        : [...prev, type]
    );
  };

  return (
    <div className="app">
      <header className="header">
        <div className="header-content">
          <FaRobot className="logo-icon" />
          <h1>Test Case Generator</h1>
          <p className="subtitle">Powered by Claude Agent SDK</p>
        </div>
      </header>

      <main className="main-content">
        <div className="container">
          {/* Mode Selection */}
          <div className="mode-selector">
            <button
              className={`mode-btn ${mode === 'manual' ? 'active' : ''}`}
              onClick={() => setMode('manual')}
            >
              Manual Input
            </button>
            <button
              className={`mode-btn ${mode === 'jira' ? 'active' : ''}`}
              onClick={() => setMode('jira')}
            >
              JIRA Issue
            </button>
          </div>

          {/* Input Form */}
          <div className="form-section">
            {mode === 'manual' ? (
              <div className="manual-form">
                <div className="form-group">
                  <label>Feature Title *</label>
                  <input
                    type="text"
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                    placeholder="e.g., User Login Feature"
                    className="input"
                  />
                </div>

                <div className="form-group">
                  <label>Description *</label>
                  <textarea
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                    placeholder="Describe the feature..."
                    className="textarea"
                    rows={3}
                  />
                </div>

                <div className="form-group">
                  <label>Acceptance Criteria *</label>
                  {criteria.map((criterion, index) => (
                    <div key={index} className="criteria-row">
                      <input
                        type="text"
                        value={criterion}
                        onChange={(e) => updateCriterion(index, e.target.value)}
                        placeholder={`Criterion ${index + 1}`}
                        className="input"
                      />
                      {criteria.length > 1 && (
                        <button
                          onClick={() => removeCriterion(index)}
                          className="btn-remove"
                        >
                          ×
                        </button>
                      )}
                    </div>
                  ))}
                  <button onClick={addCriterion} className="btn-add">
                    + Add Criterion
                  </button>
                </div>
              </div>
            ) : (
              <div className="jira-form">
                <div className="form-group">
                  <label>JIRA Issue Key *</label>
                  <input
                    type="text"
                    value={jiraIssue}
                    onChange={(e) => setJiraIssue(e.target.value)}
                    placeholder="e.g., PROJ-123"
                    className="input"
                  />
                </div>
              </div>
            )}

            {/* Options */}
            <div className="options-section">
              <div className="option-group">
                <h3>Test Types</h3>
                <div className="test-types-grid">
                  {['functional', 'integration', 'e2e', 'unit', 'api'].map(type => (
                    <label key={type} className="checkbox-label">
                      <input
                        type="checkbox"
                        checked={testTypes.includes(type)}
                        onChange={() => toggleTestType(type)}
                      />
                      <span>{type.toUpperCase()}</span>
                    </label>
                  ))}
                </div>
              </div>

              <div className="option-group">
                <h3>Additional Options</h3>
                <div className="additional-options">
                  <label className="checkbox-label">
                    <input
                      type="checkbox"
                      checked={includeEdgeCases}
                      onChange={(e) => setIncludeEdgeCases(e.target.checked)}
                    />
                    <span>Include Edge Cases</span>
                  </label>
                  <label className="checkbox-label">
                    <input
                      type="checkbox"
                      checked={includeNegativeTests}
                      onChange={(e) => setIncludeNegativeTests(e.target.checked)}
                    />
                    <span>Include Negative Tests</span>
                  </label>
                </div>
              </div>
            </div>

            {/* Generate Button */}
            <button
              onClick={handleGenerate}
              disabled={loading || (mode === 'manual' && (!title || !description)) || (mode === 'jira' && !jiraIssue)}
              className="btn-generate"
            >
              {loading ? (
                <>
                  <FaSpinner className="spinner" />
                  Generating Test Cases...
                </>
              ) : (
                <>
                  <FaRobot />
                  Generate Test Cases
                </>
              )}
            </button>
          </div>

          {/* Error Display */}
          {error && (
            <div className="error-box">
              <strong>Error:</strong> {error}
            </div>
          )}

          {/* Results */}
          {testCases && (
            <div className="results-section">
              <div className="results-header">
                <h2>
                  <FaCheckCircle className="success-icon" />
                  Generated {testCases.test_cases.length} Test Cases
                </h2>
                <button onClick={exportTestCases} className="btn-export">
                  <FaDownload />
                  Export JSON
                </button>
              </div>

              <div className="coverage-summary">
                <h3>Coverage Summary</h3>
                <p>{testCases.coverage_summary}</p>
              </div>

              <div className="test-cases-list">
                {testCases.test_cases.map((testCase, index) => (
                  <div key={index} className="test-case-card">
                    <div className="test-case-header">
                      <span className="test-number">#{index + 1}</span>
                      <span className={`priority-badge ${testCase.priority}`}>
                        {testCase.priority}
                      </span>
                      <span className="type-badge">{testCase.type}</span>
                    </div>

                    <h3>{testCase.title}</h3>

                    {/* PP-Specific Fields */}
                    {testCase.business_impact && (
                      <div className="project-specific-badge">
                        <span className="badge-label">Business Impact:</span>
                        <span className={`badge-value impact-${testCase.business_impact?.toLowerCase()}`}>
                          {testCase.business_impact}
                        </span>
                      </div>
                    )}
                    {testCase.data_volume && (
                      <div className="project-specific-badge">
                        <span className="badge-label">Data Volume:</span>
                        <span className="badge-value">{testCase.data_volume}</span>
                      </div>
                    )}

                    {/* XSP-Specific Fields */}
                    {testCase.platform && (
                      <div className="project-specific-badge">
                        <span className="badge-label">Platform:</span>
                        <span className="badge-value">{testCase.platform}</span>
                      </div>
                    )}
                    {testCase.user_story && (
                      <div className="section user-story">
                        <h4>User Story</h4>
                        <p className="story-text">{testCase.user_story}</p>
                      </div>
                    )}

                    {testCase.preconditions?.length > 0 && (
                      <div className="section">
                        <h4>Preconditions</h4>
                        <ul>
                          {testCase.preconditions.map((pre, i) => (
                            <li key={i}>{pre}</li>
                          ))}
                        </ul>
                      </div>
                    )}

                    <div className="section">
                      <h4>Steps</h4>
                      <ol className="steps-list">
                        {testCase.steps.map((step, i) => (
                          <li key={i}>
                            <strong>{step.action}</strong>
                            <p className="expected">Expected: {step.expected_result}</p>
                          </li>
                        ))}
                      </ol>
                    </div>

                    <div className="section">
                      <h4>Expected Outcome</h4>
                      <p>{testCase.expected_outcome}</p>
                    </div>

                    {/* PP-Specific: Compliance Requirements */}
                    {testCase.compliance_requirements?.length > 0 && (
                      <div className="section pp-specific">
                        <h4>Compliance Requirements</h4>
                        <ul>
                          {testCase.compliance_requirements.map((req, i) => (
                            <li key={i}>{req}</li>
                          ))}
                        </ul>
                      </div>
                    )}

                    {/* XSP-Specific: Performance Criteria */}
                    {testCase.performance_criteria && (
                      <div className="section xsp-specific">
                        <h4>Performance Criteria</h4>
                        <div className="performance-grid">
                          {Object.entries(testCase.performance_criteria).map(([key, value]) => (
                            <div key={key} className="perf-item">
                              <span className="perf-label">{key.replace(/_/g, ' ')}:</span>
                              <span className="perf-value">{value}</span>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* XSP-Specific: Platform Coverage */}
                    {testCase.platform_coverage?.length > 0 && (
                      <div className="section xsp-specific">
                        <h4>Platform Coverage</h4>
                        <div className="platform-badges">
                          {testCase.platform_coverage.map((platform, i) => (
                            <span key={i} className="platform-badge">{platform}</span>
                          ))}
                        </div>
                      </div>
                    )}

                    {testCase.tags?.length > 0 && (
                      <div className="tags">
                        {testCase.tags.map((tag, i) => (
                          <span key={i} className="tag">{tag}</span>
                        ))}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </main>

      <footer className="footer">
        <p>Powered by Claude Agent SDK • Autonomous Test Case Generation</p>
      </footer>
    </div>
  );
}

export default App;
