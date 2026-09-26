# Design a Payment System

> **Status:** 🟡 Starter problem  
> **Difficulty:** Advanced

## Problem

Design a payment API that must safely process customer payments despite retries, timeouts, duplicate requests, and downstream failures.

## Initial requirements

- Customers can initiate payments.
- A payment must not be charged twice because of client retries.
- Payment status must be queryable.
- External payment providers may timeout or become unavailable.
- The system must provide an audit trail.

## Do not jump directly to implementation.

First determine:

1. Functional requirements
2. Non-functional requirements
3. Scale
4. Consistency requirements
5. Failure scenarios
6. Idempotency strategy
7. Transaction boundaries
8. Reconciliation strategy

## Follow-up scenarios

- Client times out but payment succeeds.
- Payment provider returns an unknown result.
- Application crashes after receiving provider confirmation.
- Event is delivered twice.
- Event is delivered out of order.
- Payment provider is unavailable for 30 minutes.
- Regional failure occurs during payment processing.

## Key concepts likely involved

- Idempotency
- Distributed transactions
- Outbox
- Event-driven architecture
- Retries
- Reconciliation
- State machines
- Auditability
