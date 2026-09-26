# Consistency Models

> **Status:** 🟡 Starter note  
> **Track:** System Design Fundamentals

## Core question

After data changes in one location, **when and where must other readers observe that change?**

## Concepts to study

- Strong consistency
- Eventual consistency
- Read-after-write consistency
- Monotonic reads
- Causal consistency
- Session consistency
- CAP theorem
- PACELC
- Replication lag
- Conflict resolution

## Architectural decision

Do not ask:

> "Which database is better?"

Ask:

> "What consistency guarantees does this business operation actually require?"

## Design exercise

Design a globally distributed customer-profile service.

Compare:

1. Strongly consistent design
2. Eventually consistent design

Analyze:

- latency
- availability
- user experience
- failure behavior
- implementation complexity
- cost

## Questions

1. Can every operation use strong consistency?
2. What business data can tolerate stale reads?
3. What happens during a network partition?
4. How are conflicting writes handled?
