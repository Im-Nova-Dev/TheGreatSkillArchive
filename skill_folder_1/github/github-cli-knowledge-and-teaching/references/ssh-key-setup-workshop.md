# SSH Key Setup Workshop

## Why
SSH keys let Git push without typing passwords every time.

## Steps
1. Generate key: `ssh-keygen -t ed25519 -C "you@example.com"`
2. Start agent: `eval "$(ssh-agent -s)"`
3. Add key: `ssh-add ~/.ssh/id_ed25519`
4. Copy public key: `cat ~/.ssh/id_ed25519.pub`
5. Add to GitHub: Settings → SSH and GPG keys
6. Test: `ssh -T git@github.com`

## Troubleshooting
- Permission denied: check key added to agent
- Still asks for password: confirm using SSH repo URL
