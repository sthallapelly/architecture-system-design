# Saga

> **Status:** 🟡 Starter note

## Problem

A business transaction spans multiple independently owned services or databases.

## Core idea

Break the workflow into local transactions and define compensating actions for failures.

## Styles

- Choreography
- Orchestration

## Example

```text
Order
  |
  v
Reserve Inventory
  |
  v
Authorize Payment
  |
  v
Create Shipment
```

If payment fails:

```text
Payment failed
      |
      v
Release Inventory
      |
      v
Cancel Order
```

## Questions for deeper study

1. What does compensation actually guarantee?
2. When is orchestration preferable?
3. How do retries interact with compensation?
4. How do you observe a long-running Saga?
