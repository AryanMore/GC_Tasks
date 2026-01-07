import re
from pathlib import Path

def parse_markdown(md_text):
    lines = md_text.split("\n")
    data = []

    current_heading = "root"
    buffer = []
    in_code = False
    lang = None

    for line in lines:

        # New heading
        if re.match(r"^#{1,3}\s", line) and not in_code:
            if buffer:
                data.append({
                    "heading": current_heading,
                    "content": "\n".join(buffer),
                    "type": "mixed",
                    "language": None
                })
                buffer = []
            current_heading = line.replace("#","").strip()
            continue

        # Code block start
        if line.strip().startswith("```"):
            if not in_code:
                in_code = True
                lang = line.replace("```","").strip()
                continue
            else:
                in_code = False
                data.append({
                    "heading": current_heading,
                    "content": "\n".join(buffer),
                    "type": "code",
                    "language": lang
                })
                buffer = []
                lang = None
                continue

        buffer.append(line)

    return data


def load_md_files(folder):
    docs = []

    for file in Path(folder).rglob("*.md"):
        with open(file, encoding="utf-8") as f:
            blocks = parse_markdown(f.read())

        for i,b in enumerate(blocks):
            if len(b["content"].split()) < 20:
                continue

            docs.append({
                "doc": file.name,
                "heading": b["heading"],
                "type": b["type"],
                "language": b["language"],
                "content": b["content"],
                "position": i
            })

    return docs
