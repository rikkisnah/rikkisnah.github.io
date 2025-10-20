---
title: "The Great Load Balancer Migration: Managing Three Generations"
date: 2018-06-15T09:00:00-07:00
draft: false
---

![AWS ELB](/aws_elb.jpg)

By mid-2018, AWS had three load balancers: CLB (2009), ALB (2016), NLB (2017). Millions of customers ran each type in production. The question: how do you migrate without breaking live applications?

## The Problem

- **CLB users**: "ALB looks nice but our app works fine."
- **ALB users**: "NLB's latency is seductive but we don't need it."
- **Enterprise IT**: "Three load balancers? Pick one."

Migrations were hard because each load balancer had different routing semantics:

| Feature | CLB | ALB | NLB |
|---------|-----|-----|-----|
| **Routing** | Fixed backend pool | Path/host-based | Layer 4 only |
| **Headers** | None | Adds X-Amzn-Trace-Id | Transparent |
| **Protocols** | TCP/HTTP/HTTPS | HTTP/HTTPS/gRPC | TCP/UDP |
| **Latency** | ~8ms | ~5ms | ~50µs |

Moving from CLB to ALB meant:
- Different routing logic (could send requests to different instances)
- New headers (some legacy apps crashed on unknown headers)
- Behavior changes (connection draining, timeout semantics)

## The Migration Playbook

I spent 2018 building a repeatable migration strategy for customers:

**Phase 1: Assessment (1 week)**
- Inventory all load balancers
- Categorize by type: stable, performance-constrained, growth-constrained
- Benchmark current performance (latency, error rates, throughput)

**Phase 2: Decision Matrix (2 weeks)**

For each load balancer, evaluate:
- Is it a bottleneck? → Migrate to ALB or NLB
- Is it containerized? → Migrate to ALB
- Latency-critical? → Evaluate NLB
- Stable + working? → Keep CLB for now

**Phase 3: Pilot (1 month)**

1. Deploy new load balancer (ALB or NLB) alongside existing one
2. Route 1% of production traffic to new load balancer
3. Monitor for 24 hours: latency, errors, connection behavior
4. Fix issues before scaling

**Phase 4: Gradual Shift (2-4 weeks)**

```
Hour 0-24:     1% traffic to new LB
Hour 25-48:    5% traffic
Hour 49-96:   10% traffic
Hour 97-168:  25% traffic
Day 8-14:     50% traffic
Day 15-21:    75% traffic
Day 22-28:    95% traffic (old LB as standby)
Day 29+:      100% traffic (old LB decommissioned)
```

**Phase 5: Cleanup (1 week)**

- Delete old load balancer
- Update DNS (if needed)
- Document new architecture

## The Hard Parts

**Issue 1: Applications depending on CLB headers**
- Some legacy apps looked for specific CLB behavior
- Solution: ALB can be configured to add X-Forwarded-* headers; test this in pilot

**Issue 2: DNS caching**
- Clients cache DNS results; old LB IP still resolves
- Solution: Reduce TTL 24hrs before migration, increase after

**Issue 3: Connection draining semantics differ**
- CLB drains connections differently than ALB
- Solution: Test deployment procedures before production migration

**Issue 4: Some apps just break**
- Rare, but legacy Windows apps sometimes can't handle ALB's headers
- Solution: Keep CLB as permanent fallback for 2-3 weeks; disable only when fully confident

## Real Migration Example

**Company: $500M SaaS startup**
- 50 CLB instances = $1,500/month
- Migrated to 5 ALB instances = $150/month
- Savings: $1,350/month ($16K/year)
- Time: 8 weeks from assessment to decommissioning CLB

Beyond cost, the wins:
- **Operational simplicity**: 50 → 5 load balancers
- **Cleaner routing**: microservices on same instance no longer conflicted
- **Better monitoring**: path-based metrics gave visibility into service health

## The Insight

By 2018, load balancers had become a *commodity.* The decision wasn't "best technology"—it was "best fit for your workload."

This thinking shaped my product philosophy:
- Multiple options, each optimized for constraints
- Clear migration paths between generations
- Operational simplicity > raw performance (usually)

AWS's playbook shifted from "one product to rule them all" to "portfolio of focused products." This worked because the company built *bridges* between products (clear upgrade paths, migration tools, transparent trade-offs).

Businesses win when infrastructure evolves with their applications. Load balancer migrations proved AWS could do that at scale.

