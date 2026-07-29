"""Optional HTML engineering report (--report).

This is a non-spec extension. The CLI still works without ``--report``;
the bundle and manifest remain spec-compliant. The report embeds a
runtime timestamp, so it does NOT participate in the byte-identical
determinism guarantee of the bundle output.
"""

import html
import sys
import time
from typing import Dict, List, Tuple


def generate_report(
    bundle: str,
    used: int,
    budget: int,
    included_entries: List[Dict],
    excluded_entries: List[Dict],
    ranked_preview: List[Tuple[str, float, int]],
    tree_str: str,
    task_desc: str,
    args_path: str,
    timing: Dict[str, float],
) -> str:
    included_count = len(included_entries)
    excluded_count = len(excluded_entries)
    truncated_count = sum(1 for e in included_entries if e.get("truncated"))
    total_scanned = included_count + excluded_count
    budget_pct = round(used / budget * 100, 1) if budget > 0 else 0
    coverage = min(1.0, included_count / max(1, total_scanned))
    trunc_penalty = 1.0 - (truncated_count / max(1, included_count)) * 0.3
    quality_score = round(
        (
            min(1.0, used / max(1, budget)) * 0.35
            + coverage * 0.35
            + trunc_penalty * 0.3
        )
        * 100
    )
    bundle_conf = round(
        (
            min(1.0, used / max(1, budget)) * 0.5
            + (1.0 - truncated_count / max(1, included_count)) * 0.3
            + (1.0 if tree_str else 0.0) * 0.2
        )
        * 100
    )

    top_ranked = ranked_preview[:10] if ranked_preview else []

    def esc(s: object) -> str:
        return html.escape(str(s))

    rows_inc = "".join(
        f'<tr><td>{esc(e.get("path",""))}</td><td>{e.get("tokens",0)}</td>'
        f'<td>{esc(e.get("reason",""))}</td>'
        f'<td>{"<span class=\"tag warn\">truncated</span>" if e.get("truncated") else "<span class=\"tag ok\">full</span>"}</td></tr>'
        for e in included_entries
    )

    rows_exc = "".join(
        f'<tr><td>{esc(e.get("path",""))}</td><td>{esc(e.get("reason",""))}</td></tr>'
        for e in excluded_entries
    )

    rank_rows = "".join(
        f'<tr><td>{esc(p)}</td><td>{round(s*100, 1)}</td><td>{t}</td>'
        f'<td><div class="bar-bg"><div class="bar-fill" style="width:{round(s*100, 1)}%"></div></div></td></tr>'
        for p, s, t in top_ranked
    )

    scan_ms = round(timing.get("scan", 0) * 1000)
    rank_ms = round(timing.get("rank", 0) * 1000)
    bundle_ms = round(timing.get("bundle", 0) * 1000)
    total_ms = round(timing.get("total", 0) * 1000)

    ts = time.strftime("%Y-%m-%dT%H:%M:%S")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>ctxpack Engineering Report</title>
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
:root{{--bg:#f8fafc;--card:#ffffff;--border:#e2e8f0;--text:#1e293b;--text2:#64748b;--primary:#4f46e5;--primary2:#818cf8;--success:#10b981;--warn:#f59e0b;--err:#ef4444;--shadow:0 1px 3px rgba(0,0,0,.08),0 1px 2px rgba(0,0,0,.06)}}
@media(prefers-color-scheme:dark){{:root{{--bg:#0f172a;--card:#1e293b;--border:#334155;--text:#e2e8f0;--text2:#94a3b8;--primary:#6366f1;--primary2:#a5b4fc;--shadow:0 1px 3px rgba(0,0,0,.3),0 1px 2px rgba(0,0,0,.2)}}}}
body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Oxygen,Ubuntu,Cantarell,sans-serif;background:var(--bg);color:var(--text);line-height:1.6;padding:24px}}
.wrap{{max-width:1280px;margin:0 auto}}
h1{{font-size:1.6rem;font-weight:600;margin-bottom:4px}}
h2{{font-size:1.15rem;font-weight:600;margin-bottom:16px;padding-bottom:8px;border-bottom:2px solid var(--primary)}}
.sub{{color:var(--text2);font-size:.85rem;margin-bottom:24px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:16px;margin-bottom:28px}}
.card{{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:16px;box-shadow:var(--shadow)}}
.card .val{{font-size:1.8rem;font-weight:700;line-height:1.2}}
.card .lbl{{font-size:.78rem;color:var(--text2);text-transform:uppercase;letter-spacing:.04em}}
.card.accent{{border-left:3px solid var(--primary)}}
.card.green{{border-left:3px solid var(--success)}}
.card.amber{{border-left:3px solid var(--warn)}}
.card.red{{border-left:3px solid var(--err)}}
.section{{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:20px;margin-bottom:20px;box-shadow:var(--shadow)}}
table{{width:100%;border-collapse:collapse;font-size:.85rem}}
th{{text-align:left;padding:10px 8px;border-bottom:2px solid var(--border);color:var(--text2);font-weight:600;text-transform:uppercase;letter-spacing:.03em;font-size:.75rem}}
td{{padding:8px;border-bottom:1px solid var(--border);vertical-align:middle}}
tr:hover td{{background:color-mix(in srgb,var(--primary) 4%,transparent)}}
.tag{{display:inline-block;font-size:.7rem;padding:2px 8px;border-radius:4px;font-weight:500}}
.tag.ok{{background:color-mix(in srgb,var(--success) 15%,transparent);color:var(--success)}}
.tag.warn{{background:color-mix(in srgb,var(--warn) 15%,transparent);color:var(--warn)}}
.bar-bg{{background:var(--border);border-radius:4px;height:6px;overflow:hidden;min-width:60px}}
.bar-fill{{height:100%;border-radius:4px;background:var(--primary);transition:width .3s}}
.pipeline{{display:flex;flex-wrap:wrap;align-items:center;gap:4px 0;padding:8px 0}}
.p-node{{background:color-mix(in srgb,var(--primary) 10%,transparent);color:var(--primary);border:1px solid color-mix(in srgb,var(--primary) 30%,transparent);border-radius:6px;padding:6px 14px;font-size:.78rem;font-weight:500;white-space:nowrap}}
.p-arrow{{color:var(--text2);font-size:1rem;padding:0 4px;user-select:none}}
.charts{{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-bottom:20px}}
.chart-box{{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:16px;box-shadow:var(--shadow)}}
.chart-box h3{{font-size:.9rem;font-weight:600;margin-bottom:8px;color:var(--text2);text-transform:uppercase;letter-spacing:.03em}}
.chart-box canvas{{width:100%;height:220px;display:block}}
.cli-info{{font-family:"SFMono-Regular",Consolas,"Liberation Mono",Menlo,monospace;font-size:.8rem;background:var(--bg);padding:12px 16px;border-radius:6px;border:1px solid var(--border);overflow-x:auto;white-space:pre-wrap;word-break:break-all}}
#pipeline-svg{{width:100%;max-width:900px;height:auto;display:block;margin:0 auto}}
@media(max-width:768px){{.charts{{grid-template-columns:1fr}}}}
</style>
</head>
<body>
<div class="wrap">
<h1>ctxpack Engineering Report</h1>
<div class="sub">{esc(task_desc)} &mdash; {ts}</div>

<div class="grid">
<div class="card accent"><div class="val">{total_scanned}</div><div class="lbl">Files Scanned</div></div>
<div class="card green"><div class="val">{included_count}</div><div class="lbl">Files Included</div></div>
<div class="card red"><div class="val">{excluded_count}</div><div class="lbl">Files Excluded</div></div>
<div class="card accent"><div class="val">{used:,}</div><div class="lbl">Tokens Used / {budget:,}</div></div>
<div class="card green"><div class="val">{quality_score}%</div><div class="lbl">AI Context Quality</div></div>
<div class="card accent"><div class="val">{bundle_conf}%</div><div class="lbl">Bundle Confidence</div></div>
</div>

<div class="section">
<h2>Context Packing Pipeline</h2>
<svg id="pipeline-svg" viewBox="0 0 900 80" xmlns="http://www.w3.org/2000/svg">
<defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="var(--text2, #64748b)"/></marker></defs>
<rect x="4" y="22" width="78" height="36" rx="8" fill="color-mix(in srgb, var(--primary, #4f46e5) 10%, transparent)" stroke="color-mix(in srgb, var(--primary, #4f46e5) 30%, transparent)" stroke-width="1.5"/><text x="43" y="45" text-anchor="middle" font-size="12" font-weight="500" fill="var(--primary, #4f46e5)">Repository</text>
<line x1="82" y1="40" x2="112" y2="40" stroke="var(--text2, #64748b)" stroke-width="1.5" marker-end="url(#a)"/>
<rect x="116" y="22" width="78" height="36" rx="8" fill="color-mix(in srgb, var(--primary, #4f46e5) 10%, transparent)" stroke="color-mix(in srgb, var(--primary, #4f46e5) 30%, transparent)" stroke-width="1.5"/><text x="155" y="45" text-anchor="middle" font-size="12" font-weight="500" fill="var(--primary, #4f46e5)">Scanner</text>
<line x1="194" y1="40" x2="224" y2="40" stroke="var(--text2, #64748b)" stroke-width="1.5" marker-end="url(#a)"/>
<rect x="228" y="22" width="78" height="36" rx="8" fill="color-mix(in srgb, var(--primary, #4f46e5) 10%, transparent)" stroke="color-mix(in srgb, var(--primary, #4f46e5) 30%, transparent)" stroke-width="1.5"/><text x="267" y="45" text-anchor="middle" font-size="12" font-weight="500" fill="var(--primary, #4f46e5)">Analysis</text>
<line x1="306" y1="40" x2="336" y2="40" stroke="var(--text2, #64748b)" stroke-width="1.5" marker-end="url(#a)"/>
<rect x="340" y="22" width="78" height="36" rx="8" fill="color-mix(in srgb, var(--primary, #4f46e5) 10%, transparent)" stroke="color-mix(in srgb, var(--primary, #4f46e5) 30%, transparent)" stroke-width="1.5"/><text x="379" y="45" text-anchor="middle" font-size="12" font-weight="500" fill="var(--primary, #4f46e5)">Ranking</text>
<line x1="418" y1="40" x2="448" y2="40" stroke="var(--text2, #64748b)" stroke-width="1.5" marker-end="url(#a)"/>
<rect x="452" y="22" width="78" height="36" rx="8" fill="color-mix(in srgb, var(--primary, #4f46e5) 10%, transparent)" stroke="color-mix(in srgb, var(--primary, #4f46e5) 30%, transparent)" stroke-width="1.5"/><text x="491" y="45" text-anchor="middle" font-size="12" font-weight="500" fill="var(--primary, #4f46e5)">Budget</text>
<line x1="530" y1="40" x2="560" y2="40" stroke="var(--text2, #64748b)" stroke-width="1.5" marker-end="url(#a)"/>
<rect x="564" y="22" width="78" height="36" rx="8" fill="color-mix(in srgb, var(--success, #10b981) 10%, transparent)" stroke="color-mix(in srgb, var(--success, #10b981) 30%, transparent)" stroke-width="1.5"/><text x="603" y="45" text-anchor="middle" font-size="12" font-weight="600" fill="var(--success, #10b981)">Bundle</text>
<line x1="642" y1="40" x2="672" y2="40" stroke="var(--text2, #64748b)" stroke-width="1.5" marker-end="url(#a)"/>
<rect x="676" y="22" width="78" height="36" rx="8" fill="color-mix(in srgb, var(--primary, #4f46e5) 10%, transparent)" stroke="color-mix(in srgb, var(--primary, #4f46e5) 30%, transparent)" stroke-width="1.5"/><text x="715" y="45" text-anchor="middle" font-size="12" font-weight="500" fill="var(--primary, #4f46e5)">Manifest</text>
<line x1="754" y1="40" x2="784" y2="40" stroke="var(--text2, #64748b)" stroke-width="1.5" marker-end="url(#a)"/>
<rect x="788" y="14" width="108" height="52" rx="8" fill="color-mix(in srgb, var(--success, #10b981) 12%, transparent)" stroke="var(--success, #10b981)" stroke-width="1.5" stroke-dasharray="3,2"/><text x="842" y="37" text-anchor="middle" font-size="11" font-weight="600" fill="var(--success, #10b981)">AI-Ready</text><text x="842" y="53" text-anchor="middle" font-size="11" font-weight="600" fill="var(--success, #10b981)">Output</text>
</svg>
</div>

<div class="charts">
<div class="chart-box">
<h3>Token Budget</h3>
<canvas id="budgetChart"></canvas>
</div>
<div class="chart-box">
<h3>Included vs Excluded</h3>
<canvas id="pieChart"></canvas>
</div>
</div>

<div class="section">
<h2>Top Ranked Files</h2>
<table><thead><tr><th>File</th><th>Score</th><th>Tokens</th><th>Relevance</th></tr></thead><tbody>
{rank_rows if rank_rows else '<tr><td colspan="4" style="color:var(--text2);text-align:center">No files ranked</td></tr>'}
</tbody></table>
</div>

<div class="charts">
<div class="chart-box">
<h3>Processing Time</h3>
<canvas id="timingChart"></canvas>
</div>
<div class="chart-box">
<h3>Ranking Distribution</h3>
<canvas id="rankChart"></canvas>
</div>
</div>

<div class="section">
<h2>Included Files ({included_count})</h2>
<div style="overflow-x:auto"><table><thead><tr><th>File</th><th>Tokens</th><th>Reason</th><th>Status</th></tr></thead><tbody>
{rows_inc}
</tbody></table></div>
</div>

<div class="section">
<h2>Excluded Files ({excluded_count})</h2>
<div style="max-height:400px;overflow-y:auto"><table><thead><tr><th>File</th><th>Reason</th></tr></thead><tbody>
{rows_exc}
</tbody></table></div>
</div>

<div class="section">
<h2>Execution Summary</h2>
<div class="cli-info">
ctxpack --path {esc(args_path)} --task "{esc(task_desc)}" --budget {budget} [--out bundle.md] [--manifest manifest.json] [--report report.html]&#10;&#10;
Scan:       {scan_ms} ms&#10;
Analysis:   {rank_ms} ms&#10;
Generation: {bundle_ms} ms&#10;
Total:      {total_ms} ms&#10;&#10;
Budget:     {budget:,} tokens&#10;
Used:       {used:,} tokens ({budget_pct}%)&#10;
Remaining:  {budget - used:,} tokens&#10;
Included:   {included_count} files ({truncated_count} truncated)&#10;
Excluded:   {excluded_count} files&#10;
Quality:    {quality_score}%&#10;
Confidence: {bundle_conf}%
</div>
</div>

<div class="section">
<h2>CLI Information</h2>
<div class="cli-info">
ctxpack v1.0.0&#10;
Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}&#10;
Platform: {sys.platform}&#10;
Generated: {ts}&#10;
Source: {esc(args_path)}&#10;
Task: {esc(task_desc)}
</div>
</div>

</div>

<script>
(function(){{
var c=document.getElementById.bind(document);
var rem={budget - used};
new Chart(c('budgetChart'),[['Used',{used},'#4f46e5'],['Remaining',rem,'#e2e8f0']]);
new Chart(c('pieChart'),[['Included',{included_count},'#10b981'],['Excluded',{excluded_count},'#ef4444']]);
new Chart(c('timingChart'),[['Scan',{scan_ms},'#4f46e5'],['Analysis',{rank_ms},'#f59e0b'],['Generation',{bundle_ms},'#10b981']]);
var rd=[{','.join(f'{{"l":"{esc(p)}","v":{round(s*100,1)}}}' for p,s,t in top_ranked[:8])}];
new RankChart(c('rankChart'),rd);

function Chart(canvas,data){{
if(!canvas)return;
var ctx=canvas.getContext('2d');
var dpr=window.devicePixelRatio||1;
var rect=canvas.parentElement.getBoundingClientRect();
var w=Math.max(rect.width-32,200);
canvas.width=w*dpr;canvas.height=220*dpr;canvas.style.width=w+'px';canvas.style.height='220px';
ctx.scale(dpr,dpr);
var total=data.reduce(function(s,d){{return s+d[1];}},0)||1;
var x=0;var y=20;var bw=w-20;var bh=32;
data.forEach(function(d,i){{
var p=d[1]/total;
var w2=Math.max(bw*p-2,2);
ctx.fillStyle=d[2];
ctx.beginPath();ctx.roundRect(x+2,y+2,w2,bh-4,4);ctx.fill();
ctx.fillStyle='var(--text2,#64748b)';ctx.font='11px system-ui,-apple-system,sans-serif';
ctx.textAlign='left';ctx.fillText(d[0],x+6,y+16);
ctx.textAlign='right';ctx.fillText(d[1]+(d[0]==='Used'||d[0]==='Remaining'?' tokens':d[0]==='Scan'||d[0]==='Analysis'||d[0]==='Generation'?' ms':' files'),x+bw-2,y+16);
x+=w2+2;
}});
}}

function RankChart(canvas,data){{
if(!canvas||!data.length)return;
var ctx=canvas.getContext('2d');
var dpr=window.devicePixelRatio||1;
var rect=canvas.parentElement.getBoundingClientRect();
var w=Math.max(rect.width-32,200);
var h=Math.max(data.length*28+40,60);
canvas.width=w*dpr;canvas.height=h*dpr;canvas.style.width=w+'px';canvas.style.height=h+'px';
ctx.scale(dpr,dpr);
var mx=Math.max.apply(null,data.map(function(d){{return d.v;}}))||1;
data.forEach(function(d,i){{
var y=16+i*28;
ctx.fillStyle=colorMix('#4f46e5',d.v/mx);
ctx.beginPath();ctx.roundRect(4,y+2,Math.max((w-20)*d.v/mx-8,4),18,4);ctx.fill();
ctx.fillStyle='var(--text,#1e293b)';ctx.font='11px system-ui,-apple-system,sans-serif';ctx.textAlign='left';
var label=d.l.length>28?d.l.slice(0,25)+'...':d.l;
ctx.fillText(label,8,y+15);
ctx.fillStyle='var(--text2,#64748b)';ctx.textAlign='right';ctx.fillText(d.v.toFixed(1),w-8,y+15);
}});
}}

function colorMix(base,ratio){{
var r=parseInt(base.slice(1,3),16);var g=parseInt(base.slice(3,5),16);var b=parseInt(base.slice(5,7),16);
var mr=255-r;var mg=255-g;var mb=255-b;
var nr=Math.round(r+mr*(1-ratio));var ng=Math.round(g+mg*(1-ratio));var nb=Math.round(b+mb*(1-ratio));
return 'rgb('+nr+','+ng+','+nb+')';
}}
}}());
</script>
</body>
</html>"""
