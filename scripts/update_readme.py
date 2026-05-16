"""Refresh the StrawHat-Enterprise org profile README.

Regions controlled by HTML-comment markers:
    <!-- ABOUT:START -->       AI-refreshed prose
    <!-- PROJECTS:START -->    Deterministic tables from the GitHub API
    <!-- HIGHLIGHTS:START -->  AI-generated "recent activity" summary
    <!-- UPDATED:START -->     Timestamp

Inputs (env):
    GITHUB_TOKEN  -- must have `repo` (or `public_repo`) + `models: read`
    GITHUB_ORG    -- defaults to StrawHat-Enterprise
    MODEL         -- defaults to openai/gpt-4o-mini (GitHub Models catalog)
    README_PATH   -- defaults to profile/README.md
"""

from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone

ORG = os.environ.get("GITHUB_ORG", "StrawHat-Enterprise")
TOKEN = os.environ["GITHUB_TOKEN"]
MODEL = os.environ.get("MODEL", "openai/gpt-4o-mini")
README_PATH = os.environ.get("README_PATH", "profile/README.md")

GH_API = "https://api.github.com"
MODELS_API = "https://models.github.ai/inference/chat/completions"

# Map repo name -> category for the Featured Projects section.
# Anything not listed is bucketed under "Other".
CATEGORIES: dict[str, str] = {
    "actions-runner-helm": "Self-Hosted Runner Platform",
    "actions-runner-gitops": "Self-Hosted Runner Platform",
    "Azure-Catalog": "Infrastructure as Code",
    "InfraCreator": "Infrastructure as Code",
    "backstage-app": "Developer Platform (Backstage)",
    "Backstage-helm": "Developer Platform (Backstage)",
    "cert-automation": "Automation",
}
CATEGORY_ORDER = [
    "Self-Hosted Runner Platform",
    "Infrastructure as Code",
    "Developer Platform (Backstage)",
    "Automation",
    "Other",
]


def http_json(url: str, *, method: str = "GET", body: dict | None = None,
              extra_headers: dict | None = None) -> dict | list:
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "strawhat-profile-bot",
    }
    if extra_headers:
        headers.update(extra_headers)
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code} on {url}: {e.read().decode()[:500]}", file=sys.stderr)
        raise


def list_public_repos() -> list[dict]:
    repos: list[dict] = []
    page = 1
    while True:
        chunk = http_json(
            f"{GH_API}/orgs/{ORG}/repos?type=public&per_page=100&page={page}&sort=updated"
        )
        if not isinstance(chunk, list) or not chunk:
            break
        repos.extend(chunk)
        if len(chunk) < 100:
            break
        page += 1
    return [r for r in repos if not r.get("archived") and r["name"] != ".github"]


def recent_commits(repo: str, since_iso: str) -> list[dict]:
    try:
        data = http_json(
            f"{GH_API}/repos/{ORG}/{repo}/commits?since={since_iso}&per_page=20"
        )
    except urllib.error.HTTPError:
        return []
    return data if isinstance(data, list) else []


def render_projects(repos: list[dict]) -> str:
    grouped: dict[str, list[dict]] = {c: [] for c in CATEGORY_ORDER}
    for r in repos:
        cat = CATEGORIES.get(r["name"], "Other")
        grouped.setdefault(cat, []).append(r)

    lines: list[str] = []
    for cat in CATEGORY_ORDER:
        items = grouped.get(cat) or []
        if not items:
            continue
        lines.append(f"### {cat}\n")
        lines.append("| Repository | Description | Language |")
        lines.append("| --- | --- | --- |")
        for r in sorted(items, key=lambda x: x["name"].lower()):
            desc = (r.get("description") or "_No description provided._").replace("|", "\\|")
            lang = r.get("language") or "—"
            lines.append(
                f"| [`{r['name']}`]({r['html_url']}) | {desc} | {lang} |"
            )
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def llm(system: str, user: str) -> str:
    body = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "temperature": 0.4,
    }
    data = http_json(
        MODELS_API,
        method="POST",
        body=body,
        extra_headers={
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
        },
    )
    return data["choices"][0]["message"]["content"].strip()


def refresh_about(repos: list[dict]) -> str:
    summary = "\n".join(
        f"- {r['name']}: {r.get('description') or 'no description'} "
        f"(lang={r.get('language') or 'n/a'})"
        for r in repos[:20]
    )
    system = (
        "You write concise, professional GitHub organization profile copy. "
        "Output Markdown only. No headings. 4–6 short lines: one intro sentence, "
        "then a tight bullet list of focus areas. Avoid hype words like "
        "'cutting-edge', 'revolutionary', emojis, or first-person."
    )
    user = (
        f"Organization: {ORG}\n"
        "Theme: Cloud platform engineering on Microsoft Azure & Kubernetes, "
        "Infrastructure-as-Code, GitHub Actions self-hosted runners, and "
        "Backstage-based developer platform.\n\n"
        "Current public repos:\n"
        f"{summary}\n\n"
        "Rewrite the 'About' section. Keep it grounded in the repos above."
    )
    return llm(system, user)


def refresh_highlights(repos: list[dict]) -> str:
    since = datetime.now(timezone.utc).replace(microsecond=0)
    since = since.replace(day=max(1, since.day - 7)) if since.day > 7 else since.replace(day=1)
    since_iso = since.isoformat().replace("+00:00", "Z")

    activity: list[str] = []
    for r in repos[:10]:
        commits = recent_commits(r["name"], since_iso)
        if not commits:
            continue
        msgs = [c["commit"]["message"].splitlines()[0][:120] for c in commits[:5]]
        activity.append(f"### {r['name']}\n" + "\n".join(f"- {m}" for m in msgs))

    if not activity:
        return "_No notable activity in the last week._"

    system = (
        "Summarize recent open-source activity for an org profile README. "
        "Output Markdown only. 3–5 short bullets, each one sentence, naming the "
        "repository in backticks. Focus on user-visible themes (features, fixes, "
        "infra changes). No emojis, no headings, no closing remarks."
    )
    user = "Recent commits per repo:\n\n" + "\n\n".join(activity)
    return llm(system, user)


def replace_region(text: str, name: str, new_inner: str) -> str:
    pattern = re.compile(
        rf"(<!--\s*{re.escape(name)}:START\s*-->)(.*?)(<!--\s*{re.escape(name)}:END\s*-->)",
        re.DOTALL,
    )
    if not pattern.search(text):
        raise RuntimeError(f"Marker {name} not found in README")
    return pattern.sub(lambda m: f"{m.group(1)}\n{new_inner.strip()}\n{m.group(3)}", text)


def main() -> int:
    with open(README_PATH, encoding="utf-8") as f:
        readme = f.read()

    repos = list_public_repos()
    print(f"Found {len(repos)} public repos.", file=sys.stderr)

    readme = replace_region(readme, "PROJECTS", render_projects(repos))
    readme = replace_region(readme, "ABOUT", refresh_about(repos))
    readme = replace_region(readme, "HIGHLIGHTS", refresh_highlights(repos))
    stamp = datetime.now(timezone.utc).strftime("Last refreshed %Y-%m-%d %H:%M UTC.")
    readme = replace_region(readme, "UPDATED", stamp)

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(readme)
    print("README updated.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
