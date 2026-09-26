# Scalability, Latency & Throughput

> **Status:** 🟡 Starter note  
> **Track:** System Design Fundamentals

## Core distinction

- **Latency:** How long one operation takes.
- **Throughput:** How much work the system processes per unit time.
- **Concurrency:** How many operations are in progress at once.
- **Scalability:** How system capacity changes as demand changes.

## Architect's questions

- What is average traffic?
- What is peak traffic?
- What is the expected growth?
- What is the latency target?
- Which operations are CPU-bound?
- Which are I/O-bound?
- Where is the bottleneck?
- Can the bottleneck scale horizontally?

## Capacity estimation

Practice translating:

```text
Users
  ↓
Requests / user / day
  ↓
Requests / day
  ↓
Average RPS
  ↓
Peak RPS
  ↓
Compute / storage / network requirements
```

## Design exercise

Design an API that must support:

- 10 million users
- 1 million daily active users
- 20 requests per active user per day
- 10× peak traffic compared with the daily average

Calculate approximate average and peak requests per second and identify likely bottlenecks.

## Further topics

- Little's Law
- Horizontal vs vertical scaling
- Load balancing
- Queuing
- Backpressure
- Capacity planning
