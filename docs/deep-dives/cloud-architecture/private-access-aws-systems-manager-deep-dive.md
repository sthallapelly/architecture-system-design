# Private Access to AWS Systems Manager: Understanding the End-to-End Network Path

Creating Systems Manager VPC endpoints is often described as making Session Manager access "private." That statement is useful, but incomplete.

A Session Manager connection involves more than the managed EC2 instance. The administrator, DNS resolution, network routing, interface endpoints, security groups, IAM authorization, and the SSM Agent all participate in establishing the session.

The practical architecture question is:

> **Which parts of the Session Manager path are private, and how can we prove which path is actually being used?**

This deep dive focuses on that end-to-end path.

## Start with two independent connectivity paths

The most useful mental model is to separate the connection into two paths:

- **Path 1 — Administrator to AWS Systems Manager.** The administrator's client must reach the AWS APIs and Session Manager service used to establish the session.
- **Path 2 — Managed node to AWS Systems Manager.** SSM Agent initiates outbound communication from the managed node to Systems Manager.

These paths participate in the same session, but they do not have to use the same network path.

For example, an EC2 instance can communicate with Systems Manager through interface VPC endpoints while the administrator's laptop still reaches AWS service endpoints through the Internet.

That distinction matters when a requirement says that administrative access must remain on private enterprise and AWS networks.

![Independent private Systems Manager paths: the enterprise administrator connects through VPN or Direct Connect to interface VPC endpoints, while EC2 SSM Agent initiates outbound HTTPS on port 443 to those endpoints. Enterprise DNS forwards queries separately to a Route 53 Resolver inbound endpoint.](../../assets/diagrams/ssm/ssm-end-to-end-private-access.svg)

## What "private SSM access" can mean

Before designing the network, define the requirement precisely.

There are at least three useful levels:

- **No inbound administrative ports on the workload.** Session Manager replaces direct inbound SSH or RDP access, but service communication may still use public AWS endpoints.
- **Private managed-node connectivity.** The managed node reaches Systems Manager through interface VPC endpoints instead of relying on NAT or Internet connectivity.
- **Private end-to-end administrative connectivity.** Both the managed-node side and the administrator-side service path use private enterprise/AWS connectivity.

These are progressively different requirements. Achieving the first does not automatically achieve the second or third.

## Path 2: managed node to Systems Manager

This is usually the simpler side of the design.

SSM Agent initiates the connections required to communicate with Systems Manager. For Session Manager, the `ssmmessages` endpoint is particularly important because it carries the control and data-channel communication used by the agent.

With public service endpoints, a private EC2 instance can reach Systems Manager through an outbound Internet-capable path such as a NAT gateway.

With AWS PrivateLink, the VPC instead contains interface endpoints with private IP addresses.

When private DNS is enabled for an interface endpoint, applications can continue using the normal regional AWS service hostname while DNS inside the VPC resolves that hostname to the private IP addresses of the endpoint ENIs.

This is an important property of the design: the application or agent normally does not need to be configured with a special `vpce-...` hostname simply because PrivateLink is being used.

### Endpoint requirements are capability-dependent

Do not treat a fixed list of VPC endpoints as timeless architecture.

For current Session Manager implementations, `ssm` and `ssmmessages` are central. `ec2messages` is a legacy consideration whose applicability depends on Region and SSM Agent behavior. Other Systems Manager capabilities can require access to additional AWS services such as Amazon S3, AWS KMS, CloudWatch Logs, or Amazon EC2.

The architectural rule is more durable:

> Identify every AWS service dependency required by the capabilities you enable, then provide either an approved public-service path or the appropriate private endpoint path for each dependency.

This prevents a common failure mode where the interactive session works but logging, encryption, agent updates, or another Systems Manager feature does not.

## Interface endpoint security groups

An interface endpoint creates elastic network interfaces in the selected subnets. Those ENIs have private IP addresses and security groups.

For an EC2 managed node to use the endpoint, the endpoint security group must allow the required HTTPS traffic from the appropriate source.

This is different from opening an inbound management port on the EC2 instance.

For a normal Session Manager connection, SSM Agent initiates the service connection. The EC2 security group therefore does not require inbound TCP 22 simply to support Session Manager.

## Path 1: administrator to Systems Manager

This side is where enterprise private-access designs become more interesting.

Consider an administrator running `aws ssm start-session`. The command uses AWS service endpoints. If the administrator's DNS resolves those service names to public AWS endpoint addresses and the enterprise network routes that traffic through an Internet egress path, then the client side of the session is still using that path.

This remains true even when the managed EC2 instance uses PrivateLink.

![Side-by-side administrator paths: public DNS answers lead through enterprise Internet egress to public Systems Manager endpoints; private endpoint answers lead through VPN or Direct Connect to interface VPC endpoints. The managed node’s endpoint choice does not determine the administrator’s path.](../../assets/diagrams/ssm/ssm-public-vs-private-path.svg)

To make the administrator-side path private, several independent pieces must align:

- **Private network reachability** must exist between the administrator's network and the VPC containing the relevant interface endpoints.
- **DNS** must resolve the required AWS service hostname to the intended private endpoint addresses.
- **Routing** must carry traffic to those private addresses over the intended VPN or Direct Connect path.
- **Endpoint security groups** must permit the client-side traffic where that access pattern requires it.
- **IAM authorization** must allow the administrator to perform the required Systems Manager and Session Manager operations.

A failure in any one of these areas can break the design.

## VPN and Direct Connect solve reachability, not the whole problem

A Site-to-Site VPN or Direct Connect connection can provide private IP connectivity between an enterprise network and AWS.

That does not, by itself, cause an AWS service hostname to resolve to a VPC endpoint.

Similarly, creating a VPC endpoint does not automatically cause an enterprise DNS resolver to return that endpoint's private addresses.

Think of the responsibilities separately:

- **VPN / Direct Connect** — provides private network reachability.
- **PrivateLink interface endpoint** — provides private IP addresses for a supported AWS service.
- **DNS** — determines which addresses the service hostname resolves to.
- **Routing** — determines how packets reach those addresses.
- **Security groups** — control permitted network flows to endpoint ENIs and workloads.
- **IAM** — controls whether the authenticated principal can perform the operation.

Private connectivity works only when these layers agree.

## Hybrid DNS is often the missing piece

Inside a VPC, Amazon-provided DNS can resolve private DNS names associated with interface endpoints.

An administrator on an enterprise network normally uses enterprise DNS instead.

That creates a question:

> How does an enterprise client learn the private address associated with an AWS service endpoint?

One common architecture uses a Route 53 Resolver inbound endpoint. The enterprise DNS infrastructure forwards the relevant queries to the Resolver inbound endpoint, and those DNS queries travel across private connectivity such as Site-to-Site VPN or Direct Connect.

![Enterprise DNS conditionally forwards service-name queries over private connectivity to Route 53 Resolver. VPC private DNS returns interface endpoint private IP addresses through the resolver chain; the client then uses those addresses for HTTPS connectivity.](../../assets/diagrams/ssm/ssm-hybrid-dns.svg)

The exact forwarding strategy depends on the organization's DNS architecture. The important point is that **network connectivity and name resolution must be designed together**.

A perfectly routed Direct Connect connection does not help if the client still resolves the service name to an unintended endpoint.

## Private DNS and endpoint placement

Private DNS simplifies application behavior, but it also introduces architecture decisions.

An organization must decide:

- which VPC owns the interface endpoints,
- which networks can route to the endpoint ENIs,
- which DNS resolvers can resolve the private service names,
- which security groups are allowed to connect,
- and whether endpoints are distributed per VPC or centralized.

In a small environment, endpoints in the workload VPC may be straightforward.

In a larger multi-account environment, organizations may centralize selected interface endpoints in a shared-services or networking VPC. That can reduce duplicated endpoints and centralize controls, but it increases dependency on shared routing, DNS, and network infrastructure.

The right choice depends on isolation requirements, failure domains, operating model, traffic patterns, and cost.

## Do not confuse network access with IAM authorization

A successful TCP connection to a Systems Manager endpoint proves only that network connectivity exists. It does not mean the administrator can start a session.

Likewise, an IAM policy granting `ssm:StartSession` cannot overcome a DNS or routing failure.

Troubleshooting is easier when the layers are tested independently:

1. Can the hostname be resolved?
2. Does it resolve to the expected address?
3. Is there a route to that address?
4. Do network controls allow TCP 443?
5. Can the AWS API be reached?
6. Is the identity authenticated?
7. Is the operation authorized?
8. Is the target registered and online in Systems Manager?
9. Can SSM Agent establish the required channels?

This sequence prevents IAM changes from being used to troubleshoot network problems—or network changes from being used to troubleshoot authorization failures.

## How to verify whether the path is private

Do not rely only on the fact that a VPC endpoint exists.

Verification should gather evidence from several layers.

![Nine verification stages: DNS resolution, expected endpoint address, route, firewall and security group, endpoint connectivity, AWS authentication, IAM authorization, managed-node and agent state, and successful session. Each stage has supporting evidence; no single check proves private access.](../../assets/diagrams/ssm/ssm-private-access-verification.svg)

### 1. Verify DNS resolution

From the environment being tested, resolve the relevant regional service hostname.

The important question is not merely whether DNS succeeds. Check **which addresses are returned**.

For an enterprise client intended to use a VPC interface endpoint, the result should align with the endpoint's private addresses and the organization's DNS design.

Testing DNS from an EC2 instance inside the VPC proves the EC2 DNS path. It does not prove that an administrator's laptop on the enterprise network receives the same answer.

### 2. Verify the network route

Confirm that the resolved private address is reachable through the intended private path.

For an enterprise design, inspect the relevant enterprise routes and AWS routes associated with the VPN, Direct Connect, Transit Gateway, virtual private gateway, or other routing components in the architecture.

Do not infer routing from DNS alone.

### 3. Verify endpoint security

Check the security group associated with the interface endpoint.

It must allow HTTPS traffic from the intended source according to the design.

Also verify network ACLs or enterprise firewalls when they participate in the path.

### 4. Verify the managed-node path separately

Confirm that the managed node resolves and reaches the required Systems Manager endpoints through the intended path.

This test is independent of the administrator-side test.

A successful Session Manager connection alone does not explain which network path each side used.

### 5. Use network evidence

Where available, VPC Flow Logs can help confirm traffic involving endpoint ENIs and private addresses.

Enterprise firewall, VPN, Direct Connect, or network telemetry can provide additional evidence for the client-side path.

The goal is to build a chain of evidence:

**Expected DNS answer + expected route + allowed network flow + observed endpoint traffic + successful authenticated operation**

No single check proves the entire architecture.

## Common failure patterns

### Session Manager works, but traffic is not fully private

The managed node uses interface endpoints, but the administrator still resolves and reaches AWS public service endpoints through enterprise Internet egress.

**Lesson:** validate Path 1 and Path 2 independently.

### EC2 cannot register or appears offline

Possible causes include missing endpoint connectivity, endpoint security-group rules, DNS configuration, SSM Agent state, or instance-profile permissions.

**Lesson:** separate agent connectivity, network reachability, and IAM permissions during troubleshooting.

### Private DNS works inside the VPC but not on-premises

The VPC resolver can resolve the private service name, but enterprise DNS is not forwarding the relevant queries through a Route 53 Resolver inbound endpoint or equivalent DNS design.

**Lesson:** VPC DNS behavior does not automatically extend to enterprise clients.

### DNS returns private addresses, but the session still fails

Name resolution is correct, but routing, endpoint security groups, enterprise firewalls, IAM authorization, or agent state may still be wrong.

**Lesson:** DNS success proves name resolution, not end-to-end connectivity.

### Core sessions work but an optional capability fails

The SSM endpoints are reachable, but a feature also depends on another service such as Amazon S3, AWS KMS, or CloudWatch Logs.

**Lesson:** model service dependencies by capability rather than assuming that "SSM connectivity" is one endpoint.

## Port forwarding adds another network segment

Remote-host port forwarding introduces one more path that must be evaluated:

**Administrator → Session Manager → Managed EC2 → Remote host**

For an RDS example, the Session Manager path can be healthy while the final EC2-to-RDS connection fails because of database DNS, routing, RDS security groups, or the database listener.

This is why port forwarding should be troubleshot as two separate problems:

- Can the Session Manager tunnel be established?
- Can the managed node reach the remote host and port?

The lab for this architecture will use this distinction deliberately.

## What changes for SSH over Session Manager

Session Manager can also act as the transport for SSH.

The important architectural difference is that the SSH connection is carried through the Session Manager tunnel rather than requiring the EC2 instance to expose SSH directly to the administrator's network.

However, SSH still has its own host-level authentication and configuration requirements.

There is also an operational limitation worth understanding: Session Manager does not provide session-content logging for SSH and port-forwarding sessions because it is acting as a tunnel for encrypted traffic.

That distinction matters when evaluating the design against audit requirements.

## Architecture decision framework

When designing private administrative access through Systems Manager, answer these questions explicitly:

- Do we only need to eliminate inbound SSH/RDP, or must the complete path avoid Internet connectivity?
- Which Systems Manager capabilities are required?
- Which AWS service dependencies do those capabilities introduce?
- Where will the required interface endpoints live?
- How will workloads resolve those endpoints?
- How will enterprise administrators resolve them?
- What private network path connects enterprise clients to the endpoint VPC?
- Which security groups and firewalls control the path?
- Which IAM identities can start which session types against which targets?
- What evidence will prove that the intended private path is being used?
- What audit requirements apply, especially for SSH and port-forwarding sessions?
- What happens if centralized DNS, endpoints, or network connectivity fails?

Answering those questions produces an architecture that can be explained, tested, and operated—not merely a collection of VPC endpoints.

## From design to implementation

The next step is to prove the pattern in a controlled environment.

The accompanying lab uses a practical scenario:

**Administrator → private Session Manager path → SSM-managed EC2 → private RDS**

The lab focuses on building the required controls, establishing remote-host port forwarding, deliberately breaking selected dependencies, and verifying which component is responsible for each failure.

Direct Connect does not need to be reproduced in the lab. The same architectural responsibilities—private reachability, DNS, routing, endpoint access, IAM, and managed-node connectivity—can be demonstrated using a practical VPN-based environment while the enterprise Direct Connect variation remains an architecture concern.

## AWS references

- AWS Systems Manager — VPC endpoints and AWS PrivateLink
- AWS Systems Manager — Session Manager
- AWS Systems Manager — `ssmmessages` and `ec2messages` API behavior
- Amazon Route 53 — VPC Resolver and hybrid DNS
- AWS Systems Manager — Starting Session Manager sessions and remote-host port forwarding
