---
name: performance-review
description: Use when analyzing performance of ctxpack — evaluates complexity, memory usage, scalability, and optimization opportunities
---

# Performance Review

## Purpose
Analyze the performance characteristics of ctxpack: time complexity, memory usage, scalability with large codebases, and optimization opportunities.

## Inputs
- ctxpack.py implementation

## Outputs
- Complexity analysis (time and space)
- Scalability assessment
- Bottleneck identification
- Optimization recommendations

## Workflow
1. Analyze scan_files: O(N) where N = files scanned, each file stat'd
2. Analyze rank_files: O(N * K) where K = task keywords, each file read
3. Analyze bundle_files: O(M) where M = ranked files considered
4. Analyze build_tree: O(N) directory walk
5. Identify the bottleneck: file reading (I/O bound)
6. Check memory: all file contents loaded for ranking
7. Evaluate with large directory (10,000+ files)

## Complexity
- `scan_files`: O(N) disk I/O, O(N) memory for file list
- `rank_files`: O(N) file reads + O(N * K) string matching
- `bundle_files`: O(M) string concatenation
- `build_tree`: O(N) directory listing
- Overall: O(N) time, O(total file content size) memory

## Limitations
- Cannot benchmark without running against real codebases
- Memory analysis is approximate without heap profiling

## Success Criteria
- [ ] Complexity is documented
- [ ] Bottlenecks are identified
- [ ] Recommendations are actionable
- [ ] No obvious performance anti-patterns
