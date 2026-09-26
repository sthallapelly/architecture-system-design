# Design an Order Management System

> **Status:** 🟡 Starter problem  
> **Difficulty:** Advanced

Design an order workflow involving:

```text
Order
  ↓
Inventory
  ↓
Payment
  ↓
Shipping
  ↓
Fulfillment
```

Then introduce:

- payment failure
- inventory shortage
- duplicate order submission
- service timeout
- event loss
- duplicate events
- cancellation
- partial failure
- regional outage

Key areas:

- Saga
- Outbox
- Idempotency
- Event-driven architecture
- State machines
- Consistency
- Observability
