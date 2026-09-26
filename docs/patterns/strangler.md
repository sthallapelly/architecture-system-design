# Strangler Fig Pattern

> **Status:** 🟡 Starter note

## Problem

A legacy system needs to evolve without a risky big-bang rewrite.

## Core idea

Gradually route capabilities to new implementations while the legacy system continues operating.

```text
Clients
   |
   v
Routing / Facade
   |
   +---- New capability
   |
   +---- Legacy capability
```

## Questions

1. How do you choose the migration boundary?
2. How do you handle shared data?
3. How do you validate parity?
4. When should the legacy system finally be retired?
