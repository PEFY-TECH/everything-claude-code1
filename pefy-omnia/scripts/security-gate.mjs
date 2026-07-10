#!/usr/bin/env node

let raw = "";
for await (const chunk of process.stdin) raw += chunk;

function deny(reason) {
  process.stdout.write(JSON.stringify({
    hookSpecificOutput: {
      hookEventName: "PreToolUse",
      permissionDecision: "deny",
      permissionDecisionReason: reason
    }
  }));
}

function failOpen(message) {
  process.stderr.write(`[PEFY OMNIA security gate] ${message}\n`);
  process.exit(0);
}

let input;
try {
  input = JSON.parse(raw || "{}");
} catch {
  failOpen("Invalid hook input; no decision returned.");
}

const toolName = input.tool_name || "";
const toolInput = input.tool_input || {};

if (toolName === "Bash") {
  const command = String(toolInput.command || "");
  const normalized = command.replace(/\s+/g, " ").trim();

  const destructivePatterns = [
    { pattern: /(?:^|[;&|])\s*(?:sudo\s+)?rm\s+-[^\n]*r[^\n]*f[^\n]*\s+(?:--\s+)?(?:\/|~|\$HOME)(?:\s|$)/i, reason: "Destructive recursive deletion of a root or home path is blocked." },
    { pattern: /\bmkfs(?:\.[a-z0-9]+)?\b/i, reason: "Filesystem formatting commands are blocked." },
    { pattern: /\bdd\b[^\n]*\bof=\/dev\//i, reason: "Raw disk writes are blocked." },
    { pattern: /\bchmod\s+-R\s+777\s+\/(?:\s|$)/i, reason: "Recursive world-writable permissions on root are blocked." },
    { pattern: /\bchown\s+-R\b[^\n]*\s+\/(?:\s|$)/i, reason: "Recursive ownership changes on root are blocked." },
    { pattern: /:\s*\(\s*\)\s*\{\s*:\s*\|\s*:\s*&\s*\}\s*;\s*:/, reason: "Fork-bomb execution is blocked." },
    { pattern: /\b(?:shutdown|reboot|halt|poweroff)\b/i, reason: "Host shutdown and reboot commands require explicit operator execution." },
    { pattern: /\b(?:diskpart\s+\/s|clear-disk|format-volume)\b/i, reason: "Destructive disk-management commands are blocked." }
  ];

  for (const rule of destructivePatterns) {
    if (rule.pattern.test(normalized)) {
      deny(rule.reason);
      process.exit(0);
    }
  }

  const remoteExecution = /\b(?:curl|wget|invoke-webrequest|iwr)\b[^|\n]*\|\s*(?:sudo\s+)?(?:sh|bash|zsh|fish|pwsh|powershell)\b/i;
  if (remoteExecution.test(normalized)) {
    deny("Opaque download-and-execute pipelines are blocked. Download, inspect, verify, then execute explicitly.");
    process.exit(0);
  }

  const forcePush = /\bgit\s+push\b[^\n]*\s--force(?:\s|$)/i;
  if (forcePush.test(normalized) && !/--force-with-lease\b/i.test(normalized)) {
    deny("Uncontrolled git force-push is blocked. Use --force-with-lease only after reviewing the target branch and impact.");
    process.exit(0);
  }

  process.exit(0);
}

if (toolName === "Write" || toolName === "Edit") {
  const filePath = String(toolInput.file_path || "");
  const proposed = [toolInput.content, toolInput.new_string].filter(Boolean).join("\n");

  const isExample = /(?:\.example|\.sample|\.template|examples?\/)/i.test(filePath) ||
    /\b(?:YOUR_|EXAMPLE|PLACEHOLDER|REDACTED|CHANGE_ME)\b/i.test(proposed);

  if (!isExample && proposed) {
    const secretPatterns = [
      { pattern: /-----BEGIN (?:RSA |OPENSSH |EC |DSA )?PRIVATE KEY-----/, reason: "A private key appears in the proposed file content." },
      { pattern: /\bgh[pousr]_[A-Za-z0-9]{30,}\b/, reason: "A GitHub token appears in the proposed file content." },
      { pattern: /\bsk-[A-Za-z0-9_-]{20,}\b/, reason: "An API secret key appears in the proposed file content." },
      { pattern: /\bAKIA[0-9A-Z]{16}\b/, reason: "An AWS access key ID appears in the proposed file content." },
      { pattern: /\bxox[baprs]-[A-Za-z0-9-]{20,}\b/, reason: "A Slack token appears in the proposed file content." },
      { pattern: /(?:password|passwd|secret|api[_-]?key|access[_-]?token)\s*[:=]\s*["'][^"'\n]{12,}["']/i, reason: "A likely literal credential appears in the proposed file content." }
    ];

    for (const rule of secretPatterns) {
      if (rule.pattern.test(proposed)) {
        deny(`${rule.reason} Use an environment-variable reference or a secret manager instead.`);
        process.exit(0);
      }
    }
  }
}

process.exit(0);
