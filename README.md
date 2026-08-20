\# Graph Database Benchmark



Benchmark comparison of Neo4j, Memgraph, Apache AGE, and CognoDB using the cit-HepPh citation dataset.



\## Dataset



Source: cit-HepPh citation network.



Local prepared dataset:



\- Nodes: 34,546

\- Relationships: 421,578

\- Node type: `Paper`

\- Relationship type: `CITES`



The same node and relationship structure is used for the completed local graph database benchmarks.



\## Databases



\- Neo4j

\- Memgraph

\- Apache AGE

\- Kuzu

\- CognoDB Cloud



\## Benchmarks



The benchmark suite measures:



\- Point lookup

\- Indexed/filtered lookup

\- 1-hop traversal

\- 2-hop traversal

\- 3-hop traversal

\- Aggregation

\- Mixed read/write throughput

\- Concurrent query execution

\- Ingest throughput

\- Resource/footprint measurement



Latency metrics:



\- P50

\- P95

\- Mean



Concurrency levels:



\- 1

\- 5

\- 10

\- 25



Each benchmark uses a warm-up phase followed by 100 measured iterations.



\## Running



Create and activate a Python virtual environment and install the required packages.



Set database credentials through environment variables. Do not commit passwords, tokens, or private connection information.



Example:



```powershell

$env:PYTHONPATH = "."

python benchmark/run\_neo4j.py 9506257

python benchmark/run\_memgraph.py 9506257

python benchmark/run\_age.py 9506257

python benchmark/concurrency.py

## Results Matrix



| Metric | Neo4j | Memgraph | Apache AGE | Kuzu | CognoDB |

|---|---|---|---|---|---|

| Ingest throughput | Measured | Measured | Measured | Measured | Partial |

| 1-hop latency | Measured | Measured | Measured | Measured | N/A |

| 2-hop latency | Measured | Measured | Measured | Measured | N/A |

| 3-hop latency | Measured | Measured | Measured | Measured | N/A |

| Point lookup | Measured | Measured | Measured | Measured | N/A |

| Indexed/filtered lookup | N/A | N/A | N/A | N/A | N/A |

| Aggregation | Measured | Measured | Measured | Measured | N/A |

| Mixed read/write throughput | N/A | N/A | N/A | N/A | N/A |

| Concurrent query throughput | Measured | Measured | Measured | N/A | N/A |

| Resource/footprint | N/A | N/A | N/A | N/A | Partial |



\### Measurement caveats



`N/A` means the metric was not measured in the completed benchmark run.



CognoDB was partially loaded with 34,546 nodes and 84,750 relationships. The full dataset contains 421,578 relationships.



Kuzu was fully loaded with 34,546 nodes and 421,578 relationships.



No missing benchmark values are fabricated.


## Results Matrix

| Metric | Neo4j | Memgraph | Apache AGE | Kuzu | CognoDB |
|---|---|---|---|---|---|
| Ingest throughput | Measured | Measured | Measured | Measured | Partial |
| 1-hop latency | Measured | Measured | Measured | Measured | N/A |
| 2-hop latency | Measured | Measured | Measured | Measured | N/A |
| 3-hop latency | Measured | Measured | Measured | Measured | N/A |
| Point lookup | Measured | Measured | Measured | Measured | N/A |
| Indexed/filtered lookup | N/A | N/A | N/A | N/A | N/A |
| Aggregation | Measured | Measured | Measured | Measured | N/A |
| Mixed read/write throughput | N/A | N/A | N/A | N/A | N/A |
| Concurrent query throughput | Measured | Measured | Measured | N/A | N/A |
| Resource/footprint | N/A | N/A | N/A | N/A | Partial |

### Measurement caveats

`N/A` means the metric was not measured in the completed benchmark run.

CognoDB was partially loaded with 34,546 nodes and 84,750 relationships. The full dataset contains 421,578 relationships.

Kuzu was fully loaded with 34,546 nodes and 421,578 relationships.

No missing benchmark values are fabricated.
