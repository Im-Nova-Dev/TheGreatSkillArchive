# Teaching Q&A Examples — Git and GitHub in the Terminal

Use these when a beginner asks a question. The pattern is: short truth, analogy, tiny demonstration.

---

Q: "Do I need to be online to use Git?"

A: No. Git is local-first. You only need the internet for `git push`, `git pull`, and `gh` commands. Commit, diff, branch, and log all work offline.

Demo:
```bash
cd /tmp && mkdir offline-demo && cd offline-demo
git init
echo hi > file.txt
git add file.txt
git commit -m "first"
git log --oneline
```

---

Q: "Is a branch a copy of all my files?"

A: No. A branch is just a label pointing to one commit. Git reuses file contents efficiently; it does not duplicate everything per branch.

Demo:
```bash
git branch -v
```

---

Q: "What if I forget to `git add` before committing?"

A: The commit will only include files that were already staged or tracked. New files must be staged first. Use `git add -p` to stage only parts of a file if you want precision.

---

Q: "Can I undo a commit?"

A: Yes. Two safe routes:

- Amend the last commit: `git commit --amend`
- Revert: `git revert <sha>`
- Nuke last commit but keep changes: `git reset --soft HEAD~1`

Teach revert first for shared history, amend for private history.

---

Q: "What is the difference between `git pull` and `git fetch`?"

A:
- `git fetch` = download remote changes, but do not apply them.
- `git pull` = fetch + merge (or rebase).

For beginners, prefer pull for simplicity, then teach fetch once they understand merge.

---

Q: "Why is there a staging area at all?"

A: It lets you create a commit from only part of your current work. Without it, every commit would include all changes in the working tree.

Demo:
```bash
git add -p
```

---

Q: "What is the `.git` folder?"

A: The entire repository is stored inside `.git`. If you delete it, you delete the repo, but you keep the files on disk.

Demo:
```bash
ls .git
```

---

Q: "When should I use `rebase`?"

A: Not until they know merge well. Teach it as “rewriting your branch to look like it started from the latest main.” Safe default: use `rebase` only on private branches.

---

Q: "What does `HEAD~1` mean?"

A: “One commit before HEAD.” `HEAD~2` is two commits before HEAD. Use `git log --oneline -n 5` to see where you are before using it.

---

Q: "Why do PRs need reviews?"

A: Reviews are a GitHub feature for quality and learning. They let another person read the diff before merging, catch bugs, and suggest cleaner code. `git` itself does not enforce reviews; `gh` enables them on GitHub.

---

Q: "What if my PR is behind main?"

A: Update your branch:

```bash
git fetch origin
git merge origin/main
git push
```

Or with rebase:

```bash
git fetch origin
git rebase origin/main
git push --force-with-lease
```

Teach merge first, then rebase.
