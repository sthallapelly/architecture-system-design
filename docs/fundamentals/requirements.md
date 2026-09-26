# Requirements & Constraints

> **Status:** 🟡 Starter note  
> **Track:** System Design Fundamentals

This topic will establish how to turn an ambiguous system-design question into explicit engineering requirements.

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

## Design exercise

Take a vague requirement:

> "Design an order platform."

Turn it into at least 10 explicit functional and non-functional requirements.

## Questions for deeper study

1. Which requirements are mandatory?
2. Which requirements are negotiable?
3. Which requirements conflict?
4. Which requirements drive architecture?
5. Which assumptions must be validated?
