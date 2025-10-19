---
title: "The Great Load Balancer Migration: Managing Three Generations (2018)"
date: 2018-06-15T09:00:00-07:00
draft: false
---

![AWS ELB](/aws_elb.jpg)

## The Challenge: Three Generations of Load Balancers

By mid-2018, AWS had created an impressive portfolio of load balancing solutions. But this abundance of choice created a new problem: how do you manage migrations across three fundamentally different load balancing architectures?

By 2018, AWS had:
- **Classic Load Balancer (CLB)**: Launched 2009, mature but aging
- **Application Load Balancer (ALB)**: Launched 2016, perfect for modern apps
- **Network Load Balancer (NLB)**: Launched 2017, for extreme performance

Millions of customers were running production workloads on each type. The question became: how do you help them migrate without breaking live applications?

## The Migration Challenge

Moving from one load balancer type to another isn't simply a configuration change—it can fundamentally impact application behavior:

### CLB → ALB Migration Challenges:

**1. Routing Behavior Changes**
```
CLB: Fixed backend pool (same instances for all traffic)
ALB: Can route based on path/host/header
Result: Different instances may receive same request type
```

**2. New Headers in Requests**
```
ALB adds: X-Amzn-Trace-Id, X-Amzn-Trace-Root
Some legacy apps crash on unknown headers
```

**3. Health Check Changes**
```
CLB: Simple TCP/HTTP checks
ALB: Path-based health checks, gRPC support
Result: Different health check semantics
```

**4. Connection Behavior**
```
CLB: Long-lived connections
ALB: May close connections more aggressively
Result: Timeout issues in latency-sensitive apps
```

### ALB → NLB Migration Challenges:

**1. Protocol Support**
```
ALB: HTTP/HTTPS only
NLB: TCP/UDP at Layer 4
Result: Application-level headers no longer visible
```

**2. Latency Sensitivity**
```
ALB: 5-10ms typical latency acceptable
NLB: 10-100 microsecond latency expected
Result: Extremely tight SLA requirements
```

**3. Source IP Preservation**
```
ALB: X-Forwarded-For header for client IP
NLB: Actual client IP preserved
Result: Application filtering logic may need changes
```

## The Migration Roadmap

I worked with AWS to develop a comprehensive migration strategy:

### Phase 1: Assessment (Weeks 1-4)
- Inventory all running load balancers
- Categorize by application type and requirements
- Identify CLB instances that could be improved
- Assess performance baselines

### Phase 2: Prioritization (Week 5)
- **Tier 1**: Applications already experiencing performance issues → migrate to ALB or NLB
- **Tier 2**: Containerized/microservices apps → strong candidates for ALB
- **Tier 3**: Latency-critical apps → candidates for NLB
- **Tier 4**: Legacy, stable applications → can remain on CLB for now

### Phase 3: Pilot Deployments (Weeks 6-12)
- Create test environment with new load balancer
- Run production traffic through new load balancer (shadow traffic)
- Monitor for differences in behavior
- Collect performance baselines

### Phase 4: Gradual Traffic Shift (Weeks 13-24)
- Route small percentage (1-5%) of traffic to new load balancer
- Monitor metrics: latency, error rates, connection counts
- Gradually increase traffic percentage
- Maintain fallback to old load balancer

### Phase 5: Cutover (Week 25+)
- When traffic percentage reaches 100%, old load balancer becomes standby
- Monitor for 24 hours
- Decommission old load balancer
- Document lessons learned

## Real-World Migration Example: E-Commerce Application

To illustrate, let me walk through migrating a typical e-commerce application from CLB to ALB:

### Before: CLB Architecture
```
Internet
   |
   ↓
CLB (load all instances equally)
   |
   ├─→ EC2 Instance 1 (web server + API + images)
   ├─→ EC2 Instance 2 (web server + API + images)
   └─→ EC2 Instance 3 (web server + API + images)

Problem: Image serving (heavy CPU) impacts API response times
```

### After: ALB Architecture
```
Internet
   |
   ↓
ALB (intelligent routing)
   |
   ├─→ /api/* → API Server Pool (Instances 1-2)
   ├─→ /images/* → Image Server Pool (Instances 3-5)
   └─→ /* → Web Server Pool (Instances 6-8)

Benefit: Independent scaling, isolated failure domains
```

### Migration Steps:

**Step 1: Set up ALB alongside CLB**
- Create new ALB with same targets
- Configure routing rules
- Deploy with DNS pointing to CLB

**Step 2: Enable health checks on ALB**
- Configure path-based health checks
- Monitor ALB health status
- Verify all targets reporting healthy

**Step 3: Route shadow traffic to ALB**
- Add ALB endpoint to application
- Route 1% of production traffic through ALB
- Collect metrics for 24 hours
- Compare with CLB metrics

**Step 4: Gradual traffic increase**
```
Hour 1-24: 1% traffic to ALB
Hour 25-48: 5% traffic to ALB
Hour 49-72: 10% traffic to ALB
Hour 73-96: 25% traffic to ALB
Hour 97-120: 50% traffic to ALB
Hour 121-168: 100% traffic to ALB (CLB becomes standby)
```

**Step 5: Monitor and stabilize**
- Watch for any anomalies
- Verify application behavior identical
- Confirm performance improvements
- Test failback to CLB

**Step 6: Cleanup**
- After 2 weeks of successful operation, decommission CLB
- Update DNS records to remove CLB endpoint
- Document new architecture

## Key Metrics for Migration Success

To evaluate migration success, I tracked specific metrics:

### Performance Metrics:
- **Latency**: p50, p95, p99 latencies unchanged or improved
- **Throughput**: Requests per second throughput maintained
- **Connection Count**: Concurrent connections sustained
- **Error Rate**: 4xx/5xx error rate unchanged or improved

### Operational Metrics:
- **Health Check Stability**: Targets remain healthy
- **Auto-scaling**: Scaling policies work as expected
- **Zero-downtime Deployments**: Deployment procedures unchanged
- **Failover Behavior**: Secondary availability zones respond correctly

### Financial Metrics:
- **Cost**: New load balancer cost compared to old
- **Efficiency**: Cost per request improved
- **Savings**: If consolidating multiple load balancers

## Common Pitfalls and How to Avoid Them

Through dozens of customer migrations, I identified common failure patterns:

### Pitfall 1: Insufficient Testing
- **Problem**: Migrating without shadow traffic analysis
- **Solution**: Always run shadow traffic for 24-48 hours before cutover

### Pitfall 2: Underestimating Connection Behavior Changes
- **Problem**: ALB may close idle connections differently
- **Solution**: Test with realistic traffic patterns, including spiky workloads

### Pitfall 3: Forgetting About DNS Caching
- **Problem**: Old DNS records remain cached, causing confusion
- **Solution**: Reduce TTL 24 hours before migration, increase after cutover

### Pitfall 4: Not Planning for Rollback
- **Problem**: Can't quickly revert if new load balancer has issues
- **Solution**: Keep old load balancer live as standby for 2+ weeks

### Pitfall 5: Ignoring Application Dependencies
- **Problem**: Applications depending on specific load balancer behavior fail
- **Solution**: Audit all applications for hard dependencies before migrating

## The Broader Vision: Load Balancer as Commodity

By 2018, load balancing was becoming a solved problem. AWS had created a portfolio where:

- **Every application type** had an optimal load balancer
- **Migration paths** between generations were clear and documented
- **Automated tools** could help with assessment and migration
- **Best practices** were well-understood

This represented a maturation of AWS infrastructure. Early AWS days (2006-2010) felt cutting-edge but required deep operational expertise. By 2018, infrastructure patterns were becoming standardized, repeatable, and increasingly automated.

## Tools and Resources

To support migrations, AWS created:

1. **AWS Migration Evaluator**: Assessment tool for identifying optimization opportunities
2. **Migration Playbooks**: Step-by-step guides for specific application patterns
3. **Performance Benchmarking**: Tools to compare load balancer performance
4. **Migration Partners**: AWS Certified Partners specializing in infrastructure migrations
5. **Professional Services**: AWS teams available to lead complex migrations

## Looking Back

The Great Load Balancer Migration (2018) represents a watershed moment in AWS history. By 2009-2012, AWS was about innovation and new capabilities. By 2018, AWS was increasingly about *choice*, *specialization*, and *pragmatism*.

Instead of one load balancer trying to be everything, AWS built three specialized products. This required managing complexity—both technical and organizational. Customers had to make informed choices about which load balancer to use.

But this specialization led to better outcomes:
- Applications got infrastructure optimized for their specific needs
- Performance improved across the board
- Costs decreased through better resource utilization
- Operational burden decreased as each load balancer was focused and purposeful

The 2018 migration guidance showed AWS's maturity: not just launching new services, but helping customers evolve their infrastructure as architecture and requirements changed.

By 2018, AWS had built not just infrastructure—it had built an ecosystem of increasingly specialized, interconnected services that together addressed every possible application architecture and requirement.

The load balancer evolution was complete. The next evolution would come with containerization, serverless computing, and edge services. But the fundamental principle remained: different applications have different needs, and infrastructure should be specialized accordingly.

