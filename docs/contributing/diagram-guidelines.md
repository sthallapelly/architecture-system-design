# Architecture Diagram Guidelines

Architecture diagrams in this project should explain a design decision,
communication path, security boundary, deployment boundary, or failure boundary.

## General principles

- Prefer focused diagrams over large diagrams containing every component.
- A diagram should communicate one primary architectural idea.
- Use official AWS Architecture Icons for AWS services and resources.
- Do not approximate or invent AWS service icons.
- Use simple neutral shapes/icons for users, enterprise systems, and generic components.
- Include AWS Account, Region, VPC, subnet, or trust boundaries only when they matter to the architecture being explained.
- Do not add infrastructure simply to make a diagram look more complete.

## Communication flows

- Arrows must reflect the actual direction in which connections are initiated.
- Label protocols and ports when they matter to the design.
- Use short labels such as `HTTPS : 443`, `TCP : 3306`, or `DNS`.
- Use numbered flows when a sequence would otherwise be difficult to follow.
- Do not imply bidirectional connection initiation merely because traffic can return over an established connection.

## AWS diagrams

Use official AWS Architecture Icons when representing AWS services.

Examples:

- AWS Systems Manager
- Amazon EC2
- Amazon RDS
- AWS Direct Connect
- AWS Site-to-Site VPN
- AWS PrivateLink / VPC endpoints
- Amazon Route 53
- VPC

Service icons should identify architecture components, not decorate the diagram.

## Boundaries

Use boundaries deliberately.

Examples include:

- Enterprise network
- AWS Cloud
- AWS Account
- Region
- VPC
- Private subnet
- Security or trust boundary

Do not show a subnet merely because an EC2 instance normally belongs to one.
Show it when subnet placement, routing, availability, or security matters to
the discussion.

## Text

Keep diagram text concise.

Prefer:

`SSM Agent`

`HTTPS : 443`

`Interface VPC Endpoint`

over paragraphs of explanation inside the diagram.

Detailed explanation belongs in the surrounding article.

## Diagram complexity

Prefer:

one concept → one diagram

over:

one article → one large diagram

A complex architecture article may therefore contain several smaller diagrams.

## Source and output

Store editable diagram source and web-ready output.

Recommended structure:

docs/assets/diagrams/<topic>/
    diagram-name.drawio
    diagram-name.svg

Use SVG for the website whenever practical because it scales cleanly.

The `.drawio` file is the editable source of truth.

## Visual consistency

Diagrams across the site should use a consistent visual language:

- AWS official icons for AWS resources
- simple shapes for generic components
- consistent boundary styles
- consistent arrow styles
- concise labels
- similar spacing and alignment

Avoid decorative styling, excessive colors, shadows, gradients, or unnecessary
visual effects.

The goal is professional architecture documentation, not presentation artwork.

## Final review

Before publishing a diagram, verify:

1. What architectural idea does this diagram explain?
2. Are all displayed components necessary?
3. Are connection directions technically correct?
4. Are protocols and ports correct where shown?
5. Are AWS boundaries represented correctly?
6. Could a reader misunderstand any connection?
7. Does the diagram remain readable at normal webpage width?
8. Does the surrounding article explain details that do not belong in the diagram?