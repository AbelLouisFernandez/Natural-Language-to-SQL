import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState(null);

  const executeQuery = async () => {
    try {
      const res = await axios.post("http://localhost:8000/api/execute_natural/", { query });
      setResponse(res.data);
    } catch (error) {
      setResponse({ status: "error", message: "Failed to connect to server" });
    }
  };

  return (
    <div className="container">
      <h1>SQL BRO</h1>
      <textarea
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Describe the action you want to perform (e.g., 'Create a table for users with name and age')."
      />
      <button onClick={executeQuery}>Run Query</button>

      {response && (
        <div className={`response ${response.status}`}>
          <h3>Result:</h3>
          {response.status === "success" && Array.isArray(response.results) ? (
              <table>
                <thead>
                  <tr>
                    {response.columns.map((col, index) => <th key={index}>{col}</th>)}
                  </tr>
                </thead>
                <tbody>
                  {response.results.map((row, rowIndex) => (
                    <tr key={rowIndex}>
                      {row.map((value, colIndex) => (
                        <td key={colIndex}>{value}</td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            ) : (
              <p>{response.message}</p>
            )}

        </div>
      )}
    </div>
  );
}

export default App;
