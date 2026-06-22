# LAUNCH-PLAN: portman v0.1.0

## Product Summary
Portman is a zero-dependency Python CLI tool that finds and kills processes on localhost ports. Published to PyPI as `portman`. MIT licensed. Python 3.11+ only.

## Launch Channels

### Primary (Day 0)
1. **PyPI** — `pip install portman` (the main distribution channel)
2. **GitHub** — Public repo with README, MIT license, tagged release
3. **Product Hunt** — Launch day submission for developer tools category

### Secondary (Day 1-3)
4. **Hacker News** — Show HN post
5. **Reddit** — r/Python, r/webdev, r/programming
6. **Twitter/X** — Thread explaining the problem + solution
7. **Dev.to** — Short blog post: "Stop fighting stuck ports"
8. **LinkedIn** — Developer-focused post

### Tertiary (Day 4-7)
9. **Python Discord / Slack communities** — Share in #python, #devtools channels
10. **Indie Hackers** — Showcase post with download stats

## First Week Plan

### Day 0 — Launch Day
- [ ] Publish to PyPI (`twine upload dist/*`)
- [ ] Create GitHub release (v0.1.0) with changelog
- [ ] Submit to Product Hunt
- [ ] Post on Twitter/X
- [ ] Post on Dev.to

### Day 1 — Community Push
- [ ] Show HN on Hacker News
- [ ] Reddit posts (r/Python, r/webdev)
- [ ] LinkedIn post

### Day 2-3 — Engagement
- [ ] Respond to all comments/questions
- [ ] Share in Python Discord/Slack communities
- [ ] Indie Hackers post

### Day 4-7 — Follow-up
- [ ] Write "What I learned" post if traction
- [ ] Collect feedback, file GitHub issues for feature requests
- [ ] Monitor PyPI download stats

## Human Actions Required (EXACT List)

The following actions CANNOT be performed by agents. A human must do each one:

### PyPI Publishing
1. **Create PyPI account** at https://pypi.org/account/register/ (if not already done)
2. **Create PyPI API token** at https://pypi.org/manage/account/token/ — scope: "Entire account"
3. **Store token** in `~/.pypirc` or as `TWINE_PASSWORD` env var
4. **Run publish command**: `cd ~/businesses/portman && python -m twine upload dist/*`
5. **Verify** at https://pypi.org/project/portman/

### GitHub Release
6. **Push code** to GitHub repo: `git remote add origin <repo-url> && git push -u origin main`
7. **Create GitHub release** at https://github.com/<user>/portman/releases/new — tag: `v0.1.0`, title: "portman v0.1.0 — Initial release"
8. **Upload wheel** from `dist/` to the release assets

### Product Hunt Submission
9. **Create Product Hunt account** at https://www.producthunt.com/
10. **Submit product** at https://www.producthunt.com/posts/new — name: "Portman", tagline: "Kill stuck ports in one command", link: PyPI URL
11. **Set launch time** for 12:01 AM PST on launch day

### Social Posts
12. **Twitter/X** — Post thread (draft in `launch/social/twitter-thread.md`)
13. **Dev.to** — Create account at dev.to, publish article (draft in `launch/social/devto-article.md`)
14. **Hacker News** — Submit "Show HN" at https://news.ycombinator.com/submit
15. **Reddit** — Post to r/Python, r/webdev (draft in `launch/social/reddit-post.md`)

### Domain (Optional)
16. **Register domain** `portman.dev` or `portman-cli.com` (optional, for landing page)
17. **Deploy landing page** to GitHub Pages or Vercel (optional)

## Success Metrics
- PyPI downloads: 100+ in first week
- GitHub stars: 50+ in first week
- Product Hunt upvotes: 20+ in first day
- Zero critical bugs reported

## Risks
- **Low awareness**: CLI tools are hard to market. Mitigation: focus on pain-point messaging ("stuck port" is universally understood).
- **Competition**: `kill-port`, `fkill`, similar tools exist. Mitigation: emphasize zero-dependency + Python-native angle.
- **Platform risk**: PyPI account required. Mitigation: use API token, not password.
