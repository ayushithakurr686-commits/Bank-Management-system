import json
import random
import string
from pathlib import Path
import streamlit as st

st.set_page_config(
    page_title="NexVault · Banking",
    page_icon="💠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Creative CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; }

html, body, [class*="css"] {
    font-family: 'Syne', sans-serif !important;
    background: #060810 !important;
}

.stApp {
    background: #060810 !important;
    color: #dde2f5;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #080b14 !important;
    border-right: 1px solid #141830 !important;
    padding-top: 0 !important;
}
[data-testid="stSidebar"] .block-container { padding-top: 0 !important; }

/* ── Sidebar logo strip ── */
.sidebar-brand {
    padding: 28px 20px 20px;
    border-bottom: 1px solid #141830;
    margin-bottom: 16px;
}
.sidebar-brand .logo-mark {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 40px; height: 40px;
    background: linear-gradient(135deg, #6c47ff 0%, #00d4aa 100%);
    border-radius: 10px;
    font-size: 20px;
    margin-bottom: 10px;
}
.sidebar-brand h2 {
    font-size: 1.25rem;
    font-weight: 800;
    letter-spacing: -0.5px;
    color: #eef0ff;
    margin: 0 0 2px;
}
.sidebar-brand p {
    font-size: 0.72rem;
    color: #3a4060;
    margin: 0;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}

/* ── Nav items ── */
[data-testid="stSidebar"] [data-testid="stRadio"] label {
    display: flex !important;
    align-items: center !important;
    gap: 10px !important;
    padding: 11px 16px !important;
    margin: 3px 8px !important;
    border-radius: 10px !important;
    font-size: 0.88rem !important;
    font-weight: 600 !important;
    color: #5a6080 !important;
    cursor: pointer;
    transition: all 0.15s;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
    background: #111428 !important;
    color: #aab0d8 !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] [aria-checked="true"] + label,
[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) {
    background: #14183a !important;
    color: #a78bfa !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] div[role="radio"]:has(input:checked) + div label {
    background: #14183a !important;
    color: #a78bfa !important;
}

/* hide radio circles */
[data-testid="stSidebar"] [data-testid="stRadio"] input[type="radio"] { display: none !important; }
[data-testid="stSidebar"] [data-testid="stRadio"] > div { gap: 2px !important; }

/* ── Hero banner ── */
.hero {
    position: relative;
    border-radius: 20px;
    padding: 44px 44px 40px;
    margin-bottom: 32px;
    overflow: hidden;
    background: #0c0f1f;
    border: 1px solid #1a1f3a;
}
.hero::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 280px; height: 280px;
    background: radial-gradient(circle, rgba(108,71,255,0.18) 0%, transparent 70%);
    pointer-events: none;
}
.hero::after {
    content: '';
    position: absolute;
    bottom: -40px; left: 30%;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(0,212,170,0.12) 0%, transparent 70%);
    pointer-events: none;
}
.hero-tag {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #12163a;
    border: 1px solid #2a2f5a;
    border-radius: 99px;
    padding: 4px 12px;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #7c6bff;
    margin-bottom: 16px;
}
.hero-tag .dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: #00d4aa;
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.5; transform: scale(0.8); }
}
.hero h1 {
    font-size: 2.6rem;
    font-weight: 800;
    letter-spacing: -1px;
    line-height: 1.1;
    color: #eef0ff;
    margin: 0 0 10px;
}
.hero h1 span {
    background: linear-gradient(90deg, #6c47ff, #00d4aa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero p {
    font-size: 0.92rem;
    color: #4a5070;
    margin: 0;
}
.hero-stats {
    display: flex;
    gap: 32px;
    margin-top: 28px;
    padding-top: 24px;
    border-top: 1px solid #141830;
}
.hero-stat-val {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.4rem;
    font-weight: 500;
    color: #eef0ff;
}
.hero-stat-label {
    font-size: 0.72rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #3a4060;
    margin-top: 2px;
}

/* ── Section heading ── */
.section-head {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 24px;
}
.section-head .icon-pill {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 38px; height: 38px;
    border-radius: 10px;
    font-size: 18px;
}
.icon-pill.violet { background: #1a1240; }
.icon-pill.teal   { background: #012820; }
.icon-pill.amber  { background: #1f1200; }
.icon-pill.red    { background: #200808; }
.icon-pill.blue   { background: #021430; }
.section-head h2 {
    font-size: 1.3rem;
    font-weight: 800;
    letter-spacing: -0.3px;
    color: #eef0ff;
    margin: 0;
}
.section-head p {
    font-size: 0.78rem;
    color: #3a4060;
    margin: 0;
}

/* ── Glass form card ── */
.glass-card {
    background: #0c0f1f;
    border: 1px solid #141830;
    border-radius: 16px;
    padding: 28px 28px 24px;
    margin-bottom: 16px;
}

/* ── Inputs ── */
.stTextInput > div > div > input,
.stNumberInput > div > div > input {
    background: #0a0d1a !important;
    border: 1px solid #1e2240 !important;
    border-radius: 10px !important;
    color: #c4c8f0 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.9rem !important;
    padding: 12px 14px !important;
    transition: border-color 0.2s !important;
}
.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus {
    border-color: #6c47ff !important;
    box-shadow: 0 0 0 3px rgba(108,71,255,0.12) !important;
}
label[data-testid="stWidgetLabel"] > div > p {
    color: #5a6080 !important;
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
}

/* ── Buttons ── */
.stButton > button {
    width: 100% !important;
    padding: 13px 24px !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 0.9rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.02em !important;
    border: none !important;
    background: linear-gradient(135deg, #6c47ff 0%, #00d4aa 100%) !important;
    color: #fff !important;
    cursor: pointer !important;
    transition: opacity 0.2s, transform 0.1s !important;
    box-shadow: 0 4px 20px rgba(108,71,255,0.25) !important;
}
.stButton > button:hover { opacity: 0.88 !important; transform: translateY(-1px) !important; }
.stButton > button:active { transform: translateY(0) !important; }

/* ── Alert banners ── */
.banner {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 14px 18px;
    border-radius: 12px;
    font-size: 0.88rem;
    margin-top: 16px;
    line-height: 1.5;
}
.banner.success {
    background: #041a10;
    border: 1px solid #0d4a28;
    color: #34d994;
}
.banner.error {
    background: #180808;
    border: 1px solid #4a1212;
    color: #f06060;
}
.banner .icon { font-size: 1.1rem; flex-shrink: 0; margin-top: 1px; }
.banner b { color: inherit; display: block; margin-bottom: 2px; }

/* ── Account card (details view) ── */
.acct-card {
    border-radius: 18px;
    padding: 28px;
    background: linear-gradient(135deg, #120d2a 0%, #0a1a18 100%);
    border: 1px solid #2a1f50;
    margin-bottom: 20px;
    position: relative;
    overflow: hidden;
}
.acct-card::before {
    content: '◆';
    position: absolute;
    right: 20px; top: 20px;
    font-size: 4rem;
    color: rgba(108,71,255,0.07);
    pointer-events: none;
}
.acct-name {
    font-size: 1.5rem;
    font-weight: 800;
    color: #eef0ff;
    letter-spacing: -0.4px;
    margin-bottom: 4px;
}
.acct-email { font-size: 0.82rem; color: #4a5070; margin-bottom: 24px; }
.acct-no {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    letter-spacing: 0.15em;
    color: #6c47ff;
    background: #100c28;
    display: inline-block;
    padding: 4px 10px;
    border-radius: 6px;
    border: 1px solid #2a1f50;
    margin-bottom: 20px;
}
.balance-row { display: flex; align-items: baseline; gap: 6px; }
.balance-label { font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.1em; color: #3a4060; }
.balance-val {
    font-family: 'JetBrains Mono', monospace;
    font-size: 2rem;
    font-weight: 500;
    color: #00d4aa;
}

/* ── Info row ── */
.info-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-top: 16px; }
.info-item {
    background: #0c0f1f;
    border: 1px solid #141830;
    border-radius: 10px;
    padding: 14px 16px;
}
.info-item .lbl { font-size: 0.7rem; letter-spacing: 0.08em; text-transform: uppercase; color: #3a4060; margin-bottom: 4px; }
.info-item .val { font-size: 0.92rem; font-weight: 600; color: #c4c8f0; }

/* ── Divider ── */
hr { border-color: #141830 !important; margin: 24px 0 !important; }

/* ── Checkbox ── */
.stCheckbox label { color: #5a6080 !important; font-size: 0.85rem !important; }
.stCheckbox input[type="checkbox"]:checked { accent-color: #6c47ff; }

/* ── Delete zone ── */
.danger-zone {
    background: #120808;
    border: 1px solid #3a1010;
    border-radius: 16px;
    padding: 22px 24px;
    margin-bottom: 16px;
}
.danger-zone .dz-title {
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #f06060;
    font-weight: 700;
    margin-bottom: 6px;
}
.danger-zone .dz-desc { font-size: 0.85rem; color: #5a3030; }

/* ── Sidebar footer ── */
.sb-footer {
    position: absolute;
    bottom: 0; left: 0; right: 0;
    padding: 16px 20px;
    border-top: 1px solid #141830;
    font-size: 0.7rem;
    color: #2a3050;
    letter-spacing: 0.04em;
}

/* account-created highlight box */
.acc-created {
    background: #041a10;
    border: 1px solid #0d4a28;
    border-radius: 14px;
    padding: 22px 24px;
    margin-top: 16px;
}
.acc-created .title { font-size: 0.7rem; letter-spacing: 0.1em; text-transform: uppercase; color: #1a8a54; margin-bottom: 8px; }
.acc-created .acc-val {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.25rem;
    color: #00d4aa;
    letter-spacing: 0.12em;
    word-break: break-all;
}
.acc-created .note { font-size: 0.75rem; color: #2a6040; margin-top: 8px; }
</style>
""", unsafe_allow_html=True)

# ── Bank logic ────────────────────────────────────────────────────────────────
DATABASE = "database.json"

def load_data():
    if Path(DATABASE).exists():
        with open(DATABASE) as f:
            return json.loads(f.read())
    return []

def save_data(data):
    with open(DATABASE, "w") as f:
        f.write(json.dumps(data))

def generate_account_no():
    alpha = random.choices(string.ascii_letters, k=8)
    num = random.choices(string.digits, k=4)
    acc = alpha + num
    random.shuffle(acc)
    return "".join(acc)

def find_user(data, accno, pin):
    try:
        matches = [u for u in data if u["AccountNO."] == accno and u["pin"] == int(pin)]
        return matches[0] if matches else None
    except (ValueError, TypeError):
        return None

def banner(kind, title, body=""):
    icon = "✦" if kind == "success" else "⚠"
    return f"""
    <div class="banner {kind}">
      <span class="icon">{icon}</span>
      <div><b>{title}</b>{body}</div>
    </div>"""

data = load_data()
total_users = len(data)
total_balance = sum(u.get("balance", 0) for u in data)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
      <div class="logo-mark">💠</div>
      <h2>NexVault</h2>
      <p>Digital Banking · v2.0</p>
    </div>
    """, unsafe_allow_html=True)

    NAV = {
        "🪪  Create Account":   "create",
        "💰  Deposit":          "deposit",
        "🏧  Withdraw":         "withdraw",
        "📋  Account Details":  "details",
        "✏️  Update Details":   "update",
        "🗑️  Delete Account":   "delete",
    }
    choice = st.radio("", list(NAV.keys()), label_visibility="collapsed")
    page = NAV[choice]

    st.markdown(f"""
    <div class="sb-footer">
      {total_users} accounts &nbsp;·&nbsp; ₹{total_balance:,} total deposits
    </div>
    """, unsafe_allow_html=True)

# ── Main area ─────────────────────────────────────────────────────────────────
# Hero
st.markdown(f"""
<div class="hero">
  <div class="hero-tag"><span class="dot"></span>Live &nbsp;·&nbsp; All systems operational</div>
  <h1>Your money,<br><span>intelligently vaulted.</span></h1>
  <p>Manage deposits, withdrawals and account settings in one secure place.</p>
  <div class="hero-stats">
    <div>
      <div class="hero-stat-val">{total_users}</div>
      <div class="hero-stat-label">Accounts</div>
    </div>
    <div>
      <div class="hero-stat-val">₹{total_balance:,}</div>
      <div class="hero-stat-label">Total deposits</div>
    </div>
    <div>
      <div class="hero-stat-val">256-bit</div>
      <div class="hero-stat-label">Encryption</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# PAGE: Create Account
# ─────────────────────────────────────────────────────────────────────────────
if page == "create":
    st.markdown("""
    <div class="section-head">
      <div class="icon-pill violet">🪪</div>
      <div><h2>Open an account</h2><p>Takes less than a minute</p></div>
    </div>
    """, unsafe_allow_html=True)

    col_l, col_r = st.columns([1.6, 1])
    with col_l:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        name  = st.text_input("Full name")
        age   = st.number_input("Age", min_value=0, max_value=120, step=1, value=18)
        email = st.text_input("Email address")
        pin   = st.text_input("4-digit PIN", type="password", max_chars=4, placeholder="••••")
        clicked = st.button("Open account →")
        st.markdown('</div>', unsafe_allow_html=True)

        if clicked:
            if not all([name.strip(), email.strip(), pin]):
                st.markdown(banner("error", "Missing fields", " — please fill in all fields."), unsafe_allow_html=True)
            elif age < 12:
                st.markdown(banner("error", "Age restriction", " — must be 12 or older to open an account."), unsafe_allow_html=True)
            elif not pin.isdigit() or len(pin) != 4:
                st.markdown(banner("error", "Invalid PIN", " — PIN must be exactly 4 digits."), unsafe_allow_html=True)
            else:
                acc_no = generate_account_no()
                data.append({"name": name.strip(), "age": int(age), "email": email.strip(),
                              "AccountNO.": acc_no, "pin": int(pin), "balance": 0})
                save_data(data)
                st.markdown(f"""
                <div class="acc-created">
                  <div class="title">Account created</div>
                  <div class="acc-val">{acc_no}</div>
                  <div class="note">Save this account number — you'll need it to log in.</div>
                </div>
                """, unsafe_allow_html=True)

    with col_r:
        st.markdown("""
        <div class="glass-card" style="height:100%">
          <div style="font-size:0.7rem;letter-spacing:.08em;text-transform:uppercase;color:#3a4060;margin-bottom:14px">Eligibility</div>
          <div style="display:flex;flex-direction:column;gap:10px">
            <div style="display:flex;gap:10px;align-items:flex-start">
              <span style="color:#00d4aa;font-size:1rem;margin-top:1px">✦</span>
              <span style="font-size:0.83rem;color:#5a6080">Must be 12 years or older</span>
            </div>
            <div style="display:flex;gap:10px;align-items:flex-start">
              <span style="color:#00d4aa;font-size:1rem;margin-top:1px">✦</span>
              <span style="font-size:0.83rem;color:#5a6080">Valid email address required</span>
            </div>
            <div style="display:flex;gap:10px;align-items:flex-start">
              <span style="color:#00d4aa;font-size:1rem;margin-top:1px">✦</span>
              <span style="font-size:0.83rem;color:#5a6080">Choose a memorable 4-digit PIN</span>
            </div>
            <div style="display:flex;gap:10px;align-items:flex-start">
              <span style="color:#00d4aa;font-size:1rem;margin-top:1px">✦</span>
              <span style="font-size:0.83rem;color:#5a6080">Account number is auto-generated</span>
            </div>
          </div>
          <div style="margin-top:24px;padding-top:16px;border-top:1px solid #141830;font-size:0.72rem;color:#2a3050">
            Data stored locally on your device.
          </div>
        </div>
        """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# PAGE: Deposit
# ─────────────────────────────────────────────────────────────────────────────
elif page == "deposit":
    st.markdown("""
    <div class="section-head">
      <div class="icon-pill teal">💰</div>
      <div><h2>Deposit funds</h2><p>Add money to your account instantly</p></div>
    </div>
    """, unsafe_allow_html=True)

    col_l, col_r = st.columns([1.4, 1])
    with col_l:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        accno  = st.text_input("Account number")
        pin    = st.text_input("PIN", type="password", max_chars=4, placeholder="••••")
        amount = st.number_input("Amount (₹)", min_value=1, step=100, value=1000)
        clicked = st.button("Deposit funds →")
        st.markdown('</div>', unsafe_allow_html=True)

        if clicked:
            if not accno or not pin:
                st.markdown(banner("error", "Missing credentials", " — account number and PIN are required."), unsafe_allow_html=True)
            else:
                user = find_user(data, accno, pin)
                if not user:
                    st.markdown(banner("error", "Not found", " — invalid account number or PIN."), unsafe_allow_html=True)
                else:
                    user["balance"] += int(amount)
                    save_data(data)
                    st.markdown(banner("success", f"₹{int(amount):,} deposited", f"<br><span style='font-size:0.8rem;opacity:0.7'>New balance: ₹{user['balance']:,}</span>"), unsafe_allow_html=True)

    with col_r:
        st.markdown("""
        <div class="glass-card">
          <div style="font-size:0.7rem;letter-spacing:.08em;text-transform:uppercase;color:#3a4060;margin-bottom:12px">Quick amounts</div>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px">
        """ + "".join([
            f'<div style="background:#0a0d1a;border:1px solid #1e2240;border-radius:8px;padding:10px 14px;text-align:center;font-family:\'JetBrains Mono\',monospace;font-size:0.82rem;color:#5a6080">₹{v:,}</div>'
            for v in [500, 1000, 2000, 5000, 10000, 25000]
        ]) + """
          </div>
          <div style="margin-top:16px;font-size:0.75rem;color:#2a3050">
            Enter any custom amount in the field.
          </div>
        </div>
        """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# PAGE: Withdraw
# ─────────────────────────────────────────────────────────────────────────────
elif page == "withdraw":
    st.markdown("""
    <div class="section-head">
      <div class="icon-pill amber">🏧</div>
      <div><h2>Withdraw funds</h2><p>Pull cash out of your account</p></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        accno = st.text_input("Account number")
        pin   = st.text_input("PIN", type="password", max_chars=4, placeholder="••••")
    with col2:
        amount = st.number_input("Amount to withdraw (₹)", min_value=1, step=100, value=500)
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)

    clicked = st.button("Withdraw →")
    st.markdown('</div>', unsafe_allow_html=True)

    if clicked:
        if not accno or not pin:
            st.markdown(banner("error", "Missing credentials", " — account number and PIN are required."), unsafe_allow_html=True)
        else:
            user = find_user(data, accno, pin)
            if not user:
                st.markdown(banner("error", "Not found", " — invalid account number or PIN."), unsafe_allow_html=True)
            elif int(amount) > user["balance"]:
                st.markdown(banner("error", "Insufficient balance", f" — you only have ₹{user['balance']:,} available."), unsafe_allow_html=True)
            else:
                user["balance"] -= int(amount)
                save_data(data)
                st.markdown(banner("success", f"₹{int(amount):,} withdrawn", f"<br><span style='font-size:0.8rem;opacity:0.7'>Remaining balance: ₹{user['balance']:,}</span>"), unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# PAGE: Account Details
# ─────────────────────────────────────────────────────────────────────────────
elif page == "details":
    st.markdown("""
    <div class="section-head">
      <div class="icon-pill blue">📋</div>
      <div><h2>Account details</h2><p>View your full account profile</p></div>
    </div>
    """, unsafe_allow_html=True)

    col_l, col_r = st.columns([1, 1.2])
    with col_l:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        accno = st.text_input("Account number")
        pin   = st.text_input("PIN", type="password", max_chars=4, placeholder="••••")
        clicked = st.button("View account →")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_r:
        if "view_user" in st.session_state:
            u = st.session_state["view_user"]
            initials = "".join(p[0].upper() for p in u["name"].split()[:2])
            st.markdown(f"""
            <div class="acct-card">
              <div style="display:flex;align-items:center;gap:14px;margin-bottom:16px">
                <div style="width:52px;height:52px;border-radius:14px;background:linear-gradient(135deg,#6c47ff,#00d4aa);
                  display:flex;align-items:center;justify-content:center;font-size:1.2rem;font-weight:800;color:#fff">
                  {initials}
                </div>
                <div>
                  <div class="acct-name">{u['name']}</div>
                  <div class="acct-email">{u['email']}</div>
                </div>
              </div>
              <div class="acct-no">{u['AccountNO.']}</div>
              <div class="balance-row">
                <div class="balance-label">Balance</div>
                <div class="balance-val">₹{u['balance']:,}</div>
              </div>
              <div class="info-grid">
                <div class="info-item"><div class="lbl">Age</div><div class="val">{u['age']} yrs</div></div>
                <div class="info-item"><div class="lbl">Status</div><div class="val" style="color:#00d4aa">● Active</div></div>
              </div>
            </div>
            """, unsafe_allow_html=True)

    if clicked:
        if not accno or not pin:
            with col_l:
                st.markdown(banner("error", "Missing credentials"), unsafe_allow_html=True)
        else:
            user = find_user(data, accno, pin)
            if not user:
                with col_l:
                    st.markdown(banner("error", "Not found", " — check your account number and PIN."), unsafe_allow_html=True)
            else:
                st.session_state["view_user"] = user
                st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
# PAGE: Update Details
# ─────────────────────────────────────────────────────────────────────────────
elif page == "update":
    st.markdown("""
    <div class="section-head">
      <div class="icon-pill violet">✏️</div>
      <div><h2>Update details</h2><p>Edit your name, email or PIN</p></div>
    </div>
    """, unsafe_allow_html=True)

    if "update_user" not in st.session_state:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("<div style='font-size:0.78rem;color:#3a4060;margin-bottom:16px'>Step 1 — verify your identity</div>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1: accno = st.text_input("Account number")
        with col2: pin   = st.text_input("PIN", type="password", max_chars=4, placeholder="••••")
        clicked = st.button("Verify identity →")
        st.markdown('</div>', unsafe_allow_html=True)
        if clicked:
            user = find_user(data, accno, pin)
            if not user:
                st.markdown(banner("error", "Not found", " — invalid credentials."), unsafe_allow_html=True)
            else:
                st.session_state["update_user"] = user
                st.rerun()
    else:
        user = st.session_state["update_user"]
        st.markdown(banner("success", f"Verified — editing {user['name']}'s account"), unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("<div style='font-size:0.78rem;color:#3a4060;margin-bottom:16px'>Step 2 — make your changes</div>", unsafe_allow_html=True)
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1: new_name  = st.text_input("Name",  value=user["name"])
        with col2: new_email = st.text_input("Email", value=user["email"])
        with col3: new_pin   = st.text_input("New PIN (blank = keep)", type="password", max_chars=4, placeholder="••••")
        col_a, col_b = st.columns([1, 1])
        with col_a: save = st.button("Save changes →")
        with col_b: cancel = st.button("Cancel")
        st.markdown('</div>', unsafe_allow_html=True)

        if cancel:
            del st.session_state["update_user"]
            st.rerun()
        if save:
            if new_pin and (not new_pin.isdigit() or len(new_pin) != 4):
                st.markdown(banner("error", "Invalid PIN", " — must be exactly 4 digits."), unsafe_allow_html=True)
            else:
                user["name"]  = new_name.strip() or user["name"]
                user["email"] = new_email.strip() or user["email"]
                if new_pin: user["pin"] = int(new_pin)
                save_data(data)
                del st.session_state["update_user"]
                st.markdown(banner("success", "Details updated successfully"), unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# PAGE: Delete Account
# ─────────────────────────────────────────────────────────────────────────────
elif page == "delete":
    st.markdown("""
    <div class="section-head">
      <div class="icon-pill red">🗑️</div>
      <div><h2>Close account</h2><p>This action cannot be undone</p></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="danger-zone">
      <div class="dz-title">⚠ Danger zone</div>
      <div class="dz-desc">Closing your account will erase all your data permanently. Your balance will be forfeited if not withdrawn first.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1: accno = st.text_input("Account number")
    with col2: pin   = st.text_input("PIN", type="password", max_chars=4, placeholder="••••")
    confirm = st.checkbox("I understand this is permanent and cannot be reversed.")
    clicked = st.button("Close account permanently →")
    st.markdown('</div>', unsafe_allow_html=True)

    if clicked:
        if not accno or not pin:
            st.markdown(banner("error", "Missing credentials"), unsafe_allow_html=True)
        elif not confirm:
            st.markdown(banner("error", "Confirmation required", " — please tick the checkbox."), unsafe_allow_html=True)
        else:
            user = find_user(data, accno, pin)
            if not user:
                st.markdown(banner("error", "Not found", " — invalid account number or PIN."), unsafe_allow_html=True)
            else:
                data.remove(user)
                save_data(data)
                st.markdown(banner("success", "Account closed", " — all data has been permanently deleted."), unsafe_allow_html=True)