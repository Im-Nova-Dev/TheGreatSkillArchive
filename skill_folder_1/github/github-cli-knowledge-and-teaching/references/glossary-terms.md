# Git and GitHub Terms — Plain Definitions

Use this when a learner asks “what is X?” Give the short definition first, then the plain-English expansion, then one example.

## Beginner Terms

- **repository** — a project folder plus a hidden `.git` folder that stores history
- **commit** — a saved snapshot of your project at one point in time
- **branch** — a movable name for a commit; a separate timeline
- **merge** — combining two timelines into one
- **clone** — making a local copy of a remote repository
- **remote** — a URL pointing to another copy of the repo, usually on GitHub
- **origin** — the default name for the remote you cloned from
- **push** — sending your local commits to a remote
- **pull** — downloading remote commits and merging them into your current branch
- **fetch** — downloading remote commits without merging
- **diff** — the line-by-line differences between two states
- **HEAD** — the special pointer that says “where you are now”
- **working tree** — the files you actually edit on disk
- **staging area** — the temporary list of changes earmarked for the next commit
- **index** — another name for the staging area
- **.gitignore** — a file that tells Git which files to ignore
- **status** — current state of the working tree and staging area
- **PR (Pull Request)** — a request to merge one branch into another, hosted on GitHub
- **issue** — a GitHub feature for tracking work
- **fork** — a personal copy of someone else’s repository under your account
- **star** — GitHub’s “bookmark” feature for repos

## Intermediate Terms

- **reflog** — a local log of where HEAD has moved; useful for recovery
- **cherry-pick** — copy one commit onto another branch
- **rebase** — rewrite your branch so it appears to start from a different base
- **squash** — combine multiple commits into one
- **fast-forward** — when merging, simply moves the branch pointer forward because there is nothing to merge
- **merge commit** — a special commit with two parents, created by `git merge`
- **detached HEAD** — HEAD points directly to a commit instead of a branch
- **upstream** — the original repo you forked from, used to keep your fork in sync
- **downstream** — a consumer or fork of your repository
- **origin/main** — the `main` branch as it exists on the remote named `origin`
- **protection rules / branch protection** — GitHub settings that enforce review, status checks, or permissions before merging
- **auto-merge** — GitHub feature that merges automatically once checks pass
- **workflow** — a GitHub Actions YAML file describing automated steps
- **run** — one execution of a workflow
- **artifact** — a file produced by a workflow run
- **secret** — encrypted environment variable for Actions workflows
- **label** — colored tag attached to issues and PRs
- **review** — feedback on a PR before merging

## Advanced Terms

- **blob** — Git object that stores file content
- **tree** — Git object that stores directory structure and references to blobs
- **object database** — everything inside `.git/objects`; immutable content-addressed storage
- **SHA / SHA-1** — the 40-character hash that names every Git object; e.g. `abc123...`
- **DAG** — directed acyclic graph; the shape of Git history
- **reachability** — whether one commit can be reached by following parent links from HEAD
- **grafts / replace** — low-level ways to rewrite the apparent history
- **rerere** — “reuse recorded resolution”; Git remembers how you resolved a conflict
- **bisect** — binary search through history to find the commit that introduced a bug
- **bisect run** — automate `git bisect` with a script
- **filter-repo** — rewrite history by adding/removing files, paths, or messages
- **credential helper** — program Git uses to remember or cache login credentials
- **mode** — unix file permission bits stored with each tracked file, almost always `100644` or `100755`
- **worktree** — multiple working trees sharing the same `.git` directory
- **submodule** — a Git repo inside another Git repo, checked out at a specific commit
- **pre-push hook** — script that runs before `git push`
- **pre-commit hook** — script that runs before `git commit`
