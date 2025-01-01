# Unictl

AI-powered unified control for your systems

Unictl is a **unified control plane CLI** designed to simplify and enhance developer operations by providing a consistent interface to manage diverse systems. With extensibility and a pluggable architecture, Unictl enables seamless integration with tools like Elasticsearch, Kubernetes, and more, tailored for operations, maintenance, and troubleshooting.

## Example

```
unictl on  main [!?] via 🐍 v3.12.8
❯ unictl
╭─────────────────────────────────────────────────────╮
│ Unictl: AI-powered unified control for your systems │
╰─────────────────────────────────────────────────────╯

unictl>: /help
╭──────────────────────── Help ────────────────────────╮
│                                                      │
│     Available commands:                              │
│     /activate <plugin>  - Activate a specific plugin │
│     /list               - List all available plugins │
│     /help               - Show this help message     │
│     exit                - Exit the program           │
│                                                      │
╰──────────────────────────────────────────────────────╯

unictl>: /list
┌───────────────┬─────────────────────────────────────────────┐
│ elasticsearch │ Manage and query Elasticsearch clusters     │
│ kubernetes    │ Orchestrate and manage Kubernetes resources │
│ docker        │ Build, run, and manage Docker containers    │
│ aws           │ Control and monitor AWS cloud services      │
└───────────────┴─────────────────────────────────────────────┘

unictl>: /activate elasticsearch
Activated plugin: elasticsearch

unictl:elasticsearch>: Whats cluster status?
Processing:
This is a placeholder response.
```