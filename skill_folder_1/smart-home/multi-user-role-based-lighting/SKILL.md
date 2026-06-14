---
name: multi-user-role-based-lighting
description: Teach configuring role-based offline lighting scenes using local user profiles, priority rules, and overrides via NFC, keypad codes, or HA user switching -- preventing cloud auth leakage.
---

# Multi-User Role-Based Lighting

## Roles
- Adult morning, adult sleep, child, guest, cleaner.

## Priority
- Cleaner overrides guest; sleep overrides adult morning.

## Mechanisms
- NFC tag on nightstand for sleep mode.
- Keypad code maps to guest room lighting.
- HA user context for children.


## Teaching exercise
Define three roles and three override paths with fail default.
