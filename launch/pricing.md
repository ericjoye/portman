# Portman — Pricing

## Model: Free + Open Source (MIT)

Portman is free and open source. The core CLI tool will always be free.

## Rationale

- **Developer CLI tools thrive on adoption, not lock-in.** The goal is to get portman into as many `pip install` workflows as possible.
- **Low friction = high growth.** No signup, no license key, no paywall. Just `pip install portman`.
- **Upsell path (future):** A "Portman Pro" GUI app (Electron/Tauri) with a visual port dashboard, one-click kill, and port monitoring — priced at $9.99 one-time or $1.99/mo. This is a future consideration, not part of the v1.0 launch.

## v1.0 Launch Pricing

| Tier | Price | What's included |
|------|-------|-----------------|
| **portman CLI** (PyPI) | Free | Full CLI: list, find, kill, free commands |
| **Portman Pro GUI** (future) | $9.99 one-time | Visual dashboard, port monitoring, one-click actions |

## Recommendation

Launch as free. Measure adoption via PyPI download stats. Revisit Pro tier after 1,000+ downloads.
