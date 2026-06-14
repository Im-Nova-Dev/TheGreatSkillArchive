---
name: non-euclidean-geometry-and-hyperbolic-metric-spaces
description: Teach non-Euclidean geometry and hyperbolic metric spaces including hyperbolic plane models, curvature, Cayley graphs, Gromov hyperbolicity, Poincaré inequality, hyperbolic group theory, and connections to geometric group theory and modern metric geometry with teaching exercises.
category: quantitative-theory
---

# Non-Euclidean Geometry and Hyperbolic Metric Spaces

## Core Concepts

### 1. Curvature and the Parallel Postulate
- Euclidean geometry has zero curvature and exactly one line through a point parallel to a given line.
- Spherical geometry has positive curvature and no parallel lines.
- **Hyperbolic geometry** has constant negative curvature and infinitely many parallels through a point not on the given line.
- The curvature is the same at every point: `K < 0`.

### 2. Models of the Hyperbolic Plane
| Model | Coordinates | Geodesics |
|-------|-------------|-----------|
| Poincaré disk | Unit disk `|z| < 1` | Circular arcs orthogonal to unit circle, diameters |
| Klein disk | Unit disk | straight chords (not angle-preserving) |
| Upper half-plane | `{z : Im(z) > 0}` | semicircles orthogonal to real axis, vertical rays |

**Metric in upper half-plane:**
`ds^2 = (dx^2 + dy^2) / y^2`  
Distance formula: `dist(z, w) = arcosh(1 + |z - w|^2 / (2 * Im(z) * Im(w)))`

### 3. Hyperbolic Group Theory
A finitely generated group `G` is **hyperbolic** (Gromov hyperbolic) if its Cayley graph is a δ-hyperbolic metric space.

**δ-hyperbolicity (thin triangles):** All geodesic triangles are δ-thin — each side is contained in the δ-neighborhood of the union of the other two sides.

**Key facts:**
- Free groups are hyperbolic (Cayley graphs are trees).
- Fundamental groups of closed hyperbolic surfaces are hyperbolic.
- Negative curvature creates exponential divergence of geodesics.

**Visual`:**
```
         A
         *
        / \
       /δ+δ\
      *-----*
     B   C
A geodesic from B to C stays within δ of the A-gap between the two other sides.
```

### 4. Gromov Hyperbolicity in General Metric Spaces
A proper geodesic metric space is hyperbolic if:
`(x, y)_z ≤ -ε * max{d(z, x), d(z, y)}` for some ε > 0  
where `(x, y)_z = 1/2 * (d(z, x) + d(z, y) - d(x, y))` is the **Gromov product**.

**Consequences:**
- Boundary at infinity is a metrizable topological space.
- Quasi-isometry invariance: hyperbolic property preserved under quasi-isometries.
- Automatic continuity, solvable conjugacy problem in many hyperbolic groups.

### 5. Poincaré Inequality
In a metric measure space `(X, d, μ)`, a Poincaré inequality holds if:
`∫_γ |f - f_y|^p dμ ≤ C * r^p * ∫_B(x, r) |∇f|^p dμ`

Interpretation: Functions cannot oscillate too fast on balls. This is the analytical heart of hyperbolic geometry — it connects geometry to PDEs and analysis.

### 6. Connections to Modern Theory
- **Metric geometry**: Hyperbolic spaces are canonical examples of "negatively curved" spaces.
- **Geometric group theory**: Mostow rigidity — quasi-isometries of closed hyperbolic manifolds are homotopic to isometries.
- **Complex dynamics**: Iterated function systems with hyperbolic behavior.
- **Machine learning**: Hyperbolic embeddings for hierarchical data — trees and scale-free networks embed with lower distortion in hyperbolic space than Euclidean.
- **Topological data analysis**: Persistent homology on hyperbolic graphs.

## Teaching Exercises

1. **Distance calculation**: Compute the hyperbolic distance between `i` and `2i` in the upper half-plane model using `arcosh`. Compare to Euclidean.
2. **Triangle angle sum**: Show that a hyperbolic right-angled pentagon has angle sum less than 3π/2, contrasting with Euclidean 3π/2.
3. **Cayley graph recognition**: For the free group on two generators, draw its Cayley graph and identify δ for which it is δ-hyperbolic.
4. **Gromov product computation**: Given a tree with root and two leaves, compute `(x, y)_root` and verify hyperbolic inequality.
5. **Monthly check**: State informally what "quasi-isometry invariance" means and why it matters for distinguishing group types.

## Verification Checklist
- [ ] Understand that `K < 0` means triangles have angle sum < π.
- [ ] Can compute hyperbolic distance in at least one model.
- [ ] Can define δ-hyperbolic space and give an example.
- [ ] Know that Mostow rigidity says a closed hyperbolic manifold's shape is determined by its fundamental group.
- [ ] Recognize Poincaré inequality as the analytic face of negative curvature.

## References for Further Study
- Bridson & Haefliger, *Metric Spaces of Non-Positive Curvature*.
- Gromov, "Hyperbolic groups" (1987).
- Navarrete & Pisante, *Introduction to Gromov Hyperbolic Spaces*.
- Recent geometric group theory surveys: Dahmani, Guirardel, Osin.

---
Last updated: 2026-06-05
