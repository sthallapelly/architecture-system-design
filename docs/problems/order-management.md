# Order Management {#design-an-order-management-system}

The scenario spans an order workflow involving:

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

## Failure scenarios

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
