# System Design Case Studies {#system-design-problems}

System design requires decisions across service boundaries, data ownership, consistency, and failure recovery. These case studies establish concrete system contexts and the requirements and trade-offs that shape their architectures.

- [Payment System](payment-system.md) — Payment correctness under retries, uncertain outcomes, and provider failures.
- [Notification System](notification-system.md) — Delivery across channels with provider limits, user preferences, and duplicate processing.
- [Distributed Cache](distributed-cache.md) — Partitioning, replication, eviction, and recovery under node failure.
- [Order Management](order-management.md) — Coordination across inventory, payment, shipping, and fulfillment.

The current pages define the design scenarios and key considerations; they do not present completed implementations or measured production results.
