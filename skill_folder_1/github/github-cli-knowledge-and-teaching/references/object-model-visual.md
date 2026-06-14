# Git Object Model — Visual Explanation

Use this when a learner wants to know “what is Git actually storing?”

## The Objects

1. blob — file content only, no filename
2. tree — directory listing: filenames, modes, and blob/tree hashes
3. commit — snapshot: one tree + parent commit(s) + message + metadata
4. tag — named pointer to a commit

## Mapping

- commit -> tree (root)
- tree -> blobs and other trees
- blobs -> file contents

## One-File Example

File `hello.txt` contains `Hello!`.

Steps:
1. `git hash-object -t blob -w --stdin <<<'Hello!'` gives a blob SHA.
2. A tree object maps `.` -> `hello.txt` -> blob SHA.
3. A commit object points to that tree.

This is why Git says “snapshots,” not diffs. Diffs are calculated later.

## Teaching Hook

“Git is a content-addressed filesystem on top of a commit graph.”
