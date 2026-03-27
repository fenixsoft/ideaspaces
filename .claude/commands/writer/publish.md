---
name: "Writer: Publish"
description: "验收文章并发布到文档目录，归档工作文件"
category: Writer
tags: [writer, publish, article, archive]
---

Use the Skill tool to invoke writer-publish skill.

{{#if args}}
文章名称: {{args}}
{{else}}
发布当前文章。
{{/if}}