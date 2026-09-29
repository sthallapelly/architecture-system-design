# Labs

Hands-on implementations that validate selected architecture designs through deployment, testing, failure injection, and operational observation.

The detailed implementation artifacts live in their GitHub repositories so the labs remain reproducible without duplicating the same material across this site.

## AWS

### Private RDS Administrative Access with AWS Systems Manager {#private-rds-access-with-systems-manager}

Secure administrative access to a private Amazon RDS database through an AWS Systems Manager managed EC2 instance, without SSH, public IP addresses, or NAT dependency on the managed-node Systems Manager path.

The implementation uses Terraform and validates the architecture end to end, including Systems Manager remote-host port forwarding, PrivateLink DNS behavior, EC2-to-RDS connectivity, controlled failure experiments, and recovery.

**Technologies:** AWS Systems Manager · AWS PrivateLink · Amazon EC2 · Amazon RDS · Terraform

[View implementation and lab on GitHub](https://github.com/sthallapelly/private-rds-access-with-ssm)

**Related architecture:** [Secure Private Administrative Access on AWS](../cloud/secure-private-administrative-access-aws.md) · [Private Access to AWS Systems Manager — Deep Dive](../deep-dives/cloud-architecture/private-access-aws-systems-manager-deep-dive.md)
