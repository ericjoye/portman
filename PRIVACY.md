# Privacy Policy — portman

**Last updated:** June 20, 2026

## Overview

portman ("we", "our", "the tool") is a command-line utility that finds and kills processes on localhost ports. It helps developers manage local development servers.

## Data Collection

**portman does NOT collect, store, or transmit any data.**

When you use portman:

- **No data is logged or transmitted.** All operations happen locally on your machine. The tool does not send data to any external server.
- **No network calls.** portman does not make any network requests. It operates entirely offline.
- **No telemetry.** There is no usage tracking, analytics, or telemetry of any kind.
- **No accounts.** There is no signup, login, or user account system.

## How It Works

portman queries your operating system's network stack to list listening ports and their associated processes. It can optionally terminate processes on specified ports with your confirmation. It may read a configuration file (`~/.portmanrc`) for custom port presets and ignore lists. All operations are local — no data about your processes or ports is transmitted anywhere.

## Open Source

portman is open source under the MIT license. It uses Python 3.11+ standard library modules. The optional `psutil` dependency is used for enhanced cross-platform support.

## Changes to This Policy

We may update this privacy policy from time to time. Any changes will be reflected in the project's source code repository.

## Contact

If you have questions about this privacy policy, contact us at: [YOUR EMAIL ADDRESS]
