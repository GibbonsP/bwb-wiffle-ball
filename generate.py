import json

data = open('players.json').read()

HTML = r'''<meta charset="utf-8">
<title>BWB Wiffleball Career Register</title>
<meta name="description" content="Career batting, pitching, and fielding records for every player in BWB Wiffleball, 2017 through 2026 — regular season and postseason kept separate.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Oswald:wght@500;600;700&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@500;600&display=swap">
<style>
:root{
  --brandbar:#041e42; --brandbar-ink:#ffffff; --brandbar-line:#0c2c56;
  --paper:#f1f2f5; --card:#ffffff; --ink:#0d1b2e; --muted:#5f6672;
  --line:#dde1e6; --line-strong:#c3c9d1;
  --accent:#041e42; --accent-ink:#ffffff; --accent-soft:#e6eaf1;
  --clay:#d50032; --clay-soft:#fbe1e7; --gold:#a9832f;
  --shadow:0 1px 3px rgba(4,30,66,.09),0 8px 20px rgba(4,30,66,.08);
}
@media (prefers-color-scheme:dark){
  :root:not([data-theme="light"]){
    --paper:#0a1526; --card:#111f38; --ink:#eef1f6; --muted:#93a0b8;
    --line:#22314f; --line-strong:#324566;
    --accent:#5b8fd9; --accent-ink:#0a1526; --accent-soft:#16233d;
    --clay:#ff5470; --clay-soft:#2a1620; --gold:#c9a45c;
    --shadow:0 1px 2px rgba(0,0,0,.45),0 8px 22px rgba(0,0,0,.4);
  }
}
:root[data-theme="dark"]{
  --paper:#0a1526; --card:#111f38; --ink:#eef1f6; --muted:#93a0b8;
  --line:#22314f; --line-strong:#324566;
  --accent:#5b8fd9; --accent-ink:#0a1526; --accent-soft:#16233d;
  --clay:#ff5470; --clay-soft:#2a1620; --gold:#c9a45c;
  --shadow:0 1px 2px rgba(0,0,0,.45),0 8px 22px rgba(0,0,0,.4);
}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);
  font-family:"IBM Plex Sans",-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;
  line-height:1.5;-webkit-font-smoothing:antialiased;}
.wrap{max-width:1180px;margin:0 auto;padding:0 20px 72px;}
a{color:inherit}
button{font:inherit;color:inherit;cursor:pointer}

header.mast{background:var(--brandbar)}
.mast-inner{max-width:1180px;margin:0 auto;padding:20px 20px;
  display:flex;align-items:flex-end;justify-content:space-between;gap:16px;flex-wrap:wrap}
.brandrow{display:flex;align-items:center;gap:12px}
#brandLogo img{height:80px;width:auto;display:block}
.brand h1{font-family:"Oswald","Arial Narrow",sans-serif;font-weight:700;
  font-size:clamp(1.7rem,4.4vw,2.7rem);letter-spacing:.03em;margin:0;line-height:1;
  text-transform:uppercase;text-wrap:balance;}
.brand h1 .b1{color:var(--clay)}
.brand h1 .b2{color:var(--brandbar-ink)}
.brand p{margin:.5rem 0 0;color:rgba(255,255,255,.68);font-size:.82rem;
  letter-spacing:.13em;text-transform:uppercase;}
.tog{background:transparent;border:1px solid rgba(255,255,255,.4);color:var(--brandbar-ink);
  border-radius:999px;padding:7px 14px;font-size:.75rem;letter-spacing:.08em;text-transform:uppercase;
  display:inline-flex;gap:7px;align-items:center;}
.tog:hover{border-color:var(--clay)}
.mast-tools{display:flex;align-items:center;gap:12px;flex-wrap:wrap}
.gsearch{position:relative;width:220px}
.gsearch svg{position:absolute;left:11px;top:50%;transform:translateY(-50%);opacity:.6;
  color:var(--brandbar-ink);pointer-events:none}
.gsearch input{width:100%;padding:8px 12px 8px 34px;border:1px solid rgba(255,255,255,.4);
  border-radius:999px;background:rgba(255,255,255,.08);color:var(--brandbar-ink);font-size:.82rem}
.gsearch input::placeholder{color:rgba(255,255,255,.55)}
.gsearch input:focus{outline:none;border-color:var(--clay);background:rgba(255,255,255,.14)}
.gsearch-results{position:absolute;top:calc(100% + 6px);left:0;right:0;background:var(--card);
  border:1px solid var(--line-strong);border-radius:10px;box-shadow:var(--shadow);overflow:hidden;
  z-index:50;max-height:340px;overflow-y:auto}
.gsr-item{display:flex;align-items:center;gap:9px;width:100%;padding:8px 12px;background:none;
  border:0;border-bottom:1px solid var(--line);text-align:left;color:var(--ink);cursor:pointer;font-size:.85rem}
.gsr-item:last-child{border-bottom:0}
.gsr-item:hover,.gsr-item.active{background:var(--accent-soft)}
.gsr-item img{width:20px;height:20px;object-fit:contain;flex:none;border-radius:4px}
.gsr-item .gsr-dot{width:20px;height:20px;border-radius:50%;flex:none;background:var(--line-strong)}
.gsr-tag{margin-left:auto;font-size:.62rem;letter-spacing:.06em;text-transform:uppercase;color:var(--muted)}
.gsr-empty{padding:12px;font-size:.82rem;color:var(--muted)}
.perf{max-width:1180px;margin:0 auto 22px;padding:0 20px}
.perf i{display:block;height:3px;background:var(--pa,var(--clay));margin-top:3px}

.controls{display:flex;gap:12px;align-items:center;flex-wrap:wrap;margin-bottom:18px}
.search{flex:1;min-width:200px;position:relative}
.search input{width:100%;padding:11px 14px 11px 38px;border:1px solid var(--line-strong);
  border-radius:10px;background:var(--card);color:var(--ink);font-size:.95rem}
.search input:focus{outline:2px solid var(--accent);outline-offset:1px;border-color:transparent}
.search svg{position:absolute;left:12px;top:50%;transform:translateY(-50%);opacity:.5}
.segs{display:inline-flex;border:1px solid var(--line-strong);border-radius:10px;overflow:hidden}
.segs button{padding:10px 15px;background:var(--card);border:0;font-size:.75rem;
  letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
.segs button+button{border-left:1px solid var(--line)}
.segs button[aria-pressed="true"]{background:var(--accent);color:var(--accent-ink);font-weight:600}
.segs.post button[aria-pressed="true"]{background:var(--clay);color:#fff}

.tscroll{overflow-x:auto;border:1px solid var(--line);border-radius:8px;background:var(--card);
  box-shadow:var(--shadow)}
table{border-collapse:collapse;width:100%;font-variant-numeric:tabular-nums}
thead th{position:sticky;top:0;background:var(--accent);z-index:2;
  font-family:"Oswald","Arial Narrow",sans-serif;
  font-size:.72rem;letter-spacing:.06em;text-transform:uppercase;color:var(--accent-ink);
  font-weight:500;text-align:right;padding:12px 10px;white-space:nowrap;opacity:.9;
  border-bottom:2px solid var(--clay);cursor:pointer;user-select:none}
thead th:first-child{text-align:left}
thead th.sorted{opacity:1}
table.sortable thead th:hover{opacity:1}
table.sortable thead th[data-dir]{opacity:1;color:#fff}
thead th .ar{font-size:.6rem;margin-left:3px}
tbody td{text-align:right;padding:9px 10px;font-size:.86rem;white-space:nowrap;
  border-bottom:1px solid var(--line)}
tbody td:first-child{text-align:left;font-weight:500}
tbody tr:last-child td{border-bottom:0}
tbody tr:hover{background:var(--accent-soft)}
.pname{background:none;border:0;padding:0;font-weight:600;color:var(--accent);
  font-size:.9rem;text-align:left}
.pname:hover{text-decoration:underline}
td.mono,th.mono{font-family:"IBM Plex Mono",ui-monospace,monospace}

.azindex{margin-top:4px}
.azgrp{margin-bottom:18px}
.azh{font-family:"Oswald","Arial Narrow",sans-serif;font-size:1.3rem;margin:0 0 6px;color:var(--accent);
  border-bottom:2px solid var(--line-strong);padding-bottom:2px}
.azcols{display:grid;grid-template-columns:repeat(auto-fill,minmax(215px,1fr));gap:1px 14px}
.azitem{display:flex;flex-direction:column;align-items:flex-start;gap:1px;text-align:left;
  background:none;border:0;padding:6px 7px;border-radius:6px;width:100%;font:inherit}
.azitem:hover{background:var(--accent-soft)}
.azn{font-weight:600;color:var(--accent);font-size:.92rem}
.azm{color:var(--muted);font-size:.75rem;font-variant-numeric:tabular-nums}

.back{background:none;border:0;color:var(--accent);font-size:.82rem;letter-spacing:.06em;
  text-transform:uppercase;padding:6px 0;margin:4px 0 14px}
.back:hover{text-decoration:underline}
.phead{display:flex;align-items:baseline;gap:16px;flex-wrap:wrap;margin-bottom:6px}
.phead h2{font-family:"Oswald","Arial Narrow",sans-serif;font-weight:700;font-size:clamp(1.8rem,5vw,2.8rem);
  margin:0;letter-spacing:.01em}
.phead .yrs{color:var(--muted);font-size:.9rem;letter-spacing:.04em}
.phead-team h2{display:inline-block;border-bottom:4px solid var(--tc,var(--accent));padding-bottom:3px}
.thero{border-radius:8px;padding:22px 24px;margin:2px 0 22px;position:relative;overflow:hidden;
  background:linear-gradient(115deg,var(--tp,var(--accent)),color-mix(in srgb,var(--tp,var(--accent)) 66%,#000));
  color:var(--ts,#fff);box-shadow:var(--shadow)}
.thero::after{content:"";position:absolute;inset:0;background:
  radial-gradient(120% 180% at 100% 0%,color-mix(in srgb,var(--ts,#fff) 22%,transparent),transparent 60%);
  pointer-events:none}
.thero h2{margin:0;font-family:"Oswald","Arial Narrow",sans-serif;font-weight:700;letter-spacing:.02em;
  font-size:clamp(1.8rem,5.4vw,2.8rem);color:inherit;position:relative}
.thero .tsub{margin:5px 0 0;font-size:.85rem;letter-spacing:.03em;opacity:.9;position:relative}
.thero .tsub b{font-weight:700}
.clubdot{display:inline-block;width:9px;height:9px;border-radius:2px;margin-right:8px;
  vertical-align:middle;background:var(--cd,var(--line-strong))}
.stlogo{width:44px;height:44px;object-fit:contain;margin-right:9px;vertical-align:middle}
.tlogo-mini{width:18px;height:18px;object-fit:contain;margin-right:6px;vertical-align:middle;border-radius:3px}
.fdotlogo{width:26px;height:26px;object-fit:contain;margin-right:8px;vertical-align:middle}
.tl-wrap{margin-bottom:34px}
.tlg-scroll{overflow-x:auto;border:1px solid var(--line);border-radius:6px;box-shadow:var(--shadow)}
.tlg-grid{display:grid;grid-template-columns:238px repeat(15,minmax(58px,1fr));grid-auto-rows:32px;
  min-width:1160px;background:var(--card)}
.tlg-cell{display:flex;align-items:center;font-size:.72rem}
.tlg-head{background:var(--accent);color:var(--accent-ink);font-family:"Oswald","Arial Narrow",sans-serif;
  font-size:.68rem;letter-spacing:.04em;justify-content:center;padding:8px 2px}
.tlg-head.tlg-name{justify-content:flex-start;padding-left:12px;text-transform:uppercase;letter-spacing:.08em}
.tlg-band{border-bottom:1px solid var(--line)}
.tlg-band.even{background:color-mix(in srgb, var(--muted) 5%, transparent)}
.tlg-name{grid-column:1;padding:0 10px;gap:7px;font-weight:600;font-size:.78rem;
  border-right:1px solid var(--line);background:var(--card);position:sticky;left:0;z-index:1;overflow:hidden}
.tlg-name .pname,.tlg-name span{overflow:hidden;text-overflow:ellipsis;white-space:nowrap;text-align:left}
.tl-logo{width:24px;height:24px;object-fit:contain;flex:none}
.tl-logo-blank{background:var(--line);border-radius:4px}
.tlg-name .tl-logo{width:18px;height:18px}
.tlg-bar{margin:4px 2px;border-radius:4px;padding:0 6px;display:flex;align-items:center;
  font-size:.66rem;font-weight:700;color:#fff;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;
  background:var(--bc);cursor:default}
.splitgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:12px;
  margin:20px 0 36px}
.split{border:1px solid var(--line);border-radius:6px;background:var(--card);padding:14px 16px;
  box-shadow:var(--shadow);border-top:3px solid var(--accent)}
.split:not(.po){border-top-color:var(--tc,var(--accent))}
.split.po{border-top-color:var(--clay)}
.split h4{margin:0 0 8px;font-size:.7rem;letter-spacing:.12em;text-transform:uppercase;color:var(--muted)}
.split.po h4{color:var(--clay)}
.split .line{font-family:"IBM Plex Mono",monospace;font-size:1.02rem;font-weight:600;letter-spacing:.02em}
.split .sub{color:var(--muted);font-size:.8rem;margin-top:3px}

.savant{margin:0 0 30px}
.savant h3{font-family:"Oswald","Arial Narrow",sans-serif;font-weight:700;font-size:1.15rem;margin:0 0 2px}
.savant .smeta{color:var(--muted);font-size:.75rem;margin:0 0 8px;line-height:1.5}
.svchips{margin:2px 0 12px;gap:5px}
.svchips button{padding:3px 9px;font-size:.7rem}
.svpanels{display:grid;grid-template-columns:1fr;gap:6px 30px}
.svpanels.two{grid-template-columns:1fr}
@media(min-width:700px){.svpanels.two{grid-template-columns:1fr 1fr}}
.svpanel h4{font-size:.66rem;letter-spacing:.11em;text-transform:uppercase;color:var(--muted);
  margin:0 0 3px;padding-bottom:3px;border-bottom:1px solid var(--line-strong)}
.svrow{display:grid;grid-template-columns:74px 1fr 46px;align-items:center;gap:9px;padding:3px 0}
.svlab{font-size:.66rem;letter-spacing:.04em;text-transform:uppercase;color:var(--muted)}
.svbar{position:relative;height:17px;display:flex;align-items:center}
.svbar::before{content:"";position:absolute;left:0;right:0;height:4px;border-radius:3px;
  background:linear-gradient(90deg,#3b62b0,#c9cdd6 50%,#d22d49);opacity:.30}
.svdot{position:absolute;top:50%;width:18px;height:18px;border-radius:50%;
  transform:translate(-50%,-50%);display:flex;align-items:center;justify-content:center;
  font-size:.62rem;font-weight:700;color:#fff;border:1.5px solid var(--card);
  box-shadow:0 1px 2px rgba(0,0,0,.25)}
.svval{font-family:"IBM Plex Mono",monospace;font-size:.76rem;text-align:right;
  font-variant-numeric:tabular-nums;color:var(--ink)}
.svleg{margin:8px 0 0;font-size:.7rem;color:var(--muted)}
.svunqtag{font-weight:400;text-transform:none;letter-spacing:0;color:var(--muted);font-style:italic}
.svrow.svunq{opacity:.5}
.svrow.svunq .svbar::before{opacity:.55;background-image:
    repeating-linear-gradient(45deg, rgba(255,255,255,.55) 0 3px, transparent 3px 6px),
    linear-gradient(90deg,#3b62b0,#c9cdd6 50%,#d22d49)}
.svrow.svunq .svdot{border-style:dashed;border-width:2px;opacity:.85}
.cmpsvbar .svdot{font-size:.56rem;overflow:visible}
.svdotltr{position:absolute;top:-12px;left:50%;transform:translateX(-50%);
  font-size:.5rem;font-weight:800;line-height:1.4;color:var(--ink);background:var(--card);
  border:1px solid var(--line-strong);border-radius:3px;padding:0 3px;pointer-events:none}
.svrow.cmpsvunq{opacity:.85}
.svdot.svunq-dot{border-style:dashed;border-width:2px;opacity:.7}

.accolades{margin:0 0 34px}
.acc-block{margin:0 0 16px}
.acc-block h4{font-size:.72rem;letter-spacing:.11em;text-transform:uppercase;color:var(--muted);margin:0 0 8px}
.rings{display:flex;flex-wrap:wrap;gap:8px}
.ring{display:inline-flex;align-items:center;gap:6px;border:1px solid var(--line-strong);
  border-radius:999px;padding:4px 12px;font-size:.84rem;font-variant-numeric:tabular-nums}
.ring .rt{color:var(--muted)}
.ring .trophy,.champbar .ring,.pb-trophy .tl .trophy{color:var(--gold)}
.acc-years{margin:0;font-size:.86rem;font-variant-numeric:tabular-nums;line-height:1.9}
.awroll{margin:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:4px 18px}
.awroll>div{display:flex;gap:8px;align-items:baseline;font-size:.86rem;
  padding:3px 0;border-bottom:1px solid var(--line)}
.awroll dt{font-weight:600;white-space:nowrap}
.awroll dt b{font-family:"IBM Plex Mono",monospace;color:var(--accent);font-weight:600}
.awroll dd{margin:0;color:var(--muted);font-variant-numeric:tabular-nums;text-align:right;flex:1}
td.awc,th.awc{white-space:normal;min-width:5.5em}
td.awc{font-size:.76rem;font-weight:600;color:var(--accent);letter-spacing:.02em}
.acc-leg{margin:14px 0 0;font-size:.76rem;color:var(--muted);line-height:1.7}
.acc-leg b{color:var(--ink);font-weight:600}

.leadership{margin:0 0 20px}
.leadership h4{font-size:.72rem;letter-spacing:.11em;text-transform:uppercase;color:var(--muted);margin:0 0 8px}
.leadership p{margin:0 0 4px;font-size:.9rem}
.acc-grid{display:grid;grid-template-columns:repeat(auto-fill,76px);gap:16px 18px;margin-top:2px}
.acc-trophy{display:flex;flex-direction:column;align-items:center;gap:6px}
.acc-trophy-svg{width:44px;height:69px;filter:drop-shadow(0 3px 4px rgba(0,0,0,.35))}
.acc-trophy .acc-yr{color:var(--ink)}
.acc-trophy .acc-yr,.acc-pennant .acc-yr{font-family:"IBM Plex Mono",monospace;font-weight:700;font-size:.76rem}
.acc-pennant{width:70px;height:64px;display:flex;flex-direction:column;align-items:center;justify-content:flex-start;
  gap:2px;padding-top:9px;clip-path:polygon(0 0,100% 0,100% 55%,50% 100%,0 55%);box-shadow:0 2px 6px rgba(0,0,0,.28);
  border:0;font:inherit;cursor:default}
button.acc-pennant{cursor:pointer}
button.acc-pennant:hover{filter:brightness(1.12)}
.acc-pennant.title{background:linear-gradient(165deg,var(--tc,var(--accent)),color-mix(in srgb,var(--tc,var(--accent)) 62%,#000))}
.acc-pennant.pennant{background:linear-gradient(165deg,var(--tp,var(--tc,var(--accent))),var(--ts,color-mix(in srgb,var(--tc,var(--accent)) 55%,#000)))}
.acc-pennant .acc-yr{color:#fff}
.acc-pennant .acc-star{color:var(--gold);font-size:.72rem;line-height:1;filter:drop-shadow(0 1px 1px rgba(0,0,0,.4))}
.acc-divlogo{width:22px;height:22px;object-fit:contain;filter:drop-shadow(0 1px 2px rgba(0,0,0,.4))}
.stand .rk{display:inline-block;min-width:1.6em;color:var(--ink);font-variant-numeric:tabular-nums;
  font-size:.8rem;margin-right:2px}
.divh{font-family:"Oswald","Arial Narrow",sans-serif;font-size:1.05rem;margin:22px 0 6px;
  color:var(--accent);letter-spacing:.02em;display:flex;align-items:center;gap:9px}
.divh:first-of-type{margin-top:6px}
.divh button.pname.divlink{font:inherit;color:inherit;letter-spacing:inherit}
.divlogo{height:48px;width:auto}
sup.seed{font-size:.62rem;font-weight:700;margin-left:3px;vertical-align:top}
sup.seed.z{color:var(--accent)}
sup.seed.x{color:var(--clay)}
.stand td.pos{color:var(--accent)}
.stand td.neg{color:var(--clay)}
.stand tbody tr:first-child td{font-weight:600}

/* playoff bracket */
.pbwrap{overflow-x:auto;padding:2px 0 6px;margin:2px 0 30px}
.pbracket{display:grid;grid-template-columns:auto 34px auto 34px auto;
  align-items:center;column-gap:0;row-gap:10px;min-width:max-content}
.pb-col{display:flex;flex-direction:column;justify-content:center;gap:22px;grid-row:2}
.pb-lanehead{display:flex;flex-direction:column;align-items:center;gap:8px;
  grid-row:1;justify-self:center}
.pbround{margin:0;font-family:"Oswald","Arial Narrow",sans-serif;font-size:.72rem;
  letter-spacing:.09em;text-transform:uppercase;color:var(--muted);white-space:nowrap}
.pbicon{height:160px;width:auto}
.pb-conn{grid-row:2;display:flex;align-items:center;justify-content:center;
  color:var(--line-strong);font-size:1.4rem;line-height:1;font-weight:700}
.pb-conn::before{content:"❯"}
.pb-match{border:1px solid var(--line);border-radius:10px;background:var(--card);
  box-shadow:var(--shadow);width:260px;flex:none;overflow:hidden}
.pb-match h5{margin:0;padding:6px 11px;font-size:.6rem;letter-spacing:.11em;text-transform:uppercase;
  color:var(--muted);border-bottom:1px solid var(--line);background:var(--accent-soft)}
.pb-score{padding:5px 11px;font-size:.72rem;color:var(--muted);border-top:1px solid var(--line);
  font-variant-numeric:tabular-nums;background:color-mix(in srgb,var(--muted) 7%,transparent)}
.pb-score-row{padding:2px 0;display:flex;align-items:baseline;gap:5px;white-space:nowrap}
.pb-score button.pname{color:inherit;font:inherit;text-decoration:underline;text-underline-offset:2px}
.pb-score button.pb-boxlink{display:block;text-align:left}
.pb-row{display:flex;align-items:center;gap:9px;padding:9px 11px;font-size:.85rem;white-space:nowrap}
.pb-row+.pb-row{border-top:1px solid var(--line)}
.pb-row .sd{color:var(--muted);font-size:.7rem;min-width:1em;font-variant-numeric:tabular-nums}
.pb-row .dot{width:9px;height:9px;border-radius:2px;background:var(--cd,var(--line-strong));flex:none}
.pblogo{width:22px;height:22px;object-fit:contain;flex:none}
.pb-row button.pname,.pb-row span.nm{font:inherit;color:inherit;text-align:left}
.pb-row.win{font-weight:700;background:color-mix(in srgb,var(--cd,var(--accent)) 12%,transparent)}
.pb-row.win::after{content:"›";margin-left:auto;padding-left:8px;color:var(--cd,var(--accent));font-weight:700}
.gscore{margin-left:auto;font-variant-numeric:tabular-nums}
.game-cards{display:flex;flex-wrap:wrap;gap:14px;margin-bottom:20px}

/* -------------------------- player comparison -------------------------- */
.cmppicker{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin:14px 0 24px}
.cmppicker input{padding:8px 12px;border:1px solid var(--line-strong);border-radius:6px;
  background:var(--card);color:var(--ink);font:inherit;font-size:.88rem;min-width:190px}
.cmpvs{font-family:"Oswald","Arial Narrow",sans-serif;text-transform:uppercase;
  letter-spacing:.08em;color:var(--muted);font-size:.78rem;flex:none}
.cmpgo{background:var(--accent);color:var(--accent-ink);padding:8px 16px;border-radius:6px;font-weight:600}
.cmpheads{display:flex;align-items:center;justify-content:center;gap:28px;margin:10px 0 26px;flex-wrap:wrap}
.cmpplayer{display:flex;flex-direction:column;align-items:center;gap:6px;text-align:center;min-width:170px}
.cmpplayer .pphoto{width:64px;height:64px;border-radius:50%;object-fit:cover}
.cmpname{font-size:1.05rem;font-weight:700;color:var(--accent)}
.cmpblock{margin:0 0 26px}
.cmpblock h4{text-align:center}
.cmptable{width:100%;max-width:480px;margin:0 auto;border-collapse:collapse}
.cmptable td{text-align:center;padding:5px 10px;border-bottom:1px solid var(--line)}
.cmplab{color:var(--muted);font-size:.7rem;text-transform:uppercase;letter-spacing:.05em;width:100px}
.cmpwin{color:var(--accent);font-weight:700}
.cmpwinsample{padding:1px 6px;border-radius:4px;background:var(--accent-soft)}
.gscoreboard{font-family:"Oswald","Arial Narrow",sans-serif;font-size:.95rem;letter-spacing:.03em;
  margin:14px 0;text-align:center;color:var(--ink)}
.gtable{border-collapse:collapse;width:100%;max-width:640px;margin:0 auto;table-layout:fixed}
.gtable th,.gtable td{border:1px solid var(--line-strong);text-align:center;vertical-align:middle;padding:8px 6px}
.gcorner{background:var(--paper)}
.gtop,.gside{background:var(--card);font-family:"Oswald","Arial Narrow",sans-serif;font-size:.74rem;
  letter-spacing:.01em;line-height:1.25;color:var(--ink);font-weight:500}
.gside{text-align:right;padding:8px 10px}
.gcatlogo{width:20px;height:20px;object-fit:contain;display:block;margin:0 auto 4px}
.gside .gcatlogo{margin:0 0 4px auto}
.gcell{height:96px;min-width:104px;position:relative}
.gcell.correct{background:color-mix(in srgb, var(--accent) 10%, transparent)}
.gcell.wrong{background:color-mix(in srgb, var(--clay) 8%, transparent)}
.gguess{width:100%;height:100%;border:1px dashed var(--line-strong);background:none;border-radius:8px;
  color:var(--muted);font-size:.78rem;cursor:pointer;font-family:inherit}
.gguess:hover{border-color:var(--accent);color:var(--accent)}
.gform{display:flex;flex-direction:column;gap:4px;align-items:center}
.gform input{width:100%;padding:5px 6px;border:1px solid var(--line-strong);border-radius:6px;font-size:.78rem;
  background:var(--card);color:var(--ink);font-family:inherit}
.gformbtns{display:flex;gap:4px}
.gsubmit,.gcancel{font-size:.66rem;padding:3px 8px;border-radius:6px;border:1px solid var(--line-strong);
  background:var(--card);cursor:pointer;font-family:inherit;color:var(--ink)}
.gsubmit{background:var(--accent);color:var(--accent-ink);border-color:var(--accent)}
.gerr{font-size:.62rem;color:var(--clay);margin:2px 0 0;line-height:1.3}
.gpick{display:block;font-size:.82rem}
.gpoolnote{display:block;font-size:.6rem;color:var(--muted);margin-top:3px;font-weight:400}
.gmiss{color:var(--clay);font-weight:600;text-decoration:line-through;font-size:.8rem}
.statpad{display:flex;flex-direction:column;gap:14px;max-width:640px;margin:0 auto}
.sprow{border:1px solid var(--line-strong);border-radius:10px;padding:12px 14px;background:var(--card)}
.sprow.answered{background:color-mix(in srgb, var(--accent) 8%, var(--card))}
.spquals{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:8px}
.spq{display:inline-flex;align-items:center;gap:5px;font-size:.74rem;font-weight:600;padding:3px 8px;
  border-radius:999px;border:1px solid var(--line-strong);background:var(--paper)}
.spqlogo{width:16px;height:16px;object-fit:contain}
.spqtag{font-style:normal;font-weight:400;text-transform:uppercase;letter-spacing:.04em;font-size:.6rem;
  color:var(--muted);margin-left:2px}
.spval{display:flex;align-items:center;gap:10px;flex-wrap:wrap}
.spyear{color:var(--muted);font-variant-numeric:tabular-nums;font-size:.85rem}
.spscore{margin-left:auto;font-family:"Oswald","Arial Narrow",sans-serif;font-size:1.1rem;color:var(--accent)}
.spretry{background:none;border:0;color:var(--muted);font-size:.7rem;padding:4px 0 0;cursor:pointer;
  text-decoration:underline;font-family:inherit}
.spretry:hover{color:var(--accent)}
.spform{display:flex;gap:6px;flex-wrap:wrap;align-items:center}
.spform select{padding:6px 8px;border:1px solid var(--line-strong);border-radius:6px;font-size:.82rem;
  background:var(--paper);color:var(--ink);font-family:inherit}
.spform select.spplayer{flex:1;min-width:160px}
.sprow.tiered{background:color-mix(in srgb, var(--tier) 14%, var(--card));border-color:var(--tier)}
.sptierrow{display:flex;align-items:baseline;gap:8px;flex-wrap:wrap;margin-top:2px}
.sptier{font-family:"Oswald","Arial Narrow",sans-serif;font-size:.72rem;letter-spacing:.08em;
  text-transform:uppercase;font-weight:700}
.sppct{font-size:.72rem;color:var(--muted)}
.sprk{border:1px solid var(--line-strong);border-radius:10px;padding:12px 14px;background:var(--card);
  margin-bottom:12px}
.sprklist{list-style:none;margin:6px 0 0;padding:0;display:flex;flex-direction:column;gap:4px}
.sprklist li{display:flex;align-items:baseline;gap:8px;font-size:.84rem}
.sprk-n{color:var(--muted);font-variant-numeric:tabular-nums;min-width:1.4em}
.sprklist li b{margin-left:auto;font-variant-numeric:tabular-nums}
.sprk-mine{background:color-mix(in srgb, var(--accent) 12%, transparent);border-radius:6px;padding:2px 6px;
  margin:0 -6px}
.sprk-tag{font-size:.62rem;text-transform:uppercase;letter-spacing:.04em;color:var(--accent);font-weight:700}
.sprk-yours{font-size:.8rem;color:var(--muted);margin:8px 0 0}
.b0team{display:flex;align-items:center;gap:12px;margin:16px 0}
.b0logo{width:44px;height:44px;object-fit:contain;flex:none}
.b0result{border:1px solid var(--tier,var(--line-strong));border-radius:12px;padding:18px 20px;margin:16px 0;
  background:color-mix(in srgb, var(--tier,var(--line-strong)) 12%, var(--card));text-align:center}
.b0record{font-family:"Oswald","Arial Narrow",sans-serif;font-size:2.4rem;font-weight:700;color:var(--tier,var(--ink))}
.b0roster{list-style:decimal;margin:0 0 10px;padding-left:22px;display:flex;flex-direction:column;gap:2px}
.b0pool{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:2px}
.b0row{display:flex;align-items:center;gap:12px;flex-wrap:wrap;padding:8px 10px;border-bottom:1px solid var(--line)}
.b0row.b0picked{background:color-mix(in srgb, var(--accent) 10%, transparent);border-radius:6px}
.b0stats{margin-left:auto;font-size:.76rem;color:var(--muted);font-variant-numeric:tabular-nums}
.b0draft,.b0remove{font-size:.7rem;padding:3px 10px;border-radius:6px;border:1px solid var(--line-strong);
  background:var(--card);cursor:pointer;font-family:inherit;color:var(--ink)}
.b0draft{background:var(--accent);color:var(--accent-ink);border-color:var(--accent)}
.b0remove{color:var(--clay);border-color:var(--clay)}
.b0pround{font-size:.62rem;text-transform:uppercase;letter-spacing:.08em;font-weight:700;color:var(--accent-ink);
  background:var(--accent);border-radius:4px;padding:2px 6px;margin-left:8px;vertical-align:middle}
.b0gamelog{list-style:none;margin:14px 0 0;padding:0;display:flex;flex-wrap:wrap;gap:5px;justify-content:center}
.b0gamelog li{font-size:.68rem;font-variant-numeric:tabular-nums;padding:3px 7px;border-radius:5px;
  background:var(--paper);border:1px solid var(--line-strong)}
.b0gamelog li.b0win{color:var(--accent);border-color:var(--accent)}
.b0gamelog li.b0loss{color:var(--clay);border-color:var(--clay)}
.b0sharebox{display:block;width:100%;max-width:360px;margin:8px auto 0;font-family:inherit;font-size:.78rem;
  padding:8px;border-radius:6px;border:1px solid var(--line-strong);background:var(--paper);color:var(--ink);
  resize:none}
.b0sharebox[hidden]{display:none}
.game-cards .pb-row.win::after{content:none}
.pb-trophy{display:flex;flex-direction:column;gap:9px;padding:24px 28px;border-radius:10px;min-width:240px;
  background:linear-gradient(115deg,var(--tp,var(--gold)),color-mix(in srgb,var(--tp,var(--gold)) 62%,#000));
  color:var(--ts,#fff);box-shadow:var(--shadow)}
.pb-trophy .tl{font-size:.78rem;letter-spacing:.13em;text-transform:uppercase;opacity:.85}
.pb-champrow{display:flex;align-items:center;gap:14px}
.pbtrophylogo{width:64px;height:64px;object-fit:contain;flex:none}
.pb-trophy .tn{font-family:"Oswald","Arial Narrow",sans-serif;font-size:1.9rem;font-weight:700;line-height:1.1}
.pb-trophy button.pname{color:inherit;font:inherit;text-decoration:underline;text-underline-offset:3px}
.capdot{font-size:.56rem;font-weight:700;background:var(--accent);color:var(--accent-ink);
  border-radius:3px;padding:0 3px;margin-left:2px;vertical-align:middle}
.phase{margin:34px 0 0}
.phase>h3,.viewhead{font-family:"Oswald","Arial Narrow",sans-serif;font-weight:700;font-size:1.35rem;margin:0 0 2px;
  letter-spacing:.02em}
.phase.post>h3{color:var(--clay)}
.pmeta{color:var(--muted);font-size:.82rem;margin:0 0 14px}
section.stat{margin:0 0 22px}
section.stat h4{font-size:.72rem;letter-spacing:.11em;text-transform:uppercase;color:var(--muted);
  margin:0 0 8px}
tfoot td{text-align:right;padding:10px;font-weight:700;font-size:.84rem;
  border-top:2px solid var(--line-strong);background:var(--accent-soft)}
.phase.post tfoot td{background:var(--clay-soft)}
.phase.exh tfoot td{background:var(--line)}
.phase.exh>h3{color:var(--muted)}
tfoot td:first-child{text-align:left;letter-spacing:.08em;text-transform:uppercase;font-size:.72rem}
th.lft,td.lft{text-align:left !important}
.detail tbody td.lft{color:var(--muted);font-weight:500}
.detail tbody tr.splitrow td{color:var(--muted);background:color-mix(in srgb,var(--muted) 6%,transparent)}
.detail tbody tr.splitrow td:first-child{color:var(--muted)}
.detail tbody tr.totrow td{font-weight:700;border-bottom:2px solid var(--line-strong)}
.ntm{font-weight:700;font-size:.72rem;letter-spacing:.04em;color:var(--muted)}
.h2htoggle{background:none;border:0;color:var(--muted);font-size:.7rem;padding:0 6px 0 0;
  cursor:pointer;vertical-align:middle}
.h2htoggle:hover{color:var(--accent)}
.h2hdetail td{padding:10px 10px 14px;background:var(--paper)}
.h2hdetail .tscroll{box-shadow:none}
table.h2hsub{font-size:.82rem}
table.h2hsub thead th{padding:7px 10px}
.dir td.tm{color:var(--muted)}
.pt{color:var(--clay);font-weight:700;padding-left:1px}
.estd{color:var(--gold);font-weight:700}
.detail tbody tr.estrow td.lft:first-child{font-style:italic}
.nopost{border:1px dashed var(--line-strong);border-radius:12px;padding:22px;color:var(--muted);
  font-size:.9rem;text-align:center}

.note{margin-top:40px;padding-top:18px;border-top:1px solid var(--line);
  color:var(--muted);font-size:.8rem;line-height:1.65}
.note b{color:var(--ink);font-weight:600}
.empty{padding:40px;text-align:center;color:var(--muted)}
.lead{color:var(--muted);font-size:.88rem;margin:12px 0 20px;max-width:64ch}
.annivpin{height:26px;width:auto;vertical-align:middle;margin-left:9px;position:relative;top:-2px}

.ticker{position:relative;overflow-x:auto;overflow-y:hidden;white-space:nowrap;margin:0 0 14px;
  background:var(--card);border-top:1px solid var(--line);border-bottom:1px solid var(--line);
  cursor:grab;scrollbar-width:thin;overscroll-behavior-x:contain}
.ticker.drag{cursor:grabbing}
.ticker::-webkit-scrollbar{height:6px}
.ticker::-webkit-scrollbar-thumb{background:var(--line-strong);border-radius:3px}
.ticker-track{display:inline-flex;padding:7px 4px}
.tk-item{display:inline-flex;flex-direction:column;align-items:stretch;gap:4px;min-width:150px;
  padding:6px 14px;border-right:1px solid var(--line);font-size:.8rem;cursor:pointer;
  font-variant-numeric:tabular-nums;user-select:none;-webkit-user-select:none}
.tk-item:hover{color:var(--accent)}
.tk-head{display:flex;align-items:center;justify-content:space-between;gap:8px}
.tk-item .tk-d{color:var(--muted);font-size:.72rem}
.tk-head .gtag{margin-left:0}
.tk-row{display:flex;align-items:center;gap:6px}
.tk-nm{flex:1;overflow:hidden;text-overflow:ellipsis}
.tk-r{font-weight:600}
.tk-logo{width:16px;height:16px;object-fit:contain;flex:none}
.tk-w{font-weight:700}
.nav{max-width:1180px;margin:0 auto 20px;padding:0 20px;display:flex;gap:20px;
  border-bottom:1px solid var(--line);overflow-x:auto}
.nav button{background:none;border:0;border-bottom:3px solid transparent;padding:9px 2px;
  margin-bottom:-1px;font-family:"Oswald","Arial Narrow",sans-serif;
  font-size:.85rem;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);white-space:nowrap}
.nav button.active{color:var(--ink);border-color:var(--clay);font-weight:600}
.nav button:hover{color:var(--ink)}
.subtabs{display:flex;gap:20px;margin:20px 0 26px;border-bottom:1px solid var(--line);overflow-x:auto}
.subtabs button{background:none;border:0;border-bottom:3px solid transparent;padding:9px 2px;
  margin-bottom:-1px;font-family:"Oswald","Arial Narrow",sans-serif;
  font-size:.85rem;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);white-space:nowrap}
.subtabs button[aria-pressed="true"]{color:var(--ink);border-color:var(--clay);font-weight:600}
.subtabs button:hover{color:var(--ink)}
.subtabs2{gap:14px;margin:0 0 18px}
.subtabs2 button{font-size:.72rem;padding:6px 2px}
.subtabs2 button[aria-pressed="true"]{border-color:var(--accent)}

.chips{display:flex;flex-wrap:wrap;gap:6px;margin:16px 0 22px}
.chips button{border:1px solid var(--line-strong);background:var(--card);border-radius:999px;
  padding:5px 13px;font-size:.8rem;font-variant-numeric:tabular-nums;color:var(--muted)}
.chips button[aria-pressed="true"]{background:var(--accent);color:var(--accent-ink);
  border-color:transparent;font-weight:600}
.chips button:hover{border-color:var(--accent)}
.logchips{margin:2px 0 12px}

.recgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px;margin-bottom:26px}
.rec{border:1px solid var(--line);border-radius:6px;background:var(--card);padding:13px 15px;
  box-shadow:var(--shadow);border-top:3px solid var(--accent)}
.rec.po{border-top-color:var(--clay)}
.rec h4{margin:0 0 6px;font-size:.66rem;letter-spacing:.12em;text-transform:uppercase;color:var(--muted)}
.rec.po h4{color:var(--clay)}
.rec .big{font-family:"IBM Plex Mono",monospace;font-size:1.15rem;font-weight:600;letter-spacing:.02em}
.rec .sub{color:var(--muted);font-size:.8rem;margin-top:2px}
td.res-W{color:var(--accent);font-weight:700}
td.res-L{color:var(--clay);font-weight:700}
.gtag{font-size:.6rem;letter-spacing:.07em;text-transform:uppercase;color:var(--ink);
  border:1px solid var(--line-strong);border-radius:4px;padding:1px 5px;margin-left:7px}
.recgrid + .segs{margin-bottom:20px}
.bvtgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:12px;margin:0 0 28px}
.bvtcard{display:flex;align-items:center;gap:12px;border:1px solid var(--line);border-radius:8px;
  background:var(--card);padding:12px 14px;box-shadow:var(--shadow);text-decoration:none;color:inherit}
.bvtcard:hover{border-color:var(--line-strong)}
.bvtcard h4{margin:0 0 2px;font-size:.88rem;color:var(--ink)}
.bvtlogo{width:40px;height:40px;flex:none;display:flex;align-items:center;justify-content:center}
.bvtlogo img{max-width:100%;max-height:100%;object-fit:contain}
.officegrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:14px;margin:0 0 28px}
.officegrid-lead{grid-template-columns:repeat(auto-fill,minmax(210px,1fr))}
.officecard{border:1px solid var(--line);border-radius:10px;background:var(--card);padding:18px 14px 16px;
  box-shadow:var(--shadow);display:flex;flex-direction:column;align-items:center;text-align:center;gap:8px}
.officecard.big{padding:24px 18px 20px;border-top:3px solid var(--accent)}
.officephoto{width:64px;height:64px;border-radius:50%;object-fit:cover;box-shadow:var(--shadow)}
.officephoto.big{width:92px;height:92px}
.officephoto-blank{display:block;background:var(--line)}
.officename{font-weight:700;font-size:.92rem}
.officecard.big .officename{font-size:1.05rem}
.officetitles{list-style:none;margin:0;padding:0;color:var(--muted);font-size:.76rem;line-height:1.5}
.vs{font-family:"IBM Plex Mono",monospace;color:var(--muted);font-weight:600;padding:0 .35em}
.wteam{font-weight:700}
.linescore td.b,.linescore th.b{border-left:2px solid var(--line-strong)}
.aka{color:var(--muted);font-size:.82rem;margin:2px 0 18px;line-height:1.9}
.aka2{color:var(--muted);font-size:.8rem}
.tbadge{display:inline-block;border:1px solid var(--line-strong);border-radius:999px;
  padding:3px 10px;margin:0 6px 6px 0;font-size:.8rem;white-space:nowrap}
.tbadge b{font-family:"IBM Plex Mono",monospace;color:var(--accent)}
a{color:var(--accent)}
.subnav{margin:2px 0 22px;font-size:.8rem;letter-spacing:.04em}
.cap{font-size:.58rem;font-weight:700;letter-spacing:.05em;background:var(--accent);color:var(--accent-ink);
  border-radius:3px;padding:0 4px;vertical-align:middle}
.champyear{border:1px solid var(--line);border-radius:6px;background:var(--card);padding:16px 18px;
  margin-bottom:14px;box-shadow:var(--shadow)}
.champhead{display:flex;align-items:center;gap:18px;flex-wrap:wrap;margin-bottom:14px}
.champtext{display:flex;flex-direction:column;gap:5px;min-width:0}
.champhead h4{margin:0;font-family:"Oswald","Arial Narrow",sans-serif;font-size:1.7rem;line-height:1.1}
.champlogo{height:140px;width:auto;flex:none}
.champbadges{display:flex;gap:12px;margin-left:auto}
.pobadge,.wsbadge{height:96px;width:auto;border-radius:8px}
.cscore{color:var(--muted);font-size:.88rem;font-variant-numeric:tabular-nums}
.champphoto{display:block;max-width:100%;height:auto;max-height:520px;width:auto;
  margin:0 auto 12px;border-radius:10px;box-shadow:var(--shadow);object-fit:contain}
.champroster{margin:0;padding-left:1.3em;font-size:.87rem;columns:2;column-gap:20px}
.champroster li{margin:2px 0;break-inside:avoid}
@media (max-width:480px){.champroster{columns:1}}
.asgyear{border:1px solid var(--line);border-radius:6px;background:var(--card);padding:14px 16px;
  margin-bottom:12px;box-shadow:var(--shadow)}
.asgyear h4{margin:0 0 10px;font-family:"Oswald","Arial Narrow",sans-serif;font-size:1.05rem}
.asg2{display:grid;grid-template-columns:1fr 1fr;gap:14px}
@media (max-width:520px){.asg2{grid-template-columns:1fr}}
.asgcol h5{margin:0 0 5px;font-size:.66rem;letter-spacing:.11em;text-transform:uppercase;color:var(--muted)}
.asgcol ol{margin:0;padding-left:1.4em;font-size:.87rem}
.asgcol li{margin:2px 0}
.asgcol li.mut{list-style:none;color:var(--muted);margin-left:-1.4em}
.asgmeta{margin:11px 0 0;padding-top:9px;border-top:1px solid var(--line);font-size:.82rem;color:var(--muted)}
.asgmeta b{color:var(--ink);font-weight:600}
.awyear{margin-bottom:20px}
.awyear h4{font-family:"Oswald","Arial Narrow",sans-serif;font-size:1.2rem;margin:0 0 8px}
.awyear h5{font-size:.66rem;letter-spacing:.11em;text-transform:uppercase;color:var(--muted);margin:12px 0 6px}
td.am{white-space:normal;color:var(--muted);font-size:.8rem;max-width:32ch}
details{border:1px solid var(--line);border-radius:10px;background:var(--card);
  margin-bottom:10px;overflow:hidden}
details summary{padding:10px 14px;cursor:pointer;font-size:.82rem;font-weight:600;
  letter-spacing:.03em;list-style:none}
details summary::-webkit-details-marker{display:none}
details summary::before{content:"▸";color:var(--muted);margin-right:8px;display:inline-block}
details[open] summary::before{content:"▾"}
details[open] summary{border-bottom:1px solid var(--line)}
details .tscroll{border:0;box-shadow:none;border-radius:0}

.champbar{display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin:0 0 24px;
  padding:12px 18px;border-radius:8px;box-shadow:var(--shadow);
  background:linear-gradient(115deg,var(--tp,var(--accent)),color-mix(in srgb,var(--tp,var(--accent)) 68%,#000));
  color:var(--ts,#fff)}
.champbar .ring{font-size:1.3rem;line-height:1}
.champbar b{font-family:"Oswald","Arial Narrow",sans-serif;font-size:1.15rem;letter-spacing:.02em}
.champbar .cy{opacity:.85;font-size:.82rem;letter-spacing:.04em;margin-left:auto}
.champbar button.pname{color:inherit;text-decoration:underline;text-underline-offset:3px;font-weight:700}
.herofeature{border-radius:8px;overflow:hidden;margin:0 0 24px;box-shadow:var(--shadow);background:var(--brandbar)}
.herophoto{display:block;width:100%;aspect-ratio:16/9;max-height:480px;object-fit:cover;object-position:center 22%}
.herocap{background:var(--brandbar);color:var(--brandbar-ink);padding:18px 22px 20px}
.herotag{display:inline-block;background:var(--clay);color:#fff;font-family:"Oswald","Arial Narrow",sans-serif;
  font-size:.68rem;letter-spacing:.1em;text-transform:uppercase;padding:3px 10px;border-radius:3px;margin-bottom:10px}
.herocap h2{margin:0 0 6px;font-family:"Oswald","Arial Narrow",sans-serif;font-weight:700;
  font-size:clamp(1.3rem,3.2vw,1.9rem);line-height:1.15}
.herocap p{margin:0;font-size:.85rem;color:rgba(255,255,255,.75)}
.herocap button.pname{color:#fff;text-decoration:underline;text-underline-offset:3px;font-weight:700}
.snapgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:13px;margin-bottom:12px}
.snapdiv{border:1px solid var(--line);border-radius:6px;background:var(--card);padding:13px 16px;
  box-shadow:var(--shadow)}
.snapdiv h4{margin:0 0 8px;font-family:"Oswald","Arial Narrow",sans-serif;font-size:.95rem;color:var(--accent)}
.snapdiv ol{list-style:none;margin:0;padding:0}
.snapdiv li{display:flex;align-items:center;gap:8px;padding:4px 0;font-size:.86rem}
.snapdiv li b{margin-left:auto;font-family:"IBM Plex Mono",monospace;font-variant-numeric:tabular-nums}
.snaplogo{width:22px;height:22px;object-fit:contain;border-radius:4px;flex:none}
.divchamps{list-style:none;margin:0 0 20px;padding:0;max-width:440px}
.divchamps li{display:flex;align-items:center;gap:10px;padding:7px 0;border-bottom:1px solid var(--line);font-size:.9rem}
.divchamps li:last-child{border-bottom:0}
.divchamps .dy{color:var(--muted);font-size:.82rem;font-family:"IBM Plex Mono",monospace}
.divchamps li b{margin-left:auto;font-family:"IBM Plex Mono",monospace;font-variant-numeric:tabular-nums}
.asglist .asgvs{color:var(--muted);font-size:.84rem}
.asglist .asgr{margin-left:auto;display:flex;align-items:center;gap:10px}
.asglist .res-W{color:var(--accent);font-weight:700;font-size:.82rem}
.asglist .res-L{color:var(--clay);font-weight:700;font-size:.82rem}
.asglist button.pname[data-g]{font-size:.8rem}
.hsub{font-family:"Oswald","Arial Narrow",sans-serif;font-weight:600;font-size:1.4rem;margin:36px 0 15px;
  text-transform:uppercase;letter-spacing:.02em;color:var(--accent);
  padding-left:12px;border-left:5px solid var(--clay)}
.hsub:first-of-type{margin-top:8px}
.llgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:13px;margin-bottom:38px}
.llist{border:1px solid var(--line);border-radius:6px;background:var(--card);padding:12px 13px 14px;
  box-shadow:var(--shadow)}
.llist h4{margin:0 0 8px;font-size:.66rem;letter-spacing:.11em;text-transform:uppercase;color:var(--muted)}
.llist ol{margin:0;padding-left:1.4em;font-size:.88rem}
.llist li{margin:5px 0;display:flex;justify-content:space-between;gap:8px;align-items:center;
  position:relative;padding:4px 6px;border-radius:5px;isolation:isolate}
.llist li::before{content:"";position:absolute;left:0;top:0;bottom:0;z-index:-1;
  width:var(--w,0%);background:color-mix(in srgb,var(--accent) 15%,transparent);
  border-radius:5px;transition:width .3s ease}
.llist li b{font-family:"IBM Plex Mono",monospace;font-variant-numeric:tabular-nums;color:var(--ink);flex:none}
.llist .ln{min-width:0;flex:1;display:flex;flex-direction:column;gap:1px}
.llist .lt{color:var(--muted);font-size:.7rem;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.llist .lt button.pname{display:inline;font-size:inherit;font-weight:600}
.llist button.pname{text-align:left;display:block;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.llogo{width:26px;height:26px;object-fit:contain;flex:none;border-radius:5px}
.tmcell{display:inline-flex;align-items:center;gap:6px}
.llogo-sm{width:18px;height:18px;object-fit:contain;flex:none;border-radius:4px}
.llogo-lg{width:38px;height:38px;object-fit:contain;flex:none;border-radius:7px;vertical-align:middle}
.muteam{display:inline-flex;align-items:center;gap:10px}
.tmchips{display:inline-flex;align-items:center;gap:3px;flex-wrap:wrap}
.tmchip{padding:0;border:none;background:none;cursor:pointer;line-height:0;border-radius:4px}
.tmchip:hover{outline:1.5px solid var(--line-strong)}
.numhist{margin:0 0 26px}
.numhist h4{margin:0 0 10px;font-size:.7rem;letter-spacing:.12em;text-transform:uppercase;color:var(--muted)}
.numrow{display:flex;flex-wrap:wrap;gap:12px}
.numring{position:relative;display:inline-flex;align-items:center;justify-content:center;
  width:46px;height:46px;border-radius:50%;border:3px solid var(--rc-p,var(--line-strong));
  background:var(--card);box-shadow:var(--shadow),inset 0 0 0 3px var(--rc-s,var(--line-strong))}
.numring b{font-family:"IBM Plex Mono",monospace;font-weight:700;font-size:1rem;color:var(--ink)}
.numring-tip{position:absolute;bottom:calc(100% + 7px);left:50%;transform:translateX(-50%);
  background:var(--ink);color:var(--paper);font-size:.7rem;font-weight:500;padding:4px 9px;
  border-radius:5px;white-space:nowrap;opacity:0;pointer-events:none;transition:opacity .12s ease;z-index:5}
/* the first/last ring in the row sits flush against the page edge — a
   centered tooltip there would spill off-screen, so anchor those two to
   the ring's own edge instead of straddling its center */
.numring:last-child .numring-tip{left:auto;right:0;transform:none}
.numring:first-child .numring-tip{left:0;right:auto;transform:none}
.numring:hover .numring-tip{opacity:1}
.sparks{display:flex;gap:12px;flex-wrap:wrap;margin:0 0 26px}
.sparkcard{border:1px solid var(--line);border-radius:6px;background:var(--card);
  padding:10px 14px;flex:1;min-width:170px;box-shadow:var(--shadow)}
.sparkcard h4{margin:0 0 3px;font-size:.63rem;letter-spacing:.11em;text-transform:uppercase;color:var(--muted)}
.sparkcard .spv{font-family:"IBM Plex Mono",monospace;font-size:1.05rem;font-weight:600}
.sparkcard .spv small{color:var(--muted);font-weight:400;font-size:.7rem;margin-left:6px}
svg.spark{display:block;width:100%;height:38px;margin-top:3px;overflow:visible}
.recent{list-style:none;padding:0;margin:0 0 22px;font-size:.88rem}
.recent li{padding:7px 0;border-bottom:1px solid var(--line);display:flex;gap:14px;flex-wrap:wrap;align-items:baseline}
.recent li>span{color:var(--muted)}
.recent li b{font-family:"IBM Plex Mono",monospace;color:var(--ink)}

@media (prefers-reduced-motion:no-preference){
  main{animation:f .16s ease-out}
  @keyframes f{from{opacity:.45}to{opacity:1}}
}
@media (max-width:560px){
  .brand p{font-size:.72rem}
  thead th,tbody td{padding:8px 7px;font-size:.8rem}
}

.editbtn{border:1px solid var(--accent);background:var(--accent-soft);color:var(--accent);
  border-radius:8px;padding:5px 12px;font-size:.78rem;font-weight:600;letter-spacing:.02em;
  align-self:center;white-space:nowrap}
.editbtn:hover{background:var(--accent);color:var(--accent-ink)}
.modalwrap{position:fixed;inset:0;background:rgba(10,14,28,.55);z-index:50;
  display:flex;align-items:flex-start;justify-content:center;padding:4vh 16px;overflow-y:auto}
.modal{background:var(--card);border:1px solid var(--line-strong);border-radius:8px;
  max-width:760px;width:100%;box-shadow:var(--shadow);margin-bottom:4vh}
.modalhead{display:flex;align-items:center;justify-content:space-between;gap:12px;
  padding:16px 20px;border-bottom:1px solid var(--line);position:sticky;top:0;background:var(--card);
  border-radius:8px 8px 0 0}
.modalhead h3{margin:0;font-family:"Oswald","Arial Narrow",sans-serif;font-size:1.2rem}
.modalx{background:none;border:0;font-size:1rem;color:var(--muted);padding:4px 8px;border-radius:6px}
.modalx:hover{background:var(--accent-soft);color:var(--ink)}
.modalbody{padding:16px 20px 22px}
.editrowd{border:1px solid var(--line);border-radius:10px;background:var(--paper);margin-bottom:10px;overflow:hidden}
.editrowd summary{padding:9px 13px;cursor:pointer;font-size:.85rem;font-weight:600}
.editrow{padding:4px 13px 14px}
.editrow h5{font-size:.66rem;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin:12px 0 6px}
.efsub{text-transform:none;letter-spacing:0;font-weight:400;font-family:"IBM Plex Mono",monospace;
  display:inline-flex;align-items:center;gap:3px;margin-left:8px;color:var(--ink)}
.ef3{display:grid;grid-template-columns:1fr 1fr 2fr;gap:8px;margin-bottom:8px}
.efgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(64px,1fr));gap:7px}
.ef{display:flex;flex-direction:column;gap:2px;font-size:.68rem;color:var(--muted)}
.ef.wide{grid-column:span 1}
.ef input,.ef select{font:inherit;font-size:.82rem;padding:5px 6px;border:1px solid var(--line-strong);
  border-radius:6px;background:var(--card);color:var(--ink);width:100%}
.editrowbtns{display:flex;gap:8px;margin-top:12px}
.saveRow,.saveBtn{background:var(--accent);color:var(--accent-ink);border:0;border-radius:8px;
  padding:7px 14px;font-size:.8rem;font-weight:600}
.saveRow:disabled,.saveBtn:disabled{opacity:.5}
.delRow{background:none;border:1px solid var(--clay);color:var(--clay);border-radius:8px;
  padding:7px 14px;font-size:.8rem;font-weight:600}
#addSeasonRow{margin-top:4px}
.imgpreview{width:100%;max-width:220px;aspect-ratio:1;border:1px dashed var(--line-strong);
  border-radius:12px;display:flex;align-items:center;justify-content:center;overflow:hidden;
  background:var(--paper);margin-bottom:12px}
.imgpreview img{width:100%;height:100%;object-fit:cover}
.imgph{color:var(--muted);font-size:.8rem}
#imgPick{display:block;margin-bottom:10px;font-size:.82rem;color:var(--muted)}
.tlogo{width:92px;height:92px;border-radius:14px;object-fit:cover;box-shadow:var(--shadow);
  vertical-align:middle;margin-right:14px;background:var(--card)}
.thero .tlogo{background:rgba(255,255,255,.15)}
.logohist{margin:0 0 22px}
.logohist h4{margin:0 0 10px;font-size:.7rem;letter-spacing:.12em;text-transform:uppercase;color:var(--muted)}
.logohist-row{display:flex;gap:12px;flex-wrap:wrap}
.logohist-item{display:flex;flex-direction:column;align-items:center;gap:7px;border:1px solid var(--line);
  border-radius:6px;background:var(--card);padding:12px 14px;min-width:88px;box-shadow:var(--shadow)}
.logohist-item img{width:60px;height:60px;object-fit:contain}
.logohist-item span{font-size:.74rem;color:var(--muted);font-variant-numeric:tabular-nums;white-space:nowrap}
.pphoto{width:64px;height:64px;border-radius:50%;object-fit:cover;box-shadow:var(--shadow);
  vertical-align:middle;margin-right:12px;flex:none}
.banner{width:100%;max-height:220px;object-fit:cover;border-radius:14px;margin-bottom:18px;
  box-shadow:var(--shadow);display:block}
.barchart text{font-family:"IBM Plex Sans",sans-serif}
.hero-row{display:flex;align-items:center;gap:2px}
.namewrap{display:flex;flex-direction:column;gap:6px}
.sitefoot{max-width:1180px;margin:44px auto 0;padding:22px 20px 34px;border-top:1px solid var(--line);
  display:flex;flex-direction:column;align-items:center;gap:10px}
.footsocial{display:flex;gap:12px}
.footsocial a{color:var(--muted);display:inline-flex;padding:8px;border-radius:10px;
  border:1px solid var(--line-strong)}
.footsocial a:hover{color:var(--accent);border-color:var(--accent)}
.footnote{font-size:.78rem;letter-spacing:.03em;margin:0;color:var(--muted)}
.followgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:12px;margin-bottom:32px}
.followcard{display:flex;align-items:center;gap:13px;border:1px solid var(--line);border-radius:6px;
  background:var(--card);padding:14px 16px;text-align:left;box-shadow:var(--shadow)}
.followcard .fico{flex:none;width:38px;height:38px;border-radius:10px;display:flex;align-items:center;
  justify-content:center;color:#fff}
.followcard.ig .fico{background:linear-gradient(135deg,#4f5bd5,#962fbf 30%,#d62976 55%,#fa7e1e 75%,#feda75)}
.followcard.yt .fico{background:#ff0000}
.followcard.pw .fico{background:none}
.followcard b{display:block;font-family:"Oswald","Arial Narrow",sans-serif;font-size:1rem}
.followcard span{color:var(--muted);font-size:.8rem}
</style>

<header class="mast">
  <div class="mast-inner">
    <div class="brand">
      <div class="brandrow">
        <span id="brandLogo"></span>
        <h1><span class="b1">BWB</span> <span class="b2">Wiffleball</span></h1>
      </div>
      <p id="subtitle">Established in 2012</p>
    </div>
    <div class="mast-tools">
      <div class="gsearch">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/></svg>
        <input id="gsearch" type="search" placeholder="Search players & teams…" autocomplete="off" aria-label="Search players and teams">
        <div class="gsearch-results" id="gsearchResults" hidden></div>
      </div>
      <button class="tog" id="tog" aria-label="Toggle colour theme">
        <span id="togi">◐</span><span id="togt">Theme</span>
      </button>
    </div>
  </div>
</header>
<div class="perf"><i></i></div>
<div class="ticker" id="ticker" aria-label="Recent scores"></div>
<nav class="nav" id="nav"></nav>

<div class="wrap"><main id="app"></main></div>

<footer class="sitefoot">
  <div class="footsocial">
    <a href="https://www.instagram.com/bwbwiffleball" target="_blank" rel="noopener" aria-label="BWB Wiffleball on Instagram">
      <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.8">
        <rect x="2.5" y="2.5" width="19" height="19" rx="5.5"/><circle cx="12" cy="12" r="4.3"/>
        <circle cx="17.4" cy="6.6" r="1.15" fill="currentColor" stroke="none"/></svg>
    </a>
    <a href="https://www.youtube.com/@bwbwiffleball" target="_blank" rel="noopener" aria-label="BWB Wiffleball on YouTube">
      <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.8">
        <rect x="2" y="5" width="20" height="14" rx="4.5"/><path d="M10 9.2v5.6l5.1-2.8z" fill="currentColor" stroke="none"/></svg>
    </a>
    <a href="https://prowiffleball.com/leagues/5" target="_blank" rel="noopener" aria-label="BWB Wiffleball on ProWiffleball">
      <svg viewBox="0 0 34 34" width="24" height="24"><rect width="34" height="34" rx="7" fill="#1e4fa8"/>
        <text x="17" y="23" text-anchor="middle" font-family="Arial Black,Arial,sans-serif" font-weight="900"
          font-style="italic" font-size="14" fill="#fff">PRO</text></svg>
    </a>
  </div>
  <p class="footnote">@bwbwiffleball · BWB Wiffleball Career Register</p>
</footer>

<script id="data" type="application/json">__DATA__</script>
<script>
const DB = JSON.parse(document.getElementById('data').textContent);
if(DB.leagueLogo){
  document.getElementById('brandLogo').innerHTML = `<img src="${DB.leagueLogo}" alt="BWB Wiffleball">`;
}
/* the 15th-anniversary mark — a small inline pin next to a section's own
   heading text wherever it's shown, never floating alone in open space */
function annivBadge(){
  return DB.anniversaryLogo
    ? `<img class="annivpin" src="${DB.anniversaryLogo}" alt="15th Anniversary, 2012–2026" title="15th Anniversary, 2012–2026">`
    : '';
}
const P = DB.players;
/* surname-first helpers so the player index reads like a register */
const SUFFIXES = new Set(['jr','jr.','sr','sr.','ii','iii','iv','v']);
function nameParts(n){
  const p = String(n).trim().split(/\s+/);
  if(p.length < 2) return {first:'', last:p[0]||'', suffix:''};
  let suffix = '';
  if(p.length > 2 && SUFFIXES.has(p[p.length-1].toLowerCase())) suffix = p.pop();
  const last = p.pop();
  return {first:p.join(' '), last, suffix};
}
function nameLast(n){ const q=nameParts(n); return (q.last+' '+q.first+' '+q.suffix).trim().toLowerCase(); }
function nameLF(n){ const q=nameParts(n); return q.first ? `${q.last}, ${q.first}${q.suffix?' '+q.suffix:''}` : q.last; }
const NAMES = Object.keys(P).sort((a,b)=>nameLast(a).localeCompare(nameLast(b)));
const RANGE = DB.seasonRange.join('–');

const tog = document.getElementById('tog');
function applyTheme(t){
  if(t) document.documentElement.setAttribute('data-theme',t);
  else document.documentElement.removeAttribute('data-theme');
  try{ t? localStorage.setItem('bwb-theme',t) : localStorage.removeItem('bwb-theme'); }catch(e){}
}
try{ const s=localStorage.getItem('bwb-theme'); if(s) applyTheme(s); }catch(e){}
tog.addEventListener('click',()=>{
  const cur = document.documentElement.getAttribute('data-theme');
  const dark = cur ? cur==='dark' : matchMedia('(prefers-color-scheme:dark)').matches;
  applyTheme(dark?'light':'dark');
});

/* global header search — players and teams, available on every page (lives
   outside the router-controlled #app, wired once here). Substring match,
   ranked so a name/team that STARTS WITH the query beats one that merely
   contains it; each list capped so one category can't crowd out the other. */
function gsMatches(qRaw){
  const q = qRaw.trim().toLowerCase();
  if(!q) return [];
  const rank = s => { const i = s.toLowerCase().indexOf(q); return i<0 ? 99 : i===0 ? 0 : 1; };
  const players = NAMES.filter(n=>n.toLowerCase().includes(q))
    .sort((a,b)=>rank(a)-rank(b) || a.localeCompare(b)).slice(0,6)
    .map(n=>({type:'player', key:n, label:n, sub:(TEAMS[latestTeam(P[n])]||{}).nick || '', photo:P[n].photo}));
  const teams = TEAMNAMES.filter(t=>t.toLowerCase().includes(q))
    .sort((a,b)=>rank(a)-rank(b) || a.localeCompare(b)).slice(0,5)
    .map(t=>({type:'team', key:t, label:TEAMS[t].nick||t, sub:t, logo:TEAMS[t].logo}));
  return [...players, ...teams];
}
function gsRender(items){
  const box = document.getElementById('gsearchResults');
  if(!items.length){
    box.innerHTML = '<div class="gsr-empty">No players or teams match.</div>';
    box.hidden = false;
    return;
  }
  box.innerHTML = items.map((it,i)=>{
    const mark = it.type==='player'
      ? (it.photo?`<img src="${it.photo}" alt="">`:'<span class="gsr-dot"></span>')
      : (it.logo?`<img src="${it.logo}" alt="">`:'<span class="gsr-dot"></span>');
    return `<button type="button" class="gsr-item${i===0?' active':''}" data-i="${i}">
      ${mark}<span>${esc(it.label)}${it.sub?`<br><small style="color:var(--muted)">${esc(it.sub)}</small>`:''}</span>
      <span class="gsr-tag">${it.type}</span></button>`;
  }).join('');
  box.hidden = false;
}
(function wireGlobalSearch(){
  const input = document.getElementById('gsearch');
  const box = document.getElementById('gsearchResults');
  let items = [], activeIdx = 0;
  const go = it => {
    if(!it) return;
    location.hash = it.type==='player' ? '#/p/'+encodeURIComponent(it.key) : '#/t/'+encodeURIComponent(it.key);
    input.value = ''; box.hidden = true; items = [];
  };
  const setActive = idx => {
    activeIdx = Math.max(0, Math.min(items.length-1, idx));
    box.querySelectorAll('.gsr-item').forEach((el,i)=>el.classList.toggle('active', i===activeIdx));
  };
  input.addEventListener('input', ()=>{
    items = gsMatches(input.value);
    activeIdx = 0;
    if(input.value.trim()) gsRender(items); else box.hidden = true;
  });
  input.addEventListener('keydown', e=>{
    if(box.hidden || !items.length) return;
    if(e.key==='ArrowDown'){ e.preventDefault(); setActive(activeIdx+1); }
    else if(e.key==='ArrowUp'){ e.preventDefault(); setActive(activeIdx-1); }
    else if(e.key==='Enter'){ e.preventDefault(); go(items[activeIdx]); }
    else if(e.key==='Escape'){ box.hidden = true; }
  });
  box.addEventListener('click', e=>{
    const btn = e.target.closest('.gsr-item'); if(!btn) return;
    go(items[+btn.dataset.i]);
  });
  document.addEventListener('click', e=>{
    if(!e.target.closest('.gsearch')) box.hidden = true;
  });
})();

/* ---------------- franchise colours (from the club wordmark sheet) ------- */
const FRANCHISE_COLORS = {
  'Brookside Kraken':{p:'#3aa8ff',s:'#ff2fd6'}, 'Brookside Panthers':{p:'#111111',s:'#e11d1d'},
  'Beaver Brook Lavahogs':{p:'#ff6d01',s:'#111111'}, 'Brookside Squirrels':{p:'#3d85c6',s:'#7a4a12'},
  'Brookside Royals':{p:'#e23b2e',s:'#ffffff'}, 'Davenport Sox':{p:'#ff9900',s:'#111111'},
  'Brentwood Aces':{p:'#e8b420',s:'#1f3ad0'}, 'Gleason Devils':{p:'#3fb6bf',s:'#9c0d0d'},
  'Downtown Angels':{p:'#674ea7',s:'#ffffff'}, 'Brentwood Mustangs':{p:'#8f9196',s:'#e11d1d'},
  'Brentwood Braves':{p:'#0b3d70',s:'#d21f1f'}, 'Glenwood Process':{p:'#1f47ff',s:'#ffffff'},
  'Harris Kings':{p:'#e23b2e',s:'#3aa8ff'}, 'Purchase PawSox':{p:'#0b3d70',s:'#e11d1d'},
  'Brentwood Gladiators':{p:'#3d2185',s:'#f2b90c'}, 'Purchase Dragons':{p:'#ff6d01',s:'#111111'},
  'Shelton Shock':{p:'#122a63',s:'#4285f4'}, 'Brentwood Bananas':{p:'#f2c010',s:'#2a9d47'},
  'Downtown Titans':{p:'#8a1414',s:'#ffa500'}, 'Silver Lake Snapping Turtles':{p:'#2f9e46',s:'#7a4a12'},
};
function _hx(h){ h=h.replace('#',''); return [parseInt(h.slice(0,2),16),parseInt(h.slice(2,4),16),parseInt(h.slice(4,6),16)]; }
function _lum(hex){ const [r,g,b]=_hx(hex).map(v=>{v/=255; return v<=.03928?v/12.92:Math.pow((v+.055)/1.055,2.4);}); return .2126*r+.7152*g+.0722*b; }
function _hsl(hex){ let [r,g,b]=_hx(hex).map(v=>v/255); const mx=Math.max(r,g,b),mn=Math.min(r,g,b),d=mx-mn;
  let h=0,s=0,l=(mx+mn)/2; if(d){ s=d/(1-Math.abs(2*l-1));
    h = mx===r ? ((g-b)/d)%6 : mx===g ? (b-r)/d+2 : (r-g)/d+4; h*=60; if(h<0) h+=360; } return [h,s,l]; }
function _tohex(h,s,l){ const c=(1-Math.abs(2*l-1))*s, x=c*(1-Math.abs((h/60)%2-1)), m=l-c/2;
  let [r,g,b] = h<60?[c,x,0]:h<120?[x,c,0]:h<180?[0,c,x]:h<240?[0,x,c]:h<300?[x,0,c]:[c,0,x];
  return '#'+[r,g,b].map(v=>Math.round((v+m)*255).toString(16).padStart(2,'0')).join(''); }
/* theme-neutral accent: pick the club colour nearer mid-lightness, then clamp */
function teamAccent(full){
  const c = FRANCHISE_COLORS[full]; if(!c) return null;
  const pick = Math.abs(_lum(c.p)-0.32) <= Math.abs(_lum(c.s)-0.32) ? c.p : c.s;
  let [h,s,l] = _hsl(pick);
  s = Math.max(s, 0.42); l = Math.min(Math.max(l, 0.42), 0.60);
  return _tohex(h,s,l);
}
function setTeamVars(full){
  const c = FRANCHISE_COLORS[full];
  app.style.removeProperty('--tc'); app.style.removeProperty('--tp'); app.style.removeProperty('--ts');
  const a = teamAccent(full);
  if(a) app.style.setProperty('--tc', a);
  if(c){ app.style.setProperty('--tp', c.p); app.style.setProperty('--ts', c.s); }
}

function setNav(v){
  const b=(k,l)=>`<button data-v="${k}" class="${v===k?'active':''}">${l}</button>`;
  document.getElementById('nav').innerHTML =
    b('home','Home')+b('players','Players')+b('teams','Teams')+b('standings','Standings')
    +b('leaders','Leaders')+b('records','Records')+b('games','Games')+b('champs','Champions')
    +b('awards','Awards')+b('beavers','Beavers')+b('office','League Office')+b('arcade','Arcade');
  document.querySelectorAll('#nav button').forEach(x=>x.addEventListener('click',()=>{
    location.hash = x.dataset.v==='home' ? '#/' : '#/'+x.dataset.v;
  }));
}

const rate = v => !isFinite(v) ? '—' : (v>=1 ? v.toFixed(3) : v.toFixed(3).replace(/^0/,''));
const two  = v => !isFinite(v) ? '—' : v.toFixed(2);
const ipStr= outs => Math.floor(outs/3) + '.' + (outs%3);
const avg = d => d.AB ? d.H/d.AB : NaN;
const obp = d => (d.AB+d.BB+d.HBP+d.SF) ? (d.H+d.BB+d.HBP)/(d.AB+d.BB+d.HBP+d.SF) : NaN;
const slg = d => d.AB ? d.TB/d.AB : NaN;
const ops = d => obp(d)+slg(d);
/* BWB games are 3 innings, so ERA and K-rate are per 3 IP (a full game), not per 9 */
const era = d => d.IPouts ? 3*d.ER/(d.IPouts/3) : NaN;
const whip= d => d.IPouts ? (d.pBB+d.pH)/(d.IPouts/3) : NaN;
const k9  = d => d.IPouts ? 3*d.pK/(d.IPouts/3) : NaN;
const fld = d => d.TC ? (d.PO+d.A)/d.TC : NaN;
const esc = s => String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const TROPHY = '<svg class="trophy" viewBox="0 0 24 24" width="1em" height="1em" fill="currentColor" aria-hidden="true"><path d="M6 3h12v2h2a1 1 0 0 1 1 1c0 3.3-2.2 5.6-5 5.95A5.5 5.5 0 0 1 13 15.9V18h3v2H8v-2h3v-2.1A5.5 5.5 0 0 1 8 11.95C5.2 11.6 3 9.3 3 6a1 1 0 0 1 1-1h2V3Zm0 4H4.6c.3 1.7 1.6 3 3.2 3.4A7.4 7.4 0 0 1 6 7Zm12 0a7.4 7.4 0 0 1-1.8 3.4c1.6-.4 2.9-1.7 3.2-3.4H18Z"/></svg>';
const phLabel = p => p==='AllStar' ? 'All-Star' : p==='Exhib' ? 'Exhibition' : p;

/* display rows for one player, one phase — one per year, split by club with a
   season total row (Baseball-Reference style) when they changed clubs mid-year */
function byYear(pl, type){
  const rank = s => s.split ? 0 : s.tot ? 2 : 1;
  return pl.seasons.filter(s=>s.type===type).slice()
    .sort((a,b)=> a.year-b.year || rank(a)-rank(b));
}
function teamLink(nm){
  return (typeof TEAMS!=='undefined' && TEAMS[nm])
    ? `<button class="pname" data-t="${esc(nm)}">${esc(nm)}</button>` : esc(nm);
}
/* name a franchise went by in a given season (with its location prefix kept) */
function histName(full, y){
  const t = (typeof TEAMS!=='undefined') && TEAMS[full];
  if(!t) return full;
  const nm = (t.nameByYear||{})[y];
  if(!nm || nm===t.nick) return full;
  return (t.loc && !nm.startsWith(t.loc)) ? t.loc+' '+nm : nm;
}
/* the logo a franchise used in a given season, falling back to its current logo */
function teamLogoForYear(full, y){
  const t = (typeof TEAMS!=='undefined') && TEAMS[full];
  if(!t) return null;
  const hist = t.logoHistory;
  if(hist) for(const h of hist){
    if(y>=h.from && (h.to==null || y<=h.to)) return h.logo;
  }
  return t.logo || null;
}
/* short nickname a franchise went by in a given season — like histName but
   without the location prefix, for narrow game/box-score contexts ("vs X") */
function histNick(full, y){
  const t = (typeof TEAMS!=='undefined') && TEAMS[full];
  if(!t) return full;
  return (t.nameByYear||{})[y] || t.nick;
}
/* clickable team reference that DISPLAYS the era-accurate name for year y but
   still LINKS to the current franchise page (data-t stays the live key) —
   the full-name and nickname variants used wherever a game/record is tied to
   one specific year, so a page never claims a modern name existed back then */
function histTeamLink(full, y){
  return (typeof TEAMS!=='undefined' && TEAMS[full])
    ? `<button class="pname" data-t="${esc(full)}">${esc(histName(full, y))}</button>` : esc(full);
}
function histNickLink(full, y){
  return (typeof TEAMS!=='undefined' && TEAMS[full])
    ? `<button class="pname" data-t="${esc(full)}">${esc(histNick(full, y))}</button>` : esc(full);
}
/* full franchise name for a single-team player-season (or the latest team
   on record for a career total); abbreviated nicknames joined "A/B" for a
   player who split a year between two teams (a full "Brookside Panthers /
   Brentwood Braves" would blow out a narrow leader-list column). Also
   resolves the era-accurate logo(s) for that team/year — a split season
   shows only the second (most recent) club's mark, matching the single
   logo the rest of a split row's badges use. */
function teamOfPlayer(x, year, isCareer){
  const ty = P[x.n].teamsByYear || {};
  let team, yr;
  if(isCareer){
    const ys = Object.keys(ty).map(Number).sort((a,b)=>b-a);
    yr = ys[0]; team = yr!=null ? (ty[yr].team || '') : '';
  } else {
    yr = year; team = (ty[yr] && ty[yr].team) || (x.s && x.s.team) || '';
  }
  if(!team) return {label:'', logo:null, logo2:null};
  if(team.includes(' / ')){
    const teams = team.split(' / ');
    return {label: esc(teams.map(t=>TEAMS[t]?TEAMS[t].nick:t).join('/')),
      logo: teamLogoForYear(teams[0], yr), logo2: teams[1] ? teamLogoForYear(teams[1], yr) : null};
  }
  return {label: esc(TEAMS[team] ? histName(team, yr) : team), logo: TEAMS[team] ? teamLogoForYear(team, yr) : null, logo2:null};
}
function teamCell(d){
  if(d.tot) return `<span class="ntm">${d.nTeams}TM</span>`;
  if(!d.team) return '—';
  return d.team.split(' / ').map(full => {
      if(TEAMS[full]) return `<button class="pname" data-t="${esc(full)}">${esc(histName(full, d.year))}</button>`;
      if(full==='Brookside Beavers') return `<button class="pname" data-beavers>${esc(full)}</button>`;
      return esc(full);
    }).join(' / ')
    + (d.teamPartial ? '<span class="pt">*</span>' : '');
}
function latestTeam(pl){
  const ys = Object.keys(pl.teamsByYear).map(Number).sort((a,b)=>b-a);
  for(const y of ys){ const t=pl.teamsByYear[y]; if(t && t.team) return t.team; }
  return '';
}
/* every distinct franchise a player has ever been credited to (splitting a
   two-team season's combined "A / B" string), in first-appearance order —
   each as its own list of contiguous stints (a player who left and came
   back to the same club gets two ranges, not one span papering over the
   gap) — for showing a player's whole career team history at a glance,
   not just their latest club */
function careerTeams(pl){
  const ys = Object.keys(pl.teamsByYear).map(Number).sort((a,b)=>a-b);
  const order = [], byTeam = {};
  ys.forEach(y=>{
    const t = pl.teamsByYear[y] && pl.teamsByYear[y].team;
    if(!t) return;
    t.split(' / ').forEach(tm=>{
      if(!tm) return;
      if(!byTeam[tm]){ byTeam[tm]=[]; order.push(tm); }
      const stints = byTeam[tm], open = stints[stints.length-1];
      if(open && open.to===y-1) open.to = y; else stints.push({from:y, to:y});
    });
  });
  return order.map(tm=>({team:tm, stints:byTeam[tm]}));
}
/* compact row of small clickable team-logo chips covering a player's whole
   career, each tooltipped with the franchise name and the years it covers */
function teamHistoryChips(pl){
  const teams = careerTeams(pl);
  if(!teams.length) return '—';
  return `<span class="tmchips">${teams.map(t=>{
    const lastYr = t.stints[t.stints.length-1].to;
    const logo = TEAMS[t.team] ? teamLogoForYear(t.team, lastYr) : null;
    const label = TEAMS[t.team] ? histName(t.team, lastYr) : t.team;
    const yrs = t.stints.map(s=>s.from===s.to?String(s.from):`${s.from}–${s.to}`).join(', ');
    return `<button class="pname tmchip" data-t="${esc(t.team)}" title="${esc(label)} · ${yrs}">${logo
      ? `<img class="llogo llogo-sm" src="${logo}" alt="${esc(label)}">` : esc(TEAMS[t.team]?TEAMS[t.team].nick:t.team)}</button>`;
  }).join('')}</span>`;
}
const yearsOf = (pl,type) => [...new Set(pl.seasons.filter(s=>s.type===type).map(s=>s.year))].sort();

/* ---------------- directory ---------------- */
const app = document.getElementById('app');
let mode='bat', phase='reg', sortKey='G', sortDir=-1, query='', pView='stats';

const BAT_COLS = [
  ['name','Player','s'],['team','Tm','s'],['yrs','Yrs','n'],['G','G','n'],['PA','PA','n'],['AB','AB','n'],
  ['R','R','n'],['H','H','n'],['HR','HR','n'],['RBI','RBI','n'],['BB','BB','n'],['K','K','n'],
  ['AVG','AVG','r'],['OBP','OBP','r'],['SLG','SLG','r'],['OPS','OPS','r'],['OPS+','OPS+','n']
];
const PIT_COLS = [
  ['name','Player','s'],['team','Tm','s'],['yrs','Yrs','n'],['G','G','n'],['IP','IP','n'],['W','W','n'],['L','L','n'],
  ['SV','SV','n'],['pH','H','n'],['ER','ER','n'],['pBB','BB','n'],['pK','K','n'],
  ['ERA','ERA','r'],['WHIP','WHIP','r'],['K9','K/3','r'],['ERA+','ERA+','n']
];

function rowVals(name){
  const pl = P[name];
  const isPost = phase==='post';
  const c = isPost ? pl.careerPO : pl.careerReg;
  return {
    name, team: latestTeam(pl) || '—', teamCount: careerTeams(pl).length,
    yrs: yearsOf(pl, isPost?'Playoffs':'Regular').length,
    G: mode==='bat'? c.G_bat : c.G_pit,
    PA:c.PA, AB:c.AB, R:c.R, H:c.H, HR:c.HR, RBI:c.RBI, BB:c.BB, K:c.K,
    AVG:avg(c), OBP:obp(c), SLG:slg(c), OPS:ops(c), 'OPS+':opsPlusFor(c, careerWeights(pl, isPost)),
    IP:c.IPouts/3, W:c.W, L:c.L, SV:c.SV, pH:c.pH, ER:c.ER, pBB:c.pBB, pK:c.pK,
    ERA:era(c), WHIP:whip(c), K9:k9(c), 'ERA+':eraPlusFor(c, careerWeightsPit(pl, isPost)),
    _ipouts:c.IPouts, _bat:c.G_bat
  };
}
function cell(v,type,key){
  if(key==='team') return String(v).split(' / ').map(teamLink).join(' / ');
  if(type==='s') return esc(String(v));
  if(type==='r') return (key==='ERA'||key==='WHIP'||key==='K9')?two(v):rate(v);
  if(key==='IP') return ipStr(Math.round(v*3));
  return isFinite(v)? String(v) : '—';
}

function renderHome(){
  setNav('home');
  const ll=(t,items,fmt,low)=>{
    const w = svBarW(items, low);
    return `<div class="llist"><h4>${t}</h4><ol>${items.map(it=>{
      const logo = it.logo2 ? `<img class="llogo" src="${it.logo2}" alt="">` : (it.logo?`<img class="llogo" src="${it.logo}" alt="">`:'');
      return `<li style="--w:${w(it.v).toFixed(1)}%">${logo}<span class="ln"><button class="pname" data-p="${esc(it.n)}">${esc(it.n)}</button>${
        it.tm?`<span class="lt">${it.tm}</span>`:''}</span><b>${fmt(it.v)}</b></li>`;
    }).join('')}</ol></div>`;
  };
  const rank = (arr, dir) => arr.filter(x=>isFinite(x.v)).sort((a,b)=>dir*(b.v-a.v)).slice(0,7);
  const withTeam = (items, year, isCareer) => items.map(it=>{
    const ti = teamOfPlayer(it, year, isCareer);
    return {...it, tm:ti.label, logo:ti.logo, logo2:ti.logo2};
  });

  // ---- career (regular season) ----
  const cReg = f => NAMES.map(n=>({n, v:f(P[n].careerReg)}));
  const cPool = flt => NAMES.map(n=>({n, c:P[n].careerReg})).filter(flt);
  const cRank = (arr, dir) => withTeam(rank(arr, dir), null, true);
  const cGrid = [
    ll('Home runs', cRank(cReg(c=>c.HR), 1), v=>v),
    ll('RBI', cRank(cReg(c=>c.RBI), 1), v=>v),
    ll('OPS · 150+ PA', cRank(cPool(x=>x.c.PA>=150).map(x=>({n:x.n, v:ops(x.c)})), 1), rate),
    ll('Batting average · 150+ AB', cRank(cPool(x=>x.c.AB>=150).map(x=>({n:x.n, v:x.c.H/x.c.AB})), 1), rate),
    ll('Wins', cRank(cReg(c=>c.W), 1), v=>v),
    ll('Strikeouts', cRank(cReg(c=>c.pK), 1), v=>v),
    ll('ERA · 60+ IP', cRank(cPool(x=>x.c.IPouts>=180).map(x=>({n:x.n, v:era(x.c)})), -1), two, true),
  ].join('');

  // ---- most recent regular season ----
  const LY = Math.max(...NAMES.flatMap(n=>P[n].seasons.filter(s=>s.type==='Regular').map(s=>s.year)));
  const yReg = NAMES.map(n=>({n, s:P[n].seasons.find(s=>s.year===LY && s.type==='Regular' && !s.split)})).filter(x=>x.s);
  const yStat = (f, flt) => yReg.filter(flt||(()=>true)).map(x=>({n:x.n, v:f(x.s)}));
  const yRank = (arr, dir) => withTeam(rank(arr, dir), LY, false);
  const yGrid = [
    ll('Home runs', yRank(yStat(s=>s.HR), 1), v=>v),
    ll('RBI', yRank(yStat(s=>s.RBI), 1), v=>v),
    ll('Runs', yRank(yStat(s=>s.R), 1), v=>v),
    ll('OPS · 9+ G', yRank(yStat(s=>ops(s), x=>x.s.G_bat>=9), 1), rate),
    ll('Batting average · 9+ G', yRank(yStat(s=>avg(s), x=>x.s.G_bat>=9), 1), rate),
    ll('Wins', yRank(yStat(s=>s.W), 1), v=>v),
    ll('Strikeouts', yRank(yStat(s=>s.pK), 1), v=>v),
    ll('ERA · 12+ IP', yRank(yStat(s=>era(s), x=>x.s.IPouts>=36), -1), two, true),
  ].join('');
  const recent = GIDS.slice(0,7).map(id=>{ const g=GAMES[id];
    return `<li><button class="pname" data-g="${id}">${g.date}</button>
      <span>${teamLink(g.away.team)} <b>${g.away.R}–${g.home.R}</b> ${teamLink(g.home.team)}
      ${g.phase!=='Regular'?`<span class="gtag">${esc(gameTag(g))}</span>`:''}</span></li>`; }).join('');
  const rc = CHAMPS[0], rcColor = FRANCHISE_COLORS[rc.tm];
  const champbar = !rc ? '' : rc.photo ? `<div class="herofeature">
      <img class="herophoto" src="${rc.photo}" alt="${esc(rc.full)} — ${rc.y} champions">
      <div class="herocap">
        <span class="herotag">${rc.y} World Series</span>
        <h2>The ${esc(rc.tm)} are ${rc.y} BWB Champions!</h2>
        <p>${rc.score?`${esc(rc.score)} overall on the year, regular season and playoffs combined. `:''}<button class="pname" data-t="${esc(rc.full)}">See the ${esc(rc.tm)} franchise page →</button></p>
      </div>
    </div>` : `<div class="champbar"${rcColor?` style="--tp:${rcColor.p};--ts:${rcColor.s}"`:''}>
      <span class="ring">${TROPHY}</span>
      <span>Reigning champions — <button class="pname" data-t="${esc(rc.full)}">${esc(rc.tm)}</button>${rc.score?` · ${esc(rc.score)} overall`:''}</span>
      <span class="cy">${rc.y} World Series</span>
    </div>`;

  // ---- standings snapshot: top of each division, most recent year with division data ----
  const snapYears = ALL_YEARS.filter(y=>(DB.divisions||{})[y]);
  const snapY = snapYears[snapYears.length-1];
  let standingsSnap = '';
  if(snapY){
    const DIVS = DB.divisions[snapY];
    const divCards = Object.keys(DIVS).map(dn=>{
      const rows = DIVS[dn].map(([tm])=>standRow(tm, snapY)).filter(Boolean)
        .sort((a,b)=>b.PCT-a.PCT || b.DIFF-a.DIFF).slice(0,3);
      const items = rows.map(r=>{
        const logo = teamLogoForYear(r.name, snapY);
        return `<li>${logo?`<img class="snaplogo" src="${logo}" alt="">`:'<span class="snaplogo" style="background:var(--line)"></span>'}
          <button class="pname" data-t="${esc(r.name)}">${esc(histName(r.name,snapY))}</button>
          <b>${recWL(r)}</b></li>`;
      }).join('');
      return `<div class="snapdiv"><h4>${esc(dn)} Division</h4><ol>${items}</ol></div>`;
    }).join('');
    standingsSnap = `<h3 class="hsub">${snapY} Standings${annivBadge()}</h3>
      <div class="snapgrid">${divCards}</div>
      <p class="lead"><button class="pname" data-go="standings">Full standings, any season →</button></p>`;
  }

  // ---- playoff bracket: most recent year with a recorded postseason ----
  const poYears = ALL_YEARS.filter(y=>PLAYOFFS[String(y)]);
  const poY = poYears[poYears.length-1];
  const bracketSnap = poY ? `<h3 class="hsub">${poY} Playoffs</h3>${playoffBracket(poY)}` : '';

  app.innerHTML = `
    ${DB.banner?`<img class="banner" src="${DB.banner}" alt="">`:''}
    ${editBtn('Edit banner','editBannerBtn')}
    ${champbar}
    ${bracketSnap}
    ${standingsSnap}
    <h3 class="hsub">${LY} season leaders</h3>
    <div class="llgrid">${yGrid}</div>
    <h3 class="hsub">Career leaders · regular season</h3>
    <div class="llgrid">${cGrid}</div>
    <h3 class="hsub">Latest games</h3>
    <ul class="recent">${recent}</ul>
    <h3 class="hsub">Follow BWB Wiffleball</h3>
    <div class="followgrid">
      <a class="followcard ig" href="https://www.instagram.com/bwbwiffleball" target="_blank" rel="noopener">
        <span class="fico"><svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.8">
          <rect x="2.5" y="2.5" width="19" height="19" rx="5.5"/><circle cx="12" cy="12" r="4.3"/>
          <circle cx="17.4" cy="6.6" r="1.15" fill="currentColor" stroke="none"/></svg></span>
        <span><b>Instagram</b><span>@bwbwiffleball</span></span>
      </a>
      <a class="followcard yt" href="https://www.youtube.com/@bwbwiffleball" target="_blank" rel="noopener">
        <span class="fico"><svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.8">
          <rect x="2" y="5" width="20" height="14" rx="4.5"/><path d="M10 9.2v5.6l5.1-2.8z" fill="currentColor" stroke="none"/></svg></span>
        <span><b>YouTube</b><span>@bwbwiffleball</span></span>
      </a>
      <a class="followcard pw" href="https://prowiffleball.com/leagues/5" target="_blank" rel="noopener">
        <span class="fico"><svg viewBox="0 0 34 34" width="26" height="26"><rect width="34" height="34" rx="7" fill="#1e4fa8"/>
          <text x="17" y="23" text-anchor="middle" font-family="Arial Black,Arial,sans-serif" font-weight="900"
            font-style="italic" font-size="14" fill="#fff">PRO</text></svg></span>
        <span><b>ProWiffleball</b><span>Live stats &amp; box scores</span></span>
      </a>
    </div>
    <p class="note">Leaders use regular-season totals. Generated ${esc(DB.generated)} from the BWB League Lineup export.</p>`;
  app.querySelectorAll('[data-go]').forEach(b=>b.addEventListener('click',()=>{ location.hash='#/'+b.dataset.go; }));
  app.querySelectorAll('.pname[data-p]').forEach(b=>b.addEventListener('click',()=>{ location.hash='#/p/'+encodeURIComponent(b.dataset.p); }));
  app.querySelectorAll('.pname[data-t]').forEach(b=>b.addEventListener('click',()=>{ location.hash='#/t/'+encodeURIComponent(b.dataset.t); }));
  app.querySelectorAll('.pname[data-g]').forEach(b=>b.addEventListener('click',()=>{ location.hash='#/g/'+b.dataset.g; }));
  app.querySelectorAll('.pname[data-series]').forEach(b=>b.addEventListener('click',()=>{
    const [yy,rk] = b.dataset.series.split('|'); location.hash = '#/series/'+yy+'/'+rk; }));
  document.getElementById('editBannerBtn').addEventListener('click', ()=>{
    openImageEditor('Home Banner', DB.banner, 900, async url=>{
      const before = DB.banner;
      DB.banner = url;
      if(await saveDB()) return true;
      DB.banner = before; return false;
    });
  });
}

function renderDir(){
  setNav('players');
  const cols = mode==='bat'?BAT_COLS:PIT_COLS;
  let rows = NAMES.map(rowVals);
  rows = rows.filter(r => mode==='pit' ? r._ipouts>0 : r._bat>0);
  if(query){ const q=query.toLowerCase(); rows = rows.filter(r=>r.name.toLowerCase().includes(q)); }
  rows.sort((a,b)=>{
    let x=a[sortKey], y=b[sortKey];
    if(sortKey==='name') return sortDir*nameLast(x).localeCompare(nameLast(y));
    if(sortKey==='team') return sortDir*(a.teamCount-b.teamCount) || String(x).localeCompare(String(y));
    if(!isFinite(x)) x=-Infinity; if(!isFinite(y)) y=-Infinity;
    return sortDir*(x-y);
  });
  const th = cols.map(([k,label,t])=>{
    const on = k===sortKey;
    return `<th class="${on?'sorted':''} ${t==='r'?'mono':''} ${t==='s'?'lft':''}" data-k="${k}">${label}${on?`<span class="ar">${sortDir<0?'▼':'▲'}</span>`:''}</th>`;
  }).join('');
  const body = rows.map(r=>'<tr>'+cols.map(([k,label,t],i)=>{
    if(i===0) return `<td class="lft"><button class="pname" data-p="${esc(r.name)}">${esc(r.name)}</button></td>`;
    if(k==='team') return `<td class="lft tm">${teamHistoryChips(P[r.name])}</td>`;
    return `<td class="${t==='r'?'mono':''} ${t==='s'?'lft tm':''}">${cell(r[k],t,k)}</td>`;
  }).join('')+'</tr>').join('');
  const azFiltered = NAMES.filter(n => !query || n.toLowerCase().includes(query.toLowerCase()));
  const azGroups = {};
  azFiltered.forEach(n=>{ const L=(nameParts(n).last[0]||'#').toUpperCase(); (azGroups[L]=azGroups[L]||[]).push(n); });
  const azHtml = Object.keys(azGroups).sort().map(L=>`
    <div class="azgrp"><h3 class="azh">${L}</h3>
      <div class="azcols">${azGroups[L].map(n=>{
        const y=P[n].years, tms=careerTeams(P[n]).map(t=>TEAMS[t.team]?TEAMS[t.team].nick:t.team);
        return `<button class="azitem" data-p="${esc(n)}">
          <span class="azn">${esc(nameLF(n))}</span>
          <span class="azm">${y[0]}${y.length>1?'–'+y[y.length-1]:''}${tms.length?` · ${esc(tms.join('/'))}`:''}</span>
        </button>`;}).join('')}</div>
    </div>`).join('') || '<p class="empty">No players match.</p>';

  app.innerHTML = `
    <div class="controls">
      <div class="search">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/></svg>
        <input id="q" type="search" placeholder="Search players…" value="${esc(query)}">
      </div>
      <div class="segs" role="group" aria-label="View">
        <button data-pv="stats" aria-pressed="${pView==='stats'}">Stats</button>
        <button data-pv="az" aria-pressed="${pView==='az'}">A–Z</button>
      </div>
      ${pView==='stats'?`
      <div class="segs post" role="group" aria-label="Phase">
        <button data-ph="reg" aria-pressed="${phase==='reg'}">Regular</button>
        <button data-ph="post" aria-pressed="${phase==='post'}">Postseason</button>
      </div>
      <div class="segs" role="group" aria-label="Stat group">
        <button data-m="bat" aria-pressed="${mode==='bat'}">Batting</button>
        <button data-m="pit" aria-pressed="${mode==='pit'}">Pitching</button>
      </div>`:''}
      <button class="pname" id="cmpLink">Compare Players →</button>
    </div>
    ${pView==='az' ? `<div class="azindex">${azHtml}</div>` : `
    <div class="tscroll"><table class="dir">
      <thead><tr>${th}</tr></thead>
      <tbody>${body || '<tr><td colspan="'+cols.length+'" class="empty">No players match.</td></tr>'}</tbody>
    </table></div>`}
    <p class="note" id="footnote"></p>`;
  footnote();
  document.getElementById('cmpLink').addEventListener('click',()=>{ location.hash='#/compare'; });
  const qi = document.getElementById('q');
  qi.addEventListener('input',e=>{ query=e.target.value; const p=qi.selectionStart; renderDir();
    const n=document.getElementById('q'); n.focus(); n.setSelectionRange(p,p); });
  app.querySelectorAll('.segs [data-pv]').forEach(b=>b.addEventListener('click',()=>{
    if(pView!==b.dataset.pv){ pView=b.dataset.pv; renderDir(); }
  }));
  app.querySelectorAll('.azitem').forEach(b=>b.addEventListener('click',()=>{
    location.hash='#/p/'+encodeURIComponent(b.dataset.p);
  }));
  app.querySelectorAll('.segs [data-ph]').forEach(b=>b.addEventListener('click',()=>{
    if(phase!==b.dataset.ph){ phase=b.dataset.ph; renderDir(); }
  }));
  app.querySelectorAll('.segs [data-m]').forEach(b=>b.addEventListener('click',()=>{
    if(mode===b.dataset.m) return;
    mode=b.dataset.m;
    const batKeys=['PA','AB','H','HR','RBI','AVG','OBP','SLG','OPS','OPS+'];
    const pitKeys=['IP','W','L','SV','pH','ER','pBB','pK','ERA','WHIP','K9','ERA+'];
    if(mode==='pit' && batKeys.includes(sortKey)) sortKey='W';
    if(mode==='bat' && pitKeys.includes(sortKey)) sortKey='HR';
    sortDir=-1; renderDir();
  }));
  app.querySelectorAll('thead th').forEach(h=>h.addEventListener('click',()=>{
    const k=h.dataset.k;
    if(k===sortKey) sortDir*=-1; else { sortKey=k; sortDir = k==='name'?1:-1; }
    renderDir();
  }));
  app.querySelectorAll('.pname[data-p]').forEach(b=>b.addEventListener('click',()=>{
    location.hash = '#/p/'+encodeURIComponent(b.dataset.p);
  }));
  app.querySelectorAll('.pname[data-t]').forEach(b=>b.addEventListener('click',()=>{
    location.hash = '#/t/'+encodeURIComponent(b.dataset.t);
  }));
}

function footnote(){
  const fn = document.getElementById('footnote'); if(!fn) return;
  fn.innerHTML = `<b>About this register.</b> Regular season and postseason are kept separate throughout — the
  toggle above switches the leaderboard between them, and every player page carries each phase, plus the
  exhibition sets (All-Star, spring training, fall ball), as its own block. Spans ${RANGE}.
  Rates: AVG / OBP / SLG standard, OPS = OBP + SLG. BWB games run 3 innings, so <b>ERA</b> is earned runs
  per 3 IP — a full game — and <b>K/3</b> is strikeouts on the same basis; WHIP is baserunners per inning.
  IP is shown as whole.thirds (.1 = ⅓, .2 = ⅔); rate stats use exact thirds, not the printed decimal.
  Fielding % = (PO + A) / TC.
  <br><b>Team</b> comes from the league's player-roster lookup, matched per registration; a season with two
  entries shows both clubs (Team A / Team B). <span class="pt">*</span> marks the handful of early
  registrations with no roster row, where the club is estimated from game appearances. The 2017 season was
  logged with first names only; those records have been matched to the right player by the league.
  <br>Generated ${esc(DB.generated)} from the BWB League Lineup export.`;
}

/* ---------------- player detail ---------------- */
const slash = d => `${rate(avg(d))}/${rate(obp(d))}/${rate(slg(d))}`;
const wl = d => `${d.W}–${d.L}`;

const ZERO_KEYS = ['G_bat','GS_bat','AB','R','1B','2B','3B','HR','RBI','BB','K','HBP','SB','CS','SF','SH',
  'H','TB','PA','G_pit','IPouts','pR','ER','pH','pBB','pHB','pK','CG','W','L','SV','BS',
  'G_fld','INN','TC','PO','A','E','DP'];
function sumRows(rows){
  const t = {}; for(const k of ZERO_KEYS) t[k]=0;
  for(const d of rows) for(const k of ZERO_KEYS) t[k]+=(d[k]||0);
  return t;
}
/* OPS+ is always season-specific: every player-season's OBP/SLG is compared
   to THAT season's own league average, never a blended or all-time figure.
   LEAGUE_BY_YEAR[type][year] is that year's combined batting line across
   every player who recorded one, built the same way a team's own per-year
   total is (sum every non-"tot" row so a split season counts once). Regular
   and Playoffs get their own tables since the two pools of games (and thus
   league averages) aren't the same; any other phase (All-Star, Spring,
   Fall, NWLA) falls back to that year's Regular-season table on the
   reasoning that exhibition rosters are drawn from the same player pool. */
function buildLeagueByYear(type){
  const byYear = {};
  NAMES.forEach(n=>P[n].seasons.forEach(s=>{
    if(s.type===type && !s.tot) (byYear[s.year] = byYear[s.year] || []).push(s);
  }));
  const out = {};
  Object.keys(byYear).forEach(y=>{ out[y] = sumRows(byYear[y]); });
  return out;
}
const LEAGUE_BY_YEAR = buildLeagueByYear('Regular');
const LEAGUE_BY_YEAR_POST = buildLeagueByYear('Playoffs');
function leagueRatesFor(year, post){
  const lg = (post ? LEAGUE_BY_YEAR_POST[year] : null) || LEAGUE_BY_YEAR[year];
  return lg ? {obp:obp(lg), slg:slg(lg), era:era(lg)} : null;
}
/* OPS+ for a stat bucket, normalized against a PA-weighted blend of the
   league averages for whichever year(s) contributed to it. `weights` is
   an array of {year, pa[, post]} — for a single season that's one entry
   (so the "blend" is just that year's own league average); for a career
   or any other multi-year bucket it's one entry per year the player
   actually had plate appearances, weighted by how many — a year a player
   barely played contributes little to their own baseline, same as a real
   career OPS+'s weighted league average. */
function opsPlusFor(d, weights){
  let wObp=0, wSlg=0, totPA=0;
  (weights||[]).forEach(w=>{
    const r = w && w.pa ? leagueRatesFor(w.year, w.post) : null;
    if(!r) return;
    wObp += r.obp*w.pa; wSlg += r.slg*w.pa; totPA += w.pa;
  });
  if(!totPA || !d || !d.AB) return NaN;
  const lo = wObp/totPA, ls = wSlg/totPA;
  return (lo && ls) ? Math.round(100*(obp(d)/lo + slg(d)/ls - 1)) : NaN;
}
/* the {year,pa} weights for one player's own career (or postseason career) —
   the shared shape opsPlusFor needs, reused everywhere a "career OPS+" is shown */
function careerWeights(pl, post){
  return pl.seasons.filter(s=>s.type===(post?'Playoffs':'Regular') && !s.tot && s.PA)
    .map(s=>({year:s.year, pa:s.PA, post}));
}
/* ERA+ is OPS+'s pitching mirror: 100 * (that season's league ERA / the
   player's own ERA), blended across whichever year(s) contributed —
   weighted by innings (outs) instead of PA, everything else identical to
   opsPlusFor's reasoning (a single-season bucket is just that year's own
   league rate; a career blends every year the player actually pitched,
   weighted by how much). A perfect 0.00 ERA sample makes this mathematically
   infinite — left as Infinity rather than special-cased, since every
   display site already falls back to "—" for a non-finite value exactly
   like they do for OPS+. */
function eraPlusFor(d, weights){
  let wEra=0, totOuts=0;
  (weights||[]).forEach(w=>{
    const r = w && w.outs ? leagueRatesFor(w.year, w.post) : null;
    if(!r) return;
    wEra += r.era*w.outs; totOuts += w.outs;
  });
  if(!totOuts || !d || !d.IPouts) return NaN;
  const le = wEra/totOuts;
  return le ? Math.round(100*(le/era(d))) : NaN;
}
function careerWeightsPit(pl, post){
  return pl.seasons.filter(s=>s.type===(post?'Playoffs':'Regular') && !s.tot && s.IPouts)
    .map(s=>({year:s.year, outs:s.IPouts, post}));
}

/* ============================== LIVE EDITING ==============================
   Owner-only editing via the `artifact` capability. An edit mutates the
   in-memory DB object, then the WHOLE page is republished with the updated
   data blob spliced in — every render function above keeps reading DB/P/
   TEAMS exactly as before; only the bootstrap and this section change. A
   viewer who isn't the owner gets `not_writer`/`not_granted` from the
   platform itself when they try to save — that's the real access control,
   not just hiding buttons. */
let ARTIFACT_CAP = null, EDIT_READONLY = false;
(async () => {
  try{ ARTIFACT_CAP = window.claude && window.claude.use ? await window.claude.use('artifact') : null; }
  catch(e){ ARTIFACT_CAP = null; }
  if(ARTIFACT_CAP) document.querySelectorAll('.editbtn[hidden]').forEach(b=>b.hidden = false);
})();
const editBtn = (label, id) => `<button class="editbtn" id="${id}" ${ARTIFACT_CAP?'':'hidden'}>✎ ${esc(label)}</button>`;

function closeModal(){ const m = document.getElementById('editModal'); if(m) m.remove(); }
function openModal(title, bodyHtml){
  closeModal();
  const wrap = document.createElement('div');
  wrap.id = 'editModal'; wrap.className = 'modalwrap';
  wrap.innerHTML = `<div class="modal"><div class="modalhead"><h3>${esc(title)}</h3>
    <button class="modalx" id="modalx" aria-label="Close">✕</button></div>
    <div class="modalbody">${bodyHtml}</div></div>`;
  document.body.appendChild(wrap);
  wrap.addEventListener('click', e=>{ if(e.target===wrap) closeModal(); });
  document.getElementById('modalx').addEventListener('click', closeModal);
  return wrap;
}

/* Splice the updated DB into a fresh copy of this page's own source and
   publish it. Never serialize the live DOM (it carries routed-page state) —
   fetch this artifact's own pristine markup instead and edit only the data
   script tag. A successful publish reloads this view with the new data. */
async function saveDB(){
  if(!ARTIFACT_CAP){ alert("Editing isn't available in this view — open the artifact from Claude to edit."); return false; }
  const btns = document.querySelectorAll('.modal .saveRow, .modal .saveBtn, .modal .delRow');
  btns.forEach(b=>b.disabled = true);
  try{
    const res = await fetch(location.href, {cache:'no-store'});
    if(!res.ok) throw new Error('could not reload this page (HTTP '+res.status+')');
    const html = await res.text();
    const openTag = '<script id="data" type="application/json">';
    const start = html.indexOf(openTag);
    const openEnd = start + openTag.length;
    const end = start<0 ? -1 : html.indexOf('<'+'/script>', openEnd);
    if(start<0 || end<0) throw new Error('could not find the data block in this page');
    const newHtml = html.slice(0, openEnd) + JSON.stringify(DB) + html.slice(end);
    await ARTIFACT_CAP.publish(newHtml);
    return true;
  }catch(e){
    const code = e && e.code;
    if(code==='not_writer' || code==='not_granted' || code==='consent_required'){
      EDIT_READONLY = true;
      document.querySelectorAll('.editbtn').forEach(b=>b.hidden = true);
      closeModal();
      alert("This copy is read-only for you — only the site's owner can save edits.");
    } else if(code==='conflict'){
      alert('Someone else saved a change just now — reloading to the latest version. Please redo your edit.');
    } else {
      alert('Save failed: ' + ((e && e.message) || e));
      btns.forEach(b=>b.disabled = false);
    }
    return false;
  }
}

/* ---- player season-row editor ---- */
function recomputePlayer(pl){
  const live = pl.seasons.filter(s=>!s.split);
  pl.career = sumRows(live);
  pl.careerReg = sumRows(live.filter(s=>s.type==='Regular'));
  pl.careerPO = sumRows(live.filter(s=>s.type==='Playoffs'));
  pl.years = [...new Set(pl.seasons.map(s=>s.year))].sort((a,b)=>a-b);
  const tby = {};
  pl.years.forEach(y=>{
    const rows = live.filter(s=>s.year===y);
    const pick = rows.find(s=>s.type==='Regular') || rows.find(s=>s.type==='Playoffs') || rows[0];
    tby[y] = pick ? {team: pick.team, partial: !!pick.teamPartial} : {team:null, partial:false};
  });
  pl.teamsByYear = tby;
}
const SEASON_TYPES = ['Regular','Playoffs','AllStar','Spring','Fall','Exhib','NWLA'];
const EDIT_BAT = [['G_bat','G'],['GS_bat','GS'],['AB','AB'],['R','R'],['1B','1B'],['2B','2B'],
  ['3B','3B'],['HR','HR'],['RBI','RBI'],['BB','BB'],['K','K'],['HBP','HBP'],['SB','SB'],['CS','CS'],
  ['SF','SF'],['SH','SH']];
const EDIT_PIT = [['G_pit','G'],['pR','R'],['ER','ER'],['pH','H'],['pBB','BB'],['pHB','HB'],
  ['pK','K'],['CG','CG'],['W','W'],['L','L'],['SV','SV'],['BS','BS']];
const EDIT_FLD = [['G_fld','G'],['INN','INN'],['TC','TC'],['PO','PO'],['A','A'],['E','E'],['DP','DP']];
const numField = (row,key,label) => `<label class="ef"><span>${esc(label)}</span>
  <input type="number" step="1" data-k="${key}" value="${row[key]||0}"></label>`;
function seasonRowForm(row, idx){
  const ip = Math.floor((row.IPouts||0)/3), thirds = (row.IPouts||0)%3;
  return `<div class="editrow" data-idx="${idx}">
    <div class="ef3">
      <label class="ef"><span>Year</span><input type="number" step="1" data-k="year" value="${row.year}"></label>
      <label class="ef"><span>Type</span><select data-k="type">${SEASON_TYPES.map(t=>
        `<option value="${t}" ${t===row.type?'selected':''}>${t}</option>`).join('')}</select></label>
      <label class="ef"><span>Team</span><input list="teamlist" data-k="team" value="${esc(row.team||'')}"></label>
    </div>
    <h5>Batting</h5><div class="efgrid">${EDIT_BAT.map(([k,l])=>numField(row,k,l)).join('')}</div>
    <h5>Pitching<span class="efsub">IP <input type="number" step="1" min="0" data-k="_ip" value="${ip}" style="width:3.2em"> . <input type="number" step="1" min="0" max="2" data-k="_thirds" value="${thirds}" style="width:2.6em"></span></h5>
    <div class="efgrid">${EDIT_PIT.map(([k,l])=>numField(row,k,l)).join('')}</div>
    <h5>Fielding</h5><div class="efgrid">${EDIT_FLD.map(([k,l])=>numField(row,k,l)).join('')}</div>
    <div class="editrowbtns">
      <button class="saveRow" data-idx="${idx}">Save row</button>
      <button class="delRow" data-idx="${idx}">Delete row</button>
    </div>
  </div>`;
}
function readSeasonForm(el){
  const row = {};
  el.querySelectorAll('[data-k]').forEach(inp=>{
    const k = inp.dataset.k;
    if(k==='_ip' || k==='_thirds') return;
    if(k==='year') row.year = +inp.value;
    else if(k==='type') row.type = inp.value;
    else if(k==='team') row.team = inp.value.trim() || null;
    else row[k] = +inp.value || 0;
  });
  row.H = (row['1B']||0)+(row['2B']||0)+(row['3B']||0)+(row.HR||0);
  row.TB = (row['1B']||0)+2*(row['2B']||0)+3*(row['3B']||0)+4*(row.HR||0);
  row.PA = (row.AB||0)+(row.BB||0)+(row.HBP||0)+(row.SF||0)+(row.SH||0);
  row.IPouts = (+el.querySelector('[data-k="_ip"]').value||0)*3 + (+el.querySelector('[data-k="_thirds"]').value||0);
  row.teamPartial = false;
  return row;
}
function rowSummary(r){
  return `${r.year} · ${esc(r.type)}${r.team?' · '+esc(r.team):''}${r.split?' (split)':r.tot?' (2TM total)':''}`;
}
function openSeasonEditor(pl){
  const teamOptions = `<datalist id="teamlist">${TEAMNAMES.map(t=>`<option value="${esc(t)}">`).join('')}</datalist>`;
  const wrap = openModal(`Edit Seasons — ${pl.name}`, `${teamOptions}
    <p class="pmeta">Corrects a season's aggregate stat line. H, TB, PA and IP-outs are derived
    automatically from what you enter here; this doesn't touch box scores or game logs.</p>
    <div id="seasonRows"></div>
    <button class="saveBtn" id="addSeasonRow">+ Add a season row</button>`);
  function render(){
    document.getElementById('seasonRows').innerHTML = pl.seasons.map((r,i)=>
      `<details class="editrowd"><summary>${rowSummary(r)}</summary>${seasonRowForm(r,i)}</details>`).join('');
    wrap.querySelectorAll('.saveRow').forEach(b=>b.addEventListener('click', async ()=>{
      const before = pl.seasons.slice();
      pl.seasons[+b.dataset.idx] = readSeasonForm(b.closest('.editrow'));
      recomputePlayer(pl);
      if(!await saveDB()){ pl.seasons = before; recomputePlayer(pl); render(); }
    }));
    wrap.querySelectorAll('.delRow').forEach(b=>b.addEventListener('click', async ()=>{
      if(!confirm('Delete this season row?')) return;
      const before = pl.seasons.slice();
      pl.seasons.splice(+b.dataset.idx, 1);
      recomputePlayer(pl);
      if(!await saveDB()){ pl.seasons = before; recomputePlayer(pl); render(); }
    }));
  }
  render();
  document.getElementById('addSeasonRow').addEventListener('click', ()=>{
    const blank = {year: new Date().getFullYear(), type:'Regular', team:null, teamPartial:false};
    ZERO_KEYS.forEach(k=>blank[k]=0);
    pl.seasons.push(blank);
    render();
  });
}

/* ---- image editing: logos, photos, banners — embedded as data URIs so the
   page stays publicly shareable (no assets capability, which would make the
   artifact org-internal). Resized/recompressed client-side to keep the
   whole page under the artifact size cap regardless of what gets uploaded. */
function resizeImageFile(file, maxDim, quality){
  return new Promise((resolve, reject)=>{
    const reader = new FileReader();
    reader.onerror = () => reject(new Error('could not read that file'));
    reader.onload = () => {
      const img = new Image();
      img.onerror = () => reject(new Error('could not decode that image'));
      img.onload = () => {
        const scale = Math.min(1, maxDim / Math.max(img.width, img.height));
        const w = Math.max(1, Math.round(img.width*scale)), h = Math.max(1, Math.round(img.height*scale));
        const cv = document.createElement('canvas');
        cv.width = w; cv.height = h;
        cv.getContext('2d').drawImage(img, 0, 0, w, h);
        resolve(cv.toDataURL('image/jpeg', quality));
      };
      img.src = reader.result;
    };
    reader.readAsDataURL(file);
  });
}
function openImageEditor(title, currentUrl, maxDim, onSave){
  let pending = currentUrl || null;
  const body = `<div class="imgedit">
    <div class="imgpreview" id="imgPreview">${pending?`<img src="${pending}">`:'<span class="imgph">No image yet</span>'}</div>
    <input type="file" accept="image/*" id="imgPick">
    <p class="pmeta">Resized and recompressed in your browser before saving, so it stays small — the whole
    page (all stats, every image) has to fit under one size limit.</p>
    <div class="editrowbtns">
      <button class="saveBtn" id="imgSaveBtn">Save</button>
      ${currentUrl?'<button class="delRow" id="imgRemoveBtn">Remove image</button>':''}
    </div>
  </div>`;
  openModal(title, body);
  document.getElementById('imgPick').addEventListener('change', async e=>{
    const f = e.target.files[0]; if(!f) return;
    try{
      pending = await resizeImageFile(f, maxDim, 0.75);
      document.getElementById('imgPreview').innerHTML = `<img src="${pending}">`;
    }catch(err){ alert("Couldn't use that image: " + err.message); }
  });
  document.getElementById('imgSaveBtn').addEventListener('click', async ()=>{
    if(!pending){ alert('Pick an image first.'); return; }
    if(await onSave(pending)) closeModal();
  });
  const rm = document.getElementById('imgRemoveBtn');
  if(rm) rm.addEventListener('click', async ()=>{
    if(!confirm('Remove this image?')) return;
    if(await onSave(null)) closeModal();
  });
}

/* column spec: {l label, m mono?, f value fn, lft left-align?, noTot blank in totals row, cls extra td/th class} */
function statTable(title, cols, rows, career, totLabel, cls, sortable){
  const lft = c => (c.lft || ['Season','Tm','Player','Opp','Date'].includes(c.l)) ? 'lft' : '';
  const cc = c => `${c.m?'mono':''} ${lft(c)} ${c.cls||''}`;
  const th = cols.map(c=>`<th class="${cc(c)}">${c.l}</th>`).join('');
  const tr = d => `<tr class="${d.tot?'totrow':d.split?'splitrow':''}${d.est?' estrow':''}">`+cols.map(c=>`<td class="${cc(c)}">${c.f(d)}</td>`).join('')+'</tr>';
  const foot = '<tr>'+cols.map((c,i)=>`<td class="${cc(c)}">${i===0?totLabel:(c.noTot?'':c.f(career))}</td>`).join('')+'</tr>';
  return `<section class="stat ${cls||''}"><h4>${title}</h4><div class="tscroll"><table class="detail${sortable?' sortable':''}">
    <thead><tr>${th}</tr></thead>
    <tbody>${rows.map(tr).join('')}</tbody>
    <tfoot>${foot}</tfoot>
  </table></div></section>`;
}
/* click-to-sort for tables with no inherent row order (rosters, leaderboard-style) */
function makeSortable(tbl){
  if(tbl.dataset.sortWired) return; tbl.dataset.sortWired = '1';
  const heads = [...tbl.tHead.rows[0].cells];
  const body = tbl.tBodies[0];
  heads.forEach((th, ci)=>{
    th.classList.add('sortcol');
    th.addEventListener('click', ()=>{
      const dir = th.dataset.dir === 'desc' ? 'asc' : 'desc';
      heads.forEach(h=>{ h.removeAttribute('data-dir'); const a=h.querySelector('.ar'); if(a) a.remove(); });
      th.dataset.dir = dir;
      const num = t => { const m = String(t).replace(/[,–—%]/g,'').match(/-?\d+\.?\d*/); return m?parseFloat(m[0]):NaN; };
      const rows = [...body.rows];
      rows.sort((r1,r2)=>{
        const a=(r1.cells[ci]||{}).textContent||'', b=(r2.cells[ci]||{}).textContent||'';
        const na=num(a), nb=num(b);
        const cmp = (!isNaN(na)&&!isNaN(nb)) ? na-nb : a.trim().toLowerCase().localeCompare(b.trim().toLowerCase());
        return dir==='asc' ? cmp : -cmp;
      });
      rows.forEach(r=>body.appendChild(r));
      const ar = document.createElement('span'); ar.className='ar'; ar.textContent = dir==='desc'?' ▼':' ▲';
      th.appendChild(ar);
    });
  });
}

const PHASE_META = {
  Regular:  {cls:'',      head:'Regular Season', tot:'Regular',     unit:'year'},
  Playoffs: {cls:'post',  head:'Postseason',     tot:'Postseason',  unit:'year'},
  AllStar:  {cls:'exh',   head:'All-Star Games', tot:'All-Star',    unit:'appearance'},
  Spring:   {cls:'exh',   head:'Spring Training',tot:'Spring',      unit:'year'},
  Fall:     {cls:'exh',   head:'Fall Ball',      tot:'Fall',        unit:'year'},
  Exhib:    {cls:'exh',   head:'Exhibition',     tot:'Exhibition', unit:'appearance'},
  NWLA:     {cls:'exh',   head:'NWLA Tournament',tot:'NWLA',        unit:'appearance'},
};

const AW_ABBR = {
  'MVP':'MVP', 'CY Young':'CYA', 'Rookie of the Year':'RoY', 'Batting Title':'BT',
  'Home Run King':'HRK', 'Comeback Player of the Year':'CPoY', 'Golden Hands':'GH',
  'Silver Slugger':'SS', 'Reliever of the Year':'RoR', 'Manager of the Year':'MgrY',
  'Postseason MVP':'PoMVP',
};
function yearAwards(pl, y){
  const h = pl.honors || {rings:[],awards:[],asg:[]};
  const out = [];
  if(h.rings.some(r=>r.year===y)) out.push('WS');
  h.awards.filter(a=>a.year===y).forEach(a=>{ const ab=AW_ABBR[a.award]; if(ab && !out.includes(ab)) out.push(ab); });
  if(h.asg.some(s=>s.year===y)) out.push('AS');
  return out.join(', ');
}

function phaseBlock(pl, type){
  const rows = byYear(pl, type);
  if(!rows.length) return '';
  const meta = PHASE_META[type];
  const career = sumRows(rows.filter(d=>!d.split));   // split rows would double-count
  const yrs = yearsOf(pl, type);
  const seasonCols = [{l:'Season',f:d=>d.year+(d.est?'<span class="estd" title="estimated">†</span>':'')},{l:'Tm',f:teamCell,noTot:1}];
  const awCol = type==='Regular'
    ? [{l:'Awards',lft:1,noTot:1,cls:'awc',f:d=>d.split?'':yearAwards(pl,d.year)}] : [];

  const batCols = [...seasonCols,
    {l:'G',f:d=>d.G_bat},{l:'PA',f:d=>d.PA},{l:'AB',f:d=>d.AB},{l:'R',f:d=>d.R},
    {l:'H',f:d=>d.H},{l:'2B',f:d=>d['2B']},{l:'3B',f:d=>d['3B']},{l:'HR',f:d=>d.HR},
    {l:'RBI',f:d=>d.RBI},{l:'BB',f:d=>d.BB},{l:'K',f:d=>d.K},{l:'HBP',f:d=>d.HBP},
    {l:'AVG',m:1,f:d=>rate(avg(d))},{l:'OBP',m:1,f:d=>rate(obp(d))},
    {l:'SLG',m:1,f:d=>rate(slg(d))},{l:'OPS',m:1,f:d=>rate(ops(d))},
    {l:'OPS+',m:1,f:d=>{
      const v = d.year!=null
        ? opsPlusFor(d, [{year:d.year, pa:d.PA, post:type==='Playoffs'}])
        : opsPlusFor(d, rows.filter(r=>!r.split).map(r=>({year:r.year, pa:r.PA, post:type==='Playoffs'})));
      return isFinite(v)?String(v):'—';
    }}, ...awCol];
  const bat = statTable('Batting', batCols, rows, career, meta.tot, meta.cls);

  let pit='';
  if(career.IPouts>0){
    const pitCols = [...seasonCols,
      {l:'G',f:d=>d.G_pit},{l:'IP',m:1,f:d=>ipStr(d.IPouts)},{l:'W',f:d=>d.W},{l:'L',f:d=>d.L},
      {l:'SV',f:d=>d.SV},{l:'CG',f:d=>d.CG},{l:'H',f:d=>d.pH},{l:'R',f:d=>d.pR},{l:'ER',f:d=>d.ER},
      {l:'BB',f:d=>d.pBB},{l:'K',f:d=>d.pK},
      {l:'ERA',m:1,f:d=>two(era(d))},{l:'WHIP',m:1,f:d=>two(whip(d))},{l:'K/3',m:1,f:d=>two(k9(d))},
      {l:'ERA+',m:1,f:d=>{
        const v = d.year!=null
          ? eraPlusFor(d, [{year:d.year, outs:d.IPouts, post:type==='Playoffs'}])
          : eraPlusFor(d, rows.filter(r=>!r.split).map(r=>({year:r.year, outs:r.IPouts, post:type==='Playoffs'})));
        return isFinite(v)?String(v):'—';
      }}, ...awCol];
    pit = statTable('Pitching', pitCols, rows.filter(d=>d.IPouts>0), career, meta.tot, meta.cls);
  }

  let fldT='';
  if(career.TC>0 || career.G_fld>0){
    const fCols = [...seasonCols,
      {l:'G',f:d=>d.G_fld},{l:'INN',f:d=>d.INN},{l:'TC',f:d=>d.TC},{l:'PO',f:d=>d.PO},
      {l:'A',f:d=>d.A},{l:'E',f:d=>d.E},{l:'DP',f:d=>d.DP},{l:'FLD%',m:1,f:d=>rate(fld(d))}];
    fldT = statTable('Fielding', fCols, rows.filter(d=>d.TC>0||d.G_fld>0), career, meta.tot, meta.cls);
  }
  const span = yrs.length>1 ? `${yrs[0]}–${yrs[yrs.length-1]}` : `${yrs[0]}`;
  /* Exhibition is a generic phase that can hold several one-off named events
     (Brookside Field Finale, and whatever comes after it) — name the specific
     event(s) actually played, read straight off those games' own `div` field
     rather than hardcoded, so a second event just shows up correctly too. */
  let evNote = '';
  if(type==='Exhib'){
    const evs = [...new Set(collectPlayerGames(pl, type).map(r=>r.g.div).filter(Boolean))]
      .map(d=>d.replace(/^\d{4}\s+/, ''));
    if(evs.length) evNote = ' · ' + evs.map(esc).join(', ');
  }
  return `<div class="phase ${meta.cls}">
    <h3>${meta.head}</h3>
    <p class="pmeta">${yrs.length} ${meta.unit}${yrs.length>1?'s':''} · ${span}${evNote}</p>
    ${bat}${pit}${fldT}</div>`;
}

/* ---- Baseball-Savant-style percentile rankings (per regular season) ---- */
const SV_MING = 9, SV_MINOUTS = 36;   // 9+ G batting, 12+ IP pitching (per season) — the qualified pool
/* below full qualification, still show a faded/patterned percentile estimate down to this floor —
   never adds these players into the qualified pool itself (qb/qp below stay built off SV_MING/SV_MINOUTS
   alone), just plots where they'd land against it. 3 G batting, 3 IP (9 outs) pitching. */
const SV_MIN_SHOW_G = 3, SV_MIN_SHOW_OUTS = 9;
let svYear = null;                     // sticky across player pages
function svColor(p){
  const t = Math.max(0,Math.min(100,p))/100;
  const blue=[59,98,176], grey=[201,205,214], red=[210,45,73];
  const mix=(a,b,u)=>a.map((x,i)=>Math.round(x+(b[i]-x)*u));
  const c = t<0.5 ? mix(blue,grey,t*2) : mix(grey,red,(t-0.5)*2);
  return `rgb(${c[0]},${c[1]},${c[2]})`;
}
function svPct(vals, val, lowerBetter){
  const n = vals.length; if(!n || !isFinite(val)) return null;
  let below=0, equal=0;
  vals.forEach(v=>{ if(v<val) below++; else if(v===val) equal++; });
  let p = (below + equal/2)/n;
  if(lowerBetter) p = 1-p;
  return Math.round(p*100);
}
const SV_ISO = c => slg(c) - (avg(c)||0);
const SV_BF  = c => c.IPouts + c.pH + c.pBB + c.pHB;   // outs + H + BB + HBP allowed ≈ batters faced
const SV_PCTF = v => (v*100).toFixed(1)+'%';
const SV_BAT = [
  ['AVG', c=>avg(c), rate, false], ['OBP', c=>obp(c), rate, false],
  ['SLG', c=>slg(c), rate, false],
  ['OPS+', c=>opsPlusFor(c, [{year:c.year, pa:c.PA}]), v=>isFinite(v)?String(v):'—', false],
  ['ISO', SV_ISO, rate, false], ['BB%', c=>c.PA?c.BB/c.PA:NaN, SV_PCTF, false],
  ['K%',  c=>c.PA?c.K/c.PA:NaN,  SV_PCTF, true], ['HR%', c=>c.PA?c.HR/c.PA:NaN, SV_PCTF, false],
];
const SV_PIT = [
  ['ERA', c=>era(c), two, true], ['WHIP', c=>whip(c), two, true],
  ['K/3', c=>k9(c), two, false], ['BB/3', c=>c.IPouts?3*c.pBB/(c.IPouts/3):NaN, two, true],
  ['K%',  c=>SV_BF(c)?c.pK/SV_BF(c):NaN, SV_PCTF, false],
  ['BB%', c=>SV_BF(c)?c.pBB/SV_BF(c):NaN, SV_PCTF, true],
  ['K-BB%', c=>SV_BF(c)?(c.pK-c.pBB)/SV_BF(c):NaN, SV_PCTF, false],
  ['OPP AVG', c=>(c.IPouts+c.pH)?c.pH/(c.IPouts+c.pH):NaN, rate, true],
];
/* one non-split Regular row per year for a player */
function svRegRow(pl, y){
  return pl.seasons.find(s=>s.type==='Regular' && !s.split && s.year===y) || null;
}
function svSeasons(pl){
  return [...new Set(pl.seasons.filter(s=>s.type==='Regular'&&!s.split).map(s=>s.year))]
    .sort((a,b)=>a-b);
}
/* unqualified: this subject falls short of the real qualification bar, so
   the percentile is an estimate against the qualified pool rather than a
   real ranking — pool itself is untouched either way (the subject was never
   in it, qualified or not), only the row's own look changes. */
function svPanel(title, metrics, subject, pool, unqualified){
  const rows = metrics.map(([lab,fn,fmt,low])=>{
    const p = svPct(pool.map(fn).filter(isFinite), fn(subject), low);
    if(p==null) return '';
    return `<div class="svrow${unqualified?' svunq':''}"><span class="svlab">${lab}</span>
      <span class="svbar"><span class="svdot" style="left:${p}%;background:${svColor(p)}">${p}</span></span>
      <span class="svval">${fmt(fn(subject))}</span></div>`;
  }).join('');
  const titleHTML = unqualified ? `${esc(title)} <span class="svunqtag">est. · unqualified</span>` : esc(title);
  return rows ? `<div class="svpanel${unqualified?' svpanel-unq':''}"><h4>${titleHTML}</h4>${rows}</div>` : '';
}
function savantInner(pl){
  const yrs = svSeasons(pl);
  if(!yrs.length) return '<p class="smeta">No regular-season data.</p>';
  if(svYear==null || !yrs.includes(svYear)){
    const q = yrs.filter(y=>{ const r=svRegRow(pl,y); return r && (r.G_bat>=SV_MING || r.IPouts>=SV_MINOUTS); });
    svYear = (q.length?q:yrs).slice(-1)[0];
  }
  const chips = `<div class="chips svchips">${yrs.map(y=>
    `<button data-svy="${y}" aria-pressed="${y===svYear}">${y}</button>`).join('')}</div>`;
  const row = svRegRow(pl, svYear);
  const seasonRows = NAMES.map(n=>svRegRow(P[n], svYear)).filter(Boolean);
  const qb = seasonRows.filter(r=>r.G_bat>=SV_MING);
  const qp = seasonRows.filter(r=>r.IPouts>=SV_MINOUTS);
  const batOK = row && row.G_bat>=SV_MING, pitOK = row && row.IPouts>=SV_MINOUTS;
  const batShow = row && !batOK && row.G_bat>=SV_MIN_SHOW_G;
  const pitShow = row && !pitOK && row.IPouts>=SV_MIN_SHOW_OUTS;
  const panels = (batOK ? svPanel(`Batting · vs ${qb.length}`, SV_BAT, row, qb)
      : batShow ? svPanel(`Batting · vs ${qb.length}`, SV_BAT, row, qb, true) : '')
    + (pitOK ? svPanel(`Pitching · vs ${qp.length}`, SV_PIT, row, qp)
      : pitShow ? svPanel(`Pitching · vs ${qp.length}`, SV_PIT, row, qp, true) : '');
  if(!panels){
    return `${chips}<p class="smeta">No ${svYear} regular season line long enough to estimate
      (${SV_MIN_SHOW_G}+ G batting or ${SV_MIN_SHOW_OUTS/3}+ IP pitching needed at minimum).</p>`;
  }
  const twoUp = ((batOK||batShow) && (pitOK||pitShow)) ? ' two' : '';
  const anyUnq = batShow || pitShow;
  return `${chips}
    <p class="smeta">${svYear} regular season, percentile vs qualified players (${SV_MING}+ G batting,
      ${SV_MINOUTS/3}+ IP pitching) · <span style="color:${svColor(100)}">red</span> = league-best,
      <span style="color:${svColor(0)}">blue</span> = trailing.
      K%, BB%, ERA, WHIP, BB/3, OPP AVG ranked low-is-better.
      ${anyUnq?` Faded, dashed rows are below the qualification bar — shown as an estimate against the
      qualified field (down to ${SV_MIN_SHOW_G}+ G / ${SV_MIN_SHOW_OUTS/3}+ IP) but don't count toward it.`:''}</p>
    <div class="svpanels${twoUp}">${panels}</div>`;
}
function savantCard(pl){
  if(!pl.seasons.some(s=>s.type==='Regular'&&!s.split)) return '';
  return `<section class="savant" id="savantCard"><h3>Percentile Rankings</h3>${savantInner(pl)}</section>`;
}
function wireSavant(pl){
  const host = document.getElementById('savantCard');
  if(!host) return;
  host.querySelectorAll('.svchips button').forEach(b=>b.addEventListener('click',()=>{
    svYear = +b.dataset.svy;
    host.innerHTML = '<h3>Percentile Rankings</h3>' + savantInner(pl);
    wireSavant(pl);
  }));
}

/* ---- minimal sparkline (season trajectory) ---- */
function sparkline(pts, col){
  const valid = (pts||[]).filter(p=>isFinite(p.y));
  if(valid.length < 2) return '';
  const W=150, H=34, pad=4;
  const xs=valid.map(p=>p.x), ys=valid.map(p=>p.y);
  const x0=Math.min(...xs), x1=Math.max(...xs);
  let y0=Math.min(...ys), y1=Math.max(...ys);
  if(y0===y1){ y0-=1; y1+=1; }
  const sx=v=>pad+(v-x0)/((x1-x0)||1)*(W-2*pad);
  const sy=v=>H-pad-(v-y0)/((y1-y0)||1)*(H-2*pad);
  const d=valid.map((p,i)=>(i?'L':'M')+sx(p.x).toFixed(1)+' '+sy(p.y).toFixed(1)).join(' ');
  const last=valid[valid.length-1];
  const area=`${d} L ${sx(last.x).toFixed(1)} ${H-pad} L ${sx(valid[0].x).toFixed(1)} ${H-pad} Z`;
  const c = col || 'var(--accent)';
  return `<svg class="spark" viewBox="0 0 ${W} ${H}" preserveAspectRatio="none" aria-hidden="true">
    <path d="${area}" fill="${c}" fill-opacity="0.13"/>
    <path d="${d}" fill="none" stroke="${c}" stroke-width="1.6" stroke-linejoin="round" stroke-linecap="round"
      vector-effect="non-scaling-stroke"/>
    <circle cx="${sx(last.x).toFixed(1)}" cy="${sy(last.y).toFixed(1)}" r="2.6" fill="${c}"/>
  </svg>`;
}
/* horizontal bar chart: items = [{label, value, color?}], value already 0..1 unless opts.max given */
function barChart(items, opts={}){
  if(!items.length) return '';
  const max = opts.max || Math.max(...items.map(i=>i.value), 1e-9);
  const autoLabelW = Math.min(230, 34 + Math.max(...items.map(i=>String(i.label).length))*6.3);
  const rowH = 22, gap = 7, labelW = opts.labelW || autoLabelW, barW = opts.barW || 280, pad = 6;
  const fmt = opts.fmt || (v=>v);
  const W = labelW + barW + 58, H = pad*2 + items.length*(rowH+gap) - gap;
  const rows = items.map((it,i)=>{
    const y = pad + i*(rowH+gap);
    const w = Math.max(2, (it.value/max)*barW);
    const col = it.color || 'var(--accent)';
    return `<text x="${labelW-8}" y="${y+rowH*0.68}" text-anchor="end" font-size="11" fill="var(--ink)">${esc(it.label)}</text>
      <rect x="${labelW}" y="${y}" width="${barW}" height="${rowH}" rx="4" fill="var(--line)"/>
      <rect x="${labelW}" y="${y}" width="${w.toFixed(1)}" height="${rowH}" rx="4" fill="${col}"/>
      <text x="${(labelW+w+7).toFixed(1)}" y="${y+rowH*0.68}" font-size="11" font-family="ui-monospace,monospace" fill="var(--muted)">${esc(fmt(it.value))}</text>`;
  }).join('');
  return `<svg class="barchart" viewBox="0 0 ${W} ${H}" width="100%" style="max-width:${W}px" role="img" aria-label="${esc(opts.aria||'')}">${rows}</svg>`;
}

/* one ring per team-and-number stint that has a known jersey number —
   chronological, consecutive years on the same team wearing the same
   number collapse into a single circle (a decade on the same number
   shouldn't repeat the same ring ten times), team/year(s) on hover
   (native title plus a styled tooltip). Each ring is two-toned — outer
   border in the team's primary color, inner ring in its secondary,
   from the same FRANCHISE_COLORS used for team pages/hero banners — so
   two teams never read as the same ring. Regular-season rows only
   (each split stint counted on its own, the combined "tot" row
   skipped); a player with no numbers on record yet renders nothing
   rather than a row of blank circles. */
function teamHistoryCircles(pl){
  const rows = pl.seasons.filter(s=>s.type==='Regular' && !s.tot && s.team && s.num)
    .slice().sort((a,b)=>a.year-b.year);
  if(!rows.length) return '';
  const stints = [];
  rows.forEach(s=>{
    const last = stints[stints.length-1];
    if(last && last.team===s.team && String(last.num)===String(s.num) && s.year===last.to+1){
      last.to = s.year;
    } else {
      stints.push({team:s.team, num:s.num, from:s.year, to:s.year});
    }
  });
  const items = stints.map(st=>{
    const c = FRANCHISE_COLORS[st.team] || {};
    const rcP = c.p || 'var(--line-strong)', rcS = c.s || 'var(--line-strong)';
    /* full, era-accurate name — if the franchise renamed partway through
       this merged stint, use the name it went by in the LAST year of the
       range, not whichever name happened to be active when the stint began */
    const label = TEAMS[st.team] ? histName(st.team, st.to) : st.team;
    const yrs = st.from===st.to ? String(st.from) : `${st.from}–${st.to}`;
    const tip = `${esc(label)} · ${yrs}`;
    return `<span class="numring" style="--rc-p:${rcP};--rc-s:${rcS}" title="${tip}">
      <b>${esc(String(st.num))}</b><span class="numring-tip">${tip}</span>
    </span>`;
  }).join('');
  return `<div class="numhist"><h4>Team History</h4><div class="numrow">${items}</div></div>`;
}
function playerSparks(pl){
  const rows = svSeasons(pl).map(y=>svRegRow(pl,y)).filter(Boolean);
  const bat = rows.filter(r=>r.PA>0).map(r=>({x:r.year, y:ops(r)}));
  const pit = rows.filter(r=>r.IPouts>0).map(r=>({x:r.year, y:era(r)}));
  const card = (title, pts, cur, col) => sparkline(pts, col) && `<div class="sparkcard">
    <h4>${title}</h4>
    <div class="spv">${cur}<small>${pts[0].x}–${pts[pts.length-1].x}</small></div>
    ${sparkline(pts, col)}</div>`;
  const b = card('OPS by season', bat, rate(ops(pl.careerReg)), 'var(--tc,var(--accent))');
  const p = card('ERA by season', pit, two(era(pl.careerReg)), 'var(--clay)');
  return (b||p) ? `<div class="sparks">${b||''}${p||''}</div>` : '';
}
function teamSpark(t){
  const pts = t.years.slice().sort((a,b)=>a-b).map(y=>{
    const r = t.seasons[y] && t.seasons[y].record && t.seasons[y].record.Regular;
    if(!r) return null; const g = r.W+r.L+r.T;
    return g ? {x:y, y:r.W/g} : null;
  }).filter(Boolean);
  if(pts.length < 2) return '';
  const cg = t.record.W + t.record.L;
  return `<div class="sparks"><div class="sparkcard">
    <h4>Win % by season</h4>
    <div class="spv">${cg?rate(t.record.W/cg):'—'}<small>career</small></div>
    ${sparkline(pts, 'var(--tc,var(--accent))')}</div></div>`;
}

function accolades(pl){
  const h = pl.honors || {rings:[],awards:[],asg:[]};
  const nh = (typeof NOHIT_BY_PITCHER!=='undefined' && NOHIT_BY_PITCHER[pl.name]) || [];
  const hrdYears = (typeof HRD_BY_PLAYER!=='undefined' && HRD_BY_PLAYER[pl.name]) || [];
  const asgMvpYears = (typeof ASGMVP_BY_PLAYER!=='undefined' && ASGMVP_BY_PLAYER[pl.name]) || [];
  if(!(h.rings.length || h.awards.length || h.asg.length || nh.length || hrdYears.length || asgMvpYears.length)) return '';
  const rings = h.rings.length ? `<div class="acc-block">
    <h4>${h.rings.length}× World Series</h4>
    <div class="rings">${h.rings.map(r=>`<span class="ring">${TROPHY} ${r.year} <span class="rt">${histNickLink(r.team, r.year)}</span></span>`).join('')}</div>
  </div>` : '';
  const AW_ORDER = ['MVP','CY Young','Postseason MVP','All-Star Game MVP','Rookie of the Year','Silver Slugger',
    'Golden Hands','Batting Title','Home Run King','Home Run Derby Champion','Reliever of the Year',
    'Comeback Player of the Year','Manager of the Year'];
  const grp = {};
  h.awards.forEach(a=>{ (grp[a.award] = grp[a.award] || []).push(a.year); });
  if(hrdYears.length) grp['Home Run Derby Champion'] = hrdYears.slice();
  if(asgMvpYears.length) grp['All-Star Game MVP'] = asgMvpYears.slice();
  const gkeys = Object.keys(grp).sort((a,b)=>{
    const ia=AW_ORDER.indexOf(a), ib=AW_ORDER.indexOf(b);
    return (ia<0?99:ia)-(ib<0?99:ib) || a.localeCompare(b);
  });
  const totAw = Object.values(grp).reduce((s,arr)=>s+arr.length, 0);
  const aw = totAw ? `<div class="acc-block">
    <h4>${totAw} Award${totAw>1?'s':''}</h4>
    <dl class="awroll">${gkeys.map(k=>`<div><dt>${esc(k)}${grp[k].length>1?` <b>×${grp[k].length}</b>`:''}</dt>
      <dd>${grp[k].slice().sort((x,y)=>y-x).join(', ')}</dd></div>`).join('')}</dl>
  </div>` : '';
  const caps = h.asg.filter(s=>s.cap).length;
  const asg = h.asg.length ? `<div class="acc-block">
    <h4>${h.asg.length}× All-Star${caps?` · ${caps}× captain`:''}</h4>
    <p class="acc-years">${h.asg.map(s=>`${s.year}${s.cap?'<span class="capdot">C</span>':''}`).join('&nbsp; ')}</p>
  </div>` : '';
  const nhPerf = nh.filter(x=>x.perfect).length;
  const noHit = nh.length ? `<div class="acc-block">
    <h4>${nh.length} No-Hitter${nh.length>1?'s':''}${nhPerf?` · ${nhPerf} Perfect Game${nhPerf>1?'s':''}`:''}</h4>
    <p class="acc-years">${nh.map(x=>`${x.gid?`<button class="pname" data-g="${x.gid}">${esc(x.dateDisplay)}</button>`:esc(x.dateDisplay)} vs ${histNickLink(x.opp, +x.date.slice(0,4))}${x.perfect?' <span class="estd">Perfect Game</span>':''}`).join('<br>')}</p>
  </div>` : '';
  return `<section class="stat accolades"><h3>Accolades</h3>${rings}${aw}${asg}${noHit}
    <p class="acc-leg">In the season tables below, the <b>Awards</b> column marks that year:
    WS champion · MVP · CYA Cy Young · RoY Rookie of the Year · SS Silver Slugger · GH Golden Hands ·
    BT Batting Title · HRK Home Run King · RoR Reliever · CPoY Comeback · MgrY Manager · PoMVP Postseason MVP ·
    AS All-Star.${nh.length?' No-hitters and perfect games are from the league\'s own record — see the Records page.':''}</p></section>`;
}

let playerTab = 'Regular', logYear = null, splitYear = 'all', playerSubView = 'stats';
function detail(name){
  const pl = P[name];
  if(!pl){ location.hash=''; return; }
  setNav('players');
  const cr = pl.careerReg, cp = pl.careerPO;
  const hasPost = cp.G_bat>0 || cp.G_pit>0;
  const rYrs = pl.years;

  const opsp = opsPlusFor(cr, careerWeights(pl, false));
  const hitCard = `<div class="split"><h4>Career Hitting</h4>
    ${cr.G_bat ? `<div class="line">${slash(cr)}</div>
      <div class="sub">${cr.HR} HR · ${cr.RBI} RBI${isFinite(opsp)?` · ${opsp} <span title="100 = league average for the seasons played, weighted by PA">OPS+</span>`:''}</div>`
      : `<div class="line">—</div><div class="sub">No appearances</div>`}</div>`;
  const pitCard = `<div class="split po"><h4>Career Pitching</h4>
    ${cr.G_pit ? `<div class="line">${wl(cr)}, ${two(era(cr))} ERA</div>
      <div class="sub">${cr.pK} K · ${two(whip(cr))} WHIP · ${ipStr(cr.IPouts)} IP</div>`
      : `<div class="line">—</div><div class="sub">No appearances</div>`}</div>`;

  const overviewHTML = `${teamHistoryCircles(pl)}
    <div class="splitgrid">
      ${hitCard}
      ${pitCard}
    </div>
    ${accolades(pl)}
    ${savantCard(pl)}`;

  /* each phase's Stats/Splits/Game Log used to be concatenated into one long
     scroll; returned separately here so they can be their own nested tabs
     below the phase tab bar — a phase with nothing at all (e.g. Playoffs for
     a player with no postseason) still returns a single `none` block. */
  const phaseTab = t => {
    if(t==='Playoffs' && !hasPost){
      return {none:`<div class="phase post"><h3>Postseason</h3><div class="nopost">No postseason games on record.</div></div>`};
    }
    return {
      stats: phaseBlock(pl, t),
      splits: t==='NWLA' ? playerNWLASplits(pl, splitYear) : playerSplits(pl, t, splitYear),
      log: t==='NWLA' ? playerNWLALog(pl, logYear) : playerGameLog(pl, t, logYear),
    };
  };
  const tabs = ['Regular','Playoffs','AllStar','Spring','Fall','Exhib','NWLA']
    .map(t=>[t, PHASE_META[t].head, phaseTab(t)])
    .filter(([t,,c])=> t==='Regular' || t==='Playoffs' || c.none ||
      (c.stats||'').trim() || (c.splits||'').trim() || (c.log||'').trim());
  if(!tabs.some(t=>t[0]===playerTab)) playerTab = 'Regular';
  const active = tabs.find(t=>t[0]===playerTab) || tabs[0];
  const tabBar = `<div class="subtabs" role="group" aria-label="Section">
    ${tabs.map(([k,label])=>`<button data-pt="${k}" aria-pressed="${playerTab===k}">${esc(label)}</button>`).join('')}
  </div>`;

  const activeContent = active[2];
  let activeHTML;
  if(activeContent.none){
    activeHTML = activeContent.none;
  } else {
    const views = [['stats','Stats'],['splits','Splits'],['log','Game Log']]
      .filter(([k])=>(activeContent[k]||'').trim());
    if(!views.some(([k])=>k===playerSubView)) playerSubView = views.length ? views[0][0] : 'stats';
    const viewBar = views.length>1 ? `<div class="subtabs subtabs2" role="group" aria-label="View">
      ${views.map(([k,label])=>`<button data-psv="${k}" aria-pressed="${playerSubView===k}">${esc(label)}</button>`).join('')}
    </div>` : '';
    activeHTML = viewBar + (activeContent[playerSubView] || '<p class="empty">Nothing here.</p>');
  }

  const lt = latestTeam(pl);
  setTeamVars(lt);

  /* "current team" only means something if they were actually on a roster
     in the league's most recent season — a player who last appeared years
     ago shouldn't read as still belonging to whoever they finished with */
  const curTeamEntry = pl.teamsByYear[LATEST_YEAR];
  const curTeamLabel = curTeamEntry && curTeamEntry.team
    ? curTeamEntry.team.split(' / ').map(t => TEAMS[t] ? TEAMS[t].nick : t).join('/')
    : '';

  app.innerHTML = `
    <button class="back" id="back">← Players</button>
    <div class="phead phead-team">
      <div class="hero-row">
        ${pl.photo?`<img class="pphoto" src="${pl.photo}" alt="">`:''}
        <h2>${esc(name)}</h2>
      </div>
      <span class="yrs">${rYrs.length} season${rYrs.length>1?'s':''} · ${rYrs[0]}–${rYrs[rYrs.length-1]} · ${cr.G_bat} reg. G${hasPost?` · ${cp.G_bat} postseason G`:''}${curTeamLabel?` · ${esc(curTeamLabel)}`:''}</span>
      ${editBtn('Edit seasons','editSeasonsBtn')}
      ${editBtn('Edit photo','editPhotoBtn')}
    </div>
    ${overviewHTML}
    ${tabBar}
    ${activeHTML}
    <p class="note">Each phase — regular season, postseason, the exhibition sets (All-Star, spring training, fall ball, the Brookside Field Finale) and the NWLA Tournament (national-team play, from GameChanger) — is tallied in its own block, one row per year plus a phase total; nothing is pooled across phases. Team is from the league roster (<span class="pt">*</span> = estimated from game appearances).
    <span class="estd">†</span> 2016: cumulative totals only — 2B, 3B and hits/walks allowed are extrapolated from
    the player's later rates, and Runs are unavailable. Spans ${RANGE}.</p>`;
  document.getElementById('back').addEventListener('click',()=>{ location.hash='#/players'; });
  app.querySelectorAll('[data-pt]').forEach(b=>b.addEventListener('click',()=>{
    playerTab = b.dataset.pt; logYear = null; splitYear = 'all'; detail(name);
  }));
  app.querySelectorAll('[data-psv]').forEach(b=>b.addEventListener('click',()=>{
    playerSubView = b.dataset.psv; detail(name);
  }));
  app.querySelectorAll('[data-ly]').forEach(b=>b.addEventListener('click',()=>{
    logYear = b.dataset.ly; detail(name);
  }));
  app.querySelectorAll('[data-spy]').forEach(b=>b.addEventListener('click',()=>{
    splitYear = b.dataset.spy; detail(name);
  }));
  app.querySelectorAll('.pname[data-g]').forEach(b=>b.addEventListener('click',()=>{
    location.hash='#/g/'+b.dataset.g; }));
  app.querySelectorAll('.pname[data-t]').forEach(b=>b.addEventListener('click',()=>{
    location.hash='#/t/'+encodeURIComponent(b.dataset.t); }));
  app.querySelectorAll('.pname[data-bv]').forEach(b=>b.addEventListener('click',()=>{
    location.hash='#/beavers/'+encodeURIComponent(b.dataset.bv); }));
  app.querySelectorAll('.pname[data-beavers]').forEach(b=>b.addEventListener('click',()=>{
    location.hash='#/beavers'; }));
  document.getElementById('editSeasonsBtn').addEventListener('click', ()=>openSeasonEditor(pl));
  document.getElementById('editPhotoBtn').addEventListener('click', ()=>{
    openImageEditor(`Player Photo — ${pl.name}`, pl.photo, 240, async url=>{
      const before = pl.photo;
      pl.photo = url;
      if(await saveDB()) return true;
      pl.photo = before; return false;
    });
  });
  wireSavant(pl);
  app.querySelectorAll('table.sortable').forEach(makeSortable);
}

/* ============================ PLAYER COMPARISON ============================ */
const CMP_BAT = [
  ['G',   c=>c.G_bat, v=>v, false], ['PA',  c=>c.PA, v=>v, false], ['AB', c=>c.AB, v=>v, false],
  ['R',   c=>c.R,     v=>v, false], ['H',   c=>c.H,  v=>v, false],
  ['2B',  c=>c['2B'], v=>v, false], ['3B',  c=>c['3B'], v=>v, false], ['HR', c=>c.HR, v=>v, false],
  ['RBI', c=>c.RBI,   v=>v, false], ['BB',  c=>c.BB, v=>v, false], ['K', c=>c.K, v=>v, true],
  ['AVG', c=>avg(c), rate, false], ['OBP', c=>obp(c), rate, false],
  ['SLG', c=>slg(c), rate, false], ['OPS', c=>ops(c), rate, false],
];
const CMP_PIT = [
  ['G',  c=>c.G_pit, v=>v, false], ['IP', c=>c.IPouts, ipStr, false],
  ['W',  c=>c.W, v=>v, false], ['L', c=>c.L, v=>v, true], ['SV', c=>c.SV, v=>v, false],
  ['K',  c=>c.pK, v=>v, false],
  ['ERA', c=>era(c), two, true], ['WHIP', c=>whip(c), two, true], ['K/3', c=>k9(c), two, false],
];
function cmpRow(label, valA, valB, fmt, lowerBetter){
  const winA = isFinite(valA) && (!isFinite(valB) || (lowerBetter ? valA<valB : valA>valB));
  const winB = isFinite(valB) && (!isFinite(valA) || (lowerBetter ? valB<valA : valB>valA));
  return `<tr><td class="mono${winA?' cmpwin':''}">${isFinite(valA)?fmt(valA):'—'}</td>
    <td class="lft cmplab">${label}</td>
    <td class="mono${winB?' cmpwin':''}">${isFinite(valB)?fmt(valB):'—'}</td></tr>`;
}
function cmpTable(title, rows, ca, cb, extraRowsHTML){
  const body = rows.map(([label,fn,fmt,low])=>cmpRow(label, fn(ca), fn(cb), fmt, low)).join('');
  return `<div class="cmpblock"><h4 class="hsub">${title}</h4>
    <table class="detail cmptable"><tbody>${body}${extraRowsHTML||''}</tbody></table></div>`;
}
function cmpHead(pl){
  const yrs = pl.years;
  const lt = latestTeam(pl);
  return `<div class="cmpplayer">
    ${pl.photo?`<img class="pphoto" src="${pl.photo}" alt="">`:''}
    <button class="pname cmpname" data-p="${esc(pl.name)}">${esc(pl.name)}</button>
    <span class="azm">${yrs.length} season${yrs.length>1?'s':''} · ${yrs[0]}–${yrs[yrs.length-1]}${lt&&TEAMS[lt]?` · ${esc(TEAMS[lt].nick)}`:''}</span>
  </div>`;
}
function cmpAccRow(label, a, b){
  if(!a && !b) return '';
  return `<tr><td class="mono${a>b?' cmpwin':''}">${a||'—'}</td><td class="lft cmplab">${label}</td>
    <td class="mono${b>a?' cmpwin':''}">${b||'—'}</td></tr>`;
}
/* career-line percentile comparison, reusing the same SV_BAT/SV_PIT metric
   list, svColor/svPct math and qualification bar (SV_MING/SV_MINOUTS, with
   the same SV_MIN_SHOW_G/SV_MIN_SHOW_OUTS faded-estimate floor) already
   built for a single player's own Percentile Rankings — just against a
   career-totals pool instead of one season's, and with both players' dots
   sharing one track per row instead of one dot per row */
const CMP_POOL_BAT = NAMES.map(n=>P[n].careerReg).filter(c=>c.G_bat>=SV_MING);
const CMP_POOL_PIT = NAMES.map(n=>P[n].careerReg).filter(c=>c.IPouts>=SV_MINOUTS);
function cmpCareerQual(c){
  return {
    batOK: c.G_bat>=SV_MING, pitOK: c.IPouts>=SV_MINOUTS,
    batShow: c.G_bat<SV_MING && c.G_bat>=SV_MIN_SHOW_G,
    pitShow: c.IPouts<SV_MINOUTS && c.IPouts>=SV_MIN_SHOW_OUTS,
  };
}
function cmpSvRow(label, fn, fmt, low, ca, cb, pool, unqA, unqB, nameA, nameB){
  const vals = pool.map(fn).filter(isFinite);
  const pA = svPct(vals, fn(ca), low), pB = svPct(vals, fn(cb), low);
  if(pA==null && pB==null) return '';
  const dot = (p, unq, letter, nm) => p==null ? '' :
    `<span class="svdot${unq?' svunq-dot':''}" style="left:${p}%;background:${svColor(p)}"
      title="${esc(nm)} — ${ORDINAL_TH(p)} percentile${unq?' (estimate — below the qualification bar)':''}">
      <b class="svdotltr">${letter}</b>${p}</span>`;
  return `<div class="svrow${(unqA&&pA!=null)||(unqB&&pB!=null)?' cmpsvunq':''}"><span class="svlab">${label}</span>
    <span class="svbar cmpsvbar">${dot(pA,unqA,'A',nameA)}${dot(pB,unqB,'B',nameB)}</span>
    <span class="svval">${isFinite(fn(ca))?fmt(fn(ca)):'—'} · ${isFinite(fn(cb))?fmt(fn(cb)):'—'}</span></div>`;
}
function cmpSvPanel(title, metrics, ca, cb, pool, unqA, unqB, nameA, nameB){
  const rows = metrics.map(([lab,fn,fmt,low])=>cmpSvRow(lab, fn, fmt, low, ca, cb, pool, unqA, unqB, nameA, nameB)).join('');
  return rows ? `<div class="svpanel"><h4>${esc(title)}</h4>${rows}</div>` : '';
}
function cmpSavantHTML(a, b){
  const ca = a.careerReg, cb = b.careerReg;
  const qa = cmpCareerQual(ca), qb = cmpCareerQual(cb);
  const showBat = qa.batOK||qa.batShow||qb.batOK||qb.batShow;
  const showPit = qa.pitOK||qa.pitShow||qb.pitOK||qb.pitShow;
  if(!showBat && !showPit) return '';
  const batHTML = showBat ? cmpSvPanel(`Batting · vs ${CMP_POOL_BAT.length}`, SV_BAT, ca, cb, CMP_POOL_BAT, !qa.batOK, !qb.batOK, a.name, b.name) : '';
  const pitHTML = showPit ? cmpSvPanel(`Pitching · vs ${CMP_POOL_PIT.length}`, SV_PIT, ca, cb, CMP_POOL_PIT, !qa.pitOK, !qb.pitOK, a.name, b.name) : '';
  const anyUnq = (showBat && !qa.batOK) || (showBat && !qb.batOK) || (showPit && !qa.pitOK) || (showPit && !qb.pitOK);
  return `<section class="savant"><h3>Percentile Comparison</h3>
    <p class="smeta">Career totals, percentile vs every qualified player's own career (${SV_MING}+ G batting,
      ${SV_MINOUTS/3}+ IP pitching) · <b>A</b> = ${esc(a.name)}, <b>B</b> = ${esc(b.name)} ·
      <span style="color:${svColor(100)}">red</span> = league-best, <span style="color:${svColor(0)}">blue</span> = trailing.
      K%, BB%, ERA, WHIP, BB/3, OPP AVG ranked low-is-better.
      ${anyUnq?' Faded dots are below the qualification bar — shown as an estimate, not a real ranking.':''}</p>
    <div class="svpanels two">${batHTML}${pitHTML}</div>
  </section>`;
}
function renderComparePicker(prefA, prefB, notFound){
  return `<div class="phead"><h2>Compare Players</h2></div>
    <p class="pmeta">Pick two players to compare their career lines side by side.</p>
    <div class="cmppicker">
      <input id="cmpA" list="cmplist" placeholder="Player A" value="${esc(prefA||'')}">
      <span class="cmpvs">vs</span>
      <input id="cmpB" list="cmplist" placeholder="Player B" value="${esc(prefB||'')}">
      <button class="pname cmpgo" id="cmpGo">Compare →</button>
    </div>
    <datalist id="cmplist">${NAMES.map(n=>`<option value="${esc(n)}">`).join('')}</datalist>
    ${notFound?`<p class="empty">Couldn't find "${esc(notFound)}" — pick a name from the list.</p>`:''}`;
}
function wireComparePicker(nameA, nameB){
  const go = () => {
    const a = document.getElementById('cmpA').value.trim();
    const b = document.getElementById('cmpB').value.trim();
    if(!a || !b) return;
    location.hash = '#/compare/'+encodeURIComponent(a)+'/'+encodeURIComponent(b);
  };
  document.getElementById('cmpGo').addEventListener('click', go);
  ['cmpA','cmpB'].forEach(id=>document.getElementById(id).addEventListener('keydown', e=>{
    if(e.key==='Enter') go();
  }));
}
function renderCompare(nameA, nameB){
  setNav('players');
  const a = nameA ? P[nameA] : null, b = nameB ? P[nameB] : null;
  if(!a || !b){
    app.innerHTML = `<button class="back" id="back">← Players</button>
      ${renderComparePicker(nameA, nameB, (nameA&&!a)?nameA : (nameB&&!b)?nameB : null)}`;
    document.getElementById('back').addEventListener('click',()=>{ location.hash='#/players'; });
    wireComparePicker(nameA, nameB);
    return;
  }
  const ca = a.careerReg, cb = b.careerReg;
  const hasPit = ca.IPouts>0 || cb.IPouts>0;
  const opspA = opsPlusFor(ca, careerWeights(a, false)), opspB = opsPlusFor(cb, careerWeights(b, false));
  const battingHTML = cmpTable('Career Hitting', CMP_BAT, ca, cb, cmpRow('OPS+', opspA, opspB, v=>String(v), false));
  const erapA = eraPlusFor(ca, careerWeightsPit(a, false)), erapB = eraPlusFor(cb, careerWeightsPit(b, false));
  const pitchingHTML = hasPit ? cmpTable('Career Pitching', CMP_PIT, ca, cb, cmpRow('ERA+', erapA, erapB, v=>String(v), false)) : '';
  const ha = a.honors||{rings:[],awards:[],asg:[]}, hb = b.honors||{rings:[],awards:[],asg:[]};
  const nhA = (NOHIT_BY_PITCHER[a.name]||[]).length, nhB = (NOHIT_BY_PITCHER[b.name]||[]).length;
  const hrdA = (HRD_BY_PLAYER[a.name]||[]).length, hrdB = (HRD_BY_PLAYER[b.name]||[]).length;
  const mvpA = (ASGMVP_BY_PLAYER[a.name]||[]).length, mvpB = (ASGMVP_BY_PLAYER[b.name]||[]).length;
  const accHTML = `<div class="cmpblock"><h4 class="hsub">Accolades</h4><table class="detail cmptable"><tbody>
    ${cmpAccRow('World Series', ha.rings.length, hb.rings.length)}
    ${cmpAccRow('Awards', ha.awards.length, hb.awards.length)}
    ${cmpAccRow('All-Star', ha.asg.length, hb.asg.length)}
    ${cmpAccRow('All-Star Game MVP', mvpA, mvpB)}
    ${cmpAccRow('Home Run Derby', hrdA, hrdB)}
    ${cmpAccRow('No-Hitters', nhA, nhB)}
  </tbody></table></div>`;
  const svHTML = cmpSavantHTML(a, b);
  app.innerHTML = `
    <button class="back" id="back">← Players</button>
    <div class="phead"><h2>Compare Players</h2></div>
    <div class="cmpwrap">
      <div class="cmpheads">${cmpHead(a)}<span class="cmpvs">vs</span>${cmpHead(b)}</div>
      ${battingHTML}${pitchingHTML}${accHTML}
    </div>
    ${svHTML}
    <p class="note">Career regular-season totals. <span class="cmpwin cmpwinsample">Highlighted</span> value is
    the better of the two in each row; K is fewer-is-better for batters, more-is-better for pitchers.</p>
    ${renderComparePicker(nameA, nameB)}`;
  document.getElementById('back').addEventListener('click',()=>{ location.hash='#/players'; });
  wireComparePicker(nameA, nameB);
  app.querySelectorAll('.pname[data-p]').forEach(b=>b.addEventListener('click',()=>{
    location.hash='#/p/'+encodeURIComponent(b.dataset.p); }));
}

/* ================================ TEAMS ================================ */
const TEAMS = DB.teams || {};
const TEAMNAMES = Object.keys(TEAMS).sort((a,b)=>a.localeCompare(b));
let tMode='bat', tSort='HR', tDir=-1, tQuery='', teamYear=null, teamPhase='reg';

const recWL = r => r ? `${r.W}–${r.L}${r.T?'–'+r.T:''}` : '0–0';
const wirePlayerLinks = () => app.querySelectorAll('.pname[data-p]').forEach(b=>
  b.addEventListener('click',()=>{ location.hash = '#/p/'+encodeURIComponent(b.dataset.p); }));

/* franchise all-time regular-season aggregate (sum of every season's roster lines) */
const TAGG = {};
const TAGG_WEIGHTS = {};   // [{year,pa}] per franchise — for weighting that team's career OPS+ baseline
const TAGG_PIT_WEIGHTS = {};   // [{year,outs}] per franchise — same, for career ERA+
TEAMNAMES.forEach(n=>{
  const reg=[];
  const weights=[];
  const pitWeights=[];
  Object.entries(TEAMS[n].seasons).forEach(([y,s])=>{
    const lines = (s.roster||[]).filter(e=>e.regular).map(e=>e.regular);
    reg.push(...lines);
    const yearTot = sumRows(lines);
    if(yearTot.PA) weights.push({year:+y, pa:yearTot.PA});
    if(yearTot.IPouts) pitWeights.push({year:+y, outs:yearTot.IPouts});
  });
  TAGG[n]=sumRows(reg);
  TAGG_WEIGHTS[n]=weights;
  TAGG_PIT_WEIGHTS[n]=pitWeights;
});

const T_BAT_COLS = [
  ['name','Team','s'],['yrs','Yr','n'],['G','G','n'],['PA','PA','n'],['R','R','n'],['H','H','n'],
  ['HR','HR','n'],['RBI','RBI','n'],['BB','BB','n'],['K','K','n'],
  ['AVG','AVG','r'],['OBP','OBP','r'],['SLG','SLG','r'],['OPS','OPS','r'],['OPS+','OPS+','n'],
];
const T_PIT_COLS = [
  ['name','Team','s'],['yrs','Yr','n'],['Gp','G','n'],['IP','IP','n'],['pR','R','n'],['ER','ER','n'],
  ['pH','H','n'],['pBB','BB','n'],['pK','K','n'],
  ['ERA','ERA','r'],['WHIP','WHIP','r'],['K9','K/3','r'],['ERA+','ERA+','n'],
];

function teamRowVals(n){
  const c=TAGG[n], r=TEAMS[n].record, g=r.W+r.L+r.T;
  return {
    name:n, yrs:TEAMS[n].years.length, W:r.W, L:r.L, PCT: g?r.W/g:NaN,
    G:c.G_bat, PA:c.PA, R:c.R, H:c.H, HR:c.HR, RBI:c.RBI, BB:c.BB, K:c.K,
    AVG:avg(c), OBP:obp(c), SLG:slg(c), OPS:ops(c), 'OPS+':opsPlusFor(c, TAGG_WEIGHTS[n]),
    Gp:c.G_pit, IP:c.IPouts/3, pR:c.pR, ER:c.ER, pH:c.pH, pBB:c.pBB, pK:c.pK,
    ERA:era(c), WHIP:whip(c), K9:k9(c), 'ERA+':eraPlusFor(c, TAGG_PIT_WEIGHTS[n]),
  };
}

/* full franchise history (all seasons, from the league's records) */
const FRANCHISE_SUMMARY = [
  {t:'Panthers',        f:'Brookside Panthers',           w:218,l:129,pct:.628, yr:'2012–Pres', ws:5,wsa:8, dv:11,po:14,wsz:12,as:27, por:'19–14'},
  {t:'Kraken',          f:'Brookside Kraken',             w:251,l:97, pct:.721, yr:'2012–Pres', ws:3,wsa:7, dv:9, po:14,wsz:14,as:28, por:'14–15'},
  {t:'Gladiators',      f:'Brentwood Gladiators',         w:54, l:36, pct:.600, yr:'2021–Pres', ws:2,wsa:2, dv:1, po:5, wsz:5, as:11, por:'7–6'},
  {t:'The Process',     f:'Glenwood Process',             w:70, l:33, pct:.680, yr:'2017–2021', ws:1,wsa:2, dv:2, po:5, wsz:5, as:4,  por:'5–5'},
  {t:'Kings',           f:'Harris Kings',                 w:30, l:63, pct:.323, yr:'2018–2021, 2026–Pres', ws:2,wsa:2, dv:0, po:2, wsz:2, as:5, por:'6–1'},
  {t:'Shock',           f:'Shelton Shock',               w:34, l:26, pct:.567, yr:'2022–2024, 2026–Pres', ws:1,wsa:2, dv:1, po:3, wsz:3, as:7, por:'5–3'},
  {t:'Sox',             f:null, full:'Davenport Sox',      w:12, l:3,  pct:.800, yr:'2012',      ws:1,wsa:1, dv:1, po:1, wsz:1, as:1,  por:'2–0'},
  {t:'Lavahogs',        f:'Beaver Brook Lavahogs',        w:128,l:130,pct:.496, yr:'2012–2020', ws:0,wsa:2, dv:2, po:4, wsz:5, as:11, por:'2–6'},
  {t:'Braves',          f:'Brentwood Braves',             w:42, l:47, pct:.472, yr:'2016–2017, 2023–2024', ws:0,wsa:2, dv:1, po:4, wsz:3, as:8, por:'3–7'},
  {t:'Bananas',         f:'Brentwood Bananas',            w:12, l:33, pct:.267, yr:'2022–2024', ws:0,wsa:1, dv:1, po:1, wsz:1, as:7, por:'2–2'},
  {t:'Royals',          f:null, full:'Brookside Royals',   w:57, l:38, pct:.600, yr:'2012–2014', ws:0,wsa:1, dv:0, po:1, wsz:2, as:3,  por:'1–1'},
  {t:'Aces',            f:null, full:'Brentwood Aces',     w:58, l:97, pct:.374, yr:'2013–2016', ws:0,wsa:0, dv:0, po:2, wsz:2, as:5,  por:'0–2'},
  {t:'Squirrels',       f:null, full:'Brookside Squirrels',w:66, l:69, pct:.489, yr:'2012–2015', ws:0,wsa:0, dv:0, po:2, wsz:1, as:4,  por:'0–2'},
  {t:'Dragons',         f:'Purchase Dragons',             w:16, l:29, pct:.356, yr:'2021–2023', ws:0,wsa:0, dv:0, po:1, wsz:0, as:6,  por:'0–1'},
  {t:'Mustangs',        f:'Brentwood Mustangs',           w:32, l:92, pct:.258, yr:'2015–2018', ws:0,wsa:0, dv:0, po:1, wsz:0, as:6,  por:'0–1'},
  {t:'Angels',          f:null, full:'Downtown Angels',    w:40, l:40, pct:.500, yr:'2013–2014', ws:0,wsa:0, dv:0, po:0, wsz:1, as:1,  por:'—'},
  {t:'Titans',          f:'Downtown Titans',              w:11, l:4,  pct:.733, yr:'2025',      ws:0,wsa:0, dv:0, po:0, wsz:1, as:1,  por:'—'},
  {t:'PawSox',          f:'Purchase PawSox',              w:11, l:28, pct:.282, yr:'2019–2020', ws:0,wsa:0, dv:0, po:0, wsz:1, as:3,  por:'—'},
  {t:'Devils',          f:null, full:'Gleason Devils',     w:19, l:61, pct:.238, yr:'2013–2014', ws:0,wsa:0, dv:0, po:0, wsz:0, as:0,  por:'—'},
  {t:'Snapping Turtles',f:'Silver Lake Snapping Turtles', w:4,  l:26, pct:.133, yr:'2025–Pres', ws:0,wsa:0, dv:0, po:0, wsz:0, as:2,  por:'—'},
];

/* full name each franchise played under, year by year, since the league's 2012 founding —
   collapsed into eras (consecutive years under one name); a name that already reads as a
   complete place+nickname (e.g. the Dashers' Avondale years, before the franchise relocated
   and became the Brentwood Braves) is stored as its own override rather than being built
   from that franchise's current location prefix */
const FRANCHISE_TIMELINE = [
  {full:'Brookside Panthers', nick:'Panthers', eras:[
    {from:2012,to:2012,loc:'Brookside',nick:'Jackals'},
    {from:2013,to:2026,loc:'Brookside',nick:'Panthers'}]},
  {full:'Brookside Kraken', nick:'Kraken', eras:[
    {from:2012,to:2012,loc:'Brookside',nick:'Capitals'},
    {from:2013,to:2016,loc:'Brookside',nick:'Eagles'},
    {from:2017,to:2017,loc:'Brookside',nick:'Bluefish'},
    {from:2018,to:2026,loc:'Brookside',nick:'Kraken'}]},
  {full:'Beaver Brook Lavahogs', nick:'Lavahogs', eras:[
    {from:2012,to:2012,loc:'Beaver Brook',nick:'Tornadoes'},
    {from:2013,to:2014,loc:'Beaver Brook',nick:'Warriors'},
    {from:2015,to:2015,loc:'Beaver Brook',nick:'Manatees'},
    {from:2016,to:2016,loc:'Beaver Brook',nick:'Hotdoggers'},
    {from:2017,to:2017,loc:'Beaver Brook',nick:'Hogriders'},
    {from:2018,to:2018,loc:'Beaver Brook',nick:'Sea Thieves'},
    {from:2019,to:2020,loc:'Beaver Brook',nick:'Lavahogs'}]},
  {full:'Brookside Squirrels', nick:'Squirrels', eras:[
    {from:2012,to:2012,loc:'Brookside',nick:'Boulders'},
    {from:2013,to:2015,loc:'Brookside',nick:'Squirrels'}]},
  {full:'Brookside Royals', nick:'Royals', eras:[
    {from:2012,to:2012,loc:'Brookside',nick:'Bears'},
    {from:2013,to:2014,loc:'Brookside',nick:'Royals'}]},
  {full:'Davenport Sox', nick:'Sox', eras:[
    {from:2012,to:2012,loc:'Davenport',nick:'Sox'}]},
  {full:'Brentwood Aces', nick:'Aces', eras:[
    {from:2013,to:2016,loc:'Brentwood',nick:'Aces'}]},
  {full:'Gleason Devils', nick:'Devils', eras:[
    {from:2013,to:2014,loc:'Gleason',nick:'Devils'}]},
  {full:'Downtown Angels', nick:'Angels', eras:[
    {from:2013,to:2014,loc:'Downtown',nick:'Angels'}]},
  {full:'Brentwood Mustangs', nick:'Mustangs', eras:[
    {from:2015,to:2015,loc:'Brentwood',nick:'Mustangs'},
    {from:2016,to:2016,loc:'Brentwood',nick:'Bulldogs'},
    {from:2017,to:2018,loc:'Brentwood',nick:'Mustangs'}]},
  {full:'Brentwood Braves', nick:'Braves', eras:[
    {from:2016,to:2017,loc:'Avondale',nick:'Dashers'},
    {from:2024,to:2025,loc:'Brentwood',nick:'Braves'}]},
  {full:'Glenwood Process', nick:'The Process', eras:[
    {from:2017,to:2017,loc:'Glenwood',nick:'Wildcats'},
    {from:2018,to:2021,loc:'Glenwood',nick:'Process'}]},
  {full:'Harris Kings', nick:'Kings', eras:[
    {from:2018,to:2021,loc:'Harris',nick:"Special K's"},
    {from:2026,to:2026,loc:'Harris',nick:'Kings'}]},
  {full:'Purchase PawSox', nick:'PawSox', eras:[
    {from:2019,to:2020,loc:'Purchase',nick:'PawSox'}]},
  {full:'Brentwood Gladiators', nick:'Gladiators', eras:[
    {from:2021,to:2026,loc:'Brentwood',nick:'Gladiators'}]},
  {full:'Purchase Dragons', nick:'Dragons', eras:[
    {from:2021,to:2023,loc:'Purchase',nick:'Dragons'}]},
  {full:'Shelton Shock', nick:'Shock', eras:[
    {from:2022,to:2024,loc:'Shelton',nick:'Shock'},
    {from:2026,to:2026,loc:'Shelton',nick:'Shock'}]},
  {full:'Brentwood Bananas', nick:'Bananas', eras:[
    {from:2022,to:2024,loc:'Brentwood',nick:'Bananas'}]},
  {full:'Downtown Titans', nick:'Titans', eras:[
    {from:2025,to:2025,loc:'Downtown',nick:'Titans'}]},
  {full:'Silver Lake Snapping Turtles', nick:'Snapping Turtles', eras:[
    {from:2025,to:2026,loc:'Silver Lake',nick:'Snapping Turtles'}]},
];

/* team captain / co-captains, by franchise — hand-kept, not derived from any
   box score. A co-captain's years cover when they held that role, which can
   be non-contiguous (e.g. the same person co-captaining twice with a gap). */
const LEADERSHIP = DB.leadership || {};
const leaderName = n => P[n]
  ? `<button class="pname" data-p="${esc(n)}">${esc(n)}</button>` : esc(n);
function teamLeadershipHtml(full){
  const ld = LEADERSHIP[full];
  if(!ld) return '';
  const co = ld.coCaptains && ld.coCaptains.length
    ? `<p><b>Co-Captains:</b> ${ld.coCaptains.map(c=>`${leaderName(c.name)} <span class="azm">(${esc(c.years)})</span>`).join(', ')}</p>`
    : '';
  return `<div class="leadership"><h4>Leadership</h4>
    <p><b>Captain:</b> ${leaderName(ld.captain)}</p>
    ${co}</div>`;
}

const TL_YEARS = Array.from({length:15},(_,i)=>2012+i);
function franchiseTimeline(){
  const colOf = y => (y-2012)+2;
  const head = `<div class="tlg-cell tlg-head tlg-name" style="grid-row:1;grid-column:1">Franchise</div>` +
    TL_YEARS.map(y=>`<div class="tlg-cell tlg-head" style="grid-row:1;grid-column:${colOf(y)}">${y}</div>`).join('');
  const rows = FRANCHISE_TIMELINE.map((fr,i)=>{
    const r = i+2;
    const isLive = !!TEAMS[fr.full];
    const hasPage = isLive || FRANCHISE_SUMMARY.some(d=>d.f===null && d.full===fr.full);
    const logo = isLive ? TEAMS[fr.full].logo : (DB.franchiseLogos||{})[fr.nick];
    const nameEl = hasPage
      ? `<button class="pname" data-t="${esc(fr.full)}">${esc(fr.full)}</button>`
      : `<span>${esc(fr.full)}</span>`;
    const color = teamAccent(fr.full) || '#8a90a0';
    const band = `<div class="tlg-band${i%2?' even':''}" style="grid-row:${r};grid-column:1/-1"></div>`;
    const nameCell = `<div class="tlg-cell tlg-name" style="grid-row:${r};grid-column:1">
      ${logo?`<img class="tl-logo" src="${logo}" alt="">`:'<span class="tl-logo tl-logo-blank"></span>'}${nameEl}</div>`;
    const bars = fr.eras.map(e=>{
      const range = e.from===e.to ? `${e.from}` : `${e.from}–${e.to}`;
      return `<div class="tlg-bar" style="grid-row:${r};grid-column:${colOf(e.from)}/${colOf(e.to)+1};--bc:${color}"
        title="${esc(range+' · '+e.loc+' '+e.nick)}">${esc(e.nick)}</div>`;
    }).join('');
    return band + nameCell + bars;
  }).join('');
  return `<div class="tl-wrap"><h3 class="hsub">Franchise Name History</h3>
    <p class="lead">Every name each franchise has played under since the league began in 2012. Hover a bar for the full name.</p>
    <div class="tlg-scroll"><div class="tlg-grid">${head}${rows}</div></div></div>`;
}

function teamStatTable(cols, rows){
  const th=cols.map(([k,l,s])=>`<th class="${s==='r'?'mono':''} ${s==='s'?'lft':''}">${l}</th>`).join('');
  const body=rows.map(r=>'<tr>'+cols.map(([k,l,s],i)=>{
    if(i===0) return `<td class="lft"><button class="pname" data-t="${esc(r.name)}">${esc(r.name)}</button></td>`;
    return `<td class="${s==='r'?'mono':''}">${cell(r[k],s,k)}</td>`;
  }).join('')+'</tr>').join('');
  return `<div class="tscroll"><table class="dir sortable"><thead><tr>${th}</tr></thead><tbody>${body}</tbody></table></div>`;
}
function renderTeams(){
  setNav('teams');
  const q = tQuery.toLowerCase();
  const match = (...s) => !q || s.some(x=>String(x||'').toLowerCase().includes(q));

  const sum = FRANCHISE_SUMMARY.filter(d=>match(d.t, d.f, d.full));
  const sumRows = sum.map(d=>{
    const dispName = d.f || d.full || d.t;
    const key = d.f || d.full;
    const link = key
      ? `<button class="pname" data-t="${esc(key)}">${esc(dispName)}</button>` : esc(dispName);
    const logo = (d.f && TEAMS[d.f] && TEAMS[d.f].logo) || (DB.franchiseLogos||{})[d.t];
    return `<tr>
      <td class="lft">${logo?`<img class="fdotlogo" src="${logo}" alt="">`:''}${link}</td>
      <td>${d.w}</td><td>${d.l}</td><td class="mono">${rate(d.pct)}</td>
      <td class="lft">${esc(d.yr)}</td>
      <td>${d.ws}</td><td>${d.wsa}</td><td>${d.dv}</td><td>${d.po}</td><td>${d.wsz}</td><td>${d.as}</td>
      <td class="mono">${esc(d.por)}</td></tr>`;
  }).join('');
  const summaryTable = `<div class="tscroll"><table class="dir sortable"><thead><tr>
    <th class="lft">Team</th><th>W</th><th>L</th><th class="mono">PCT</th><th class="lft">Years</th>
    <th title="World Series titles">WS</th><th title="World Series appearances">WS App</th>
    <th title="Division titles">Div</th><th title="Playoff appearances">PO</th>
    <th title="Winning seasons">Win Sz</th><th title="All-Star selections">AS</th>
    <th class="mono" title="All-time playoff record">PO Rec</th>
  </tr></thead><tbody>${sumRows}</tbody></table></div>`;

  let statRows = TEAMNAMES.map(teamRowVals);
  if(q) statRows = statRows.filter(r=>match(r.name));
  statRows.sort((a,b)=>b.W-a.W);

  app.innerHTML = `
    ${franchiseTimeline()}
    <div class="controls">
      <div class="search">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/></svg>
        <input id="tq" type="search" placeholder="Search franchises…" value="${esc(tQuery)}">
      </div>
    </div>
    <h3 class="hsub">Franchise Summary</h3>
    ${summaryTable}
    <p class="note">Full franchise history from the league's records (2012–present), including seasons
    before the stat database. WS = World Series titles; WS App = finals appearances; Div = division titles;
    PO = playoff appearances; Win Sz = winning seasons; AS = All-Star selections; PO Rec = all-time
    playoff game record. Click a header to sort; names link to the current franchise page.</p>
    <h3 class="hsub">All-Time Team Batting</h3>
    ${teamStatTable(T_BAT_COLS, statRows)}
    <h3 class="hsub">All-Time Team Pitching</h3>
    ${teamStatTable(T_PIT_COLS, statRows)}
    <p class="note">Batting and pitching are the sum of every season's roster lines, regular season,
    ${RANGE} — so the totals cover the stat-database era only and won't match the pre-2017 win totals above.
    Open a team for year-by-year detail.</p>`;
  const qi=document.getElementById('tq');
  qi.addEventListener('input',e=>{ tQuery=e.target.value; const p=qi.selectionStart; renderTeams();
    const n=document.getElementById('tq'); n.focus(); n.setSelectionRange(p,p); });
  app.querySelectorAll('.pname[data-t]').forEach(b=>b.addEventListener('click',()=>{
    teamYear=null; location.hash='#/t/'+encodeURIComponent(b.dataset.t);
  }));
  document.querySelectorAll('table.sortable').forEach(makeSortable);
}

/* ------------------------------ STANDINGS ------------------------------ */
const ALL_YEARS = [...new Set(TEAMNAMES.flatMap(n=>TEAMS[n].years))].sort((a,b)=>a-b);
const LATEST_YEAR = Math.max(...ALL_YEARS);
let standYear = null, standPhase = 'reg';
let divYear = null;

function standRow(name, y){
  const s = (TEAMS[name].seasons||{})[y];
  if(!s) return null;
  const g = (s.games||[]).filter(x=>x.phase==='Regular');
  if(!g.length) return null;
  const r = {name, W:0, L:0, T:0, RF:0, RA:0, hW:0, hL:0, aW:0, aL:0, vs:{}};
  g.forEach(x=>{
    r[x.res]++; r.RF+=x.rf; r.RA+=x.ra;
    if(x.ha==='H'){ if(x.res==='W') r.hW++; else if(x.res==='L') r.hL++; }
    else          { if(x.res==='W') r.aW++; else if(x.res==='L') r.aL++; }
    const v = r.vs[x.opp] || (r.vs[x.opp]={W:0,L:0,T:0});
    v[x.res]++;
  });
  r.PCT = (r.W+r.L) ? r.W/(r.W+r.L) : 0;
  r.DIFF = r.RF - r.RA;
  return r;
}

/* the league realigned divisions in 2021 (North -> Brookside, South -> Brentwood)
   — one continuous division under two names, same idea as a franchise name change.
   Canonical key is always the current name; divisionEraName recovers whichever
   name DB.divisions actually used for a given year. */
const DIVISION_ALIAS = { North:'Brookside', South:'Brentwood' };
const canonicalDivision = dn => DIVISION_ALIAS[dn] || dn;
function divisionEraName(canonical, year){
  if(canonical==='Brookside' && year<2021) return 'North';
  if(canonical==='Brentwood' && year<2021) return 'South';
  return canonical;
}
const PLAYOFFS = DB.playoffs || {};
/* which postseason round a game belongs to: the two division series (named
   "Wild Card" through 2024, "Divisional Series" from 2025 on) or the Final
   (branded "World Series"), determined by matching the two teams against
   that year's bracket rather than trusting any stored round field */
function playoffRound(year, teamA, teamB){
  const p = PLAYOFFS[String(year)];
  if(!p || !teamA || !teamB) return 'Playoffs';
  const pair = new Set([teamA, teamB]);
  const isDivRound = side => {
    const seeds = (p[side]||{}).seeds || [];
    const fulls = new Set(seeds.map(s=>s.full).filter(Boolean));
    return fulls.size===2 && seeds.length===2 && [...fulls].every(f=>pair.has(f));
  };
  if(isDivRound('brookside') || isDivRound('brentwood')) return year>=2025 ? 'Divisional Series' : 'Wild Card';
  return 'World Series';
}
function gameTag(g){
  if(g.phase!=='Playoffs') return phLabel(g.phase);
  const raw = g.away ? g : (g.gid && GAMES[g.gid]);
  return raw ? playoffRound(+raw.date.slice(0,4), raw.away.team, raw.home.team) : 'Playoffs';
}
function pbTeam(seedNo, t, isWin, year){
  const full = t.full && TEAMS[t.full] ? t.full : null;
  const col = full ? teamAccent(full) : 'var(--line-strong)';
  const nm = full ? histName(full, year) : t.nick;
  const logo = full ? teamLogoForYear(full, year) : null;
  const mark = logo ? `<img class="pblogo" src="${logo}" alt="">` : `<span class="dot"></span>`;
  const label = full
    ? `<button class="pname" data-t="${esc(full)}">${esc(nm)}</button>`
    : `<span class="nm">${esc(nm)}</span>`;
  return `<div class="pb-row${isWin?' win':''}" style="--cd:${col}">
    ${seedNo?`<span class="sd">${seedNo}</span>`:''}${mark}${label}</div>`;
}
/* the playoff bracket's series scores (p[side].series / p.finalSeries) are just [rf,ra]
   tuples with no game id — find the actual box scores by matching phase+year+team-pair
   against GAMES, in date order (a series' games are always listed in the order played).
   Only used to link when the count lines up with the recorded series length; a year with
   thinner playoff box-score data than its series summary just falls back to plain text. */
function seriesGids(year, teamA, teamB){
  if(!teamA || !teamB) return [];
  const pair = new Set([teamA, teamB]);
  return GIDS.filter(gid=>{
    const g = GAMES[gid];
    return g.phase==='Playoffs' && +g.date.slice(0,4)===year
      && pair.has(g.away.team) && pair.has(g.home.team) && g.away.team!==g.home.team;
  }).sort((a,b)=>(GAMES[a].dt||GAMES[a].date).localeCompare(GAMES[b].dt||GAMES[b].date));
}
/* Which side's score comes first in a games[i] tuple turns out NOT to follow a fixed
   rule — checked several years against the actual box scores and some list the
   eventual series winner's score first, others the loser's, with no consistent
   pattern by bracket side either. So the winner shown per game is read off the real,
   matched GAMES entry (away/home + R), never inferred from the tuple's own order —
   the tuple is only used for the plain-text fallback when a game couldn't be matched. */
function pbScore(games, gids, year, seriesKey){
  if(!games || !games.length) return '';
  const linked = gids && gids.length===games.length;
  const seriesRow = seriesKey
    ? `<div class="pb-score-row"><button class="pname" data-series="${year}|${seriesKey}">Full series →</button></div>` : '';
  return `<div class="pb-score">${games.map((g,i)=>{
    let winner = null;
    if(linked){
      const gm = GAMES[gids[i]];
      const wTeam = gm.away.R>gm.home.R ? gm.away.team : gm.home.team;
      winner = TEAMS[wTeam] ? histNick(wTeam, year) : wTeam;
    }
    const label = `Game ${i+1}: ${g[0]}–${g[1]}${winner?` (${esc(winner)})`:''}`;
    return `<div class="pb-score-row">${linked ? `<button class="pname" data-g="${gids[i]}">${label}</button>` : label}</div>`;
  }).join('')}${seriesRow}</div>`;
}
function pbMatch(title, rows, score){
  return `<div class="pb-match">${title?`<h5>${esc(title)}</h5>`:''}${rows}${score||''}</div>`;
}
function playoffBracket(year){
  const p = PLAYOFFS[String(year)];
  if(!p) return '';
  const round1 = year>=2025 ? 'Divisional Series' : 'Wild Card';
  const poLogo = (DB.postseasonLogos||{})[year];
  const wsLogo = (DB.worldSeriesLogos||{})[year];
  const semi = side => {
    const teamA = p[side].seeds[0] && p[side].seeds[0].full, teamB = p[side].seeds[1] && p[side].seeds[1].full;
    return pbMatch(side==='brookside'?'Brookside':'Brentwood',
      p[side].seeds.map((t,i)=>pbTeam(i+1, t, t.nick===p[side].winner, year)).join(''),
      pbScore(p[side].series, seriesGids(year, teamA, teamB), year, side));
  };
  const winOf = side => (p[side].seeds.find(t=>t.nick===p[side].winner)) || {nick:p[side].winner, full:null};
  const finalists = [winOf('brookside'), winOf('brentwood')];
  const finalRows = finalists.map(t=>pbTeam(null, t, t.nick===p.champion, year)).join('');
  const finalGids = seriesGids(year, finalists[0] && finalists[0].full, finalists[1] && finalists[1].full);
  const champFull = p.championFull && TEAMS[p.championFull] ? p.championFull : null;
  const champCol = FRANCHISE_COLORS[champFull] || {};
  const champLabel = champFull
    ? `<button class="pname" data-t="${esc(champFull)}">${esc(histName(champFull, year))}</button>`
    : esc(p.champion);
  const champLogo = champFull ? teamLogoForYear(champFull, year) : null;
  return `<div class="pbwrap"><div class="pbracket">
      <div class="pb-lanehead" style="grid-column:1">
        ${poLogo?`<img class="pbicon" src="${poLogo}" alt="">`:''}
        <h4 class="pbround">${esc(round1)}</h4>
      </div>
      <div class="pb-col" style="grid-column:1">
        ${semi('brookside')}
        ${semi('brentwood')}
      </div>
      <div class="pb-conn merge" style="grid-column:2"></div>
      <div class="pb-lanehead" style="grid-column:3">
        ${wsLogo?`<img class="pbicon" src="${wsLogo}" alt="">`:''}
        <h4 class="pbround">World Series</h4>
      </div>
      <div class="pb-col" style="grid-column:3">${pbMatch('', finalRows, pbScore(p.finalSeries, finalGids, year, 'final'))}</div>
      <div class="pb-conn line" style="grid-column:4"></div>
      <div class="pb-col" style="grid-column:5"><div class="pb-trophy"${champCol.p?` style="--tp:${champCol.p};--ts:${champCol.s}"`:''}>
        <span class="tl">${TROPHY} Champion</span>
        <div class="pb-champrow">${champLogo?`<img class="pbtrophylogo" src="${champLogo}" alt="">`:''}<span class="tn">${champLabel}</span></div>
      </div></div>
    </div></div>`;
}

/* One page per playoff series (round-1 division/wild-card series, or the
   World Series) — every game plus each side's combined batting/pitching
   across just those games, baseball-reference-postseason-page style.
   roundKey matches exactly what a team page's Playoffs column links to:
   'brookside'/'brentwood' for a round-1 series, 'final' for the WS. */
function renderSeries(year, roundKey){
  setNav('standings');
  const p = PLAYOFFS[String(year)];
  if(!p){ location.hash='#/standings'; return; }
  let teamA, teamB, roundLabel, winnerFull;
  if(roundKey==='final'){
    const finalists = ['brookside','brentwood'].map(sk=>{
      const sd = p[sk] || {};
      return (sd.seeds||[]).find(s=>s.nick===sd.winner) || {nick:sd.winner, full:null};
    });
    [teamA, teamB] = finalists;
    roundLabel = 'World Series';
    winnerFull = p.championFull;
  } else if(roundKey==='brookside' || roundKey==='brentwood'){
    const side = p[roundKey];
    if(!side || !side.seeds || side.seeds.length<2){ location.hash='#/standings'; return; }
    [teamA, teamB] = side.seeds;
    roundLabel = `${year>=2025?'Divisional Series':'Wild Card'} · ${roundKey==='brookside'?'Brookside':'Brentwood'} Bracket`;
    const w = side.seeds.find(s=>s.nick===side.winner);
    winnerFull = w && w.full;
  } else { location.hash='#/standings'; return; }
  if(!teamA || !teamB || !teamA.full || !teamB.full){ location.hash='#/standings'; return; }

  const gids = seriesGids(year, teamA.full, teamB.full);
  if(!gids.length){
    /* no box scores matched (mostly 2017-era games) — still show what the
       bracket itself knows (who played, who won) rather than bounce the
       user back to Standings with no explanation */
    const winnerName = winnerFull ? histName(winnerFull, year) : null;
    app.innerHTML = `
      <button class="back" id="back">← Standings</button>
      <div class="phead">
        <h2>${histTeamLink(teamA.full, year)}<span class="vs">vs</span>${histTeamLink(teamB.full, year)}</h2>
        <span class="yrs">${year} ${esc(roundLabel)}${winnerName?` · ${esc(winnerName)} won`:''}</span>
      </div>
      <p class="empty">No box scores on record for this series — this era predates per-game logging.</p>`;
    document.getElementById('back').addEventListener('click',()=>{ location.hash='#/standings'; });
    app.querySelectorAll('.pname[data-t]').forEach(b=>b.addEventListener('click',()=>{
      location.hash='#/t/'+encodeURIComponent(b.dataset.t); }));
    return;
  }
  let aWins=0, bWins=0;
  const gameRows = gids.map((gid,i)=>{
    const g = GAMES[gid];
    const aIsAway = g.away.team===teamA.full;
    const aR = aIsAway?g.away.R:g.home.R, bR = aIsAway?g.home.R:g.away.R;
    if(aR>bR) aWins++; else if(bR>aR) bWins++;
    return {i, gid, g, aR, bR};
  });
  /* the pitching decisions (W/L/SV) for one game, straight off whichever
     side's pit line actually carries a 1 in that column — at most one
     pitcher per game gets each, same as any real box score */
  function decisionsFor(g){
    const all = [...(g.away.pit||[]), ...(g.home.pit||[])];
    return {w: all.find(p=>p.w>0), l: all.find(p=>p.l>0), sv: all.find(p=>p.sv>0)};
  }
  /* a pitcher's postseason W-L/SV record through and including one game —
     real box scores show this next to each decision ("(1-0)", "(4)") — scoped
     to just that year's postseason (not regular season or career), matching
     how a running postseason record actually resets each October. Cached per
     pitcher since the same closer/starter often shows up in multiple games
     in the same series. */
  const tallyCache = {};
  function pitcherPostseasonTally(name){
    if(tallyCache[name]) return tallyCache[name];
    const pl = P[name];
    const map = new Map();
    if(pl){
      const games = collectPlayerGames(pl, 'Playoffs')
        .filter(r => r.pit && +r.g.date.slice(0,4)===year)
        .sort((a,b)=>((a.g.dt||a.g.date)).localeCompare(b.g.dt||b.g.date));
      let w=0,l=0,sv=0;
      games.forEach(r=>{
        w+=r.pit.w||0; l+=r.pit.l||0; sv+=r.pit.sv||0;
        map.set(String(r.g.gid), {w,l,sv});
      });
    }
    return tallyCache[name]=map;
  }
  const dateLabel = iso => { const d=new Date(iso+'T00:00:00');
    return d.toLocaleDateString('en-US', {month:'short', day:'numeric'}); };
  const gameRowHTML = (full, runs, win) => {
    const logo = TEAMS[full] ? teamLogoForYear(full, year) : null;
    return `<div class="pb-row${win?' win':''}" style="--cd:${teamAccent(full)||'var(--line-strong)'}">
      ${logo?`<img class="pblogo" src="${logo}" alt="">`:'<span class="dot"></span>'}
      ${histTeamLink(full, year)}<b class="gscore">${runs}</b></div>`;
  };
  const gamesHTML = `<div class="game-cards">${gameRows.map(r=>{
    const dec = decisionsFor(r.g);
    const decRow = (tag, p, fmt) => {
      if(!p) return '';
      const t = pitcherPostseasonTally(p.n).get(String(r.gid));
      const rec = t ? ` <span class="azm">(${fmt(t)})</span>` : '';
      return `<div class="pb-score-row"><b>${tag}</b> ${plink(p.n)}${rec}</div>`;
    };
    return `<div class="pb-match">
      <h5>Game ${r.i+1} · ${esc(dateLabel(r.g.date))}</h5>
      ${gameRowHTML(teamA.full, r.aR, r.aR>r.bR)}
      ${gameRowHTML(teamB.full, r.bR, r.bR>r.aR)}
      <div class="pb-score">
        ${decRow('W', dec.w, t=>`${t.w}-${t.l}`)}
        ${decRow('L', dec.l, t=>`${t.w}-${t.l}`)}
        ${decRow('S', dec.sv, t=>`${t.sv}`)}
        <div class="pb-score-row"><button class="pname pb-boxlink" data-g="${r.gid}">Box score →</button></div>
      </div>
    </div>`;
  }).join('')}</div>`;

  /* combine this series' own games into one roster per side — same shape
     rosterBatting/rosterPitching already expect from the ASG/team pages */
  function seriesRoster(teamFull){
    const acc = {};
    gameRows.forEach(({g})=>{
      const side = g.away.team===teamFull ? g.away : (g.home.team===teamFull ? g.home : null);
      if(!side) return;
      (side.bat||[]).forEach(b=>{
        const a = acc[b.n] || (acc[b.n]={name:b.n, rows:[]});
        a.rows.push(gameBatRow(b));
      });
      (side.pit||[]).forEach(pt=>{
        const a = acc[pt.n] || (acc[pt.n]={name:pt.n, rows:[]});
        a.rows.push(gamePitRow(pt));
      });
    });
    return Object.values(acc).map(a=>({name:a.name, series: sumRows(a.rows)}));
  }
  const weights = [{year, pa:1, post:true}];
  const pitWeights = [{year, outs:1, post:true}];
  const statsFor = (teamFull, label) => {
    const roster = seriesRoster(teamFull);
    return rosterBatting(roster, 'series', label, weights) + rosterPitching(roster, 'series', label, pitWeights);
  };

  const winnerName = winnerFull ? histName(winnerFull, year) : null;
  const hero = `<div class="phead">
      <h2>${histTeamLink(teamA.full, year)}<span class="vs">${aWins}–${bWins}</span>${histTeamLink(teamB.full, year)}</h2>
      <span class="yrs">${year} ${esc(roundLabel)}${winnerName?` · ${esc(winnerName)} won`:''}</span>
    </div>`;

  app.innerHTML = `
    <button class="back" id="back">← Standings</button>
    ${hero}
    <h3 class="hsub">Games</h3>
    ${gamesHTML}
    <h3 class="hsub">${esc(histName(teamA.full,year))}</h3>
    ${statsFor(teamA.full, histName(teamA.full,year))}
    <h3 class="hsub">${esc(histName(teamB.full,year))}</h3>
    ${statsFor(teamB.full, histName(teamB.full,year))}
    <p class="note">Combined batting and pitching from this series' own games only — click a game above for its
    full box score. OPS+ compares against ${year}'s own postseason league average.</p>`;
  document.getElementById('back').addEventListener('click',()=>{ location.hash='#/standings'; });
  app.querySelectorAll('.pname[data-g]').forEach(b=>b.addEventListener('click',()=>{
    location.hash='#/g/'+b.dataset.g; }));
  app.querySelectorAll('.pname[data-t]').forEach(b=>b.addEventListener('click',()=>{
    location.hash='#/t/'+encodeURIComponent(b.dataset.t); }));
  app.querySelectorAll('.pname[data-p]').forEach(b=>b.addEventListener('click',()=>{
    location.hash='#/p/'+encodeURIComponent(b.dataset.p); }));
  document.querySelectorAll('table.sortable').forEach(makeSortable);
}

function renderStandings(){
  setNav('standings');
  const yrs = ALL_YEARS.filter(y=>TEAMNAMES.some(n=>standRow(n,y)));
  if(!yrs.includes(standYear)) standYear = yrs[yrs.length-1];
  const chips = `<div class="chips">${yrs.map(y=>
    `<button data-sy="${y}" aria-pressed="${standYear===y}">${y}</button>`).join('')}</div>`;
  let rows = TEAMNAMES.map(n=>standRow(n, standYear)).filter(Boolean)
    .sort((a,b)=> b.PCT-a.PCT || b.DIFF-a.DIFF);
  const gbf = lead => r => {
    const v = ((lead.W - r.W) + (r.L - lead.L)) / 2;
    return v<=0 ? '—' : (Number.isInteger(v)? v : v.toFixed(1));
  };
  const seedMark = { '^':'<sup class="seed z" title="division winner">z</sup>',
                     '*':'<sup class="seed x" title="clinched playoff berth">x</sup>' };
  const DIVS = (DB.divisions||{})[standYear];
  const divNames = DIVS ? Object.keys(DIVS) : [];
  const divSet = Object.fromEntries(divNames.map(dn=>[dn, new Set(DIVS[dn].map(([t])=>t))]));
  const vsRec = (r, dn) => {
    let w=0,l=0; for(const opp in r.vs){ if(divSet[dn].has(opp)){ w+=r.vs[opp].W; l+=r.vs[opp].L; } }
    return `${w}–${l}`;
  };
  // head-to-head win diff between two tied teams (pairwise)
  const h2h = (a,b) => { const v=a.vs[b.name]||{W:0,L:0}; return v.W-v.L; };
  const divSort = (a,b) => (b.PCT-a.PCT) || (-h2h(a,b)) || (b.DIFF-a.DIFF);

  const stMark = n => { const lg=teamLogoForYear(n, standYear); return lg
    ? `<img class="stlogo" src="${lg}" alt="">`
    : `<span class="clubdot" style="--cd:${teamAccent(n)||'var(--line-strong)'}"></span>`; };
  const trow = (r,i,gb,mk)=>`<tr>
    <td class="lft"><span class="rk">${i+1}</span>${stMark(r.name)}<button class="pname" data-t="${esc(r.name)}">${esc(histName(r.name, standYear))}</button>${seedMark[mk]||''}</td>
    <td>${r.W}</td><td>${r.L}</td>
    <td class="mono">${rate(r.PCT)}</td><td class="mono">${gb(r)}</td>
    <td>${r.RF}</td><td>${r.RA}</td>
    <td class="mono ${r.DIFF>0?'pos':r.DIFF<0?'neg':''}">${r.DIFF>0?'+':''}${r.DIFF}</td>
    <td class="mono">${r.hW}–${r.hL}</td><td class="mono">${r.aW}–${r.aL}</td>
    ${divNames.map(dn=>`<td class="mono">${vsRec(r,dn)}</td>`).join('')}</tr>`;
  const thead = `<thead><tr>
      <th class="lft">Team</th><th>W</th><th>L</th><th class="mono">PCT</th><th class="mono">GB</th>
      <th>RF</th><th>RA</th><th class="mono">Diff</th><th class="mono">Home</th><th class="mono">Away</th>
      ${divNames.map(dn=>`<th class="mono">vs ${esc(dn.slice(0,3))}</th>`).join('')}
    </tr></thead>`;
  let standHTML;
  if(DIVS){
    const used=new Set();
    standHTML = divNames.map(dn=>{
      const order = DIVS[dn];
      const drows = order.map(([tm])=>rows.find(r=>r.name===tm)).filter(Boolean);
      const mk = Object.fromEntries(order.map(([tm,m])=>[tm,m]));
      drows.sort(divSort);
      drows.forEach(r=>used.add(r.name));
      const gb = gbf(drows[0]||{W:0,L:0});
      const dlogo = (DB.divisionLogos||{})[dn];
      const isDiv = /^(North|South|Brookside|Brentwood)$/.test(dn);
      const dnLabel = `${esc(dn)}${isDiv?' Division':''}`;
      return `<h4 class="divh">${dlogo?`<img class="divlogo" src="${dlogo}" alt="">`:''}${
        isDiv ? `<button type="button" class="pname divlink" data-div="${esc(canonicalDivision(dn))}">${dnLabel}</button>` : dnLabel}</h4>
        <div class="tscroll"><table class="dir stand">${thead}
        <tbody>${drows.map((r,i)=>trow(r,i,gb,mk[r.name])).join('')}</tbody></table></div>`;
    }).join('');
    const leftover = rows.filter(r=>!used.has(r.name));
    if(leftover.length){
      const gb=gbf(leftover[0]);
      standHTML += `<h4 class="divh">Other</h4><div class="tscroll"><table class="dir stand">${thead}
        <tbody>${leftover.map((r,i)=>trow(r,i,gb)).join('')}</tbody></table></div>`;
    }
  } else {
    const gb=gbf(rows[0]);
    standHTML = `<div class="tscroll"><table class="dir stand">${thead}
      <tbody>${rows.map((r,i)=>trow(r,i,gb)).join('')}</tbody></table></div>`;
  }

  const phKey = standPhase==='post' ? 'playoffs' : 'regular';
  const agg = rows.map(r=>{
    const s=(TEAMS[r.name].seasons||{})[standYear];
    const ph=((s&&s.roster)||[]).filter(e=>e[phKey]).map(e=>e[phKey]);
    return {name:r.name, made:ph.length>0, ...sumRows(ph)};
  }).filter(a=> standPhase==='reg' || a.made);
  const nk = n => `<button class="pname" data-t="${esc(n)}">${esc(histName(n, standYear))}</button>`;
  const league = sumRows(agg);
  const phaseLabel = standPhase==='post' ? 'Postseason' : 'Regular Season';
  const teamPhaseToggle = `<div class="segs post" role="group" aria-label="Team stats phase">
    <button data-sp="reg" aria-pressed="${standPhase==='reg'}">Regular</button>
    <button data-sp="post" aria-pressed="${standPhase==='post'}">Playoffs</button></div>`;
  const batT = statTable('Team Batting · '+standYear+' · '+phaseLabel, [
    {l:'Team',lft:1,f:d=>nk(d.name)},
    {l:'PA',f:d=>d.PA},{l:'AB',f:d=>d.AB},{l:'R',f:d=>d.R},{l:'H',f:d=>d.H},
    {l:'2B',f:d=>d['2B']},{l:'3B',f:d=>d['3B']},{l:'HR',f:d=>d.HR},{l:'RBI',f:d=>d.RBI},
    {l:'BB',f:d=>d.BB},{l:'K',f:d=>d.K},
    {l:'AVG',m:1,f:d=>rate(avg(d))},{l:'OBP',m:1,f:d=>rate(obp(d))},
    {l:'SLG',m:1,f:d=>rate(slg(d))},{l:'OPS',m:1,f:d=>rate(ops(d))},
    {l:'OPS+',m:1,f:d=>{const v=opsPlusFor(d, [{year:standYear, pa:d.PA, post:standPhase==='post'}]);return isFinite(v)?String(v):'—';}}], agg, league, 'League', '', true);
  const pitT = statTable('Team Pitching · '+standYear+' · '+phaseLabel, [
    {l:'Team',lft:1,f:d=>nk(d.name)},
    {l:'IP',m:1,f:d=>ipStr(d.IPouts)},{l:'R',f:d=>d.pR},{l:'ER',f:d=>d.ER},
    {l:'H',f:d=>d.pH},{l:'BB',f:d=>d.pBB},{l:'K',f:d=>d.pK},{l:'W',f:d=>d.W},{l:'L',f:d=>d.L},
    {l:'ERA',m:1,f:d=>two(era(d))},{l:'WHIP',m:1,f:d=>two(whip(d))},{l:'K/3',m:1,f:d=>two(k9(d))},
    {l:'ERA+',m:1,f:d=>{const v=eraPlusFor(d, [{year:standYear, outs:d.IPouts, post:standPhase==='post'}]);return isFinite(v)?String(v):'—';}}],
    agg, league, 'League', '', true);

  app.innerHTML = `
    <div class="phead"><h2>Standings</h2><span class="yrs">Regular season · ${standYear}</span></div>
    ${chips}
    ${standHTML}
    ${DIVS?'<p class="lead"><sup class="seed z">z</sup> division winner &nbsp; <sup class="seed x">x</sup> clinched playoff berth</p>':''}
    ${PLAYOFFS[String(standYear)]?`<h3 class="divh">${standYear} Playoffs</h3>${playoffBracket(standYear)}`:''}
    <h3 class="hsub">Team Stats</h3>
    ${teamPhaseToggle}
    ${batT}${pitT}
    <p class="note">Regular-season standings from official game results. GB is games behind the division leader;
    RF / RA are runs for and against; Diff is their difference; Home and Away are the split records;
    the trailing columns are the club's record against each division. Division ties are broken by head-to-head.
    Team Batting and Team Pitching are the sum of that season's roster lines for the selected phase above;
    the Playoffs view only lists teams that made the postseason that year.
    Clubs are shown by the name they used that season; the link opens the current franchise page.</p>`;
  app.querySelectorAll('.chips button').forEach(b=>b.addEventListener('click',()=>{ standYear=+b.dataset.sy; renderStandings(); }));
  app.querySelectorAll('[data-sp]').forEach(b=>b.addEventListener('click',()=>{ standPhase=b.dataset.sp; renderStandings(); }));
  app.querySelectorAll('[data-div]').forEach(b=>b.addEventListener('click',()=>{
    location.hash='#/div/'+encodeURIComponent(b.dataset.div); }));
  app.querySelectorAll('.pname[data-t]').forEach(b=>b.addEventListener('click',()=>{
    teamYear=null; location.hash='#/t/'+encodeURIComponent(b.dataset.t); }));
  app.querySelectorAll('.pname[data-g]').forEach(b=>b.addEventListener('click',()=>{
    location.hash='#/g/'+b.dataset.g; }));
  app.querySelectorAll('.pname[data-series]').forEach(b=>b.addEventListener('click',()=>{
    const [yy,rk] = b.dataset.series.split('|'); location.hash = '#/series/'+yy+'/'+rk; }));
}

/* ------------------------------ DIVISION PAGES ------------------------------
   Not linked from the Teams directory (the user asked to keep it off there) —
   reached from a division header on Standings or a division-logo pennant on a
   Team's Accolades. Brookside/Brentwood only; North/South (2017–2020) are the
   same two divisions under their old names (canonicalDivision unifies them),
   same idea as a franchise surviving a name change. */
function renderDivision(canonical){
  if(!['Brookside','Brentwood'].includes(canonical)){ location.hash='#/standings'; return; }
  setNav('standings');
  const years = ALL_YEARS.filter(y=>{
    const divs=(DB.divisions||{})[y]; return divs && divs[divisionEraName(canonical,y)];
  });
  if(!years.length){ location.hash='#/standings'; return; }
  if(!divYear || !years.includes(divYear)) divYear = years[years.length-1];

  const eraName = divisionEraName(canonical, divYear);
  const order = ((DB.divisions[divYear]||{})[eraName]) || [];
  const mk = Object.fromEntries(order.map(([tm,m])=>[tm,m]));
  const seedMark = { '^':'<sup class="seed z" title="division winner">z</sup>',
                     '*':'<sup class="seed x" title="clinched playoff berth">x</sup>' };
  const h2h = (a,b) => { const v=a.vs[b.name]||{W:0,L:0}; return v.W-v.L; };
  const divSort = (a,b) => (b.PCT-a.PCT) || (-h2h(a,b)) || (b.DIFF-a.DIFF);
  const rows = order.map(([tm])=>standRow(tm, divYear)).filter(Boolean).sort(divSort);
  const gbf = lead => r => {
    const v = ((lead.W - r.W) + (r.L - lead.L)) / 2;
    return v<=0 ? '—' : (Number.isInteger(v)? v : v.toFixed(1));
  };
  const gb = gbf(rows[0]||{W:0,L:0});
  const stMark = n => { const lg=teamLogoForYear(n, divYear); return lg
    ? `<img class="stlogo" src="${lg}" alt="">`
    : `<span class="clubdot" style="--cd:${teamAccent(n)||'var(--line-strong)'}"></span>`; };
  const trow = (r,i)=>`<tr>
    <td class="lft"><span class="rk">${i+1}</span>${stMark(r.name)}<button class="pname" data-t="${esc(r.name)}">${esc(histName(r.name, divYear))}</button>${seedMark[mk[r.name]]||''}</td>
    <td>${r.W}</td><td>${r.L}</td>
    <td class="mono">${rate(r.PCT)}</td><td class="mono">${gb(r)}</td>
    <td>${r.RF}</td><td>${r.RA}</td>
    <td class="mono ${r.DIFF>0?'pos':r.DIFF<0?'neg':''}">${r.DIFF>0?'+':''}${r.DIFF}</td>
    <td class="mono">${r.hW}–${r.hL}</td><td class="mono">${r.aW}–${r.aL}</td></tr>`;
  const thead = `<thead><tr>
      <th class="lft">Team</th><th>W</th><th>L</th><th class="mono">PCT</th><th class="mono">GB</th>
      <th>RF</th><th>RA</th><th class="mono">Diff</th><th class="mono">Home</th><th class="mono">Away</th>
    </tr></thead>`;
  const standTable = `<div class="tscroll"><table class="dir stand">${thead}<tbody>${rows.map((r,i)=>trow(r,i)).join('')}</tbody></table></div>`;
  const chips = `<div class="chips">${years.map(y=>
    `<button data-dy="${y}" aria-pressed="${divYear===y}">${y}</button>`).join('')}</div>`;

  // ---- division champions: the '^' team every year on record ----
  const champYears = years.filter(y=>{
    const era=divisionEraName(canonical,y);
    return ((DB.divisions[y]||{})[era]||[]).some(([,m])=>m==='^');
  });
  const champRow = y=>{
    const era=divisionEraName(canonical,y);
    const entry = ((DB.divisions[y]||{})[era]||[]).find(([,m])=>m==='^');
    const tm = entry && entry[0];
    if(!tm || !TEAMS[tm]) return '';
    const logo = teamLogoForYear(tm, y);
    const r = standRow(tm, y);
    return `<li>${logo?`<img class="snaplogo" src="${logo}" alt="">`:'<span class="snaplogo" style="background:var(--line)"></span>'}
      <button class="pname" data-t="${esc(tm)}">${esc(histName(tm, y))}</button>
      <span class="dy">${y}</span>${r?`<b>${r.W}–${r.L}</b>`:''}</li>`;
  };
  const champsHTML = champYears.length ? `<h3 class="hsub">Division Champions</h3>
    <ol class="divchamps">${champYears.slice().reverse().map(champRow).join('')}</ol>` : '';

  // ---- All-Star Game history + selections for this division's squad ----
  const stripDiv = t => t.replace(/ Division$/,'');
  const asgSquadFor = y => {
    const a = ASG[y]; if(!a) return null;
    return (a.squads||[]).find(s=>canonicalDivision(s.name)===canonical) || null;
  };
  const asgOppSquadFor = y => {
    const a = ASG[y]; if(!a) return null;
    return (a.squads||[]).find(s=>canonicalDivision(s.name)!==canonical) || null;
  };
  /* same name-normalization plink() already does (strip captain mark, drop
     periods, apply the same known alias) so a selections count merges
     with the exact P[] key plink()'s own roster links resolve to */
  const normASG = raw => {
    const disp = raw.replace(/\s*\(c\)\s*/ig,'').trim();
    let key = disp;
    if(!P[key]) key = disp.replace(/\./g,'');
    if(!P[key]) key = ({'Trevor Fraioli':'Trevor Meyler'})[disp]||disp;
    return key;
  };
  const asgYears = Object.keys(ASG).map(Number).filter(y=>asgSquadFor(y)).sort((a,b)=>b-a);
  const boxForASG = y => GIDS.find(id=>{
    const g=GAMES[id]; return g.phase==='AllStar' && g.date.slice(0,4)==y &&
      (canonicalDivision(stripDiv(g.away.team))===canonical || canonicalDivision(stripDiv(g.home.team))===canonical);
  });
  const asgWinnerName = y => { const w=(ASG[y]||{}).winner; return w ? w.trim().split(/\s+/)[0] : null; };

  let asgW=0, asgL=0;
  asgYears.forEach(y=>{
    const wn = asgWinnerName(y), our = asgSquadFor(y), opp = asgOppSquadFor(y);
    if(!wn || !our) return;
    if(wn===our.name) asgW++;
    else if(opp && wn===opp.name) asgL++;
  });
  const asgRecord = (asgW+asgL) ? `${asgW}–${asgL}` : null;

  const asgRows = asgYears.map(y=>{
    const opp = asgOppSquadFor(y);
    const gid = boxForASG(y);
    const wn = asgWinnerName(y);
    const our = asgSquadFor(y);
    const result = !wn ? null : wn===our.name ? 'W' : (opp && wn===opp.name ? 'L' : null);
    const scoreMatch = ((ASG[y]||{}).winner||'').match(/\d+\s*-\s*\d+/);
    return `<li>
      <span class="dy">${y}</span>
      <span class="asgvs">vs ${esc(opp?opp.name:'?')}</span>
      <span class="asgr">
        ${result?`<span class="res-${result}">${result}</span>`:''}
        ${scoreMatch?`<b>${esc(scoreMatch[0])}</b>`:''}
        ${gid?`<button class="pname" data-g="${gid}">box score →</button>`:''}
      </span>
    </li>`;
  }).join('');
  const asgHistoryHTML = asgYears.length ? `<h3 class="hsub">All-Star Game History</h3>
    <p class="pmeta">${asgRecord?`<b>${asgRecord}</b> all-time in the All-Star Game`:'No decided results on record'}
    (${asgYears[asgYears.length-1]}–${asgYears[0]}). <span class="cap">C</span> marks a squad captain.</p>
    <ol class="divchamps asglist">${asgRows}</ol>` : '';

  // ---- All-Star team captain history: one per squad per year, from the "(C)" marker
  //      already carried on that player's name in the squad roster ----
  const asgCaptainFor = y => {
    const sq = asgSquadFor(y);
    return sq ? (sq.players||[]).find(p=>/\(c\)/i.test(p)) || null : null;
  };
  const capRows = asgYears.map(y=>{
    const raw = asgCaptainFor(y);
    return raw ? `<li><span class="dy">${y}</span> ${plink(raw)}</li>` : '';
  }).join('');
  const asgCaptainsHTML = capRows ? `<h3 class="hsub">All-Star Team Captain History</h3>
    <p class="pmeta">Squad captain for this division's All-Star team, ${asgYears[asgYears.length-1]}–${asgYears[0]}.</p>
    <ol class="divchamps">${capRows}</ol>` : '';

  /* ---- All-Star Game stats: actual batting/pitching lines from the ASG box
     scores (GAMES, phase==='AllStar') for whichever side was this division —
     a fundamentally different source than the roster/regular-season stats a
     team page shows, since these games never touch a TEAMS roster at all ---- */
  const asgStatRows = {};
  GIDS.forEach(id=>{
    const g = GAMES[id]; if(g.phase!=='AllStar') return;
    ['away','home'].forEach(sk=>{
      const side = g[sk]; if(canonicalDivision(stripDiv(side.team))!==canonical) return;
      (side.bat||[]).forEach(b=>{
        const acc = asgStatRows[b.n] || (asgStatRows[b.n]={name:b.n, rows:[]});
        acc.rows.push(gameBatRow(b));
      });
      (side.pit||[]).forEach(p=>{
        const acc = asgStatRows[p.n] || (asgStatRows[p.n]={name:p.n, rows:[]});
        acc.rows.push(gamePitRow(p));
      });
    });
  });
  const asgRoster = Object.values(asgStatRows).map(a=>({name:a.name, asg: sumRows(a.rows)}));
  const asgBatHTML = rosterBatting(asgRoster, 'asg');
  const asgPitHTML = rosterPitching(asgRoster, 'asg');
  const asgStatsHTML = (asgBatHTML||asgPitHTML) ? `<h3 class="hsub">All-Star Game Stats</h3>
    <p class="pmeta">Combined lines from every recorded All-Star Game box score for this division, 2017 on
    (box scores don't reach back to 2013–2016).</p>
    ${asgBatHTML}${asgPitHTML}` : '';

  const selCount = {};
  asgYears.forEach(y=>{
    (asgSquadFor(y).players||[]).forEach(p=>{ const key=normASG(p); selCount[key]=(selCount[key]||0)+1; });
  });
  const selItems = Object.entries(selCount).map(([n,v])=>({n,v})).sort((a,b)=>b.v-a.v).slice(0,10);
  const selHTML = selItems.length ? `<h3 class="hsub">All-Star Selections</h3>
    <div class="llgrid">${llist('Most Selections', selItems, v=>v)}</div>` : '';

  // ---- every team that's ever called this division home ----
  const memberYears = {};
  years.forEach(y=>{
    const era = divisionEraName(canonical, y);
    ((DB.divisions[y]||{})[era]||[]).forEach(([tm])=>{ (memberYears[tm]=memberYears[tm]||[]).push(y); });
  });
  const members = Object.keys(memberYears).filter(tm=>TEAMS[tm])
    .sort((a,b)=> memberYears[b].length-memberYears[a].length);
  const memberRows = members.map(tm=>{
    const yrs = memberYears[tm];
    const span = yrs.length>1 ? `${yrs[0]}–${yrs[yrs.length-1]}` : `${yrs[0]}`;
    return `<tr><td class="lft">${TEAMS[tm].logo?`<img class="stlogo" src="${TEAMS[tm].logo}" alt="">`:''}
      <button class="pname" data-t="${esc(tm)}">${esc(tm)}</button></td>
      <td>${yrs.length}</td><td class="lft">${span}</td></tr>`;
  }).join('');
  const membersHTML = `<h3 class="hsub">Member Teams</h3>
    <div class="tscroll"><table class="dir"><thead><tr>
      <th class="lft">Team</th><th>Seasons</th><th class="lft">Years</th></tr></thead>
    <tbody>${memberRows}</tbody></table></div>`;

  const dlogo = (DB.divisionLogos||{})[canonical];
  const oldName = canonical==='Brookside' ? 'North' : 'South';
  const hadOldName = years.some(y=>y<2021);

  app.innerHTML = `
    <button class="back" id="back">← Standings</button>
    <div class="phead"><div class="hero-row">${dlogo?`<img class="tlogo" src="${dlogo}" alt="">`:''}<h2>${esc(canonical)} Division</h2></div>
    <span class="yrs">${years[0]}–${years[years.length-1]}${hadOldName?` · known as the ${oldName} Division through 2020`:''}</span></div>
    ${chips}
    ${standTable}
    <p class="lead"><sup class="seed z">z</sup> division winner &nbsp; <sup class="seed x">x</sup> clinched playoff berth</p>
    ${champsHTML}
    ${asgHistoryHTML}
    ${asgCaptainsHTML}
    ${asgStatsHTML}
    ${selHTML}
    ${membersHTML}
    <p class="note">Regular-season standings for this division only. Clubs are shown by the name they
    used that season; the link opens the current franchise page. Division Champions lists the regular-season
    winner marked <sup class="seed z">z</sup> above for every year on record. All-Star squads were North/South
    through 2021, then Brookside/Brentwood — matched here by division, not by name.</p>`;
  document.getElementById('back').addEventListener('click',()=>{ location.hash='#/standings'; });
  app.querySelectorAll('.chips button').forEach(b=>b.addEventListener('click',()=>{
    divYear=+b.dataset.dy; renderDivision(canonical); }));
  app.querySelectorAll('.pname[data-t]').forEach(b=>b.addEventListener('click',()=>{
    location.hash='#/t/'+encodeURIComponent(b.dataset.t); }));
  app.querySelectorAll('.pname[data-p]').forEach(b=>b.addEventListener('click',()=>{
    location.hash='#/p/'+encodeURIComponent(b.dataset.p); }));
  app.querySelectorAll('.pname[data-g]').forEach(b=>b.addEventListener('click',()=>{
    location.hash='#/g/'+b.dataset.g; }));
  app.querySelectorAll('table.sortable').forEach(makeSortable);
}

/* ------------------------------ LEAGUE LEADERS ------------------------------ */
let leadYear = null, leadPhase = 'reg';
const teamNick = tm => !tm ? '' :
  tm.includes(' / ') ? tm.split(' / ').map(teamNick).join('/')
  : (TEAMS[tm] ? TEAMS[tm].nick : tm);
function svBarW(items, low){
  const vs = items.map(i=>i.v).filter(isFinite);
  const base = low ? Math.min(...vs) : Math.max(...vs);
  return v => {
    if(!isFinite(v) || !isFinite(base)) return 0;
    /* base===0 (a literal 0.00 ERA/WHIP, the best possible low-is-better value)
       would otherwise divide-by-zero into every bar reading 0% — the row that
       IS the zero gets the full bar, everything else gets the floor */
    if(low && base===0) return v===0 ? 100 : 8;
    if(base===0) return 8;
    return Math.max(8, Math.min(100, (low ? base/v : v/base)*100));
  };
}
/* it.tm is trusted, pre-escaped HTML built by the caller (so a caller can embed
   a clickable date/box-score link, not just plain text) — every producer below
   escapes its own dynamic pieces before handing tm to this function. */
const llist = (t, items, fmt, low) => {
  const w = svBarW(items, low);
  /* a split season keeps both team names in the text ("NickA/NickB") but shows
     only the second (most recent) team's logo — one badge reads cleaner than
     two crammed into a narrow list row, and the second club is who they
     finished the year with */
  const logos = it => it.logo2 ? `<img class="llogo" src="${it.logo2}" alt="">` : (it.logo?`<img class="llogo" src="${it.logo}" alt="">`:'');
  return `<div class="llist"><h4>${t}</h4><ol>${items.map(it=>
  `<li style="--w:${w(it.v).toFixed(1)}%">${logos(it)}<span class="ln"><button class="pname" data-p="${esc(it.n)}">${esc(it.n)}</button>${
    it.tm?`<span class="lt">${it.tm}</span>`:''}</span><b>${fmt(it.v)}</b></li>`).join('')}</ol></div>`;
};

let leadView='top10', leadMode='bat', leadSortKey='HR', leadSortDir=-1;
function renderLeaders(){
  setNav('leaders');
  const yrs = ALL_YEARS.slice();
  const isCareer = leadYear==='career';
  if(!isCareer && !yrs.includes(leadYear)) leadYear = yrs[yrs.length-1];
  const isPost = leadPhase==='post';
  const chips = `<div class="chips">
    <button data-ly="career" aria-pressed="${isCareer}">Career</button>
    ${yrs.map(y=>`<button data-ly="${y}" aria-pressed="${leadYear===y}">${y}</button>`).join('')}</div>`;
  const phaseToggle = `<div class="segs post" role="group" aria-label="Leaders phase">
    <button data-lp="reg" aria-pressed="${!isPost}">Regular</button>
    <button data-lp="post" aria-pressed="${isPost}">Playoffs</button></div>`;

  const seasonType = isPost ? 'Playoffs' : 'Regular';
  const pool = NAMES.map(n=>{
    const s = isCareer ? (isPost ? P[n].careerPO : P[n].careerReg)
      : (P[n].seasons.find(x=>x.year===leadYear && x.type===seasonType && !x.split));
    return s ? {n, s} : null;
  }).filter(Boolean);
  const minAB = isPost ? 0 : 150, minPA = isPost ? 0 : 150, minG = isPost ? 0 : 9,
    minO = isCareer ? (isPost ? 0 : 180) : (isPost ? 0 : 36);
  const teamOf = x => teamOfPlayer(x, leadYear, isCareer);

  /* ---- Full Stats: every qualifying player's complete line for the current
     scope (year or career, regular or postseason) in one sortable table —
     same click-to-sort table the Players page uses, but scoped to whatever
     year/phase is picked above instead of always full career, and with team
     logos added (Players' own table doesn't have those). No AB/PA/IP floor —
     that's the point of "full", versus the qualified Top 10 lists above. */
  const fullViewToggle = `<div class="segs" role="group" aria-label="Leaders view">
    <button data-lv="top10" aria-pressed="${leadView==='top10'}">Top 10</button>
    <button data-lv="full" aria-pressed="${leadView==='full'}">Full Stats</button>
  </div>`;
  const fullStatsHTML = () => {
    const cols = (leadMode==='bat'?BAT_COLS:PIT_COLS).filter(([k])=>k!=='yrs');
    let rows = pool.map(x=>{
      const s = x.s, ti = teamOf(x);
      return {
        name:x.n, teamLabel:ti.label, logo:ti.logo, logo2:ti.logo2,
        G: leadMode==='bat'? s.G_bat : s.G_pit,
        PA:s.PA, AB:s.AB, R:s.R, H:s.H, HR:s.HR, RBI:s.RBI, BB:s.BB, K:s.K,
        AVG:avg(s), OBP:obp(s), SLG:slg(s), OPS:ops(s),
        'OPS+': opsPlusFor(s, isCareer ? careerWeights(P[x.n], isPost) : [{year:leadYear, pa:s.PA, post:isPost}]),
        IP:s.IPouts/3, W:s.W, L:s.L, SV:s.SV, pH:s.pH, ER:s.ER, pBB:s.pBB, pK:s.pK,
        ERA:era(s), WHIP:whip(s), K9:k9(s),
        'ERA+': eraPlusFor(s, isCareer ? careerWeightsPit(P[x.n], isPost) : [{year:leadYear, outs:s.IPouts, post:isPost}]),
        _ipouts:s.IPouts, _bat:s.G_bat,
      };
    });
    rows = rows.filter(r => leadMode==='pit' ? r._ipouts>0 : r._bat>0);
    rows.sort((a,b)=>{
      let x = leadSortKey==='team' ? a.teamLabel : a[leadSortKey];
      let y = leadSortKey==='team' ? b.teamLabel : b[leadSortKey];
      if(leadSortKey==='name' || leadSortKey==='team') return leadSortDir*String(x||'').localeCompare(String(y||''));
      if(!isFinite(x)) x=-Infinity; if(!isFinite(y)) y=-Infinity;
      return leadSortDir*(x-y);
    });
    const fullCell = (r,k,t) => {
      if(k==='team') return `<span class="tmcell">${r.logo2?`<img class="llogo" src="${r.logo2}" alt="">`:(r.logo?`<img class="llogo" src="${r.logo}" alt="">`:'')}${r.teamLabel||''}</span>`;
      const v = r[k];
      if(t==='r') return (k==='ERA'||k==='WHIP'||k==='K9') ? two(v) : rate(v);
      if(k==='IP') return ipStr(Math.round(v*3));
      return isFinite(v) ? String(v) : '—';
    };
    const th = cols.map(([k,label,t])=>{
      const on = k===leadSortKey;
      return `<th class="${on?'sorted':''} ${t==='r'?'mono':''} ${t==='s'?'lft':''}" data-k="${k}">${label}${on?`<span class="ar">${leadSortDir<0?'▼':'▲'}</span>`:''}</th>`;
    }).join('');
    const body = rows.map(r=>'<tr>'+cols.map(([k,label,t],i)=>{
      if(i===0) return `<td class="lft"><button class="pname" data-p="${esc(r.name)}">${esc(r.name)}</button></td>`;
      return `<td class="${t==='r'?'mono':''} ${t==='s'?'lft tm':''}">${fullCell(r,k,t)}</td>`;
    }).join('')+'</tr>').join('');
    return `<div class="segs" role="group" aria-label="Stat group">
      <button data-lm="bat" aria-pressed="${leadMode==='bat'}">Batting</button>
      <button data-lm="pit" aria-pressed="${leadMode==='pit'}">Pitching</button>
    </div>
    <div class="tscroll"><table class="dir">
      <thead><tr>${th}</tr></thead>
      <tbody>${body || '<tr><td colspan="'+cols.length+'" class="empty">No players match.</td></tr>'}</tbody>
    </table></div>`;
  };

  const cat = (title, f, fmt, o={}) => {
    let a = pool;
    if(o.min==='ab') a = a.filter(x=>isCareer ? x.s.AB>=minAB : x.s.G_bat>=minG);
    else if(o.min==='pa') a = a.filter(x=>isCareer ? x.s.PA>=minPA : x.s.G_bat>=minG);
    else if(o.min==='o') a = a.filter(x=>x.s.IPouts>=minO);
    const dir = o.dir||1;
    const items = a.map(x=>{ const ti=teamOf(x); return {n:x.n, v:f(x.s), tm:ti.label, logo:ti.logo, logo2:ti.logo2}; })
      .filter(x=>isFinite(x.v) && (o.zero||x.v!==0)).sort((p,q)=>dir*(q.v-p.v)).slice(0,10);
    return items.length ? llist(title, items, fmt, dir<0) : '';
  };
  const ipfmt = v => ipStr(Math.round(v*3));
  /* cat()'s formatter only ever sees a stat bucket, not the player name or
     year it came from — precompute bucket→weights by object identity (each
     pool item's `s` is the very same careerReg/careerPO/season-row object
     referenced elsewhere this render) so OPS+ can still look up the right
     season(s) to normalize against without changing cat()'s signature. */
  const opsPlusWeights = new Map(pool.map(x=>
    [x.s, isCareer ? careerWeights(P[x.n], isPost) : [{year:leadYear, pa:x.s.PA, post:isPost}]]));
  const eraPlusWeights = new Map(pool.map(x=>
    [x.s, isCareer ? careerWeightsPit(P[x.n], isPost) : [{year:leadYear, outs:x.s.IPouts, post:isPost}]]));

  const bat = [
    cat('Batting Average', s=>avg(s), rate, {min:'ab'}),
    cat('On-Base %', s=>obp(s), rate, {min:'pa'}),
    cat('Slugging %', s=>slg(s), rate, {min:'ab'}),
    cat('OPS', s=>ops(s), rate, {min:'pa'}),
    cat('OPS+', s=>opsPlusFor(s, opsPlusWeights.get(s)), v=>isFinite(v)?String(v):'—', {min:'pa'}),
    cat('Home Runs', s=>s.HR, v=>v),
    cat('RBI', s=>s.RBI, v=>v),
    cat('Runs', s=>s.R, v=>v),
    cat('Hits', s=>s.H, v=>v),
    cat('Total Bases', s=>s.TB, v=>v),
    cat('Doubles', s=>s['2B'], v=>v),
    cat('Walks', s=>s.BB, v=>v),
    cat('Stolen Bases', s=>s.SB, v=>v),
  ].join('');
  const pit = [
    cat('Wins', s=>s.W, v=>v),
    cat('ERA', s=>era(s), two, {min:'o', dir:-1, zero:true}),
    cat('ERA+', s=>eraPlusFor(s, eraPlusWeights.get(s)), v=>isFinite(v)?String(v):'—', {min:'o'}),
    cat('WHIP', s=>whip(s), two, {min:'o', dir:-1, zero:true}),
    cat('Strikeouts', s=>s.pK, v=>v),
    cat('K per 3 IP', s=>k9(s), two, {min:'o'}),
    cat('Saves', s=>s.SV, v=>v),
    cat('Innings Pitched', s=>s.IPouts/3, ipfmt),
    cat('Complete Games', s=>s.CG, v=>v),
  ].join('');

  app.innerHTML = `
    <div class="phead"><h2>League Leaders</h2>
      <span class="yrs">${isPost?'Postseason':'Regular season'} · ${isCareer?'Career '+RANGE:leadYear}</span></div>
    ${chips}
    ${phaseToggle}
    ${fullViewToggle}
    ${leadView==='full' ? fullStatsHTML() : `
    <h3 class="hsub">Batting</h3><div class="llgrid">${bat||'<p class="lead">No qualifiers.</p>'}</div>
    <h3 class="hsub">Pitching</h3><div class="llgrid">${pit||'<p class="lead">No pitching qualifiers.</p>'}</div>`}
    <p class="note">${leadView==='full'
      ? `Every player who ${leadMode==='bat'?'batted':'pitched'} in this scope, no minimum — click a header to sort.`
      : `Top 10 per category, ${isPost?'postseason':'regular season'}.${isPost
        ? ' No minimum AB/PA/IP — small postseason samples all qualify.'
        : ` Rate stats need ${isCareer?'150+ AB/PA and 60+ IP':'9+ games played and 12+ IP'};`}
    ERA and WHIP list the lowest.`} Career covers ${RANGE}. Names link to player pages.</p>`;
  app.querySelectorAll('.chips button').forEach(b=>b.addEventListener('click',()=>{
    leadYear = b.dataset.ly==='career' ? 'career' : +b.dataset.ly; renderLeaders();
  }));
  app.querySelectorAll('[data-lp]').forEach(b=>b.addEventListener('click',()=>{
    leadPhase = b.dataset.lp; renderLeaders();
  }));
  app.querySelectorAll('[data-lv]').forEach(b=>b.addEventListener('click',()=>{
    if(leadView!==b.dataset.lv){ leadView=b.dataset.lv; renderLeaders(); }
  }));
  app.querySelectorAll('[data-lm]').forEach(b=>b.addEventListener('click',()=>{
    if(leadMode===b.dataset.lm) return;
    leadMode=b.dataset.lm;
    const batKeys=['PA','AB','H','HR','RBI','AVG','OBP','SLG','OPS','OPS+'];
    const pitKeys=['IP','W','L','SV','pH','ER','pBB','pK','ERA','WHIP','K9','ERA+'];
    if(leadMode==='pit' && batKeys.includes(leadSortKey)) leadSortKey='W';
    if(leadMode==='bat' && pitKeys.includes(leadSortKey)) leadSortKey='HR';
    leadSortDir=-1; renderLeaders();
  }));
  app.querySelectorAll('thead th[data-k]').forEach(h=>h.addEventListener('click',()=>{
    const k=h.dataset.k;
    if(k===leadSortKey) leadSortDir*=-1; else { leadSortKey=k; leadSortDir = k==='name'?1:-1; }
    renderLeaders();
  }));
  app.querySelectorAll('.pname[data-p]').forEach(b=>b.addEventListener('click',()=>{
    location.hash='#/p/'+encodeURIComponent(b.dataset.p); }));
}

const phaseToggleHTML = () => `<div class="segs post" role="group" aria-label="Phase">
  <button data-tp="reg" aria-pressed="${teamPhase==='reg'}">Regular</button>
  <button data-tp="post" aria-pressed="${teamPhase==='post'}">Playoffs</button></div>`;

/* `weights` is the opsPlusFor() weight array for whatever this roster represents
   — a single team-year (one {year,pa} entry) from the team page, or omitted
   entirely for the division All-Star page's roster, which combines box
   scores across many years with no per-appearance year kept at this point in
   the pipeline, so there's no sound baseline to normalize against there. */
function rosterBatting(roster, ph, label, weights){
  const rows = roster.map(e=>({name:e.name, ...e[ph]})).filter(d=>d.G_bat>0 || d.PA>0);
  if(!rows.length) return '';
  rows.sort((a,b)=>b.PA-a.PA);
  const cols=[
    {l:'Player',lft:1,f:d=>`<button class="pname" data-p="${esc(d.name)}">${esc(d.name)}</button>`},
    {l:'G',f:d=>d.G_bat},{l:'PA',f:d=>d.PA},{l:'AB',f:d=>d.AB},{l:'R',f:d=>d.R},{l:'H',f:d=>d.H},
    {l:'2B',f:d=>d['2B']},{l:'3B',f:d=>d['3B']},{l:'HR',f:d=>d.HR},{l:'RBI',f:d=>d.RBI},
    {l:'BB',f:d=>d.BB},{l:'K',f:d=>d.K},
    {l:'AVG',m:1,f:d=>rate(avg(d))},{l:'OBP',m:1,f:d=>rate(obp(d))},
    {l:'SLG',m:1,f:d=>rate(slg(d))},{l:'OPS',m:1,f:d=>rate(ops(d))},
    {l:'OPS+',m:1,f:d=>{const v=weights?opsPlusFor(d,weights):NaN;return isFinite(v)?String(v):'—';}}];
  return statTable('Batting'+(label?' · '+label:''), cols, rows, sumRows(rows), 'Team', '', true);
}
function rosterPitching(roster, ph, label, weights){
  let rows = roster.map(e=>({name:e.name, ...e[ph]})).filter(d=>d.IPouts>0);
  if(!rows.length) return '';
  rows.sort((a,b)=>b.IPouts-a.IPouts);
  const cols=[
    {l:'Player',lft:1,f:d=>`<button class="pname" data-p="${esc(d.name)}">${esc(d.name)}</button>`},
    {l:'G',f:d=>d.G_pit},{l:'IP',m:1,f:d=>ipStr(d.IPouts)},{l:'W',f:d=>d.W},{l:'L',f:d=>d.L},
    {l:'SV',f:d=>d.SV},{l:'CG',f:d=>d.CG},{l:'H',f:d=>d.pH},{l:'R',f:d=>d.pR},{l:'ER',f:d=>d.ER},
    {l:'BB',f:d=>d.pBB},{l:'K',f:d=>d.pK},
    {l:'ERA',m:1,f:d=>two(era(d))},{l:'WHIP',m:1,f:d=>two(whip(d))},{l:'K/3',m:1,f:d=>two(k9(d))},
    {l:'ERA+',m:1,f:d=>{const v=weights?eraPlusFor(d,weights):NaN;return isFinite(v)?String(v):'—';}}];
  return statTable('Pitching'+(label?' · '+label:''), cols, rows, sumRows(rows), 'Team', '', true);
}
function gameLog(games, yr){
  if(!games || !games.length) return '';
  const rows=games.map(g=>`<tr>
    <td class="lft">${g.gid&&GAMES[g.gid]?`<button class="pname" data-g="${g.gid}">${g.date}</button>`:g.date}</td>
    <td class="lft">${g.ha==='H'?'vs':'@'} ${esc(g.opp)}${g.phase!=='Regular'?`<span class="gtag">${esc(gameTag(g))}</span>`:''}</td>
    <td class="mono">${g.rf}–${g.ra}</td>
    <td class="res-${g.res}">${g.res}</td></tr>`).join('');
  return `<section class="stat"><h4>Game Log${yr?' · '+yr:''}</h4><div class="tscroll">
    <table class="detail"><thead><tr><th class="lft">Date</th><th class="lft">Opponent</th>
    <th class="mono">Score</th><th>Res</th></tr></thead><tbody>${rows}</tbody></table></div></section>`;
}

function teamOneYear(t, y){
  const s = t.seasons[y] || {roster:[], games:[], record:{}};
  const phKey = teamPhase==='post' ? 'playoffs' : 'regular';
  const roster = s.roster.filter(e=>e[phKey]);
  const T = sumRows(roster.map(e=>e[phKey]));
  const recCards = ['Regular','Playoffs'].map(ph=>{
    const r=(s.record||{})[ph]; if(!r) return '';
    const diff=r.RF-r.RA;
    return `<div class="rec ${ph==='Playoffs'?'po':''}"><h4>${ph} Record</h4>
      <div class="big">${recWL(r)}</div>
      <div class="sub">${r.RF} RF · ${r.RA} RA · ${diff>0?'+':''}${diff}</div></div>`;
  }).join('')
  + (roster.length ? `<div class="rec"><h4>Team Batting</h4>
      <div class="big">${rate(avg(T))}/${rate(obp(T))}/${rate(slg(T))}</div>
      <div class="sub">${T.HR} HR · ${T.RBI} RBI · ${T.R} R in ${T.G_bat} G</div></div>`
    + (T.IPouts ? `<div class="rec"><h4>Team Pitching</h4>
      <div class="big">${two(era(T))} ERA</div>
      <div class="sub">${two(whip(T))} WHIP · ${T.pK} K · ${ipStr(T.IPouts)} IP</div></div>` : '') : '');
  const rosterHTML = roster.length
    ? rosterBatting(roster, phKey, undefined, [{year:y, pa:1, post:phKey==='playoffs'}])
      + rosterPitching(roster, phKey, undefined, [{year:y, outs:1, post:phKey==='playoffs'}])
    : `<p class="lead">No ${teamPhase==='post'?'playoff':'regular-season'} roster stats recorded for ${y}.</p>`;
  return `<div class="recgrid">${recCards || '<div class="rec"><h4>Record</h4><div class="big">—</div></div>'}</div>
    ${phaseToggleHTML()}
    ${rosterHTML}
    ${gameLog(s.games, y)}`;
}

/* compact franchise-history overview: one row per year, shown regardless of the year picker */
/* which division (by that year's own name — North/South pre-2021, Brookside/
   Brentwood from 2021 on) a franchise played in, straight off DB.divisions'
   own keys for that year — no canonicalizing needed, they're already
   era-accurate since that's how the raw standings data is keyed. */
function divisionOf(name, y){
  const divs = (DB.divisions||{})[y]; if(!divs) return null;
  return Object.keys(divs).find(dn => (divs[dn]||[]).some(([tm])=>tm===name)) || null;
}
const ORDINAL = n => {
  const s = ['th','st','nd','rd'], v = n%100;
  return n + (s[(v-20)%10] || s[v] || s[0]);
};
/* standing within that division that year — same sort as the division page
   itself (PCT, then head-to-head, then run differential) */
function divisionFinish(name, y, dn){
  if(!dn) return null;
  const order = ((DB.divisions[y]||{})[dn]) || [];
  const h2h = (a,b) => { const v=a.vs[b.name]||{W:0,L:0}; return v.W-v.L; };
  const rows = order.map(([tm])=>standRow(tm,y)).filter(Boolean)
    .sort((a,b)=> (b.PCT-a.PCT) || (-h2h(a,b)) || (b.DIFF-a.DIFF));
  const idx = rows.findIndex(r=>r.name===name);
  return idx<0 ? null : `${ORDINAL(idx+1)} of ${rows.length}`;
}
/* Narrative playoff result for one team-year: DNQ, a first-round loss (always
   sudden death — one game, win or go home — so no score to show), or a
   World Series result with a real series score. That score is read off the
   ACTUAL matched box scores (seriesGids + real away/home runs), never off
   PLAYOFFS[y].finalSeries' own tuple order — checked against several years
   of real results while building the bracket's per-game winner tags and
   found that order isn't consistent year to year, so it can't be trusted
   for who-won-which-game here either.
   `seriesKey` identifies the series this result links to (matching
   renderSeries' own routing: 'brookside'/'brentwood' for a round-1 exit,
   'final' for anything that reached the World Series) — null when there's
   no series to link to (DNQ, or no playoff data at all that year). */
function playoffResultFor(name, y){
  const p = PLAYOFFS[String(y)];
  if(!p) return {label:null, seriesKey:null};
  const sideKey = ['brookside','brentwood'].find(sk => ((p[sk]||{}).seeds||[]).some(s=>s.full===name));
  if(!sideKey) return {label:'DNQ', seriesKey:null};
  const side = p[sideKey];
  const seed = side.seeds.find(s=>s.full===name);
  const round1 = y>=2025 ? 'DS' : 'WC';
  if(seed.nick !== side.winner) return {label:`LOST ${round1}`, seriesKey:sideKey};
  const finalists = ['brookside','brentwood'].map(sk=>{
    const sd = p[sk] || {};
    return (sd.seeds||[]).find(s=>s.nick===sd.winner) || {nick:sd.winner, full:null};
  });
  const opp = finalists.find(f=>f.full!==name);
  const gids = seriesGids(y, name, opp && opp.full);
  let myWins=0, oppWins=0;
  gids.forEach(gid=>{
    const g = GAMES[gid];
    const iAway = g.away.team===name;
    const myR = iAway?g.away.R:g.home.R, oppR = iAway?g.home.R:g.away.R;
    if(myR>oppR) myWins++; else if(oppR>myR) oppWins++;
  });
  const champ = p.championFull===name;
  const score = gids.length ? ` ${champ?myWins:oppWins}-${champ?oppWins:myWins}` : '';
  return {label:`${champ?'WON':'LOST'} WS${score}`, seriesKey:'final'};
}
/* one combined cell for a W-L split plus its own PCT, muted and parenthetical
   so the primary W-L reads first — used for Home/Away and vs-division splits,
   which would otherwise need 2-3 columns each to show both pieces. */
function fmtSplit(w, l){
  const gp = w+l;
  return gp ? `${w}–${l} <span class="azm">(${rate(w/gp)})</span>` : '—';
}
/* this team's W-L against every opponent that CANONICAL division fielded
   that year (North/South folded into Brookside/Brentwood so one pair of
   columns works across the whole table, not just one era of it) */
function vsCanonicalRecord(r, y, canonical){
  let w=0, l=0;
  for(const opp in r.vs){
    const dn = divisionOf(opp, y);
    if(dn && canonicalDivision(dn)===canonical){ w+=r.vs[opp].W; l+=r.vs[opp].L; }
  }
  return {w, l};
}
function teamRecordTable(t){
  const yrs = t.years.slice().sort((a,b)=>a-b);
  const cHA = {hw:0,hl:0,aw:0,al:0};
  const cVs = {Brookside:{w:0,l:0}, Brentwood:{w:0,l:0}};
  const srows = yrs.map(y=>{
    const rec=(t.seasons[y]||{}).record||{};
    const R=rec.Regular||{W:0,L:0,T:0,RF:0,RA:0};
    const gp=R.W+R.L, diff=R.RF-R.RA;
    const nm=(t.nameByYear||{})[y] || t.nick;
    const nmFull = t.loc && !nm.startsWith(t.loc) ? t.loc+' '+nm : nm;
    const dn = divisionOf(t.name, y);
    const finish = divisionFinish(t.name, y, dn);
    const result = playoffResultFor(t.name, y);
    const sr = standRow(t.name, y) || {hW:0,hL:0,aW:0,aL:0,vs:{}};
    cHA.hw+=sr.hW; cHA.hl+=sr.hL; cHA.aw+=sr.aW; cHA.al+=sr.aL;
    const vsB = vsCanonicalRecord(sr, y, 'Brookside'), vsT = vsCanonicalRecord(sr, y, 'Brentwood');
    cVs.Brookside.w+=vsB.w; cVs.Brookside.l+=vsB.l; cVs.Brentwood.w+=vsT.w; cVs.Brentwood.l+=vsT.l;
    const resultCell = result.seriesKey
      ? `<button class="pname" data-series="${y}|${result.seriesKey}">${esc(result.label)}</button>`
      : esc(result.label||'—');
    return `<tr><td class="lft"><button class="pname" data-yv="${y}">${y}</button></td>
      <td class="lft">${esc(nmFull)}</td>
      <td class="lft">${dn?esc(dn):'—'}</td>
      <td>${R.W}</td><td>${R.L}</td><td class="mono">${gp?rate(R.W/gp):'—'}</td>
      <td class="lft">${resultCell}</td>
      <td class="lft">${finish?esc(finish):'—'}</td>
      <td>${R.RF}</td><td>${R.RA}</td><td>${diff>0?'+':''}${diff}</td>
      <td class="mono">${fmtSplit(sr.hW,sr.hL)}</td><td class="mono">${fmtSplit(sr.aW,sr.aL)}</td>
      <td class="mono">${fmtSplit(vsB.w,vsB.l)}</td><td class="mono">${fmtSplit(vsT.w,vsT.l)}</td></tr>`;
  }).join('');
  /* career totals across every season on record — summed, not averaged, so
     PCT and Diff are recomputed from the summed W/L/RF/RA rather than
     rolling up each year's own rate. Division/Result/Finish don't aggregate
     across years, so the total row leaves them blank. */
  const cR = {W:0,L:0,T:0,RF:0,RA:0};
  yrs.forEach(y=>{
    const R=((t.seasons[y]||{}).record||{}).Regular;
    if(R){ cR.W+=R.W; cR.L+=R.L; cR.T+=R.T||0; cR.RF+=R.RF; cR.RA+=R.RA; }
  });
  const cGp = cR.W+cR.L, cDiff = cR.RF-cR.RA;
  const totalRow = `<tr><td class="lft">Career</td><td class="lft"></td><td class="lft"></td>
    <td>${cR.W}</td><td>${cR.L}</td><td class="mono">${cGp?rate(cR.W/cGp):'—'}</td>
    <td class="lft"></td><td class="lft"></td>
    <td>${cR.RF}</td><td>${cR.RA}</td><td>${cDiff>0?'+':''}${cDiff}</td>
    <td class="mono">${fmtSplit(cHA.hw,cHA.hl)}</td><td class="mono">${fmtSplit(cHA.aw,cHA.al)}</td>
    <td class="mono">${fmtSplit(cVs.Brookside.w,cVs.Brookside.l)}</td><td class="mono">${fmtSplit(cVs.Brentwood.w,cVs.Brentwood.l)}</td></tr>`;
  return `<section class="stat"><h4>Season by Season</h4><div class="tscroll"><table class="detail">
    <thead><tr><th class="lft">Year</th><th class="lft">Name</th><th class="lft">Division</th>
    <th>W</th><th>L</th><th class="mono">PCT</th><th class="lft">Playoffs</th><th class="lft">Finish</th>
    <th>RF</th><th>RA</th><th>Diff</th>
    <th class="mono">Home</th><th class="mono">Away</th>
    <th class="mono">vs Brookside</th><th class="mono">vs Brentwood</th></tr></thead>
    <tbody>${srows}</tbody><tfoot>${totalRow}</tfoot></table></div></section>`;
}

/* yearly batting/pitching breakdown — lives under the "All years" chip, alongside the
   all-time roster and head-to-head, so the chip genuinely controls everything below it */
function teamStatsBySeason(t){
  const yrs = t.years.slice().sort((a,b)=>a-b);
  const byYear = yrs.map(y=>{
    const rs=((t.seasons[y]||{}).roster||[]).filter(e=>e.regular).map(e=>e.regular);
    return {year:y, ...sumRows(rs)};
  });
  const grand = sumRows(byYear);
  const yr0 = {l:'Season',f:d=>`<button class="pname" data-yv="${d.year}">${d.year}</button>`};
  const tbCols=[yr0,
    {l:'PA',f:d=>d.PA},{l:'AB',f:d=>d.AB},{l:'R',f:d=>d.R},{l:'H',f:d=>d.H},
    {l:'2B',f:d=>d['2B']},{l:'3B',f:d=>d['3B']},{l:'HR',f:d=>d.HR},{l:'RBI',f:d=>d.RBI},
    {l:'BB',f:d=>d.BB},{l:'K',f:d=>d.K},
    {l:'AVG',m:1,f:d=>rate(avg(d))},{l:'OBP',m:1,f:d=>rate(obp(d))},
    {l:'SLG',m:1,f:d=>rate(slg(d))},{l:'OPS',m:1,f:d=>rate(ops(d))},
    {l:'OPS+',m:1,f:d=>{
      const v = d.year!=null
        ? opsPlusFor(d, [{year:d.year, pa:d.PA}])
        : opsPlusFor(d, byYear.map(r=>({year:r.year, pa:r.PA})));
      return isFinite(v)?String(v):'—';
    }}];
  const teamBat = statTable('Team Batting by Season', tbCols, byYear, grand, 'All', '');
  const tpCols=[yr0,
    {l:'IP',m:1,f:d=>ipStr(d.IPouts)},{l:'R',f:d=>d.pR},{l:'ER',f:d=>d.ER},
    {l:'H',f:d=>d.pH},{l:'BB',f:d=>d.pBB},{l:'K',f:d=>d.pK},{l:'W',f:d=>d.W},{l:'L',f:d=>d.L},
    {l:'ERA',m:1,f:d=>two(era(d))},{l:'WHIP',m:1,f:d=>two(whip(d))},{l:'K/3',m:1,f:d=>two(k9(d))},
    {l:'ERA+',m:1,f:d=>{
      const v = d.year!=null
        ? eraPlusFor(d, [{year:d.year, outs:d.IPouts}])
        : eraPlusFor(d, byYear.map(r=>({year:r.year, outs:r.IPouts})));
      return isFinite(v)?String(v):'—';
    }}];
  const teamPit = statTable('Team Pitching by Season', tpCols, byYear, grand, 'All', '');
  return teamBat + teamPit;
}

function teamAllYears(t, name){
  const yrs = t.years.slice().sort((a,b)=>a-b);
  const acc={};
  yrs.forEach(y=>((t.seasons[y]||{}).roster||[]).forEach(e=>{
    if(!e.regular) return;
    const a = acc[e.name] || (acc[e.name]={name:e.name, _yrs:new Set(), yearPA:{}, yearOuts:{}, s:sumRows([])});
    a._yrs.add(y);
    a.yearPA[y] = (a.yearPA[y]||0) + (e.regular.PA||0);
    a.yearOuts[y] = (a.yearOuts[y]||0) + (e.regular.IPouts||0);
    for(const k of ZERO_KEYS) a.s[k]+=(e.regular[k]||0);
  }));
  const arows=Object.values(acc).map(a=>({name:a.name, yrs:a._yrs.size,
      _weights: Object.entries(a.yearPA).map(([y,pa])=>({year:+y, pa})),
      _pitWeights: Object.entries(a.yearOuts).map(([y,outs])=>({year:+y, outs})), ...a.s}))
    .sort((x,y)=>y.PA-x.PA);
  const batCols=[
    {l:'Player',lft:1,f:d=>`<button class="pname" data-p="${esc(d.name)}">${esc(d.name)}</button>`},
    {l:'Yrs',f:d=>d.yrs,noTot:1},{l:'G',f:d=>d.G_bat},{l:'PA',f:d=>d.PA},{l:'R',f:d=>d.R},{l:'H',f:d=>d.H},
    {l:'HR',f:d=>d.HR},{l:'RBI',f:d=>d.RBI},{l:'BB',f:d=>d.BB},{l:'K',f:d=>d.K},
    {l:'AVG',m:1,f:d=>rate(avg(d))},{l:'OPS',m:1,f:d=>rate(ops(d))},
    {l:'OPS+',m:1,f:d=>{const v=opsPlusFor(d, d._weights);return isFinite(v)?String(v):'—';}}];
  const batRows = arows.filter(d=>d.PA>0);
  const batTotal = sumRows(batRows);
  batTotal._weights = TAGG_WEIGHTS[name];
  const battingHTML = batRows.length
    ? statTable('Franchise Roster · Hitting', batCols, batRows, batTotal, 'Total', '', true) : '';

  const pitCols=[
    {l:'Player',lft:1,f:d=>`<button class="pname" data-p="${esc(d.name)}">${esc(d.name)}</button>`},
    {l:'Yrs',f:d=>d.yrs,noTot:1},{l:'G',f:d=>d.G_pit},{l:'IP',m:1,f:d=>ipStr(d.IPouts)},
    {l:'W',f:d=>d.W},{l:'L',f:d=>d.L},{l:'ERA',m:1,f:d=>two(era(d))},
    {l:'ERA+',m:1,f:d=>{const v=eraPlusFor(d, d._pitWeights);return isFinite(v)?String(v):'—';}}];
  const pitRows = arows.filter(d=>d.IPouts>0).sort((x,y)=>y.IPouts-x.IPouts);
  const pitTotal = sumRows(pitRows);
  pitTotal._pitWeights = TAGG_PIT_WEIGHTS[name];
  const pitchingHTML = pitRows.length
    ? statTable('Franchise Roster · Pitching', pitCols, pitRows, pitTotal, 'Total', '', true) : '';

  return battingHTML + pitchingHTML;
}

/* all-time series record vs every other franchise (regular season + playoffs) */
function teamH2H(t){
  const acc = {};
  t.years.forEach(y=>{
    const s = t.seasons[y]; if(!s) return;
    (s.games||[]).forEach(g=>{
      if(g.phase!=='Regular' && g.phase!=='Playoffs') return;
      if(!TEAMS[g.opp]) return;
      const a = acc[g.opp] || (acc[g.opp]={opp:g.opp, W:0, L:0, T:0, RF:0, RA:0, first:y, last:y, byYear:{}});
      a[g.res]++; a.RF+=g.rf; a.RA+=g.ra;
      if(y<a.first) a.first=y; if(y>a.last) a.last=y;
      const yr = a.byYear[y] || (a.byYear[y]={W:0,L:0,T:0,RF:0,RA:0});
      yr[g.res]++; yr.RF+=g.rf; yr.RA+=g.ra;
    });
  });
  const rows = Object.values(acc);
  if(!rows.length) return '';
  rows.sort((x,y)=>(y.W+y.L+y.T)-(x.W+x.L+x.T) || (y.W-y.L)-(x.W-x.L));
  const grand = {W:0,L:0,T:0,RF:0,RA:0};
  rows.forEach(r=>{ grand.W+=r.W; grand.L+=r.L; grand.T+=r.T; grand.RF+=r.RF; grand.RA+=r.RA; });
  const diffStr = df => (df>0?'+':'')+df;

  const trs = rows.map((r,i)=>{
    const df = r.RF-r.RA, gp = r.W+r.L;
    const years = Object.keys(r.byYear).map(Number).sort((a,b)=>a-b);
    const detailRows = years.map(y=>{
      const yr = r.byYear[y], ydf = yr.RF-yr.RA, ygp = yr.W+yr.L;
      return `<tr><td class="lft">${y}</td><td class="mono">${recWL(yr)}</td>
        <td class="mono">${ygp?rate(yr.W/ygp):'—'}</td><td>${yr.RF}</td><td>${yr.RA}</td>
        <td class="mono">${diffStr(ydf)}</td></tr>`;
    }).join('');
    return `<tr class="h2hrow">
      <td class="lft"><button class="h2htoggle" data-idx="${i}" aria-expanded="false">▸</button> ${teamLink(r.opp)}</td>
      <td class="mono">${recWL(r)}</td>
      <td class="mono">${gp?rate(r.W/gp):'—'}</td>
      <td>${r.RF}</td><td>${r.RA}</td>
      <td class="mono">${diffStr(df)}</td>
      <td class="mono">${r.first===r.last?r.first:r.first+'–'+r.last}</td>
    </tr>
    <tr class="h2hdetail" data-idx="${i}" hidden><td colspan="7">
      <div class="tscroll"><table class="detail h2hsub">
        <thead><tr><th class="lft">Year</th><th class="mono">W–L</th><th class="mono">PCT</th>
        <th>RF</th><th>RA</th><th class="mono">Diff</th></tr></thead>
        <tbody>${detailRows}</tbody>
      </table></div>
    </td></tr>`;
  }).join('');
  const gDf = grand.RF-grand.RA, gGp = grand.W+grand.L;

  return `<section class="stat"><h4>All-Time Head-to-Head</h4><div class="tscroll"><table class="detail">
    <thead><tr><th class="lft">Opponent</th><th class="mono">W–L</th><th class="mono">PCT</th>
    <th>RF</th><th>RA</th><th class="mono">Diff</th><th class="mono">Years</th></tr></thead>
    <tbody>${trs}</tbody>
    <tfoot><tr><td class="lft">All Opponents</td><td class="mono">${recWL(grand)}</td>
      <td class="mono">${gGp?rate(grand.W/gGp):'—'}</td><td>${grand.RF}</td><td>${grand.RA}</td>
      <td class="mono">${diffStr(gDf)}</td><td></td></tr></tfoot>
  </table></div>
  <p class="note">Regular season and playoff meetings combined; All-Star, Spring and Fall exhibition games excluded.
  Click ▸ next to a team to see the year-by-year breakdown.</p></section>`;
}

function teamLogoHistory(t){
  const hist = t.logoHistory;
  if(!hist || hist.length<2) return '';
  const items = hist.slice().sort((a,b)=>a.from-b.from).map(h=>{
    const range = h.to==null ? `${h.from}–Present` : (h.from===h.to ? `${h.from}` : `${h.from}–${h.to}`);
    return `<div class="logohist-item"><img src="${h.logo}" alt="${esc(t.name)} logo, ${range}"><span>${range}</span></div>`;
  }).join('');
  return `<div class="logohist"><h4>Logo History</h4><div class="logohist-row">${items}</div></div>`;
}

/* World Series titles, division pennants (won their side's bracket and
   reached the World Series, whether or not they went on to win it) and
   division titles (regular-season division winner, the "^" marker
   already used on Standings, shown there as a superscript "z") — all
   matched by the live franchise key so an era name change (e.g.
   Bluefish -> Kraken) doesn't split the count. Rendered as a trophy
   case: gold medallions for World Series, downward-pointing pennant
   flags (in the team's own color) for the two division categories. */
/* which division (by name, as DB.divisions actually labeled it that year —
   "North"/"South" through 2020, "Brookside"/"Brentwood" from 2021) a team
   played in for a given year — independent of PLAYOFFS' own "brookside"/
   "brentwood" side keys, which are just fixed bracket-position labels and
   don't reflect the year's real division names */
function divisionNameOf(year, team){
  const divs = (DB.divisions||{})[year];
  if(!divs) return null;
  for(const dn of Object.keys(divs)){
    if((divs[dn]||[]).some(([tm])=>tm===team)) return dn;
  }
  return null;
}
function teamAccolades(name){
  const wsYears = [], pennantEntries = [], titleEntries = [];
  Object.keys(PLAYOFFS).sort((a,b)=>a-b).forEach(y=>{
    const p = PLAYOFFS[y];
    if(p.championFull===name) wsYears.push(+y);
    ['brookside','brentwood'].forEach(side=>{
      const s = p[side]; if(!s) return;
      const seed = (s.seeds||[]).find(t=>t.full===name);
      if(seed && s.winner===seed.nick) pennantEntries.push({year:+y, div:divisionNameOf(+y,name)});
    });
  });
  Object.keys(DB.divisions||{}).sort((a,b)=>a-b).forEach(y=>{
    Object.entries(DB.divisions[y]).forEach(([dn, list])=>{
      const entry = (list||[]).find(([tm])=>tm===name);
      if(entry && entry[1]==='^') titleEntries.push({year:+y, div:dn});
    });
  });
  if(!wsYears.length && !pennantEntries.length && !titleEntries.length) return '';
  /* a classic 3-column trophy — a wiffleball finial, star, tapering neck,
     a disc on three gold pillars around a center medallion, a base with a
     nameplate — rather than the plain cup icon (TROPHY) used elsewhere
     for inline text */
  const TROPHY3 = `<svg class="acc-trophy-svg" viewBox="0 0 64 100" aria-hidden="true">
    <circle cx="32" cy="9" r="7" fill="#fff"/>
    <path d="M32 18 L34.8 25 L42 25.6 L36.4 30.2 L38.2 37.4 L32 33.2 L25.8 37.4 L27.6 30.2 L22 25.6 L29.2 25 Z" fill="var(--gold)"/>
    <path d="M32 33 L39 44 L25 44 Z" fill="var(--gold)"/>
    <ellipse cx="32" cy="46" rx="18" ry="5" fill="#2a1c0c"/>
    <rect x="16" y="46" width="4.5" height="36" fill="var(--gold)"/>
    <rect x="29.8" y="46" width="4.5" height="36" fill="var(--gold)"/>
    <rect x="43.5" y="46" width="4.5" height="36" fill="var(--gold)"/>
    <circle cx="32" cy="65" r="7.5" fill="#2a1c0c" stroke="var(--gold)" stroke-width="1.6"/>
    <ellipse cx="32" cy="82" rx="20" ry="5.5" fill="#2a1c0c"/>
    <rect x="14" y="82" width="36" height="16" rx="2" fill="#2a1c0c"/>
    <rect x="21" y="92" width="22" height="4.5" rx="1" fill="var(--gold)" opacity=".85"/>
  </svg>`;
  const trophies = years => `<div class="acc-grid">${years.map(y=>
    `<div class="acc-trophy">${TROPHY3}<span class="acc-yr">${y}</span></div>`).join('')}</div>`;
  /* titles (flat team color) vs pennants (two-tone franchise gradient) are
     the same downward-pennant shape but styled distinctly. Each shows its
     division's logo when one is on file (Brookside/Brentwood, 2021 on) —
     North/South (2017–2020) have none uploaded yet, so those fall back to
     a plain pennant (still starred, for pennants, as the fallback marker) */
  const pennants = (entries, cls) => `<div class="acc-grid">${entries.map(e=>{
    const logo = e.div && (DB.divisionLogos||{})[e.div];
    const star = (!logo && cls==='pennant') ? '<span class="acc-star">★</span>' : '';
    const inner = `${logo?`<img class="acc-divlogo" src="${logo}" alt="${esc(e.div)}">`:''}${star}<span class="acc-yr">${e.year}</span>`;
    return e.div
      ? `<button type="button" class="acc-pennant ${cls}" data-div="${esc(canonicalDivision(e.div))}">${inner}</button>`
      : `<div class="acc-pennant ${cls}">${inner}</div>`;
  }).join('')}</div>`;
  const block = (title, entries, html) => entries.length ? `<div class="acc-block">
    <h4>${entries.length}× ${title}</h4>
    ${html}
  </div>` : '';
  return `<section class="stat accolades"><h3>Team Accolades</h3>
    ${block('World Series', wsYears, trophies(wsYears))}
    ${block('Division Titles', titleEntries, pennants(titleEntries, 'title'))}
    ${block('Division Pennants', pennantEntries, pennants(pennantEntries, 'pennant'))}
  </section>`;
}
function teamDetail(name){
  const t = TEAMS[name];
  if(!t){
    const hist = FRANCHISE_SUMMARY.find(d=>d.f===null && d.full===name);
    if(hist) return renderHistoricalTeam(hist);
    location.hash='#/teams'; return;
  }
  setNav('teams');
  const yrs = t.years.slice().sort((a,b)=>a-b);
  if(teamYear!=='all' && !yrs.includes(teamYear)) teamYear = yrs[yrs.length-1];

  const chips = `<div class="chips">
    <button data-y="all" aria-pressed="${teamYear==='all'}">All years</button>
    ${yrs.map(y=>`<button data-y="${y}" aria-pressed="${teamYear===y}">${y}</button>`).join('')}
  </div>`;
  const fr=t.record, g=fr.W+fr.L+fr.T;
  setTeamVars(name);
  const logoImg = t.logo ? `<img class="tlogo" src="${t.logo}" alt="">` : '';
  const hero = FRANCHISE_COLORS[name] ? `<div class="thero">
      <div class="hero-row">${logoImg}<h2>${esc(name)}</h2></div>
      <p class="tsub"><b>${fr.W}–${fr.L}</b> regular · ${t.years.length} season${t.years.length>1?'s':''}
        · ${t.firstYear}–${t.lastYear}${t.aka&&t.aka.length?` · aka ${t.aka.map(a=>esc(t.loc&&!a.startsWith(t.loc)?t.loc+' '+a:a)).join(', ')}`:''}</p>
    </div>` : `<div class="phead"><div class="hero-row">${logoImg}<h2>${esc(name)}</h2></div>
      <span class="yrs">${t.years.length} season${t.years.length>1?'s':''} · ${t.firstYear}–${t.lastYear}
      · ${fr.W}–${fr.L} regular (${rate(g?fr.W/g:NaN)})</span></div>
    ${t.aka&&t.aka.length?`<p class="aka">Also played as ${t.aka.map(a=>esc(t.loc&&!a.startsWith(t.loc)?t.loc+' '+a:a)).join(', ')}.</p>`:''}`;
  app.innerHTML = `
    <button class="back" id="back">← All teams</button>
    ${hero}
    ${teamLeadershipHtml(name)}
    ${editBtn('Edit logo','editLogoBtn')}
    ${teamLogoHistory(t)}
    ${teamAccolades(name)}
    ${teamSpark(t)}
    ${teamRecordTable(t)}
    ${teamH2H(t)}
    ${chips}
    ${teamYear==='all' ? teamStatsBySeason(t) + teamAllYears(t, name) : teamOneYear(t, teamYear)}
    <p class="note">Records and game logs come from official results; All-Star games excluded.
    Franchises are unified across name changes (see "also played as"); the season table shows the name used that year.
    Roster lines are the stats each player recorded for this club that year — a player who changed clubs mid-year
    appears on both. Rosters list players with recorded stats, not the full signed roster.</p>`;
  document.getElementById('back').addEventListener('click',()=>{ location.hash='#/teams'; });
  app.querySelectorAll('.pname[data-g]').forEach(b=>b.addEventListener('click',()=>{
    location.hash='#/g/'+b.dataset.g; }));
  app.querySelectorAll('.pname[data-t]').forEach(b=>b.addEventListener('click',()=>{
    location.hash='#/t/'+encodeURIComponent(b.dataset.t); }));
  app.querySelectorAll('[data-div]').forEach(b=>b.addEventListener('click',()=>{
    location.hash='#/div/'+encodeURIComponent(b.dataset.div); }));
  app.querySelectorAll('.chips button').forEach(b=>b.addEventListener('click',()=>{
    const v=b.dataset.y; teamYear = v==='all' ? 'all' : +v; teamDetail(name);
  }));
  app.querySelectorAll('[data-tp]').forEach(b=>b.addEventListener('click',()=>{
    teamPhase=b.dataset.tp; teamDetail(name);
  }));
  app.querySelectorAll('.pname[data-yv]').forEach(b=>b.addEventListener('click',()=>{
    teamYear = +b.dataset.yv; teamDetail(name);
  }));
  app.querySelectorAll('.pname[data-series]').forEach(b=>b.addEventListener('click',()=>{
    const [yy,rk] = b.dataset.series.split('|');
    location.hash = '#/series/'+yy+'/'+rk;
  }));
  document.getElementById('editLogoBtn').addEventListener('click', ()=>{
    openImageEditor(`Team Logo — ${t.name}`, t.logo, 200, async url=>{
      const before = t.logo;
      t.logo = url;
      if(await saveDB()) return true;
      t.logo = before; return false;
    });
  });
  app.querySelectorAll('.h2htoggle').forEach(b=>b.addEventListener('click', ()=>{
    const open = b.getAttribute('aria-expanded')==='true';
    b.setAttribute('aria-expanded', open?'false':'true');
    b.textContent = open?'▸':'▾';
    app.querySelector(`.h2hdetail[data-idx="${b.dataset.idx}"]`).hidden = open;
  }));
  wirePlayerLinks();
  document.querySelectorAll('table.sortable').forEach(makeSortable);
}

/* Franchises that folded before the stat database begins (2012–2016, no
   TEAMS entry — record-book numbers only, from FRANCHISE_SUMMARY/TIMELINE).
   No rosters or box scores exist for these, so the page is just the
   franchise's identity, name history, and leadership. */
function renderHistoricalTeam(d){
  setNav('teams');
  const name = d.full;
  setTeamVars(name);
  const logo = (DB.franchiseLogos||{})[d.t];
  const timeline = FRANCHISE_TIMELINE.find(fr=>fr.full===name);
  const gp = d.w+d.l;
  const hero = `<div class="thero">
      <div class="hero-row">${logo?`<img class="tlogo" src="${logo}" alt="">`:''}<h2>${esc(name)}</h2></div>
      <p class="tsub"><b>${d.w}–${d.l}</b> · ${esc(d.yr)} · ${rate(gp?d.w/gp:NaN)}</p>
    </div>`;
  const erasHtml = timeline ? `<p class="aka">Played as ${timeline.eras.map(e=>
    esc(`${e.loc} ${e.nick} (${e.from===e.to?e.from:e.from+'–'+e.to})`)).join(', ')}.</p>` : '';
  app.innerHTML = `
    <button class="back" id="back">← All teams</button>
    ${hero}
    ${erasHtml}
    ${teamLeadershipHtml(name)}
    <p class="note">This franchise folded before the stat database begins in 2017, so no rosters or
    box scores are on record for it here — only the league's win-loss and title record from the
    Franchise Summary.</p>`;
  document.getElementById('back').addEventListener('click',()=>{ location.hash='#/teams'; });
  wirePlayerLinks();
}

/* ============================= GAMES / BOX SCORES ============================= */
const GAMES = DB.games || {};
const gkey = g => (GAMES[g].dt || GAMES[g].date) + '|' + g;
const GIDS = Object.keys(GAMES).sort((a,b)=>gkey(b).localeCompare(gkey(a)));
let gYear='all';
let recordsEra='all';
let recordsTab='season';

/* No-hitters & perfect games: the league's own hand-kept list (build.py reads
   the "No Hitters_Perfect Games" CSV), not derived from box scores — so it
   also covers seasons (2013–2016) that predate per-game logging entirely.
   Each entry links to a box score where one could be matched (mostly 2017 on). */
const NOHIT = (DB.noHitters || []).map(x=>({...x, pitcher:x.player}));
const NOHIT_BY_PITCHER = {};
NOHIT.forEach(x=>{ (NOHIT_BY_PITCHER[x.pitcher] = NOHIT_BY_PITCHER[x.pitcher] || []).push(x); });

/* ============================== RECORDS ============================== */
function renderRecords(){
  setNav('records');
  const lastYr = DB.seasonRange[1];
  const inEra = y => recordsEra==='all' ? true : recordsEra==='early' ? (y>=2017 && y<=2021) : y>=2022;
  const eraLabel = recordsEra==='early' ? '2017–2021' : recordsEra==='modern' ? `2022–${lastYr}` : RANGE;
  const eraChips = `<div class="chips" role="group" aria-label="Era">
    <button data-era="all" aria-pressed="${recordsEra==='all'}">All Years</button>
    <button data-era="early" aria-pressed="${recordsEra==='early'}">2017–2021 Era</button>
    <button data-era="modern" aria-pressed="${recordsEra==='modern'}">2022–${lastYr} Era</button>
  </div>`;
  const ipfmt = v => ipStr(Math.round(v*3));

  // ---- single-season records (one row per player-season; multi-team seasons combined) ----
  const seasonPool = [];
  NAMES.forEach(n=>{
    P[n].seasons.forEach(s=>{ if(s.type==='Regular' && !s.split && inEra(s.year)) seasonPool.push({n, s, y:s.year}); });
  });
  const minG=9, minO=36;
  const ySub = x => `${x.y} · ${x.s.team ? esc(histNick(x.s.team, x.y)) : esc(x.s.nTeams+'TM')}`;
  /* a "2TM" combined row has no team of its own — recover the two clubs from
     that player's own split rows for the same year (built alongside the tot
     row in build.py, same year/type, each with its own single team) */
  const splitTeamsOf = x => P[x.n].seasons
    .filter(s2=>s2.year===x.y && s2.type==='Regular' && s2.split)
    .map(s2=>s2.team);
  const sLogo = x => {
    if(x.s.team) return {logo: TEAMS[x.s.team] ? teamLogoForYear(x.s.team, x.y) : null, logo2:null};
    const [t1, t2] = splitTeamsOf(x);
    return {logo: t1 && TEAMS[t1] ? teamLogoForYear(t1, x.y) : null,
      logo2: t2 && TEAMS[t2] ? teamLogoForYear(t2, x.y) : null};
  };
  const catS = (title, f, fmt, o={}) => {
    let a = seasonPool;
    if(o.min==='g') a = a.filter(x=>x.s.G_bat>=minG);
    else if(o.min==='o') a = a.filter(x=>x.s.IPouts>=minO);
    const dir = o.dir||1;
    const items = a.map(x=>{ const lg=sLogo(x); return {n:x.n, v:f(x.s), tm:ySub(x), logo:lg.logo, logo2:lg.logo2}; })
      .filter(x=>isFinite(x.v) && (o.zero||x.v!==0)).sort((p,q)=>dir*(q.v-p.v)).slice(0,10);
    return items.length ? llist(title, items, fmt, dir<0) : '';
  };
  const seasonBat = [
    catS('Batting Average', s=>avg(s), rate, {min:'g'}),
    catS('OPS', s=>ops(s), rate, {min:'g'}),
    catS('OPS+', s=>opsPlusFor(s, [{year:s.year, pa:1}]), v=>isFinite(v)?String(v):'—', {min:'g'}),
    catS('Home Runs', s=>s.HR, v=>v),
    catS('RBI', s=>s.RBI, v=>v),
    catS('Runs', s=>s.R, v=>v),
    catS('Hits', s=>s.H, v=>v),
    catS('Total Bases', s=>s.TB, v=>v),
    catS('Walks', s=>s.BB, v=>v),
  ].join('');
  const seasonPit = [
    catS('Wins', s=>s.W, v=>v),
    catS('Strikeouts', s=>s.pK, v=>v),
    catS('ERA', s=>era(s), two, {min:'o', dir:-1, zero:true}),
    catS('ERA+', s=>eraPlusFor(s, [{year:s.year, outs:1}]), v=>isFinite(v)?String(v):'—', {min:'o'}),
    catS('WHIP', s=>whip(s), two, {min:'o', dir:-1, zero:true}),
    catS('Saves', s=>s.SV, v=>v),
    catS('Innings Pitched', s=>s.IPouts/3, ipfmt),
  ].join('');

  // ---- single-game records (regular season + playoffs, from recorded box scores) ----
  const batPool = [], pitPool = [];
  GIDS.forEach(gid=>{
    const g = GAMES[gid];
    if(g.phase!=='Regular' && g.phase!=='Playoffs') return;
    if(!inEra(+g.date.slice(0,4))) return;
    ['away','home'].forEach(sk=>{
      const s = g[sk], opp = g[sk==='away'?'home':'away'].team;
      s.bat.forEach(b=>{ if(b.n) batPool.push({n:b.n, s:b, gid, y:g.date.slice(0,4), opp, team:s.team}); });
      s.pit.forEach(p=>{ if(p.n) pitPool.push({n:p.n, s:p, gid, y:g.date.slice(0,4), opp, team:s.team}); });
    });
  });
  const gSub = x => {
    const g = GAMES[x.gid];
    const dateHTML = g ? `<button class="pname" data-g="${x.gid}">${esc(g.date)}</button>` : esc(x.y);
    return `${dateHTML} · vs ${esc(histNick(x.opp, +x.y))}`;
  };
  const gLogo = x => (x.team && TEAMS[x.team]) ? teamLogoForYear(x.team, x.y) : null;
  const catG = (pool, title, f, fmt) => {
    const items = pool.map(x=>({n:x.n, v:f(x.s), tm:gSub(x), logo:gLogo(x)})).filter(x=>isFinite(x.v) && x.v>0)
      .sort((p,q)=>q.v-p.v).slice(0,10);
    return items.length ? llist(title, items, fmt) : '';
  };
  const gameBat = [
    catG(batPool, 'Home Runs in a Game', s=>s.hr, v=>v),
    catG(batPool, 'Hits in a Game', s=>s.h, v=>v),
    catG(batPool, 'RBI in a Game', s=>s.rbi, v=>v),
    catG(batPool, 'Runs in a Game', s=>s.r, v=>v),
    catG(batPool, 'Doubles in a Game', s=>s['2b'], v=>v),
    catG(batPool, 'Triples in a Game', s=>s['3b'], v=>v),
  ].join('');
  const gamePit = [
    catG(pitPool, 'Strikeouts in a Game', s=>s.k, v=>v),
    catG(pitPool, 'Innings Pitched in a Game', s=>s.ip/3, ipfmt),
  ].join('');

  // ---- postseason records: "single postseason" = one player's whole playoff run in a
  //      year, combined across every round they appeared in (the Playoffs-type season
  //      row already is that combined line — verified no player has more than one
  //      Playoffs row for the same year); "single game" reuses the box-score pools
  //      above, filtered down to playoff games only ----
  const poPool = [];
  NAMES.forEach(n=>{
    P[n].seasons.forEach(s=>{ if(s.type==='Playoffs' && inEra(s.year)) poPool.push({n, s, y:s.year}); });
  });
  // a full postseason run is a Wild Card/Divisional Series game plus a best-of-3 World
  // Series at most — nowhere near the regular season's 9-G/12-IP bar, so rate stats here
  // need only 3+ games batting or 3+ IP pitching, as much as that short a run can offer
  const poMinG=3, poMinO=9;
  const poSub = x => `${x.y} Postseason · ${esc(histNick(x.s.team, x.y))}`;
  const poLogo = x => (x.s.team && TEAMS[x.s.team]) ? teamLogoForYear(x.s.team, x.y) : null;
  const catPO = (title, f, fmt, o={}) => {
    let a = poPool;
    if(o.min==='g') a = a.filter(x=>x.s.G_bat>=poMinG);
    else if(o.min==='o') a = a.filter(x=>x.s.IPouts>=poMinO);
    const dir = o.dir||1;
    const items = a.map(x=>({n:x.n, v:f(x.s), tm:poSub(x), logo:poLogo(x)}))
      .filter(x=>isFinite(x.v) && (o.zero||x.v!==0)).sort((p,q)=>dir*(q.v-p.v)).slice(0,10);
    return items.length ? llist(title, items, fmt, dir<0) : '';
  };
  const poBat = [
    catPO('Batting Average', s=>avg(s), rate, {min:'g'}),
    catPO('OPS', s=>ops(s), rate, {min:'g'}),
    catPO('OPS+', s=>opsPlusFor(s, [{year:s.year, pa:1, post:true}]), v=>isFinite(v)?String(v):'—', {min:'g'}),
    catPO('Home Runs', s=>s.HR, v=>v),
    catPO('RBI', s=>s.RBI, v=>v),
    catPO('Runs', s=>s.R, v=>v),
    catPO('Hits', s=>s.H, v=>v),
    catPO('Total Bases', s=>s.TB, v=>v),
    catPO('Walks', s=>s.BB, v=>v),
  ].join('');
  const poPit = [
    catPO('Wins', s=>s.W, v=>v),
    catPO('Strikeouts', s=>s.pK, v=>v),
    catPO('ERA', s=>era(s), two, {min:'o', dir:-1, zero:true}),
    catPO('ERA+', s=>eraPlusFor(s, [{year:s.year, outs:1, post:true}]), v=>isFinite(v)?String(v):'—', {min:'o'}),
    catPO('WHIP', s=>whip(s), two, {min:'o', dir:-1, zero:true}),
    catPO('Saves', s=>s.SV, v=>v),
    catPO('Innings Pitched', s=>s.IPouts/3, ipfmt),
  ].join('');
  const poBatPool = batPool.filter(x=>GAMES[x.gid].phase==='Playoffs');
  const poPitPool = pitPool.filter(x=>GAMES[x.gid].phase==='Playoffs');
  const poGameBat = [
    catG(poBatPool, 'Home Runs in a Game', s=>s.hr, v=>v),
    catG(poBatPool, 'Hits in a Game', s=>s.h, v=>v),
    catG(poBatPool, 'RBI in a Game', s=>s.rbi, v=>v),
    catG(poBatPool, 'Runs in a Game', s=>s.r, v=>v),
    catG(poBatPool, 'Doubles in a Game', s=>s['2b'], v=>v),
    catG(poBatPool, 'Triples in a Game', s=>s['3b'], v=>v),
  ].join('');
  const poGamePit = [
    catG(poPitPool, 'Strikeouts in a Game', s=>s.k, v=>v),
    catG(poPitPool, 'Innings Pitched in a Game', s=>s.ip/3, ipfmt),
  ].join('');

  // ---- streaks (era-filtered, like the rest of the page) ----
  // team win/loss streaks: from each franchise's own game log (TEAMS[..].seasons[y].games),
  // unified across name changes. W/L results come from the league's official game results,
  // not individual box scores, so this is reliable across every year — unlike player hitting
  // streaks below, no per-game-logging caveat applies here. Streaks reset at a season boundary:
  // this is a summer rec league with a long off-season (and some franchises go dormant for
  // years at a time, e.g. Harris Kings fielded no team 2022–2025) — splicing a "streak" across
  // that gap would misrepresent a stale, long-dead run as current or continuous.
  //
  // A handful of days in the raw data are forfeit batches, not real games: a team is credited
  // with a whole day's worth of W/L results — sometimes a dozen-plus, vs. a normal day's 1–3 —
  // at a canned, repeated score, e.g. Harris Kings went 0–6 sixteen times in a single day in
  // 2019 (all with an empty box score and a zeroed line despite a nonzero run total). Flag a
  // (team, date) as a forfeit batch when it has 4+ games and one score accounts for a strict
  // majority of them, and drop just those games before building streaks — tested against every
  // 4+-games-in-a-day case in the data: this cleanly separates the confirmed forfeit dates from
  // real high-volume days (e.g. a legitimate 6-game day where every score differs, which this
  // rule correctly leaves alone). Filtering at the game level (not the whole streak) matters:
  // one franchise had a real game the day right after five forfeit-day games, all in what would
  // otherwise read as one continuous streak — only removing the forfeit games themselves keeps
  // the real game from being thrown out along with them.
  const dropForfeitDays = games => {
    const byDate = {};
    games.forEach(g=>{ (byDate[g.date] = byDate[g.date] || []).push(g); });
    const badDates = new Set();
    Object.entries(byDate).forEach(([date, gs])=>{
      if(gs.length<4) return;
      const counts = {};
      gs.forEach(g=>{ const k=g.rf+'-'+g.ra; counts[k]=(counts[k]||0)+1; });
      if(Math.max(...Object.values(counts))/gs.length > 0.5) badDates.add(date);
    });
    return games.filter(g=>!badDates.has(g.date));
  };
  const teamWinStreaks = [], teamLoseStreaks = [];
  TEAMNAMES.forEach(full=>{
    const t = TEAMS[full];
    let games = [];
    t.years.forEach(y=>{
      const s = t.seasons[y]; if(!s || !inEra(+y)) return;
      (s.games||[]).forEach(g=>{ if(g.phase==='Regular') games.push(g); });
    });
    games = dropForfeitDays(games);
    games.sort((a,b)=>(a.dt||a.date).localeCompare(b.dt||b.date));
    let curRes=null, curLen=0, curStart=null;
    const flush = (res,len,start,end,ongoing) => (res==='W'?teamWinStreaks:teamLoseStreaks)
      .push({full, v:len, endYear:+end.slice(0,4), range: start===end?start:`${start} – ${end}`, ongoing});
    games.forEach((g,i)=>{
      const isWL = g.res==='W' || g.res==='L';
      const newSeason = i>0 && g.date.slice(0,4)!==games[i-1].date.slice(0,4);
      if(isWL && g.res===curRes && !newSeason){ curLen++; }
      else {
        if(curRes) flush(curRes, curLen, curStart, games[i-1].date, false);
        curRes = isWL ? g.res : null; curLen = isWL ? 1 : 0; curStart = isWL ? g.date : null;
      }
      if(i===games.length-1 && curRes) flush(curRes, curLen, curStart, g.date, +g.date.slice(0,4)===LATEST_YEAR);
    });
  });
  teamWinStreaks.sort((a,b)=>b.v-a.v); teamLoseStreaks.sort((a,b)=>b.v-a.v);
  const teamStreakList = (title, items) => {
    if(!items.length) return '';
    const w = svBarW(items, false);
    return `<div class="llist"><h4>${title}</h4><ol>${items.map(it=>{
      const logo = teamLogoForYear(it.full, it.endYear);
      return `<li style="--w:${w(it.v).toFixed(1)}%">${logo?`<img class="llogo" src="${logo}" alt="">`:''}<span class="ln">${
        histTeamLink(it.full, it.endYear)}<span class="lt">${esc(it.range)}${it.ongoing?' · ongoing':''}</span></span><b>${it.v}</b></li>`;
    }).join('')}</ol></div>`;
  };
  const streakTeam = [
    teamStreakList('Longest Winning Streaks', teamWinStreaks.slice(0,10)),
    teamStreakList('Longest Losing Streaks', teamLoseStreaks.slice(0,10)),
  ].join('');

  // player batting streaks: consecutive regular-season games meeting some per-game condition
  // (hit / home run / reached base), reset at a season boundary (same reasoning as team streaks
  // above — this is a summer league with a long off-season, so splicing across it would
  // misrepresent the streak). Restricted to games where an individual batting line was recorded,
  // 2020 on — matching the same "per-game lines where recorded (2020 on)" reliability boundary
  // already used on a player's own Game Log tab. A game the player didn't bat in (pitched only,
  // etc.) is skipped rather than treated as breaking the streak. `hit` decides whether a given
  // game's bat line extends the streak; shared by all three streak types below.
  function playerStreaks(hit){
    const out = [];
    NAMES.forEach(n=>{
      const batGames = collectPlayerGames(P[n], 'Regular')
        .filter(r=>r.bat && +r.g.date.slice(0,4)>=2020 && inEra(+r.g.date.slice(0,4)))
        .sort((a,b)=>((a.g.dt||a.g.date)).localeCompare(b.g.dt||b.g.date));
      let curLen=0, curStart=null;
      const flush = (len,start,end,side,g,ongoing) => out.push({n, v:len, start, end, side, g, ongoing});
      batGames.forEach((r,i)=>{
        const newSeason = i>0 && r.g.date.slice(0,4)!==batGames[i-1].g.date.slice(0,4);
        if(newSeason && curLen>0){
          flush(curLen, curStart, batGames[i-1].g.date, batGames[i-1].side, batGames[i-1].g, false);
          curLen=0; curStart=null;
        }
        if(hit(r.bat)){
          if(curLen===0) curStart=r.g.date;
          curLen++;
        } else {
          if(curLen>0) flush(curLen, curStart, batGames[i-1].g.date, batGames[i-1].side, batGames[i-1].g, false);
          curLen=0; curStart=null;
        }
        if(i===batGames.length-1 && curLen>0)
          flush(curLen, curStart, r.g.date, r.side, r.g, +r.g.date.slice(0,4)===LATEST_YEAR);
      });
    });
    out.sort((a,b)=>b.v-a.v);
    return out;
  }
  const streakList = (title, streaks, fmt) => {
    const items = streaks.slice(0,10).map(x=>{
      const team = x.g[x.side].team, yr = +x.end.slice(0,4);
      return {n:x.n, v:x.v, tm:`${x.start===x.end?x.start:`${x.start} – ${x.end}`}${x.ongoing?' · ongoing':''} · ${esc(histNick(team,yr))}`,
        logo: TEAMS[team] ? teamLogoForYear(team, yr) : null};
    });
    return items.length ? llist(title, items, fmt||(v=>v)) : '';
  };
  const streakHit = streakList('Longest Hitting Streaks (games)', playerStreaks(b=>b.h>0));
  const streakHR = streakList('Longest Home Run Streaks (games)', playerStreaks(b=>b.hr>0));
  const streakOB = streakList('Longest On-Base Streaks (games)', playerStreaks(b=>b.h>0 || b.bb>0 || b.hbp>0));

  /* pitcher streaks: same idea as the batting streaks above (consecutive
     regular-season appearances meeting some condition, reset at a season
     boundary), but walking each player's per-game PITCHING line instead —
     restricted to games with a recorded individual pitching line, 2020 on.
     `valueFn` lets a streak accumulate something other than "1 per game":
     the scoreless streak sums real innings pitched (outs) across every
     game in the streak, the traditional way a scoreless streak is measured,
     rather than just counting outings. */
  function pitcherStreaks(cond, valueFn){
    const out = [];
    NAMES.forEach(n=>{
      const pitGames = collectPlayerGames(P[n], 'Regular')
        .filter(r=>r.pit && +r.g.date.slice(0,4)>=2020 && inEra(+r.g.date.slice(0,4)))
        .sort((a,b)=>((a.g.dt||a.g.date)).localeCompare(b.g.dt||b.g.date));
      let curVal=0, curGames=0, curStart=null;
      const flush = (val,start,end,side,g,ongoing) => out.push({n, v:val, start, end, side, g, ongoing});
      pitGames.forEach((r,i)=>{
        const newSeason = i>0 && r.g.date.slice(0,4)!==pitGames[i-1].g.date.slice(0,4);
        if(newSeason && curGames>0){
          flush(curVal, curStart, pitGames[i-1].g.date, pitGames[i-1].side, pitGames[i-1].g, false);
          curVal=0; curGames=0; curStart=null;
        }
        if(cond(r.pit, r.g)){
          if(curGames===0) curStart=r.g.date;
          curVal += valueFn(r.pit, r.g); curGames++;
        } else {
          if(curGames>0) flush(curVal, curStart, pitGames[i-1].g.date, pitGames[i-1].side, pitGames[i-1].g, false);
          curVal=0; curGames=0; curStart=null;
        }
        if(i===pitGames.length-1 && curGames>0)
          flush(curVal, curStart, r.g.date, r.side, r.g, +r.g.date.slice(0,4)===LATEST_YEAR);
      });
    });
    out.sort((a,b)=>b.v-a.v);
    return out;
  }
  const streakScoreless = streakList('Longest Scoreless Innings Streaks',
    pitcherStreaks(p=>p.r===0, p=>p.ip), v=>ipStr(v));
  /* a complete game, per real appearance, isn't a stored field on the box
     score itself — derived instead straight from the two real numbers that
     ARE recorded: this pitcher's own IP for the game equals the game's
     full length (in outs), meaning nobody else on their side recorded an
     out that game either. */
  const streakCG = streakList('Longest Complete-Game Streaks (starts)',
    pitcherStreaks((p,g)=>p.ip===(g.innings||3)*3, ()=>1));

  // ---- no-hitters & perfect games (not era-filtered — this list is a full historical
  //      record regardless of which era the rest of the page is showing) ----
  const nPerf = NOHIT.filter(x=>x.perfect).length;
  const nhTeamCell = (team, y) => {
    const logo = TEAMS[team] ? teamLogoForYear(team, y) : null;
    return `<span class="tmcell">${logo?`<img class="llogo" src="${logo}" alt="">`:''}${histTeamLink(team, y)}</span>`;
  };
  const nhRows = NOHIT.slice().reverse().map(x=>{
    const y = +x.date.slice(0,4);
    return `<tr>
    <td class="lft">${x.gid?`<button class="pname" data-g="${x.gid}">${esc(x.dateDisplay)}</button>`:esc(x.dateDisplay)}${x.postseason?' <span class="gtag">Post</span>':''}</td>
    <td class="lft"><button class="pname" data-p="${esc(x.pitcher)}">${esc(x.pitcher)}</button></td>
    <td class="lft">${nhTeamCell(x.team, y)}</td>
    <td class="lft">${nhTeamCell(x.opp, y)}</td>
    <td class="mono">${ipStr(x.ip)}</td><td>${x.k}</td><td>${x.bb}</td>
    <td class="mono">${esc(x.score)}</td>
    <td>${x.perfect?'<span class="estd">Perfect Game</span>':''}</td></tr>`;
  }).join('');
  const nohitBlock = NOHIT.length ? `<div class="tscroll"><table class="detail">
    <thead><tr><th class="lft">Date</th><th class="lft">Pitcher</th><th class="lft">Team</th>
    <th class="lft">Opponent</th><th class="mono">IP</th><th>K</th><th>BB</th><th class="mono">Score</th>
    <th></th></tr></thead>
    <tbody>${nhRows}</tbody></table></div>
    <p class="pmeta">${nPerf} perfect game${nPerf===1?'':'s'} among ${NOHIT.length} no-hitter${NOHIT.length===1?'':'s'},
    per the league's own records, ${Math.min(...NOHIT.map(x=>+x.date.slice(0,4)))}–${Math.max(...NOHIT.map(x=>+x.date.slice(0,4)))}.</p>`
    : '<p class="lead">None on record.</p>';

  const tabs = [
    ['season', 'Single-Season', 'Single-Season Records', `<div class="phase">
      <p class="pmeta">Best individual regular seasons in league history, ${eraLabel} — one row per player-season
      (a player split across two clubs counts once, combined). Rate stats need 9+ games batting or 12+ IP pitching.</p>
      <h4 class="hsub">Batting</h4><div class="llgrid">${seasonBat}</div>
      <h4 class="hsub">Pitching</h4><div class="llgrid">${seasonPit}</div>
    </div>`],
    ['game', 'Single-Game', 'Single-Game Records', `<div class="phase">
      <p class="pmeta">Best individual game lines from recorded box scores, ${eraLabel}, regular season and playoffs.</p>
      <h4 class="hsub">Batting</h4><div class="llgrid">${gameBat}</div>
      <h4 class="hsub">Pitching</h4><div class="llgrid">${gamePit}</div>
    </div>`],
    ['postseason', 'Postseason', 'Postseason Records', `<div class="phase">
      <p class="pmeta">Best individual postseason performances, ${eraLabel}. Single Postseason combines every
      round a player appeared in during one year's playoff run (Wild Card/Divisional Series plus World Series);
      rate stats need ${poMinG}+ games batting or ${poMinO/3}+ IP pitching, well below the regular-season bar
      since a full postseason run rarely offers more than that. Single Game is drawn from playoff box scores only.</p>
      <h4 class="hsub">Single Postseason · Batting</h4><div class="llgrid">${poBat}</div>
      <h4 class="hsub">Single Postseason · Pitching</h4><div class="llgrid">${poPit}</div>
      <h4 class="hsub">Single Game · Batting</h4><div class="llgrid">${poGameBat}</div>
      <h4 class="hsub">Single Game · Pitching</h4><div class="llgrid">${poGamePit}</div>
    </div>`],
    ['streaks', 'Streaks', 'Streaks', `<div class="phase">
      <p class="pmeta">Longest runs in the selected era, regular season. Team win/loss streaks are unified
      across a franchise's name changes; player streaks are limited to games with an individual batting or
      pitching line, 2020 on. A handful of days in the record are forfeit batches rather than real games (many
      results logged at once, mostly at the same canned score) — those games are excluded from streaks.</p>
      <h4 class="hsub">Team</h4><div class="llgrid">${streakTeam}</div>
      <h4 class="hsub">Batting</h4><div class="llgrid">${streakHit}${streakHR}${streakOB}</div>
      <h4 class="hsub">Pitching</h4><div class="llgrid">${streakScoreless}${streakCG}</div>
    </div>`],
    ['nohit', 'No-Hitters/Perfect Games', 'No-Hitters &amp; Perfect Games', `<div class="phase">
      ${nohitBlock}
      <p class="note">From the league's own hand-kept no-hitter log, which predates and reaches further back
      than this site's per-game data — several of these games are from 2013–2016, before individual box scores
      were tracked here. Dates link to a box score where one could be matched to the game log (2017 on).
      Not affected by the era toggle above — this list always covers the league's full history.</p>
    </div>`],
  ];
  if(!tabs.some(t=>t[0]===recordsTab)) recordsTab = 'season';
  const tabBar = `<div class="subtabs" role="group" aria-label="Section">
    ${tabs.map(([k,label])=>`<button data-rt="${k}" aria-pressed="${recordsTab===k}">${label}</button>`).join('')}
  </div>`;
  const active = tabs.find(t=>t[0]===recordsTab);

  app.innerHTML = `
    <div class="phead"><h2>Records</h2><span class="yrs">${RANGE}</span></div>
    ${eraChips}
    ${tabBar}
    <h3>${active[2]}</h3>
    ${active[3]}`;
  app.querySelectorAll('[data-era]').forEach(b=>b.addEventListener('click',()=>{
    recordsEra=b.dataset.era; renderRecords(); }));
  app.querySelectorAll('[data-rt]').forEach(b=>b.addEventListener('click',()=>{
    recordsTab=b.dataset.rt; renderRecords(); }));
  app.querySelectorAll('.pname[data-p]').forEach(b=>b.addEventListener('click',()=>{
    location.hash='#/p/'+encodeURIComponent(b.dataset.p); }));
  app.querySelectorAll('.pname[data-g]').forEach(b=>b.addEventListener('click',()=>{
    location.hash='#/g/'+b.dataset.g; }));
  app.querySelectorAll('.pname[data-t]').forEach(b=>b.addEventListener('click',()=>{
    location.hash='#/t/'+encodeURIComponent(b.dataset.t); }));
}

function renderGames(){
  setNav('games');
  const yrs=[...new Set(GIDS.map(id=>GAMES[id].date.slice(0,4)))].sort();
  const list=GIDS.filter(id=> gYear==='all' || GAMES[id].date.slice(0,4)===gYear);
  const chips=`<div class="chips"><button data-gy="all" aria-pressed="${gYear==='all'}">All</button>
    ${yrs.map(y=>`<button data-gy="${y}" aria-pressed="${gYear===y}">${y}</button>`).join('')}</div>`;
  const gamesTeamCell = (team, y) => {
    const logo = TEAMS[team] ? teamLogoForYear(team, y) : null;
    return `<span class="tmcell">${logo?`<img class="llogo" src="${logo}" alt="">`:''}${histTeamLink(team, y)}</span>`;
  };
  const body=list.map(id=>{
    const g=GAMES[id], a=g.away.R, hh=g.home.R, yr=+g.date.slice(0,4);
    return `<tr>
      <td class="lft"><button class="pname" data-g="${id}">${g.date}</button></td>
      <td class="lft ${a>hh?'wteam':''}">${gamesTeamCell(g.away.team, yr)}</td>
      <td class="mono b">${a}–${hh}</td>
      <td class="lft ${hh>a?'wteam':''}">${gamesTeamCell(g.home.team, yr)}</td>
      <td class="lft">${g.loc?esc(g.loc):'TBA'}</td>
      <td class="lft">${g.date.slice(0,4)}${g.phase!=='Regular'?` <span class="gtag">${esc(gameTag(g))}</span>`:''}</td></tr>`;
  }).join('');
  app.innerHTML=`<p class="lead">${list.length} games. Box scores are built from the recorded player lines —
    2017–19 games were usually logged as a single line per team, so those boxes are thin.</p>
    ${chips}
    <div class="tscroll"><table class="dir"><thead><tr><th class="lft">Date</th><th class="lft">Away</th>
    <th class="mono b">R</th><th class="lft">Home</th><th class="lft">Field</th><th class="lft">Season</th></tr></thead>
    <tbody>${body}</tbody></table></div>`;
  app.querySelectorAll('.chips button').forEach(b=>b.addEventListener('click',()=>{ gYear=b.dataset.gy; renderGames(); }));
  app.querySelectorAll('.pname[data-g]').forEach(b=>b.addEventListener('click',()=>{ location.hash='#/g/'+b.dataset.g; }));
  app.querySelectorAll('.pname[data-t]').forEach(b=>b.addEventListener('click',()=>{ location.hash='#/t/'+encodeURIComponent(b.dataset.t); }));
}

const BOX_BAT=[
  {l:'Batting',lft:1,f:d=>d.n?`<button class="pname" data-p="${esc(d.n)}">${esc(d.n)}</button>`:''},
  {l:'AB',f:d=>d.ab},{l:'R',f:d=>d.r},{l:'H',f:d=>d.h},{l:'2B',f:d=>d['2b']},{l:'3B',f:d=>d['3b']},
  {l:'HR',f:d=>d.hr},{l:'RBI',f:d=>d.rbi},{l:'BB',f:d=>d.bb},{l:'K',f:d=>d.k},{l:'HBP',f:d=>d.hbp}];
const BOX_PIT=[
  {l:'Pitching',lft:1,f:d=>d.n?`<button class="pname" data-p="${esc(d.n)}">${esc(d.n)}</button>`:''},
  {l:'IP',m:1,f:d=>ipStr(d.ip)},{l:'H',f:d=>d.h},{l:'R',f:d=>d.r},{l:'ER',f:d=>d.er},
  {l:'BB',f:d=>d.bb},{l:'K',f:d=>d.k},{l:'W',f:d=>d.w},{l:'L',f:d=>d.l},{l:'SV',f:d=>d.sv}];
const sumBox=(rows,keys)=>{ const t={}; keys.forEach(k=>t[k]=0); rows.forEach(r=>keys.forEach(k=>t[k]+=(r[k]||0))); return t; };

function boxSide(g, sk, yr){
  const s=g[sk]; let out='';
  if(s.bat.length){
    const tot=sumBox(s.bat,['ab','r','h','2b','3b','hr','rbi','bb','k','hbp']);
    out+=statTable(esc(histName(s.team, yr))+' — Batting', BOX_BAT, s.bat, tot, 'Total', '');
  }
  if(s.pit.length){
    const tot=sumBox(s.pit,['ip','h','r','er','bb','k','w','l','sv']);
    out+=statTable(esc(histName(s.team, yr))+' — Pitching', BOX_PIT, s.pit, tot, 'Total', '');
  }
  return out;
}
function lineScore(g, yr){
  const n=Math.max(g.away.line.length, g.home.line.length);
  const hd=Array.from({length:n},(_,i)=>`<th class="mono">${i+1}</th>`).join('');
  const rw=(nm,s,win)=>`<tr><td class="lft${win?' wteam':''}">${histTeamLink(nm, yr)}</td>
    ${Array.from({length:n},(_,i)=>`<td class="mono">${s.line[i]!=null?s.line[i]:''}</td>`).join('')}
    <td class="mono b">${s.R}</td><td class="mono">${s.H}</td><td class="mono">${s.E}</td></tr>`;
  return `<div class="tscroll"><table class="detail linescore"><thead><tr><th class="lft"></th>${hd}
    <th class="mono b">R</th><th class="mono">H</th><th class="mono">E</th></tr></thead><tbody>
    ${rw(g.away.team,g.away,g.away.R>g.home.R)}${rw(g.home.team,g.home,g.home.R>g.away.R)}</tbody></table></div>`;
}
function boxScore(gid){
  const g=GAMES[gid];
  if(!g){ location.hash='#/games'; return; }
  setNav('games');
  const yr = +g.date.slice(0,4);
  const a=g.away.R, hh=g.home.R;
  const bs=s=>s.bat.reduce((x,b)=>x+b.r,0);
  const untied = (g.away.bat.length && bs(g.away)!==a) || (g.home.bat.length && bs(g.home)!==hh);
  const muTeam = (team, y) => {
    const logo = TEAMS[team] ? teamLogoForYear(team, y) : null;
    return `<span class="muteam">${logo?`<img class="llogo-lg" src="${logo}" alt="">`:''}${histTeamLink(team, y)}</span>`;
  };
  app.innerHTML=`
    <button class="back" id="back">← All games</button>
    <div class="phead"><h2>${muTeam(g.away.team,yr)}<span class="vs">${a}–${hh}</span>${muTeam(g.home.team,yr)}</h2></div>
    <p class="pmeta">${esc(g.div)} · ${g.date}${g.loc?' · '+esc(g.loc):''} · ${g.innings} innings</p>
    ${lineScore(g, yr)}
    ${boxSide(g,'away',yr)}${boxSide(g,'home',yr)}
    <p class="note">The line score is the recorded official result. Batting and pitching lines are the
    player stats logged for the game${untied?', whose totals do not tie to the line score — both appear as recorded':''}.${g.away.bat.length<3&&g.home.bat.length<3?' This game predates per-player logging; the single line is the team total.':''}</p>`;
  document.getElementById('back').addEventListener('click',()=>{ location.hash='#/games'; });
  wirePlayerLinks();
  app.querySelectorAll('.pname[data-t]').forEach(b=>b.addEventListener('click',()=>{
    location.hash='#/t/'+encodeURIComponent(b.dataset.t); }));
}

/* every logged game a player appeared in for one phase, across all years —
   the shared source for both the year-scoped game log and the career splits below */
function collectPlayerGames(pl, type){
  if(!pl.gids || !pl.gids.length) return [];
  const out=[];
  pl.gids.forEach(gid=>{
    const g=GAMES[gid]; if(!g || g.phase!==type) return;
    let side=null, bat=null, pit=null;
    for(const sk of ['away','home']){
      const bb=g[sk].bat.find(x=>x.n===pl.name), pp=g[sk].pit.find(x=>x.n===pl.name);
      if(bb||pp){ side=sk; bat=bb||null; pit=pp||null; break; }
    }
    if(!side) return;
    const opp = side==='away'? g.home.team : g.away.team;
    out.push({g,side,bat,pit,opp});
  });
  return out;
}

function playerGameLog(pl, type, selYear){
  const games = collectPlayerGames(pl, type);
  if(!games.length) return '';
  const byYr={};
  games.forEach(r=>{ (byYr[r.g.date.slice(0,4)] = byYr[r.g.date.slice(0,4)] || []).push(r); });
  const yrs=Object.keys(byYr).sort();
  if(!yrs.length) return '';
  const y = yrs.includes(String(selYear)) ? String(selYear) : yrs[yrs.length-1];
  const rows=byYr[y].map(({g,side,bat,pit,opp})=>`<tr>
    <td class="lft"><button class="pname" data-g="${g.gid}">${g.date.slice(5)}</button></td>
    <td class="lft">${side==='away'?'@':'vs'} ${histTeamLink(opp, +g.date.slice(0,4))}${type==='Playoffs'?`<span class="gtag">${esc(gameTag(g))}</span>`:''}</td>
    <td>${bat?bat.ab:''}</td><td>${bat?bat.r:''}</td><td>${bat?bat.h:''}</td><td>${bat?bat.hr:''}</td>
    <td>${bat?bat.rbi:''}</td><td>${bat?bat.bb:''}</td><td>${bat?bat.k:''}</td>
    <td class="mono">${pit?ipStr(pit.ip):''}</td><td>${pit?pit.h:''}</td><td>${pit?pit.r:''}</td>
    <td>${pit?pit.er:''}</td><td>${pit?pit.k:''}</td></tr>`).join('');
  const yearChips = yrs.length>1 ? `<div class="chips logchips">${yrs.map(yy=>
    `<button data-ly="${yy}" aria-pressed="${yy===y}">${yy}</button>`).join('')}</div>` : '';
  return `<section class="stat"><h3 class="viewhead">Game Log</h3>
    <p class="pmeta">Per-game lines where recorded (2020 on). Click a date for the full box score.</p>
    ${yearChips}
    <div class="tscroll"><table class="detail"><thead><tr>
    <th class="lft">Date</th><th class="lft">Opp</th><th>AB</th><th>R</th><th>H</th><th>HR</th><th>RBI</th><th>BB</th><th>K</th>
    <th class="mono">IP</th><th>H</th><th>R</th><th>ER</th><th>K</th></tr></thead><tbody>${rows}</tbody></table></div></section>`;
}

/* NWLA per-game lines live in the separate Beavers box-score set (BV_ALL_GAMES,
   flattened across every tournament), not the main GAMES dict — matched here
   by name against each game's bat/pit lines */
function playerNWLALog(pl, selYear){
  if(!BV_ALL_GAMES.length) return '';
  const games = BV_ALL_GAMES.filter(g => (g.bat||[]).some(b=>b.n===pl.name) || (g.pit||[]).some(p=>p.n===pl.name));
  if(!games.length) return '';
  const byYr={};
  games.forEach(g=>{ (byYr[(g.date||'').slice(0,4)] = byYr[(g.date||'').slice(0,4)] || []).push(g); });
  const yrs=Object.keys(byYr).sort();
  const y = yrs.includes(String(selYear)) ? String(selYear) : yrs[yrs.length-1];
  const rows = byYr[y].map(g=>{
    const bat = (g.bat||[]).find(b=>b.n===pl.name);
    const pit = (g.pit||[]).find(p=>p.n===pl.name);
    return `<tr>
      <td class="lft"><button class="pname" data-bv="${esc(g.gid)}">${esc((g.date||'').slice(5))}</button></td>
      <td class="lft">${g.ha==='H'?'vs':'@'} ${esc(g.opp)}${g.phase?`<span class="gtag">${esc(g.phase)}</span>`:''}</td>
      <td>${bat?bat.ab:''}</td><td>${bat?bat.r:''}</td><td>${bat?bat.h:''}</td><td>${bat?bat.hr:''}</td>
      <td>${bat?bat.rbi:''}</td><td>${bat?bat.bb:''}</td><td>${bat?bat.k:''}</td>
      <td class="mono">${pit?ipStr(pit.ip):''}</td><td>${pit?pit.h:''}</td><td>${pit?pit.r:''}</td>
      <td>${pit?pit.er:''}</td><td>${pit?pit.k:''}</td></tr>`;
  }).join('');
  const yearChips = yrs.length>1 ? `<div class="chips logchips">${yrs.map(yy=>
    `<button data-ly="${yy}" aria-pressed="${yy===y}">${yy}</button>`).join('')}</div>` : '';
  return `<section class="stat"><h3 class="viewhead">Game Log</h3>
    <p class="pmeta">From the <button class="pname" data-beavers>Brookside Beavers</button>' NWLA tournament box scores. Click a date for the full box score.</p>
    ${yearChips}
    <div class="tscroll"><table class="detail"><thead><tr>
    <th class="lft">Date</th><th class="lft">Opp</th><th>AB</th><th>R</th><th>H</th><th>HR</th><th>RBI</th><th>BB</th><th>K</th>
    <th class="mono">IP</th><th>H</th><th>R</th><th>ER</th><th>K</th></tr></thead><tbody>${rows}</tbody></table></div></section>`;
}

/* ------------------------------ PLAYER SPLITS ------------------------------
   Home/Away, by field and vs-each-team breakdowns, built straight from the
   same per-game bat/pit lines the game logs use (not the season roster
   totals) — so a raw box-score line first gets reshaped into the ZERO_KEYS
   fields sumRows()/avg()/era() etc. already expect. */
function gameBatRow(bat){
  if(!bat) return null;
  const h=bat.h||0, d2=bat['2b']||0, d3=bat['3b']||0, hr=bat.hr||0, singles=h-d2-d3-hr;
  return {G_bat:1, AB:bat.ab||0, R:bat.r||0, H:h, '2B':d2, '3B':d3, HR:hr,
    RBI:bat.rbi||0, BB:bat.bb||0, K:bat.k||0, HBP:bat.hbp||0, SB:bat.sb||0,
    TB: singles + 2*d2 + 3*d3 + 4*hr, PA: (bat.ab||0)+(bat.bb||0)+(bat.hbp||0)};
}
function gamePitRow(pit){
  if(!pit) return null;
  return {G_pit:1, IPouts:pit.ip||0, W:pit.w||0, L:pit.l||0, SV:pit.sv||0,
    pH:pit.h||0, pR:pit.r||0, ER:pit.er||0, pBB:pit.bb||0, pK:pit.k||0};
}
/* group a player's per-game rows by an arbitrary key (side, field, opponent)
   and sum each bucket down to one ZERO_KEYS-shaped stat line */
function splitGroup(games, keyFn, labelFn){
  const buckets = {};
  games.forEach(r=>{
    const k = keyFn(r); if(k==null) return;
    const b = buckets[k] || (buckets[k] = {label:labelFn(k), rows:[]});
    if(r.bat) b.rows.push(gameBatRow(r.bat));
    if(r.pit) b.rows.push(gamePitRow(r.pit));
  });
  return Object.values(buckets).map(b=>({label:b.label, ...sumRows(b.rows)}));
}
const splitByUsage = (a,b) => (b.G_bat+b.G_pit) - (a.G_bat+a.G_pit);
/* a function rather than a static array — the OPS+ column needs the year
   weights for whichever games feed this particular split table, which vary
   per call (see playerSplits) */
const splitBatCols = weights => [
  {l:'Split',lft:1,f:d=>d.label},
  {l:'G',f:d=>d.G_bat},{l:'PA',f:d=>d.PA},{l:'AB',f:d=>d.AB},{l:'R',f:d=>d.R},{l:'H',f:d=>d.H},
  {l:'2B',f:d=>d['2B']},{l:'3B',f:d=>d['3B']},{l:'HR',f:d=>d.HR},{l:'RBI',f:d=>d.RBI},
  {l:'BB',f:d=>d.BB},{l:'K',f:d=>d.K},
  {l:'AVG',m:1,f:d=>rate(avg(d))},{l:'OBP',m:1,f:d=>rate(obp(d))},
  {l:'SLG',m:1,f:d=>rate(slg(d))},{l:'OPS',m:1,f:d=>rate(ops(d))},
  {l:'OPS+',m:1,f:d=>{const v=weights?opsPlusFor(d,weights):NaN;return isFinite(v)?String(v):'—';}}];
const splitPitCols = weights => [
  {l:'Split',lft:1,f:d=>d.label},
  {l:'G',f:d=>d.G_pit},{l:'IP',m:1,f:d=>ipStr(d.IPouts)},{l:'W',f:d=>d.W},{l:'L',f:d=>d.L},
  {l:'SV',f:d=>d.SV},{l:'H',f:d=>d.pH},{l:'R',f:d=>d.pR},{l:'ER',f:d=>d.ER},
  {l:'BB',f:d=>d.pBB},{l:'K',f:d=>d.pK},
  {l:'ERA',m:1,f:d=>two(era(d))},{l:'WHIP',m:1,f:d=>two(whip(d))},{l:'K/3',m:1,f:d=>two(k9(d))},
  {l:'ERA+',m:1,f:d=>{const v=weights?eraPlusFor(d,weights):NaN;return isFinite(v)?String(v):'—';}}];
function splitDim(title, rows, weights, pitWeights){
  if(!rows.length) return '';
  const total = sumRows(rows);
  const bat = total.PA>0 ? statTable('Batting', splitBatCols(weights), rows, total, 'Total', '', true) : '';
  const pit = total.IPouts>0
    ? statTable('Pitching', splitPitCols(pitWeights), rows.filter(d=>d.IPouts>0), total, 'Total', '', true) : '';
  return (bat||pit) ? `<div class="splitdim"><h4 class="divh">${esc(title)}</h4>${bat}${pit}</div>` : '';
}
/* "All" plus a chip per year a player has games in for this split — a second,
   independent year picker from the game log's below it (that one always shows
   a single year; splits default to pooling every year for a bigger sample) */
function splitYearChips(yrs, y){
  if(yrs.length<2) return '';
  return `<div class="chips logchips">
    <button data-spy="all" aria-pressed="${y==='all'}">All</button>
    ${yrs.map(yy=>`<button data-spy="${yy}" aria-pressed="${y===yy}">${yy}</button>`).join('')}</div>`;
}
function playerSplits(pl, type, selYear){
  const allGames = collectPlayerGames(pl, type);
  if(!allGames.length) return '';
  const yrs = [...new Set(allGames.map(r=>r.g.date.slice(0,4)))].sort();
  const y = yrs.includes(selYear) ? selYear : 'all';
  const games = y==='all' ? allGames : allGames.filter(r=>r.g.date.slice(0,4)===y);
  const homeAway = splitGroup(games, r=>r.side, k=>k==='home'?'Home':'Away')
    .sort((a,b)=> a.label==='Home' ? -1 : 1);
  const byField = splitGroup(games, r=>r.g.loc||'TBA', k=>esc(k)).sort(splitByUsage);
  const vsTeam = splitGroup(games, r=>r.opp||'Unknown', k=>teamLink(k)).sort(splitByUsage);
  /* one year picked → that year's own baseline (weight value is irrelevant
     with a single entry); "All" pooled → each year's actual share of this
     player's own PA across the games behind these splits, same PA-weighting
     principle as a career OPS+ */
  const post = type==='Playoffs';
  const weights = y!=='all' ? [{year:+y, pa:1, post}] : (()=>{
    const byYr = {};
    games.forEach(r=>{
      if(!r.bat) return;
      const yr = +r.g.date.slice(0,4);
      byYr[yr] = (byYr[yr]||0) + (gameBatRow(r.bat).PA||0);
    });
    return Object.entries(byYr).map(([yr,pa])=>({year:+yr, pa, post}));
  })();
  const pitWeights = y!=='all' ? [{year:+y, outs:1, post}] : (()=>{
    const byYr = {};
    games.forEach(r=>{
      if(!r.pit) return;
      const yr = +r.g.date.slice(0,4);
      byYr[yr] = (byYr[yr]||0) + (gamePitRow(r.pit).IPouts||0);
    });
    return Object.entries(byYr).map(([yr,outs])=>({year:+yr, outs, post}));
  })();
  const blocks = [splitDim('Home vs Away', homeAway, weights, pitWeights), splitDim('By Field', byField, weights, pitWeights),
    splitDim('vs Each Team', vsTeam, weights, pitWeights)].join('');
  return blocks ? `<section class="splits"><h3 class="viewhead">Splits</h3>
    <p class="pmeta">Built from per-game lines where recorded (2020 on) — may run lighter than the phase totals above, which also cover earlier, season-only years.</p>
    ${splitYearChips(yrs, y)}
    ${blocks}</section>` : '';
}
/* NWLA box scores (BV_ALL_GAMES) track home/away and opponent but not a field/venue,
   so this only offers two of the three split dimensions */
function playerNWLASplits(pl, selYear){
  if(!BV_ALL_GAMES.length) return '';
  const allGames = BV_ALL_GAMES
    .map(g=>({g, bat:(g.bat||[]).find(b=>b.n===pl.name)||null, pit:(g.pit||[]).find(p=>p.n===pl.name)||null,
      side: g.ha==='H' ? 'home' : 'away', opp:g.opp}))
    .filter(r=>r.bat||r.pit);
  if(!allGames.length) return '';
  const yrs = [...new Set(allGames.map(r=>(r.g.date||'').slice(0,4)))].sort();
  const y = yrs.includes(selYear) ? selYear : 'all';
  const games = y==='all' ? allGames : allGames.filter(r=>(r.g.date||'').slice(0,4)===y);
  const homeAway = splitGroup(games, r=>r.side, k=>k==='home'?'Home':'Away')
    .sort((a,b)=> a.label==='Home' ? -1 : 1);
  const vsTeam = splitGroup(games, r=>r.opp||'Unknown', k=>esc(k)).sort(splitByUsage);
  const blocks = [splitDim('Home vs Away', homeAway), splitDim('vs Each Team', vsTeam)].join('');
  return blocks ? `<section class="splits"><h3 class="viewhead">Splits</h3>
    ${splitYearChips(yrs, y)}
    ${blocks}</section>` : '';
}

/* ============================== CHAMPIONSHIPS ============================== */
const CHAMPS = DB.champs || [];
const CHAMP_SRC = 'https://bwbwiffleball.blogspot.com/p/champs-of-bwb-wiffleball.html';
const AWARDS = DB.awards || {};
const ASG = DB.asg || {};
/* Home Run Derby champs live only on the year-by-year ASG record (a.hrd), not in any
   player's honors.awards — build a name lookup so a player's own Accolades card can
   show it as a normal award tile alongside MVP/Cy Young/etc. */
const HRD_BY_PLAYER = {};
Object.entries(ASG).forEach(([y,a])=>{
  if(a.hrd && a.hrd!=='N/A') (HRD_BY_PLAYER[a.hrd] = HRD_BY_PLAYER[a.hrd] || []).push(+y);
});
/* All-Star Game MVP, same idea — a.mvp is normally one name, but a tie (2024:
   TJ Ciafone AND James Duffelmeyer) is stored "/"-separated, same convention
   plink()/tnick() already use for a multi-name field. */
const ASGMVP_BY_PLAYER = {};
Object.entries(ASG).forEach(([y,a])=>{
  if(!a.mvp || a.mvp==='N/A') return;
  a.mvp.split('/').map(x=>x.trim()).filter(Boolean).forEach(n=>{
    (ASGMVP_BY_PLAYER[n] = ASGMVP_BY_PLAYER[n] || []).push(+y);
  });
});
const NICK2FULL = DB.nick2full || {};
const AWARD_TEAM_ALIAS = {
  "Special K's":'Kings', 'The Process':'Process', 'Wildcats':'Process', 'Dashers':'Braves',
  'Hotdoggers':'Lavahogs', 'Hogriders':'Lavahogs', 'Soxs':'Sox', 'Bulldogs':'Mustangs',
  'Eagles':'Kraken', 'Bluefish':'Kraken', 'Mustangs&Kraken':'Kraken', 'Avondale Dashers':'Braves',
};
/* link a player name that may carry "(C)", periods (A.J.), or be a "/"/"," list */
function plink(raw){
  if(!raw) return '';
  return raw.split('/').map(chunk => chunk.split(',').map(x=>{
    const cap=/\(c\)/i.test(x);
    const disp=x.replace(/\s*\(c\)\s*/ig,'').trim();
    let key=disp;
    if(!P[key]) key=disp.replace(/\./g,'');
    if(!P[key]) key=({'Trevor Fraioli':'Trevor Meyler'})[disp]||disp;
    const el = P[key] ? `<button class="pname" data-p="${esc(key)}">${esc(disp)}</button>` : esc(disp);
    return el + (cap?' <span class="cap">C</span>':'');
  }).join(', ')).join(' / ');
}
function tnick(raw, year){
  if(!raw) return '';
  return raw.split('/').map(part=>{
    const p=part.trim(), nick=AWARD_TEAM_ALIAS[p]||p, full=NICK2FULL[nick];
    if(!full) return esc(p);
    const label = year!=null ? histNick(full, year) : TEAMS[full].nick;
    const logo = year!=null ? teamLogoForYear(full, year) : null;
    return `<button class="pname" data-t="${esc(full)}">${logo?`<img class="tlogo-mini" src="${logo}" alt="">`:''}${esc(label)}</button>`;
  }).join(' / ');
}
const wireHonors = () => {
  app.querySelectorAll('.pname[data-p]').forEach(b=>b.addEventListener('click',()=>{ location.hash='#/p/'+encodeURIComponent(b.dataset.p); }));
  app.querySelectorAll('.pname[data-t]').forEach(b=>b.addEventListener('click',()=>{ location.hash='#/t/'+encodeURIComponent(b.dataset.t); }));
  app.querySelectorAll('.pname[data-g]').forEach(b=>b.addEventListener('click',()=>{ location.hash='#/g/'+b.dataset.g; }));
};

function champsSection(){
  const tally={};
  CHAMPS.forEach(c=>{ const k=c.tm||c.full; tally[k]=(tally[k]||0)+1; });
  const badges=Object.entries(tally).sort((a,b)=>b[1]-a[1]).map(([k,n])=>
    `<span class="tbadge">${TEAMS[k]?teamLink(k):esc(k)} <b>×${n}</b></span>`).join('');

  const cards=CHAMPS.map(c=>{
    const season = c.tm && TEAMS[c.tm] && (TEAMS[c.tm].seasons||{})[c.y];
    let roster = season ? (season.roster||[]).map(r=>r.name) : (c.pl||[]).slice();
    if(c.captain && roster.includes(c.captain)){
      roster = [c.captain, ...roster.filter(n=>n!==c.captain)];
    }
    const rosterHTML = roster && roster.length
      ? `<ul class="champroster">${roster.map(n=>
          `<li>${plink(n===c.captain ? n+' (C)' : n)}</li>`).join('')}</ul>`
      : `<p class="lead">No roster on record.</p>`;
    const franchiseRow = !c.tm && FRANCHISE_SUMMARY.find(d=>d.full===c.full || d.f===c.full);
    const logo = c.tm ? teamLogoForYear(c.tm, c.y)
      : franchiseRow && (DB.franchiseLogos||{})[franchiseRow.t];
    const poLogo = (DB.postseasonLogos||{})[c.y];
    const wsLogo = (DB.worldSeriesLogos||{})[c.y];
    const badges = (poLogo||wsLogo) ? `<div class="champbadges">
        ${poLogo?`<img class="pobadge" src="${poLogo}" alt="${c.y} Postseason">`:''}
        ${wsLogo?`<img class="wsbadge" src="${wsLogo}" alt="${c.y} World Series">`:''}
      </div>` : '';
    return `<div class="champyear">
      <div class="champhead">
        ${logo?`<img class="champlogo" src="${logo}" alt="">`:''}
        <div class="champtext">
          <h4>${c.y} — ${c.tm&&TEAMS[c.tm]?teamLink(c.tm):esc(c.full)}</h4>
          <span class="cscore">${esc(c.score)}${c.tm&&TEAMS[c.tm]&&c.full!==c.tm?` · <span class="aka2">${esc(c.full)}</span>`:''}</span>
        </div>
        ${badges}
      </div>
      ${c.photo?`<img class="champphoto" src="${c.photo}" alt="${esc(c.full)} — ${c.y} champions" loading="lazy">`:''}
      ${rosterHTML}
    </div>`;
  }).join('');

  return `<h3 class="hsub" id="h-champs">Champions</h3>
    <p class="aka">Titles by franchise: ${badges}</p>
    ${cards}
    <p class="note">Overall: the champion's combined regular-season + postseason record that year.
    <span class="cap">C</span> marks the team captain, where on record.</p>`;
}

function asgSection(){
  const yrs=Object.keys(ASG).map(Number).sort((a,b)=>b-a);
  const boxFor=y=>Object.keys(GAMES).find(id=>GAMES[id].phase==='AllStar'&&GAMES[id].date.slice(0,4)==y);
  const blocks=yrs.map(y=>{
    const a=ASG[y], gid=boxFor(y);
    const sq=s=>`<div class="asgcol"><h5>${esc(s.name)} ${y}</h5><ol>${s.players.map(p=>`<li>${plink(p)}</li>`).join('')||'<li class="mut">—</li>'}</ol></div>`;
    const meta=[];
    if(a.winner) meta.push(`<b>Result:</b> ${esc(a.winner)}`);
    if(a.mvp && a.mvp!=='N/A') meta.push(`<b>MVP:</b> ${plink(a.mvp)}`);
    if(a.hrd && a.hrd!=='N/A') meta.push(`<b>HR Derby:</b> ${plink(a.hrd)}`);
    if(a.series) meta.push(`<b>Series:</b> ${esc(a.series)}`);
    if(gid) meta.push(`<button class="pname" data-g="${gid}">box score →</button>`);
    return `<div class="asgyear">
      <h4>${y} All-Star Game</h4>
      <div class="asg2">${sq(a.squads[0])}${sq(a.squads[1])}</div>
      ${meta.length?`<p class="asgmeta">${meta.join(' &nbsp;·&nbsp; ')}</p>`:''}</div>`;
  }).join('');
  return `<h3 class="hsub" id="h-asg">All-Star Games &amp; Home Run Derby</h3>
    <p class="lead">Rosters, results, game MVPs and Home Run Derby champions, ${yrs[yrs.length-1]}–${yrs[0]}.
    Squads were North / South through 2021, then Brookside / Brentwood.</p>
    ${blocks}`;
}

function awardsSection(){
  const yrs=Object.keys(AWARDS).map(Number).sort((a,b)=>b-a);
  const tbl=(rows,y)=>`<div class="tscroll"><table class="detail"><thead><tr>
    <th class="lft">Award</th><th class="lft">Winner</th><th class="lft">Team</th><th class="lft">Notes</th>
    </tr></thead><tbody>${rows.map(r=>`<tr>
      <td class="lft">${esc(r.award)}</td>
      <td class="lft">${plink(r.winner)}</td>
      <td class="lft">${tnick(r.team, y)}</td>
      <td class="lft am">${esc(r.note||'')}</td></tr>`).join('')}</tbody></table></div>`;
  const blocks=yrs.map(y=>{
    const list=AWARDS[y], divs=[...new Set(list.map(r=>r.div).filter(Boolean))];
    let inner;
    if(divs.length){
      inner=divs.map(dv=>`<h5>${dv} Division</h5>${tbl(list.filter(r=>r.div===dv), y)}`).join('');
    } else {
      inner=tbl(list, y);
    }
    return `<div class="awyear"><h4>${y}</h4>${inner}</div>`;
  }).join('');
  return `<h3 class="hsub" id="h-awards">Annual Awards</h3>
    <p class="lead">League awards by year, ${yrs[yrs.length-1]}–${yrs[0]}. 2016 and earlier (plus 2017)
    were voted by division. 2026 is a preview ballot.</p>${blocks}`;
}

function renderChampsPage(){
  setNav('champs');
  app.innerHTML = `
    <div class="phead"><h2>Champions of BWB Wiffleball</h2>
      <span class="yrs">${CHAMPS.length} title games · ${CHAMPS[CHAMPS.length-1].y}–${CHAMPS[0].y}</span></div>
    ${champsSection()}
    <p class="note">Compiled from the league's championship page
      (<a href="${CHAMP_SRC}" target="_blank" rel="noopener">bwbwiffleball.blogspot.com</a>).
      Seasons before 2017 predate the stat database; franchise links use the current franchise name where a
      team has been renamed (e.g. Brookside Eagles → Brookside Kraken). Scores are the title-game results as recorded.</p>`;
  wireHonors();
}

let awardsTab = 'awards';
function renderAwards(){
  setNav('awards');
  const tabBar = `<div class="subtabs" role="group" aria-label="Section">
    <button data-at="awards" aria-pressed="${awardsTab==='awards'}">Awards</button>
    <button data-at="asg" aria-pressed="${awardsTab==='asg'}">All-Star Games</button>
  </div>`;
  const note = awardsTab==='asg'
    ? `<p class="note">All-Star history from the league's own ASG records. Names link to a player or
       franchise page where one exists in the database (2017 on). <span class="cap">C</span> marks an
       All-Star captain.</p>`
    : `<p class="note">Annual awards from the league's own award records. Names link to a player or
       franchise page where one exists in the database (2017 on). World Series champions have their own tab.</p>`;
  app.innerHTML = `
    <div class="phead"><h2>Awards &amp; All-Star</h2></div>
    ${tabBar}
    ${awardsTab==='asg' ? asgSection() : awardsSection()}
    ${note}`;
  wireHonors();
  app.querySelectorAll('[data-at]').forEach(b=>b.addEventListener('click',()=>{
    awardsTab = b.dataset.at; renderAwards();
  }));
}

/* League Office: who actually runs BWB — hand-kept, not derived from any
   game or roster data. Each entry's titles are shown in the order given;
   the first group (Commissioner-level) gets a larger card, League
   Operations shares one row of equal-weight cards below it. */
const LEAGUE_OFFICE_LEAD = [
  {name:'Parker Gibbons', titles:['Founder','Commissioner','Head of Operations']},
  {name:'Peter Fraioli', titles:['Co-Commissioner','Head of Content Management and Design','League Operations Lead']},
  {name:'Trevor Meyler', titles:['Assistant Commissioner','League Operations Lead']},
];
const LEAGUE_OFFICE_OPS = ['TJ Ciafone','Peter Sposato','Victor Cottini','Dan Brady','Austin Corvino','Vinny Spoto'];
const LEAGUE_OFFICE_OTHER = [{name:'Griffin Krueger', titles:['League Columnist']}];
function officeCard(name, titles, big){
  const pl = P[name];
  const photo = pl && pl.photo
    ? `<img class="officephoto${big?' big':''}" src="${pl.photo}" alt="">`
    : `<span class="officephoto${big?' big':''} officephoto-blank"></span>`;
  const link = pl ? `<button class="pname officename" data-p="${esc(name)}">${esc(name)}</button>` : esc(name);
  return `<div class="officecard${big?' big':''}">
    ${photo}
    ${link}
    <ul class="officetitles">${titles.map(t=>`<li>${esc(t)}</li>`).join('')}</ul>
  </div>`;
}
function renderOffice(){
  setNav('office');
  app.innerHTML = `
    <div class="phead"><h2>League Office</h2></div>
    <p class="lead">The people who run BWB Wiffleball off the field.</p>
    <div class="officegrid officegrid-lead">${LEAGUE_OFFICE_LEAD.map(o=>officeCard(o.name, o.titles, true)).join('')}</div>
    <h3 class="hsub">League Operations</h3>
    <div class="officegrid">${LEAGUE_OFFICE_OPS.map(n=>officeCard(n, ['League Operations'], false)).join('')}</div>
    <h3 class="hsub">Columnist</h3>
    <div class="officegrid">${LEAGUE_OFFICE_OTHER.map(o=>officeCard(o.name, o.titles, false)).join('')}</div>`;
  app.querySelectorAll('.pname[data-p]').forEach(b=>b.addEventListener('click',()=>{
    location.hash = '#/p/'+encodeURIComponent(b.dataset.p);
  }));
}

function buildTicker(){
  const el = document.getElementById('ticker');
  if(!el || !GIDS.length) return;
  const ids = GIDS.slice(0, 26);
  const tkLogo = (tm,y) => { const lg = teamLogoForYear(tm,y); return lg ? `<img class="tk-logo" src="${lg}" alt="">` : ''; };
  const tkRow = (tm,yr,r,win) => `<span class="tk-row${win?' tk-w':''}">
    ${tkLogo(tm,yr)}<span class="tk-nm">${esc(histNick(tm,yr))}</span><span class="tk-r">${r}</span></span>`;
  const items = ids.map(id=>{
    const g = GAMES[id];
    const yr = +g.date.slice(0,4);
    const aw = g.away.R>g.home.R, hw = g.home.R>g.away.R;
    return `<span class="tk-item" data-g="${id}">
      <span class="tk-head"><span class="tk-d">${g.date.slice(5).replace('-','/')}</span>
      ${g.phase!=='Regular'?`<span class="gtag">${esc(gameTag(g))}</span>`:''}</span>
      ${tkRow(g.away.team,yr,g.away.R,aw)}
      ${tkRow(g.home.team,yr,g.home.R,hw)}</span>`;
  }).join('');
  el.innerHTML = `<div class="ticker-track">${items}</div>`;
  let down=false, moved=0, startX=0, startL=0;
  const start = x=>{ down=true; moved=0; startX=x; startL=el.scrollLeft; el.classList.add('drag'); };
  const move = x=>{ if(!down) return; const dx=x-startX; moved=Math.max(moved,Math.abs(dx)); el.scrollLeft=startL-dx; };
  const end = ()=>{ down=false; el.classList.remove('drag'); };
  el.addEventListener('pointerdown', e=>{ if(e.button===0) start(e.clientX); });
  el.addEventListener('pointermove', e=>move(e.clientX));
  addEventListener('pointerup', end);
  el.addEventListener('pointerleave', end);
  el.addEventListener('wheel', e=>{ if(Math.abs(e.deltaY)>Math.abs(e.deltaX)){ el.scrollLeft+=e.deltaY; e.preventDefault(); } }, {passive:false});
  el.addEventListener('click', e=>{
    if(moved>5) return;           // that was a drag, not a click
    const t = e.target.closest('.tk-item');
    if(t) location.hash = '#/g/'+t.dataset.g;
  });
}

/* --------------------------- BROOKSIDE BEAVERS ----------------------------
   `beavers` is a list, one entry per national-team tournament appearance (so
   future tournaments just add another entry) — BV_LIST is that list, and the
   flattened views below (games/roster) are what most helpers actually need. */
const BV_LIST = DB.beavers || [];
const BV_ALL_GAMES = BV_LIST.flatMap(t=>t.games);
const BV_INREG = new Set(BV_LIST.flatMap(t=>t.inRegister));
const bvName = n => BV_INREG.has(n)
  ? `<button class="pname" data-p="${esc(n)}">${esc(n)}</button>` : esc(n);

function bvLineScore(g){
  const bea = {n:'Brookside Beavers', line:g.line_bea, R:g.rf, H:g.he_bea[0], E:g.he_bea[1]};
  const opp = {n:esc(g.opp), line:g.line_opp, R:g.ra, H:g.he_opp[0], E:g.he_opp[1]};
  const [away, home] = g.ha==='H' ? [opp, bea] : [bea, opp];
  const n = Math.max(away.line.length, home.line.length, g.innings);
  const hd = Array.from({length:n},(_,i)=>`<th class="mono">${i+1}</th>`).join('');
  const rw = (s,win) => `<tr><td class="lft${win?' wteam':''}">${s.n}</td>
    ${Array.from({length:n},(_,i)=>`<td class="mono">${s.line[i]!=null?s.line[i]:(i>=s.line.length?'':'')}</td>`).join('')}
    <td class="mono b">${s.R}</td><td class="mono">${s.H}</td><td class="mono">${s.E}</td></tr>`;
  return `<div class="tscroll"><table class="detail linescore"><thead><tr><th class="lft"></th>${hd}
    <th class="mono b">R</th><th class="mono">H</th><th class="mono">E</th></tr></thead><tbody>
    ${rw(away, away.R>home.R)}${rw(home, home.R>away.R)}</tbody></table></div>`;
}

const BV_BAT = [
  {l:'Batting',lft:1,f:d=>bvName(d.n)},
  {l:'AB',f:d=>d.ab},{l:'R',f:d=>d.r},{l:'H',f:d=>d.h},{l:'2B',f:d=>d['2b']},
  {l:'3B',f:d=>d['3b']},{l:'HR',f:d=>d.hr},{l:'RBI',f:d=>d.rbi},{l:'BB',f:d=>d.bb},{l:'K',f:d=>d.k}];
const BV_PIT = [
  {l:'Pitching',lft:1,f:d=>bvName(d.n)},
  {l:'IP',m:1,f:d=>ipStr(d.ip)},{l:'H',f:d=>d.h},{l:'R',f:d=>d.r},{l:'ER',f:d=>d.er},
  {l:'BB',f:d=>d.bb},{l:'K',f:d=>d.k},{l:'W',f:d=>d.w},{l:'L',f:d=>d.l},{l:'SV',f:d=>d.sv}];

function bvBox(name, batRows, pitRows){
  let out = '';
  if(batRows && batRows.length){
    const bt = sumBox(batRows,['ab','r','h','2b','3b','hr','rbi','bb','k']);
    out += statTable(esc(name)+' — Batting', BV_BAT, batRows, bt, 'Total', '');
  }
  if(pitRows && pitRows.length){
    const pt = sumBox(pitRows,['ip','h','r','er','bb','k','w','l','sv']);
    out += statTable(esc(name)+' — Pitching', BV_PIT, pitRows, pt, 'Total', '');
  }
  return out;
}
function bvGameCard(g){
  const bea = ['Brookside Beavers', g.bat, g.pit];
  const opp = [g.opp, g.opp_bat||[], g.opp_pit||[]];
  const [away, home] = g.ha==='H' ? [opp, bea] : [bea, opp];
  const tag = `${g.ha==='H'?'vs':'@'} ${esc(g.opp)}`;
  const note = g.opp_note ? `<p class="note">${esc(g.opp_note)}</p>` : '';
  return `<details id="bvg-${esc(g.gid)}"><summary>Game ${g.g} · ${tag} · <b class="${g.res==='W'?'wteam':''}">${g.res} ${g.rf}–${g.ra}</b> <span class="tk-d">${g.time} ET</span></summary>
    ${bvLineScore(g)}
    ${bvBox(away[0], away[1], away[2])}
    ${bvBox(home[0], home[1], home[2])}
    ${note}</details>`;
}

/* career (all-tournament) per-player totals — merges a player's rows across
   every tournament they appeared in, so this stays correct as more get added */
function mergeBvRows(rows, keys){
  const byName = new Map();
  rows.forEach(r=>{
    const cur = byName.get(r.name) || Object.fromEntries(keys.map(k=>[k,0]));
    keys.forEach(k=>{ cur[k] = (cur[k]||0) + (r[k]||0); });
    byName.set(r.name, {...cur, name:r.name});
  });
  return [...byName.values()];
}
const BV_BAT_KEYS = ['G','PA','AB','R','H','2B','3B','HR','RBI','BB','K','TB'];
const BV_PIT_KEYS = ['G','IPouts','pH','pR','ER','pBB','pK','W','L','SV'];
/* shared by both the all-tournament overview and each tournament's own page —
   no OPS+ here — the Beavers' NWLA tournament games have no BWB league-year
   context to normalize against, so every row would just show '—' */
const bvBatCols = () => [
  {l:'Player',lft:1,f:d=>bvName(d.name)},
  {l:'G',f:d=>d.G},{l:'PA',f:d=>d.PA},{l:'AB',f:d=>d.AB},{l:'R',f:d=>d.R},{l:'H',f:d=>d.H},
  {l:'2B',f:d=>d['2B']},{l:'3B',f:d=>d['3B']},{l:'HR',f:d=>d.HR},{l:'RBI',f:d=>d.RBI},
  {l:'BB',f:d=>d.BB},{l:'K',f:d=>d.K},
  {l:'AVG',m:1,f:d=>rate(avg(d))},{l:'OBP',m:1,f:d=>rate(obp(d))},
  {l:'SLG',m:1,f:d=>rate(slg(d))},{l:'OPS',m:1,f:d=>rate(ops(d))}];
const bvPitCols = () => [
  {l:'Player',lft:1,f:d=>bvName(d.name)},
  {l:'G',f:d=>d.G},{l:'IP',m:1,f:d=>ipStr(d.IPouts)},{l:'W',f:d=>d.W},{l:'L',f:d=>d.L},
  {l:'SV',f:d=>d.SV},{l:'H',f:d=>d.pH},{l:'R',f:d=>d.pR},{l:'ER',f:d=>d.ER},
  {l:'BB',f:d=>d.pBB},{l:'K',f:d=>d.pK},
  {l:'ERA',m:1,f:d=>two(era(d))},{l:'WHIP',m:1,f:d=>two(whip(d))},{l:'K/3',m:1,f:d=>two(k9(d))}];
/* each tournament's page is addressed by its start date — the one field
   guaranteed unique per BV_LIST entry (two BWB trips never start the same
   day), so a URL keeps working even if more tournaments get inserted
   out of chronological order later */
const bvTournamentHref = t => '#/beavers/t/'+encodeURIComponent(t.meta.date);
function bvTournamentLabel(t){ return `${(t.meta.date||'').slice(0,4)} ${t.meta.event||t.meta.season}`; }
/* which tournament a given game id belongs to — a game-focused deep link
   (e.g. from a player's own NWLA Game Log tab) needs to land on that
   tournament's own page now that games no longer show on the overview */
function bvTournamentForGame(gid){
  return BV_LIST.find(t=>t.games.some(g=>String(g.gid)===String(gid)));
}

function renderBeavers(){
  setNav('beavers');
  if(!BV_LIST.length){ app.innerHTML = '<p class="empty">No national-team data.</p>'; return; }
  const logo = (BV_LIST.find(t=>t.logo)||{}).logo;
  const rec = BV_LIST.reduce((t,x)=>({W:t.W+x.meta.record.W, L:t.L+x.meta.record.L}), {W:0,L:0});
  const bat = mergeBvRows(BV_LIST.flatMap(t=>t.batting), BV_BAT_KEYS).map(r=>({...r, HBP:0, SF:0}))
    .sort((a,b)=>b.PA-a.PA || b.AB-a.AB);
  const pit = mergeBvRows(BV_LIST.flatMap(t=>t.pitching), BV_PIT_KEYS).sort((a,b)=>b.IPouts-a.IPouts);
  const bTot = bat.reduce((t,r)=>{['G','PA','AB','R','H','2B','3B','HR','RBI','BB','K','TB'].forEach(k=>t[k]=(t[k]||0)+r[k]);return t;},{HBP:0,SF:0});
  const pTot = pit.reduce((t,r)=>{['G','IPouts','pH','pR','ER','pBB','pK','W','L','SV'].forEach(k=>t[k]=(t[k]||0)+r[k]);return t;},{});

  /* one card per tournament linking out to its own roster/stats/game-log
     page — the overview itself only ever shows the combined, all-tournament
     picture below */
  const tournamentsHtml = BV_LIST.slice().sort((a,b)=>(b.meta.date||'').localeCompare(a.meta.date||''))
    .map(t=>{
      const tw = t.meta.record.W, tl = t.meta.record.L, tgp = tw+tl;
      return `<a class="bvtcard" href="${bvTournamentHref(t)}">
        <div class="bvtlogo">${t.logo?`<img src="${t.logo}" alt="">`:''}</div>
        <div><h4>${esc(bvTournamentLabel(t))}</h4>
        <span class="pmeta">${tw}–${tl} · ${esc(t.meta.location)} · ${tgp} game${tgp===1?'':'s'}</span></div>
      </a>`;
    }).join('');

  const gp = rec.W+rec.L;
  const overview = `<div class="recgrid">
      <div class="rec"><h4>Record</h4><div class="big">${rec.W}–${rec.L}</div>
        <div class="sub">${gp?rate(rec.W/gp):'—'} · ${gp} game${gp===1?'':'s'}</div></div>
      <div class="rec"><h4>Team Batting</h4><div class="big">${rate(avg(bTot))}/${rate(obp(bTot))}/${rate(slg(bTot))}</div>
        <div class="sub">${bTot.HR||0} HR · ${bTot.RBI||0} RBI · ${bTot.R||0} R</div></div>
      <div class="rec"><h4>Team Pitching</h4><div class="big">${two(era(pTot))} ERA</div>
        <div class="sub">${two(whip(pTot))} WHIP · ${pTot.pK||0} K · ${ipStr(pTot.IPouts||0)} IP</div></div>
    </div>`;
  const hero = `<div class="thero" style="--tp:#c99a2e;--ts:#fff">
      <div class="hero-row">${logo?`<img class="tlogo" src="${logo}" alt="">`:''}<h2>Brookside Beavers</h2></div>
      <p class="tsub"><b>${rec.W}–${rec.L}</b> all-time · ${BV_LIST.length} tournament${BV_LIST.length===1?'':'s'}</p>
    </div>`;

  app.innerHTML = `
    ${hero}
    ${overview}
    <h3 class="hsub">Tournaments</h3>
    <div class="bvtgrid">${tournamentsHtml}</div>
    <h3 class="hsub">Batting — All Tournaments</h3>
    ${statTable('', bvBatCols(), bat, {...bTot, name:'Total'}, 'Total', '', true)}
    <h3 class="hsub">Pitching — All Tournaments</h3>
    ${statTable('', bvPitCols(), pit, {...pTot, name:'Total'}, 'Total', '', true)}
    <p class="note">Combined across every tournament below. Two-sided box scores are from the team's
      GameChanger books; Beavers lines reconcile to the printed team totals, opponent batting is
      best-effort from the same screenshots (cells that could not be pinned are noted on the game).
      Games run 3–5 innings, so <b>ERA</b> and <b>K/3</b> are per 3 IP; every run is booked earned.
      Source: web.gc.com/teams/ohCbq6OU84HI.</p>`;
  wirePlayerLinks();
}
/* one tournament's own page: its roster's batting/pitching for just that
   trip (not merged with any other tournament) plus every game it played,
   grouped by phase (pool play, bracket, etc.) same as the overview used
   to show inline for all of them at once */
function renderBeaverTournament(dateKey, focusGid){
  setNav('beavers');
  const t = BV_LIST.find(x=>x.meta.date===dateKey);
  if(!t){ location.hash = '#/beavers'; return; }
  const bat = t.batting.map(r=>({...r, HBP:0, SF:0})).slice().sort((a,b)=>b.PA-a.PA || b.AB-a.AB);
  const pit = t.pitching.slice().sort((a,b)=>b.IPouts-a.IPouts);
  const bTot = sumBox(bat, [...BV_BAT_KEYS, 'HBP', 'SF']);
  const pTot = sumBox(pit, BV_PIT_KEYS);
  const phases = [];
  t.games.forEach(g=>{
    let p = phases.find(x=>x.name===g.phase);
    if(!p){ p = {name:g.phase, gs:[]}; phases.push(p); }
    p.gs.push(g);
  });
  const tw = t.meta.record.W, tl = t.meta.record.L, tgp = tw+tl;
  const hero = `<div class="thero" style="--tp:#c99a2e;--ts:#fff">
      <div class="hero-row">${t.logo?`<img class="tlogo" src="${t.logo}" alt="">`:''}<h2>${esc(bvTournamentLabel(t))}</h2></div>
      <p class="tsub"><b>${tw}–${tl}</b> · ${esc(t.meta.location)} · ${esc(t.meta.date)}${t.meta.level?` · ${esc(t.meta.level)}`:''}</p>
    </div>`;
  const overview = `<div class="recgrid">
      <div class="rec"><h4>Record</h4><div class="big">${tw}–${tl}</div>
        <div class="sub">${tgp?rate(tw/tgp):'—'} · ${tgp} game${tgp===1?'':'s'}</div></div>
      <div class="rec"><h4>Team Batting</h4><div class="big">${rate(avg(bTot))}/${rate(obp(bTot))}/${rate(slg(bTot))}</div>
        <div class="sub">${bTot.HR||0} HR · ${bTot.RBI||0} RBI · ${bTot.R||0} R</div></div>
      <div class="rec"><h4>Team Pitching</h4><div class="big">${two(era(pTot))} ERA</div>
        <div class="sub">${two(whip(pTot))} WHIP · ${pTot.pK||0} K · ${ipStr(pTot.IPouts||0)} IP</div></div>
    </div>`;
  app.innerHTML = `
    <button class="back" id="back">← Brookside Beavers</button>
    ${hero}
    ${overview}
    <h3 class="hsub">Roster — Batting</h3>
    ${statTable('', bvBatCols(), bat, {...bTot, name:'Total'}, 'Total', '', true)}
    <h3 class="hsub">Roster — Pitching</h3>
    ${statTable('', bvPitCols(), pit, {...pTot, name:'Total'}, 'Total', '', true)}
    ${phases.map(p=>`<h3 class="hsub">${esc(p.name)}</h3>${p.gs.map(bvGameCard).join('')}`).join('')}
    <p class="note">Two-sided box scores from the team's GameChanger books. Beavers lines reconcile to
      the printed team totals; opponent batting is best-effort from the same screenshots (cells that
      could not be pinned are noted on the game). Games run 3–5 innings, so <b>ERA</b> and <b>K/3</b>
      are per 3 IP; every run is booked earned. Source: web.gc.com/teams/ohCbq6OU84HI.</p>`;
  document.getElementById('back').addEventListener('click',()=>{ location.hash = '#/beavers'; });
  wirePlayerLinks();
  if(focusGid){
    const el = document.getElementById('bvg-'+focusGid);
    if(el){ el.open = true; el.scrollIntoView({block:'start'}); }
  }
}

/* ============================== BWB GRID ==============================
   An original 9-square trivia grid built entirely from this site's own data:
   every square needs a player who fits both its row and column category.
   One guess per square. Categories span franchises (5+ all-time players
   only, so no category is a two-name gimme), divisions, awards/All-Star
   honors, and career statistical thresholds sized to this league's own
   numbers (checked against the real leaderboards before picking each
   cutoff). "Today's Grid" is the same puzzle for everyone on a given day
   (seeded off the date, no server needed); "Practice Grid" reshuffles
   freely. No fabricated pick-frequency stats — landing a square shows how
   many players in league history actually qualify for it, which is real
   and computed, not guessed at. */
function gridTeamCats(){
  const rosterOf = {};
  NAMES.forEach(n=>{
    const teams = new Set();
    P[n].seasons.forEach(s=>{ if(s.type==='Regular' && s.team) teams.add(s.team); });
    teams.forEach(t=>{ (rosterOf[t] = rosterOf[t] || new Set()).add(n); });
  });
  return TEAMNAMES.filter(full => (rosterOf[full]||new Set()).size>=5).map(full=>{
    const yrs = TEAMS[full].years||[];
    return {key:'team:'+full, label:TEAMS[full].nick||full,
      logo: teamLogoForYear(full, yrs[yrs.length-1]), set: rosterOf[full]};
  });
}
function gridDivCats(){
  return ['Brookside','Brentwood'].map(canon=>({
    key:'div:'+canon, label:canon+' Division',
    set: new Set(NAMES.filter(n=>P[n].seasons.some(s=>
      s.type==='Regular' && s.team && canonicalDivision(divisionOf(s.team, s.year))===canon))),
  }));
}
function gridAwardCats(){
  const winners = {};
  const add = (award, name) => (winners[award] = winners[award] || new Set()).add(name);
  NAMES.forEach(n=>{
    const h = P[n].honors || {rings:[],awards:[],asg:[]};
    h.awards.forEach(a=>add(a.award, n));
    if(h.rings.length) add('World Series Champion', n);
    if(h.asg.length) add('All-Star', n);
  });
  Object.keys(HRD_BY_PLAYER).forEach(n=>add('Home Run Derby Champion', n));
  Object.keys(ASGMVP_BY_PLAYER).forEach(n=>add('All-Star Game MVP', n));
  Object.keys(NOHIT_BY_PITCHER).forEach(n=>add('Threw a No-Hitter', n));
  return Object.keys(winners).filter(k=>winners[k].size>=3)
    .map(k=>({key:'award:'+k, label:k, set:winners[k]}));
}
function gridStatCats(){
  const c = n => P[n].careerReg;
  // cutoffs picked against this league's own career leaderboards (not scaled from
  // any other sport) so each lands with roughly 3-15 qualifiers, never 0 or "everyone"
  return [
    ['100+ Career Home Runs', n=>c(n).HR>=100],
    ['300+ Career RBI', n=>c(n).RBI>=300],
    ['200+ Career Runs', n=>c(n).R>=200],
    ['300+ Career Hits', n=>c(n).H>=300],
    ['150+ Career Walks', n=>c(n).BB>=150],
    ['100+ Career Games Played', n=>c(n).G_bat>=100],
    ['.400+ Career AVG (150+ PA)', n=>c(n).PA>=150 && c(n).AB>0 && avg(c(n))>=0.400],
    ['1.500+ Career OPS (150+ PA)', n=>c(n).PA>=150 && c(n).AB>0 && ops(c(n))>=1.500],
    ['30+ Career Wins', n=>c(n).W>=30],
    ['150+ Career Strikeouts (Pitching)', n=>c(n).pK>=150],
    ['50+ Career Innings Pitched', n=>c(n).IPouts>=150],
    ['5+ Career Saves', n=>c(n).SV>=5],
  ].map(([label,test])=>({key:'stat:'+label, label, set:new Set(NAMES.filter(test))}));
}
let GRID_CATS = null;
function gridCats(){
  if(!GRID_CATS) GRID_CATS = [...gridTeamCats(), ...gridDivCats(), ...gridAwardCats(), ...gridStatCats()];
  return GRID_CATS;
}
function gridIntersection(a,b){ let n=0; a.set.forEach(x=>{ if(b.set.has(x)) n++; }); return n; }
function mulberry32(seed){
  return function(){
    seed |= 0; seed = (seed + 0x6D2B79F5) | 0;
    let t = Math.imul(seed ^ (seed>>>15), 1 | seed);
    t = (t + Math.imul(t ^ (t>>>7), 61 | t)) ^ t;
    return ((t ^ (t>>>14)) >>> 0) / 4294967296;
  };
}
function gridSeedFromString(s){ let h=0; for(let i=0;i<s.length;i++) h=(Math.imul(31,h)+s.charCodeAt(i))|0; return h; }
/* pick 3 row + 3 column categories with every one of the 9 squares having a real
   answer (checked, not assumed) — retries a fresh shuffle until one works, which
   given how much these category pools overlap resolves almost immediately */
function pickGrid(rng){
  const pool = gridCats();
  for(let attempt=0; attempt<300; attempt++){
    const shuffled = pool.slice();
    for(let i=shuffled.length-1;i>0;i--){ const j=Math.floor(rng()*(i+1)); [shuffled[i],shuffled[j]]=[shuffled[j],shuffled[i]]; }
    const rows = shuffled.slice(0,3), cols = shuffled.slice(3,6);
    if(rows.every(r=>cols.every(c=>gridIntersection(r,c)>0))) return {rows, cols};
  }
  return {rows: pool.slice(0,3), cols: pool.slice(3,6)};  // pathological fallback, never hit in practice
}
function newPracticeGrid(){ const {rows, cols} = pickGrid(Math.random); return {rows, cols, answers:{}}; }
function gridDailyKey(){
  const d = new Date();
  return `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`;
}
let gridMode = 'daily', gridDaily = null, gridPractice = null, gridActiveCell = null, gridError = null;
function getDailyGrid(){
  const key = gridDailyKey();
  if(!gridDaily || gridDaily.key!==key){
    const rng = mulberry32(gridSeedFromString('bwb-grid-'+key));
    const {rows, cols} = pickGrid(rng);
    gridDaily = {key, rows, cols, answers:{}};
    try{ const raw = localStorage.getItem('bwb-grid-'+key); if(raw) gridDaily.answers = JSON.parse(raw); }catch(e){}
  }
  return gridDaily;
}
function saveDailyGrid(){ try{ localStorage.setItem('bwb-grid-'+gridDaily.key, JSON.stringify(gridDaily.answers)); }catch(e){} }
function gridHeadHTML(cat){ return `${cat.logo?`<img class="gcatlogo" src="${cat.logo}" alt="">`:''}<span>${esc(cat.label)}</span>`; }
/* every name already locked in as a CORRECT answer elsewhere in this grid —
   guessing one of these again for a different square is refused, not just
   discouraged, since the whole point of a 9-square grid is 9 different names */
function gridUsedNames(puzzle){
  return new Set(Object.values(puzzle.answers).filter(a=>a.correct).map(a=>a.name));
}
function gridCellHTML(k, ans){
  if(ans){
    if(ans.correct) return `<button class="pname gpick" data-p="${esc(ans.name)}">${esc(ans.name)}</button>
      <span class="gpoolnote">${ans.pool} player${ans.pool===1?'':'s'} ${ans.pool===1?'qualifies':'qualify'}</span>`;
    return `<span class="gmiss">${esc(ans.name)}</span>`;
  }
  if(gridActiveCell===k){
    return `<form class="gform" data-cell="${k}">
      <input type="text" list="gridNames" placeholder="Player name…" autocomplete="off" value="${gridError?esc(gridError.name):''}">
      <div class="gformbtns"><button type="submit" class="gsubmit">Lock in</button>
        <button type="button" class="gcancel" data-cell="${k}">Cancel</button></div>
      ${gridError?`<p class="gerr">${gridError.reason==='used'
        ? `You've already used "${esc(gridError.name)}" elsewhere in this grid — pick someone else.`
        : `Couldn't find "${esc(gridError.name)}" — pick a name from the list.`}</p>`:''}
    </form>`;
  }
  return `<button class="gguess" type="button" data-cell="${k}">Guess</button>`;
}
/* a shareable, Wordle-style result: no answers, just a row of emoji plus
   the headline number, safe to post without spoiling that day's puzzle for
   anyone else in the league. Tries the clipboard first; since this page runs
   inside a sandboxed Artifact iframe, a blocked clipboard falls back to
   revealing the text in a selected, read-only box rather than window.prompt
   (sandboxed iframes generally can't show OS-level modals at all). */
function shareResultButton(id){
  return `<p class="note"><button type="button" class="pname" id="${id}">Share result →</button></p>
    <textarea class="b0sharebox" id="${id}box" readonly hidden></textarea>`;
}
function wireShareButton(id, getText){
  const btn = document.getElementById(id);
  if(!btn) return;
  btn.addEventListener('click', async ()=>{
    const text = getText();
    try{
      await navigator.clipboard.writeText(text);
      const orig = btn.textContent;
      btn.textContent = 'Copied to clipboard!';
      setTimeout(()=>{ btn.textContent = orig; }, 1600);
    }catch(e){
      const box = document.getElementById(id+'box');
      if(box){
        box.value = text; box.hidden = false;
        box.focus(); box.select();
      }
      btn.textContent = 'Select the text below and copy →';
    }
  });
}
/* Grid and Stat Pad share one "Arcade" nav slot with this sub-tab bar; each
   game's own render function still owns its full page (simplest way to keep
   two otherwise-unrelated games from tangling their state together) — the
   tab bar just switches the hash, and the router does the rest. */
function arcadeTabBar(active){
  return `<div class="subtabs" role="group" aria-label="Arcade game">
    <button data-ag="grid" aria-pressed="${active==='grid'}">Grid</button>
    <button data-ag="statpad" aria-pressed="${active==='statpad'}">Stat Pad</button>
    <button data-ag="b0" aria-pressed="${active==='b0'}">15-0</button>
  </div>`;
}
const ARCADE_ROUTES = {grid:'#/grid', statpad:'#/statpad', b0:'#/15-0'};
function wireArcadeTabBar(){
  app.querySelectorAll('[data-ag]').forEach(b=>b.addEventListener('click',()=>{
    location.hash = ARCADE_ROUTES[b.dataset.ag];
  }));
}
function gridShareText(puzzle){
  const rows = [];
  for(let ri=0; ri<3; ri++){
    let row = '';
    for(let ci=0; ci<3; ci++){
      const ans = puzzle.answers[ri+','+ci];
      row += ans ? (ans.correct?'🟩':'🟥') : '⬜';
    }
    rows.push(row);
  }
  const solved = Object.values(puzzle.answers).filter(a=>a.correct).length;
  return `BWB Grid ${puzzle.key}\n${rows.join('\n')}\n${solved}/9 correct`;
}
function renderGrid(){
  setNav('arcade');
  if(gridMode==='practice' && !gridPractice) gridPractice = newPracticeGrid();
  const puzzle = gridMode==='daily' ? getDailyGrid() : gridPractice;
  const rowsHTML = puzzle.rows.map((rc,ri)=>{
    const cells = puzzle.cols.map((cc,ci)=>{
      const k = ri+','+ci;
      return `<td class="gcell${puzzle.answers[k]?(puzzle.answers[k].correct?' correct':' wrong'):''}">${gridCellHTML(k, puzzle.answers[k])}</td>`;
    }).join('');
    return `<tr><th class="gside">${gridHeadHTML(rc)}</th>${cells}</tr>`;
  }).join('');
  const topRow = `<tr><th class="gcorner"></th>${puzzle.cols.map(cc=>`<th class="gtop">${gridHeadHTML(cc)}</th>`).join('')}</tr>`;
  const solved = Object.values(puzzle.answers).filter(a=>a.correct).length;
  const attempted = Object.keys(puzzle.answers).length;
  const done = attempted===9;
  app.innerHTML = `
    <div class="phead"><h2>Arcade</h2><span class="yrs">${gridMode==='daily'?`Today's Grid · ${puzzle.key}`:'Practice Grid'}</span></div>
    ${arcadeTabBar('grid')}
    <p class="lead">Every square needs one BWB Wiffleball player who fits <b>both</b> its row and column category —
      one guess per square, right or wrong. Landing a square shows how many players in league history actually
      qualify for it; fewer means you found a rarer answer.</p>
    <div class="segs" role="group" aria-label="Grid mode">
      <button data-gm="daily" aria-pressed="${gridMode==='daily'}">Today's Grid</button>
      <button data-gm="practice" aria-pressed="${gridMode==='practice'}">Practice Grid</button>
    </div>
    ${gridMode==='practice'?'<p class="note"><button class="pname" id="gridShuffle">Shuffle a new practice grid →</button></p>':''}
    <div class="gscoreboard">${solved} / 9 correct${attempted>solved?` · ${attempted-solved} missed`:''}</div>
    <div class="tscroll"><table class="gtable"><thead>${topRow}</thead><tbody>${rowsHTML}</tbody></table></div>
    ${done && gridMode==='daily' ? shareResultButton('gridShare') : ''}
    <datalist id="gridNames">${NAMES.map(n=>`<option value="${esc(n)}">`).join('')}</datalist>
    <p class="note">Franchise categories only use clubs with 5+ all-time players, so no square is a two-name gimme.
      Career stat thresholds are sized to this league's own numbers, not borrowed from anywhere else.</p>`;
  wireGrid();
  if(done && gridMode==='daily') wireShareButton('gridShare', ()=>gridShareText(puzzle));
}
function wireGrid(){
  wireArcadeTabBar();
  app.querySelectorAll('[data-gm]').forEach(b=>b.addEventListener('click',()=>{
    gridMode = b.dataset.gm; gridActiveCell = null; gridError = null;
    if(gridMode==='practice' && !gridPractice) gridPractice = newPracticeGrid();
    renderGrid();
  }));
  const shuffleBtn = document.getElementById('gridShuffle');
  if(shuffleBtn) shuffleBtn.addEventListener('click', ()=>{
    gridPractice = newPracticeGrid(); gridActiveCell = null; gridError = null; renderGrid();
  });
  app.querySelectorAll('.gguess').forEach(b=>b.addEventListener('click', ()=>{
    gridActiveCell = b.dataset.cell; gridError = null; renderGrid();
    const input = app.querySelector('.gform input'); if(input) input.focus();
  }));
  app.querySelectorAll('.gcancel').forEach(b=>b.addEventListener('click', ()=>{
    gridActiveCell = null; gridError = null; renderGrid();
  }));
  app.querySelectorAll('.gform').forEach(f=>f.addEventListener('submit', e=>{
    e.preventDefault();
    const cellK = f.dataset.cell;
    const [ri,ci] = cellK.split(',').map(Number);
    const puzzle = gridMode==='daily' ? gridDaily : gridPractice;
    const typed = f.querySelector('input').value.trim();
    if(!P[typed]){ gridError = {name: typed, reason:'notfound'}; renderGrid();
      const input = app.querySelector('.gform input'); if(input) input.focus();
      return; }
    const rowCat = puzzle.rows[ri], colCat = puzzle.cols[ci];
    const correct = rowCat.set.has(typed) && colCat.set.has(typed);
    if(correct && gridUsedNames(puzzle).has(typed)){
      gridError = {name: typed, reason:'used'}; renderGrid();
      const input = app.querySelector('.gform input'); if(input) input.focus();
      return;
    }
    gridError = null;
    puzzle.answers[cellK] = {name: typed, correct, pool: gridIntersection(rowCat, colCat)};
    gridActiveCell = null;
    if(gridMode==='daily') saveDailyGrid();
    renderGrid();
  }));
  app.querySelectorAll('.pname[data-p]').forEach(b=>b.addEventListener('click',()=>{
    location.hash='#/p/'+encodeURIComponent(b.dataset.p);
  }));
}

/* ============================== BWB STAT PAD ==============================
   A second original game, distinct from the Grid: instead of "find any
   right answer," this one is "find the best answer." Five rows, each with
   1-2 requirements (some checked in the specific season you submit, some
   checked anywhere in the player's career); submit a player and a year for
   each, and your score for that row is that player's real single-season
   total in one target counting stat for the year you picked. The scoring
   idea — submit a player+year meeting stated requirements, score = their
   real stat total that year — is a generic constrained-optimization format;
   every requirement, stat cutoff, and word of copy here is original and
   built from this site's own data, not reproduced from anywhere else. */
const STATPAD_STATS = [
  {key:'HR', label:'Home Runs', get:s=>(s&&s.HR)||0},
  {key:'RBI', label:'RBI', get:s=>(s&&s.RBI)||0},
  {key:'R', label:'Runs', get:s=>(s&&s.R)||0},
  {key:'H', label:'Hits', get:s=>(s&&s.H)||0},
  {key:'BB', label:'Walks', get:s=>(s&&s.BB)||0},
  {key:'W', label:'Wins', get:s=>(s&&s.W)||0},
  {key:'pK', label:'Strikeouts (Pitching)', get:s=>(s&&s.pK)||0},
  {key:'SV', label:'Saves', get:s=>(s&&s.SV)||0},
];
function statTargetMeta(key){ return STATPAD_STATS.find(s=>s.key===key); }
/* "same season" requirements need a year-by-year roster, unlike the Grid's
   career-wide "ever played for" sets */
function statpadTeamCats(){
  const yearsOf = {};
  NAMES.forEach(n=>{
    P[n].seasons.forEach(s=>{ if(s.type==='Regular' && s.team){
      const m = yearsOf[s.team] = yearsOf[s.team] || {};
      (m[n] = m[n] || new Set()).add(s.year);
    }});
  });
  return TEAMNAMES.filter(full=>Object.keys(yearsOf[full]||{}).length>=5).map(full=>{
    const yrs = TEAMS[full].years||[];
    return {key:'team:'+full, label:TEAMS[full].nick||full, sameSeason:true,
      logo: teamLogoForYear(full, yrs[yrs.length-1]),
      yearsFor: n => (yearsOf[full]||{})[n] || new Set()};
  });
}
function statpadDivCats(){
  const yearsOf = {};
  NAMES.forEach(n=>{
    P[n].seasons.forEach(s=>{
      if(s.type!=='Regular' || !s.team) return;
      const canon = canonicalDivision(divisionOf(s.team, s.year));
      if(!canon) return;
      const m = yearsOf[canon] = yearsOf[canon] || {};
      (m[n] = m[n] || new Set()).add(s.year);
    });
  });
  return Object.keys(yearsOf).map(canon=>({
    key:'div:'+canon, label:canon+' Division', sameSeason:true,
    yearsFor: n => (yearsOf[canon]||{})[n] || new Set(),
  }));
}
/* career-wide requirements reuse the Grid's own award/stat category sets —
   those are already "true at any point in their career," exactly what a
   "career" requirement here needs, so no separate logic to duplicate */
function statpadAnytimeCats(){
  return [...gridAwardCats(), ...gridStatCats()].map(c=>({...c, sameSeason:false}));
}
let STATPAD_QUALS = null;
function statpadQualPool(){
  if(!STATPAD_QUALS) STATPAD_QUALS = [...statpadTeamCats(), ...statpadDivCats(), ...statpadAnytimeCats()];
  return STATPAD_QUALS;
}
/* years a name could legally submit for one row: their own real regular
   seasons, narrowed by every "same season" requirement in that row (an
   "anytime" requirement doesn't narrow years — it's checked separately) */
function statpadRowYears(quals, name){
  let yrs = new Set(svSeasons(P[name]));
  quals.filter(q=>q.sameSeason).forEach(q=>{
    const qy = q.yearsFor(name);
    yrs = new Set([...yrs].filter(y=>qy.has(y)));
  });
  return yrs;
}
function statpadRowEligible(quals, name){
  if(quals.some(q=>!q.sameSeason && !q.set.has(name))) return false;
  return statpadRowYears(quals, name).size>0;
}
/* every real (name,year) combo that legally satisfies one row, as the target
   stat's actual value that year — the full field a submitted answer is
   being judged against, so "how good" reflects this league's real range
   for that exact combination of requirements, not a guessed-at scale */
function statpadRowCombos(quals, meta){
  const combos = [];
  NAMES.forEach(n=>{
    if(quals.some(q=>!q.sameSeason && !q.set.has(n))) return;
    statpadRowYears(quals, n).forEach(y=>{ combos.push({name:n, year:y, value: meta.get(svRegRow(P[n], y))}); });
  });
  return combos;
}
/* black/bronze/silver/gold/platinum, in that low-to-high order — an
   original 5-band tier read on the same percentile svColor already uses,
   not tied to any other game's specific cutoffs or palette */
/* Platinum is reserved for the single best real answer that row could have
   had (an exact match on the max, not just a high percentile) — checked by
   value against the row's own field, not inferred from the percentile band,
   since ties near the top could otherwise land just under it or over it by
   svPct's tie-averaging */
function statpadTier(pct, isBest){
  if(isBest) return {name:'Platinum', color:'#d7e6ea'};
  if(pct==null) return {name:'Silver', color:'#b7bcc4'};
  if(pct>=60) return {name:'Gold', color:'var(--gold)'};
  if(pct>=40) return {name:'Silver', color:'#b7bcc4'};
  if(pct>=20) return {name:'Bronze', color:'#b3763f'};
  return {name:'Black', color:'#71757c'};
}
function statpadFailureReason(quals, name, year){
  if(!P[name]) return `Couldn't find "${name}" — pick a name from the list.`;
  const failedCareer = quals.filter(q=>!q.sameSeason && !q.set.has(name));
  if(failedCareer.length) return `${name} doesn't have: ${failedCareer.map(q=>q.label).join(', ')}.`;
  if(!svRegRow(P[name], year)) return `${name} has no recorded regular season in ${year}.`;
  const failedSeason = quals.filter(q=>q.sameSeason && !q.yearsFor(name).has(year));
  if(failedSeason.length) return `${name} wasn't with ${failedSeason.map(q=>q.label).join(', ')} in ${year}.`;
  return null;
}
/* the exact (player, year) pairs already locked into other rows — the same
   player can fill two rows in two different years, but the identical
   player-and-year combo can't answer two rows */
function statpadUsedCombos(puzzle, excludeRow){
  const set = new Set();
  Object.entries(puzzle.answers).forEach(([idx,a])=>{ if(+idx!==excludeRow) set.add(a.name+'|'+a.year); });
  return set;
}
function sameQualSet(a,b){
  if(a.length!==b.length) return false;
  return a.map(q=>q.key).sort().join('|') === b.map(q=>q.key).sort().join('|');
}
function pickStatpadRow(rng, pool, existingRows){
  for(let tries=0; tries<30; tries++){
    const count = rng()<0.55 ? 2 : 1;
    const shuffled = pool.slice();
    for(let i=shuffled.length-1;i>0;i--){ const j=Math.floor(rng()*(i+1)); [shuffled[i],shuffled[j]]=[shuffled[j],shuffled[i]]; }
    const quals = shuffled.slice(0, count);
    if(existingRows.some(r=>sameQualSet(r,quals))) continue;
    if(NAMES.some(n=>statpadRowEligible(quals, n))) return quals;
  }
  return [pool[Math.floor(rng()*pool.length)]];
}
function pickStatpad(rng){
  const pool = statpadQualPool();
  const rows = [];
  for(let i=0;i<5;i++) rows.push(pickStatpadRow(rng, pool, rows));
  const stat = STATPAD_STATS[Math.floor(rng()*STATPAD_STATS.length)];
  return {statKey: stat.key, rows};
}
let statpadMode='daily', statpadDaily=null, statpadPractice=null, statpadReopenRow=null,
  statpadErrorRow=null, statpadErrorMsg=null, statpadErrorName=null;
function getDailyStatpad(){
  const key = gridDailyKey();
  if(!statpadDaily || statpadDaily.key!==key){
    const rng = mulberry32(gridSeedFromString('bwb-statpad-'+key));
    const {statKey, rows} = pickStatpad(rng);
    statpadDaily = {key, statKey, rows, answers:{}, guesses:0};
    try{ const raw = localStorage.getItem('bwb-statpad-'+key); if(raw) Object.assign(statpadDaily, JSON.parse(raw)); }catch(e){}
  }
  return statpadDaily;
}
function saveDailyStatpad(){
  try{ localStorage.setItem('bwb-statpad-'+statpadDaily.key,
    JSON.stringify({answers: statpadDaily.answers, guesses: statpadDaily.guesses})); }catch(e){}
}
function newPracticeStatpad(){ const {statKey, rows} = pickStatpad(Math.random); return {statKey, rows, answers:{}, guesses:0}; }
function statpadQualChip(q){
  return `<span class="spq">${q.logo?`<img class="spqlogo" src="${q.logo}" alt="">`:''}${esc(q.label)}
    <i class="spqtag">${q.sameSeason?'that season':'career'}</i></span>`;
}
const ORDINAL_TH = n => { const s=['th','st','nd','rd'], v=n%100; return n+(s[(v-20)%10]||s[v]||s[0]); };
function statpadRowHTML(puzzle, ri){
  const row = puzzle.rows[ri];
  const ans = puzzle.answers[ri];
  const meta = statTargetMeta(puzzle.statKey);
  const showForm = !ans || statpadReopenRow===ri;
  const qualsHTML = `<div class="spquals">${row.map(statpadQualChip).join('')}</div>`;
  let bodyHTML, rowStyle = '', tierClass = '';
  if(!showForm){
    const vals = puzzle.rowValues[ri];
    const pct = svPct(vals, ans.value, false);
    const isBest = vals.length>0 && ans.value===Math.max(...vals);
    const tier = statpadTier(pct, isBest);
    rowStyle = ` style="--tier:${tier.color}"`;
    tierClass = ' tiered';
    bodyHTML = `<div class="spval"><button class="pname" data-p="${esc(ans.name)}">${esc(ans.name)}</button>
      <span class="spyear">${ans.year}</span><b class="spscore" style="color:${tier.color}">${ans.value} ${esc(meta.label)}</b></div>
      <div class="sptierrow"><span class="sptier" style="color:${tier.color}">${tier.name}</span>${pct!=null?
        `<span class="sppct">${ORDINAL_TH(pct)} percentile of every valid answer</span>`:''}</div>
      <button type="button" class="spretry" data-row="${ri}">Try a different player →</button>`;
  } else {
    const errHere = statpadErrorRow===ri;
    bodyHTML = `<form class="spform" data-row="${ri}">
      <select class="spplayer">
        <option value="" disabled ${errHere?'':'selected'}>Choose a player…</option>
        ${NAMES.map(n=>`<option value="${esc(n)}"${errHere&&n===statpadErrorName?' selected':''}>${esc(n)}</option>`).join('')}
      </select>
      <select class="spyear">${ALL_YEARS.map(y=>`<option value="${y}">${y}</option>`).join('')}</select>
      <button type="submit" class="gsubmit">Submit</button>
      ${ans?`<button type="button" class="gcancel" data-row="${ri}">Cancel</button>`:''}
    </form>
    ${errHere?`<p class="gerr">${esc(statpadErrorMsg)}</p>`:''}`;
  }
  return `<div class="sprow${ans&&!showForm?' answered':''}${tierClass}"${rowStyle}>${qualsHTML}${bodyHTML}</div>`;
}
/* revealed only once every row is filled — the actual best real answers for
   each row, so a finished pad becomes a little of its own leaderboard */
function statpadRevealHTML(puzzle){
  const meta = statTargetMeta(puzzle.statKey);
  const blocks = puzzle.rows.map((row,ri)=>{
    const ans = puzzle.answers[ri];
    const top5 = puzzle.rowCombos[ri].slice().sort((a,b)=>b.value-a.value).slice(0,5);
    const items = top5.map((c,i)=>{
      const mine = c.name===ans.name && c.year===ans.year;
      return `<li class="${mine?'sprk-mine':''}"><span class="sprk-n">${i+1}.</span>
        <button class="pname" data-p="${esc(c.name)}">${esc(c.name)}</button>
        <span class="spyear">${c.year}</span><b>${c.value}</b>${mine?' <span class="sprk-tag">your pick</span>':''}</li>`;
    }).join('');
    const inTop5 = top5.some(c=>c.name===ans.name && c.year===ans.year);
    return `<div class="sprk"><div class="spquals">${row.map(statpadQualChip).join('')}</div>
      <ol class="sprklist">${items}</ol>
      ${inTop5?'':`<p class="sprk-yours">Your pick — <button class="pname" data-p="${esc(ans.name)}">${esc(ans.name)}</button>
        ${ans.year}: <b>${ans.value}</b> ${esc(meta.label)}</p>`}
    </div>`;
  }).join('');
  return `<h3 class="hsub">Best Possible Answers</h3>
    <p class="pmeta">The top 5 real player-seasons that could have legally answered each row, ${esc(meta.label)} —
    now that the pad is done, see how close you got.</p>${blocks}`;
}
const STATPAD_TIER_EMOJI = {Black:'⬛', Bronze:'🟫', Silver:'⬜', Gold:'🟨', Platinum:'💎'};
function statpadShareText(puzzle){
  const meta = statTargetMeta(puzzle.statKey);
  const strip = puzzle.rows.map((_,ri)=>{
    const ans = puzzle.answers[ri];
    const vals = puzzle.rowValues[ri];
    const isBest = vals.length>0 && ans.value===Math.max(...vals);
    const pct = svPct(vals, ans.value, false);
    return STATPAD_TIER_EMOJI[statpadTier(pct, isBest).name];
  }).join('');
  const total = Object.values(puzzle.answers).reduce((s,a)=>s+a.value,0);
  return `BWB Stat Pad ${puzzle.key} (${meta.label})\n${strip}\n${total} total ${meta.label}`;
}
function renderStatpad(){
  setNav('arcade');
  if(statpadMode==='practice' && !statpadPractice) statpadPractice = newPracticeStatpad();
  const puzzle = statpadMode==='daily' ? getDailyStatpad() : statpadPractice;
  const meta = statTargetMeta(puzzle.statKey);
  if(!puzzle.rowCombos){
    puzzle.rowCombos = puzzle.rows.map(row=>statpadRowCombos(row, meta));
    puzzle.rowValues = puzzle.rowCombos.map(combos=>combos.map(c=>c.value));
  }
  const total = Object.values(puzzle.answers).reduce((s,a)=>s+a.value,0);
  const filled = Object.keys(puzzle.answers).length;
  const done = filled===puzzle.rows.length;
  const rowsHTML = puzzle.rows.map((_,ri)=>statpadRowHTML(puzzle, ri)).join('');
  const revealHTML = done ? statpadRevealHTML(puzzle) : '';
  app.innerHTML = `
    <div class="phead"><h2>Arcade</h2><span class="yrs">${statpadMode==='daily'?`Today's Pad · ${puzzle.key}`:'Practice Pad'}</span></div>
    ${arcadeTabBar('statpad')}
    <p class="lead">Target stat: <b>${esc(meta.label)}</b>, single season. Submit one player — and the year — per
      row that meets its requirements: a "career" tag means true anytime in their career, a "that season" tag
      means it has to hold in the year you submit. Your score for a row is that player's real ${esc(meta.label)}
      total in the year you pick, so the goal is finding the <i>best</i> valid year, not just any valid one.</p>
    <div class="segs" role="group" aria-label="Stat Pad mode">
      <button data-spm="daily" aria-pressed="${statpadMode==='daily'}">Today's Pad</button>
      <button data-spm="practice" aria-pressed="${statpadMode==='practice'}">Practice Pad</button>
    </div>
    ${statpadMode==='practice'?'<p class="note"><button class="pname" id="statpadShuffle">Shuffle a new practice pad →</button></p>':''}
    <div class="gscoreboard">${total} total ${esc(meta.label)} · ${filled}/5 rows filled · ${puzzle.guesses||0} guess${puzzle.guesses===1?'':'es'}</div>
    <div class="statpad">${rowsHTML}</div>
    ${revealHTML}
    ${done && statpadMode==='daily' ? shareResultButton('statpadShare') : ''}
    <p class="note">Franchise requirements only use clubs with 5+ all-time players. Award/honor and career-total
      requirements are checked against this league's own real record — nothing here is estimated. Once a row is
      filled, it's ranked against every real player-year that could have legally answered that exact row and
      tiered <span style="color:${statpadTier(10,false).color}">Black</span> ·
      <span style="color:${statpadTier(30,false).color}">Bronze</span> ·
      <span style="color:${statpadTier(50,false).color}">Silver</span> ·
      <span style="color:${statpadTier(70,false).color}">Gold</span> ·
      <span style="color:${statpadTier(null,true).color}">Platinum</span>, worst to best — Platinum is only the single
      best real answer that row could have had, the rest split evenly across the other four.</p>`;
  wireStatpad();
  if(done && statpadMode==='daily') wireShareButton('statpadShare', ()=>statpadShareText(puzzle));
}
function wireStatpad(){
  wireArcadeTabBar();
  app.querySelectorAll('[data-spm]').forEach(b=>b.addEventListener('click',()=>{
    statpadMode = b.dataset.spm; statpadReopenRow=null; statpadErrorRow=null;
    if(statpadMode==='practice' && !statpadPractice) statpadPractice = newPracticeStatpad();
    renderStatpad();
  }));
  const shuffleBtn = document.getElementById('statpadShuffle');
  if(shuffleBtn) shuffleBtn.addEventListener('click', ()=>{
    statpadPractice = newPracticeStatpad(); statpadReopenRow=null; statpadErrorRow=null; renderStatpad();
  });
  app.querySelectorAll('.spretry').forEach(b=>b.addEventListener('click',()=>{
    statpadReopenRow = +b.dataset.row; statpadErrorRow=null; renderStatpad();
    const sel = app.querySelector('.spform select.spplayer'); if(sel) sel.focus();
  }));
  app.querySelectorAll('.gcancel').forEach(b=>b.addEventListener('click',()=>{
    statpadReopenRow = null; statpadErrorRow = null; renderStatpad();
  }));
  app.querySelectorAll('.spform').forEach(f=>f.addEventListener('submit', e=>{
    e.preventDefault();
    const ri = +f.dataset.row;
    const puzzle = statpadMode==='daily' ? statpadDaily : statpadPractice;
    const name = f.querySelector('select.spplayer').value;
    const year = +f.querySelector('select.spyear').value;
    if(!name) return;
    puzzle.guesses = (puzzle.guesses||0) + 1;
    let reason = statpadFailureReason(puzzle.rows[ri], name, year);
    if(!reason && statpadUsedCombos(puzzle, ri).has(name+'|'+year))
      reason = `${name} in ${year} already answers another row — pick a different player or year.`;
    if(reason){
      statpadErrorRow = ri; statpadErrorMsg = reason; statpadErrorName = name;
      if(statpadMode==='daily') saveDailyStatpad();
      renderStatpad();
      return;
    }
    const value = statTargetMeta(puzzle.statKey).get(svRegRow(P[name], year));
    puzzle.answers[ri] = {name, year, value};
    statpadReopenRow = null; statpadErrorRow = null;
    if(statpadMode==='daily') saveDailyStatpad();
    renderStatpad();
  }));
  app.querySelectorAll('.pname[data-p]').forEach(b=>b.addEventListener('click',()=>{
    location.hash='#/p/'+encodeURIComponent(b.dataset.p);
  }));
}

/* ============================== BWB 15-0 ==============================
   A third original Arcade game: a 5-round draft. Each round deals one real
   BWB team-and-year — that club's actual roster for that single season —
   and you draft exactly one player from it onto your team; the next round
   deals a different team-year. No player can be drafted twice even under a
   different year. 2 of the 5 rounds — a random pair, different every deal
   — are Pitcher Rounds: the pool for those two rounds is only players who
   actually pitched that season, and whoever you draft there joins your
   pitching staff automatically — they still hit for you too, same as
   everyone else, using their real batting line. No manual
   lineup step, no budget or salary cap: every player is a free pick, so the
   season simulation itself is where the real difficulty lives. Once locked,
   an actual 15-game simulation (not a single formula) determines the
   record chasing a perfect 15-0. Only the general shape (deal themed pools
   round by round, draft a fixed roster, project a season record from it)
   is a generic, widely-cloned format; the pool logic, the regression, the
   two-sided simulation and all the wording and visuals are original and
   built from this site's own numbers — an openly rough estimate, not a
   real simulation of an actual wiffleball game. */
const B0_GAMES = 15, B0_ROSTER = 5, B0_PITCHER_COUNT = 2;
/* which 2 of the 5 rounds are Pitcher Rounds is itself random per deal —
   drawn from the same seeded rng as everything else, so the daily draft is
   still reproducible/shareable, and practice drafts get a fresh pair each
   time — a partial Fisher-Yates shuffle of the 5 round indices. */
function b0PickPitcherRounds(rng){
  const idxs = [0,1,2,3,4];
  for(let i=idxs.length-1;i>0;i--){ const j=Math.floor(rng()*(i+1)); [idxs[i],idxs[j]]=[idxs[j],idxs[i]]; }
  return idxs.slice(0, B0_PITCHER_COUNT).sort((a,b)=>a-b);
}
let B0_AVG = null;
/* league-average AVG/SLG/BB-rate/HBP-rate/ERA (every regular-season line
   ever recorded, combined) and league-average runs per team-game (straight
   off real box scores) — the real numbers the sample-size regression and
   the win projection are scaled against */
function b0League(){
  if(B0_AVG) return B0_AVG;
  const rows = [];
  NAMES.forEach(n=>{ P[n].seasons.forEach(s=>{ if(s.type==='Regular' && !s.split) rows.push(s); }); });
  const tot = sumRows(rows);
  let runs=0, games=0;
  GIDS.forEach(gid=>{ const g=GAMES[gid]; if(g.phase==='Regular'){ runs+=g.away.R+g.home.R; games+=2; } });
  B0_AVG = {
    avg: avg(tot), slg: slg(tot), ops: ops(tot), era: era(tot),
    bbRate: tot.PA ? tot.BB/tot.PA : 0, hbpRate: tot.PA ? tot.HBP/tot.PA : 0,
    oneBRate: tot.PA ? tot['1B']/tot.PA : 0, twoBRate: tot.PA ? tot['2B']/tot.PA : 0,
    threeBRate: tot.PA ? tot['3B']/tot.PA : 0, hrRate: tot.PA ? tot.HR/tot.PA : 0,
    sbRate: tot.PA ? tot.SB/tot.PA : 0, csRate: tot.PA ? tot.CS/tot.PA : 0,
    kRate: tot.IPouts ? tot.pK/tot.IPouts : 0, bbAllowedRate: tot.IPouts ? tot.pBB/tot.IPouts : 0,
    hAllowedRate: tot.IPouts ? tot.pH/tot.IPouts : 0,
    rpg: games ? runs/games : 5,
  };
  return B0_AVG;
}
let B0_RUNS_POOL = null;
/* every real team-game run total this league has actually produced (each
   game counted twice — once for each side), the pool the simulation
   bootstraps from instead of an idealized Poisson curve. BWB scoring runs
   far bursier than Poisson assumes (real box scores here include 30+ run
   games), so sampling straight from what's actually happened captures that
   real blowout-or-shutout shape instead of a tame bell curve built from
   just the mean. A handful of dates are forfeit batches, not real games —
   the same signature the Records page's streak-building already flags
   (4+ games logged on one date, one score pair accounting for a strict
   majority of them) — excluded here for the same reason: they're canned,
   repeated placeholders, not real single-game outcomes to sample from. */
function b0RunsPool(){
  if(B0_RUNS_POOL) return B0_RUNS_POOL;
  const regGames = GIDS.map(gid=>GAMES[gid]).filter(g=>g.phase==='Regular');
  const byDate = {};
  regGames.forEach(g=>{ (byDate[g.date] = byDate[g.date] || []).push(g); });
  const badDates = new Set();
  Object.entries(byDate).forEach(([date, gs])=>{
    if(gs.length<4) return;
    const counts = {};
    gs.forEach(g=>{ const k=g.away.R+'-'+g.home.R; counts[k]=(counts[k]||0)+1; });
    if(Math.max(...Object.values(counts))/gs.length > 0.5) badDates.add(date);
  });
  const pool = [];
  regGames.forEach(g=>{ if(badDates.has(g.date)) return; pool.push(g.away.R, g.home.R); });
  B0_RUNS_POOL = pool;
  return pool;
}
/* a 2-game hot streak and a 15-game season shouldn't count for the same
   thing — shrink each player-season's rate-driving fields toward league
   average by how far its own games-played (batting) or innings (pitching)
   falls short of this site's own established qualification bar (SV_MING/
   SV_MINOUTS, the same 9 games / 12 IP already used for percentile
   rankings elsewhere), instead of trusting a tiny sample at face value.
   AB/PA/IPouts themselves are untouched — those games really happened. */
function b0Shrink(value, leagueRate, denom, w){ return w*value + (1-w)*leagueRate*denom; }
function b0RegressLine(line){
  const lg = b0League();
  const out = {...line};
  if(line.AB>0){
    const w = Math.min(1, (line.G_bat||0)/SV_MING), pa = line.PA;
    out.H = w*line.H + (1-w)*lg.avg*line.AB;
    out.BB = b0Shrink(line.BB, lg.bbRate, pa, w);
    out.HBP = b0Shrink(line.HBP, lg.hbpRate, pa, w);
    out.TB = w*line.TB + (1-w)*lg.slg*line.AB;
    out['1B'] = b0Shrink(line['1B'], lg.oneBRate, pa, w);
    out['2B'] = b0Shrink(line['2B'], lg.twoBRate, pa, w);
    out['3B'] = b0Shrink(line['3B'], lg.threeBRate, pa, w);
    out.HR = b0Shrink(line.HR, lg.hrRate, pa, w);
    out.SB = b0Shrink(line.SB, lg.sbRate, pa, w);
    out.CS = b0Shrink(line.CS, lg.csRate, pa, w);
  }
  if(line.IPouts>0){
    const w = Math.min(1, line.IPouts/SV_MINOUTS), outs = line.IPouts;
    out.ER = w*line.ER + (1-w)*(lg.era/9)*outs;
    out.pK = b0Shrink(line.pK, lg.kRate, outs, w);
    out.pBB = b0Shrink(line.pBB, lg.bbAllowedRate, outs, w);
    out.pH = b0Shrink(line.pH, lg.hAllowedRate, outs, w);
  }
  return out;
}
let B0_ROUND_POOL = null, B0_PITCHER_POOL = null;
/* every (team, year) with a real, playable-sized roster that season — the
   deck the game's 3 open rounds get dealt from. Regression is applied
   once, here, so the pool's own display and everything drafted from it
   already agree with what the simulation will actually use. */
/* line = the player's own real regular-season totals for that team-year
   (integers, exactly what actually happened, what gets shown while
   drafting) — never overwritten. regLine = the same season shrunk toward
   league average for sample size, used only for the simulation's team
   totals (b0Simulate), never for display. Showing the regressed numbers
   instead of the real ones was a real bug — a player's "stat line" read
   something like "1.38 HR" instead of a real integer. */
function b0RoundPool(){
  if(B0_ROUND_POOL) return B0_ROUND_POOL;
  const pairs = [];
  TEAMNAMES.forEach(t=>{
    Object.entries(TEAMS[t].seasons||{}).forEach(([y,s])=>{
      const roster = (s.roster||[])
        .filter(e=>e.regular && (e.regular.AB>0 || e.regular.IPouts>0))
        .map(e=>({name:e.name, line:e.regular, regLine: b0RegressLine(e.regular)}));
      if(roster.length>=5) pairs.push({team:t, year:+y, roster});
    });
  });
  B0_ROUND_POOL = pairs;
  return pairs;
}
/* the same deck, but each team-year's roster trimmed to only the players
   who actually pitched that season — the pool the 2 forced Pitcher Rounds
   deal from, so every option there is a real, legal pitching pick. */
function b0PitcherPool(){
  if(B0_PITCHER_POOL) return B0_PITCHER_POOL;
  const pairs = [];
  TEAMNAMES.forEach(t=>{
    Object.entries(TEAMS[t].seasons||{}).forEach(([y,s])=>{
      const roster = (s.roster||[])
        .filter(e=>e.regular && e.regular.IPouts>0)
        .map(e=>({name:e.name, line:e.regular, regLine: b0RegressLine(e.regular)}));
      if(roster.length>=2) pairs.push({team:t, year:+y, roster});
    });
  });
  B0_PITCHER_POOL = pairs;
  return pairs;
}
/* draw one game's runs by taking a REAL team-game run total off the
   league's own board and scaling it to this team's own projected rate —
   preserves the real, bursty shape of actual BWB scoring (see b0RunsPool)
   instead of assuming a smooth textbook curve centered on the mean */
function b0BootstrapDraw(rate, avgRate, pool, rng){
  const raw = pool[Math.floor(rng()*pool.length)];
  const scale = avgRate>0 ? rate/avgRate : 1;
  return Math.max(0, Math.round(raw*scale));
}
/* offense comes from all 5 drafted players; pitching comes ONLY from the
   2 picks made in the Pitcher Rounds — a player who happened to pitch a
   little that season but wasn't drafted IN a Pitcher Round simply doesn't
   count toward the team's run prevention */
function b0Simulate(picks, pitcherNames, rng){
  const teamBat = sumRows(picks.map(p=>p.regLine));
  const teamPit = sumRows(picks.filter(p=>pitcherNames.includes(p.name)).map(p=>p.regLine));
  const teamOPS = ops(teamBat), teamERA = era(teamPit);
  const lg = b0League();
  const pool = b0RunsPool();
  const projRPG = lg.ops>0 ? lg.rpg*(teamOPS/lg.ops) : lg.rpg;
  const projRA = (isFinite(teamERA) && lg.era>0) ? lg.rpg*(teamERA/lg.era) : lg.rpg;
  const winPct = projRPG/(projRPG+projRA);
  const rand = rng || Math.random;
  const log = [];
  let wins=0;
  for(let g=1; g<=B0_GAMES; g++){
    const rs = b0BootstrapDraw(projRPG, lg.rpg, pool, rand), ra = b0BootstrapDraw(projRA, lg.rpg, pool, rand);
    const win = rs>ra || (rs===ra && rand()<0.5);   // BWB games can't literally end tied — a coin flip breaks it
    if(win) wins++;
    log.push({g, rs, ra, win});
  }
  return {teamOPS, teamERA, projRPG, projRA, winPct, wins, losses: B0_GAMES-wins, log};
}
/* deal all 5 rounds at once: 2 randomly-chosen round indices (a fresh draw
   every deal — see b0PickPitcherRounds) come from the pitcher-only pool,
   the other 3 from the general pool — every round a distinct (team, year)
   pair. Also verifies the two Pitcher Rounds can actually supply 2
   DIFFERENT real people (the same person could in theory be the only
   shared option in both, if they pitched in both dealt seasons) — cheap
   to check with only 2 small rosters, and retrying the whole deal on the
   rare miss is simpler than a mid-draft dead end. */
function b0Rounds(rng){
  const normalPool = b0RoundPool(), pitcherPool = b0PitcherPool();
  const pIdxs = b0PickPitcherRounds(rng);
  const openIdxs = [0,1,2,3,4].filter(i=>!pIdxs.includes(i));
  let rounds = null;
  for(let attempt=0; attempt<200 && !rounds; attempt++){
    const usedKeys = new Set();
    const trial = new Array(B0_ROSTER);
    let ok = true;
    for(const idx of pIdxs){
      let picked=null;
      for(let t=0; t<50 && !picked; t++){
        const cand = pitcherPool[Math.floor(rng()*pitcherPool.length)];
        const key = cand.team+'|'+cand.year;
        if(!usedKeys.has(key)){ picked=cand; usedKeys.add(key); }
      }
      if(!picked){ ok=false; break; }
      trial[idx] = picked;
    }
    if(ok && pIdxs.length===2){
      const [r1,r2] = pIdxs.map(i=>trial[i]);
      if(!r1.roster.some(p1=>r2.roster.some(p2=>p2.name!==p1.name))) ok=false;
    }
    if(ok) for(const idx of openIdxs){
      let picked=null;
      for(let t=0; t<200 && !picked; t++){
        const cand = normalPool[Math.floor(rng()*normalPool.length)];
        const key = cand.team+'|'+cand.year;
        if(!usedKeys.has(key)){ picked=cand; usedKeys.add(key); }
      }
      if(!picked){ ok=false; break; }
      trial[idx] = picked;
    }
    if(ok) rounds = trial;
  }
  if(!rounds) rounds = [0,1,2,3,4].map(i=>pIdxs.includes(i)?pitcherPool[0]:normalPool[0]);   // pathological fallback, never hit in practice
  return rounds.map((r,i)=>({...r, isPitcherRound: pIdxs.includes(i)}));
}
function newB0Deal(rng){ return {rounds: b0Rounds(rng), picks: [], pitchers: [], locked:false, result:null}; }
let b0Mode='daily', b0ShowStats=true, b0Daily=null, b0Practice=null;
/* storage key versioned (v7 = which 2 rounds are Pitcher Rounds is now
   itself random per deal, shifting the whole rng sequence a deal draws
   from) so a browser with an in-progress draft saved under the old, fixed
   4-and-5 shape is ignored, not misread against newly-regenerated rounds
   that no longer line up with it. */
function getDailyB0(){
  const key = gridDailyKey();
  if(!b0Daily || b0Daily.key!==key){
    const rng = mulberry32(gridSeedFromString('bwb-b0v7-'+key));
    b0Daily = {key, ...newB0Deal(rng)};
    try{
      const raw = localStorage.getItem('bwb-b0v7-'+key);
      if(raw){
        const saved = JSON.parse(raw);
        if(Array.isArray(saved.picks) && saved.picks.every(p=>p && p.line && p.regLine && typeof p.line==='object')){
          b0Daily.picks = saved.picks;
          b0Daily.pitchers = Array.isArray(saved.pitchers) ? saved.pitchers : [];
          b0Daily.locked = !!saved.locked;
        }
      }
    }catch(e){}
  }
  return b0Daily;
}
function saveDailyB0(){
  try{ localStorage.setItem('bwb-b0v7-'+b0Daily.key,
    JSON.stringify({picks: b0Daily.picks, pitchers: b0Daily.pitchers, locked: b0Daily.locked})); }catch(e){}
}
function newPracticeB0(){ return newB0Deal(Math.random); }
/* a player-season can hit, pitch, or both — show whichever lines are real
   for that specific year rather than assuming one or the other */
function b0LineSummary(line){
  const parts = [];
  if(line.AB>0) parts.push(`${rate(avg(line))}/${rate(obp(line))}/${rate(slg(line))} · ${line.HR} HR · ${line.RBI} RBI`);
  if(line.IPouts>0) parts.push(`${wl(line)}, ${two(era(line))} ERA · ${line.pK} K`);
  return parts.join(' — ');
}
function b0PlayerRow(pick, alreadyPicked){
  const isPitcher = pick.line.IPouts>0;
  const statsHTML = b0ShowStats ? `<span class="b0stats">${b0LineSummary(pick.line)}</span>` : '';
  const actionHTML = alreadyPicked
    ? '<span class="pmeta">Already on your team</span>'
    : `<button type="button" class="b0draft" data-name="${esc(pick.name)}">Draft</button>`;
  return `<li class="b0row">
    <button class="pname" data-p="${esc(pick.name)}">${esc(pick.name)}</button>
    ${isPitcher&&b0ShowStats?'<span class="gtag">P</span>':''}
    ${statsHTML}${actionHTML}</li>`;
}
/* the daily simulation's "luck" is seeded off the day alone (not the
   roster), so two people who draft the same day's rounds differently are
   compared on team-building, not on who got the friendlier random draw;
   practice mode has no such fairness need, so it just uses fresh
   randomness each run */
function b0SimRng(puzzle){
  return b0Mode==='daily' ? mulberry32(gridSeedFromString('bwb-b0v3-sim-'+puzzle.key)) : Math.random;
}
const B0_RESULT_EMOJI = {win:'🟩', loss:'🟥'};
function b0ShareText(puzzle){
  const r = puzzle.result;
  const strip = r.log.map(x=>B0_RESULT_EMOJI[x.win?'win':'loss']).join('');
  return `BWB 15-0 ${puzzle.key}\n${strip}\n${r.wins}-${r.losses}`;
}
function b0RosterHTML(puzzle){
  if(!puzzle.picks.length) return '<p class="empty">No picks yet — Round 1 is below.</p>';
  return `<ol class="b0roster">${puzzle.picks.map((p,i)=>`<li>
      <button class="pname" data-p="${esc(p.name)}">${esc(p.name)}</button>
      <span class="pmeta">${esc(TEAMS[p.team].nick||p.team)} · ${p.year}${puzzle.pitchers.includes(p.name)?' · <span class="gtag">P</span>':''}</span>
      ${!puzzle.locked && i===puzzle.picks.length-1 ? '<button type="button" class="b0remove" id="b0Undo">Undo</button>' : ''}
    </li>`).join('')}</ol>`;
}
function renderB0(){
  setNav('arcade');
  if(b0Mode==='practice' && !b0Practice) b0Practice = newPracticeB0();
  const puzzle = b0Mode==='daily' ? getDailyB0() : b0Practice;
  if(puzzle.locked && !puzzle.result) puzzle.result = b0Simulate(puzzle.picks, puzzle.pitchers, b0SimRng(puzzle));
  const draftDone = puzzle.picks.length===B0_ROSTER;
  const roundIdx = puzzle.picks.length;
  const round = puzzle.rounds[roundIdx];
  const pickedNames = new Set(puzzle.picks.map(p=>p.name));
  const lg = b0League();
  let bodyHTML;
  if(puzzle.locked && puzzle.result){
    const r = puzzle.result;
    const gameLogHTML = r.log.map(x=>
      `<li class="${x.win?'b0win':'b0loss'}">G${x.g} <b>${x.rs}-${x.ra}</b> ${x.win?'W':'L'}</li>`).join('');
    bodyHTML = `<div class="b0result" style="--tier:${statpadTier(null, r.wins===B0_GAMES).color}">
      <div class="b0record">${r.wins}-${r.losses}</div>
      <p class="pmeta">A simulated ${B0_GAMES}-game season, one game at a time, chasing a perfect ${B0_GAMES}-0 —
        this team's combined ${rate(r.teamOPS)} OPS (all 5) projects to about ${r.projRPG.toFixed(1)} runs a game
        scored, and its two Pitcher Round picks' combined ${two(r.teamERA)} ERA projects to about
        ${r.projRA.toFixed(1)} runs a game allowed, against a league that's averaged ${lg.rpg.toFixed(1)} runs a
        game in real games — an expected win rate of ${rate(r.winPct)}. Each game's score is a real BWB team-game
        run total pulled off the league's own board and scaled to this rate, not a textbook bell curve, so
        blowouts and shutouts show up as often as they actually have around here. Every rate here is also already
        regressed toward league average by how much each player actually played that season.</p>
      <ul class="b0gamelog">${gameLogHTML}</ul>
      ${b0Mode==='daily' ? shareResultButton('b0Share') : ''}
    </div>`;
  } else if(!draftDone && round){
    const yrs = TEAMS[round.team].years||[];
    const logo = teamLogoForYear(round.team, round.year<=yrs[yrs.length-1] ? round.year : yrs[yrs.length-1]);
    const poolHTML = round.roster.map(p=>b0PlayerRow(p, pickedNames.has(p.name))).join('');
    bodyHTML = `<div class="b0team">${logo?`<img class="b0logo" src="${logo}" alt="">`:''}
        <div><h3 class="hsub" style="margin:0">${esc(TEAMS[round.team].nick||round.team)} · ${round.year}
          ${round.isPitcherRound?'<span class="b0pround">Pitcher Round</span>':''}</h3>
        <span class="pmeta">Round ${roundIdx+1} of ${B0_ROSTER} · ${round.roster.length} on this roster
          ${round.isPitcherRound?'· everyone here pitched this season — whoever you draft joins your staff':''}</span></div>
      </div>
      <ul class="b0pool">${poolHTML}</ul>`;
  } else {
    bodyHTML = '';
  }
  const lockGateHTML = (draftDone && !puzzle.locked)
    ? '<p class="note"><button type="button" class="pname" id="b0Lock">Lock in this team →</button></p>' : '';
  app.innerHTML = `
    <div class="phead"><h2>Arcade</h2><span class="yrs">${b0Mode==='daily'?`Today's Draft · ${puzzle.key}`:'Practice Draft'}</span></div>
    ${arcadeTabBar('b0')}
    <p class="lead">Five rounds, one real BWB team-and-year dealt each round — draft exactly one player from that
      season's actual roster before moving to the next round (no player twice, even in a different year). Two of
      the five rounds — a random pair, different every deal — are <b>Pitcher Rounds</b>: the pool there is only
      players who actually pitched that season, and whoever you draft joins your pitching staff automatically —
      they still hit for you too. No budget, no cap — every player's a free pick; the ${B0_GAMES}-game simulation
      is where the real difficulty lives. Lock in once all 5 are drafted to chase a perfect ${B0_GAMES}-0.</p>
    <div class="segs" role="group" aria-label="15-0 mode">
      <button data-b0m="daily" aria-pressed="${b0Mode==='daily'}">Today's Draft</button>
      <button data-b0m="practice" aria-pressed="${b0Mode==='practice'}">Practice Draft</button>
    </div>
    ${b0Mode==='practice'?'<p class="note"><button class="pname" id="b0Shuffle">Deal a new practice draft →</button></p>':''}
    <div class="segs" role="group" aria-label="Stat visibility">
      <button data-b0v="show" aria-pressed="${b0ShowStats}">Draft — stats shown</button>
      <button data-b0v="hide" aria-pressed="${!b0ShowStats}">Blind — stats hidden</button>
    </div>
    <h3 class="hsub">Your Team (${puzzle.picks.length}/${B0_ROSTER}${puzzle.picks.length?`, ${puzzle.pitchers.length} P`:''})</h3>
    ${b0RosterHTML(puzzle)}
    ${lockGateHTML}
    ${bodyHTML}`;
  wireB0();
  if(puzzle.locked && puzzle.result && b0Mode==='daily') wireShareButton('b0Share', ()=>b0ShareText(puzzle));
}
function wireB0(){
  wireArcadeTabBar();
  app.querySelectorAll('[data-b0m]').forEach(b=>b.addEventListener('click',()=>{
    b0Mode = b.dataset.b0m;
    if(b0Mode==='practice' && !b0Practice) b0Practice = newPracticeB0();
    renderB0();
  }));
  const shuffleBtn = document.getElementById('b0Shuffle');
  if(shuffleBtn) shuffleBtn.addEventListener('click', ()=>{ b0Practice = newPracticeB0(); renderB0(); });
  app.querySelectorAll('[data-b0v]').forEach(b=>b.addEventListener('click',()=>{
    b0ShowStats = b.dataset.b0v==='show'; renderB0();
  }));
  app.querySelectorAll('.b0draft[data-name]').forEach(b=>b.addEventListener('click',()=>{
    const puzzle = b0Mode==='daily' ? b0Daily : b0Practice;
    if(puzzle.locked || puzzle.picks.length>=B0_ROSTER) return;
    if(puzzle.picks.some(p=>p.name===b.dataset.name)) return;   // no player twice, even a different year
    const round = puzzle.rounds[puzzle.picks.length];
    const pick = round.roster.find(p=>p.name===b.dataset.name);
    if(!pick) return;
    puzzle.picks.push({name:pick.name, team:round.team, year:round.year, line:pick.line, regLine:pick.regLine});
    if(round.isPitcherRound) puzzle.pitchers.push(pick.name);
    if(b0Mode==='daily') saveDailyB0();
    renderB0();
  }));
  const undoBtn = document.getElementById('b0Undo');
  if(undoBtn) undoBtn.addEventListener('click', ()=>{
    const puzzle = b0Mode==='daily' ? b0Daily : b0Practice;
    if(puzzle.locked) return;
    const last = puzzle.picks.pop();
    if(last) puzzle.pitchers = puzzle.pitchers.filter(n=>n!==last.name);
    if(b0Mode==='daily') saveDailyB0();
    renderB0();
  });
  const lockBtn = document.getElementById('b0Lock');
  if(lockBtn) lockBtn.addEventListener('click', ()=>{
    const puzzle = b0Mode==='daily' ? b0Daily : b0Practice;
    puzzle.locked = true;
    puzzle.result = b0Simulate(puzzle.picks, puzzle.pitchers, b0SimRng(puzzle));
    if(b0Mode==='daily') saveDailyB0();
    renderB0();
  });
  app.querySelectorAll('.pname[data-p]').forEach(b=>b.addEventListener('click',()=>{
    location.hash='#/p/'+encodeURIComponent(b.dataset.p);
  }));
}

function dispatch(h){
  let m;
  if(h === '#/standings') return renderStandings();
  if((m = h.match(/^#\/div\/(.+)$/))) return renderDivision(decodeURIComponent(m[1]));
  if((m = h.match(/^#\/series\/(\d+)\/(\w+)$/))) return renderSeries(+m[1], m[2]);
  if(h === '#/leaders') return renderLeaders();
  if(h === '#/records') return renderRecords();
  if(h === '#/champs') return renderChampsPage();
  if(h === '#/awards') return renderAwards();
  if(h === '#/beavers') return renderBeavers();
  if((m = h.match(/^#\/beavers\/t\/(.+)$/))) return renderBeaverTournament(decodeURIComponent(m[1]));
  if((m = h.match(/^#\/beavers\/(.+)$/))){
    const gid = decodeURIComponent(m[1]);
    const t = bvTournamentForGame(gid);
    return t ? renderBeaverTournament(t.meta.date, gid) : renderBeavers();
  }
  if((m = h.match(/^#\/g\/(\d+)$/))) return boxScore(m[1]);
  if(h === '#/games') return renderGames();
  if((m = h.match(/^#\/t\/(.+)$/))) return teamDetail(decodeURIComponent(m[1]));
  if(h === '#/teams') return renderTeams();
  if((m = h.match(/^#\/p\/(.+)$/))) return detail(decodeURIComponent(m[1]));
  if(h === '#/players') return renderDir();
  if(h === '#/compare') return renderCompare(null, null);
  if((m = h.match(/^#\/compare\/([^/]+)\/([^/]+)$/)))
    return renderCompare(decodeURIComponent(m[1]), decodeURIComponent(m[2]));
  if(h === '#/arcade') return renderGrid();
  if(h === '#/grid') return renderGrid();
  if(h === '#/statpad') return renderStatpad();
  if(h === '#/15-0') return renderB0();
  if(h === '#/office') return renderOffice();
  return renderHome();
}
function route(){
  const raw = location.hash || '';
  const h = raw.replace(/#h-[\w-]+$/,'');   // ignore in-page anchor
  ['--tc','--tp','--ts'].forEach(v=>app.style.removeProperty(v));  // clear franchise tint
  dispatch(h);
  document.querySelectorAll('table.sortable').forEach(makeSortable);
  // scroll-to-top belongs to real navigation only (this fires on hashchange); in-page
  // toggles (tabs, year chips, phase switches) call their render function directly
  // without touching the hash, so they never reach here and the page stays put
  if(h === raw) scrollTo(0,0);
}
addEventListener('hashchange', route);
(function(){ const rc = CHAMPS[0] && FRANCHISE_COLORS[CHAMPS[0].tm]; const el = document.querySelector('.perf i');
  if(rc && el){ el.style.setProperty('--pa', rc.p); el.style.setProperty('--pb', rc.s); } })();
buildTicker();
route();
</script>
'''

open('index.html','w').write(HTML.replace('__DATA__', data))
print('wrote index.html')
