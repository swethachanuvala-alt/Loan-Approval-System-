"""
Hand-drawn SVG illustrations (bank, coins, house, card, shield, skyline ...).

They are embedded as base64 <img> tags, so there are no external image files to
host or break once you deploy.  Want real photos instead?  Drop them in an
`assets/` folder and use st.image("assets/yourfile.jpg").
"""
from __future__ import annotations

import base64

_DEFS = """
<defs>
  <radialGradient id="glow" cx="50%" cy="50%" r="50%">
    <stop offset="0" stop-color="#C084FC" stop-opacity="0.55"/>
    <stop offset="0.6" stop-color="#7E22CE" stop-opacity="0.22"/>
    <stop offset="1" stop-color="#3B0764" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="roof" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#C084FC"/><stop offset="1" stop-color="#6B21A8"/>
  </linearGradient>
  <linearGradient id="col" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#D8B4FE"/><stop offset="0.5" stop-color="#F3E8FF"/><stop offset="1" stop-color="#C084FC"/>
  </linearGradient>
  <linearGradient id="step1" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#A855F7"/><stop offset="1" stop-color="#7E22CE"/>
  </linearGradient>
  <linearGradient id="step2" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#7E22CE"/><stop offset="1" stop-color="#581C87"/>
  </linearGradient>
  <linearGradient id="step3" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#581C87"/><stop offset="1" stop-color="#3B0764"/>
  </linearGradient>
  <linearGradient id="coin" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#F3E8FF"/><stop offset="0.5" stop-color="#D8B4FE"/><stop offset="1" stop-color="#A855F7"/>
  </linearGradient>
  <linearGradient id="shield" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#E9D5FF"/><stop offset="0.45" stop-color="#A855F7"/><stop offset="1" stop-color="#6B21A8"/>
  </linearGradient>
  <linearGradient id="shieldno" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#F0ABFC"/><stop offset="0.5" stop-color="#C026D3"/><stop offset="1" stop-color="#581C87"/>
  </linearGradient>
  <linearGradient id="cardg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#8B7CF6"/><stop offset="0.55" stop-color="#A855F7"/><stop offset="1" stop-color="#D946EF"/>
  </linearGradient>
  <linearGradient id="wall" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#E9D5FF"/><stop offset="1" stop-color="#9333EA"/>
  </linearGradient>
  <linearGradient id="sky1" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#A855F7"/><stop offset="1" stop-color="#3B0764"/>
  </linearGradient>
  <linearGradient id="sky2" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#6D28D9"/><stop offset="1" stop-color="#1E0B3A"/>
  </linearGradient>
  <linearGradient id="sky3" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#C084FC"/><stop offset="1" stop-color="#581C87"/>
  </linearGradient>
</defs>
"""

_STYLE = """
<style>
  .bob1{animation:bob 4.2s ease-in-out infinite}
  .bob2{animation:bob 5.4s ease-in-out infinite;animation-delay:-1.6s}
  .bob3{animation:bob 3.6s ease-in-out infinite;animation-delay:-2.4s}
  .tw{animation:tw 2.8s ease-in-out infinite}
  .tw2{animation:tw 3.6s ease-in-out infinite;animation-delay:-1.2s}
  @keyframes bob{0%,100%{transform:translateY(0)}50%{transform:translateY(-12px)}}
  @keyframes tw{0%,100%{opacity:.25}50%{opacity:1}}
</style>
"""


def _svg(view_box: str, body: str) -> str:
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{view_box}">'
            f'{_STYLE}{_DEFS}{body}</svg>')


def img(svg: str, width: str = "100%", extra_style: str = "", alt: str = "illustration") -> str:
    """Wrap an SVG string in an <img> tag with a base64 data-URI."""
    b64 = base64.b64encode(svg.encode("utf-8")).decode("ascii")
    return (f'<img alt="{alt}" src="data:image/svg+xml;base64,{b64}" '
            f'style="width:{width};max-width:100%;height:auto;{extra_style}"/>')


def _coin(cx: float, cy: float, r: float = 26) -> str:
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#coin)" stroke="#A855F7" stroke-width="2.5"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r * 0.68:.1f}" fill="none" stroke="#7E22CE" stroke-opacity=".55" stroke-width="2"/>'
            f'<path d="M{cx} {cy - r * 0.38:.1f} L{cx + r * 0.12:.1f} {cy - r * 0.1:.1f} L{cx + r * 0.4:.1f} {cy - r * 0.08:.1f} '
            f'L{cx + r * 0.18:.1f} {cy + r * 0.1:.1f} L{cx + r * 0.26:.1f} {cy + r * 0.38:.1f} L{cx} {cy + r * 0.22:.1f} '
            f'L{cx - r * 0.26:.1f} {cy + r * 0.38:.1f} L{cx - r * 0.18:.1f} {cy + r * 0.1:.1f} L{cx - r * 0.4:.1f} {cy - r * 0.08:.1f} '
            f'L{cx - r * 0.12:.1f} {cy - r * 0.1:.1f} Z" fill="#7E22CE" fill-opacity=".75"/>')


def _sparkle(cx: float, cy: float, s: float = 10, cls: str = "tw") -> str:
    return (f'<path class="{cls}" d="M{cx} {cy - s} Q{cx} {cy} {cx + s} {cy} Q{cx} {cy} {cx} {cy + s} '
            f'Q{cx} {cy} {cx - s} {cy} Q{cx} {cy} {cx} {cy - s} Z" fill="#F3E8FF"/>')


# ------------------------------------------------------------------------------ hero
def bank_hero() -> str:
    cols = "".join(
        f'<g><rect x="{x}" y="192" width="44" height="150" rx="5" fill="url(#col)"/>'
        f'<rect x="{x - 4}" y="192" width="52" height="10" rx="3" fill="#C084FC"/>'
        f'<rect x="{x - 4}" y="332" width="52" height="10" rx="3" fill="#C084FC"/>'
        f'<rect x="{x + 12}" y="206" width="3" height="124" fill="#9333EA" fill-opacity=".25"/>'
        f'<rect x="{x + 28}" y="206" width="3" height="124" fill="#9333EA" fill-opacity=".25"/></g>'
        for x in (117, 187, 258, 329, 399)
    )
    body = f"""
    <circle cx="280" cy="235" r="215" fill="url(#glow)"/>
    <circle cx="280" cy="235" r="190" fill="none" stroke="#D8B4FE" stroke-opacity=".28" stroke-dasharray="4 10"/>
    <ellipse cx="280" cy="398" rx="250" ry="16" fill="#140826" fill-opacity=".55"/>
    <rect x="54" y="374" width="452" height="20" rx="5" fill="url(#step3)"/>
    <rect x="66" y="358" width="428" height="18" rx="5" fill="url(#step2)"/>
    <rect x="78" y="342" width="404" height="18" rx="5" fill="url(#step1)"/>
    <rect x="100" y="192" width="360" height="150" fill="#3B0764" fill-opacity=".6"/>
    {cols}
    <rect x="90" y="168" width="380" height="26" rx="5" fill="url(#wall)"/>
    <polygon points="78,172 280,64 482,172" fill="url(#roof)"/>
    <polygon points="112,166 280,76 448,166" fill="none" stroke="#F3E8FF" stroke-opacity=".35" stroke-width="2"/>
    <circle cx="280" cy="130" r="26" fill="#F3E8FF" fill-opacity=".92"/>
    {_coin(280, 130, 20)}
    <g class="bob1"><g transform="translate(70 120)">{_coin(0, 0, 30)}</g></g>
    <g class="bob2"><g transform="translate(500 70)">{_coin(0, 0, 22)}</g></g>
    <g class="bob3"><g transform="translate(520 220)">{_coin(0, 0, 17)}</g></g>
    <g class="bob2"><g transform="translate(455 318) rotate(8)">
      <rect x="-62" y="-40" width="124" height="80" rx="12" fill="url(#cardg)" stroke="#F3E8FF" stroke-opacity=".5" stroke-width="2"/>
      <rect x="-62" y="-18" width="124" height="14" fill="#1E0B3A" fill-opacity=".55"/>
      <rect x="-48" y="8" width="26" height="19" rx="4" fill="#F3E8FF" fill-opacity=".9"/>
      <rect x="-12" y="14" width="46" height="5" rx="2.5" fill="#F3E8FF" fill-opacity=".7"/>
      <rect x="-12" y="24" width="30" height="5" rx="2.5" fill="#F3E8FF" fill-opacity=".45"/>
    </g></g>
    <g class="bob1"><g transform="translate(90 310)">
      <path d="M0 -44 L36 -31 V6 C36 28 18 43 0 52 C-18 43 -36 28 -36 6 V-31 Z" fill="url(#shield)" stroke="#F3E8FF" stroke-opacity=".7" stroke-width="3"/>
      <polyline points="-14,2 -4,14 16,-12" fill="none" stroke="#fff" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>
    </g></g>
    {_sparkle(190, 52, 12)}{_sparkle(400, 30, 9, "tw2")}{_sparkle(540, 150, 11)}{_sparkle(30, 230, 9, "tw2")}{_sparkle(520, 380, 8)}
    """
    return _svg("0 0 560 430", body)


# ------------------------------------------------------------------------------ small icons
def icon_form() -> str:
    body = """
    <circle cx="60" cy="60" r="56" fill="url(#glow)"/>
    <rect x="30" y="20" width="60" height="80" rx="9" fill="url(#col)" stroke="#A855F7" stroke-width="3"/>
    <rect x="42" y="34" width="36" height="6" rx="3" fill="#7E22CE"/>
    <rect x="42" y="48" width="36" height="5" rx="2.5" fill="#A855F7" fill-opacity=".7"/>
    <rect x="42" y="60" width="26" height="5" rx="2.5" fill="#A855F7" fill-opacity=".7"/>
    <rect x="42" y="72" width="30" height="5" rx="2.5" fill="#A855F7" fill-opacity=".7"/>
    <g transform="translate(86 78) rotate(40)"><rect x="-5" y="-26" width="10" height="42" rx="3" fill="#D946EF"/>
    <polygon points="-5,16 5,16 0,27" fill="#F3E8FF"/></g>
    """
    return _svg("0 0 120 120", body)


def icon_model() -> str:
    pts_l = [(24, 36), (24, 60), (24, 84)]
    pts_m = [(60, 28), (60, 52), (60, 76), (60, 98)]
    pts_r = [(96, 60)]
    lines = "".join(f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke="#D8B4FE" stroke-opacity=".5" stroke-width="1.6"/>'
                    for a in pts_l for b in pts_m)
    lines += "".join(f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke="#D8B4FE" stroke-opacity=".5" stroke-width="1.6"/>'
                     for a in pts_m for b in pts_r)
    dots = "".join(f'<circle cx="{x}" cy="{y}" r="7" fill="url(#coin)" stroke="#A855F7" stroke-width="2"/>'
                   for x, y in pts_l + pts_m) + '<circle cx="96" cy="60" r="11" fill="url(#cardg)" stroke="#F3E8FF" stroke-width="2.5"/>'
    return _svg("0 0 120 120", f'<circle cx="60" cy="60" r="56" fill="url(#glow)"/>{lines}{dots}')


def icon_approved() -> str:
    body = """
    <circle cx="60" cy="60" r="56" fill="url(#glow)"/>
    <g transform="translate(60 60)">
      <path d="M0 -44 L36 -31 V6 C36 28 18 43 0 52 C-18 43 -36 28 -36 6 V-31 Z" fill="url(#shield)" stroke="#F3E8FF" stroke-opacity=".7" stroke-width="3"/>
      <polyline points="-14,2 -4,14 16,-12" fill="none" stroke="#fff" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>
    </g>
    """
    return _svg("0 0 120 120", body)


def icon_declined() -> str:
    body = """
    <circle cx="60" cy="60" r="56" fill="url(#glow)"/>
    <g transform="translate(60 60)">
      <path d="M0 -44 L36 -31 V6 C36 28 18 43 0 52 C-18 43 -36 28 -36 6 V-31 Z" fill="url(#shieldno)" stroke="#F3E8FF" stroke-opacity=".7" stroke-width="3"/>
      <line x1="-13" y1="-12" x2="13" y2="14" stroke="#fff" stroke-width="7" stroke-linecap="round"/>
      <line x1="13" y1="-12" x2="-13" y2="14" stroke="#fff" stroke-width="7" stroke-linecap="round"/>
    </g>
    """
    return _svg("0 0 120 120", body)


def house_key() -> str:
    body = f"""
    <circle cx="150" cy="120" r="115" fill="url(#glow)"/>
    <ellipse cx="150" cy="212" rx="105" ry="10" fill="#140826" fill-opacity=".5"/>
    <polygon points="38,112 150,26 262,112" fill="url(#roof)"/>
    <polygon points="62,112 150,44 238,112" fill="none" stroke="#F3E8FF" stroke-opacity=".35" stroke-width="2"/>
    <rect x="62" y="110" width="176" height="98" rx="6" fill="url(#wall)"/>
    <path d="M132 208 V164 A18 18 0 0 1 168 164 V208 Z" fill="#3B0764"/>
    <circle cx="160" cy="180" r="3" fill="#E9D5FF"/>
    <rect x="80" y="130" width="34" height="30" rx="5" fill="#3B0764" fill-opacity=".8"/>
    <rect x="186" y="130" width="34" height="30" rx="5" fill="#3B0764" fill-opacity=".8"/>
    <line x1="97" y1="130" x2="97" y2="160" stroke="#C084FC" stroke-width="2"/>
    <line x1="203" y1="130" x2="203" y2="160" stroke="#C084FC" stroke-width="2"/>
    <rect x="206" y="52" width="20" height="40" fill="#6B21A8"/>
    <g class="bob2"><g transform="translate(262 70)">{_coin(0, 0, 22)}</g></g>
    <g class="bob1"><g transform="translate(36 150)">{_coin(0, 0, 17)}</g></g>
    <g class="bob3"><g transform="translate(262 168) rotate(-30)">
      <circle cx="0" cy="0" r="13" fill="none" stroke="#F0ABFC" stroke-width="6"/>
      <rect x="10" y="-3" width="40" height="6" rx="3" fill="#F0ABFC"/>
      <rect x="36" y="3" width="5" height="11" rx="2" fill="#F0ABFC"/><rect x="45" y="3" width="5" height="8" rx="2" fill="#F0ABFC"/>
    </g></g>
    {_sparkle(60, 40, 10)}{_sparkle(240, 20, 8, "tw2")}
    """
    return _svg("0 0 300 230", body)


def coins_stack() -> str:
    def stack(x, n, tone):
        out = ""
        for i in range(n):
            y = 150 - i * 15
            out += (f'<ellipse cx="{x}" cy="{y + 9}" rx="38" ry="13" fill="{tone}"/>'
                    f'<rect x="{x - 38}" y="{y - 6}" width="76" height="15" fill="{tone}"/>'
                    f'<ellipse cx="{x}" cy="{y - 6}" rx="38" ry="13" fill="url(#coin)" stroke="#A855F7" stroke-width="2"/>'
                    f'<ellipse cx="{x}" cy="{y - 6}" rx="24" ry="7.5" fill="none" stroke="#7E22CE" stroke-opacity=".5" stroke-width="2"/>')
        return out
    body = f"""
    <circle cx="130" cy="95" r="100" fill="url(#glow)"/>
    <ellipse cx="130" cy="168" rx="115" ry="10" fill="#140826" fill-opacity=".5"/>
    {stack(78, 3, "#9333EA")}{stack(150, 5, "#7E22CE")}{stack(200, 2, "#A855F7")}
    <g class="bob1"><g transform="translate(150 28)">{_coin(0, 0, 20)}</g></g>
    {_sparkle(40, 50, 9)}{_sparkle(228, 60, 8, "tw2")}
    """
    return _svg("0 0 260 180", body)


def skyline() -> str:
    """Wide banner: purple city skyline with a bank at the centre."""
    rng = [(20, 70, "sky2"), (62, 110, "sky1"), (112, 80, "sky3"), (152, 135, "sky2"), (206, 95, "sky1"),
           (640, 100, "sky1"), (690, 140, "sky2"), (748, 84, "sky3"), (796, 120, "sky1"), (848, 90, "sky2"),
           (900, 130, "sky3"), (952, 76, "sky1"), (1000, 112, "sky2"), (1050, 88, "sky3"), (1100, 124, "sky1")]
    b = ""
    for x, hgt, g in rng:
        w = 36
        y = 200 - hgt
        b += f'<rect x="{x}" y="{y}" width="{w}" height="{hgt}" rx="3" fill="url(#{g})"/>'
        for r in range(int(hgt // 18)):
            for c in range(2):
                op = 0.9 if (r * 3 + c + x) % 5 else 0.25
                b += f'<rect x="{x + 7 + c * 14}" y="{y + 8 + r * 18}" width="8" height="8" rx="1.5" fill="#F3E8FF" fill-opacity="{op}"/>'
    bank = (
        '<polygon points="262,92 420,22 578,92" fill="url(#roof)"/>'
        '<rect x="272" y="92" width="296" height="14" rx="3" fill="url(#wall)"/>'
        + "".join(f'<rect x="{x}" y="106" width="26" height="76" rx="3" fill="url(#col)"/>' for x in (284, 332, 380, 428, 476, 524))
        + '<rect x="262" y="182" width="316" height="10" rx="3" fill="url(#step1)"/>'
        '<rect x="250" y="192" width="340" height="12" rx="3" fill="url(#step2)"/>'
        f'<g transform="translate(420 66)">{_coin(0, 0, 13)}</g>'
    )
    stars = "".join(_sparkle(x, y, s, c) for x, y, s, c in
                    [(120, 30, 7, "tw"), (330, 18, 6, "tw2"), (600, 28, 8, "tw"), (800, 20, 6, "tw2"), (1010, 34, 7, "tw"), (1160, 22, 6, "tw2")])
    body = f'<rect width="1200" height="200" fill="none"/>{stars}{b}{bank}<rect y="200" width="1200" height="4" fill="#A855F7" fill-opacity=".5"/>'
    return _svg("0 0 1200 204", body)
