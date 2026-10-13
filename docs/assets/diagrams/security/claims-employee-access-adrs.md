# Claims Platform: Security Architecture Decisions

These records apply the security concepts to the [claims employee-access deep dive](claims-employee-access.md) and its partner/workload extensions. **All records are Proposed; none has implementation evidence yet.** The original ADR-001 through ADR-006 numbering is preserved.

A documented pattern is an option. A proposed decision states how this platform intends to use it. Acceptance requires tested behavior, provider compatibility, and recorded limitations.

## Decision register

| ADR | Decision | Planned application |
| --- | --- | --- |
| 001 | BFF with Authorization Code + PKCE | Employee baseline |
| 002 | Operation scopes plus application-owned authority | Employee baseline; reuse for machine access |
| 003 | Prefer private key JWT for machine client authentication | Partner/workload extension |
| 004 | Application evaluator and authoritative entitlements | Baseline; external engine selection deferred |
| 005 | Gateway screening and independent service enforcement | Baseline |
| 006 | Fresh issuer-status check for sensitive approval | Baseline; introspection contract must be verified |
| 007 | Explicit downstream authority and targeted token exchange | Conditional Ledger extension |
| 008 | Sender constraints based on replay risk and supported key operations | Mechanism selection deferred |
| 009 | API-owned assurance/freshness requirements, BFF-coordinated step-up | Sensitive-operation extension |
| 010 | Event-fed restrictions with enforcement on affected request paths | Adoption deferred pending response target and provider support |
| 011 | Original JWT forwarding initially; Phantom Tokens as an optional variant | Baseline retained; transformation deferred |

## ADR-001: Frontend client authentication

**Proposed decision:** use BFF with Authorization Code + PKCE and confidential-client authentication. Keep usable OAuth tokens outside JavaScript and expose a protected browser session.

**Reason:** payment approval justifies reducing browser extraction of API credentials.

**Alternatives:** direct SPA + PKCE; token mediation; Token Handler/OAuth Proxy deployment with separate agent and proxy responsibilities.

**Consequences:** session storage, proxy capacity, CSRF controls, backend credentials, and coordinated refresh. XSS can still initiate actions through the session. BFF client-authentication configuration is a separate choice from ADR-003.

**Acceptance evidence:** no usable OAuth tokens exposed to JavaScript; callback, session rotation, CSRF, logout, concurrent refresh, and session-store failure behave correctly.

**Revisit:** direct API connectivity becomes essential or BFF operating cost no longer matches the required isolation.

Supporting concept: [Browser Token and Session Architecture](../../security/browser-session-architecture.md).

## ADR-002: API access-control model

**Proposed decision:** use operation scopes (`payment:read`, `payment:create`, `payment:approve`) and application-owned business permissions. Do not require custom group or approval-limit claims initially.

**Reason:** preserve client-grant restrictions without encoding changing resource rights into the scope catalog. Groups establish issuance eligibility; they do not replace the client grant.

**Alternatives:** broad API scope plus explicit client restrictions and role/permission claims; more granular scopes.

**Consequences:** the API distinguishes scope grants from current business authority. Read access is requested at login; additional workflow grants add authorization redirects and safe grant-state handling. Scope acquisition does not establish stronger authentication.

**Acceptance evidence:** wrong-scope requests fail; issuance eligibility holds; a reporting/read grant cannot approve; a denied workflow upgrade preserves safe session behavior.

**Revisit:** capability vocabulary or client-access requirements change materially.

Supporting concept: [Scopes, Groups, and API Access Decisions](../../security/scopes-and-api-access.md).

## ADR-003: Machine-to-Machine Client Authentication

**Proposed decision:** use Client Credentials for independently authorized partner/workload access. **Prefer `private_key_jwt`** for controlled workloads when the issuer and protected signing/rotation lifecycle support it.

Use **mTLS** where certificate automation, the issuer-facing TLS path, or partner requirements favor it. Use **client secrets** as an explicitly scoped fallback with protected delivery, rotation, and access logging.

**Reason:** separate integration identities and avoid routinely transmitting reusable shared secrets where asymmetric operations are reliable. Replicas may share one logical client only when their responsibility and authority are the same.

**Alternatives and consequences:**

| Method | Benefit | Operating responsibility |
| --- | --- | --- |
| Secret | Broad compatibility | Distribution, exposure control, coordinated rotation |
| Private key JWT | Short-lived signed client proof | Key/signing protection, clocks, assertion targeting and replay policy |
| mTLS | Certificate-key proof at transport boundary | Certificate identity, trust, renewal and TLS termination |

Client authentication does not make an issued bearer token replay-resistant. Credential retirement and access-token revocation have separate effects.

**Acceptance evidence:** actual provider profile supports the method; correct requests succeed; wrong-key, expired/wrong-audience assertions and applicable replays fail; rotation works across deployments with bounded overlap and rollback; signer/certificate failure causes no weaker fallback. Measure token acquisition under renewal bursts and exclude credentials from logs.

For mTLS, also validate certificate identity and protected proxy propagation. A secret deployment records why it was chosen and demonstrates rotation.

**Revisit:** provider support, partner requirements, platform identity, or operational reliability changes.

Supporting concepts: [Client Credentials](../../security/client-credentials-machine-identity.md) and [Client Authentication Methods](../../security/client-authentication-methods.md).

## ADR-004: Fine-grained authorization strategy

**Proposed decision:** use an application evaluator with authoritative database entitlements and persisted payment facts. External policy-engine selection remains deferred.

**Reason:** account rights and limits change independently of login; payment state is service-owned. Roles, attributes, and explicit account relationships can be represented without another policy service.

**Alternatives:** token claims, entitlement service, local/remote OPA, OpenFGA relationship evaluation.

**Consequences:** database availability, consistency, and concurrent changes are authorization concerns. Current lookup does not make check-and-commit atomic. Token claims and caches need an explicit stale-access bound.

**Acceptance evidence:** removed account access blocks approval; cross-unit access and self-approval fail; reads/search/export preserve visibility; concurrent entitlement/payment updates cannot commit stale authority unchecked.

**Revisit:** shared policy governance or relationship complexity justifies external evaluation. Compare actual decision and listing workloads before selecting OPA or OpenFGA.

Supporting concepts: [Runtime Authorization Models](../../security/runtime-authorization-models.md) and [Policy Architecture](../../security/policy-decision-enforcement.md).

## ADR-005: Gateway and service enforcement

**Proposed decision:** screen credentials and capabilities at the gateway; independently validate the accepted token and enforce business rules in Payment API. Initially forward the original Payment API JWT.

**Reason:** routing changes or approved alternate ingress must not eliminate payment enforcement.

**Alternatives:** protected gateway context; gateway-issued signed assertion; issuer-supported Phantom Token resolution under ADR-011.

**Consequences:** duplicated credential checks and consistent configuration. Approval rules have one owner in the service. Strip caller-supplied identity headers and control every admitted ingress path.

**Acceptance evidence:** forged headers have no authority; approved direct ingress retains checks; route/method aliases cannot expose unprotected operations; gateway/service audience rules agree.

**Revisit:** transformation or a new internal trust contract becomes necessary. Changing representation requires an explicit update to this forwarding contract.

Supporting concept: [Gateway and API Enforcement Boundaries](../../security/gateway-api-enforcement.md).

## ADR-006: Token activity for sensitive approval

**Proposed decision:** perform local JWT checks on all operations and uncached authenticated introspection for approval. No local-only fallback when required status is unavailable.

**Reason:** approval requires fresher issuer activity than signature/expiry checks provide.

**Alternatives:** local-only short-lived tokens; cached introspection; status checks on every request; event-fed restrictions.

**Consequences:** approval depends on issuer latency, limits, availability, and introspection credentials. The result is point-in-time, not atomic with later revocation, and does not replace current entitlements.

**Acceptance evidence:** the provider accepts the actual validation-client credentials; revoked tokens fail; timeouts prevent mutation; latency and load are measured. Record revocation propagation and in-flight limitations.

**Revisit:** measured constraints or access-removal requirements warrant another status strategy. A Phantom Token cache or event stream does not silently replace this approval requirement.

Supporting concept: [JWT Validation, Introspection, and Revocation](../../security/token-validation-revocation.md).

## ADR-007: Downstream authority and token exchange

**Proposed decision:** preserve user-dependent authority for Ledger account checks through a Ledger-targeted exchange where the provider supports the required semantics. Use independent workload authority for settlement. Relay only when Ledger is an intentional recipient.

**Reason:** a Payment API token or broad machine identity must not bypass the user's account restrictions.

**Consequences:** exchange adds issuer policy and availability dependencies. Audience/capability attenuation and subject/actor attribution require verification; RFC 8693 does not guarantee them automatically. No retry with a broader identity after denial.

**Acceptance evidence:** wrong audience/target fails; unauthorized accounts remain denied; subject and actor are represented as intended; cache partitioning prevents cross-user reuse; exchanged-token revocation behavior is documented.

**Revisit:** provider limitations or downstream authority requirements change.

Supporting concept: [Downstream Delegation and Token Exchange](../../security/downstream-delegation-token-exchange.md).

## ADR-008: Sender-constrained token adoption

**Proposed decision:** assess mTLS-bound tokens for controlled partner/workload paths and DPoP for supported application paths. **Defer mechanism selection** until issuer, client, gateway, API, and key operations are verified.

**Reason:** limit replay of a stolen token without its bound key.

**Consequences:** certificate/key lifecycle, proof validation, replay tracking, and proxy handling. Token plus usable key compromise remains a risk. Client authentication under ADR-003 is insufficient on its own.

**Acceptance evidence:** missing/wrong key, proof replay, and incorrect method/URI fail; renewal preserves binding; proxy evidence is trustworthy; failed proof checks cannot downgrade to bearer acceptance.

**Revisit:** replay risk, termination topology, or supported proof mechanisms change.

Supporting concept: [Sender-Constrained Tokens](../../security/sender-constrained-tokens.md).

## ADR-009: Authentication assurance and freshness

**Proposed decision:** Payment API owns sensitive-operation assurance/freshness requirements. The BFF handles a supported authentication challenge and reauthentication; the API verifies issuer-authenticated evidence before approval.

**Reason:** business permission and a newly issued token do not prove recent strong user authentication.

**Consequences:** an agreed `acr`/`auth_time` or introspection contract, enrolled authenticators, safe continuation state, and cancellation handling. The qualifying methods and freshness window remain policy choices to establish before implementation.

**Acceptance evidence:** an old authentication event fails despite token refresh; insufficient assurance challenges; account switching/cancellation cannot approve; resumed requests recheck entitlements and payment version; retries are bounded.

**Revisit:** operation risk, supported assurance profiles, or transaction-confirmation requirements change. Step-up is not transaction signing.

Supporting concept: [Step-Up Authentication](../../security/step-up-authentication.md).

## ADR-010: Continuous access and shared security signals

**Proposed decision:** where faster access restriction is required, use a dedicated event receiver to maintain trusted restrictions consumed by BFF and API enforcement. **Defer adoption** until an enforcement-time target, correlation contract, and provider capabilities are established.

**Reason:** later session/device/risk changes cannot be observed through local JWT validation alone.

**Consequences:** durable delivery, subject/session mapping, deduplication, regional propagation, and recovery. Delivery acknowledgement is not enforcement. Removing a BFF session does not automatically block its token elsewhere.

**Acceptance evidence:** affected old-token requests fail on relevant paths; duplicate/late events cannot restore restricted access; outage and replay/reconciliation behavior meet the freshness policy; measure end-to-end enforcement delay.

**Revisit:** issuer/event availability, risk requirements, or the status strategy in ADR-006 changes.

Supporting concept: [Continuous Access Evaluation and Shared Signals](../../security/continuous-access-evaluation.md).

## ADR-011: External and internal token representation

**Proposed decision:** retain original JWT forwarding for the initial employee baseline. Treat opaque external tokens with gateway-resolved internal JWTs as an optional Phantom Token variant.

**Reason:** the BFF already isolates usable tokens from JavaScript. Additional claim-exposure requirements, especially for partner clients, may justify resolution.

**Consequences:** issuer-specific resolution support, protected gateway credentials, cache bounds, and prevention of internal-JWT bypass. A signed introspection response is not automatically a forwardable access token. Resolution does not automatically change audience or lower authority.

**Acceptance evidence:** verify the internal access-token contract; reject bypasses; demonstrate cache expiry, revocation handling, and resolution outage. Preserve approval freshness under ADR-006 and any adopted sender binding.

**Revisit:** external claim exposure or provider/gateway capabilities warrant the extra dependency.

Supporting concept: [Phantom Token Architecture](../../security/phantom-token-architecture.md).

## Recording acceptance

For each accepted record, add the evidence reference, provider/version/configuration, observed behavior, date, and remaining limitations. Change the rationale and consequences if implementation changes the decision.

Keep one enterprise lab. Validate the employee baseline first, then partner/settlement authority, followed by selected supported extensions. Comparing OPA, OpenFGA, or other deployment options does not require implementing all of them.
