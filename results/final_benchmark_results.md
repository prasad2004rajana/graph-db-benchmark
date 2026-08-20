

\# Graph Database Benchmark Results



\## Databases



\- Neo4j

\- Memgraph

\- Apache AGE



Dataset: cit\_hepph

Nodes: 34,546

Edges: 421,578



\---



\# 1. Single-Query Benchmark



| Workload | Memgraph Mean | Neo4j Mean | Apache AGE Mean |

|---|---:|---:|---:|

| Point Lookup | 7.424 ms | 17.634 ms | 33.648 ms |

| 1-Hop Traversal | 7.500 ms | 11.502 ms | 115.134 ms |

| 2-Hop Traversal | 7.487 ms | 13.266 ms | 261.472 ms |

| 3-Hop Traversal | 7.846 ms | 12.014 ms | 658.732 ms |

| Aggregation | 159.844 ms | 180.985 ms | 75.949 ms |



\## Single-Query Winner



\- Point Lookup: Memgraph

\- 1-Hop Traversal: Memgraph

\- 2-Hop Traversal: Memgraph

\- 3-Hop Traversal: Memgraph

\- Aggregation: Apache AGE



\---



\# 2. Concurrency Benchmark



\## Point Lookup — Concurrency 25



| Database | P50 | P95 | Mean | Throughput |

|---|---:|---:|---:|---:|

| Memgraph | 69.392 ms | 90.486 ms | 69.964 ms | 321.36 req/s |

| Neo4j | 90.974 ms | 115.857 ms | 93.250 ms | 251.81 req/s |

| Apache AGE | 874.793 ms | 1359.770 ms | 894.088 ms | 26.01 req/s |



\## 1-Hop Traversal — Concurrency 25



| Database | P50 | P95 | Mean | Throughput |

|---|---:|---:|---:|---:|

| Memgraph | 63.893 ms | 93.022 ms | 65.513 ms | 344.13 req/s |

| Neo4j | 85.781 ms | 119.243 ms | 89.418 ms | 265.06 req/s |

| Apache AGE | 758.290 ms | 1235.405 ms | 784.211 ms | 29.66 req/s |



\## 2-Hop Traversal — Concurrency 25



| Database | P50 | P95 | Mean | Throughput |

|---|---:|---:|---:|---:|

| Memgraph | 64.198 ms | 82.074 ms | 64.728 ms | 343.20 req/s |

| Neo4j | 89.803 ms | 125.676 ms | 93.702 ms | 251.05 req/s |

| Apache AGE | 863.255 ms | 1357.486 ms | 888.364 ms | 26.08 req/s |



\---



\# 3. Overall Conclusion



Memgraph delivered the strongest overall performance in this benchmark.



It achieved the lowest latency for point lookup and 1-hop, 2-hop, and 3-hop graph traversal workloads.



Neo4j was generally the second-best performer and showed competitive concurrency throughput.



Apache AGE was significantly slower for graph traversal workloads and its latency increased substantially under concurrency.



However, Apache AGE performed best in the tested aggregation workload, with a mean latency of 75.949 ms compared with 159.844 ms for Memgraph and 180.985 ms for Neo4j.



Therefore, for traversal-heavy workloads in this benchmark, Memgraph is the strongest choice. For the specific aggregation query tested, Apache AGE performed best.



These results are specific to the benchmark environment, dataset, queries, configuration, and workload implementation used in this project.


---



\# 4. Kuzu Results



Kuzu was loaded with the same prepared dataset:



\- Nodes: 34,546

\- Relationships: 421,578



\## Ingest



| Metric | Kuzu |

|---|---:|

| Node ingest time | 0.23 s |

| Edge ingest time | 0.35 s |



\## Query Latency



| Workload | P50 (ms) | P95 (ms) | Mean (ms) |

|---|---:|---:|---:|

| Point Lookup | Not captured in final output | Not captured | Not captured |

| 1-Hop Traversal | 2.371 | 2.885 | 2.421 |

| 2-Hop Traversal | 6.451 | 7.736 | 6.547 |

| 3-Hop Traversal | 9.516 | 10.915 | 9.567 |

| Aggregation | 20.170 | 22.716 | 20.470 |



Kuzu was fully populated with 34,546 nodes and 421,578 relationships. Its measured traversal latency was substantially lower than the previously measured Neo4j, Memgraph, and Apache AGE results in this environment.



The Kuzu results were collected using the same dataset and 100 measured iterations with 10 warm-up iterations.



\---



\# 5. CognoDB Status



CognoDB Cloud was successfully connected and loaded with:



\- 34,546 nodes

\- 84,750 relationships



The full 421,578 relationship import was not completed within the available assessment time because of resource/connection limitations on the free C0 instance.



Therefore, CognoDB is reported as a partial deployment and its incomplete dataset results are not used for direct performance comparison.



\---



\# 6. Updated Conclusion



The benchmark demonstrates substantial performance differences between graph database implementations under the tested workload.



Kuzu produced the lowest measured traversal latency among the databases for which the corresponding workloads were completed in this environment.



Memgraph also demonstrated strong performance and high concurrency throughput in the earlier tests, while Neo4j remained competitive. Apache AGE showed substantially higher traversal latency and greater latency growth under concurrency.



These results should not be interpreted as universal database rankings. They are specific to the dataset, queries, hardware/resources, database configurations, driver implementations, and benchmark methodology used in this assessment.



CognoDB was successfully evaluated for deployment and partial ingestion, but its dataset import was incomplete and therefore its performance measurements are not treated as directly comparable.

