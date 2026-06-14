# Workshop FAQ Deep Dive

## Logistics

**Q: What if a learner doesn’t have Bash / Zsh?**
Use the session-zero setup script. If that fails, use the embedded Docker container or Git Bash on Windows.

**Q: Wi-Fi goes down mid-lesson?**
Fall back to offline scenario: clone a local bundle, then merge as if remote existed.

**Q: Learners are mixed Windows / Mac / Linux?**
Focus on POSIX-compatible commands. Avoid advanced shell features like process substitution.

---

## Content

**Q: “Why not teach GitHub Desktop first?”**
A: Terminal-first demos transfer to anywhere — CI scripts, Dockerfiles, servers. GUI comes later as optional efficiency.

**Q: “Why split Git from GitHub in teaching order?”**
A: Git is the local tool you control. GitHub is the collaboration layer. Understanding local first prevents “magic” confusion.

**Q: “What if they already know some Git?”**
Give a readiness test. Fast path: skip sessions 1-3, take advanced exercises immediately.
