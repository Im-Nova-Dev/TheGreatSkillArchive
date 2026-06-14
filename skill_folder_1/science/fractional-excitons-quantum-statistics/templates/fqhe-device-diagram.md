# FQHE Device Diagram Template (LaTeX/TikZ)

Copy and modify for presentations/papers.

```latex
\documentclass[tikz,border=5pt]{standalone}
\usepackage{tikz}
\usetikzlibrary{positioning,patterns,calc}

\begin{document}
\begin{tikzpicture}[
  layer/.style={draw, thick, minimum width=6cm, minimum height=0.6cm},
  label/.style={font=\small, text width=3.5cm, align=center},
  arrow/.style={->, thick, >=stealth}
]

% Layer stack (bottom to top)
% Coordinates: y position for each layer center
\def\yb{0}   % substrate
\def\ybn{1}  % bottom hBN
\def\ybg{2}  % bottom graphene
\def\yhm{3}  % middle hBN (tunnel barrier)
\def\ytg{4}  % top graphene
\def\ytn{5}  % top hBN
\def\ytgate{6} % top gate

% Substrate
\node[layer, pattern=north east lines, pattern color=gray!30] at (0,\yb) {};
\node[label, left] at (-3.5,\yb) {SiO$__2$/Si substrate};

% Back gate (graphite)
\node[layer, fill=gray!20] at (0,\yb+0.5) {};
\node[label, left] at (-3.5,\yb+0.5) {Graphite back gate};

% Bottom hBN
\node[layer, pattern=dots, pattern color=blue!30] at (0,\ybn) {};
\node[label, left] at (-3.5,\ybn) {hBN $\sim$20~nm};

% Bottom graphene (electron layer)
\node[layer, fill=black!10] at (0,\ybg) {};
\node[label, left] at (-3.5,\ybg) {Monolayer graphene\\$\nu_e$ (electrons)};

% Middle hBN (tunnel barrier)
\node[layer, pattern=dots, pattern color=red!30] at (0,\yhm) {};
\node[label, left] at (-3.5,\yhm) {hBN $\sim$5~nm\\tunnel barrier};

% Top graphene (hole layer)
\node[layer, fill=black!10] at (0,\ytg) {};
\node[label, left] at (-3.5,\ytg) {Monolayer graphene\\$\nu_h$ (holes)};

% Top hBN
\node[layer, pattern=dots, pattern color=blue!30] at (0,\ytn) {};
\node[label, left] at (-3.5,\ytn) {hBN $\sim$20~nm};

% Top gate (graphite)
\node[layer, fill=gray!20] at (0,\ytgate) {};
\node[label, left] at (-3.5,\ytgate) {Graphite top gate};

% Magnetic field arrow
\draw[arrow, blue, thick] (4,\ytgate+0.8) -- (4,\yb-0.8)
  node[midway, right] {\large $\mathbf{B} \perp$ plane};

% Dual-gate control labels
\draw[arrow, red] (4.5,\ybg) -- (6,\ybg) node[right] {$\nu_e$ via $V_{bg}$};
\draw[arrow, red] (4.5,\ytg) -- (6,\ytg) node[right] {$\nu_h$ via $V_{tg}$};

% Displacement field
\draw[arrow, purple] (6.5, \yhm) -- (8, \yhm) node[right] {$\mathbf{D}$ field\\tunes exciton energy};

% PL excitation/collection
\draw[arrow, orange, dashed] (-5,\ytgate+1) -- (-5,\ybg)
  node[midway, left] {PL laser / collection};

% Contact leads
\draw[thick] (-4,\ybg) -- (-5,\ybg) node[left] {Source};
\draw[thick] ( 4,\ybg) -- ( 5,\ybg) node[right] {Drain};

% Legend
\begin{scope}[shift={(-3.5,-1.5)}]
  \node[label] {Legend:};
  \draw[fill=black!10] (1.5,-0.3) rectangle (2.0,0.0) node[right=0.2] {Graphene};
  \draw[pattern=dots, pattern color=blue!30] (1.5,-0.8) rectangle (2.0,-0.5) node[right=0.2] {hBN dielectric};
  \draw[pattern=dots, pattern color=red!30] (1.5,-1.3) rectangle (2.0,-1.0) node[right=0.2] {hBN tunnel barrier};
  \draw[fill=gray!20] (1.5,-1.8) rectangle (2.0,-1.5) node[right=0.2] {Graphite gate};
\end{scope}

\end{tikzpicture}
\end{document}
```

---

## Simplified ASCII Version (for quick docs)

```
┌──────────────────────────────────────────────┐
│  Top gate (Graphite)                         │
│  ────────────────────────────────────────   │
│  hBN ~20 nm (top dielectric)                 │
│  ────────────────────────────────────────   │
│  Monolayer graphene  ← ν_h (holes)          │
│  ────────────────────────────────────────   │
│  hBN ~5 nm  ← TUNNEL BARRIER                │
│  ────────────────────────────────────────   │
│  Monolayer graphene  ← ν_e (electrons)      │
│  ────────────────────────────────────────   │
│  hBN ~20 nm (bottom dielectric)             │
│  ────────────────────────────────────────   │
│  Back gate (Graphite)                        │
└──────────────────────────────────────────────┘
         ↑              ↑
      B-field      D-field
   (perpendicular) (displacement)
```

Key parameters to annotate:
- B > 20 T, T < 100 mK
- Mobility > 500,000 cm²/Vs
- Dual-gate independent control of ν_e, ν_h
- PL excitation/collection through top window