# Transactional Outbox

> **Status:** 🟡 Starter note

## Problem

A service updates its database and must publish an event. A failure between these two operations can create inconsistency.

## Core idea

Store the business change and an outbound event record in the same database transaction. A separate publisher later delivers the event.

```text
Application
    |
    +---- Business DB transaction ----+
    |                                  |
    |                           Outbox record
    |                                  |
    +----------------------------------+
                       |
                       v
                 Outbox Publisher
                       |
                       v
                 Event Broker
                       |
                       v
                   Consumers
```

## Important limitation

Outbox does not automatically provide exactly-once processing.

Consumers still need to handle duplicate delivery safely.

## Questions for deeper study

1. What happens if the publisher crashes after publishing?
2. How is the outbox cleaned up?
3. How do you preserve event ordering?
4. How do you scale the publisher?
5. What happens when the broker is unavailable?
