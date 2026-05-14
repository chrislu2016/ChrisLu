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
    education = [
        "- **Ph.D. in Journalism and Communication**, Tsinghua University, 2023.9 - Present. GPA: 3.95/4.0. Advisor: Min Hang.",
        "- **M.A. in Media Economics**, Communication University of China, 2020.9 - 2023.6. GPA: 3.99/4.0. Advisor: Suhui Zheng.",
        "- **B.A. in International Economics and Trade** with a second degree in French Literature, Beijing Foreign Studies University, 2016.9 - 2020.6. GPA: 3.63/4.0.",
    ]
    selected_publications = [
        "- Huang, P., & **Lu, H.** (2026). Digital feminist humor as a weapon: A humor and topic analysis of the Weibo posts of the Fat Cat event. *Feminist Media Studies*, 0(0). (SSCI, Q2)",
        "- Huang, P., **Lu, H.**, & Zhu, M. (2026). Negotiating fluidity: How China's “fourth-love” redoes gender within heteronormativity. *Sexualities*, 0(0). (SSCI, Q1)",
        "- Zhang, Z., & **Lu, H.** (2025). From human-machine competition back to human-centered collaboration: Development paths and subjectivity reflections on human-AI collaboration. *Chinese Editorials*, (09), 82-87. (CSSCI)",
        "- **Lu, H.** (2025). Marginalization and centrifugalization: Power relations in Tuwei remix culture. *Contemporary Youth Research*, (03), 34-48.",
        "- **Lu, H.** (2024). Can AI match the expertise of financial journalists in writing news commentary? An online experimental analysis based on the HSM model. *Chinese Journal of Journalism & Communication*, (10), 28-48. (CSSCI TOP)",
        "- **Lu, H.**, & Zheng, S. (2024). Causes and countermeasures of public opinion risks faced by transnational digital platforms in information geopolitics: A case study of multiple international sanctions against TikTok. *Modern Communication*, (07), 59-66. (CSSCI TOP)",
    ]
    selected_conferences = [
        "- **Lu, H.** (2026). Cognitive Offloading in the Age of Generative AI: Rethinking Critical Media Education for Combating Fake News Vulnerability. Paper presented at the IAMCR Annual Conference, Galway, Ireland.",
        "- **Lu, H.**, & Huang, P. (2026). Digital feminist humor as a weapon: A humor and topic analysis of the Weibo posts of the Fat Cat event. Oral presentation at the 76th ICA, Cape Town, South Africa.",
        "- **Lu, H.** (2025). The Role of News on the Confidence-Boosting Effect of Economic Policy Announcement: Empirical Quasi-natural Experiment Evidence of China. Oral presentation at the 111th NCA, Denver, United States.",
        "- **Lu, H.** (2025). Empowerment or Exploitation: A Network Ethnography on a Tuwei Culture Content Creators' Community in Douyin. Oral presentation at the 111th NCA, Denver, United States.",
    ]
    projects = [
        "- **The Role and Mechanisms of News in Boosting Confidence in Economic Policy Communication**, university-funded project, PI, 2024.12 - Present.",
        "- **Coordinating Economic Governance and Public Opinion Communication to Build Market Expectation Guidance Mechanisms**, university-funded project, 2024.6 - 2025.12.",
        "- **Brand Analysis of CHN Energy Wuhai Energy Group**, university-funded project, 2023.9 - 2024.6.",
        "- **Social Incentives and Mechanisms of Intimate Relationships among Chinese College Students**, company-funded project, 2023.10 - 2025.9.",
    ]
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
            "My academic work examines **policy communication, national image, financial communication, and media economics**.",
            "",
            f"You can reach me at [{profile['email']}](mailto:{profile['email']}). You can also download my [CV]({{{{ site.baseurl }}}}/ChrisLu-CV.pdf).",
            "",
            f"_Last updated: {data['updated']}._",
        ]
    )
    lines.extend(section("Education", education))
    lines.extend(section("Selected Publications", selected_publications))
    lines.extend(section("Selected Conference Presentations", selected_conferences))
    lines.extend(section("Research Projects", projects))
    lines.extend(section("Teaching", [
        "- Teaching Assistant, Journalism Economics and Basics of Accounting, Tsinghua University, 2023F/W & 2024F/W.",
        "- Teaching Assistant, Economic Journalism and Communication, Tsinghua University, 2024S/S.",
        "- Teaching Assistant, Media Economics Research, Tsinghua University, 2025S/S.",
    ]))
    lines.extend(section("Languages", [
        "- Chinese; English (TEM-8); French (TFU-4); Korean (TOPIK-5).",
    ]))
    lines.extend(section("Skills", [
        "- **Natural Language Processing**: Python (LDA, Word2Vec), Gephi.",
        "- **Social Network Analysis**: Gephi, CiteSpace, UCINET.",
        "- **Econometrics and Statistics**: Stata, SPSS, OXmetrics.",
        "- **Qualitative Research**: NVivo.",
    ]))
    return "\n".join(lines).rstrip() + "\n"


def build_cv(data: dict) -> str:
    profile = data["profile"]
    publications = [
        "- Huang, P., & **Lu, H.** (2026). Digital feminist humor as a weapon: A humor and topic analysis of the Weibo posts of the Fat Cat event. *Feminist Media Studies, 0*(0). (SSCI, Q2)",
        "- Huang, P., **Lu, H.**, & Zhu, M. (2026). Negotiating fluidity: How China's “fourth-love” redoes gender within heteronormativity. *Sexualities, 0*(0). (SSCI, Q1)",
        "- Zhang, Z., & **Lu, H.** (2025). From human-machine competition to human-centeredness: The development path of human-AI collaboration and reflections on subjectivity. *Chinese Editorials*, (9), 82-87. (in Chinese, CSSCI)",
        "- **Lu, H.** (2025). Marginalization and decentralization: Power relations in \"Tuwei\" secondary creation culture. *Contemporary Youth Research*, (3), 34-48. (in Chinese, CSSCI)",
        "- **Lu, H.** (2024). Can AI match the expertise of financial journalists in writing news commentary? An online experimental analysis based on the Heuristic-Systematic Model. *Chinese Journal of Journalism & Communication*, (10), 28-48. (in Chinese, CSSCI TOP)",
        "- Hang, M., & **Lu, H.** (2024). Exploration of the paths and mechanisms for data elements empowering the development of the publishing industry. *Chinese Editorials*, (07), 18-23. (in Chinese, CSSCI)",
        "- **Lu, H.**, & Zheng, S. (2024). Causes and countermeasures of public opinion risks faced by multinational digital platforms in information geopolitics: A case study of multiple international sanctions against TikTok. *Modern Communication*, (07), 59-66. (in Chinese, CSSCI TOP)",
        "- **Lu, H.** (2024). Research on the institutional logic of short video micro-dramas industry. *Contemporary Television*, (02), 60-66. (in Chinese, CSSCI)",
        "- Zheng, S., **Lu, H.**, & Yin, W. (2022). An exploration of the driving forces behind the shortening trend of window periods from an institutional logic perspective. *Film Art*, (03), 155-160. (in Chinese, CSSCI TOP)",
        "- Zheng, S., Xi, Z., & **Lu, H.** (2022). Branding strategies of cultural variety shows: A case study of *The Reader*. *Television Research*, (05), 80-82. (in Chinese, CSSCI)",
    ]
    conferences = [
        "- **Lu, H.** (2026). Cognitive Offloading in the Age of Generative AI: Rethinking Critical Media Education for Combating Fake News Vulnerability. Paper presented at the International Association for Media and Communication Research (IAMCR) Annual Conference, Media Education Research Section (MER), Galway, Ireland.",
        "- **Lu, H.**, & Huang, P. (2026). Digital feminist humor as a weapon: A humor and topic analysis of the Weibo posts of the Fat Cat event. Oral presentation at the 76th ICA, Feminist Scholarship Division, Cape Town, South Africa.",
        "- **Lu, H.** (2025). The Role of News on the Confidence-Boosting Effect of Economic Policy Announcement: Empirical Quasi-natural Experiment Evidence of China. Oral presentation at the 111th NCA, Political Communication Division, Denver, United States.",
        "- **Lu, H.** (2025). Empowerment or Exploitation: A Network Ethnography on a Tuwei Culture Content Creators' Community in Douyin. Oral presentation at the 111th NCA, Ethnography Division, Denver, United States.",
        "- **Lu, H.** (2025). More than mere information transmission: How news influences confidence in economic policy communication? A quasi-natural experiment based on the Central Economic Work Conference. Oral presentation at the 2025 Tsinghua University Doctoral Student Academic Forum on Journalism and Communication & Young Scholars Forum, Beijing, China. (Excellent Paper Award)",
        "- **Lu, H.**, Huang, P., & Xu, B. (2025). Research on integrated media brand building in the convergence transformation of traditional magazines and journals: The case of \"Sanlian Zhongdu.\" Oral presentation at the 2025 Academic Annual Conference of the Media Economics and Management Committee of the Chinese Association for History of Journalism and Mass Communication, Changsha, China. (Excellent Paper Award)",
        "- Huang, P., & **Lu, H.** (2024). Exploring the gender attraction perceptions of the fourth queer heterosexual group in China. Oral presentation at the 74th ICA, LGBTQ+ Panel, Gold Coast, Australia.",
        "- **Lu, H.**, Huang, P., & Xu, B. (2024). Can National Financial Literacy Better Explain the Differences in Financial Media Systems Among Countries? Oral presentation at the 2024 Annual Conference of the China Association for the History of Journalism and Mass Communication, Hangzhou, China. (in Chinese)",
    ]
    working_papers = [
        "- **Lu, H.**, & Yang, Z. (under review). Transnational digital platforms in informational geopolitics: A qualitative comparative analysis of 31 countries' motives to sanction TikTok. Journal article. (in Chinese)",
        "- Liu, C., & **Lu, H.** (under review). Informal systems for proactive disclosure: The role of Confucian culture and media monitoring on corporate ESG disclosure. Journal article. (in Chinese)",
        "- **Lu, H.** (under review). The role of news on the confidence-boosting effect of economic policy announcements: Empirical quasi-natural experiment evidence from China. Journal article. (in Chinese)",
    ]
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
            "School of Journalism and Communication, Tsinghua University, China",
            "",
            f"- Email: [{profile['email']}](mailto:{profile['email']})",
            f"- Homepage: [{profile['homepage']}]({profile['homepage']})",
            "- Languages: Chinese, English (TEM-8), French (TFU-4), Korean (TOPIK-5)",
            "- Research interests: policy communication, national image, financial communication, media economics",
            f"Last updated: {data['updated']}",
        ]
    )
    lines.extend(section("Education", [
        "- **Tsinghua University**, China, Sep. 2023 - Present. Ph.D. in Journalism and Communication | GPA: 3.95/4.0 | Supervisor: Min Hang.",
        "- **Communication University of China**, China, Sep. 2020 - Jun. 2023. Master in Media Economics | GPA: 3.99/4.0 | Supervisor: Suhui Zheng.",
        "- **Beijing Foreign Studies University**, China, Sep. 2016 - Jun. 2020. Bachelor in International Economics & Trade + French Literature | GPA: 3.63/4.0.",
    ]))
    lines.extend(section("Publications", publications))
    lines.extend(section("Conference Papers", conferences))
    lines.extend(section("Working Papers", working_papers))
    lines.extend(section("Projects", [
        "- Research on the Role and Mechanism of News in Confidence during Economic Policy Communication, University-funded Project, Dec. 2024 - Present.",
        "- Construction of a Market Expectation Guidance Mechanism by Coordinating Economic Governance and Public Opinion Propaganda, University-funded Project, Jun. 2024 - Dec. 2025.",
        "- The Analysis of the Branding Situation of Guoneng Energy Group Wuhai Energy, University-funded Project, Sep. 2023 - Jun. 2024.",
        "- Research on the Social Incentives and Mechanisms of Intimate Relationships among Chinese College Students, Company-funded Project, Oct. 2023 - Jun. 2025.",
        "- Video Empowerment in Innovative International Communication of Traditional Culture, University-funded Project, Oct. 2022 - Jun. 2024.",
        "- Short-Form Video Consumption Among Gen Z, University-funded Project, Dec. 2020 - May 2022.",
    ]))
    lines.extend(section("Work Experience", [
        "- **Tsinghua University Education Foundation**, Public Relations Department, Sep. 2023 - Jun. 2024. Maintained donor relationships, produced brand films, and updated the foundation's media channel.",
        "- **Beijing Kuaishou Technology Co., Ltd.**, Content Operations Specialist, May 2021 - Aug. 2021. Managed creators' communities, led celebrity author introductions and live broadcast projects.",
        "- **Guilin TV Station**, Video Journalist and Editor, Dec. 2019 - Feb. 2020. Reported and edited news for *Guilin News*.",
    ]))
    lines.extend(section("Teaching Experience", [
        "- Economics and Basics of Accounting for Journalist, Teaching Assistant, Tsinghua University, 2023F/W & 2024F/W.",
        "- Economic Journalism and Communication, Teaching Assistant, Tsinghua University, 2024S/S.",
    ]))
    lines.extend(section("Awards & Honors", [
        "- Bachelor: Social Work Award (2018), Outstanding Student Leader (2017/2019), Third-Class Scholarship (2019), Outstanding Graduate (2020).",
        "- Master: National Scholarship (2022), Second-Class Scholarship (2021), Merit Student (2021/2023), Outstanding Graduate (2023).",
        "- Ph.D.: National Scholarship (2025), Second-Class Scholarship (2024), Outstanding TA (2024).",
    ]))
    lines.extend(section("Skills", [
        "- **NLP**: Python (LDA, Word2Vec), Gephi (Visualization).",
        "- **QCA**: fsQCA.",
        "- **Network Analysis**: Gephi, CiteSpace, UCINET.",
        "- **Statistical Modeling**: Stata, SPSS, OXmetrics.",
        "- **Time Series Analysis**: OXmetrics, Eviews.",
        "- **Grounded Theory**: NVivo.",
        "- **Media Skills**: Audition, Final Cut Pro, InDesign.",
    ]))
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    data = load_resume()
    ABOUT_PATH.write_text(build_about(data), encoding="utf-8")
    CV_PATH.write_text(build_cv(data), encoding="utf-8")
    print(f"Generated {ABOUT_PATH.relative_to(ROOT)}")
    print(f"Generated {CV_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
