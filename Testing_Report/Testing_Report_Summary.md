# System Testing Summary — Group 03

**Date:** 10 October 2025  
**Tests Conducted:**  

- **Test 1:** Web Search  
- **Test 2:** Library + Web Combined Search  

## Objective
To assess the retrieval system’s accuracy, speed, and reliability using both Web and Library searches, and identify areas for improvement before full rollout.

## Test Results Overview

| Metric | Test 1 (Web) | Test 2 (Library) |
|--------|---------------|-------------------------|
| Dataset size | 60 docs | 31 docs |
| Success rate | **98%** | **94% (Library)** |
| Avg. time/query | **80s** | **124s (Library)** |
| Main issue | 12 unreachable links | 2 year mismatches |
| Stability | High | High, slower runtime |

## Key Findings
- Web search is faster and consistent but depends on external site availability.  
- Library search yields highly accurate metadata, but mismatched publication years caused two minor errors.  
- Using Web as fallback ensures full coverage at the cost of longer processing time.

## Conclusion
The system performs reliably across both Web and Library environments.  
With small adjustments to error handling and metadata consistency, it is ready for large-scale deployment.