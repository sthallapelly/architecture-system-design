# Circuit Breaker

> **Status:** 🟡 Starter note

## Problem

Repeated calls to an unhealthy dependency can amplify failure and exhaust resources.

## States

```text
CLOSED → OPEN → HALF-OPEN → CLOSED
```

## Questions

- What failure threshold should open the circuit?
- How long should it remain open?
- What fallback exists?
- How does this interact with retries?
