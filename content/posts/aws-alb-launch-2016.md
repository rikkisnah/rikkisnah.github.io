---
title: "Application Load Balancer: The Layer 7 Revolution"
date: 2016-08-11T09:00:00-07:00
draft: false
---

![Setting up an Application Load Balancer with AWS EC2](/aws_alb.png)

Classic Load Balancer shipped in 2009 and became a tech debt monster by 2016: 3 microservices = 3 load balancers = $150/month just for routing.

ALB fixed this with Layer 7 intelligence: one load balancer could route traffic based on paths, hostnames, and HTTP headers.

## The Problem

CLB worked fine for one big app per load balancer. But by 2016, everything was microservices:

```
GET /api/users     → User Service (port 3000)
GET /api/products  → Product Service (port 3001)
GET /images/*      → Image Cache (port 8080)
GET /*             → Web Frontend (port 3000)
```

With CLB, you needed 4 separate load balancers (one per service). 4 × $30/month = $120/month, plus management overhead.

## What ALB Did

**Path-based routing** meant one load balancer could intelligently distribute traffic:

```
ALB listens on :80/:443
  ├─ /api/* → route to API target group
  ├─ /images/* → route to Image target group
  └─ /* → route to Web target group
```

Same for host-based:
```
api.myapp.com     → API target group
images.myapp.com  → CDN origin
www.myapp.com     → Web target group
```

And dynamic port mapping (critical for ECS):
```
EC2 instance 1 runs:
  - Microservice A on port 3000
  - Microservice B on port 3001
  - Microservice C on port 3002

ALB automatically discovers + routes to all 3
```

## Why It Mattered

ALB was perfect for containerized workloads. When you run 5 containers on the same EC2 instance, each on different ports, you need intelligent routing. ALB was *designed* for this.

Performance:
- **Latency**: ~5ms (vs. CLB's ~8ms, not huge)
- **Throughput**: 1–3M RPS per load balancer
- **Features**: WebSockets, HTTP/2, Gzip compression

Market impact:
- By late 2016: ALB became the default for new deployments
- By 2017: ALB shipped more units than CLB
- By 2020: CLB was legacy; ALB was standard

## The Missed Insight (Almost)

Early ALB design proposed "just make it faster than CLB." But the winning feature wasn't speed—it was *architectural simplicity.*

One load balancer instead of three meant:
- 75% lower operational overhead
- Fewer DNS entries to manage
- Simpler monitoring and alerting
- Fewer things to break

This taught me: **in infrastructure, simplicity beats performance.** A 10% faster system that requires 3x the management loses to a simpler system every time.

ALB proved that constraint: better operational model > better specs.

