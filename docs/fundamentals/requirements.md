# Requirements & Constraints

Explicit engineering requirements turn an ambiguous system-design request into constraints that can guide architecture decisions.

## Questions to answer

### Functional requirements

What must the system do?

### Non-functional requirements

What qualities must the system provide?

Examples:

- Availability
- Latency
- Throughput
- Durability
- Security
- Scalability
- Compliance
- Cost constraints

### Constraints

What limits the solution?

Examples:

- Existing systems
- Budget
- Data residency
- Migration constraints
- Team capabilities
- Technology restrictions
- Regulatory requirements

## Architect's habit

Before designing components, clarify:

> **Who uses the system, what do they need, at what scale, with what reliability and latency, under what constraints?**

## Design scenario {#design-exercise}

Take a vague requirement:

> "Design an order platform."

The architecture depends on explicit functional requirements and measurable non-functional requirements.

## Architecture questions

1. Which requirements are mandatory?
2. Which requirements are negotiable?
3. Which requirements conflict?
4. Which requirements drive architecture?
5. Which assumptions must be validated?
