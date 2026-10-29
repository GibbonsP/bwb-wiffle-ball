"""Draws the 1200x630 link-preview images (img/og/<kind>-<slug>.jpg) listed in scripts/share_cards.json
(written by generate.py). Needs Google Chrome and Pillow. Skips images that already exist unless --force;
pass slugs (e.g. p-peter-fraioli) to redraw just those.   python3 scripts/make_og.py [--force] [slug ...]"""
import json, os, subprocess, sys, tempfile, html, concurrent.futures as cf
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
CARDS = json.load(open(os.path.join(ROOT, 'scripts/share_cards.json')))
force = '--force' in sys.argv; only = [a for a in sys.argv[1:] if not a.startswith('--')]
os.makedirs(os.path.join(ROOT, 'img/og'), exist_ok=True)
def furl(p): return 'file://' + os.path.join(ROOT, p) if p else ''
CSS = '''*{box-sizing:border-box;margin:0}html,body{width:1200px;height:630px;background:#0b1a33}
.c{position:relative;width:1200px;height:630px;overflow:hidden;color:#fff;font-family:"IBM Plex Sans",Arial,sans-serif;background:radial-gradient(90% 120% at 25% 30%,#1d3a70 0%,#0e2145 50%,#070f1f 100%)}
.c::before{content:"";position:absolute;left:0;right:0;top:0;height:12px;background:linear-gradient(90deg,#3b62b0,#c9cdd6 50%,#d22d49)}
.brand{position:absolute;left:56px;bottom:40px;display:flex;align-items:center;gap:14px;font-family:Oswald,sans-serif;font-weight:600;font-size:26px;letter-spacing:.14em;text-transform:uppercase;color:rgba(255,255,255,.8)}
.brand img{height:62px}
.art{position:absolute;left:64px;top:92px;width:400px;height:400px;display:flex;align-items:center;justify-content:center}
.art .ph{width:380px;height:380px;border-radius:50%;object-fit:cover;border:10px solid rgba(255,255,255,.92);box-shadow:0 18px 40px rgba(0,0,0,.45);background:#22345e}
.art .ini{width:380px;height:380px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-family:Oswald,sans-serif;font-weight:700;font-size:150px;background:linear-gradient(135deg,#3b62b0,#1d3a70);border:10px solid rgba(255,255,255,.92)}
.art .lg{max-width:390px;max-height:390px;filter:drop-shadow(0 16px 30px rgba(0,0,0,.5))}
.art svg{width:390px;height:390px;filter:drop-shadow(0 16px 30px rgba(0,0,0,.5))}
.tx{position:absolute;left:520px;right:56px;top:112px}
.tx h1{font-family:Oswald,sans-serif;font-weight:700;font-size:92px;line-height:1.02;letter-spacing:.005em}
.tx .sub{margin-top:14px;font-size:32px;color:rgba(255,255,255,.85)}
.tx .bar{width:260px;height:8px;border-radius:4px;margin:22px 0 22px;background:linear-gradient(90deg,#3b62b0,#c9cdd6 50%,#d22d49)}
.tx .st{font-family:Oswald,sans-serif;font-weight:500;font-size:36px;letter-spacing:.04em;line-height:1.3}
.tx .ln{margin-top:10px;font-family:"IBM Plex Mono",monospace;font-size:34px;color:rgba(255,255,255,.8)}
.tl{position:absolute;right:52px;bottom:34px;height:96px;filter:drop-shadow(0 6px 14px rgba(0,0,0,.5))}'''
def page(c):
    n = html.escape(c['title']); size = 92 if len(c['title']) < 16 else 76 if len(c['title']) < 22 else 64
    if c['kind'] == 'p':
        ini = ''.join(w[0] for w in c['title'].split()[:2]).upper()
        art = f'<img class="ph" src="{furl(c["photo"])}">' if c['photo'] else f'<div class="ini">{ini}</div>'
        tl = f'<img class="tl" src="{furl(c["logo"])}">' if c['logo'] else ''
    elif c['kind'] == 't':
        art = f'<img class="lg" src="{furl(c["logo"])}">'; tl = ''
    else:
        art = '<div id="lg"></div>'; tl = ''
    line = f'<div class="ln">{html.escape(c["line"])}</div>' if c.get('line') else ''
    return f'''<!doctype html><meta charset="utf-8"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Oswald:wght@500;600;700&family=IBM+Plex+Sans:wght@400;500&family=IBM+Plex+Mono:wght@500&display=swap">
<style>{CSS}.tx h1{{font-size:{size}px}}</style><div class="c"><div class="art">{art}</div>
<div class="tx"><h1>{n}</h1><div class="sub">{html.escape(c["sub"])}</div><div class="bar"></div><div class="st">{html.escape(c["stats"])}</div>{line}</div>
{tl}<script>{LOGO_JS}
document.getElementById('lg') && (document.getElementById('lg').innerHTML = savantLogoSVG(390));</script><div class="brand"><img src="{furl('img/data/05707d53ff4086a5a1ea.png')}"><span>BWB Wiffleball</span></div></div>'''
def logo_js():
    """the Savant logo function, lifted from generate.py so the preview and the site always match"""
    src = open(os.path.join(ROOT, 'generate.py')).read()
    def fn(name):
        i = src.index('function ' + name + '('); j = src.index('{', i); d = 0
        for k in range(j, len(src)):
            d += (src[k] == '{') - (src[k] == '}')
            if d == 0: return src[i:k + 1]
    return fn('svColor') + '\n' + fn('savantLogoSVG')
def render(c):
    out = os.path.join(ROOT, 'img/og/%s-%s.jpg' % (c['kind'], c['slug']))
    key = '%s-%s' % (c['kind'], c['slug'])
    if (os.path.exists(out) and not force and not (only and key in only)) or (only and key not in only): return None
    with tempfile.TemporaryDirectory() as td:
        h = os.path.join(td, 'c.html'); open(h, 'w').write(page(c)); png = os.path.join(td, 'c.png')
        subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--force-device-scale-factor=1', '--window-size=1200,630',
                        '--user-data-dir=' + os.path.join(td, 'u'), '--virtual-time-budget=9000', '--screenshot=' + png, 'file://' + h],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=90)
        Image.open(png).convert('RGB').resize((1200, 630)).save(out, 'JPEG', quality=84, optimize=True)
    return key
LOGO_JS = logo_js()
if __name__ == '__main__':
    with cf.ThreadPoolExecutor(4) as ex:
        done = [k for k in ex.map(render, CARDS) if k]
    print('drew', len(done), 'preview images')
