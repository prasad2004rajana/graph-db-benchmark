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

\- CognoDB Cloud



\## Benchmarks



The benchmark suite measures:



\- Point lookup

\- 1-hop traversal

\- 2-hop traversal

\- 3-hop traversal

\- Aggregation

\- Concurrent query execution



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

