
#!/usr/bin/env python3
import json, sys
from pathlib import Path

def td(s): 
    return s.replace("|","\\|") if isinstance(s, str) else s

def render_table(rows):
    if not rows:
        return ""
    header = "| " + " | ".join(rows[0]) + " |"
    sep = "| " + " | ".join(["---"]*len(rows[0])) + " |"
    body = "\n".join("| " + " | ".join(r) + " |" for r in rows[1:])
    return "\n".join([header, sep, body])

def main():
    data_path = Path("data/resume.json")
    j = json.loads(data_path.read_text(encoding="utf-8"))

    out = []
    name = j.get("profile",{}).get("name_kr","") or ""
    name_en = j.get("profile",{}).get("name_en","") or ""
    out.append(f"# {name} ({name_en})")
    photo = j.get("profile_photo")
    if photo:
        # Keep the extension from json value, but our path is fixed to assets/profile_photo.ext
        suffix = Path(photo).suffix
        out.append(f"![](assets/profile_photo{suffix})")
    out.append("")

    prof = j.get("profile",{})
    prof_rows = [
        ["항목","내용"],
        ["이름(한글)", td(prof.get("name_kr",""))],
        ["이름(영문)", td(prof.get("name_en",""))],
        ["생년월일", td(prof.get("dob",""))],
        ["현재 직위", td(prof.get("current_position",""))],
        ["소속", td(prof.get("affiliation",""))],
        ["E-mail", td(prof.get("email",""))],
    ]
    out.append("## Profile")
    out.append(render_table(prof_rows))
    out.append("")

    ri = j.get("research_interest",[])
    if ri:
        out.append("## Research Interests")
        rows = [["관심분야"]] + [[td(x)] for x in ri]
        out.append(render_table(rows))
        out.append("")

    edu = j.get("education",[])
    if edu:
        out.append("## Education")
        rows = [["기관","학위","기간","세부"]]
        for e in edu:
            rows.append([td(e.get("institution","")), td(e.get("degree","")), td(e.get("dates","")), td("; ".join(e.get("details",[])))])
        out.append(render_table(rows))
        out.append("")

    pubs = j.get("publications",[])
    if pubs:
        out.append("## Publications")
        rows = [["구분","인용","발행일"]]
        for p in pubs:
            rows.append([td(p.get("category","") or ""), td(p.get("citation","")), td(p.get("date",""))])
        out.append(render_table(rows))
        out.append("")

    prjs = j.get("projects",[])
    if prjs:
        out.append("## Projects")
        rows = [["프로젝트","기간","주관/출연처","사업명","주요내용"]]
        for p in prjs:
            rows.append([td(p.get("title","")), td(p.get("dates","")), td(p.get("sponsor","")), td(p.get("program","")), td("; ".join(p.get("bullets",[])))])
        out.append(render_table(rows))
        out.append("")

    exps = j.get("experience",[])
    if exps:
        out.append("## Experience")
        rows = [["기관","부서/연구실","직무/직책","기간"]]
        for e in exps:
            rows.append([td(e.get("org","")), td(e.get("dept","")), td(e.get("org_role","")), td(e.get("dates",""))])
        out.append(render_table(rows))
        out.append("")

    h = j.get("honors_awards",[])
    if h:
        out.append("## Honors & Awards")
        rows = [["상훈/설명"]]+[[td(x)] for x in h]
        out.append(render_table(rows))
        out.append("")

    ip = j.get("intellectual_property",[])
    if ip:
        out.append("## Intellectual Property")
        rows = [["지식재산"]]+[[td(x)] for x in ip]
        out.append(render_table(rows))
        out.append("")

    sk = j.get("technical_strength",{})
    out.append("## Technical Strength")
    rows = [["항목","내용"]]
    if sk.get("hardware"):
        rows.append(["H/W", ", ".join(sk["hardware"])])
    if sk.get("software"):
        rows.append(["S/W", ", ".join(sk["software"])])
    if sk.get("frameworks"):
        rows.append(["Framework/Platform/API", ", ".join(sk["frameworks"])])
    if sk.get("os"):
        rows.append(["OS", ", ".join(sk["os"])])
    if sk.get("languages"):
        rows.append(["Languages", ", ".join(sk["languages"])])
    if sk.get("libraries"):
        rows.append(["Libraries", ", ".join(sk["libraries"])])
    if sk.get("other_tools"):
        rows.append(["Other tools", ", ".join(sk["other_tools"])])
    out.append(render_table(rows))
    out.append("")

    Path("README.md").write_text("\n".join(out), encoding="utf-8")
    print("README.md generated.")

if __name__ == "__main__":
    main()
