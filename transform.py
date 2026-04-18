import re

file_path = r'C:\Users\ajgup\Downloads\HTMLs\python-introduction.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1) UPDATE NAV: reorder to NumPy -> Mini Project -> OOP -> Practice
old_nav = """        <a href="#oop">\U0001f3d7\ufe0f OOP (Classes)</a>
        <a href="#numpy-pandas">\U0001f4ca NumPy &amp; Pandas</a>
        <a href="#practice">\U0001f3cb\ufe0f Practice Exercises</a>
        <a href="#mini-project">\U0001f3ac Mini Project: Movies</a>"""

new_nav = """        <a href="#numpy-pandas">\U0001f4ca NumPy &amp; Pandas</a>
        <a href="#mini-project">\U0001f3ac Mini Project: Movies</a>
        <a href="#oop">\U0001f3d7\ufe0f OOP (Classes)</a>
        <a href="#practice">\U0001f3cb\ufe0f Practice Exercises</a>"""

content = content.replace(old_nav, new_nav)

# 2) Extract sections to reorder
lines = content.split('\n')

def find_section(lines, section_id):
    start = None
    for i, line in enumerate(lines):
        if f'<section id="{section_id}"' in line:
            start = i
        if start is not None and '</section>' in line and i > start:
            return start, i
    return None, None

oop_start, oop_end = find_section(lines, 'oop')
numpy_start, numpy_end = find_section(lines, 'numpy-pandas')
practice_start, practice_end = find_section(lines, 'practice')
mini_start, mini_end = find_section(lines, 'mini-project')

print(f"OOP: {oop_start}-{oop_end}")
print(f"NumPy: {numpy_start}-{numpy_end}")
print(f"Practice: {practice_start}-{practice_end}")
print(f"Mini: {mini_start}-{mini_end}")

# Find comment/blank lines before each section
def find_block_start(lines, section_start):
    pos = section_start
    for i in range(section_start - 1, max(section_start - 5, 0), -1):
        stripped = lines[i].strip()
        if stripped == '' or stripped.startswith('<!--'):
            pos = i
        else:
            break
    return pos

before_oop = find_block_start(lines, oop_start)
before_numpy = find_block_start(lines, numpy_start)
before_practice = find_block_start(lines, practice_start)
before_mini = find_block_start(lines, mini_start)

print(f"before: oop={before_oop}, numpy={before_numpy}, practice={before_practice}, mini={before_mini}")

# Extract blocks
oop_block = lines[before_oop:oop_end+1]
numpy_block = lines[before_numpy:numpy_end+1]
practice_block = lines[before_practice:practice_end+1]
mini_block = lines[before_mini:mini_end+1]

# Lines before these 4 sections
prefix = lines[:before_oop]
# Lines after all 4 sections
suffix = lines[mini_end+1:]

# Reassemble in new order: NumPy, MiniProject, OOP, Practice
new_lines = prefix + numpy_block + [''] + mini_block + [''] + oop_block + [''] + practice_block + suffix
content = '\n'.join(new_lines)

# 3) Renumber sections
counter = [0]
def replace_label(m):
    counter[0] += 1
    sid = m.group(1)
    if sid == 'mini-project':
        return f'<section id="{sid}" data-label="\U0001f3ac Mini Project"'
    return f'<section id="{sid}" data-label="Section {counter[0]}"'

content = re.sub(r'<section id="([^"]+)" data-label="[^"]*"', replace_label, content)

# 4) ADD COLLAPSIBLE CSS
old_css = 'section{border:1px solid var(--b);border-radius:var(--r);padding:20px 14px 14px;background:rgba(15,26,51,.55);margin-bottom:24px;border-top:3px solid var(--brand);position:relative}'
new_css = """section{border:1px solid var(--b);border-radius:var(--r);padding:0;background:rgba(15,26,51,.55);margin-bottom:24px;border-top:3px solid var(--brand);position:relative;overflow:hidden}
    .sec-header{display:flex;align-items:center;justify-content:space-between;padding:16px 14px 12px;cursor:pointer;user-select:none}
    .sec-header:hover{background:rgba(255,255,255,.04)}
    .sec-header h2{margin:0;flex:1}
    .sec-toggle{width:28px;height:28px;border-radius:8px;border:1px solid var(--b);background:rgba(255,255,255,.06);color:var(--text);display:flex;align-items:center;justify-content:center;font-size:14px;flex-shrink:0;transition:transform .2s}
    section.collapsed .sec-toggle{transform:rotate(-90deg)}
    .sec-body{padding:0 14px 14px}
    section.collapsed .sec-body{display:none}"""

content = content.replace(old_css, new_css)

# 5) Wrap each section with clickable header + collapsible body
def wrap_section(m):
    section_tag = m.group(1)
    h2_content = m.group(2)
    rest = m.group(3)
    return f'''{section_tag}
    <div class="sec-header" onclick="this.parentElement.classList.toggle('collapsed')">
      {h2_content.strip()}
      <span class="sec-toggle">\u25bc</span>
    </div>
    <div class="sec-body">{rest}</div>
    </section>'''

content = re.sub(
    r'(<section id="[^"]*" data-label="[^"]*">)\s*\n\s*(<h2[^>]*>.*?</h2>)(.*?)</section>',
    wrap_section,
    content,
    flags=re.DOTALL
)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Done! Sections reordered and made collapsible.")
