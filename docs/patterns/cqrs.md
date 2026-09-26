# CQRS

> **Status:** 🟡 Starter note

## Core idea

Separate the models or paths used to change state from those used to read state.

```text
Commands → Write Model → Events
                              |
                              v
                         Read Model
                              |
                              v
                           Queries
```

## Important caution

CQRS introduces additional models and synchronization complexity. It should solve a real problem rather than be applied automatically.
