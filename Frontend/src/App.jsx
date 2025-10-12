import { useState, useEffect } from "react";
import "./App.css";

function App() {
  const [filters, setFilters] = useState({
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
  const [currentView, setCurrentView] = useState("search"); // 'search', 'history', or 'batch'
  const [savedSearches, setSavedSearches] = useState([]);
  const [showSaveModal, setShowSaveModal] = useState(false);
  const [searchName, setSearchName] = useState("");

  // Batch search state
  const [csvFile, setCsvFile] = useState(null);
  const [batchResults, setBatchResults] = useState(null);
  const [batchLoading, setBatchLoading] = useState(false);
  const [batchError, setBatchError] = useState(null);

  // Load saved searches from localStorage on mount
  useEffect(() => {
    const saved = localStorage.getItem("searchHistory");
    if (saved) {
      try {
        setSavedSearches(JSON.parse(saved));
      } catch (err) {
        console.error("Error loading saved searches:", err);
      }
    }
  }, []);

  // Save searches to localStorage whenever they change
  useEffect(() => {
    localStorage.setItem("searchHistory", JSON.stringify(savedSearches));
  }, [savedSearches]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResults(null);

    try {
      // Remove empty fields
      const cleanedFilters = Object.fromEntries(
        Object.entries(filters).filter(
          ([_, value]) => value !== "" && value !== undefined
        )
      );

      const response = await fetch(
        "http://localhost:8000/api/cascading-search",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(cleanedFilters),
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
    setFilters({
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

  const handleSaveSearch = () => {
    setShowSaveModal(true);
  };

  const confirmSaveSearch = () => {
    if (!searchName.trim()) {
      alert("Please enter a name for this search");
      return;
    }

    const newSearch = {
      id: Date.now(),
      name: searchName,
      filters: filters,
      results: results,
      timestamp: new Date().toISOString(),
    };

    setSavedSearches([newSearch, ...savedSearches]);
    setShowSaveModal(false);
    setSearchName("");
    alert("Search saved successfully!");
  };

  const loadSearch = (search) => {
    setFilters(search.filters);
    setResults(search.results);
    setCurrentView("search");
  };

  const deleteSearch = (id) => {
    if (window.confirm("Are you sure you want to delete this search?")) {
      setSavedSearches(savedSearches.filter((search) => search.id !== id));
    }
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

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file && file.type === "text/csv") {
      setCsvFile(file);
      setBatchError(null);
    } else {
      setBatchError("Please select a valid CSV file");
      setCsvFile(null);
    }
  };

  const handleBatchSearch = async () => {
    if (!csvFile) {
      setBatchError("Please select a CSV file first");
      return;
    }

    setBatchLoading(true);
    setBatchError(null);
    setBatchResults(null);

    try {
      const formData = new FormData();
      formData.append("file", csvFile);

      const response = await fetch("http://localhost:8000/api/batch-search", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(
          errorData.detail || `HTTP error! status: ${response.status}`
        );
      }

      const data = await response.json();
      setBatchResults(data);
    } catch (err) {
      setBatchError(err.message);
    } finally {
      setBatchLoading(false);
    }
  };

  const downloadBatchResultsCSV = () => {
    if (
      !batchResults ||
      !batchResults.results ||
      batchResults.results.length === 0
    )
      return;

    const headers = [
      "Row",
      "Title",
      "Country",
      "Phase",
      "Status",
      "Result URL",
      "Error",
    ];
    const rows = batchResults.results.map((result) => {
      const firstResult = result.search_result?.results?.[0];
      let resultUrl = "N/A";

      if (firstResult && Array.isArray(firstResult)) {
        resultUrl = firstResult[1] || "N/A";
      }

      return [
        result.row_number,
        result.search_input.english_title,
        result.search_input.country,
        result.search_result?.phase || "N/A",
        result.error ? "Failed" : "Success",
        resultUrl,
        result.error || "",
      ];
    });

    const csvContent = [
      headers.join(","),
      ...rows.map((row) => row.map((cell) => `"${cell}"`).join(",")),
    ].join("\n");

    const blob = new Blob([csvContent], { type: "text/csv" });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `batch_search_results_${new Date().toISOString()}.csv`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
  };

  return (
    <div className="app">
      <header className="header">
        <h1>Census Document Search</h1>
        <p>Document Discovery - Cascading Search</p>
      </header>

      <nav className="nav">
        <button
          className={`nav-button ${currentView === "search" ? "active" : ""}`}
          onClick={() => setCurrentView("search")}
        >
          🔍 Search
        </button>
        <button
          className={`nav-button ${currentView === "batch" ? "active" : ""}`}
          onClick={() => setCurrentView("batch")}
        >
          📊 Batch Search
        </button>
        <button
          className={`nav-button ${currentView === "history" ? "active" : ""}`}
          onClick={() => setCurrentView("history")}
        >
          📚 History ({savedSearches.length})
        </button>
        <button
          className={`nav-button ${currentView === "api-docs" ? "active" : ""}`}
          onClick={() => setCurrentView("api-docs")}
        >
          📄 API Docs
        </button>
      </nav>

      <main className="main-content">
        {currentView === "search" && (
          <>
            <section className="search-section">
              <div className="card">
                <div className="card-header">
                  <h2 className="card-title">Search Filters</h2>
                  <p className="card-description">
                    Filter documents by various criteria. The system will search
                    libraries first, then bureaus, then the web.
                  </p>
                </div>
                <div className="card-content">
                  <form onSubmit={handleSubmit} className="search-form">
                    <div className="form-grid">
                      <div className="form-group">
                        <label htmlFor="englishTitle">
                          Title (English) <span className="required">*</span>
                        </label>
                        <input
                          type="text"
                          id="englishTitle"
                          value={filters.englishTitle}
                          onChange={(e) =>
                            setFilters({
                              ...filters,
                              englishTitle: e.target.value,
                            })
                          }
                          placeholder="e.g., National Census"
                          required
                        />
                      </div>

                      <div className="form-group">
                        <label htmlFor="country">
                          Country <span className="required">*</span>
                        </label>
                        <input
                          type="text"
                          id="country"
                          value={filters.country}
                          onChange={(e) =>
                            setFilters({ ...filters, country: e.target.value })
                          }
                          placeholder="e.g., Argentina"
                          required
                        />
                      </div>

                      <div className="form-group">
                        <label htmlFor="originalTitle">Original Title</label>
                        <input
                          type="text"
                          id="originalTitle"
                          value={filters.originalTitle}
                          onChange={(e) =>
                            setFilters({
                              ...filters,
                              originalTitle: e.target.value,
                            })
                          }
                          placeholder="Title in original language"
                        />
                      </div>

                      <div className="form-group">
                        <label htmlFor="province">Province</label>
                        <input
                          type="text"
                          id="province"
                          value={filters.province}
                          onChange={(e) =>
                            setFilters({ ...filters, province: e.target.value })
                          }
                          placeholder="e.g., Buenos Aires"
                        />
                      </div>

                      <div className="form-group">
                        <label htmlFor="cite">Year</label>
                        <input
                          type="text"
                          id="cite"
                          value={filters.cite}
                          onChange={(e) =>
                            setFilters({ ...filters, cite: e.target.value })
                          }
                          placeholder="e.g., 1869"
                        />
                      </div>

                      <div className="form-group">
                        <label htmlFor="publisher">Author/Publisher</label>
                        <input
                          type="text"
                          id="publisher"
                          value={filters.publisher}
                          onChange={(e) =>
                            setFilters({
                              ...filters,
                              publisher: e.target.value,
                            })
                          }
                          placeholder="Publisher name"
                        />
                      </div>

                      <div className="form-group">
                        <label htmlFor="volume">Volume Number</label>
                        <input
                          type="text"
                          id="volume"
                          value={filters.volume}
                          onChange={(e) =>
                            setFilters({ ...filters, volume: e.target.value })
                          }
                          placeholder="e.g., Volume I"
                        />
                      </div>

                      <div className="form-group">
                        <label htmlFor="coloniser">Coloniser</label>
                        <input
                          type="text"
                          id="coloniser"
                          value={filters.coloniser}
                          onChange={(e) =>
                            setFilters({
                              ...filters,
                              coloniser: e.target.value,
                            })
                          }
                          placeholder="Colonial power"
                        />
                      </div>

                      <div className="form-group">
                        <label htmlFor="numLibResults">Library Results</label>
                        <input
                          type="number"
                          id="numLibResults"
                          value={filters.numLibResults}
                          onChange={(e) =>
                            setFilters({
                              ...filters,
                              numLibResults: parseInt(e.target.value) || 2,
                            })
                          }
                          min="1"
                          placeholder="2"
                        />
                      </div>

                      <div className="form-group">
                        <label htmlFor="numBurResults">Bureau Results</label>
                        <input
                          type="number"
                          id="numBurResults"
                          value={filters.numBurResults}
                          onChange={(e) =>
                            setFilters({
                              ...filters,
                              numBurResults: parseInt(e.target.value) || 5,
                            })
                          }
                          min="1"
                          placeholder="5"
                        />
                      </div>

                      <div className="form-group">
                        <label htmlFor="wsResults">Web Results</label>
                        <input
                          type="number"
                          id="wsResults"
                          value={filters.wsResults}
                          onChange={(e) =>
                            setFilters({
                              ...filters,
                              wsResults: parseInt(e.target.value) || 5,
                            })
                          }
                          min="1"
                          placeholder="5"
                        />
                      </div>
                    </div>

                    <div className="button-group">
                      <button
                        type="submit"
                        className="search-button"
                        disabled={loading}
                      >
                        <span className="button-icon">🔍</span>
                        {loading ? "Searching..." : "Search"}
                      </button>
                      <button
                        type="button"
                        className="reset-button"
                        onClick={handleReset}
                        disabled={loading}
                      >
                        <span className="button-icon">🔄</span>
                        Reset
                      </button>
                    </div>
                  </form>
                </div>
              </div>
            </section>

            {error && (
              <div className="error-message">
                <span className="error-icon">⚠️</span>
                <div>
                  <strong>Error:</strong> {error}
                </div>
              </div>
            )}

            {results && (
              <section className="results-section">
                <div className="card">
                  <div className="card-header">
                    <div className="results-header-content">
                      <h2 className="card-title">Search Results</h2>
                      <div className="results-badges">
                        <span className="badge badge-primary">
                          {results.phase.toUpperCase()} Phase
                        </span>
                        <span className="badge badge-secondary">
                          ⏱️ {results.time_taken.toFixed(2)}s
                        </span>
                        <span className="badge badge-info">
                          📊 {getParsedResults().length} results
                        </span>
                      </div>
                    </div>
                  </div>

                  <div className="card-content">
                    {results.status === "no_results" ? (
                      <div className="no-results">
                        <span className="no-results-icon">🔍</span>
                        <p>
                          No results found in any phase (Library, Bureau, or
                          Web).
                        </p>
                        <p className="no-results-hint">
                          Try adjusting your search criteria or using different
                          keywords.
                        </p>
                      </div>
                    ) : (
                      <>
                        <div className="download-section">
                          <button
                            onClick={downloadCSV}
                            className="download-button"
                          >
                            <span className="button-icon">📥</span>
                            Download Results (CSV)
                          </button>
                          <button
                            onClick={handleSaveSearch}
                            className="save-button"
                          >
                            <span className="button-icon">💾</span>
                            Save Search
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
                                  <td className="index-cell">{index + 1}</td>
                                  <td>
                                    <span className="source-badge">
                                      {result.source}
                                    </span>
                                  </td>
                                  <td className="title-cell">{result.title}</td>
                                  <td>
                                    <a
                                      href={result.url}
                                      target="_blank"
                                      rel="noopener noreferrer"
                                      className="url-link"
                                    >
                                      View Document →
                                    </a>
                                  </td>
                                </tr>
                              ))}
                            </tbody>
                          </table>
                        </div>
                      </>
                    )}
                  </div>
                </div>
              </section>
            )}
          </>
        )}

        {currentView === "batch" && (
          <section className="batch-section">
            <div className="card">
              <div className="card-header">
                <h2 className="card-title">Batch Search via CSV</h2>
                <p className="card-description">
                  Upload a CSV file with multiple census documents to search.
                  The system will perform cascading searches for each row in
                  parallel.
                </p>
              </div>
              <div className="card-content">
                <div className="batch-upload-section">
                  <div className="upload-info">
                    <h3>CSV Format Requirements:</h3>
                    <ul>
                      <li>
                        <strong>Required columns:</strong> "Title (In English)",
                        "Country"
                      </li>
                      <li>
                        <strong>Optional columns:</strong> "Original title",
                        "Province", "Date/Year of census", "Author/Publisher",
                        "Volume number (if applicable)", "Colonising power"
                      </li>
                    </ul>
                    <div className="sample-download">
                      {/* <p>
                        <strong>Tip:</strong> You can use the test_data.csv file
                        in the Backend/GoogleSearch_WS/testcsv/ folder as a
                        reference.
                      </p> */}
                    </div>
                  </div>

                  <div className="file-upload-container">
                    <label htmlFor="csv-upload" className="file-upload-label">
                      <span className="upload-icon">📁</span>
                      <span className="upload-text">
                        {csvFile ? csvFile.name : "Choose CSV File"}
                      </span>
                    </label>
                    <input
                      type="file"
                      id="csv-upload"
                      accept=".csv"
                      onChange={handleFileChange}
                      className="file-upload-input"
                    />
                  </div>

                  <div className="button-group">
                    <button
                      onClick={handleBatchSearch}
                      className="search-button"
                      disabled={batchLoading || !csvFile}
                    >
                      <span className="button-icon">🚀</span>
                      {batchLoading ? "Processing..." : "Start Batch Search"}
                    </button>
                    <button
                      onClick={() => {
                        setCsvFile(null);
                        setBatchResults(null);
                        setBatchError(null);
                      }}
                      className="reset-button"
                      disabled={batchLoading}
                    >
                      <span className="button-icon">🔄</span>
                      Reset
                    </button>
                  </div>
                </div>

                {batchError && (
                  <div className="error-message">
                    <span className="error-icon">⚠️</span>
                    <div>
                      <strong>Error:</strong> {batchError}
                    </div>
                  </div>
                )}

                {batchLoading && (
                  <div className="loading-section">
                    <div className="loading-spinner"></div>
                    <p>
                      Processing batch search... This may take a while depending
                      on the number of rows.
                    </p>
                  </div>
                )}

                {batchResults && (
                  <div className="batch-results-summary">
                    <h3>Batch Search Summary</h3>
                    <div className="summary-stats">
                      <div className="stat-card">
                        <span className="stat-icon">📊</span>
                        <div>
                          <div className="stat-value">
                            {batchResults.total_rows}
                          </div>
                          <div className="stat-label">Total Rows</div>
                        </div>
                      </div>
                      <div className="stat-card success">
                        <span className="stat-icon">✅</span>
                        <div>
                          <div className="stat-value">
                            {batchResults.successful_searches}
                          </div>
                          <div className="stat-label">Successful</div>
                        </div>
                      </div>
                      <div className="stat-card error">
                        <span className="stat-icon">❌</span>
                        <div>
                          <div className="stat-value">
                            {batchResults.failed_searches}
                          </div>
                          <div className="stat-label">Failed</div>
                        </div>
                      </div>
                      <div className="stat-card">
                        <span className="stat-icon">⏱️</span>
                        <div>
                          <div className="stat-value">
                            {batchResults.total_time_taken.toFixed(2)}s
                          </div>
                          <div className="stat-label">Total Time</div>
                        </div>
                      </div>
                    </div>

                    <div className="download-section">
                      <button
                        onClick={downloadBatchResultsCSV}
                        className="download-button"
                      >
                        <span className="button-icon">📥</span>
                        Download Results (CSV)
                      </button>
                    </div>

                    <div className="batch-results-table-container">
                      <table className="results-table">
                        <thead>
                          <tr>
                            <th>Row</th>
                            <th>Title</th>
                            <th>Country</th>
                            <th>Phase</th>
                            <th>Status</th>
                            <th>Results</th>
                          </tr>
                        </thead>
                        <tbody>
                          {batchResults.results.map((result, index) => (
                            <tr key={index}>
                              <td className="index-cell">
                                {result.row_number}
                              </td>
                              <td className="title-cell">
                                {result.search_input.english_title}
                              </td>
                              <td>{result.search_input.country}</td>
                              <td>
                                {result.search_result ? (
                                  <span className="badge badge-primary">
                                    {result.search_result.phase.toUpperCase()}
                                  </span>
                                ) : (
                                  <span className="badge badge-secondary">
                                    N/A
                                  </span>
                                )}
                              </td>
                              <td>
                                {result.error ? (
                                  <span className="status-badge error">
                                    ❌ Failed
                                  </span>
                                ) : result.search_result?.status ===
                                  "no_results" ? (
                                  <span className="status-badge warning">
                                    ⚠️ No Results
                                  </span>
                                ) : (
                                  <span className="status-badge success">
                                    ✅ Success
                                  </span>
                                )}
                              </td>
                              <td>
                                {result.error ? (
                                  <span className="error-text">
                                    {result.error}
                                  </span>
                                ) : result.search_result?.results?.length >
                                  0 ? (
                                  <div className="result-links">
                                    {result.search_result.results
                                      .slice(0, 2)
                                      .map((res, idx) => {
                                        const url = Array.isArray(res)
                                          ? res[1]
                                          : res.url;
                                        const title =
                                          Array.isArray(res) && res[2]
                                            ? res[2]
                                            : "View";
                                        return (
                                          <a
                                            key={idx}
                                            href={url}
                                            target="_blank"
                                            rel="noopener noreferrer"
                                            className="url-link"
                                            title={title}
                                          >
                                            Result {idx + 1} →
                                          </a>
                                        );
                                      })}
                                    {result.search_result.results.length >
                                      2 && (
                                      <span className="more-results">
                                        +
                                        {result.search_result.results.length -
                                          2}{" "}
                                        more
                                      </span>
                                    )}
                                  </div>
                                ) : (
                                  <span className="no-results-text">
                                    No results found
                                  </span>
                                )}
                              </td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </section>
        )}

        {currentView === "history" && (
          <section className="history-section">
            <div className="card">
              <div className="card-header">
                <h2 className="card-title">Search History</h2>
                <p className="card-description">
                  View and manage your saved searches. Click on any search to
                  load it.
                </p>
              </div>
              <div className="card-content">
                {savedSearches.length === 0 ? (
                  <div className="no-results">
                    <span className="no-results-icon">📚</span>
                    <p>No saved searches yet.</p>
                    <p className="no-results-hint">
                      Perform a search and click "Save Search" to save it for
                      later.
                    </p>
                  </div>
                ) : (
                  <div className="history-list">
                    {savedSearches.map((search) => (
                      <div key={search.id} className="history-item">
                        <div className="history-item-header">
                          <h3 className="history-item-title">{search.name}</h3>
                          <div className="history-item-actions">
                            <button
                              onClick={() => loadSearch(search)}
                              className="history-load-button"
                              title="Load this search"
                            >
                              📂 Load
                            </button>
                            <button
                              onClick={() => deleteSearch(search.id)}
                              className="history-delete-button"
                              title="Delete this search"
                            >
                              🗑️ Delete
                            </button>
                          </div>
                        </div>
                        <div className="history-item-details">
                          <span className="history-item-date">
                            🕒 {new Date(search.timestamp).toLocaleString()}
                          </span>
                          <span className="history-item-phase">
                            {search.results?.phase
                              ? `Phase: ${search.results.phase.toUpperCase()}`
                              : "No results"}
                          </span>
                          <span className="history-item-results">
                            {search.results?.results
                              ? `${
                                  Array.isArray(search.results.results)
                                    ? search.results.results.length
                                    : 0
                                } results`
                              : "0 results"}
                          </span>
                        </div>
                        <div className="history-item-filters">
                          <strong>Filters:</strong>
                          <div className="filter-chips">
                            {search.filters.englishTitle && (
                              <span className="filter-chip">
                                📖 {search.filters.englishTitle}
                              </span>
                            )}
                            {search.filters.country && (
                              <span className="filter-chip">
                                🌍 {search.filters.country}
                              </span>
                            )}
                            {search.filters.cite && (
                              <span className="filter-chip">
                                📅 {search.filters.cite}
                              </span>
                            )}
                            {search.filters.province && (
                              <span className="filter-chip">
                                📍 {search.filters.province}
                              </span>
                            )}
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          </section>
        )}

        {currentView === "api-docs" && (
          <section className="api-docs-section">
            <div className="card">
              <div className="card-header">
                <h2 className="card-title">API Documentation</h2>
                <p className="card-description">
                  Interactive API documentation with Swagger UI
                </p>
              </div>
              <div className="card-content">
                <div className="api-docs-content">
                  <div className="api-docs-intro">
                    <h3>🚀 Interactive API Documentation</h3>
                    <p>
                      The Census PDF Finder API provides comprehensive
                      documentation through an interactive Swagger UI interface.
                      This allows you to explore all available endpoints, view
                      request/response schemas, and even test API calls directly
                      from your browser.
                    </p>
                  </div>

                  <div className="api-docs-link-section">
                    <h4>Access the Documentation:</h4>
                    <a
                      href="http://localhost:8000/docs"
                      target="_blank"
                      rel="noopener noreferrer"
                      className="api-docs-link"
                    >
                      <span className="link-icon">📖</span>
                      <span className="link-text">
                        http://localhost:8000/docs
                      </span>
                      <span className="link-arrow">→</span>
                    </a>
                    <p className="api-docs-note">
                      <strong>Note:</strong> Make sure the backend server is
                      running on port 8000
                    </p>
                  </div>

                  <div className="api-docs-features">
                    <h4>What's Available:</h4>
                    <ul className="features-list">
                      <li>
                        <span className="feature-icon">📋</span>
                        <div>
                          <strong>OpenAPI/Swagger Specification</strong>
                          <p>
                            Complete API specification following OpenAPI 3.0
                            standards
                          </p>
                        </div>
                      </li>
                      <li>
                        <span className="feature-icon">🔍</span>
                        <div>
                          <strong>Interactive Testing</strong>
                          <p>
                            Test API endpoints directly from the documentation
                            interface
                          </p>
                        </div>
                      </li>
                      <li>
                        <span className="feature-icon">📦</span>
                        <div>
                          <strong>Request/Response Schemas</strong>
                          <p>
                            Detailed schemas for all request bodies and response
                            formats
                          </p>
                        </div>
                      </li>
                      <li>
                        <span className="feature-icon">🔐</span>
                        <div>
                          <strong>Authentication Details</strong>
                          <p>
                            Information about API authentication and
                            authorization
                          </p>
                        </div>
                      </li>
                      <li>
                        <span className="feature-icon">💡</span>
                        <div>
                          <strong>Example Requests</strong>
                          <p>Sample requests and responses for each endpoint</p>
                        </div>
                      </li>
                    </ul>
                  </div>

                  <div className="api-docs-endpoints">
                    <h4>Available Endpoints:</h4>
                    <div className="endpoints-grid">
                      <div className="endpoint-card">
                        <span className="endpoint-method post">POST</span>
                        <span className="endpoint-path">
                          /api/cascading-search
                        </span>
                        <p className="endpoint-desc">
                          Perform cascading search across libraries, bureaus,
                          and web
                        </p>
                      </div>
                      <div className="endpoint-card">
                        <span className="endpoint-method post">POST</span>
                        <span className="endpoint-path">/api/batch-search</span>
                        <p className="endpoint-desc">
                          Upload CSV file for batch processing of multiple
                          searches
                        </p>
                      </div>
                      <div className="endpoint-card">
                        <span className="endpoint-method get">GET</span>
                        <span className="endpoint-path">/api/health</span>
                        <p className="endpoint-desc">Check API health status</p>
                      </div>
                      <div className="endpoint-card">
                        <span className="endpoint-method get">GET</span>
                        <span className="endpoint-path">/api/libraries</span>
                        <p className="endpoint-desc">
                          Get list of all libraries
                        </p>
                      </div>
                      <div className="endpoint-card">
                        <span className="endpoint-method get">GET</span>
                        <span className="endpoint-path">/api/filters</span>
                        <p className="endpoint-desc">
                          Get list of all saved filters
                        </p>
                      </div>
                    </div>
                  </div>

                  <div className="api-docs-help">
                    <h4>Need Help?</h4>
                    <p>
                      For detailed information about each endpoint, parameter
                      descriptions, and to try out the API in real-time, visit
                      the{" "}
                      <a
                        href="http://localhost:8000/docs"
                        target="_blank"
                        rel="noopener noreferrer"
                      >
                        interactive documentation
                      </a>
                      .
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </section>
        )}
      </main>

      {/* Save Search Modal */}
      {showSaveModal && (
        <div className="modal-overlay" onClick={() => setShowSaveModal(false)}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h3>Save Search</h3>
              <button
                className="modal-close"
                onClick={() => setShowSaveModal(false)}
              >
                ✕
              </button>
            </div>
            <div className="modal-content">
              <label htmlFor="searchName">Search Name:</label>
              <input
                type="text"
                id="searchName"
                value={searchName}
                onChange={(e) => setSearchName(e.target.value)}
                placeholder="e.g., Argentina Census 1869"
                className="modal-input"
                autoFocus
                onKeyPress={(e) => {
                  if (e.key === "Enter") {
                    confirmSaveSearch();
                  }
                }}
              />
            </div>
            <div className="modal-footer">
              <button
                className="modal-button modal-button-cancel"
                onClick={() => setShowSaveModal(false)}
              >
                Cancel
              </button>
              <button
                className="modal-button modal-button-confirm"
                onClick={confirmSaveSearch}
              >
                Save
              </button>
            </div>
          </div>
        </div>
      )}

      <footer className="footer">
        <p>Document Search API v1.0.0</p>
      </footer>
    </div>
  );
}

export default App;
