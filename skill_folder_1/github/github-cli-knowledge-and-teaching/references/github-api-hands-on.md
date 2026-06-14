# GitHub API Hands-On Mini Module

## Prerequisites
- `gh auth login` completed
- Understanding of REST basics

## Explore with gh
```
gh api repos/{owner}/{repo} --jq .full_name
gh api repos/{owner}/{repo}/issues --jq '.[].title'
gh api repos/{owner}/{repo}/pulls --jq '.[].title'
```

## Exercises
1. List your last 5 issues and their states.
2. Print the title and URL of the latest PR you opened.
3. Use `gh api` to list Actions runs and their statuses.
4. Create a repo via API: `gh api repos --method POST -f name=my-new-repo`

## Discussion
- Why use API vs CLI?
- Where do tokens fit in?
- When should you avoid API access?
