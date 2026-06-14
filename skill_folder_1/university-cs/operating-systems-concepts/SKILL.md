---
name: operating-systems-concepts
description: Teach operating systems fundamentals including processes, threads, scheduling, memory management, virtual memory, file systems, concurrency, synchronization, and deadlock with teaching narratives and common problems.
---

# Operating Systems Concepts

## Mental model
OS is a resource multiplexer: CPU, memory, disk, and network.

## Core topics

1. Processes and threads
   - States and transitions
   - PCB and context switch

2. CPU scheduling
   - FCFS, SJF, Round Robin, MLFQ
   - Preemptive vs non-preemptive

3. Synchronization
   - Mutex, semaphore, monitor
   - Producer-consumer, readers-writers
   - Priority inversion

4. Memory management
   - Contiguous, paging, segmentation
   - Page tables, TLB
   - Demand paging and page replacement

5. Virtual memory
   - Address translation
   - Copy-on-write
   - Memory-mapped files

6. File systems
   - Inodes and directory structures
   - Allocation: contiguous, linked, indexed
   - Journaling

7. Deadlock
   - Conditions, prevention, avoidance, detection

## Teaching approach
Use the dining philosophers as a recurring example.
Draw state diagrams.
Relate to real OS behavior in Linux and Windows.
