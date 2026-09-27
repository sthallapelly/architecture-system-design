# Private Systems Manager Connectivity over Direct Connect

## Architecture problem

An enterprise administrator needs AWS Systems Manager / Session Manager access to EC2 instances from an enterprise network. An existing Direct Connect path must carry the enterprise-to-AWS management connectivity without relying on the public Internet.

## Scope and boundaries

The design scope includes the enterprise network path, Direct Connect routing and return paths, DNS resolution, and access to Systems Manager through AWS PrivateLink interface VPC endpoints. The `ssm` and `ssmmessages` services are central to the management and session connectivity under examination. Endpoint security groups and EC2 SSM Agent connectivity form additional boundaries; network reachability alone does not establish authorization. [AWS Systems Manager endpoint documentation](https://docs.aws.amazon.com/systems-manager/latest/userguide/setup-create-vpc.html)

Administrator-to-service connectivity and agent-to-service connectivity require separate validation. This page establishes the problem and acceptance criteria; it does not yet document a deployed configuration or validation results.

## Validation objective

A successful session is only one part of the evidence. Acceptance requires confirming DNS answers, forward and return routing, endpoint access controls, and observed traffic paths for both administrator and agent connections. The evidence must demonstrate that management traffic uses the intended private path without public Internet fallback.

See [Cloud Architecture](../../cloud/index.md) for the broader connectivity and isolation context.
