---
title: "Network Load Balancer: Extreme Performance for the Cloud"
date: 2017-09-21T09:00:00-07:00
draft: false
---

![AWS ELB](/aws_elb.jpg)

## The Performance Frontier

By 2017, AWS had successfully addressed the needs of modern, containerized, microservices-based applications with the Application Load Balancer. But there was an entirely different class of workloads that neither CLB nor ALB could adequately serve:

- **Real-time Financial Trading**: Sub-millisecond latency requirements
- **Internet of Things (IoT)**: Millions of concurrent connections
- **Video Streaming**: UDP protocol support and extreme throughput
- **Gaming**: Ultra-low latency, millions of concurrent connections
- **DNS/DNSSEC**: Need for Layer 4 performance without Layer 7 overhead

These workloads didn't need intelligent application routing—they needed *raw performance*. In September 2017, AWS launched the **Network Load Balancer (NLB)**—a revolutionary load balancing architecture designed for extreme performance, scalability, and ultra-low latency.

## The Performance Challenge

To understand NLB's significance, consider the performance requirements of modern ultra-scale applications:

### Scale at the Edge:
- **Millions of Requests Per Second**: Handling 20+ million RPS
- **Ultra-Low Latency**: Single-digit microsecond latencies
- **Extreme Concurrency**: Hundreds of millions of concurrent connections
- **Consistency**: Latency distribution matters more than peak throughput

Traditional load balancers were architected for throughput and availability. NLB was architected for *consistency* and *performance*.

## NLB Architecture: Layer 4 on Steroids

NLB returned to Layer 4 (TCP/UDP) but with a completely rethought architecture:

### Key Design Decisions:

**1. Connectionless Packet Processing**
- Rather than maintaining connection state in the load balancer, NLB uses flow hashing
- Each packet in a flow gets hashed to the same target
- Eliminates connection state bottleneck
- Enables true horizontal scaling

**2. Static IP Addresses**
```
NLB automatically assigns static/Elastic IP addresses per Availability Zone
- Clients can configure firewall rules for known IPs
- Critical for on-premises integration
- Enables DNS caching and edge routing
```

This was a huge differentiator. For the first time, clients connecting to AWS load balancers could get static, known IP addresses.

**3. UDP Protocol Support**
- Full UDP support with same performance characteristics as TCP
- Critical for gaming, video, DNS, IoT
- Bidirectional communication support
- Connectionless flow tracking

**4. Ultra-Low Latency Architecture**
- Kernel-space packet processing
- Minimal context switching
- Optimized memory access patterns
- Hardware-accelerated packet processing where available

## NLB vs. ALB: The Trade-off Matrix

Each load balancer was optimized for different requirements:

### ALB (Application Load Balancer):
- **Layer 7**: Application-aware routing
- **Typical Latency**: 5-10 milliseconds
- **Throughput**: 1-3 million RPS
- **Ideal For**: Web applications, APIs, microservices
- **Routing Complexity**: High (path, host, header-based)

### NLB (Network Load Balancer):
- **Layer 4**: Network-level performance
- **Typical Latency**: 10-100 microseconds (100x faster!)
- **Throughput**: 20+ million RPS
- **Ideal For**: Real-time, extreme scale, ultra-low latency
- **Routing Complexity**: Low (connection-based)

### When to Use NLB:
1. **Extreme Performance Required**: Sub-millisecond latency critical
2. **Massive Scale**: Hundreds of millions of connections
3. **Non-HTTP Protocols**: DNS, gaming, IoT with UDP/TCP
4. **Static IPs Required**: For firewall allowlisting
5. **Extreme Throughput**: Needing 20M+ RPS

## Technical Deep Dive: NLB Performance

NLB achieved performance targets through fundamental architectural choices:

### Flow Hashing:
```
For each packet:
1. Extract source/dest IP, source/dest port, protocol
2. Calculate hash of 5-tuple
3. Route to same target based on hash
4. No connection state needed in load balancer
```

This approach meant:
- Stateless load balancing (scales infinitely)
- Consistent targeting (same connection always routes to same target)
- Minimal CPU overhead (just hashing)

### Preserve Source IP:
- Target servers see actual client IP, not load balancer IP
- Critical for IP-based filtering and logging
- No need for X-Forwarded-For header manipulation
- Direct client-target communication possible (no proxying overhead)

### Connection Draining & Health Checks:
- Graceful deregistration of unhealthy targets
- Health check intervals configurable
- Cross-zone load balancing available
- Targets in failed AZs automatically removed

## Real-World Use Cases

### Use Case 1: Extreme Scale Gaming
```
- 50 million concurrent gaming sessions
- Requires microsecond latency (impact on player experience)
- UDP-based game protocol
- Standard ALB would create latency bottleneck
- NLB enables sub-millisecond player-to-server latency
```

### Use Case 2: DNS Resolution
```
- DNS providers need to handle billions of queries daily
- Each query must be answered in <100ms globally
- UDP protocol for query/response
- Millions of concurrent queries to same NLB
- NLB's static IPs enable reliable DNS caching by ISPs
```

### Use Case 3: Cryptocurrency Exchange
```
- Financial trading at extreme scale
- Microsecond latencies critical for trade execution
- Millions of concurrent trader connections
- Ultra-low latency affects profitability directly
- NLB ensures consistent sub-millisecond latencies
```

## The Static IP Advantage

One of NLB's most important features—but easily overlooked—was the provision of static/Elastic IP addresses per Availability Zone:

### Why This Matters:
1. **Firewall Rules**: On-premises firewalls can allowlist known IPs
2. **BGP/DNS**: Third-party CDNs and DNS providers can reliably route to known IPs
3. **Legacy Integration**: Systems expecting fixed IPs can integrate with cloud
4. **Compliance**: Some compliance regimes require known, fixed IPs
5. **Cost Predictability**: Bandwidth pricing could be calculated from known IPs

This seemingly simple feature opened up entire new categories of use cases for AWS infrastructure.

## Pricing Model

NLB introduced a different pricing model than ALB:

### NLB Pricing:
- Hourly load balancer charge (slightly higher than ALB)
- Per-flow charge based on new connections
- Data processing charges based on GB processed

This meant:
- Short-lived connections (web requests) might be more expensive on NLB
- Long-lived connections (persistent gaming/IoT) amortized better on NLB
- Choice between ALB (pay for throughput) and NLB (pay for flows)

## Market Impact and Adoption

NLB rapidly became the go-to load balancer for specific use cases:

### Early Adopters:
- **Gaming Companies**: Needed ultra-low latency for competitive games
- **Streaming Services**: Video platforms using UDP-based protocols
- **Financial Services**: Trading firms needing microsecond precision
- **IoT Platforms**: Services connecting millions of IoT devices
- **DNS Providers**: Services needing extreme query throughput

### Competitive Advantages:
- No competitor offered equivalent Layer 4 performance
- Static IPs differentiated from Google Cloud and Azure
- UDP support on-parity with on-premises infrastructure
- AWS infrastructure could finally handle extreme-scale workloads

## The Complete Load Balancing Portfolio

By late 2017, AWS offered three distinct load balancing solutions:

| Product | Layer | Ideal For | Latency | Throughput |
|---------|-------|-----------|---------|-----------|
| **Classic LB** | 4/7 | Legacy apps, backward compatibility | 5-10ms | 1M RPS |
| **ALB** | 7 | Web, APIs, microservices, ECS | 5-10ms | 3M RPS |
| **NLB** | 4 | Gaming, IoT, DNS, extreme scale | 10-100µs | 20M+ RPS |

This created an embarrassment of riches for customers—each product perfectly optimized for specific use cases.

## The Broader Vision

NLB represented AWS's commitment to being the infrastructure platform for *any* application architecture:

- Monolithic web application? Use ALB (or CLB for legacy)
- Containerized microservices? Use ALB with ECS dynamic discovery
- Real-time gaming platform? Use NLB for sub-millisecond latencies
- IoT platform? Use NLB for massive connection scale
- DNS provider? Use NLB with static IPs

By offering load balancing solutions optimized for different performance characteristics, AWS was saying: "Build whatever you want to build. We have infrastructure for it."

## Looking Back

The Network Load Balancer (2017) represented AWS's recognition that "one size fits all" doesn't apply to infrastructure. Different applications have fundamentally different requirements, and trying to serve all requirements with a single product creates compromises.

NLB proved that you could build infrastructure optimized specifically for performance and scale, without sacrificing reliability or operability. It also proved that static IP addresses—a feature from traditional infrastructure—could be valuable in cloud environments, especially for real-time, extreme-scale applications.

By 2018, NLB would be joined by additional features like PrivateLink and deeper integrations with emerging services. But the 2017 launch of NLB marked the moment when AWS created a complete, differentiated portfolio of load balancing solutions for every possible use case.

