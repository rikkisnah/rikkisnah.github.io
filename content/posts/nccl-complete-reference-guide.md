---
title: "The Complete NCCL Reference Guide: Commands, Errors, and Troubleshooting for OCI GPU Infrastructure"
date: 2025-11-15T00:00:00-07:00
draft: false
tags: ["NCCL", "GPU", "OCI", "HPC", "NVIDIA", "Infrastructure", "Troubleshooting", "Distributed Training", "InfiniBand", "GB200", "H100", "A100"]
categories: ["Technical Deep Dive", "Cloud Infrastructure"]
---

**Disclaimer:** This article reflects my personal research and analysis based on publicly available information and is not representative of my employer's official position.

![NCCL - NVIDIA Collective Communications Library](/posts/nccl-complete-reference-guide/nccl.jpg)

## Executive Summary

NCCL (NVIDIA Collective Communication Library) is the cornerstone of distributed GPU computing, enabling efficient communication between GPUs in multi-node clusters. This comprehensive guide provides every NCCL command, parameter, error message, and troubleshooting technique you need for successful deployment on Oracle Cloud Infrastructure (OCI).

## Table of Contents
1. [Why NCCL Exists](#why-nccl-exists)
2. [Understanding Collective Communications](#understanding-collective-communications)
3. [NCCL Fundamentals](#nccl-fundamentals)
4. [Complete NCCL Commands Reference](#complete-nccl-commands-reference)
5. [All NCCL Environment Variables](#all-nccl-environment-variables)
6. [NCCL Error Messages and Solutions](#nccl-error-messages-and-solutions)
7. [OCI GPU-Specific Configurations](#oci-gpu-specific-configurations)
8. [Advanced Troubleshooting Scenarios](#advanced-troubleshooting-scenarios)
9. [Performance Tuning Reference](#performance-tuning-reference)
10. [Quick Reference Tables](#quick-reference-tables)

## Why NCCL Exists

### The Distributed Training Challenge

Modern AI models have grown exponentially in size and complexity. Training these models requires distributing computation across multiple GPUs, often spanning multiple nodes in a cluster. This distribution creates a fundamental challenge: **how do GPUs efficiently share and synchronize data during training?**

**The Scale Problem:**
- GPT-3: 175 billion parameters (~700GB in FP32)
- GPT-4: Estimated 1+ trillion parameters
- Training requires hundreds to thousands of GPUs working in parallel
- Each GPU must exchange gradients, weights, and activations with peers

**Why Traditional Approaches Fail:**

| Approach | Why It Doesn't Scale | Performance Impact |
|----------|---------------------|-------------------|
| **Point-to-Point MPI** | Every GPU sends to every other GPU (O(n²) messages) | Latency increases exponentially with GPU count |
| **Parameter Server** | Centralized bottleneck; single server overwhelmed | Network bandwidth saturated; server becomes bottleneck |
| **CPU-mediated transfers** | Data travels GPU→CPU→Network→CPU→GPU | 10-100x slower than GPU-direct communication |
| **Naive broadcast** | Sequential sends waste bandwidth | Only one GPU sending at a time |
| **TCP/IP sockets** | High latency, CPU overhead | Cannot leverage RDMA or GPU-direct |

### NCCL's Solution: Optimized Collective Primitives

NCCL (NVIDIA Collective Communications Library) solves these problems by providing **highly optimized collective communication patterns** specifically designed for GPU clusters:

**Key Innovations:**

1. **Ring and Tree Algorithms**: Mathematically optimal data flow patterns that minimize hops and maximize bandwidth utilization
2. **GPU-Direct RDMA**: Bypasses CPU entirely - GPUs communicate directly via InfiniBand/RoCE
3. **NVLink Exploitation**: Uses high-speed GPU-to-GPU interconnects (900GB/s on H100, 1800GB/s on GB200)
4. **Topology Awareness**: Automatically discovers and optimizes for your specific hardware layout
5. **Overlap Communication**: Hides network latency by overlapping computation with data transfers
6. **Multi-rail Support**: Aggregates bandwidth across multiple NICs per GPU

**Performance Impact:**
```
Traditional MPI AllReduce (8 GPUs):
  - Time: 45ms for 1GB gradient sync
  - Bandwidth: ~22 GB/s aggregate

NCCL AllReduce (8 GPUs with NVLink):
  - Time: 1.8ms for 1GB gradient sync  (25x faster)
  - Bandwidth: ~550 GB/s aggregate     (25x higher)

At 1000 GPUs (cross-node with InfiniBand):
  - NCCL achieves 90% of theoretical network bandwidth
  - MPI achieves <30% due to inefficient messaging patterns
```

### The Training Workflow Where NCCL Matters

**Distributed Data Parallel (DDP) Training Loop:**

```
1. Forward Pass (local on each GPU)
   ├─ Each GPU processes different batch of data
   └─ Computes local loss and gradients

2. Gradient Synchronization ← NCCL CRITICAL PATH
   ├─ AllReduce: Sum gradients across all GPUs
   ├─ Average: Divide by number of GPUs
   └─ Result: Synchronized gradients on all GPUs

3. Parameter Update (local on each GPU)
   ├─ Apply optimizer step with synchronized gradients
   └─ All GPUs now have identical updated weights

4. Repeat for next batch
```

**Without NCCL:** Gradient synchronization takes 40-60% of training time
**With NCCL:** Gradient synchronization takes 3-8% of training time (often overlapped)

### Alternative Libraries and When NCCL is Used

| Library | Use Case | Relationship to NCCL |
|---------|----------|---------------------|
| **NCCL** | NVIDIA GPUs (CUDA) | Primary implementation |
| **RCCL** | AMD GPUs (ROCm) | AMD's port of NCCL |
| **MPI** | CPU clusters, legacy HPC | Can use NCCL as transport layer |
| **Gloo** | Facebook's library | CPU fallback; PyTorch uses NCCL for GPUs |
| **oneCCL** | Intel GPUs/CPUs | Intel's equivalent |
| **SCCL** | Microsoft's research | Experimental custom collectives |

**In practice:** Every major ML framework uses NCCL for NVIDIA GPUs:
- PyTorch: `torch.distributed` uses NCCL backend
- TensorFlow: `tf.distribute.Strategy` uses NCCL
- JAX: `pmap` and `pjit` use NCCL
- MXNet: `KVStore` uses NCCL

## Understanding Collective Communications

### What Are Collective Operations?

Collective operations are **coordinated communication patterns** where multiple processes work together to exchange data. Unlike point-to-point communication (A sends to B), collectives involve **all participants simultaneously**.

**Key Characteristics:**
- **Synchronization point**: All processes must participate
- **Optimized data flow**: Minimizes total data movement
- **Bandwidth efficient**: Maximizes use of available network links
- **Mathematically proven**: Optimal algorithms for specific topologies

### The Mathematics Behind Collectives

**AllReduce Example (Ring Algorithm):**

For N GPUs with ring topology:
```
Number of steps: 2(N-1)
Data per GPU:    M / N  (where M = total data size)
Total bandwidth: M × (2(N-1)/N) ≈ 2M as N→∞

Scaling: Bandwidth stays constant regardless of GPU count!
```

**Compare to Naive Approach:**
```
Each GPU broadcasts to all others: N × (N-1) messages
Total data movement: M × N × (N-1)

Scaling: O(N²) - becomes prohibitively expensive
```

### Collective Operation Deep Dive

#### 1. AllReduce - The Workhorse of Distributed Training

**What it does:** Reduce data across all GPUs, distribute result to all

**Real-world example:**
```python
# PyTorch distributed training
# Each GPU has computed local gradients
local_gradient = torch.tensor([1.5, 2.0, 3.5])  # GPU 0
local_gradient = torch.tensor([2.0, 1.5, 4.0])  # GPU 1
local_gradient = torch.tensor([1.0, 2.5, 3.0])  # GPU 2

# AllReduce with SUM operation
dist.all_reduce(local_gradient, op=dist.ReduceOp.SUM)

# Result on ALL GPUs:
# [4.5, 6.0, 10.5]  = sum of all local gradients

# Averaged gradient (divide by 3):
# [1.5, 2.0, 3.5]   = global averaged gradient
```

**Why it's critical:** 95% of distributed training communication is AllReduce

**Data Flow (Ring Algorithm for 4 GPUs):**
```
Step 1 (Reduce-Scatter):
GPU0: [A] → GPU1
GPU1: [B] → GPU2
GPU2: [C] → GPU3
GPU3: [D] → GPU0

Step 2-3: Continue ring pattern
Each GPU accumulates partial sums

Step 4-6 (AllGather):
GPUs exchange final results
All GPUs end with complete reduced data
```

#### 2. AllGather - Collecting Distributed Data

**What it does:** Each GPU contributes unique data, all GPUs receive full dataset

**Real-world example:**
```python
# Distributed inference with tensor parallelism
# Each GPU has different shard of model output

local_output = torch.tensor([0.1, 0.2])  # GPU 0: predictions for samples 0-1
local_output = torch.tensor([0.3, 0.4])  # GPU 1: predictions for samples 2-3
local_output = torch.tensor([0.5, 0.6])  # GPU 2: predictions for samples 4-5

# AllGather collects all outputs
output_list = [torch.zeros_like(local_output) for _ in range(world_size)]
dist.all_gather(output_list, local_output)

# Result on ALL GPUs:
# [[0.1, 0.2], [0.3, 0.4], [0.5, 0.6]]
```

**Use cases:**
- Gathering predictions from tensor-parallel model shards
- Collecting metrics from all workers
- Building global vocabulary in NLP training

#### 3. ReduceScatter - Efficient Parameter Sharding

**What it does:** Reduce data, but distribute different chunks to each GPU

**Real-world example:**
```python
# ZeRO optimizer: Reduce gradients but shard across GPUs
# Each GPU only needs subset of parameters

gradient = torch.tensor([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])  # All GPUs

output = torch.zeros(2)  # Each GPU gets 2 elements
dist.reduce_scatter(output, [gradient], op=dist.ReduceOp.SUM)

# Results distributed:
# GPU 0: [sum(1.0s), sum(2.0s)]  - first 2 elements
# GPU 1: [sum(3.0s), sum(4.0s)]  - middle 2 elements
# GPU 2: [sum(5.0s), sum(6.0s)]  - last 2 elements
```

**Use cases:**
- ZeRO optimizer (DeepSpeed)
- Fully Sharded Data Parallel (FSDP)
- Memory-efficient large model training

#### 4. Broadcast - Initialization and Control

**What it does:** One GPU sends data to all others

**Real-world example:**
```python
# Synchronize model weights at training start
if rank == 0:
    # Only rank 0 loads the checkpoint
    model_state = torch.load('checkpoint.pt')
else:
    model_state = torch.zeros_like(model)

# Broadcast from rank 0 to all
dist.broadcast(model_state, src=0)

# Now all GPUs have identical model weights
```

**Use cases:**
- Initial model weight distribution
- Broadcasting hyperparameters
- Sending control signals (stop training, save checkpoint)

#### 5. Reduce - Aggregation to Single GPU

**What it does:** Aggregate data to one destination GPU

**Real-world example:**
```python
# Collect validation loss from all GPUs to rank 0 for logging

local_loss = torch.tensor([0.45])  # Different on each GPU

if rank == 0:
    total_loss = torch.zeros(1)
else:
    total_loss = None

dist.reduce(local_loss, dst=0, op=dist.ReduceOp.SUM)

if rank == 0:
    avg_loss = total_loss / world_size
    print(f"Validation loss: {avg_loss}")
```

**Use cases:**
- Metrics aggregation for logging
- Gradient accumulation to parameter server
- Checkpointing (aggregate to master node)

### Collective Patterns in Popular Training Frameworks

**PyTorch Distributed Data Parallel (DDP):**
```
Forward:  Local computation (no collectives)
Backward: AllReduce gradients (NCCL)
Update:   Local parameter update
```

**DeepSpeed ZeRO Stage 2:**
```
Forward:  Local computation
Backward: ReduceScatter gradients (sharded)
Update:   AllGather parameters (for next forward)
```

**Megatron-LM Tensor Parallelism:**
```
Forward:  AllReduce across tensor-parallel GPUs
         AllGather activations for next layer
Backward: ReduceScatter gradients
         AllReduce for tensor-parallel layers
```

**FSDP (Fully Sharded Data Parallel):**
```
Forward:  AllGather parameters (just-in-time)
         Discard after layer
Backward: AllGather parameters again
         ReduceScatter gradients (sharded)
```

### Why Optimized Collectives Matter

**Training throughput is bounded by slowest collective:**

```
Example: Training GPT-3 style model on 1024 GPUs

Naive AllReduce:
  - Gradient size: 700GB
  - Naive algorithm: 700GB × 1024 transfers = 716TB total
  - Time @ 100GB/s: 7,160 seconds (2 hours!)

NCCL Ring AllReduce:
  - Same gradient: 700GB
  - Ring algorithm: 2 × 700GB = 1.4TB total
  - Time @ 100GB/s: 14 seconds

Speedup: 512x faster!

This difference means:
  - Naive: 2% of time training, 98% waiting
  - NCCL: 85% of time training, 15% communication
```

### Topology Awareness in NCCL

NCCL automatically optimizes collective algorithms based on your hardware:

**Single Node (NVLink):**
```
8 GPUs fully connected via NVLink
→ Uses NVLink-optimized ring/tree
→ 900 GB/s per GPU (H100)
→ AllReduce completes in microseconds
```

**Multi-Node (InfiniBand):**
```
Network topology:
  - 8 GPUs per node (NVLink connected)
  - Nodes connected via InfiniBand (400Gbps)

NCCL strategy:
  1. Intra-node reduce using NVLink (fast)
  2. Inter-node reduce using IB (one GPU per node)
  3. Intra-node broadcast results back (fast)

Result: Minimize slow cross-node traffic
```

**Multi-Rack (GB200 NVL72):**
```
72 GPUs in single rack with NVLink mesh
→ NCCL discovers 18-way NVLink connections
→ Uses custom algorithms for NVLink fabric
→ Achieves 1400+ GB/s aggregate bandwidth
```

## NCCL Fundamentals

### Core Collective Operations

NCCL implements five fundamental collective operations:

| Operation | Description | Use Case | Data Flow Pattern |
|-----------|-------------|----------|-------------------|
| **AllReduce** | Sum/average data from all GPUs, distribute result to all | Gradient synchronization in distributed training | All → Reduce → All |
| **AllGather** | Collect unique data from each GPU, share complete set with all | Sharded state replication | [A], [B], [C] → [A,B,C] on all |
| **ReduceScatter** | Reduce data and distribute unique portions to each GPU | Model parallelism | Full data → Reduced chunks |
| **Broadcast** | Send data from root to all GPUs | Weight initialization | Root → All |
| **Reduce** | Aggregate data to single destination | Parameter server architectures | All → Root |

### NCCL Algorithms

| Algorithm | Best For | Characteristics | Bandwidth Scaling |
|-----------|----------|-----------------|-------------------|
| **Ring** | Small messages | Linear topology, low memory overhead | O(n) latency |
| **Tree** | Medium messages | Hierarchical, reduced latency | O(log n) latency |
| **SplitTree** | Large messages | Multiple trees, maximum bandwidth | Parallel processing |
| **CollNet** | Network offload | Hardware acceleration | Hardware-dependent |

### NCCL Protocols

| Protocol | Message Size | Latency | Throughput | Memory Usage |
|----------|-------------|---------|------------|--------------|
| **Simple** | Large (>256KB) | High | Maximum | Standard |
| **LL (Low Latency)** | Small (<4KB) | Minimum | Lower | Reduced |
| **LL128** | Medium (4KB-256KB) | Low | High | 128-byte chunks |

## Complete NCCL Commands Reference

### Basic NCCL Test Commands

```bash
# Single GPU test
./build/all_reduce_perf -b 8 -e 16G -f 2 -g 1

# Multi-GPU single node
./build/all_reduce_perf -b 8 -e 16G -f 2 -g 8

# Multi-node with MPI
mpirun -np 16 -H node1:8,node2:8 ./build/all_reduce_perf -b 8 -e 16G -f 2 -g 1

# With environment variables
mpirun -np 16 \
  -x NCCL_DEBUG=INFO \
  -x NCCL_TREE_THRESHOLD=0 \
  ./build/all_reduce_perf -b 8 -e 16G -f 2 -g 1
```

### Building NCCL Tests

```bash
# Clone repository
git clone https://github.com/NVIDIA/nccl-tests.git
cd nccl-tests

# Build with MPI support
make MPI=1 MPI_HOME=/usr/mpi/gcc/openmpi-4.1.5rc2

# Build with CUDA path specified
make CUDA_HOME=/usr/local/cuda-12.2 MPI=1

# Build for specific NCCL version
make NCCL_HOME=/usr/local/nccl-2.19 MPI=1

# Clean build
make clean && make MPI=1
```

### NCCL Test Parameters

| Parameter | Description | Example Values | Default |
|-----------|-------------|----------------|---------|
| `-b` | Minimum size | 8, 1K, 1M, 1G | 8 |
| `-e` | Maximum size | 128M, 1G, 16G | 128M |
| `-f` | Size increment factor | 2, 4 | 2 |
| `-g` | GPUs per thread | 1, 2, 4, 8 | 1 |
| `-c` | Check correctness | 0, 1 | 1 |
| `-n` | Number of iterations | 20, 100, 1000 | 20 |
| `-w` | Warmup iterations | 5, 10 | 5 |
| `-p` | Parallel operations | 0, 1 | 0 |
| `-t` | Number of threads | 1, 2, 4 | 1 |
| `-d` | CUDA device | 0, 1, 2... | All |

### All NCCL Test Binaries

```bash
# Collective operations tests
all_reduce_perf      # AllReduce performance test
all_gather_perf      # AllGather performance test
broadcast_perf       # Broadcast performance test
reduce_perf          # Reduce performance test
reduce_scatter_perf  # ReduceScatter performance test
alltoall_perf       # AlltoAll performance test

# Point-to-point tests
sendrecv_perf       # Send/Receive performance
hypercube_perf      # Hypercube pattern test

# Scatter operations
scatter_perf        # Scatter performance test
gather_perf         # Gather performance test
```

## All NCCL Environment Variables

### Core Communication Variables

```bash
# Debug and logging
export NCCL_DEBUG=INFO           # OFF, VERSION, WARN, INFO, TRACE
export NCCL_DEBUG_SUBSYS=ALL     # INIT, COLL, P2P, SHM, NET, GRAPH, TUNING, ENV, ALLOC, ALL
export NCCL_DEBUG_FILE=/path/to/log.txt

# Algorithm selection
export NCCL_ALGO=Ring             # Ring, Tree, SplitTree, CollNet, Auto
export NCCL_PROTO=Simple          # Simple, LL, LL128

# Tree-specific parameters
export NCCL_TREE_THRESHOLD=0      # Disable tree for messages below size
export NCCL_MIN_NCHANNELS=4       # Minimum number of channels
export NCCL_MAX_NCHANNELS=16      # Maximum number of channels

# Shared memory
export NCCL_SHM_DISABLE=0         # 0=enabled, 1=disabled
export NCCL_SHM_USE_CUDA_MEMCPY=0 # Use CUDA memcpy for shared memory

# P2P settings
export NCCL_P2P_DISABLE=0         # Disable P2P communication
export NCCL_P2P_LEVEL=LOC         # LOC, NVL, PIX, PXB, PHB, NODE, SYS
export NCCL_P2P_READ=1            # Use P2P reads
export NCCL_P2P_DIRECT_DISABLE=0 # Disable direct P2P
```

### Network and InfiniBand Variables

```bash
# Network interface selection
export NCCL_SOCKET_IFNAME=eth0,ens1f0   # Comma-separated interfaces
export NCCL_SOCKET_FAMILY=AF_INET       # AF_INET, AF_INET6
export NCCL_NET="IB"                    # IB, Socket
export NCCL_NET_SHARED_BUFFERS=1        # Enable shared buffers

# InfiniBand configuration
export NCCL_IB_DISABLE=0                # 0=enabled, 1=disabled
export NCCL_IB_HCA=mlx5_0,mlx5_1       # Specific HCA devices
export NCCL_IB_HCA=^mlx5_2,mlx5_3      # Exclude specific HCAs (^ prefix)
export NCCL_IB_TC=41                    # Traffic class (0-255)
export NCCL_IB_SL=0                     # Service level (0-15)
export NCCL_IB_GID_INDEX=3              # GID table index
export NCCL_IB_QPS_PER_CONNECTION=4     # Queue pairs per connection
export NCCL_IB_SPLIT_DATA_ON_QPS=0      # Split data across QPs
export NCCL_IB_TIMEOUT=18               # IB timeout (4us * 2^timeout)
export NCCL_IB_RETRY_CNT=7              # IB retry count
export NCCL_IB_PCI_RELAXED_ORDERING=0   # PCIe relaxed ordering
export NCCL_IB_CUDA_SUPPORT=1           # CUDA support for IB
export NCCL_IB_ADAPTIVE_ROUTING=0       # Adaptive routing

# RoCE-specific
export NCCL_IB_ROCE_VERSION_NUM=2       # RoCE version (1 or 2)
export NCCL_IB_AR_THRESHOLD=8192        # Adaptive routing threshold

# GPU Direct RDMA
export NCCL_NET_GDR_LEVEL=LOC           # LOC, PATH, PIX, PXB, PHB, NODE, SYS
export NCCL_NET_GDR_READ=1              # Enable GDR read
export NCCL_NET_GDR_FLUSH_DISABLE=0     # Disable GDR flush
```

### Topology and Affinity Variables

```bash
# Topology configuration
export NCCL_TOPO_FILE=/path/to/topology.xml  # Custom topology file
export NCCL_GRAPH_FILE=/path/to/graph.xml    # Custom graph file
export NCCL_TOPO_DUMP_FILE=/path/to/dump.xml # Dump detected topology

# CPU affinity
export NCCL_CPU_AFFINITY=0,1,2,3        # CPU cores to use
export NCCL_SET_THREAD_AFFINITY=0       # Set thread affinity

# NUMA settings
export NCCL_NUMA_NODE=0                 # NUMA node to use
export NCCL_SOCKET_NTHREADS=4          # Threads per socket

# Cross-NIC communication
export NCCL_CROSS_NIC=0                 # 0=same NIC only, 1=allow cross-NIC
export NCCL_SINGLE_RING_THRESHOLD=262144 # Single ring threshold
```

### Advanced and Platform-Specific Variables

```bash
# GB200-specific (NVIDIA)
export NCCL_CUMEM_ENABLE=1              # Enable CUDA unified memory
export NCCL_NVLS_ENABLE=1               # Enable NVLink Sharp
export NCCL_MNNVL_ENABLE=1              # Enable multi-node NVLink
export NCCL_NVLS_NCHANNELS=16          # NVLink Sharp channels
export NCCL_NVLS_TREE_THRESHOLD=0       # NVLink Sharp tree threshold

# AMD MI300X (RCCL)
export NCCL_MIN_NRINGS=4                # Minimum number of rings
export NCCL_MAX_NRINGS=16               # Maximum number of rings
export NCCL_NTHREADS=512               # Number of NCCL threads
export NCCL_NSOCKS_PERTHREAD=4         # Sockets per thread
export NCCL_SOCKET_NTHREADS=8          # Socket threads
export NCCL_BUFFSIZE=4194304           # Buffer size

# Collectives Network (CollNet)
export NCCL_COLLNET_ENABLE=1           # Enable CollNet
export NCCL_COLLNET_NODE_THRESHOLD=2   # Minimum nodes for CollNet

# UCX integration
export UCX_TLS=tcp,cuda_copy,cuda_ipc  # UCX transport layer
export UCX_NET_DEVICES=eth0            # UCX network devices
export UCX_MEMTYPE_CACHE=n             # Memory type cache
export UCX_RNDV_THRESH=8192           # Rendezvous threshold

# Performance tuning
export NCCL_LAUNCH_MODE=PARALLEL       # PARALLEL, GROUP
export NCCL_BUFFSIZE=4194304          # Ring buffer size (4MB default)
export NCCL_LL_BUFFSIZE=16384         # LL protocol buffer size
export NCCL_LL128_BUFFSIZE=1048576    # LL128 protocol buffer size
export NCCL_CHECKS_DISABLE=0          # Disable data checks
export NCCL_CHECK_POINTERS=0          # Check CUDA pointers

# Multi-process service
export CUDA_MPS_PIPE_DIRECTORY=/tmp/nvidia-mps
export CUDA_MPS_LOG_DIRECTORY=/tmp/nvidia-log

# Timeout and reliability
export NCCL_TIMEOUT_MS=600000         # Timeout in milliseconds (10 min)
export NCCL_CONNECT_TIMEOUT_MS=60000  # Connection timeout (1 min)
export NCCL_ASYNC_ERROR_HANDLING=1    # Async error handling
```

## NCCL Error Messages and Solutions

### Common NCCL Errors

| Error Message | Root Cause | Solution |
|---------------|------------|----------|
| `NCCL WARN NET/IB: No device found` | NCCL cannot access InfiniBand devices | 1. Check `ibv_devinfo`<br>2. Set `NCCL_IB_HCA` explicitly<br>3. Verify RDMA modules loaded<br>4. Check `NCCL_IB_DISABLE` is 0 |
| `NCCL WARN failed to open RDMA device` | RDMA device permissions or driver issue | 1. Check device permissions<br>2. Verify user in rdma group<br>3. Reload IB drivers<br>4. Check `ulimit -l` for locked memory |
| `NCCL WARN Bootstrap: no socket interface found` | Network interface not accessible | 1. Set `NCCL_SOCKET_IFNAME`<br>2. Check interface with `ip addr`<br>3. Verify network connectivity<br>4. Check firewall rules |
| `NCCL WARN Cuda failure 'out of memory'` | Insufficient GPU memory | 1. Reduce batch size<br>2. Check `nvidia-smi` for memory usage<br>3. Clear GPU memory<br>4. Reduce `NCCL_BUFFSIZE` |
| `NCCL WARN Ring/Tree : no path found` | Topology detection failure | 1. Set `NCCL_TOPO_FILE`<br>2. Check PCIe topology<br>3. Verify NVLink connections<br>4. Set `NCCL_P2P_LEVEL` |
| `NCCL WARN Connect: Transport/P2P setup failed` | P2P communication failure | 1. Check `NCCL_P2P_DISABLE`<br>2. Verify GPU peer access<br>3. Check PCIe ACS settings<br>4. Update GPU drivers |
| `NCCL WARN AllReduce: invalid size` | Mismatched buffer sizes | 1. Verify all ranks use same size<br>2. Check data type consistency<br>3. Align buffer sizes |
| `NCCL WARN Timeout` | Operation exceeded timeout | 1. Increase `NCCL_TIMEOUT_MS`<br>2. Check network latency<br>3. Verify all ranks participating<br>4. Check for deadlocks |
| `NCCL WARN Got completion with error` | RDMA completion error | 1. Check IB fabric health<br>2. Verify QP state<br>3. Check for packet loss<br>4. Review IB counters |
| `NCCL WARN Call to ibv_create_qp failed` | Queue pair creation failure | 1. Check `ulimit -n` for file descriptors<br>2. Reduce `NCCL_IB_QPS_PER_CONNECTION`<br>3. Check IB resources |
| `NCCL WARN NUMA node mismatch` | GPU-CPU affinity issue | 1. Check `numactl --hardware`<br>2. Set proper CPU affinity<br>3. Use `--bind-to numa` with MPI |
| `NCCL WARN peer access disabled` | GPU peer access not enabled | 1. Enable peer access in code<br>2. Check GPU topology<br>3. Verify PCIe configuration |

### Advanced Error Patterns

#### Pattern: Slow AllReduce Performance
```bash
# Symptoms: Lower than expected bandwidth
# Debug approach:
export NCCL_DEBUG=INFO
export NCCL_DEBUG_SUBSYS=INIT,NET,GRAPH

# Check topology
nvidia-smi topo -m

# Test different algorithms
export NCCL_ALGO=Ring  # Test Ring
export NCCL_ALGO=Tree  # Test Tree

# Check for throttling
nvidia-smi -q -d PERFORMANCE
```

#### Pattern: Inconsistent Performance Across Runs
```bash
# Enable consistent settings
export NCCL_NTHREADS=512
export NCCL_NSOCKS_PERTHREAD=4
export NCCL_MIN_NCHANNELS=8
export NCCL_MAX_NCHANNELS=8

# Pin CPU affinity
export NCCL_CPU_AFFINITY=0-7
export NCCL_SET_THREAD_AFFINITY=1

# Disable dynamic frequency
sudo nvidia-smi -pm 1
sudo nvidia-smi -lgc 1980  # Lock GPU clocks
```

#### Pattern: Multi-Node Hangs
```bash
# Debug multi-node issues
export NCCL_DEBUG=TRACE
export NCCL_DEBUG_FILE=/tmp/nccl_debug.log

# Test connectivity
mpirun -np 2 -H node1:1,node2:1 hostname

# Check firewall
sudo iptables -F  # Temporarily flush rules

# Verify environment propagation
mpirun -x NCCL_DEBUG=VERSION -np 2 env | grep NCCL
```

## OCI GPU-Specific Configurations

### GB200 NVL72 Configuration

```bash
# Full rack (72 GPUs) with NVLink fabric
mpirun --mca btl_tcp_if_include eth0 \
  --map-by ppr:4:node \
  --host $(cat hostfile | paste -sd, | sed 's/,/:4,/g'):4 \
  -x NCCL_DEBUG=WARN \
  -x NCCL_CUMEM_ENABLE=1 \
  -x NCCL_NET_PLUGIN=sys \
  -x NCCL_NVLS_ENABLE=1 \
  -x NCCL_MNNVL_ENABLE=1 \
  -x NCCL_IB_HCA=^mlx5 \
  -x NCCL_IB_DISABLE=1 \
  -x NCCL_TOPO_FILE=/etc/nvidia-imex/topology.xml \
  -x NCCL_GRAPH_FILE=/etc/nvidia-imex/graph.xml \
  -np 72 \
  /opt/oci-hpc/nccl-tests/build/all_reduce_perf -b 8 -e 16G -f 2 -g 1

# GB200 with InfiniBand (cross-rack)
mpirun --mca btl_tcp_if_include eth0 \
  --map-by ppr:4:node \
  --hostfile hostfile \
  -x NCCL_DEBUG=INFO \
  -x NCCL_IB_HCA=mlx5_0,mlx5_1,mlx5_2,mlx5_3 \
  -x NCCL_IB_TC=41 \
  -x NCCL_IB_SL=0 \
  -x NCCL_IB_GID_INDEX=3 \
  -x NCCL_NET_GDR_LEVEL=LOC \
  -x NCCL_NET_GDR_READ=1 \
  -x NCCL_P2P_LEVEL=NVL \
  -x NCCL_CROSS_NIC=1 \
  -np 144 \
  /opt/oci-hpc/nccl-tests/build/all_reduce_perf -b 1M -e 16G -f 2 -g 1
```

### H100/H200 Configuration

```bash
# H100/H200 8-GPU nodes with RoCE
mpirun --mca pml ucx \
  --bind-to numa \
  -npernode 8 \
  --mca coll ^hcoll \
  -x NCCL_DEBUG=WARN \
  -x NCCL_NET_PLUGIN="aws-ofi-nccl" \
  -x UCX_TLS=tcp,cuda_copy,cuda_ipc \
  -x UCX_NET_DEVICES=eth0 \
  -x NCCL_IB_HCA=mlx5_0:1,mlx5_1:1,mlx5_2:1,mlx5_3:1 \
  -x NCCL_IB_TC=105 \
  -x NCCL_IB_SL=5 \
  -x NCCL_IB_GID_INDEX=3 \
  -x NCCL_IB_QPS_PER_CONNECTION=4 \
  -x NCCL_IB_SPLIT_DATA_ON_QPS=1 \
  -x NCCL_SOCKET_IFNAME=ens1f0 \
  -x NCCL_SOCKET_FAMILY=AF_INET \
  -x NCCL_P2P_LEVEL=NVL \
  -x NCCL_MIN_NCHANNELS=4 \
  -x NCCL_TREE_THRESHOLD=0 \
  --np 64 \
  --hostfile hostfile \
  /opt/oci-hpc/nccl-tests/build/all_reduce_perf -b 1G -e 16G -f 2 -g 1
```

### A100 Configuration

```bash
# A100 with NVSwitch
mpirun --bind-to numa \
  -npernode 8 \
  --mca btl ^openib \
  --mca pml ob1 \
  -x NCCL_DEBUG=INFO \
  -x NCCL_IB_HCA=mlx5_0,mlx5_1,mlx5_2,mlx5_3 \
  -x NCCL_IB_TC=41 \
  -x NCCL_IB_SL=0 \
  -x NCCL_IB_GID_INDEX=3 \
  -x NCCL_SOCKET_IFNAME=bond0 \
  -x NCCL_P2P_LEVEL=NVL \
  -x NCCL_NET_GDR_LEVEL=LOC \
  -x NCCL_NET_GDR_READ=1 \
  -x NCCL_ALGO=Ring \
  -x NCCL_PROTO=Simple \
  -x NCCL_MIN_NCHANNELS=4 \
  -x NCCL_BUFFSIZE=8388608 \
  --np 32 \
  --hostfile hostfile \
  /opt/oci-hpc/nccl-tests/build/all_reduce_perf -b 8M -e 8G -f 2 -g 1
```

### MI300X (AMD) Configuration

```bash
# AMD MI300X with RCCL
mpirun --bind-to numa \
  --mca oob_tcp_if_exclude docker,lo \
  --mca btl_tcp_if_exclude docker,lo \
  --mca btl ^openib \
  -npernode 8 \
  -x NCCL_DEBUG=VERSION \
  -x NCCL_IB_HCA=mlx5_0,mlx5_2,mlx5_3,mlx5_4,mlx5_5,mlx5_7,mlx5_8,mlx5_9 \
  -x NCCL_SOCKET_IFNAME=rdma0 \
  -x NCCL_IB_TC=41 \
  -x NCCL_IB_SL=0 \
  -x NCCL_IB_GID_INDEX=3 \
  -x NCCL_IB_QPS_PER_CONNECTION=2 \
  -x NCCL_IB_SPLIT_DATA_ON_QPS=4 \
  -x NCCL_ALGO=Ring \
  -x NCCL_PROTO=Simple \
  -x NCCL_MIN_NRINGS=4 \
  -x NCCL_MAX_NRINGS=16 \
  -x NCCL_BUFFSIZE=4194304 \
  -x NCCL_NTHREADS=512 \
  -x NCCL_NSOCKS_PERTHREAD=4 \
  -x NCCL_SOCKET_NTHREADS=8 \
  --host hpc-node-1:8,hpc-node-2:8 \
  --np 16 \
  /opt/rccl-tests/build/all_reduce_perf -b 8 -e 16G -f 2 -g 1
```

## Advanced Troubleshooting Scenarios

### Scenario 1: Debugging Topology Detection

```bash
# Step 1: Dump detected topology
export NCCL_TOPO_DUMP_FILE=/tmp/topology.xml
mpirun -np 8 ./all_reduce_perf -b 8 -e 8 -g 1

# Step 2: Analyze topology
cat /tmp/topology.xml

# Step 3: Check GPU-NIC affinity
nvidia-smi topo -m

# Step 4: Verify NVLink status
nvidia-smi nvlink -s
nvidia-smi nvlink -c

# Step 5: Create custom topology if needed
cat > /tmp/custom_topo.xml << EOF
<system>
  <cpu numaid="0" affinity="00000000,0000ffff">
    <pci busid="0000:07:00.0" class="0x030200" vendor="0x10de"/>
    <pci busid="0000:08:00.0" class="0x020000" vendor="0x15b3"/>
  </cpu>
</system>
EOF

export NCCL_TOPO_FILE=/tmp/custom_topo.xml
```

### Scenario 2: Resolving IB Device Enumeration Issues

```bash
# Step 1: List all IB devices
ibv_devinfo

# Step 2: Check device to GPU mapping
for i in /sys/class/infiniband/*/device; do
  echo $(basename $(dirname $i)): $(readlink $i)
done

# Step 3: Find correct GID index
show_gids | grep -v 0000:0000

# Step 4: Test specific device
export NCCL_IB_HCA=mlx5_0
export NCCL_IB_GID_INDEX=3
./all_reduce_perf -b 8M -e 8M -g 1

# Step 5: Verify RDMA connectivity
ib_write_bw -d mlx5_0 -i 3 --report_gbits
```

### Scenario 3: Performance Profiling

```bash
# Step 1: Enable detailed timing
export NCCL_DEBUG=INFO
export NCCL_DEBUG_SUBSYS=INIT,COLL,NET

# Step 2: Profile with nvprof
nvprof --print-gpu-trace mpirun -np 8 ./all_reduce_perf -b 1G -e 1G

# Step 3: Use Nsight Systems
nsys profile -t cuda,nvtx,mpi \
  mpirun -np 8 ./all_reduce_perf -b 1G -e 1G

# Step 4: Analyze bandwidth vs message size
for size in 8 1K 1M 100M 1G 10G; do
  echo "Testing size: $size"
  mpirun -np 8 ./all_reduce_perf -b $size -e $size -n 100
done
```

### Scenario 4: Multi-Rail Configuration

```bash
# Configure multiple rails
export NCCL_IB_HCA=mlx5_0,mlx5_1,mlx5_2,mlx5_3
export NCCL_IB_SPLIT_DATA_ON_QPS=1
export NCCL_IB_QPS_PER_CONNECTION=2
export NCCL_CROSS_NIC=1
export NCCL_SINGLE_RING_THRESHOLD=262144

# Test with rail isolation
for rail in 0 1 2 3; do
  export NCCL_IB_HCA=mlx5_${rail}
  echo "Testing rail $rail"
  ./all_reduce_perf -b 1G -e 1G
done
```

## Performance Tuning Reference

### Bandwidth Formulas

**Bus Bandwidth vs Algorithm Bandwidth:**
```
Algorithm_BW = Bus_BW × (2 × (n-1) / n)  # For AllReduce
Algorithm_BW = Bus_BW × ((n-1) / n)       # For Broadcast/Reduce
Algorithm_BW = Bus_BW                     # For AllGather
```

**Expected Bandwidth by Interconnect:**
| Interconnect | Theoretical | Typical AllReduce |
|--------------|-------------|-------------------|
| PCIe 3.0 x16 | 16 GB/s | 12-14 GB/s |
| PCIe 4.0 x16 | 32 GB/s | 25-28 GB/s |
| PCIe 5.0 x16 | 64 GB/s | 50-55 GB/s |
| NVLink 3.0 | 600 GB/s | 480-540 GB/s |
| NVLink 4.0 (H100) | 900 GB/s | 720-810 GB/s |
| NVLink 5.0 (GB200) | 1800 GB/s | 1400-1600 GB/s |
| InfiniBand HDR | 200 Gbps | 20-22 GB/s |
| InfiniBand NDR | 400 Gbps | 40-45 GB/s |
| RoCE 100G | 100 Gbps | 10-11 GB/s |
| RoCE 400G | 400 Gbps | 40-45 GB/s |

### Optimal Parameter Settings by Message Size

| Message Size | Algorithm | Protocol | Channels | Notes |
|-------------|-----------|----------|----------|--------|
| < 1KB | Ring | LL | 1-2 | Minimize latency |
| 1KB - 256KB | Ring/Tree | LL128 | 2-4 | Balance latency/BW |
| 256KB - 10MB | Tree | Simple | 4-8 | Moderate bandwidth |
| 10MB - 100MB | SplitTree | Simple | 8-16 | High bandwidth |
| > 100MB | SplitTree | Simple | 16-32 | Maximum bandwidth |

## Quick Reference Tables

### MPI Launch Options

| Option | Description | Example |
|--------|-------------|---------|
| `-np` | Number of processes | `-np 16` |
| `-npernode` | Processes per node | `-npernode 8` |
| `--hostfile` | File with hostnames | `--hostfile hosts.txt` |
| `-H` | Inline host specification | `-H node1:4,node2:4` |
| `--bind-to` | Process binding | `--bind-to numa` |
| `--map-by` | Process mapping | `--map-by ppr:4:node` |
| `-x` | Export environment variable | `-x NCCL_DEBUG=INFO` |
| `--mca` | MCA parameter | `--mca btl tcp,self` |
| `--oversubscribe` | Allow oversubscription | `--oversubscribe` |

### NCCL Info Commands

```bash
# Check NCCL version
nccl-test -V

# GPU topology
nvidia-smi topo -m

# NVLink status
nvidia-smi nvlink -s

# PCIe bandwidth test
cuda-samples/1_Utilities/bandwidthTest/bandwidthTest

# InfiniBand status
ibstat
ibv_devinfo

# RDMA connectivity test
ib_write_bw
ib_read_bw

# Network interface info
ip addr show
ethtool -S <interface>

# CPU/NUMA topology
lscpu
numactl --hardware

# Check GPU clocks
nvidia-smi -q -d CLOCK

# Monitor GPU utilization
nvidia-smi dmon -s pucvmet
```

### Common Testing Patterns

```bash
# Quick smoke test
./all_reduce_perf -b 8 -e 128M -f 2 -g 1

# Full bandwidth sweep
./all_reduce_perf -b 8 -e 16G -f 2 -g 1

# Stress test (long duration)
./all_reduce_perf -b 1G -e 1G -n 10000 -g 1

# Latency test (small messages)
./all_reduce_perf -b 8 -e 8K -f 2 -n 1000 -g 1

# Multi-threaded test
./all_reduce_perf -b 1G -e 1G -t 4 -g 2

# Correctness validation
./all_reduce_perf -b 1M -e 100M -c 1 -n 100

# All operations test
for op in all_reduce all_gather broadcast reduce reduce_scatter; do
  ./${op}_perf -b 1M -e 1G -f 2
done
```

## Conclusion

This comprehensive guide covers every aspect of NCCL deployment, troubleshooting, and optimization on OCI. From basic commands to advanced debugging scenarios, these references enable successful NCCL implementation across all OCI GPU shapes. Regular testing with these commands and monitoring of error patterns ensures optimal performance and reliability in production environments.

## References

1. NVIDIA NCCL User Guide: https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/overview.html
2. NVIDIA NCCL Tests Repository: https://github.com/NVIDIA/nccl-tests
3. NVIDIA NCCL Source Code: https://github.com/NVIDIA/nccl
4. OCI HPC GitHub Repository: https://github.com/oracle-quickstart/oci-hpc
5. AMD RCCL Documentation: https://rocm.docs.amd.com/projects/rccl/en/latest/
6. NCCL Environment Variables: https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/env.html
7. NCCL Test Performance Metrics: https://github.com/NVIDIA/nccl-tests/blob/master/doc/PERFORMANCE.md