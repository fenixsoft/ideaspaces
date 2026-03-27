---
name: "Writer: Compose"
description: "执行文章写作任务，启动 Agent Team 完成写作和校审"
category: Writer
tags: [writer, compose, article, agent-teams]
---

Use the Skill tool to invoke writer-compose skill.

**重要**: 需要启用 Agent Teams 功能。在 settings.json 中设置：
```json
{ "env": { "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1" } }
```

{{#if args}}
文章名称: {{args}}
{{else}}
执行当前文章的写作任务。
{{/if}}