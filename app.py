import html
from urllib.parse import quote_plus
import streamlit as st

st.set_page_config(page_title="Price Basket", page_icon="🛒", layout="wide")

# category, item, brand, pack, qty, paid price, unit, kg/L quantity, SS, FP, CS
ITEMS = [
    ("Fruits", "Blackberries", "Any brand", "125 g", 1, 7.45, "kg", .125, 6.95, 6.95, 6.95),
    ("Fruits", "Bananas", "Any brand", "1 kg equivalent", 1, 3.53, "kg", 1, 3.48, 3.64, 3.60),
    ("Fruits", "Strawberries", "Any brand", "250 g equivalent", 1, 8.00, "kg", .25, 4.95, 5.95, 9.81),
    ("Vegetables", "Green Chillies", "Any brand", "200 g equivalent", 1, 1.73, "kg", .2, 1.50, 1.50, 2.67),
    ("Vegetables", "Cabbage", "Any brand", "1 kg equivalent", 1, 2.42, "kg", 1, 2.15, 3.25, 4.30),
    ("Breakfast", "Butter", "Any brand", "200 g equivalent", 1, 5.87, "kg", .2, 2.60, 5.75, 6.34),
    ("Vegetables", "Baby Corn", "Fresh produce", "100 g equivalent", 1, 1.70, "kg", .1, 1.38, 1.38, 1.90),
    ("Vegetables", "Corn", "Any brand", "550 g equivalent", 1, 1.95, "kg", .55, 2.75, 1.65, 4.02),
    ("Vegetables", "Onions", "Any brand", "700 g equivalent", 1, 2.04, "kg", .7, 1.30, 1.35, 2.60),
    ("Vegetables", "Potatoes", "Any brand", "1 kg equivalent", 1, 1.65, "kg", 1, 1.25, 1.50, 3.95),
    ("Breakfast", "Ham", "Any brand", "100 g equivalent", 1, 5.50, "kg", .1, 1.78, 1.66, 7.45),
    ("Breakfast", "Sausages", "Johnsonville Smoked Chicken Cheese", "360 g", 1, 9.67, "kg", .36, 9.90, 9.90, 12.65),
    ("Vegetables", "Kai Lan", "Any brand", "200 g equivalent", 1, 1.60, "kg", .2, 1.40, 1.20, 2.50),
    ("Vegetables", "Radish", "Fresh produce", "400 g equivalent", 1, 1.41, "kg", .4, .80, 1.45, 1.80),
    ("Vegetables", "Brown Shimeji Mushrooms", "Fresh produce", "150 g equivalent", 1, .90, "kg", .15, .90, 2.04, 3.00),
    ("Vegetables", "Garlic", "Any brand", "200 g equivalent", 1, 1.16, "kg", .2, 1.15, 2.10, 1.32),
    ("Vegetables", "Green Beans", "Fresh produce", "150 g equivalent", 1, 1.46, "kg", .15, .51, 1.23, 2.50),
    ("Rice, Noodles & Pasta", "Rice", "Royal Umbrella", "5 kg", 1, 16.60, "kg", 5, 16.25, 16.60, 16.60),
    ("Rice, Noodles & Pasta", "Indomie", "Any flavour", "5 x 85 g", 1, 2.60, "kg", .425, 2.15, 2.62, 2.80),
    ("Breakfast", "Eggs", "Any brand", "15 eggs equivalent", 1, 5.14, "item", 15, 3.90, 4.65, 4.80),
    ("Vegetables", "Broccoli", "Any brand", "280 g equivalent", 1, 3.17, "kg", .28, 1.34, 2.55, 2.66),
    ("Vegetables", "Xiao Bai Cai", "Any brand", "200 g", 1, 1.40, "kg", .2, 1.40, 1.50, 2.00),
    ("Vegetables", "Gourd", "Fresh produce", "400 g equivalent", 1, 1.75, "kg", .4, 2.50, 2.17, 2.76),
    ("Meat, Poultry, Seafood & Frozen", "Chicken", "Frozen chicken", "1 kg equivalent", 1, 9.76, "kg", 1, 6.95, 7.95, 6.50),
    ("Meat, Poultry, Seafood & Frozen", "Pork", "Frozen minced pork", "500 g", 1, 5.47, "kg", .5, 8.10, 4.95, 5.00),
    ("Meat, Poultry, Seafood & Frozen", "Beef", "Frozen minced beef", "500 g", 1, 6.90, "kg", .5, 6.00, 7.05, 12.10),
    ("Meat, Poultry, Seafood & Frozen", "Fish", "Fish fillet", "500 g equivalent", 1, 7.20, "kg", .5, 4.33, 15.12, 13.50),
    ("Meat, Poultry, Seafood & Frozen", "Prawns", "Frozen prawns", "700 g equivalent", 1, 21.72, "kg", .7, 14.95, 19.95, 11.83),
    ("Vegetables", "Carrots", "Any brand", "500 g", 1, 1.00, "kg", .5, .94, .95, 1.90),
    ("Breakfast", "Loaf Bread", "Any brand", "400 g", 1, 4.10, "kg", .4, 2.50, 2.50, 2.50),
    ("Breakfast", "Fresh Milk", "Any brand", "946 ml", 2, 3.63, "L", .946, 3.35, 3.35, 3.35),
    ("Breakfast", "Smoked Salmon", "100 g comparable pack", "100 g", 1, 6.50, "kg", .1, 5.99, 7.10, 8.90),
    ("Beverages", "100PLUS", "Active", "12 x 300 ml", 1, 9.47, "L", 3.6, 8.95, 9.47, 9.95),
    ("Fruits", "Apples", "Any brand", "650 g equivalent", 1, 3.67, "kg", .65, 4.26, 2.80, 3.94),
    ("Fruits", "Oranges", "Any brand", "800 g equivalent", 1, 5.76, "kg", .8, 6.32, 3.95, 7.95),
]

# ---------------------------------------------------------------- config ----
# key, display name, index into an ITEMS row
STORES = (
    ("ss", "Sheng Siong", 8),
    ("cs", "Cold Storage", 10),
    ("fp", "NTUC FairPrice", 9),
    ("rm", "RedMart", 5),
)
DELIVERY = {
    "ss": ("S$6", "Free from S$100"),
    "cs": ("S$6.99", "Free from S$80"),
    "fp": ("S$5 + S$3.99 service", "Free from S$59"),
    "rm": ("From S$3.99", "Free from S$60 &middot; 6h slot"),
}
# The whole taxonomy lives here: name, default annual spend, default
# achievable saving %, note. Add, remove or rename freely -- the nav, the
# cards and the totals all derive from this tuple. DATA_CATEGORY below names
# the one category that has a real price table behind it.
SAVINGS_CATEGORIES = (
    ("Food", 24000, 12, "Groceries plus dining and delivery. The only category with verified prices below."),
    ("Health", 8000, 10, "Insurance, medical, dental, fitness. Savings come from policy review, not daily choices."),
    ("Travel", 15000, 8, "Large and lumpy. Savings come from timing and fare class, not loyalty."),
    ("Culture", 4000, 15, "Entertainment, subscriptions, events. High percentage, small base."),
    ("Education", 6000, 8, "Courses, enrichment, tuition. Priced by provider; little room to shop around."),
    ("Parenting", 9000, 10, "Childcare, gear, activities. Gear is comparable; childcare mostly is not."),
)
DATA_CATEGORY = "Food"
# Per-item search URLs. Sheng Siong has no public search endpoint I could
# verify, so it falls back to a scoped web search rather than a dead link.
LINK_TEMPLATES = {
    "ss": "https://www.google.com/search?q=sheng+siong+{q}",
    "cs": "https://coldstorage.com.sg/search?q={q}",
    "fp": "https://www.fairprice.com.sg/search?query={q}",
    "rm": "https://www.lazada.sg/catalog/?q={q}",
}

BASKET_ANNUAL = sum(max(0, r[5] - r[8]) * 52 for r in ITEMS)


def sgd(value, dp=2):
    return f"S${value:,.{dp}f}"


st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap');
:root{color-scheme:light}
.stApp{background:#f6f8fb;color:#17202a}
html,body,[class*=css]{font-family:'DM Sans',system-ui,sans-serif}
.block-container{max-width:1500px;padding:1.6rem 2rem 3rem}
#MainMenu,footer,header{visibility:hidden}

.hero{align-items:center;display:flex;gap:12px;margin-bottom:14px}
.mark{align-items:center;background:linear-gradient(135deg,#27835d,#185f43);border-radius:12px;color:#fff;display:flex;font-size:22px;height:44px;justify-content:center;width:44px}
.hero h1{font-size:29px;letter-spacing:-.8px;margin:0}
.hero p{color:#718078;font-size:13px;margin:3px 0 0}

/* category nav pills */
div[data-testid="stPills"]{margin:0 0 4px}
div[data-testid="stPills"] button{border-radius:999px!important;font-size:13.5px!important;font-weight:600!important;padding:6px 16px!important}

.band{background:linear-gradient(135deg,#176b49,#27835d);border-radius:14px;color:#fff;display:flex;align-items:flex-end;justify-content:space-between;gap:16px;margin:6px 0 12px;padding:16px 20px}
.band span{display:block;font-size:11px;font-weight:700;letter-spacing:.08em;opacity:.85;text-transform:uppercase}
.band strong{display:block;font-size:38px;letter-spacing:-1.5px;line-height:1.05;margin-top:4px}
.band small{font-size:11.5px;opacity:.85;text-align:right;line-height:1.5}

.cards{display:grid;gap:12px;grid-template-columns:repeat(auto-fit,minmax(212px,1fr));margin:0 0 12px}
.card{background:#fff;border:1px solid #e4eae6;border-radius:12px;padding:13px 15px}
.card.lead{border-color:#bcdccb;box-shadow:0 4px 14px rgba(22,50,37,.06)}
.card h3{color:#203128;font-size:13.5px;font-weight:700;margin:0 0 9px}
.card .big{color:#176b49;font-size:24px;font-weight:700;letter-spacing:-.7px}
.card .sub{color:#8a948e;font-size:11px;margin-top:1px}
.kv{border-top:1px solid #eef2f0;display:flex;justify-content:space-between;font-size:11.5px;margin-top:9px;padding-top:7px}
.kv i{color:#75817b;font-style:normal}
.kv b{color:#203128;font-weight:600}
.bar{background:#eef3f0;border-radius:3px;height:5px;margin-top:10px;overflow:hidden}
.bar div{background:linear-gradient(90deg,#27835d,#176b49);height:100%}
.hint{background:#eaf6ef;border-radius:6px;color:#246244;display:inline-block;font-size:10.5px;margin-top:8px;padding:3px 7px}
.why{color:#8a948e;font-size:11.5px;line-height:1.5;margin-top:8px}

.sec{align-items:baseline;display:flex;gap:10px;margin:24px 0 10px}
.sec h2{font-size:19px;letter-spacing:-.4px;margin:0}
.sec p{color:#8a948e;font-size:12px;margin:0}

.tiles{display:grid;gap:10px;grid-template-columns:repeat(4,1fr);margin:12px 0}
.tile{background:#fff;border:1px solid #e4eae6;border-radius:11px;padding:10px 13px}
.tile span{color:#75817b;display:block;font-size:10.5px;font-weight:700;letter-spacing:.06em;text-transform:uppercase}
.tile strong{display:block;font-size:19px;letter-spacing:-.5px;margin-top:2px}
.tile small{color:#8a948e;display:block;font-size:10.5px;margin-top:1px}
.tile.win{background:#eaf6ef;border-color:#bcdccb}
.tile.win strong,.tile.win small{color:#176b49}

.delivery{display:grid;gap:10px;grid-template-columns:repeat(4,1fr);margin:0 0 12px}
.dcard{background:#fff;border:1px dashed #dfe7e2;border-radius:10px;font-size:12px;padding:9px 12px}
.dcard b{color:#526059;display:block;font-size:10.5px;font-weight:700;letter-spacing:.06em;margin-bottom:3px;text-transform:uppercase}
.dcard em{color:#8a948e;display:block;font-size:11px;font-style:normal;margin-top:2px}

.shell{background:#fff;border:1px solid #e4eae6;border-radius:12px;box-shadow:0 6px 20px rgba(22,50,37,.05);overflow:auto}
.t{border-collapse:separate;border-spacing:0;font-size:13px;min-width:760px;width:100%}
.t thead th{background:#f5f8f6;border-bottom:1px solid #dfe7e2;color:#526059;font-size:11px;font-weight:700;letter-spacing:.06em;padding:10px;position:sticky;text-align:right;text-transform:uppercase;top:0;z-index:3}
.t thead th.itemh{left:0;text-align:left;z-index:4}
.t thead th.savh{background:#eaf3ed;color:#246244}
.t thead th em{color:#9aa49e;display:block;font-size:9.5px;font-style:normal;font-weight:400;letter-spacing:.02em;text-transform:none}
.t td{border-bottom:1px solid #edf1ee;padding:8px 10px;vertical-align:middle}
.t tbody tr:last-child td{border-bottom:0}
.catrow td{background:#f3f7f4;color:#27835d;font-size:10.5px;font-weight:700;letter-spacing:.09em;padding:6px 10px;text-transform:uppercase}
.t td.item{background:#fff;font-weight:600;left:0;min-width:180px;position:sticky;z-index:2}
.t td.item em{color:#9aa49e;display:block;font-size:10.5px;font-style:normal;font-weight:400;margin-top:1px}
.t tbody tr:hover td,.t tbody tr:hover td.item{background:#fbfdfc}
.pc{text-align:right;white-space:nowrap}
.pc a{color:inherit;display:block;padding:1px 0;text-decoration:none}
.pc a:hover .p{text-decoration:underline}
.pc .p{font-size:13.5px;font-weight:600}
.pc .u{color:#9aa49e;font-size:10.5px;margin-top:1px}
.pc.best{background:#eaf6ef}
.pc.best .p{color:#126b48;font-weight:700}
.pc.best .u{color:#5f9179}
.pc.miss{color:#c2c9c5;text-align:right}
.sv{background:#f7fbf9;color:#176b49;font-weight:700;text-align:right;white-space:nowrap}
.sv.zero{color:#c2c9c5;font-weight:400}
.note{color:#75817b;font-size:12px;line-height:1.6;margin:10px 2px}
.swipe-note{color:#8a948e;display:none;font-size:11px;margin:6px 2px;text-align:right}
.empty{background:#fff;border:1px dashed #dfe7e2;border-radius:12px;color:#8a948e;font-size:13px;line-height:1.6;padding:22px}
.empty b{color:#203128;display:block;font-size:14px;margin-bottom:5px}

@media(max-width:760px){
  .block-container{padding:.7rem .5rem 1.6rem}
  .hero{margin:0 .2rem 10px}.hero h1{font-size:23px}.hero p{font-size:11.5px}
  .mark{font-size:19px;height:38px;width:38px}
  .band{border-radius:11px;flex-direction:column;align-items:flex-start;gap:6px;padding:13px 15px}
  .band strong{font-size:31px}.band small{text-align:left}
  .cards{grid-template-columns:repeat(2,1fr)}
  .delivery,.tiles{grid-template-columns:repeat(2,1fr)}
  .sec{margin:18px 0 8px}.sec h2{font-size:17px}
  .t{font-size:12px;min-width:640px}
  .t td{padding:7px 8px}.t thead th{padding:8px}
  .t td.item{min-width:126px}
  .pc .p{font-size:12.5px}
  .swipe-note{display:block}
}
</style>
<div class="hero"><div class="mark">&#128722;</div><div><h1>Price Basket</h1>
<p>Lifestyle spend, by category &mdash; and what is realistically recoverable from each.</p></div></div>
""", unsafe_allow_html=True)

# --------------------------------------------------- state + category nav ----
# Canonical values live under v_* keys so they survive a category switch even
# though the input widgets are only rendered for the category being viewed.
for index, (_, default_spend, default_pct, _note) in enumerate(SAVINGS_CATEGORIES):
    st.session_state.setdefault(f"v_spend_{index}", default_spend)
    st.session_state.setdefault(f"v_pct_{index}", default_pct)

VIEWS = ("Overview", *[c[0] for c in SAVINGS_CATEGORIES])
if hasattr(st, "pills"):
    view = st.pills("Category", VIEWS, default="Overview", label_visibility="collapsed")
else:  # streamlit < 1.40 fallback
    view = st.radio("Category", VIEWS, horizontal=True, label_visibility="collapsed")
view = view or "Overview"


def category_rows():
    out = []
    for index, (name, _, _, note) in enumerate(SAVINGS_CATEGORIES):
        spend = st.session_state[f"v_spend_{index}"]
        pct = st.session_state[f"v_pct_{index}"]
        out.append({
            "index": index, "name": name, "note": note,
            "spend": spend, "pct": pct, "saving": spend * pct / 100,
        })
    return out


def card_html(row, total, lead=False):
    share = (row["saving"] / total * 100) if total else 0
    hint = ""
    if row["name"] == DATA_CATEGORY:
        hint = f'<div class="hint">Verified grocery basket alone implies {sgd(BASKET_ANNUAL, 0)}/yr</div>'
    return (
        f'<div class="card{" lead" if lead else ""}"><h3>{html.escape(row["name"])}</h3>'
        f'<div class="big">{sgd(row["saving"], 0)}</div>'
        f'<div class="sub">recoverable per year</div>'
        f'<div class="kv"><i>Annual spend</i><b>{sgd(row["spend"], 0)}</b></div>'
        f'<div class="kv"><i>Saving rate</i><b>{row["pct"]}%</b></div>'
        f'<div class="kv"><i>Effective spend</i><b>{sgd(row["spend"] - row["saving"], 0)}</b></div>'
        f'<div class="bar"><div style="width:{share:.0f}%"></div></div>'
        f'<div class="sub">{share:.0f}% of total opportunity</div>{hint}</div>'
    )


rows = category_rows()
total_spend = sum(r["spend"] for r in rows)
total_saving = sum(r["saving"] for r in rows)

# ------------------------------------------------------------- overview ----
if view == "Overview":
    biggest = max(rows, key=lambda r: r["saving"])["name"] if total_saving else "&mdash;"
    st.markdown(
        f'<div class="band"><div><span>Total recoverable per year</span>'
        f'<strong>{sgd(total_saving, 0)}</strong></div>'
        f'<small>on {sgd(total_spend, 0)} of tracked annual spend<br>'
        f'biggest single pool: <b>{html.escape(biggest)}</b></small></div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="cards">' + "".join(card_html(r, total_saving) for r in rows) + "</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="note">Pick a category above to edit its assumptions. '
        f"Only {html.escape(DATA_CATEGORY)} is backed by verified like-for-like "
        "prices today; every other category is your estimate until a data source "
        "is plugged in.</div>",
        unsafe_allow_html=True,
    )

# ------------------------------------------------------ category detail ----
else:
    active = next(r for r in rows if r["name"] == view)
    index = active["index"]
    share = (active["saving"] / total_saving * 100) if total_saving else 0
    st.markdown(
        f'<div class="band"><div><span>{html.escape(view)} &mdash; recoverable per year</span>'
        f'<strong>{sgd(active["saving"], 0)}</strong></div>'
        f'<small>{share:.0f}% of your total opportunity<br>'
        f'{sgd(active["spend"] - active["saving"], 0)} effective spend after savings</small></div>',
        unsafe_allow_html=True,
    )
    edit_spend, edit_pct = st.columns([1, 1.6])
    with edit_spend:
        st.session_state[f"v_spend_{index}"] = st.number_input(
            "Annual spend (S$)", 0, 300000,
            st.session_state[f"v_spend_{index}"], 500, key=f"w_spend_{index}",
        )
    with edit_pct:
        st.session_state[f"v_pct_{index}"] = st.slider(
            "Achievable saving %", 0, 50,
            st.session_state[f"v_pct_{index}"], 1, key=f"w_pct_{index}",
            help="What you can realistically capture on top of what you already do "
                 "-- not the headline advertised discount.",
        )
    st.markdown(f'<div class="why">{html.escape(active["note"])}</div>', unsafe_allow_html=True)

# ------------------------------------------- grocery price detail (data) ----
if view in ("Overview", DATA_CATEGORY):
    st.markdown(
        '<div class="sec"><h2>Grocery price detail</h2>'
        "<p>The only category with verified like-for-like data</p></div>",
        unsafe_allow_html=True,
    )

    FOOD_GROUPS = ("Breakfast", "Fruits", "Vegetables", "Meat, Poultry, Seafood & Frozen", "Rice, Noodles & Pasta", "Beverages")
    control_group, control_item, control_sort = st.columns([1, 1.25, 1])
    with control_group:
        selected_group = st.selectbox("Food group", ("All groups", *FOOD_GROUPS))
    available_items = [row[1] for row in ITEMS if selected_group == "All groups" or row[0] == selected_group]
    with control_item:
        selected_item = st.selectbox("Item", ("All items", *available_items))
    with control_sort:
        sort_mode = st.selectbox("Sort by", ("Food group", "Biggest savings", "Item name"))

    display_items = [
        row for row in ITEMS
        if (selected_group == "All groups" or row[0] == selected_group)
        and (selected_item == "All items" or row[1] == selected_item)
    ]

    GROUP_ORDER = {name: i for i, name in enumerate(FOOD_GROUPS)}
    ITEM_ORDER = {name: i for i, name in enumerate(("Fresh Milk", "Eggs", "Loaf Bread", "Ham", "Sausages", "Butter", "Smoked Salmon", "Apples", "Oranges", "Bananas", "Blackberries", "Strawberries", "Broccoli", "Cabbage", "Baby Corn", "Corn", "Garlic", "Brown Shimeji Mushrooms", "Carrots", "Green Beans", "Green Chillies", "Radish", "Kai Lan", "Gourd", "Onions", "Potatoes", "Xiao Bai Cai", "Chicken", "Pork", "Beef", "Fish", "Prawns", "Rice", "Indomie", "100PLUS"))}

    def annual_saving(row):
        return max(0, row[5] - row[8]) * 52 if row[5] is not None and row[8] is not None else 0

    if sort_mode == "Biggest savings":
        ordered = sorted(display_items, key=lambda r: (-annual_saving(r), r[1]))
    elif sort_mode == "Item name":
        ordered = sorted(display_items, key=lambda r: r[1])
    else:
        ordered = sorted(display_items, key=lambda r: (GROUP_ORDER.get(r[0], 99), ITEM_ORDER.get(r[1], 99), r[1]))
    show_sections = sort_mode == "Food group"

    if not display_items:
        st.markdown(
            '<div class="empty"><b>Nothing matches that filter</b>'
            "Widen the food group or item selection to see prices.</div>",
            unsafe_allow_html=True,
        )
    else:
        # basket total per store, for the current filter
        totals = {key: sum(r[idx] for r in display_items if r[idx] is not None) for key, _, idx in STORES}
        cheapest_store = min(totals, key=totals.get)

        tiles = '<div class="tiles">'
        for key, label, _ in STORES:
            win = " win" if key == cheapest_store else ""
            delta = totals[key] - totals[cheapest_store]
            foot = "cheapest basket" if key == cheapest_store else f"+{sgd(delta)} vs best"
            tiles += (
                f'<div class="tile{win}"><span>{html.escape(label)}</span>'
                f"<strong>{sgd(totals[key])}</strong><small>{foot}</small></div>"
            )
        st.markdown(tiles + "</div>", unsafe_allow_html=True)

        delivery = '<div class="delivery">'
        for key, label, _ in STORES:
            fee, free = DELIVERY[key]
            delivery += f'<div class="dcard"><b>{html.escape(label)} delivery</b>{fee}<em>{free}</em></div>'
        st.markdown(delivery + "</div>", unsafe_allow_html=True)

        head = '<div class="shell"><table class="t"><thead><tr><th class="itemh">Item</th>'
        for key, label, _ in STORES:
            caption = "you pay now" if key == "rm" else "price &middot; per unit"
            head += f"<th>{html.escape(label)}<em>{caption}</em></th>"
        head += '<th class="savh">Sheng Siong<em>savings / year</em></th></tr></thead><tbody>'

        body = ""
        last_group = None
        for row in ordered:
            group, item, brand, pack, _qty, paid, unit, amount = row[:8]
            store_prices = row[8:]
            if show_sections and group != last_group:
                body += f'<tr class="catrow"><td colspan="6">{html.escape(group)}</td></tr>'
                last_group = group
            price_map = {"ss": store_prices[0], "fp": store_prices[1], "cs": store_prices[2], "rm": paid}
            available = [p for p in price_map.values() if p is not None]
            lowest = min(available) if len(available) >= 2 else None
            search = quote_plus(f"{brand} {item} {pack}")
            unit_label = "each" if unit == "item" else unit
            subtitle = pack if show_sections else f"{group} &middot; {pack}"
            body += f'<tr><td class="item">{html.escape(item)}<em>{subtitle}</em></td>'
            for key, _, _ in STORES:
                price = price_map[key]
                url = LINK_TEMPLATES[key].format(q=search)
                if price is None:
                    body += f'<td class="pc miss"><a href="{url}" target="_blank" rel="noopener">&mdash;</a></td>'
                    continue
                best = " best" if lowest is not None and price == lowest else ""
                body += (
                    f'<td class="pc{best}"><a href="{url}" target="_blank" rel="noopener">'
                    f'<div class="p">{sgd(price)}</div>'
                    f'<div class="u">{sgd(price / amount)}/{unit_label}</div></a></td>'
                )
            saving = annual_saving(row)
            body += f'<td class="sv">{sgd(saving)}</td></tr>' if saving > 0 else '<td class="sv zero">&mdash;</td></tr>'

        st.markdown(
            '<div class="swipe-note">Swipe to compare stores &rarr;</div>'
            + head + body + "</tbody></table></div>"
            '<div class="note">Green marks the cheapest verified price in each row. '
            "RedMart prices are transcribed from your order screenshots and act as "
            "the baseline you currently pay; the savings column is RedMart minus "
            "Sheng Siong, assuming one purchase per item per week. Where an "
            "identical product is unavailable, the closest practical substitute is "
            "normalised to the RedMart quantity. Delivery fees are manually "
            "recorded and carry no capture date.</div>",
            unsafe_allow_html=True,
        )

# ------------------------------------------------- categories without data ----
else:
    st.markdown(
        f'<div class="sec"><h2>{html.escape(view)} detail</h2>'
        "<p>No data source connected yet</p></div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="empty"><b>{html.escape(view)} is an estimate, not measured</b>'
        f"The figure above is your assumption &times; your spend. Nothing here is "
        f"verified against real prices the way the grocery basket is. Plug in a "
        f"data source for this category to replace the estimate with evidence.</div>",
        unsafe_allow_html=True,
    )
