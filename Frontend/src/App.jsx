import { useState } from "react";
import "./App.css";

function App() {
  const [formData, setFormData] = useState({
    englishTitle: "",
    originalTitle: "",
    country: "",
    province: "",
    cite: "",
    publisher: "",
    volume: "",
    coloniser: "",
    numLibResults: 2,
    numBurResults: 5,
    wsResults: 5,
    wsAmt: 15,
    maxWorkers: 9,
  });

  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSearch = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResults(null);

    try {
      const response = await fetch(
        "http://localhost:8000/api/cascading-search",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(formData),
        }
      );

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setResults(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setFormData({
      englishTitle: "",
      originalTitle: "",
      country: "",
      province: "",
      cite: "",
      publisher: "",
      volume: "",
      coloniser: "",
      numLibResults: 2,
      numBurResults: 5,
      wsResults: 5,
      wsAmt: 15,
      maxWorkers: 9,
    });
    setResults(null);
    setError(null);
  };

  const parseResult = (result) => {
    // Handle different result formats from the API
    // Library/Bureau results: [source, url, title, description]
    // Web results: [[url, size, title, snippet], ...]
    if (Array.isArray(result)) {
      if (result.length === 4) {
        // Library/Bureau format: [source, url, title, description]
        return {
          source: result[0] || "N/A",
          url: result[1] || "N/A",
          title: result[2] || "N/A",
          description: result[3] || "",
        };
      } else if (result.length >= 2) {
        // Web format: [url, size, title, snippet]
        return {
          url: result[0] || "N/A",
          title: result[2] || result[0] || "N/A",
          source: "Web",
          description: result[3] || "",
        };
      }
    } else if (typeof result === "object") {
      // Already an object format
      return {
        source: result.source || result.Source || "N/A",
        url: result.url || result.URL || "N/A",
        title: result.title || result.Title || "N/A",
        description: result.description || "",
      };
    }
    return {
      source: "N/A",
      url: "N/A",
      title: "N/A",
      description: "",
    };
  };

  const getParsedResults = () => {
    if (!results || !results.results) return [];

    // Check if results is a single result (flat array of 4 items)
    if (
      results.results.length === 4 &&
      typeof results.results[0] === "string"
    ) {
      return [parseResult(results.results)];
    }

    // Multiple results, each is an array
    return results.results.map(parseResult);
  };

  const downloadCSV = () => {
    if (!results || !results.results || results.results.length === 0) return;

    const parsedResults = getParsedResults();
    const headers = ["Source", "Title", "URL", "Phase"];
    const rows = parsedResults.map((result) => [
      result.source,
      result.title,
      result.url,
      results.phase || "N/A",
    ]);

    const csvContent = [
      headers.join(","),
      ...rows.map((row) => row.map((cell) => `"${cell}"`).join(",")),
    ].join("\n");

    const blob = new Blob([csvContent], { type: "text/csv" });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `cascading_search_results_${new Date().toISOString()}.csv`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
  };

  return (
    <div className="app">
      <header className="header">
        <h1>Census Document Search</h1>
        <p>Document Discovery</p>
      </header>

      <nav className="nav">
        <button className="nav-button active">🔍 Search</button>
        <button className="nav-button">📚 History</button>
        <button className="nav-button">📄 API Docs</button>
      </nav>

      <main className="main-content">
        <section className="search-section">
          <h2>Document Search</h2>
          <p className="subtitle">
            Search for census documents using filters. If no results are found
            in the CSV database, you can search the web.
          </p>

          <form onSubmit={handleSearch} className="search-form">
            <h3>Search Filters</h3>
            <p className="filter-subtitle">
              Filter documents by various criteria. All filters support partial
              matching.
            </p>

            <div className="form-grid">
              <div className="form-group">
                <label htmlFor="englishTitle">Title (English) *</label>
                <input
                  type="text"
                  id="englishTitle"
                  name="englishTitle"
                  value={formData.englishTitle}
                  onChange={handleInputChange}
                  placeholder="e.g., Title in English"
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="country">Country *</label>
                <input
                  type="text"
                  id="country"
                  name="country"
                  value={formData.country}
                  onChange={handleInputChange}
                  placeholder="e.g., Argentina"
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="originalTitle">Original Title</label>
                <input
                  type="text"
                  id="originalTitle"
                  name="originalTitle"
                  value={formData.originalTitle}
                  onChange={handleInputChange}
                  placeholder="Title in original language"
                />
              </div>

              <div className="form-group">
                <label htmlFor="province">Province</label>
                <input
                  type="text"
                  id="province"
                  name="province"
                  value={formData.province}
                  onChange={handleInputChange}
                  placeholder="e.g., National Record"
                />
              </div>

              <div className="form-group">
                <label htmlFor="cite">Cite</label>
                <input
                  type="text"
                  id="cite"
                  name="cite"
                  value={formData.cite}
                  onChange={handleInputChange}
                  placeholder="Citation information"
                />
              </div>

              <div className="form-group">
                <label htmlFor="publisher">Author/Publisher</label>
                <input
                  type="text"
                  id="publisher"
                  name="publisher"
                  value={formData.publisher}
                  onChange={handleInputChange}
                  placeholder="Publisher name"
                />
              </div>

              <div className="form-group">
                <label htmlFor="volume">Volume Number</label>
                <input
                  type="text"
                  id="volume"
                  name="volume"
                  value={formData.volume}
                  onChange={handleInputChange}
                  placeholder="e.g., Volume I"
                />
              </div>

              <div className="form-group">
                <label htmlFor="coloniser">Coloniser</label>
                <input
                  type="text"
                  id="coloniser"
                  name="coloniser"
                  value={formData.coloniser}
                  onChange={handleInputChange}
                  placeholder="Coloniser information"
                />
              </div>
            </div>

            <div className="button-group">
              <button
                type="submit"
                className="search-button"
                disabled={loading}
              >
                {loading ? "⏳ Searching..." : "🔍 Search"}
              </button>
              <button
                type="button"
                className="reset-button"
                onClick={handleReset}
              >
                🔄 Reset
              </button>
            </div>
          </form>
        </section>

        {error && (
          <div className="error-message">
            <strong>Error:</strong> {error}
          </div>
        )}

        {results && (
          <section className="results-section">
            <div className="results-header">
              <h3>Search Results</h3>
              <div className="results-info">
                <span className="badge">
                  {results.phase.toUpperCase()} Phase
                </span>
                <span className="time">
                  Time: {results.time_taken.toFixed(2)}s
                </span>
                <span className="count">
                  {getParsedResults().length} results
                </span>
              </div>
            </div>

            {results.status === "no_results" ? (
              <div className="no-results">
                <p>No results found in any phase (Library, Bureau, or Web).</p>
              </div>
            ) : (
              <>
                <div className="download-section">
                  <button onClick={downloadCSV} className="download-button">
                    📥 Download Results (CSV)
                  </button>
                </div>

                <div className="table-container">
                  <table className="results-table">
                    <thead>
                      <tr>
                        <th>#</th>
                        <th>Source</th>
                        <th>Title</th>
                        <th>URL</th>
                      </tr>
                    </thead>
                    <tbody>
                      {getParsedResults().map((result, index) => (
                        <tr key={index}>
                          <td>{index + 1}</td>
                          <td>{result.source}</td>
                          <td>{result.title}</td>
                          <td>
                            <a
                              href={result.url}
                              target="_blank"
                              rel="noopener noreferrer"
                            >
                              View Document
                            </a>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </>
            )}
          </section>
        )}
      </main>

      <footer className="footer">
        <p>Document Search API v1.0.0</p>
      </footer>
    </div>
  );
}

export default App;
