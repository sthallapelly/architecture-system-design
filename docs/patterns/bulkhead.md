# Bulkhead

> **Status:** 🟡 Starter note

## Problem

A failure or overload in one workload consumes shared resources and impacts unrelated workloads.

## Core idea

Isolate resources so failure remains contained.

Examples:

- thread pools
- connection pools
- queues
- compute capacity
- tenant cells

## Key trade-off

Isolation improves resilience but can reduce overall resource utilization.
