#!/usr/bin/env python3
"""Generate homepage and CV pages from the structured resume file."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESUME_PATH = ROOT / "resume" / "resume.json"
ABOUT_PATH = ROOT / "_pages" / "about.md"
CV_PATH = ROOT / "_pages" / "cv.md"


def load_resume() -> dict:
    with RESUME_PATH.open(encoding="utf-8") as file:
        return json.load(file)


def bullet(text: str) -> str:
    return f"- {text}"


def section(title: str, lines: list[str]) -> list[str]:
    return ["", title, "=" * len(title), "", *lines]


def education_lines(items: list[dict]) -> list[str]:
    lines = []
    for item in items:
        line = (
            f"- **{item['institution']}**，{item['location']}，{item['period']}  "
            f"{item['degree']} | {item['details']}"
        )
        lines.append(line)
    return lines


def project_lines(items: list[dict]) -> list[str]:
    return [
        f"- **{item['title']}**，{item['type']}，{item['period']}"
        for item in items
    ]


def experience_lines(items: list[dict]) -> list[str]:
    lines = []
    for item in items:
        lines.append(
            f"- **{item['organization']}**，{item['role']}，{item['period']}  "
            f"{item['description']}"
        )
    return lines


def skill_lines(items: list[dict]) -> list[str]:
    return [f"- **{item['category']}**：{item['items']}" for item in items]


def front_matter(title: str, permalink: str, extra: list[str] | None = None) -> list[str]:
    lines = [
        "---",
        f'title: "{title}"',
        f"permalink: {permalink}",
        "author_profile: true",
    ]
    if extra:
        lines.extend(extra)
    lines.append("---")
    return lines


def build_about(data: dict) -> str:
    profile = data["profile"]
    lines = front_matter(
        "About me",
        "/",
        [
            "redirect_from:",
            "  - /about/",
            "  - /about.html",
        ],
    )
    lines.extend(
        [
            "",
            "<!-- This page is generated from resume/resume.json by scripts/generate_site.py. -->",
            "",
            f"Hello, I'm **{profile['name_en']} ({profile['preferred_name']}) / {profile['name_cn']}**, currently pursuing my Ph.D. in the School of Journalism and Communication at **Tsinghua University**.",
            "",
            "My research focuses on **economic communication, national image, gender studies, digital culture, and media industries**.",
            "",
            f"You can reach me at [{profile['email']}](mailto:{profile['email']}). You can also download my [CV]({{{{ site.baseurl }}}}/ChrisLu-CV.pdf).",
            "",
            f"_Last updated: {data['updated']}._",
        ]
    )
    lines.extend(section("Education", education_lines(data["education"])))
    lines.extend(section("Selected Publications", [bullet(item) for item in data["publications"][:6]]))
    lines.extend(section("Selected Conference Presentations", [bullet(item) for item in data["conferences"][:4]]))
    lines.extend(section("Research Projects", project_lines(data["projects"][:4])))
    lines.extend(section("Teaching", [bullet(item) for item in data["teaching"]]))
    lines.extend(section("Skills", skill_lines(data["skills"])))
    return "\n".join(lines).rstrip() + "\n"


def build_cv(data: dict) -> str:
    profile = data["profile"]
    lines = front_matter(
        "CV",
        "/cv/",
        [
            "layout: archive",
            "redirect_from:",
            "  - /resume",
        ],
    )
    lines.extend(
        [
            "",
            "<!-- This page is generated from resume/resume.json by scripts/generate_site.py. -->",
            "",
            f"# {profile['name_cn']} {profile['name_en']}",
            "",
            profile["affiliation"],
            "",
            f"- Email: [{profile['email']}](mailto:{profile['email']})",
            f"- Homepage: [{profile['homepage']}]({profile['homepage']})",
            f"- Languages: {'、'.join(profile['languages'])}",
            f"- Research interests: {'、'.join(profile['research_interests'])}",
            f"Last updated: {data['updated']}",
        ]
    )
    lines.extend(section("Education", education_lines(data["education"])))
    lines.extend(section("Publications", [bullet(item) for item in data["publications"]]))
    lines.extend(section("Conference Presentations", [bullet(item) for item in data["conferences"]]))
    lines.extend(section("Works in Progress", [bullet(item) for item in data["works_in_progress"]]))
    lines.extend(section("Research Projects", project_lines(data["projects"])))
    lines.extend(section("Professional Experience", experience_lines(data["experience"])))
    lines.extend(section("Teaching", [bullet(item) for item in data["teaching"]]))
    lines.extend(section("Honors", [bullet(item) for item in data["honors"]]))
    lines.extend(section("Skills", skill_lines(data["skills"])))
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    data = load_resume()
    ABOUT_PATH.write_text(build_about(data), encoding="utf-8")
    CV_PATH.write_text(build_cv(data), encoding="utf-8")
    print(f"Generated {ABOUT_PATH.relative_to(ROOT)}")
    print(f"Generated {CV_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
