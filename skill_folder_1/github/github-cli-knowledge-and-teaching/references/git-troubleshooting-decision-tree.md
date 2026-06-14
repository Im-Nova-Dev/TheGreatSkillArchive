# Git Troubleshooting Decision Tree

``` 
Problem
 ├─ Push rejected
 │   ├─ Non-fast-forward? → git pull --rebase → resolve → push
 │   └─ Protected branch? → open PR instead
 ├─ Merge conflict
 │   ├─ Binary file? → choose version manually
 │   └─ Text file? → resolve markers → add → commit
 ├─ Detached HEAD
 │   └─ Need to save work? → git switch -c new-branch
 ├─ Lost commits
 │   └─ Found? → git reflog → git checkout <sha>
 └─ Bad rebase
     └─ Abort? → git rebase --abort
```
