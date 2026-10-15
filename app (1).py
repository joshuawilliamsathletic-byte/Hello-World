import html
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Hello World Motion Lab", page_icon="✨", layout="wide")

FONTS = ["Arial", "Courier New", "Georgia", "Times New Roman", "Verdana"]
BACKGROUNDS = {
    "Light": ("#ffffff", "#111827"),
    "Dark": ("#0b1020", "#ffffff"),
    "Blue Sky": ("linear-gradient(135deg, #7dd3fc, #dbeafe)", "#082f49"),
    "Sunset": ("linear-gradient(135deg, #431407, #ea580c, #fda4af)", "#ffffff"),
    "Space": ("radial-gradient(circle at 50% 120%, #312e81, #09090b 70%)", "#ffffff"),
}
EFFECTS = ["None", "Rain", "Snow", "Hail", "Wind Gust", "Confetti", "Tornado"]

st.title("✨ Hello World Motion Lab")
st.write("Type a name, customize the look, and experiment with browser animations.")

with st.sidebar:
    st.header("Controls")
    name = st.text_input("Enter your name", value="Hello World", max_chars=80)
    font_family = st.selectbox("Font type", FONTS)
    font_size = st.slider("Font size", min_value=20, max_value=100, value=48, step=2)
    background = st.selectbox("Background", list(BACKGROUNDS.keys()))
    display_mode = st.selectbox("Name display mode", ["Centered", "Ticker Tape", "Repeated"])
    effect = st.selectbox("Dynamic action", EFFECTS)
    speed = st.slider("Animation speed", min_value=0.5, max_value=3.0, value=1.0, step=0.1)
    density = st.slider("Effect density", min_value=10, max_value=100, value=45, step=5)
    st.caption("Animations run in the preview itself, without repeatedly refreshing the Streamlit page.")

bg, text_color = BACKGROUNDS[background]
safe_name = html.escape(name or "Hello World")
safe_font = font_family.replace("'", "")
# Keep all user-controlled values escaped or selected from fixed lists.
if display_mode == "Repeated":
    name_markup = '<div class="repeated">' + "".join(
        f'<div>{safe_name}</div>' for _ in range(6)
    ) + "</div>"
elif display_mode == "Ticker Tape":
    name_markup = f'<div class="ticker"><span>{safe_name}&nbsp;&nbsp;&nbsp; ✦ &nbsp;&nbsp;&nbsp;{safe_name}&nbsp;&nbsp;&nbsp; ✦ &nbsp;&nbsp;&nbsp;</span></div>'
else:
    name_markup = f'<div class="center-name">{safe_name}</div>'

html_doc = f"""
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<style>
  * {{ box-sizing: border-box; }}
  html, body {{ margin: 0; padding: 0; }}
  .stage {{
    position: relative; width: 100%; height: 620px; overflow: hidden;
    border-radius: 18px; background: {bg}; color: {text_color};
    font-family: '{safe_font}', sans-serif;
  }}
  .particles {{ position:absolute; inset:0; overflow:hidden; pointer-events:none; }}
  .particle {{ position:absolute; top:-12%; left:var(--x); opacity:var(--opacity);
    animation: fall var(--duration) linear var(--delay) infinite;
    font-size:var(--size); transform:rotate(var(--rotation)); will-change:transform; }}
  @keyframes fall {{
    0% {{ transform:translate3d(0,-5vh,0) rotate(0deg); }}
    100% {{ transform:translate3d(var(--drift),125vh,0) rotate(720deg); }}
  }}
  .center-name, .ticker, .repeated {{
    position:absolute; z-index:5; left:0; right:0; top:50%;
    transform:translateY(-50%); font-size:{font_size}px; font-weight:700;
    line-height:1.35; text-shadow:0 2px 12px rgba(0,0,0,.12);
  }}
  .center-name {{ text-align:center; padding:0 22px; overflow-wrap:anywhere; }}
  .ticker {{ top:50%; white-space:nowrap; overflow:hidden; transform:translateY(-50%); }}
  .ticker span {{ display:inline-block; padding-left:100%; animation: ticker 12s linear infinite; }}
  @keyframes ticker {{ from {{ transform:translateX(0); }} to {{ transform:translateX(-100%); }} }}
  .repeated {{ top:50%; transform:translateY(-50%); text-align:center; display:flex;
    flex-direction:column; gap:8px; opacity:.96; overflow-wrap:anywhere; }}
  .repeated div:nth-child(even) {{ opacity:.55; }}
  .wind-line {{ position:absolute; left:-35%; width:35%; height:2px; top:var(--y);
    background:linear-gradient(90deg, transparent, currentColor, transparent);
    opacity:.45; animation: gust var(--duration) linear var(--delay) infinite; }}
  @keyframes gust {{ from {{ transform:translateX(0) skewX(-20deg); }}
    to {{ transform:translateX(420%) skewX(-20deg); }} }}
  .tornado {{ position:absolute; left:50%; top:50%; width:220px; height:340px;
    transform:translate(-50%,-50%); opacity:.55; animation:spin 7s linear infinite; }}
  .tornado i {{ position:absolute; left:50%; top:50%; border:3px solid currentColor;
    border-left-color:transparent; border-right-color:transparent; border-radius:50%;
    transform:translate(-50%,-50%) rotateX(65deg); }}
  @keyframes spin {{ to {{ rotate:360deg; }} }}
  .hint {{ position:absolute; bottom:12px; right:14px; z-index:6; font-size:12px; opacity:.65; }}
  @media (prefers-reduced-motion: reduce) {{
    *, *::before, *::after {{ animation-duration:30s !important; }}
  }}
</style>
</head>
<body>
<div class="stage" id="stage">
  <div class="particles" id="particles"></div>
  <div class="wind-layer" id="wind-layer"></div>
  {name_markup}
  <div class="hint">Hello World Motion Lab</div>
</div>
<script>
(() => {{
  const effect = {effect!r};
  const density = {density};
  const speed = {speed};
  const particles = document.getElementById("particles");
  const windLayer = document.getElementById("wind-layer");
  const stage = document.getElementById("stage");
  const symbols = {{
    "Rain": ["💧", "💧", "💧"],
    "Snow": ["❄", "❅", "❆"],
    "Hail": ["🧊", "•", "●"],
    "Confetti": ["🎉", "🟡", "🟣", "🟢", "🔵", "🟠", "✦"]
  }};
  if (symbols[effect]) {{
    for (let i = 0; i < density; i++) {{
      const p = document.createElement("span");
      p.className = "particle";
      p.textContent = symbols[effect][Math.floor(Math.random() * symbols[effect].length)];
      p.style.setProperty("--x", Math.random() * 100 + "%");
      p.style.setProperty("--opacity", (0.35 + Math.random() * 0.6).toFixed(2));
      p.style.setProperty("--size", (effect === "Hail" ? 10 + Math.random()*12 : 14 + Math.random()*16) + "px");
      p.style.setProperty("--duration", ((effect === "Rain" ? 1.2 : effect === "Hail" ? .8 : 4 + Math.random()*5) / speed) + "s");
      p.style.setProperty("--delay", (-Math.random() * 8) + "s");
      p.style.setProperty("--drift", ((Math.random() - .5) * (effect === "Rain" ? 70 : 180)) + "px");
      p.style.setProperty("--rotation", (Math.random()*360) + "deg");
      particles.appendChild(p);
    }}
  }} else if (effect === "Wind Gust") {{
    stage.style.color = getComputedStyle(stage).color;
    for (let i = 0; i < Math.max(12, density / 2); i++) {{
      const line = document.createElement("div");
      line.className = "wind-line";
      line.style.setProperty("--y", Math.random() * 100 + "%");
      line.style.setProperty("--duration", (1.5 + Math.random()*2) / speed + "s");
      line.style.setProperty("--delay", (-Math.random()*4) + "s");
      windLayer.appendChild(line);
    }}
  }} else if (effect === "Tornado") {{
    const twister = document.createElement("div");
    twister.className = "tornado";
    for (let i = 0; i < 12; i++) {{
      const ring = document.createElement("i");
      const width = 35 + (i / 11) * 170;
      ring.style.width = width + "px";
      ring.style.height = (12 + i * 3) + "px";
      ring.style.marginTop = (i - 5.5) * 12 + "px";
      twister.appendChild(ring);
    }}
    twister.style.animationDuration = (7 / speed) + "s";
    particles.appendChild(twister);
  }}
}})();
</script>
</body>
</html>
"""

components.html(html_doc, height=640, scrolling=False)
st.caption("Tip: Choose a different effect or background in the sidebar to experiment. The preview animation loops continuously.")
