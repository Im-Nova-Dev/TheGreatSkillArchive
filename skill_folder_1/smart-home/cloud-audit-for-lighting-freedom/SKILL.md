---
name: cloud-audit-for-lighting-freedom
description: Teach auditing existing smart lighting gear for cloud dependencies and mapping each device to a local alternative path. Covers packet capture, API endpoint analysis, DNS sinkhole verification, and prioritizing which devices to replace first.
---

# Cloud Audit for Lighting Freedom

## Objective
Identify exactly which devices phone home, what data they send, and whether local control is possible without replacement.

## Audit flow
1. Router/ firewall: look for outbound to vendor domains.
2. Wireshark or router capture on IoT VLAN.
3. For each device, document:
   - Device name/model
   - Cloud endpoint
   - Local API presence
   - Migration decision: keep, jailbreak, or replace.

## Decision matrix
- Cloud mandatory + no API → replace.
- Cloud optional + local API → disable cloud, keep.
- Open firmware available → flash or migrate adapter.

## Teaching exercise
Give 3 common bulbs/brands; apprentice completes audit within 20 minutes using public docs.
