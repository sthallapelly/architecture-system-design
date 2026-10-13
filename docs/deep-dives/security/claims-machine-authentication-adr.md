# ADR-003: Machine-to-Machine Client Authentication

**Status:** Proposed — provider support, implementation, and validation pending.

**Scope:** partner and workload token acquisition in the claims platform. This decision does not replace the existing employee-access ADRs or settle BFF client authentication.

## Context

Settlement and partner integrations need distinct client identities with limited scopes and resource authority. Their token-acquisition credentials must be protected and rotated without giving every integration the same access.

Client Credentials is the selected grant for independently authorized machine access. This record selects the method used to authenticate those clients to the authorization server.

## Proposed decision

**Prefer `private_key_jwt` for controlled claims workloads**, subject to provider support and a reliable private-key/signing lifecycle. Register public verification keys with the issuer and use short-lived, correctly targeted assertions with defined replay handling.

Use **mTLS** where certificate automation, the issuer-facing TLS path, or partner requirements favor it. Use **client secrets** as an explicitly scoped fallback when asymmetric integration is unavailable; require protected delivery, rotation, and access logging.

Keep identities separate by integration responsibility and environment. Replicas may share a logical client when they perform the same role under the same authority.

## Alternatives and consequences

| Option | Advantage | Cost / risk |
| --- | --- | --- |
| Shared secret | Broad compatibility and simple integration | Reusable credential distribution and rotation |
| Private key JWT | No shared secret presented; application-layer proof | Signer/key protection, clocks, replay policy and key registration |
| mTLS | Certificate-key proof at transport boundary | Certificate/trust lifecycle and TLS termination complexity |

Asymmetric authentication does not make an issued bearer token resistant to replay. Sender constraints remain a separate design decision. Authentication-credential retirement and access-token revocation also have different effects.

## Evidence required before acceptance

- Selected issuer supports the registered method and assertion audience/profile.
- Valid requests succeed; wrong key, expired/wrong-audience assertions and applicable replays fail.
- Private-key access is controlled; assertions and tokens are absent from logs.
- Rotation works across active deployments with a bounded overlap and rollback procedure.
- Signer or certificate failures prevent unsafe fallback; token-cache behavior matches API policy.
- Token-acquisition latency and burst behavior meet the workload's measured requirements.

An mTLS deployment additionally validates certificate identity matching and any trusted proxy certificate propagation. A secret-based deployment documents why it was chosen and demonstrates rotation.

## Revisit when

Provider capabilities, partner requirements, workload platform identity, or operational reliability changes. Capture actual validation evidence and any changed assumptions before marking this ADR Accepted.

## Supporting concept

[Client Secrets, Private Key JWT, and mTLS](../../security/client-authentication-methods.md)
'''
