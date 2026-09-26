# Availability & Reliability

> **Status:** 🟡 Starter note  
> **Track:** System Design Fundamentals

## Distinguish the terms

**Availability** asks whether the service is usable when requested.

**Reliability** is broader: the ability of a system to perform correctly and consistently over time.

**Durability** concerns whether stored data remains intact.

## Key concepts

- Availability targets
- SLA
- SLO
- SLI
- Error budgets
- MTTR
- MTBF
- RTO
- RPO
- Fault domains
- Redundancy
- Failover
- Graceful degradation

## Design questions

1. What does 99.9% availability mean operationally?
2. What changes when the target becomes 99.99%?
3. Which failure domains must be isolated?
4. What is the recovery strategy?
5. What data can be lost?
6. How quickly must service recover?

## Design exercise

Design a service with a 99.99% availability target and an RPO of five minutes.

Identify:

- failure domains
- replication strategy
- recovery process
- monitoring
- operational risks
