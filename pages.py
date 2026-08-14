# pages.py

LOGO_B64 = ""

LOGIN_HTML = r"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ورود · توسط Kourosh</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@100;200;300;400;500;600;700;800;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.19.0/dist/tabler-icons.min.css">
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:'Vazirmatn',sans-serif !important}
:root{--bg:#060a14;--card:rgba(12,19,38,0.92);--accent:#10b981;--accent2:#059669;--text:#E8F4FF;--dim:#48577A;--mid:#8AA0C4;--border:rgba(16,185,129,0.2)}
html,body{height:100%;overflow:hidden;background:var(--bg);color:var(--text);font-family:'Vazirmatn',sans-serif !important}
body{display:flex;align-items:center;justify-content:center;padding:20px}
.bg{position:fixed;inset:0;background:radial-gradient(ellipse 80% 60% at 50% 0%,rgba(16,185,129,0.12),transparent 70%),var(--bg);z-index:0}
.grid{position:fixed;inset:0;background-image:linear-gradient(rgba(16,185,129,0.03) 1px,transparent 1px),linear-gradient(90deg,rgba(16,185,129,0.03) 1px,transparent 1px);background-size:44px 44px;z-index:0}
.orb{position:fixed;border-radius:50%;filter:blur(90px);z-index:0;animation:fl 9s ease-in-out infinite}
.o1{width:380px;height:380px;background:rgba(16,185,129,0.08);top:-100px;right:-80px}
.o2{width:280px;height:280px;background:rgba(5,150,105,0.05);bottom:-60px;left:-60px;animation-delay:4s}
@keyframes fl{0%,100%{transform:translateY(0)}50%{transform:translateY(-18px)}}
.wrap{position:relative;z-index:10;width:100%;max-width:400px}
.card{background:var(--card);border:1px solid var(--border);border-radius:20px;padding:38px 34px 34px;backdrop-filter:blur(24px);box-shadow:0 0 80px rgba(16,185,129,0.08),0 20px 60px rgba(0,0,0,.6)}
.brand{display:flex;align-items:center;gap:14px;margin-bottom:28px}
.brand-img{width:48px;height:48px;border-radius:50%;overflow:hidden;border:1px solid var(--border);box-shadow:0 0 20px rgba(16,185,129,0.35);flex-shrink:0}
.brand-img img{width:100%;height:100%;object-fit:cover}
.brand-name{font-size:16px;font-weight:800;color:var(--text)}
.brand-name a{color:inherit;text-decoration:none}
.brand-sub{font-size:11px;color:var(--dim);margin-top:2px}
h1{font-size:21px;font-weight:800;color:var(--text);margin-bottom:5px;letter-spacing:-.02em}
.sub{font-size:12px;color:var(--mid);margin-bottom:24px;line-height:1.6}
.hint{display:flex;align-items:center;gap:10px;background:rgba(16,185,129,0.07);border:1px solid rgba(16,185,129,0.18);border-radius:10px;padding:10px 14px;margin-bottom:20px}
.hint-label{font-size:11px;color:var(--mid);flex:1}
.hint-val{font-family:ui-monospace,monospace;font-size:13px;font-weight:700;color:var(--accent);background:rgba(16,185,129,0.12);border:1px solid rgba(16,185,129,0.3);padding:4px 11px;border-radius:7px;cursor:pointer;transition:.15s;letter-spacing:.08em}
.hint-val:hover{background:rgba(16,185,129,0.24)}
.field{margin-bottom:18px}
.field label{display:block;font-size:10.5px;font-weight:700;color:var(--mid);margin-bottom:7px;text-transform:uppercase;letter-spacing:.06em}
.inp-wrap{position:relative}
input[type=password]{width:100%;padding:13px 44px 13px 16px;border-radius:11px;border:1px solid var(--border);background:rgba(0,0,0,.35);color:var(--text);font-size:14px;outline:none;transition:.2s}
input[type=password]:focus{border-color:var(--accent);background:rgba(0,0,0,.45);box-shadow:0 0 0 3px rgba(16,185,129,0.15)}
.ic{position:absolute;left:14px;top:50%;transform:translateY(-50%);color:var(--dim);font-size:18px;pointer-events:none;transition:.2s}
input:focus+.ic{color:var(--accent)}
.err{display:none;background:rgba(239,68,68,.1);border:1px solid rgba(239,68,68,.3);border-radius:10px;padding:10px 14px;margin-bottom:14px;font-size:12px;color:#FB8585;align-items:center;gap:8px}
.err.show{display:flex}
.btn{width:100%;padding:13px;border-radius:11px;border:none;cursor:pointer;background:linear-gradient(135deg,#10b981,#059669);color:#fff;font-size:14px;font-weight:800;display:flex;align-items:center;justify-content:center;gap:8px;box-shadow:0 4px 20px rgba(16,185,129,.35);transition:.2s;position:relative;overflow:hidden}
.btn:hover{background:linear-gradient(135deg,#059669,#047857)}
.btn:disabled{opacity:.5;cursor:not-allowed}
.footer{margin-top:22px;padding-top:18px;border-top:1px solid var(--border);display:flex;align-items:center;justify-content:center;gap:8px;font-size:11px;color:var(--dim)}
.footer a{color:var(--accent);font-weight:700;text-decoration:none;display:flex;align-items:center;gap:4px}
@keyframes spin{to{transform:rotate(360deg)}}
</style>
</head>
<body>
<div class="bg"></div><div class="grid"></div>
<div class="orb o1"></div><div class="orb o2"></div>
<div class="wrap">
  <div class="card">
    <div class="brand">
      <div class="brand-img"></div>
      <div><div class="brand-name"><a href="https://t.me/kouroxlog" target="_blank">توسط Kourosh</a></div><div class="brand-sub">v9.8</div></div>
    </div>
    <h1>ورود به پنل مدیریت</h1>
    <p class="sub">رمز عبور را برای دسترسی به داشبورد وارد کنید</p>
    <div class="err" id="err"><i class="ti ti-alert-circle"></i><span id="err-text"></span></div>
    <div class="hint">
      <span class="hint-label">رمز پیش‌فرض سیستم</span>
      <span class="hint-val" onclick="document.getElementById('pw').value='KouroshKING';document.getElementById('pw').focus()">KouroshKING</span>
    </div>
    <form id="form">
      <div class="field">
        <label>رمز عبور</label>
        <div class="inp-wrap">
          <input type="password" id="pw" placeholder="رمز عبور را وارد کنید" autofocus required>
          <i class="ti ti-lock ic"></i>
        </div>
      </div>
      <button class="btn" type="submit" id="btn"><i class="ti ti-login-2"></i> ورود به داشبورد</button>
    </form>
    <div class="footer">پشتیبانی <a href="https://t.me/kouroxlog" target="_blank"><i class="ti ti-brand-telegram"></i>@kouroxlog</a></div>
  </div>
</div>
<script>
document.getElementById('form').addEventListener('submit',async e=>{
  e.preventDefault();
  const btn=document.getElementById('btn'),err=document.getElementById('err'),et=document.getElementById('err-text');
  err.classList.remove('show');btn.disabled=true;
  btn.innerHTML='<i class="ti ti-loader-2" style="animation:spin 1s linear infinite"></i> در حال ورود...';
  try{
    const r=await fetch('/api/login',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({password:document.getElementById('pw').value})});
    if(!r.ok){const d=await r.json().catch(()=>({}));throw new Error(d.detail||'خطا در ورود');}
    location.href='/dashboard';
  }catch(e){
    et.textContent=e.message;err.classList.add('show');
    btn.disabled=false;btn.innerHTML='<i class="ti ti-login-2"></i> ورود به داشبورد';
  }
});
</script>
</body></html>"""


DASHBOARD_HTML = r"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>توسط Kourosh - مدیریت VLESS</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@100;200;300;400;500;600;700;800;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.19.0/dist/tabler-icons.min.css">
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
*{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent;font-family:'Vazirmatn',sans-serif !important}
:root{
  --bg:#060a14;--bg2:#0a1020;--bg3:#0d1428;
  --card:#0c1326;--card-b:rgba(16,185,129,0.14);--card-bh:rgba(16,185,129,0.3);
  --accent:#10b981;--accent2:#059669;--accent-d:rgba(16,185,129,0.1);
  --green:#10b981;--green-bg:rgba(16,185,129,0.12);--green-t:#34d399;
  --red:#EF4444;--red-bg:rgba(239,68,68,0.12);--red-t:#FB8585;
  --amber:#F2A33D;--amber-bg:rgba(242,163,61,0.12);--amber-t:#F9C988;
  --purple:#9D7BF0;--purple-bg:rgba(157,123,240,0.12);--purple-t:#BCA4F7;
  --t1:#EFF4FF;--t2:#8AA0C4;--t3:#48577A;
  --sidebar-w:248px;--radius:16px;--shadow:0 12px 40px rgba(0,0,0,0.5);
}
html,body{min-height:100%;background:var(--bg);color:var(--t1);font-size:13.5px}
body{display:flex;overflow-x:hidden}
.sidebar{width:var(--sidebar-w);min-height:100vh;background:var(--bg2);border-left:1px solid var(--card-b);display:flex;flex-direction:column;flex-shrink:0;position:fixed;right:0;top:0;bottom:0;z-index:200;transition:transform .25s cubic-bezier(.4,0,.2,1)}
.logo{display:flex;align-items:center;gap:12px;padding:20px 16px 16px;border-bottom:1px solid var(--card-b)}
.logo-img{width:38px;height:38px;border-radius:50%;overflow:hidden;border:1px solid var(--card-b);box-shadow:0 0 14px rgba(16,185,129,.35);flex-shrink:0}
.logo-img img{width:100%;height:100%;object-fit:cover}
.logo-name{font-size:14px;font-weight:800;color:var(--t1)}
.logo-name a{color:inherit;text-decoration:none}
.logo-sub{font-size:9.5px;color:var(--accent);font-weight:600}
.nav-wrap{flex:1;padding:12px 8px;overflow-y:auto}
.nav-sec{font-size:9px;font-weight:700;color:var(--t3);text-transform:uppercase;letter-spacing:.12em;padding:12px 10px 4px}
.nav-it{display:flex;align-items:center;gap:10px;padding:10px 12px;border-radius:11px;color:var(--t2);cursor:pointer;font-size:12.5px;font-weight:600;transition:.15s;margin-bottom:2px}
.nav-it:hover{background:var(--accent-d);color:var(--accent)}
.nav-it.on{background:var(--accent-d);color:var(--accent);border:1px solid var(--card-b)}
.nav-it i{font-size:17px}
.nav-badge{margin-right:auto;background:var(--accent-d);color:var(--accent);font-size:10px;font-weight:700;padding:2px 7px;border-radius:10px}
.sb-foot{padding:12px 14px;border-top:1px solid var(--card-b)}
.logout-btn{display:flex;align-items:center;justify-content:center;gap:7px;background:var(--red-bg);color:var(--red-t);border-radius:9px;padding:9px;font-size:12px;font-weight:700;border:1px solid rgba(239,68,68,.2);cursor:pointer;width:100%;transition:.15s}
.logout-btn:hover{background:rgba(239,68,68,.25)}
.main{margin-right:var(--sidebar-w);flex:1;padding:28px 28px 60px;min-width:0}
.mob-top{display:none;position:fixed;top:0;right:0;left:0;height:52px;background:var(--bg2);border-bottom:1px solid var(--card-b);z-index:150;align-items:center;justify-content:space-between;padding:0 14px}
.mob-logo{display:flex;align-items:center;gap:8px;font-weight:800;font-size:14px}
.menu-btn{background:var(--card);border:1px solid var(--card-b);color:var(--t1);width:36px;height:36px;border-radius:9px;display:flex;align-items:center;justify-content:center;cursor:pointer;font-size:18px}
.topbar{display:flex;align-items:flex-start;justify-content:space-between;margin-bottom:22px;flex-wrap:wrap;gap:12px}
.tb-title{font-size:20px;font-weight:800;color:var(--t1);display:flex;align-items:center;gap:8px}
.tb-sub{font-size:11px;color:var(--t3);margin-top:3px}
.tb-right{display:flex;align-items:center;gap:8px}
.badge{font-size:10px;font-weight:700;padding:5px 11px;border-radius:20px;display:inline-flex;align-items:center;gap:6px}
.bg-green{background:var(--green-bg);color:var(--green-t)}
.bg-blue{background:var(--accent-d);color:var(--accent)}
.dot{width:6px;height:6px;border-radius:50%;display:inline-block}
.dg{background:var(--green)}
.pulse{animation:pulse 2s infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.25}}
.metrics{display:grid;grid-template-columns:repeat(4,1fr);gap:13px;margin-bottom:18px}
.metric{background:var(--card);border:1px solid var(--card-b);border-radius:18px;padding:18px 20px;box-shadow:var(--shadow);transition:.2s}
.metric:hover{border-color:var(--card-bh);transform:translateY(-1px)}
.m-icon{width:36px;height:36px;border-radius:10px;background:var(--accent-d);display:flex;align-items:center;justify-content:center;margin-bottom:11px;color:var(--accent);font-size:18px}
.m-label{font-size:10px;color:var(--t3);margin-bottom:4px;font-weight:700;text-transform:uppercase;letter-spacing:.05em}
.m-val{font-size:22px;font-weight:800;color:var(--t1);line-height:1}
.m-sub{font-size:10px;color:var(--t3);margin-top:6px;display:flex;align-items:center;gap:4px}
.card{background:var(--card);border:1px solid var(--card-b);border-radius:18px;padding:20px;box-shadow:var(--shadow);margin-bottom:16px}
.card-title{font-size:13px;font-weight:800;color:var(--t1);margin-bottom:15px;display:flex;align-items:center;gap:7px}
.g2{display:grid;grid-template-columns:1fr 1fr;gap:13px;margin-bottom:16px}
.g3{display:grid;grid-template-columns:2fr 1fr;gap:13px;margin-bottom:16px}
.sr{display:flex;align-items:center;justify-content:space-between;padding:10px 0;border-bottom:1px solid rgba(16,185,129,0.06);font-size:12px}
.sr:last-child{border-bottom:none}
.sr-k{color:var(--t2);display:flex;align-items:center;gap:6px}
.sr-v{font-weight:700;color:var(--t1)}
.pg{display:none}
.pg.on{display:block}
.btn{font-size:12px;font-weight:700;border-radius:10px;padding:8px 16px;cursor:pointer;display:inline-flex;align-items:center;gap:6px;border:none;transition:all .15s;white-space:nowrap}
.btn-p{background:linear-gradient(135deg,#10b981,#059669);color:#fff;box-shadow:0 3px 14px rgba(16,185,129,.3)}
.btn-p:hover{background:linear-gradient(135deg,#059669,#047857)}
.btn-g{background:var(--accent-d);color:var(--accent);border:1px solid var(--card-b)}
.btn-g:hover{background:rgba(16,185,129,.2)}
.btn-d{background:var(--red-bg);color:var(--red-t);border:1px solid rgba(239,68,68,.2)}
.btn-d:hover{background:rgba(239,68,68,.25)}
.btn-amber{background:var(--amber-bg);color:var(--amber-t);border:1px solid rgba(242,163,61,.2)}
.btn-sm{padding:5px 11px;font-size:11px;border-radius:8px}
.inp{background:rgba(0,0,0,.3);border:1px solid var(--card-b);color:var(--t1);border-radius:10px;padding:9px 13px;font-size:12.5px;outline:none;width:100%;transition:.18s}
.inp:focus{border-color:var(--accent);box-shadow:0 0 0 3px var(--accent-d)}
select.inp{appearance:none;cursor:pointer}
.form-g{margin-bottom:14px}
.form-g label{display:block;font-size:10.5px;font-weight:700;color:var(--t2);margin-bottom:6px;text-transform:uppercase;letter-spacing:.05em}
.form-row{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.modal{display:none;position:fixed;inset:0;background:rgba(0,0,0,.75);z-index:500;align-items:center;justify-content:center;backdrop-filter:blur(6px);padding:20px}
.modal.open{display:flex}
.modal-box{background:var(--card);border:1px solid var(--card-b);border-radius:22px;padding:26px;width:100%;max-width:540px;box-shadow:var(--shadow);max-height:90vh;overflow-y:auto}
.modal-head{display:flex;align-items:center;justify-content:space-between;margin-bottom:20px;padding-bottom:14px;border-bottom:1px solid var(--card-b)}
.modal-title{font-size:15px;font-weight:800;color:var(--t1);display:flex;align-items:center;gap:7px}
.close-btn{background:none;border:none;color:var(--t3);cursor:pointer;font-size:20px}
.close-btn:hover{color:var(--red-t)}
.toast{position:fixed;bottom:22px;left:50%;transform:translateX(-50%) translateY(40px);background:var(--card);border:1px solid var(--card-b);color:var(--t1);border-radius:12px;padding:10px 20px;font-size:12.5px;font-weight:700;opacity:0;transition:all .25s;z-index:999;pointer-events:none}
.toast.show{opacity:1;transform:translateX(-50%) translateY(0)}
.toast.ok{border-color:rgba(16,185,129,.4);background:var(--green-bg);color:var(--green-t)}
.toast.err{border-color:rgba(239,68,68,.4);background:var(--red-bg);color:var(--red-t)}
.ch{position:relative;height:210px}
.tbl{width:100%;border-collapse:collapse;font-size:12px}
.tbl th{text-align:right;padding:10px 12px;color:var(--t3);font-size:10px;font-weight:700;text-transform:uppercase;border-bottom:1px solid var(--card-b)}
.tbl td{padding:12px;border-bottom:1px solid rgba(16,185,129,0.05);color:var(--t1)}
.tbl tr:hover td{background:var(--accent-d)}
.sub-card{background:var(--card);border:1px solid var(--card-b);border-radius:18px;padding:18px 20px;margin-bottom:14px;position:relative;overflow:hidden;transition:.2s}
.sub-card:hover{border-color:var(--card-bh);box-shadow:var(--shadow)}
.sub-head{display:flex;align-items:flex-start;justify-content:space-between;gap:10px;margin-bottom:12px;flex-wrap:wrap}
.sub-label{font-size:15px;font-weight:800;color:var(--t1)}
.sub-links-box{background:rgba(0,0,0,.25);border:1px solid var(--card-b);border-radius:12px;padding:10px 12px;margin-top:10px;font-family:ui-monospace,monospace;font-size:10.5px;color:var(--accent);word-break:break-all}
.ubar{height:6px;border-radius:4px;background:rgba(16,185,129,0.1);overflow:hidden;margin-bottom:5px}
.ubar-f{height:100%;border-radius:4px;transition:width .5s ease}
.utxt{font-size:10.5px;color:var(--t3);display:flex;justify-content:space-between}
.cfg-checklist{max-height:160px;overflow-y:auto;border:1px solid var(--card-b);border-radius:10px;padding:8px 12px;background:rgba(0,0,0,.2)}
.cfg-chk-item{display:flex;align-items:center;gap:8px;padding:5px 0;font-size:12px;color:var(--t1);cursor:pointer}
.overlay{display:none;position:fixed;inset:0;background:rgba(0,0,0,.5);z-index:180}
.overlay.open{display:block}
@media(max-width:900px){
  .metrics{grid-template-columns:1fr 1fr}
  .g2,.g3{grid-template-columns:1fr}
  .main{margin-right:0;padding:68px 16px 40px}
  .sidebar{transform:translateX(100%)}
  .sidebar.open{transform:translateX(0)}
  .mob-top{display:flex}
}
</style>
</head>
<body>
<div class="mob-top">
  <div class="mob-logo"><i class="ti ti-shield-check" style="color:var(--accent)"></i> <a href="https://t.me/kouroxlog" target="_blank" style="color:inherit;text-decoration:none;">توسط Kourosh</a></div>
  <button class="menu-btn" id="open-sb"><i class="ti ti-menu-2"></i></button>
</div>
<div class="overlay" id="overlay"></div>
<aside class="sidebar" id="sb">
  <button class="menu-btn" id="close-sb" style="position:absolute;left:10px;top:14px"><i class="ti ti-x"></i></button>
  <div class="logo">
    <div class="logo-img"></div>
    <div><div class="logo-name"><a href="https://t.me/kouroxlog" target="_blank">توسط Kourosh</a></div><div class="logo-sub">v9.8 · gRPC / WS / XHTTP</div></div>
  </div>
  <div class="nav-wrap">
    <div class="nav-sec">پنل</div>
    <div class="nav-it on" data-pg="overview"><i class="ti ti-layout-dashboard"></i> داشبورد</div>
    <div class="nav-it" data-pg="subs"><i class="ti ti-users-group"></i> اشتراک‌ها <span class="nav-badge" id="subs-nb">0</span></div>
    <div class="nav-it" data-pg="links"><i class="ti ti-link"></i> کانفیگ‌ها <span class="nav-badge" id="links-nb">0</span></div>
    <div class="nav-it" data-pg="connections"><i class="ti ti-plug-connected"></i> اتصالات <span class="nav-badge" id="conns-nb">0</span></div>
    <div class="nav-sec">سیستم</div>
    <div class="nav-it" data-pg="settings"><i class="ti ti-brand-cloudflare"></i> تنظیمات وورکر</div>
    <div class="nav-it" data-pg="logs"><i class="ti ti-history"></i> لاگ فعالیت‌ها</div>
    <div class="nav-it" data-pg="errors"><i class="ti ti-alert-triangle"></i> خطاها</div>
  </div>
  <div class="sb-foot">
    <button class="logout-btn" id="logout-btn"><i class="ti ti-logout"></i> خروج از پنل</button>
  </div>
</aside>

<main class="main">

<!-- PAGE 1: OVERVIEW -->
<section class="pg on" id="pg-overview">
  <div class="topbar">
    <div><div class="tb-title"><i class="ti ti-layout-dashboard"></i> داشبورد اصلی</div><div class="tb-sub" id="last-upd">در حال بارگذاری...</div></div>
    <div class="tb-right">
      <span class="badge bg-green"><span class="dot dg pulse"></span> سرویس فعال</span>
      <span class="badge bg-blue" id="uptime-badge">—</span>
      <button class="btn btn-g btn-sm" onclick="fetchStats()"><i class="ti ti-refresh"></i> رفرش</button>
    </div>
  </div>
  <div class="metrics">
    <div class="metric"><div class="m-icon"><i class="ti ti-plug-connected"></i></div><div class="m-label">اتصالات زنده</div><div class="m-val" id="m-conns">—</div><div class="m-sub"><span class="dot dg pulse"></span> آنلاین</div></div>
    <div class="metric"><div class="m-icon"><i class="ti ti-transfer"></i></div><div class="m-label">کل ترافیک</div><div class="m-val" id="m-traffic">—</div><div class="m-sub">از زمان راه‌اندازی</div></div>
    <div class="metric"><div class="m-icon"><i class="ti ti-users-group"></i></div><div class="m-label">اشتراک‌های فعال</div><div class="m-val" id="m-subs">—</div><div class="m-sub" id="m-ssub">از کل</div></div>
    <div class="metric"><div class="m-icon"><i class="ti ti-link"></i></div><div class="m-label">کانفیگ‌های فعال</div><div class="m-val" id="m-alinks">—</div><div class="m-sub" id="m-lsub">از کل</div></div>
  </div>
  <div class="g3">
    <div class="card"><div class="card-title"><i class="ti ti-chart-area"></i> مصرف ساعتی ترافیک (MB)</div><div class="ch"><canvas id="ch1"></canvas></div></div>
    <div class="card">
      <div class="card-title"><i class="ti ti-activity"></i> وضعیت پروتکل‌ها</div>
      <div class="sr"><span class="sr-k"><i class="ti ti-route"></i> VLESS gRPC</span><span class="sr-v" style="color:var(--green-t)">● فعال</span></div>
      <div class="sr"><span class="sr-k"><i class="ti ti-wifi"></i> VLESS WebSocket</span><span class="sr-v" style="color:var(--green-t)">● فعال</span></div>
      <div class="sr"><span class="sr-k"><i class="ti ti-bolt"></i> XHTTP Ultra (Auto)</span><span class="sr-v" style="color:var(--green-t)">● فعال</span></div>
      <div class="sr"><span class="sr-k"><i class="ti ti-clock"></i> آپتایم</span><span class="sr-v" id="uptime-inline">—</span></div>
    </div>
  </div>
</section>

<!-- PAGE 2: SUBSCRIPTIONS -->
<section class="pg" id="pg-subs">
  <div class="topbar">
    <div><div class="tb-title"><i class="ti ti-users-group"></i> مدیریت اشتراک‌ها</div><div class="tb-sub">مدیریت والد برای کانفیگ‌ها، سهمیه حجم، زمان و محدودیت آی‌پی</div></div>
    <div class="tb-right">
      <button class="btn btn-p" onclick="openSubModal()"><i class="ti ti-plus"></i> اشتراک جدید</button>
      <button class="btn btn-g" onclick="loadSubs()"><i class="ti ti-refresh"></i></button>
    </div>
  </div>
  <div id="subs-list">
    <div style="text-align:center;padding:40px;color:var(--t3)"><i class="ti ti-loader-2" style="animation:spin 1s linear infinite;font-size:24px"></i><br>در حال بارگذاری اشتراک‌ها...</div>
  </div>
</section>

<!-- PAGE 3: LINKS -->
<section class="pg" id="pg-links">
  <div class="topbar">
    <div><div class="tb-title"><i class="ti ti-link"></i> مدیریت کانفیگ‌ها</div><div class="tb-sub">ساخت و مدیریت کانفیگ‌های VLESS (gRPC / WS / XHTTP)</div></div>
    <div class="tb-right">
      <button class="btn btn-p" onclick="openLinkModal()"><i class="ti ti-plus"></i> کانفیگ جدید</button>
      <button class="btn btn-g" onclick="loadLinks()"><i class="ti ti-refresh"></i></button>
    </div>
  </div>
  <div id="links-list">
    <div style="text-align:center;padding:40px;color:var(--t3)"><i class="ti ti-loader-2" style="animation:spin 1s linear infinite;font-size:24px"></i><br>در حال بارگذاری کانفیگ‌ها...</div>
  </div>
</section>

<!-- PAGE 4: CONNECTIONS -->
<section class="pg" id="pg-connections">
  <div class="topbar">
    <div><div class="tb-title"><i class="ti ti-plug-connected"></i> اتصالات زنده</div><div class="tb-sub">لیست اتصالات فعال کلاینت‌ها</div></div>
    <div class="tb-right"><button class="btn btn-g" onclick="loadConns()"><i class="ti ti-refresh"></i> رفرش</button></div>
  </div>
  <div class="card"><div id="conns-table">در حال بارگذاری...</div></div>
</section>

<!-- PAGE: SETTINGS (CLOUDFLARE WORKER) -->
<section class="pg" id="pg-settings">
  <div class="topbar">
    <div><div class="tb-title"><i class="ti ti-brand-cloudflare"></i> تنظیمات Cloudflare Worker (DPI Bypass)</div><div class="tb-sub">عبور از اختلال اینترنت ایرانسل و رایتل با پروکسی معکوس کلادفلر</div></div>
    <div class="tb-right"><button class="btn btn-g" onclick="loadSettings()"><i class="ti ti-refresh"></i> رفرش</button></div>
  </div>

  <div class="card" style="margin-bottom:16px">
    <div class="card-title"><i class="ti ti-settings"></i> تنظیمات دامنه وورکر و آی‌پی تمیز</div>
    <form id="form-settings">
      <div class="form-g">
        <label>دامنه وورکر کلادفلر (WORKER_DOMAIN)</label>
        <input class="inp" id="st-worker-domain" placeholder="مثلاً: worker.mydomain.com یا x4g-proxy.sub.workers.dev">
        <div style="font-size:10.5px;color:var(--t3);margin-top:4px">دامنه اختصاصی یا زیردامنه وورکر کلادفلر که کلاینت‌ها به آن متصل می‌شوند.</div>
      </div>
      <div class="form-g">
        <label>آی‌پی تمیز کلادفلر (CLEAN_IP - اختیاری)</label>
        <input class="inp" id="st-clean-ip" placeholder="مثلاً: 104.21.x.x (در صورت خالی بودن، از خود دامنه وورکر استفاده می‌شود)">
        <div style="font-size:10.5px;color:var(--t3);margin-top:4px">آی‌پی تمیز کلادفلر جهت درج در فیلد address لینک‌های VLESS کلاینت.</div>
      </div>
      <button class="btn btn-p" type="submit" style="margin-top:10px"><i class="ti ti-check"></i> ذخیره تنظیمات وورکر</button>
    </form>
  </div>

  <div class="card">
    <div class="card-title" style="display:flex;justify-content:space-between;align-items:center">
      <span><i class="ti ti-code"></i> اسکریپت Cloudflare Worker (Reverse Proxy)</span>
      <button class="btn btn-sm btn-g" onclick="copyWorkerScript()"><i class="ti ti-copy"></i> کپی کد Worker</button>
    </div>
    <div style="font-size:11px;color:var(--t2);margin-bottom:10px">
      این کد را کپی کرده و در پنل کلادفلر (بخش Workers & Pages -> Create Worker) قرار داده و Deploy کنید.
    </div>
    <textarea id="worker-code-box" readonly style="width:100%;height:220px;background:rgba(0,0,0,0.4);border:1px solid var(--card-b);color:var(--accent);font-family:ui-monospace,monospace;font-size:11px;padding:12px;border-radius:10px;outline:none;resize:vertical"></textarea>
  </div>
</section>

<!-- PAGE 5: LOGS -->
<section class="pg" id="pg-logs">
  <div class="topbar">
    <div><div class="tb-title"><i class="ti ti-history"></i> لاگ فعالیت‌ها</div><div class="tb-sub">تاریخچه رخدادهای سیستم و پنل</div></div>
    <div class="tb-right"><button class="btn btn-g" onclick="loadActivity()"><i class="ti ti-refresh"></i> رفرش</button></div>
  </div>
  <div class="card"><div id="logs-list">در حال دریافت لاگ‌ها...</div></div>
</section>

<!-- PAGE 6: ERRORS -->
<section class="pg" id="pg-errors">
  <div class="topbar">
    <div><div class="tb-title"><i class="ti ti-alert-triangle"></i> خطاها</div><div class="tb-sub">آخرین خطاهای شبکه و اتصالات</div></div>
    <div class="tb-right"><button class="btn btn-g" onclick="fetchStats()"><i class="ti ti-refresh"></i> رفرش</button></div>
  </div>
  <div class="card"><div id="errs-full">هیچ خطایی ثبت نشده است.</div></div>
</section>

</main>

<!-- MODAL: SUBSCRIPTION -->
<div class="modal" id="modal-sub">
  <div class="modal-box">
    <div class="modal-head">
      <div class="modal-title" id="sub-modal-title"><i class="ti ti-users-group"></i> ساخت اشتراک جدید</div>
      <button class="close-btn" onclick="closeModal('modal-sub')"><i class="ti ti-x"></i></button>
    </div>
    <form id="form-sub">
      <div class="form-g"><label>عنوان اشتراک</label><input class="inp" id="sub-label" placeholder="مثلاً: اشتراک VIP کاربر ۱" required></div>
      <div class="form-row">
        <div class="form-g"><label>حجم کل (0 = نامحدود)</label><input class="inp" type="number" step="0.1" id="sub-limit-val" value="0"></div>
        <div class="form-g"><label>واحد حجم</label><select class="inp" id="sub-limit-unit"><option value="GB">گیگابایت (GB)</option><option value="MB">مگابایت (MB)</option></select></div>
      </div>
      <div class="form-row">
        <div class="form-g"><label>اعتبار (روز - 0 = نامحدود)</label><input class="inp" type="number" id="sub-exp" value="0"></div>
        <div class="form-g"><label>محدودیت آی‌پی همزمان (0 = نامحدود)</label><input class="inp" type="number" id="sub-iplimit" value="0"></div>
      </div>
      <div class="form-row">
        <div class="form-g"><label>محدودیت سرعت (0 = نامحدود)</label><input class="inp" type="number" step="0.1" id="sub-speed-val" value="0"></div>
        <div class="form-g"><label>واحد سرعت</label><select class="inp" id="sub-speed-unit"><option value="MBIT">مگابیت/ثانیه (Mbps)</option><option value="KB">کیلوبایت/ثانیه (KB/s)</option></select></div>
      </div>
      <div class="form-g"><label>توضیحات / یادداشت</label><input class="inp" id="sub-note" placeholder="توضیحات اختیاری..."></div>
      <div class="form-g">
        <label>اتصال کانفیگ‌ها به این اشتراک</label>
        <div class="cfg-checklist" id="sub-links-checklist">در حال بارگذاری لیست کانفیگ‌ها...</div>
      </div>
      <button class="btn btn-p" type="submit" style="width:100%;margin-top:14px;justify-content:center"><i class="ti ti-check"></i> ذخیره اشتراک</button>
    </form>
  </div>
</div>

<!-- MODAL: LINK -->
<div class="modal" id="modal-link">
  <div class="modal-box">
    <div class="modal-head">
      <div class="modal-title" id="link-modal-title"><i class="ti ti-link"></i> ساخت کانفیگ جدید</div>
      <button class="close-btn" onclick="closeModal('modal-link')"><i class="ti ti-x"></i></button>
    </div>
    <form id="form-link">
      <div class="form-g"><label>عنوان کانفیگ</label><input class="inp" id="nl-label" placeholder="مثلاً: VLESS gRPC Direct" required></div>
      <div class="form-g">
        <label>پروتکل / ترابرد</label>
        <select class="inp" id="nl-proto">
          <option value="vless-grpc" selected>VLESS · gRPC (پیش‌فرض)</option>
          <option value="vless-ws">VLESS · WebSocket</option>
          <option value="xhttp">XHTTP Ultra · Mode: auto</option>
        </select>
      </div>
      <div class="form-g"><label>اشتراک والد (اختیاری)</label><select class="inp" id="nl-sub"><option value="">بدون اشتراک (مستقل)</option></select></div>
      <div class="form-row">
        <div class="form-g"><label>حجم (0 = نامحدود)</label><input class="inp" type="number" step="0.1" id="nl-val" value="0"></div>
        <div class="form-g"><label>واحد حجم</label><select class="inp" id="nl-unit"><option value="GB">GB</option><option value="MB">MB</option></select></div>
      </div>
      <div class="form-row">
        <div class="form-g"><label>اعتبار (روز - 0 = نامحدود)</label><input class="inp" type="number" id="nl-exp" value="0"></div>
        <div class="form-g"><label>محدودیت آی‌پی (0 = نامحدود)</label><input class="inp" type="number" id="nl-iplimit" value="0"></div>
      </div>
      <div class="form-g"><label>توضیحات</label><input class="inp" id="nl-note" placeholder="توضیحات اختیاری..."></div>
      
      <!-- ADVANCED SETTINGS ACCORDION -->
      <div style="margin-top:14px;border-top:1px dashed var(--card-b);padding-top:10px">
        <button type="button" class="btn btn-sm btn-g" onclick="const box=document.getElementById('adv-settings-box');box.style.display=box.style.display==='none'?'block':'none'" style="width:100%;justify-content:space-between">
          <span><i class="ti ti-adjustments"></i> تنظیمات پیشرفته (ALPN, Fragment, Mux, SNI, Clean IP)</span>
          <i class="ti ti-chevron-down"></i>
        </button>
        <div id="adv-settings-box" style="display:none;margin-top:12px;padding:14px;background:rgba(0,0,0,0.25);border:1px solid var(--card-b);border-radius:14px">
          <div class="form-row">
            <div class="form-g"><label>آی‌پی تمیز اختصاصی (Clean IP)</label><input class="inp" id="nl-clean-ip" placeholder="مثلاً: 104.21.x.x"></div>
            <div class="form-g"><label>SNI اختصاصی</label><input class="inp" id="nl-sni" placeholder="مثلاً: sni.domain.com"></div>
          </div>
          <div class="form-row">
            <div class="form-g"><label>Host Header اختصاصی</label><input class="inp" id="nl-host" placeholder="مثلاً: host.domain.com"></div>
            <div class="form-g"><label>ALPN</label><input class="inp" id="nl-alpn" placeholder="پیش‌فرض: http/1.1 یا h2"></div>
          </div>
          <div style="font-weight:700;font-size:11px;color:var(--t2);margin:10px 0 6px"><i class="ti ti-scissors"></i> تنظیمات Fragment (ضد فیلترینگ / Anti-DPI)</div>
          <div class="form-row">
            <div class="form-g"><label>نوع پکت Fragment</label><input class="inp" id="nl-fg-packets" placeholder="خالی = غیرفعال (مثلاً: tlshello یا 1-3)"></div>
            <div class="form-g"><label>طول Fragment (Length)</label><input class="inp" id="nl-fg-len" value="10-20" placeholder="10-20"></div>
          </div>
          <div class="form-g"><label>فاصله زمانی Fragment (Interval)</label><input class="inp" id="nl-fg-interval" value="10-20" placeholder="10-20"></div>
          <div style="font-weight:700;font-size:11px;color:var(--t2);margin:10px 0 6px"><i class="ti ti-arrows-join-2"></i> تنظیمات Multiplexing (Mux)</div>
          <div class="form-row" style="align-items:center">
            <div class="form-g" style="margin-bottom:0">
              <label class="cfg-chk-item" style="padding:0">
                <input type="checkbox" id="nl-mux-enable">
                <span>فعال‌سازی Mux (Multiplexing)</span>
              </label>
            </div>
            <div class="form-g" style="margin-bottom:0"><label>همزمانی Mux (Concurrency)</label><input class="inp" type="number" id="nl-mux-concurrency" value="8"></div>
          </div>
        </div>
      </div>

      <button class="btn btn-p" type="submit" style="width:100%;margin-top:14px;justify-content:center"><i class="ti ti-check"></i> ذخیره کانفیگ</button>
    </form>
  </div>
</div>

<!-- MODAL: QR CODE -->
<div class="modal" id="modal-qr" onclick="this.classList.remove('open')">
  <div style="background:var(--card);border:1px solid var(--card-b);border-radius:22px;padding:26px;text-align:center;max-width:320px;width:100%" onclick="event.stopPropagation()">
    <div style="font-size:14px;font-weight:800;margin-bottom:14px" id="qr-title">QR Code</div>
    <div style="background:#fff;padding:12px;border-radius:14px;margin-bottom:14px"><img id="qr-img" src="" alt="QR" style="width:100%;display:block"></div>
    <button class="btn btn-g" style="width:100%;justify-content:center" onclick="closeModal('modal-qr')"><i class="ti ti-x"></i> بستن</button>
  </div>
</div>

<div class="toast" id="toast"></div>

<script>
function toast(msg,type=''){
  const t=document.getElementById('toast');
  t.textContent=msg;t.className='toast show '+(type||'');
  setTimeout(()=>t.classList.remove('show'),2400);
}
function esc(s){return String(s||'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}
function fmtB(b){if(!b||b===0)return '0 B';if(b<1024)return b+' B';if(b<1024**2)return (b/1024).toFixed(1)+' KB';if(b<1024**3)return (b/1024**2).toFixed(2)+' MB';return (b/1024**3).toFixed(2)+' GB'}

function openModal(id){document.getElementById(id).classList.add('open')}
function closeModal(id){document.getElementById(id).classList.remove('open')}

function showQR(title, text){
  document.getElementById('qr-title').textContent=title;
  document.getElementById('qr-img').src='https://api.qrserver.com/v1/create-qr-code/?size=260x260&data='+encodeURIComponent(text);
  openModal('modal-qr');
}

// Navigation & Tab Switching
const sb=document.getElementById('sb'),overlay=document.getElementById('overlay');
function openSb(){sb.classList.add('open');overlay.classList.add('open')}
function closeSb(){sb.classList.remove('open');overlay.classList.remove('open')}
document.getElementById('open-sb').addEventListener('click',openSb);
document.getElementById('close-sb').addEventListener('click',closeSb);
overlay.addEventListener('click',closeSb);

function navTo(name){
  document.querySelectorAll('.nav-it').forEach(n=>n.classList.toggle('on',n.dataset.pg===name));
  document.querySelectorAll('.pg').forEach(p=>p.classList.toggle('on',p.id==='pg-'+name));
  const loaders={overview:fetchStats,subs:loadSubs,links:loadLinks,connections:loadConns,settings:loadSettings,logs:loadActivity,errors:fetchStats};
  if(loaders[name])loaders[name]();
  closeSb();window.scrollTo({top:0,behavior:'smooth'});
}
document.querySelectorAll('.nav-it').forEach(el=>el.addEventListener('click',()=>navTo(el.dataset.pg)));

document.getElementById('logout-btn').addEventListener('click',async()=>{
  await fetch('/api/logout',{method:'POST'});
  location.href='/login';
});

const WORKER_SCRIPT_TEMPLATE = `/**
 * Cloudflare Worker Reverse Proxy for X4G Panel (VLESS + WebSocket + TLS)
 */
const DEFAULT_BACKEND_HOST = "x4g-backend.up.railway.app";

export default {
  async fetch(request, env, ctx) {
    try {
      const backendHost = env.BACKEND_HOST || DEFAULT_BACKEND_HOST;
      const url = new URL(request.url);
      url.hostname = backendHost;
      url.protocol = "https:";

      const headers = new Headers(request.headers);
      headers.set("Host", backendHost);
      headers.set("X-Forwarded-Host", request.headers.get("Host") || url.hostname);
      headers.set("X-Forwarded-Proto", "https");

      const clientIp = request.headers.get("CF-Connecting-IP");
      if (clientIp) {
        headers.set("X-Real-IP", clientIp);
        const existingFwd = request.headers.get("X-Forwarded-For");
        headers.set("X-Forwarded-For", existingFwd ? \`\${existingFwd}, \${clientIp}\` : clientIp);
      }

      const fetchInit = {
        method: request.method,
        headers: headers,
        redirect: "manual",
      };

      if (request.method !== "GET" && request.method !== "HEAD") {
        fetchInit.body = request.body;
      }

      const response = await fetch(url.toString(), fetchInit);
      const responseHeaders = new Headers(response.headers);
      responseHeaders.set("Access-Control-Allow-Origin", "*");

      return new Response(response.body, {
        status: response.status,
        statusText: response.statusText,
        headers: responseHeaders,
      });
    } catch (err) {
      return new Response(\`Cloudflare Worker Proxy Error: \${err.message}\`, { status: 502 });
    }
  },
};`;

async function loadSettings(){
  try{
    const r=await fetch('/api/settings'),d=await r.json();
    document.getElementById('st-worker-domain').value = d.worker_domain||'';
    document.getElementById('st-clean-ip').value = d.clean_ip||'';
    document.getElementById('worker-code-box').value = WORKER_SCRIPT_TEMPLATE;
  }catch(e){toast('خطا در دریافت تنظیمات','err')}
}

document.addEventListener('submit',async e=>{
  if(e.target && e.target.id==='form-settings'){
    e.preventDefault();
    const payload = {
      worker_domain: document.getElementById('st-worker-domain').value.trim(),
      clean_ip: document.getElementById('st-clean-ip').value.trim(),
    };
    try{
      const r=await fetch('/api/settings',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});
      if(r.ok){
        toast('تنظیمات وورکر ذخیره شد ✓','ok');
        loadSettings();
      }else{
        toast('خطا در ذخیره تنظیمات','err');
      }
    }catch(err){toast('خطا در ارتباط با سرور','err')}
  }
});

function copyWorkerScript(){
  const code = document.getElementById('worker-code-box').value;
  navigator.clipboard.writeText(code).then(()=>toast('کد Cloudflare Worker کپی شد ✓','ok'));
}

// STATS & DASHBOARD OVERVIEW
let ch1;
async function fetchStats(){
  try{
    const r=await fetch('/stats'),d=await r.json();
    document.getElementById('m-conns').textContent=d.active_connections;
    document.getElementById('m-traffic').textContent=d.total_traffic_mb.toFixed(1)+' MB';
    document.getElementById('m-subs').textContent=d.active_subs??0;
    document.getElementById('m-ssub').textContent='از '+d.subs_count+' اشتراک';
    document.getElementById('m-alinks').textContent=d.active_links??0;
    document.getElementById('m-lsub').textContent='از '+d.links_count+' کانفیگ';
    document.getElementById('uptime-inline').textContent=d.uptime;
    document.getElementById('uptime-badge').textContent=d.uptime;
    document.getElementById('last-upd').textContent='بروزرسانی: '+new Date().toLocaleTimeString('fa-IR');
    document.getElementById('subs-nb').textContent=d.subs_count||0;
    document.getElementById('links-nb').textContent=d.links_count||0;
    document.getElementById('conns-nb').textContent=d.active_connections||0;
    
    if(d.hourly){
      const labels=Object.keys(d.hourly).sort(),vals=labels.map(k=>+(d.hourly[k]/1024**2).toFixed(2));
      if(ch1){ch1.data.labels=labels;ch1.data.datasets[0].data=vals;ch1.update()}
    }
  }catch(e){console.error(e)}
}

function initChart(){
  const ctx=document.getElementById('ch1').getContext('2d');
  ch1=new Chart(ctx,{
    type:'line',
    data:{labels:[],datasets:[{label:'ترافیک (MB)',data:[],borderColor:'#10b981',backgroundColor:'rgba(16,185,129,0.1)',fill:true,tension:.4}]},
    options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},scales:{x:{grid:{display:false}},y:{beginAtZero:true}}}
  });
}

// SUBSCRIPTION MANAGEMENT
let allAvailableLinks = [];
let currentSubId = '';

async function loadSubs(){
  try{
    const r=await fetch('/api/subs'),d=await r.json();
    if(d.subs) renderSubs(d.subs);
  }catch(e){toast('خطا در بارگذاری اشتراک‌ها','err')}
}

function renderSubs(subs){
  const el=document.getElementById('subs-list');
  if(!subs.length){
    el.innerHTML='<div class="card" style="text-align:center;padding:40px;color:var(--t3)"><i class="ti ti-users-group" style="font-size:32px;display:block;margin-bottom:10px"></i>هیچ اشتراکی تعریف نشده است. بر روی «اشتراک جدید» کلیک کنید.</div>';
    return;
  }
  el.innerHTML=subs.map(s=>{
    const pct = s.limit_bytes === 0 ? 0 : Math.min(100, (s.used_bytes / s.limit_bytes) * 100);
    const bc = pct > 90 ? 'var(--red)' : pct > 70 ? 'var(--amber)' : 'var(--green)';
    const expText = s.expires_at ? new Date(s.expires_at).toLocaleDateString('fa-IR') : 'نامحدود';
    return `
      <div class="sub-card">
        <div class="sub-head">
          <div>
            <div class="sub-label">${esc(s.label)}</div>
            <div style="font-size:10.5px;color:var(--t3);margin-top:4px">
              <span class="badge bg-blue" style="margin-left:6px"><i class="ti ti-link"></i> ${s.links_count} کانفیگ</span>
              <span class="badge bg-green"><i class="ti ti-plug-connected"></i> ${s.connections} اتصال فعال</span>
              <span style="margin-right:8px"><i class="ti ti-calendar"></i> انقضا: ${expText}</span>
            </div>
          </div>
          <div style="display:flex;gap:6px">
            <button class="btn btn-sm btn-g" onclick="openSubModal('${s.sub_id}')"><i class="ti ti-edit"></i> ویرایش</button>
            <button class="btn btn-sm btn-d" onclick="deleteSub('${s.sub_id}')"><i class="ti ti-trash"></i> حذف</button>
          </div>
        </div>
        <div style="margin-top:10px">
          <div class="ubar"><div class="ubar-f" style="width:${pct}%;background:${bc}"></div></div>
          <div class="utxt"><span>مصرف: ${esc(s.used_fmt)}</span><span>سهمیه: ${esc(s.limit_fmt)}</span></div>
        </div>
        <div class="sub-links-box">
          <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:6px">
            <span style="font-weight:700;color:var(--t1)"><i class="ti ti-world"></i> صفحه وب اختصاصی کاربر:</span>
            <button class="btn btn-sm btn-p" onclick="navigator.clipboard.writeText('${esc(s.sub_url)}').then(()=>toast('لینک صفحه وب کپی شد ✓','ok'))"><i class="ti ti-copy"></i> کپی صفحه وب</button>
          </div>
          <div style="word-break:break-all;color:var(--accent2);margin-bottom:8px">${esc(s.sub_url)}</div>
          
          <div style="display:flex;align-items:center;justify-content:space-between;margin-top:8px;padding-top:8px;border-top:1px dashed var(--card-b)">
            <span style="font-weight:700;color:var(--t1)"><i class="ti ti-rss"></i> لینک ساب کلینت‌ها (V2ray/Sing-box):</span>
            <div style="display:flex;gap:6px">
              <button class="btn btn-sm btn-g" onclick="navigator.clipboard.writeText('${esc(s.raw_sub_url)}').then(()=>toast('لینک ساب کپی شد ✓','ok'))"><i class="ti ti-copy"></i> کپی ساب</button>
              <button class="btn btn-sm btn-g" onclick="showQR('${esc(s.label)}', '${esc(s.raw_sub_url)}')"><i class="ti ti-qrcode"></i> QR</button>
            </div>
          </div>
        </div>
      </div>
    `;
  }).join('');
}

async function openSubModal(sid=''){
  currentSubId = sid;
  document.getElementById('sub-modal-title').textContent = sid ? 'ویرایش اشتراک' : 'ساخت اشتراک جدید';
  
  // Load links for checklist
  const lr = await fetch('/api/links'), ld = await lr.json();
  allAvailableLinks = ld.links || [];
  
  let targetSub = null;
  if(sid){
    const sr = await fetch('/api/subs'), sd = await sr.json();
    targetSub = (sd.subs || []).find(s=>s.sub_id===sid);
  }
  
  document.getElementById('sub-label').value = targetSub ? targetSub.label : '';
  document.getElementById('sub-limit-val').value = targetSub ? (targetSub.limit_bytes / (1024**3)).toFixed(1) : 0;
  document.getElementById('sub-exp').value = 0;
  document.getElementById('sub-iplimit').value = targetSub ? targetSub.ip_limit : 0;
  document.getElementById('sub-speed-val').value = targetSub ? (targetSub.speed_limit_bytes * 8 / 1024 / 1024).toFixed(1) : 0;
  document.getElementById('sub-note').value = targetSub ? targetSub.note : '';
  
  const chkEl = document.getElementById('sub-links-checklist');
  if(!allAvailableLinks.length){
    chkEl.innerHTML = '<span style="color:var(--t3)">هیچ کانفیگی برای انتخاب وجود ندارد.</span>';
  } else {
    chkEl.innerHTML = allAvailableLinks.map(l=>{
      const isChecked = targetSub && targetSub.links && targetSub.links.includes(l.uuid);
      return `
        <label class="cfg-chk-item">
          <input type="checkbox" value="${l.uuid}" ${isChecked?'checked':''}>
          <span>${esc(l.label)} <small style="color:var(--t3)">(:${l.port||443})</small></span>
        </label>
      `;
    }).join('');
  }
  openModal('modal-sub');
}

document.getElementById('form-sub').addEventListener('submit',async e=>{
  e.preventDefault();
  const checkedUuids = Array.from(document.querySelectorAll('#sub-links-checklist input:checked')).map(i=>i.value);
  const payload = {
    label: document.getElementById('sub-label').value.trim(),
    limit_value: parseFloat(document.getElementById('sub-limit-val').value)||0,
    limit_unit: document.getElementById('sub-limit-unit').value,
    expires_days: parseInt(document.getElementById('sub-exp').value)||0,
    ip_limit: parseInt(document.getElementById('sub-iplimit').value)||0,
    speed_limit_value: parseFloat(document.getElementById('sub-speed-val').value)||0,
    speed_limit_unit: document.getElementById('sub-speed-unit').value,
    note: document.getElementById('sub-note').value.trim(),
    links: checkedUuids,
  };
  
  const url = currentSubId ? ('/api/subs/' + currentSubId) : '/api/subs';
  const method = currentSubId ? 'PATCH' : 'POST';
  
  try{
    const r=await fetch(url,{method,headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});
    if(r.ok){
      toast('اشتراک با موفقیت ذخیره شد ✓','ok');
      closeModal('modal-sub');
      loadSubs();
    } else {
      toast('خطا در ذخیره اشتراک','err');
    }
  }catch(err){toast('خطا در ارتباط با سرور','err')}
});

async function deleteSub(sid){
  if(!confirm('آیا از حذف این اشتراک اطمینان دارید؟ کانفیگ‌های مرتبط از این اشتراک جدا می‌شوند.')) return;
  try{
    const r=await fetch('/api/subs/'+sid,{method:'DELETE'});
    if(r.ok){toast('اشتراک حذف شد','ok');loadSubs();}
  }catch(e){toast('خطا در حذف','err')}
}

// LINKS MANAGEMENT
async function loadLinks(){
  try{
    const r=await fetch('/api/links'),d=await r.json();
    if(d.links) renderLinks(d.links);
  }catch(e){toast('خطا در بارگذاری کانفیگ‌ها','err')}
}

function protoChipText(proto){
  if(proto==='vless-ws') return '<span class="badge bg-blue"><i class="ti ti-wifi"></i> VLESS WS</span>';
  if(proto==='xhttp') return '<span class="badge bg-green" style="background:var(--purple-bg);color:var(--purple-t)"><i class="ti ti-bolt"></i> XHTTP Auto</span>';
  return '<span class="badge bg-green"><i class="ti ti-route"></i> VLESS gRPC</span>';
}

let currentLinkId = '';

function renderLinks(links){
  const el=document.getElementById('links-list');
  if(!links.length){
    el.innerHTML='<div class="card" style="text-align:center;padding:40px;color:var(--t3)"><i class="ti ti-link" style="font-size:32px;display:block;margin-bottom:10px"></i>هیچ کانفیگی ساخته نشده است. بر روی «کانفیگ جدید» کلیک کنید.</div>';
    return;
  }
  el.innerHTML=links.map(l=>{
    return `
      <div class="sub-card">
        <div class="sub-head">
          <div>
            <div class="sub-label">${esc(l.label)}</div>
            <div style="font-size:10.5px;color:var(--t3);margin-top:4px">
              ${protoChipText(l.protocol)}
              <span class="badge bg-blue" style="margin-right:6px"><i class="ti ti-plug-connected"></i> ${l.connected_ips||0} آی‌پی متصل</span>
            </div>
          </div>
          <div style="display:flex;gap:6px">
            <button class="btn btn-sm btn-g" onclick="openLinkModal('${l.uuid}')"><i class="ti ti-edit"></i> ویرایش</button>
            <button class="btn btn-sm btn-g" onclick="navigator.clipboard.writeText('${esc(l.vless_link)}').then(()=>toast('لینک VLESS کپی شد ✓','ok'))"><i class="ti ti-copy"></i> کپی VLESS</button>
            <button class="btn btn-sm btn-g" onclick="showQR('${esc(l.label)}', '${esc(l.vless_link)}')"><i class="ti ti-qrcode"></i> QR</button>
            <button class="btn btn-sm btn-d" onclick="deleteLink('${l.uuid}')"><i class="ti ti-trash"></i></button>
          </div>
        </div>
        <div class="sub-links-box" style="margin-top:8px;font-size:10px">
          ${esc(l.vless_link)}
        </div>
      </div>
    `;
  }).join('');
}

async function openLinkModal(uid=''){
  currentLinkId = uid;
  document.getElementById('link-modal-title').innerHTML = uid ? '<i class="ti ti-edit"></i> ویرایش کانفیگ' : '<i class="ti ti-link"></i> ساخت کانفیگ جدید';

  const sr=await fetch('/api/subs'),sd=await sr.json();
  const sel=document.getElementById('nl-sub');
  sel.innerHTML='<option value="">بدون اشتراک (مستقل)</option>'+(sd.subs||[]).map(s=>`<option value="${s.sub_id}">${esc(s.label)}</option>`).join('');

  let targetLink = null;
  if(uid){
    const lr=await fetch('/api/links'),ld=await lr.json();
    targetLink = (ld.links||[]).find(l=>l.uuid===uid);
  }

  document.getElementById('nl-label').value = targetLink ? targetLink.label : '';
  document.getElementById('nl-proto').value = targetLink ? targetLink.protocol : 'vless-grpc';
  document.getElementById('nl-sub').value = targetLink ? (targetLink.sub_id || '') : '';
  document.getElementById('nl-val').value = targetLink ? (targetLink.limit_bytes / (1024**3)).toFixed(1) : 0;
  document.getElementById('nl-exp').value = 0;
  document.getElementById('nl-iplimit').value = targetLink ? targetLink.ip_limit : 0;
  document.getElementById('nl-note').value = targetLink ? (targetLink.note || '') : '';
  document.getElementById('nl-clean-ip').value = targetLink ? (targetLink.clean_ip || '') : '';
  document.getElementById('nl-sni').value = targetLink ? (targetLink.sni || '') : '';
  document.getElementById('nl-host').value = targetLink ? (targetLink.host || '') : '';
  document.getElementById('nl-alpn').value = targetLink ? (targetLink.alpn || '') : '';
  document.getElementById('nl-fg-packets').value = targetLink ? (targetLink.fragment_packets || '') : '';
  document.getElementById('nl-fg-len').value = targetLink ? (targetLink.fragment_length || '10-20') : '10-20';
  document.getElementById('nl-fg-interval').value = targetLink ? (targetLink.fragment_interval || '10-20') : '10-20';
  document.getElementById('nl-mux-enable').checked = targetLink ? !!targetLink.mux_enable : false;
  document.getElementById('nl-mux-concurrency').value = targetLink ? (targetLink.mux_concurrency || 8) : 8;

  openModal('modal-link');
}

document.getElementById('form-link').addEventListener('submit',async e=>{
  e.preventDefault();
  const payload={
    label: document.getElementById('nl-label').value.trim(),
    protocol: document.getElementById('nl-proto').value||'vless-grpc',
    sub_id: document.getElementById('nl-sub').value||null,
    limit_value: parseFloat(document.getElementById('nl-val').value)||0,
    limit_unit: document.getElementById('nl-unit').value,
    expires_days: parseInt(document.getElementById('nl-exp').value)||0,
    ip_limit: parseInt(document.getElementById('nl-iplimit').value)||0,
    note: document.getElementById('nl-note').value.trim(),
    clean_ip: document.getElementById('nl-clean-ip').value.trim(),
    sni: document.getElementById('nl-sni').value.trim(),
    host_header: document.getElementById('nl-host').value.trim(),
    alpn: document.getElementById('nl-alpn').value.trim(),
    fragment_packets: document.getElementById('nl-fg-packets').value.trim(),
    fragment_length: document.getElementById('nl-fg-len').value.trim(),
    fragment_interval: document.getElementById('nl-fg-interval').value.trim(),
    mux_enable: document.getElementById('nl-mux-enable').checked,
    mux_concurrency: parseInt(document.getElementById('nl-mux-concurrency').value)||8,
  };

  const url = currentLinkId ? ('/api/links/' + currentLinkId) : '/api/links';
  const method = currentLinkId ? 'PATCH' : 'POST';

  try{
    const r=await fetch(url,{method,headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});
    if(r.ok){
      toast(currentLinkId ? 'کانفیگ ویرایش شد ✓' : 'کانفیگ جدید ساخته شد ✓','ok');
      closeModal('modal-link');
      loadLinks();
    } else {
      toast('خطا در ذخیره کانفیگ','err');
    }
  }catch(e){toast('خطا در ارتباط با سرور','err')}
});

async function deleteLink(uid){
  if(!confirm('آیا از حذف این کانفیگ اطمینان دارید؟')) return;
  try{
    const r=await fetch('/api/links/'+uid,{method:'DELETE'});
    if(r.ok){toast('کانفیگ حذف شد','ok');loadLinks();}
  }catch(e){toast('خطا در حذف','err')}
}

// CONNECTIONS & LOGS
async function loadConns(){
  try{
    const r=await fetch('/api/connections'),d=await r.json();
    const el=document.getElementById('conns-table');
    if(!d.configs||!d.configs.length){
      el.innerHTML='<div style="text-align:center;padding:20px;color:var(--t3)">هیچ اتصال فعالی وجود ندارد.</div>';
      return;
    }
    el.innerHTML=`
      <table class="tbl">
        <thead><tr><th>کانفیگ</th><th>آی‌پی کلاینت</th><th>مصرف بایت</th><th>آخرین اتصال</th></tr></thead>
        <tbody>
          ${d.configs.map(c=>(c.connections||[]).map(ip=>`
            <tr>
              <td><strong>${esc(c.label)}</strong></td>
              <td><code>${esc(ip.ip)}</code></td>
              <td>${esc(ip.bytes_fmt)}</td>
              <td>${new Date(ip.last_connected_at||Date.now()).toLocaleTimeString('fa-IR')}</td>
            </tr>
          `).join('')).join('')}
        </tbody>
      </table>
    `;
  }catch(e){}
}

async function loadActivity(){
  try{
    const r=await fetch('/api/activity'),d=await r.json();
    const el=document.getElementById('logs-list');
    if(!d.logs||!d.logs.length){el.innerHTML='<div style="padding:20px;color:var(--t3)">لاگی ثبت نشده است.</div>';return}
    el.innerHTML=d.logs.slice().reverse().map(l=>`
      <div style="padding:8px 0;border-bottom:1px solid rgba(16,185,129,0.06);font-size:12px;display:flex;justify-content:space-between">
        <span><strong>[${l.kind}]</strong> ${esc(l.message)}</span>
        <span style="color:var(--t3)">${new Date(l.time).toLocaleTimeString('fa-IR')}</span>
      </div>
    `).join('');
  }catch(e){}
}

document.addEventListener('DOMContentLoaded',()=>{
  initChart();
  fetchStats();
  setInterval(fetchStats,5000);
});
</script>
</body></html>"""


def get_public_page_html(uuid_key: str) -> str:
    """صفحه پابلیک ساب - سیستم اشتراک‌ها و کانفیگ‌های gRPC توسط Kourosh با فونت وزیرمتن"""
    return f"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
<title>توسط Kourosh Sub</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@100;200;300;400;500;600;700;800;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.19.0/dist/tabler-icons.min.css">
<style>
*{{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent;font-family:'Vazirmatn',sans-serif !important}}
:root{{
  --bg:#060a14;--bg2:#0a1020;--bg3:#0d1428;
  --card:#0c1326;--card-b:rgba(16,185,129,0.14);--card-bh:rgba(16,185,129,0.3);
  --accent:#10b981;--accent2:#059669;--accent-d:rgba(16,185,129,0.1);
  --green:#10b981;--green-bg:rgba(16,185,129,0.12);--green-t:#34d399;
  --red:#EF4444;--red-bg:rgba(239,68,68,0.12);--red-t:#FB8585;
  --amber:#F2A33D;--amber-bg:rgba(242,163,61,0.12);--amber-t:#F9C988;
  --purple:#9D7BF0;--purple-bg:rgba(157,123,240,0.12);--purple-t:#BCA4F7;
  --t1:#EFF4FF;--t2:#8AA0C4;--t3:#48577A;
  --radius:18px;--shadow:0 12px 40px rgba(0,0,0,0.45);
}}
html,body{{min-height:100%;background:var(--bg);font-family:'Vazirmatn',sans-serif !important;color:var(--t1);font-size:14px}}
.bg-fx{{position:fixed;inset:0;background:radial-gradient(ellipse 70% 45% at 50% -8%,rgba(16,185,129,0.14),transparent 62%),var(--bg);z-index:0;pointer-events:none}}
.grid-fx{{position:fixed;inset:0;background-image:linear-gradient(rgba(16,185,129,0.03) 1px,transparent 1px),linear-gradient(90deg,rgba(16,185,129,0.03) 1px,transparent 1px);background-size:46px 46px;z-index:0;pointer-events:none}}
.wrap{{position:relative;z-index:10;max-width:800px;margin:0 auto;padding:24px 16px 64px}}
.top{{display:flex;align-items:center;justify-content:space-between;margin-bottom:26px;gap:10px}}
.brand{{display:flex;align-items:center;gap:11px}}
.brand-img{{width:40px;height:40px;border-radius:50%;overflow:hidden;border:1px solid var(--card-b);box-shadow:0 0 14px rgba(16,185,129,.35);flex-shrink:0}}
.brand-img img{{width:100%;height:100%;object-fit:cover}}
.brand-name{{font-size:15px;font-weight:800;color:var(--t1)}}
.brand-name a{{color:inherit;text-decoration:none}}
.brand-sub{{font-size:9.5px;color:var(--accent);font-weight:600}}

.sub-info{{background:var(--card);border:1px solid var(--card-b);border-radius:22px;padding:24px;margin-bottom:16px;box-shadow:var(--shadow);position:relative;overflow:hidden}}
.sub-name{{font-size:22px;font-weight:800;color:var(--t1);margin-bottom:6px}}
.sub-desc{{font-size:12.5px;color:var(--t2);line-height:1.8;margin-bottom:14px}}
.sub-sub-box{{background:var(--accent-d);border:1px solid var(--card-b);border-radius:13px;padding:12px 14px;display:flex;align-items:center;gap:9px;flex-wrap:wrap}}
.sub-sub-url{{font-family:ui-monospace,monospace;font-size:10.5px;color:var(--accent);word-break:break-all;flex:1}}

.stats-bar{{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-bottom:18px}}
.stat-card{{background:var(--card);border:1px solid var(--card-b);border-radius:16px;padding:16px 17px}}
.stat-label{{font-size:9px;color:var(--t3);font-weight:700;text-transform:uppercase;letter-spacing:.07em;margin-bottom:7px}}
.stat-val{{font-size:22px;font-weight:800;color:var(--t1);line-height:1}}
.stat-sub{{font-size:9.5px;color:var(--t3);margin-top:6px}}

.copy-all-bar{{display:flex;align-items:center;gap:12px;background:linear-gradient(120deg,var(--accent) 0%,#059669 100%);border-radius:18px;padding:16px 19px;margin-bottom:18px;box-shadow:0 10px 30px rgba(16,185,129,.28);flex-wrap:wrap}}
.copy-all-text{{flex:1;min-width:160px}}
.copy-all-title{{font-size:13.5px;font-weight:800;color:#fff;display:flex;align-items:center;gap:6px}}
.copy-all-sub{{font-size:10px;color:rgba(255,255,255,.8);margin-top:3px}}
.copy-all-btn{{background:#fff;color:#047857;border:none;border-radius:12px;padding:10px 19px;font-size:12.5px;font-weight:800;cursor:pointer;display:flex;align-items:center;gap:6px;transition:.18s;white-space:nowrap}}
.copy-all-btn:hover{{transform:translateY(-1px)}}

.cfg-card{{background:var(--card);border:1px solid var(--card-b);border-radius:18px;margin-bottom:14px;overflow:hidden}}
.cfg-top{{padding:17px 19px 15px}}
.cfg-head{{display:flex;align-items:flex-start;justify-content:space-between;gap:8px;margin-bottom:12px;flex-wrap:wrap}}
.cfg-label{{font-size:14.5px;font-weight:800;color:var(--t1)}}
.cfg-status{{display:flex;align-items:center;gap:5px;font-size:10px;font-weight:700;padding:4px 10px;border-radius:20px}}
.cfg-status.ok{{background:var(--green-bg);color:var(--green-t)}}
.cfg-status.no{{background:var(--red-bg);color:var(--red-t)}}
.ubar{{height:6px;border-radius:4px;background:rgba(16,185,129,0.1);overflow:hidden;margin-bottom:5px}}
.ubar-f{{height:100%;border-radius:4px;transition:width .5s ease}}
.utxt{{font-size:10px;color:var(--t3);display:flex;justify-content:space-between}}
.cfg-bottom{{padding:15px 19px;border-top:1px dashed var(--card-b)}}
.cfg-vless{{background:rgba(0,0,0,.3);border:1px solid var(--card-b);border-radius:10px;padding:11px 13px;font-size:10px;font-family:ui-monospace,monospace;color:var(--accent);word-break:break-all;margin-top:9px}}

.btn{{font-size:11.5px;font-weight:700;border-radius:10px;padding:8px 15px;cursor:pointer;display:inline-flex;align-items:center;gap:5px;border:none;transition:all .15s}}
.btn-p{{background:linear-gradient(135deg,#10b981,#059669);color:#fff}}
.btn-g{{background:var(--accent-d);color:var(--accent);border:1px solid var(--card-b)}}

.toast{{position:fixed;bottom:22px;left:50%;transform:translateX(-50%) translateY(40px);background:var(--card);border:1px solid var(--card-b);color:var(--t1);border-radius:12px;padding:10px 20px;font-size:12.5px;font-weight:700;opacity:0;transition:all .25s;z-index:999;pointer-events:none}}
.toast.show{{opacity:1;transform:translateX(-50%) translateY(0)}}
.toast.ok{{background:var(--green-bg);color:var(--green-t);border-color:rgba(16,185,129,.4)}}

.qr-modal{{display:none;position:fixed;inset:0;background:rgba(0,0,0,.75);z-index:600;align-items:center;justify-content:center;backdrop-filter:blur(6px)}}
.qr-modal.open{{display:flex}}
.qr-box{{background:var(--card);border:1px solid var(--card-b);border-radius:22px;padding:26px;text-align:center;max-width:320px;width:100%}}

.footer{{text-align:center;padding-top:28px;font-size:11px;color:var(--t3)}}
.footer a{{color:var(--accent);font-weight:700;text-decoration:none}}
</style>
</head>
<body>
<div class="bg-fx"></div><div class="grid-fx"></div>
<div class="toast" id="toast"></div>

<div class="qr-modal" id="qr-modal" onclick="this.classList.remove('open')">
  <div class="qr-box" onclick="event.stopPropagation()">
    <div style="font-size:14px;font-weight:800;margin-bottom:14px" id="qr-label">QR Code</div>
    <div style="background:#fff;padding:12px;border-radius:14px;margin-bottom:14px"><img id="qr-img" src="" alt="QR" style="width:100%;display:block"></div>
    <button class="btn btn-g" style="width:100%;justify-content:center" onclick="document.getElementById('qr-modal').classList.remove('open')"><i class="ti ti-x"></i> بستن</button>
  </div>
</div>

<div class="wrap">
  <div class="top">
    <div class="brand">
      <div class="brand-img"></div>
      <div><div class="brand-name"><a href="https://t.me/kouroxlog" target="_blank">توسط Kourosh</a></div><div class="brand-sub">Secure Sub</div></div>
    </div>
  </div>
  <div id="root">
    <div style="text-align:center;padding:80px 20px;color:var(--t3)"><i class="ti ti-loader-2" style="animation:spin 1s linear infinite;font-size:32px"></i><br><br>در حال بارگذاری اشتراک...</div>
  </div>
  <div class="footer">پشتیبانی: <a href="https://t.me/kouroxlog" target="_blank">@kouroxlog</a> · توسط Kourosh</div>
</div>

<script>
const UUID_KEY='{uuid_key}';

function toast(msg,type=''){{
  const t=document.getElementById('toast');
  t.textContent=msg;t.className='toast show '+(type||'');
  setTimeout(()=>t.classList.remove('show'),2400);
}}
function esc(s){{return String(s||'').replace(/[&<>"']/g,c=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}}[c]))}}
function fmtB(b){{if(!b||b===0)return '0 B';if(b<1024)return b+' B';if(b<1024**2)return (b/1024).toFixed(1)+' KB';if(b<1024**3)return (b/1024**2).toFixed(2)+' MB';return (b/1024**3).toFixed(2)+' GB'}}

function showQR(label,link){{
  document.getElementById('qr-label').textContent=label;
  document.getElementById('qr-img').src='https://api.qrserver.com/v1/create-qr-code/?size=260x260&data='+encodeURIComponent(link);
  document.getElementById('qr-modal').classList.add('open');
}}

async function loadData(){{
  const r=await fetch('/api/public/sub/'+UUID_KEY);
  return r.json();
}}

function renderContent(d){{
  const activeCount=d.links.filter(l=>l.active).length;
  const baseSubUrl = d.sub_url || (window.location.protocol + '//' + window.location.host + '/p/' + UUID_KEY);
  const rawSubUrl = d.raw_sub_url || (window.location.protocol + '//' + window.location.host + '/sub/' + UUID_KEY);

  window._x4gSubUrl  = baseSubUrl;
  window._x4gRawSubUrl = rawSubUrl;
  window._x4gSubName = d.name;
  window._x4gLinks   = d.links.map(l => ({{
    vless : l.vless_link,
    label : l.label,
  }}));

  document.getElementById('root').innerHTML=`
    <div class="sub-info">
      <div style="font-size:10px;font-weight:700;color:var(--accent);text-transform:uppercase;margin-bottom:8px"><i class="ti ti-users-group"></i> اشتراک اختصاصی VLESS</div>
      <div class="sub-name">${{esc(d.name)}}</div>
      ${{d.desc ? `<div class="sub-desc">${{esc(d.desc)}}</div>` : ''}}
      <div style="font-size:10.5px;color:var(--t3);margin-bottom:14px"><i class="ti ti-clock"></i> بروزرسانی: ${{new Date().toLocaleTimeString('fa-IR')}}</div>
      
      <div class="sub-sub-box">
        <span class="sub-sub-url">${{esc(rawSubUrl)}}</span>
        <button class="btn btn-p" style="padding:6px 12px;font-size:10.5px"
          onclick="navigator.clipboard.writeText(window._x4gRawSubUrl).then(()=>toast('لینک ساب کپی شد ✓','ok'))">
          <i class="ti ti-copy"></i> کپی لینک ساب
        </button>
        <button class="btn btn-g" style="padding:6px 12px;font-size:10.5px"
          onclick="showQR(window._x4gSubName, window._x4gRawSubUrl)">
          <i class="ti ti-qrcode"></i> QR
        </button>
      </div>
    </div>

    <div class="copy-all-bar">
      <div class="copy-all-text">
        <div class="copy-all-title"><i class="ti ti-copy"></i> کپی همه‌ی کانفیگ‌ها</div>
        <div class="copy-all-sub">تمام کانفیگ‌های فعال این اشتراک را یک‌جا کپی کن</div>
      </div>
      <button class="copy-all-btn" onclick="copyAllConfigs()"><i class="ti ti-clipboard-copy"></i> کپی همه (${{activeCount}})</button>
    </div>

    <div class="stats-bar">
      <div class="stat-card">
        <div class="stat-label">کانفیگ‌های فعال</div>
        <div class="stat-val">${{activeCount}}</div>
        <div class="stat-sub">از ${{d.links.length}} کانفیگ</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">اتصالات زنده</div>
        <div class="stat-val">${{d.active_connections}}</div>
        <div class="stat-sub" style="color:var(--green-t)">● آنلاین</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">کل مصرف / سهمیه</div>
        <div class="stat-val" style="font-size:16px;margin-top:2px">${{esc(d.total_used_fmt)}}</div>
        <div class="stat-sub">سهمیه: ${{esc(d.limit_fmt)}}</div>
      </div>
    </div>

    <div style="font-size:12px;font-weight:800;color:var(--t2);margin-bottom:13px;display:flex;align-items:center;gap:6px"><i class="ti ti-link" style="color:var(--accent)"></i> کانفیگ‌های VLESS</div>
    <div>
      ${{d.links.map((l, i) => {{
        const pct = l.limit_bytes === 0 ? 0 : Math.min(100, l.used_bytes / l.limit_bytes * 100);
        const bc  = pct > 90 ? 'var(--red)' : pct > 70 ? 'var(--amber)' : 'var(--green)';
        const lim = l.limit_bytes === 0 ? '∞' : fmtB(l.limit_bytes);
        return `
          <div class="cfg-card">
            <div class="cfg-top">
              <div class="cfg-head">
                <div>
                  <div class="cfg-label">${{esc(l.label)}}</div>
                  <div style="font-size:10px;color:var(--accent);margin-top:4px"><i class="ti ti-route"></i> ${{esc(l.protocol.toUpperCase())}}</div>
                </div>
                <span class="cfg-status ${{l.active ? 'ok' : 'no'}}">${{l.active ? '● فعال' : '● غیرفعال'}}</span>
              </div>
              <div>
                <div class="ubar"><div class="ubar-f" style="width:${{pct}}%;background:${{bc}}"></div></div>
                <div class="utxt"><span>${{esc(l.used_fmt)}} مصرف شده</span><span>سهمیه: ${{lim}}</span></div>
              </div>
            </div>
            <div class="cfg-bottom">
              <div style="display:flex;align-items:center;justify-content:space-between">
                <span style="font-size:11px;font-weight:700;color:var(--t2)"><i class="ti ti-key"></i> لینک کانفیگ:</span>
                <div style="display:flex;gap:6px">
                  <button class="btn btn-p" onclick="navigator.clipboard.writeText(window._x4gLinks[${{i}}].vless).then(()=>toast('لینک کپی شد ✓','ok'))"><i class="ti ti-copy"></i> کپی</button>
                  <button class="btn btn-g" onclick="showQR(window._x4gLinks[${{i}}].label, window._x4gLinks[${{i}}].vless)"><i class="ti ti-qrcode"></i> QR</button>
                </div>
              </div>
              <div class="cfg-vless">${{esc(l.vless_link)}}</div>
            </div>
          </div>
        `;
      }}).join('')}}
    </div>
  `;
  setTimeout(() => autoRefresh(), 30000);
}}

function copyAllConfigs(){{
  const links=window._x4gLinks||[];
  if(!links.length){{toast('کانفیگی برای کپی نیست','');return}}
  const text=links.map(l=>l.vless).join('\\n');
  navigator.clipboard.writeText(text).then(()=>toast('همه‌ی '+links.length+' کانفیگ کپی شد ✓','ok'));
}}

async function autoRefresh(){{
  try{{
    const data = await loadData();
    renderContent(data);
  }} catch(e) {{}}
}}

async function init(){{
  try{{
    const data = await loadData();
    renderContent(data);
  }} catch(e) {{
    document.getElementById('root').innerHTML = '<div style="text-align:center;padding:40px;color:var(--red-t)"><i class="ti ti-alert-circle"></i> خطا در بارگذاری اطلاعات اشتراک</div>';
  }}
}}

init();
</script>
</body></html>"""
