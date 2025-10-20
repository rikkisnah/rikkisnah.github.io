---
title: "Network Load Balancer: Extreme Performance for the Cloud"
date: 2017-09-21T09:00:00-07:00
draft: false
---

![Network Load Balancer: DNS routing with cross-zone load balancing](/aws_nlb.png)

ALB solved microservices routing. NLB solved an entirely different problem: what if you need 20M requests per second at 10 microseconds of latency?

Answer: don't use ALB. ALB's Layer 7 inspection has overhead. NLB dropped back to Layer 4 and optimized for raw speed.

## The Market Gap

By 2017, certain workloads were impossible on AWS:
- **High-frequency trading**: Microsecond latencies matter (literally worth $1M per millisecond)
- **Gaming**: 50M concurrent sessions, sub-100ms latency required
- **DNS**: Billions of queries/day, must be answered in <50ms
- **Video streaming**: Millions of concurrent UDP streams

These needed a load balancer that didn't inspect application data—just hashed flows and forwarded packets fast.

## What NLB Did

**Flow hashing instead of connection state:**
```
For each packet:
  1. Extract: source IP, dest IP, source port, dest port, protocol
  2. Hash the 5-tuple
  3. Always route packets from same flow to same target
  4. No connection state = scales infinitely horizontally
```

Result: **10–100 microsecond latency** (vs. ALB's 5ms). 100x faster.

**Static IP addresses per Availability Zone:**

For the first time, an AWS load balancer gave you known, static IP addresses. This mattered for:
- Firewall allowlisting (on-premises integration)
- BGP announcements (for CDN providers)
- DNS caching (ISPs cache based on IP)

**UDP support:**

ALB was HTTP/HTTPS only. NLB handled UDP, enabling:
- DNS queries
- Gaming protocols
- Video streaming protocols
- IoT sensor data

## Real Wins

- **Cryptocurrency exchange**: 500K traders sending orders per second. NLB's latency meant their orders hit the exchange microseconds faster than competitors. Worth millions in Q4.

- **Gaming company**: 50M concurrent players. NLB handled it at 1/10th the latency of ALB. Players noticed.

- **DNS provider**: Billions of queries/day. NLB's static IPs meant ISP caching worked. Their query response time improved 20%.

## The Trade-off

NLB didn't do path-based routing. You couldn't say "route /api to one service." It was pure Layer 4: TCP/UDP only.

For 90% of applications: wrong choice. You're paying for microsecond latency you don't need.

For 10% (real-time, extreme scale, non-HTTP): only choice.

## Market Adoption

- **Gaming**: NLB became standard
- **Financial services**: Default for trading systems
- **DNS/CDN**: Adopted rapidly
- **General web apps**: Still preferred ALB (simpler mental model)

By 2019, AWS had three load balancers, each optimized for different constraints:
- **Classic (CLB)**: Legacy, backward compatibility
- **Application (ALB)**: Microservices, HTTP-first, simplicity
- **Network (NLB)**: Extreme performance, non-HTTP, millions of RPS

This portfolio strategy—multiple products optimized for different trade-offs—became the AWS playbook everywhere.

