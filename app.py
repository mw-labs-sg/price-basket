import html
import re
from datetime import date, datetime
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
    ("Groceries", 12000, 10, "The only category with verified like-for-like prices. Savings are a real basket comparison, not an estimate."),
    ("Dining out", 15000, 15, "Restaurants, hawker, delivery. Usually the largest recoverable pool, but nothing here is measured yet."),
    ("Health", 8000, 10, "Insurance, medical, dental, fitness. Savings come from policy review, not daily choices."),
    ("Travel", 15000, 8, "Large and lumpy. Savings come from timing and fare class, not loyalty."),
    ("Culture", 4000, 15, "Entertainment, subscriptions, events. High percentage, small base."),
    ("Education", 6000, 8, "Courses, enrichment, tuition. Priced by provider; little room to shop around."),
    ("Parenting", 9000, 10, "Childcare, gear, activities. Gear is comparable; childcare mostly is not."),
)
DATA_CATEGORY = "Groceries"
# Per-item search URLs. Sheng Siong has no public search endpoint I could
# verify, so it falls back to a scoped web search rather than a dead link.
LINK_TEMPLATES = {
    "ss": "https://www.google.com/search?q=sheng+siong+{q}",
    "cs": "https://coldstorage.com.sg/search?q={q}",
    "fp": "https://www.fairprice.com.sg/search?query={q}",
    "rm": "https://www.lazada.sg/catalog/?q={q}",
}

BASKET_ANNUAL = sum(max(0, r[5] - r[8]) * 52 for r in ITEMS)

# ---------------------------------------------------------- dining deals ----
# Hand-checked against published sources on the date below. Dining promos
# expire constantly -- re-check before relying on any single row. Anything
# found with an end date already past was left out (e.g. the DBS/POSB/Maybank/
# OCBC weekend 1-for-1, which ran only to 30 Jun 2026).
DEALS_CATEGORY = "Dining out"
DEALS_CHECKED = "29 Aug 2026"
# name, cost, what you get, coverage, best for, url
DINING_PROGRAMMES = (
    ("Burpple Beyond Lite", "S$49/yr", "1-for-1 on mains, limited redemptions", "500+ restaurants", "Breaks even in 1-2 uses", "https://www.burpple.com/beyond"),
    ("Burpple Beyond Standard", "S$69/yr", "1-for-1 on mains, more redemptions", "500+ restaurants", "Regular casual dining", "https://www.burpple.com/beyond"),
    ("Burpple Beyond Gold", "S$99/yr", "1-for-1, unlimited per merchant", "500+ restaurants", "Best tier if you dine out weekly", "https://www.burpple.com/beyond"),
    ("The Entertainer", "S$80/yr", "1-for-1 dining, spa, attractions", "2,000+ offers", "Hotel dining; one dinner repays it", "https://www.theentertainerme.com/"),
    ("Chope", "Free", "1 Chope-Dollar per S$1; deals to 50% off", "4,000+ restaurants", "Free layer, stacks on everything", "https://www.chope.co/singapore-restaurants"),
    ("Eatigo", "Free", "10-50% off, priced by time slot", "600+ restaurants", "Off-peak flexibility", "https://eatigo.com/sg/singapore/en"),
    ("ShopBack Dine-In", "Free", "5-15% cashback on a linked card", "2,000+ outlets", "Stacks on top of card rebate", "https://www.shopback.sg/guide/how-to/earn-cashback-in-store"),
    ("Fave", "Free", "Prepaid vouchers, up to 20% back", "Chains and local brands", "Places you go repeatedly", "https://myfave.com/"),
)
# card, dining rate, min monthly spend, monthly cap, implied annual ceiling
DINING_CARDS = (
    ("BOC NVMO", "10%", "S$800", "S$25", 300),
    ("Citi Cash Back", "6%", "S$800", "S$80", 960),
    ("Maybank Family & Friends", "6-8%", "S$800-1,600", "S$20-30", 360),
    ("HSBC Live+", "5% (8% new)", "S$600", "S$250/quarter", 1000),
    ("Maybank XL Cashback", "5%", "S$500", "S$80", 960),
    ("OCBC 365", "5%", "S$800-1,600", "S$80-160", 1920),
    ("POSB Everyday", "5%", "S$800", "S$20", 240),
)
# Specific restaurants, cross-checked across two independent guides on the
# date above. name, venue, cuisine/what, was ++, now ++, cards, ends
# "ends" of None means no published end date. Prices are ++ (add ~19.9% for
# service charge and GST).
DINING_RESTAURANTS = (
    ("Plate", "Carlton City Hotel, Tanjong Pagar", "Rotating themed buffets", "S$56-62++", "S$28-31++", "Citi, DBS/POSB, Maybank, OCBC, StanChart", "18 Dec 2026"),
    ("Sun's Cafe", "Hotel Grand Pacific, Bras Basah", "Peranakan and Nyonya", "S$60++", "S$30-32.50++", "DBS/POSB, UOB, HSBC, OCBC, Maybank, Citi", None),
    ("Royale", "Mercure Singapore Bugis", "International buffet", "From S$65++", "From S$32.50++", "DBS/POSB, Maybank, OCBC, Citi, UOB", None),
    ("The Line", "Shangri-La Singapore", "International buffet", "From S$68++", "From S$34++", "HSBC Premier", None),
    ("Racines", "Sofitel Singapore City Centre", "French-Chinese buffet", "S$68-128++", "S$34-64++", "SAFRA members", None),
    ("Crossroads Buffet", "Marriott Tang Plaza", "Weekday lunch buffet", "S$70++", "S$35++", "DBS/POSB", "30 Nov 2026"),
    ("CLOVE", "Swissotel The Stamford", "International buffet", "S$80-130++", "S$40-65++", "OCBC, DBS/POSB, Citi, HSBC, UOB", "31 Oct 2026"),
    ("Cafe Mosaic", "Carlton Hotel, Bras Basah", "Hong Kong dim sum and tze char", "S$62-128++", "S$31++ lunch / S$64++ dinner", "DBS/POSB, Citi, OCBC, UOB", None),
    ("Makan@Jen", "JEN Singapore Orchardgateway", "Weekday buffet", "S$88++", "S$44++", "Not specified", None),
    ("The Landmark", "Village Hotel Bugis", "MUIS halal international", "S$85.90-102.90++", "S$42.95-51.45++", "UOB", None),
    ("Atrium Restaurant", "Holiday Inn Atrium, Outram", "Nyonya halal spread", "S$99-129++", "S$49.50-64.50++", "None; odd groups need DBS/POSB, Citi, UOB", "9 Sep 2026"),
    ("Seasonal Tastes", "The Westin, Marina Bay", "International buffet", "S$98-108++", "S$49-54++", "DBS/POSB, OCBC, UOB, Citi, Maybank, BOC, JCB", "31 Aug 2026"),
)
DEALS_SOURCES = (
    ("1-for-1 buffets, Aug 2026", "https://www.misslobang.com/article/best-1-for-1-buffet-deals-singapore-august-2026"),
    ("Eatbook buffet deals", "https://eatbook.sg/1-for-1-buffet-2026/"),
    ("Dining apps compared", "https://divedeals.sg/blog/best-dining-deals-app-singapore"),
    ("Cashback cards for dining", "https://sethisfy.com/great-cards-for-good-food/"),
    ("MoneySmart dining cards", "https://www.moneysmart.sg/credit-cards/dining"),
    ("Chope bank card promos", "https://www.chope.co/singapore-restaurants/pages/bankcardspromoguide"),
)


def sgd(value, dp=2):
    return f"S${value:,.{dp}f}"


st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap');

/* Dark palette. Every colour is a token so the theme can be retuned in one
   place; .streamlit/config.toml carries the matching widget chrome. */
:root{
  /* Warm charcoal, not green-black -- the cold near-black is what made the
     old palette feel severe. */
  --bg:#181513; --surface:#211d1a; --raised:#2a2522; --border:#38312c;
  --text:#f2ece6; --muted:#bcaea3; --dim:#a3958a;
  /* Apricot is the brand + interactive colour: links, buttons, nav, headings. */
  --accent:#f0a869; --accent-deep:#d98a48; --accent-dim:#8c5c33;
  --soft:rgba(240,168,105,.13); --softer:rgba(240,168,105,.07);
  /* Sage is reserved for one meaning only: money saved / cheapest option. */
  --good:#8fce9f; --good-deep:#63ab77; --good-dim:#436f4e;
  --good-soft:rgba(143,206,159,.14); --good-softer:rgba(143,206,159,.07);
  --shadow:0 8px 26px rgba(0,0,0,.42);
  color-scheme:dark;
}
.stApp{background:var(--bg);color:var(--text)}
html,body,[class*=css]{font-family:'DM Sans',system-ui,sans-serif}
.block-container{max-width:1500px;padding:1.6rem 2rem 3.5rem}
#MainMenu,footer,header{visibility:hidden}
::selection{background:var(--accent-dim);color:#fff}

.hero{align-items:center;display:flex;gap:13px;margin-bottom:15px}
.mark{align-items:center;background:linear-gradient(135deg,var(--accent),var(--accent-deep));border-radius:13px;box-shadow:0 4px 14px rgba(240,168,105,.20);color:#06120c;display:flex;font-size:23px;height:46px;justify-content:center;width:46px}
.hero h1{color:var(--text);font-size:30px;letter-spacing:-.9px;margin:0}
.hero p{color:var(--muted);font-size:13px;margin:4px 0 0}

/* category nav pills */
div[data-testid="stPills"]{margin:2px 0 6px}
div[data-testid="stPills"] button{border-radius:999px!important;font-size:13.5px!important;font-weight:600!important;padding:6px 16px!important}

.band{background:linear-gradient(135deg,#3a2a1e,#241b15);border:1px solid var(--border);border-radius:15px;display:flex;align-items:flex-end;justify-content:space-between;gap:16px;margin:8px 0 14px;padding:18px 21px;position:relative;overflow:hidden}
.band::after{background:radial-gradient(circle at 88% 12%,rgba(240,168,105,.22),transparent 62%);content:'';inset:0;position:absolute}
.band>*{position:relative;z-index:1}
.band span{color:var(--accent);display:block;font-size:11px;font-weight:700;letter-spacing:.09em;text-transform:uppercase}
.band strong{color:#fff;display:block;font-size:40px;letter-spacing:-1.6px;line-height:1.04;margin-top:5px}
.band small{color:var(--muted);font-size:11.5px;line-height:1.55;text-align:right}
.band small b{color:var(--text)}

.cards{display:grid;gap:13px;grid-template-columns:repeat(auto-fit,minmax(216px,1fr));margin:0 0 14px}
.card{background:var(--surface);border:1px solid var(--border);border-radius:13px;padding:14px 16px;transition:border-color .15s,transform .15s}
.card:hover{border-color:var(--accent-dim);transform:translateY(-1px)}
.card h3{color:var(--text);font-size:13.5px;font-weight:700;margin:0 0 10px}
.card .big{color:var(--good);font-size:25px;font-weight:700;letter-spacing:-.8px}
.card .sub{color:var(--dim);font-size:11px;margin-top:2px}
.kv{border-top:1px solid var(--border);display:flex;justify-content:space-between;font-size:11.5px;margin-top:9px;padding-top:8px}
.kv i{color:var(--muted);font-style:normal}
.kv b{color:var(--text);font-weight:600}
.bar{background:var(--raised);border-radius:3px;height:5px;margin-top:11px;overflow:hidden}
.bar div{background:linear-gradient(90deg,var(--good),var(--good-deep));height:100%}
.hint{background:var(--good-soft);border:1px solid var(--good-dim);border-radius:7px;color:var(--good);display:inline-block;font-size:10.5px;margin-top:9px;padding:4px 8px}
.why{color:var(--muted);font-size:12px;line-height:1.6;margin-top:9px}

.sec{align-items:baseline;display:flex;flex-wrap:wrap;gap:10px;margin:26px 0 11px}
.sec h2{color:var(--text);font-size:19px;letter-spacing:-.4px;margin:0}
.sec p{color:var(--dim);font-size:12px;margin:0}

.tiles{display:grid;gap:11px;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));margin:12px 0}
.tile{background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:11px 14px}
.tile span{color:var(--muted);display:block;font-size:10.5px;font-weight:700;letter-spacing:.07em;text-transform:uppercase}
.tile strong{color:var(--text);display:block;font-size:20px;letter-spacing:-.5px;margin-top:3px}
.tile small{color:var(--dim);display:block;font-size:10.5px;margin-top:2px}
.tile.win{background:var(--good-soft);border-color:var(--good-dim)}
.tile.win strong,.tile.win small{color:var(--good)}

.delivery{display:grid;gap:11px;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));margin:0 0 13px}
.dcard{background:var(--surface);border:1px dashed var(--border);border-radius:11px;color:var(--text);font-size:12px;padding:10px 13px}
.dcard b{color:var(--muted);display:block;font-size:10.5px;font-weight:700;letter-spacing:.07em;margin-bottom:4px;text-transform:uppercase}
.dcard em{color:var(--dim);display:block;font-size:11px;font-style:normal;margin-top:3px}

.shell{background:var(--surface);border:1px solid var(--border);border-radius:13px;box-shadow:var(--shadow);overflow:auto}
.t{border-collapse:separate;border-spacing:0;color:var(--text);font-size:13px;min-width:760px;width:100%}
.t thead th{background:var(--raised);border-bottom:1px solid var(--border);color:var(--muted);font-size:11px;font-weight:700;letter-spacing:.07em;padding:11px 10px;position:sticky;text-align:right;text-transform:uppercase;top:0;z-index:3}
.t thead th.itemh{left:0;text-align:left;z-index:4}
.t thead th.savh{background:#233025;color:var(--good)}
.t thead th em{color:var(--dim);display:block;font-size:9.5px;font-style:normal;font-weight:400;letter-spacing:.02em;text-transform:none}
.t td{border-bottom:1px solid var(--border);padding:9px 10px;vertical-align:middle}
.t tbody tr:last-child td{border-bottom:0}
.catrow td{background:var(--raised);color:var(--accent);font-size:10.5px;font-weight:700;letter-spacing:.1em;padding:7px 10px;text-transform:uppercase}
.t td.item{background:var(--surface);font-weight:600;left:0;min-width:180px;position:sticky;z-index:2}
.t td.item em{color:var(--dim);display:block;font-size:10.5px;font-style:normal;font-weight:400;margin-top:2px}
.t tbody tr:hover td,.t tbody tr:hover td.item{background:var(--raised)}
.pc{text-align:right;white-space:nowrap}
.pc a{color:inherit;display:block;padding:1px 0;text-decoration:none}
.pc a:hover .p{text-decoration:underline}
.pc .p{font-size:13.5px;font-weight:600}
.pc .u{color:var(--dim);font-size:10.5px;margin-top:2px}
.pc.best{background:var(--good-soft);box-shadow:inset 2px 0 0 var(--good)}
.pc.best .p{color:var(--good);font-weight:700}
.pc.best .u{color:#a5d6b1}
.pc.miss{color:var(--dim);text-align:right}
.sv{background:var(--good-softer);color:var(--good);font-weight:700;text-align:right;white-space:nowrap}
.sv.zero{color:var(--dim);font-weight:400}
.note{background:var(--surface);border:1px solid var(--border);border-radius:11px;color:var(--muted);font-size:12px;line-height:1.65;margin:12px 0;padding:13px 15px}
.note b{color:var(--text)}
.swipe-note{color:var(--dim);display:none;font-size:11px;margin:7px 2px;text-align:right}
.empty{background:var(--surface);border:1px dashed var(--border);border-radius:13px;color:var(--muted);font-size:13px;line-height:1.65;padding:24px}
.empty b{color:var(--text);display:block;font-size:14.5px;margin-bottom:6px}

/* deals + restaurant tables */
.t.deals{min-width:820px}
.t.deals thead th{text-align:left}
.t.deals td{text-align:left;white-space:normal}
.t.deals td.nm{background:var(--surface);font-weight:600;left:0;min-width:165px;position:sticky;z-index:2}
.t.deals tbody tr:hover td.nm{background:var(--raised)}
.t.deals td.nm em{color:var(--dim);display:block;font-size:10.5px;font-style:normal;font-weight:400;margin-top:2px}
.t.deals td.cost{font-weight:700;white-space:nowrap}
.t.deals td.cost.free{color:var(--good)}
.t.deals td.go{white-space:nowrap}
.t.deals td.go a{background:var(--soft);border:1px solid var(--accent-dim);border-radius:7px;color:var(--accent);font-weight:700;padding:6px 11px;text-decoration:none}
.t.deals td.go a:hover{background:var(--accent-dim);color:#fff}
.t.deals td.num{text-align:right;white-space:nowrap}
.t.deals td.was{color:var(--dim);text-decoration:line-through;white-space:nowrap}
.t.deals td.now{color:var(--good);font-weight:700;white-space:nowrap}
.ends{border-radius:6px;font-size:10.5px;font-weight:600;padding:3px 7px;white-space:nowrap}
.ends.soon{background:rgba(224,138,60,.16);color:#e2a163}
.ends.ok{background:var(--raised);color:var(--muted)}
.ends.open{background:var(--good-softer);color:var(--good)}
.srcs{color:var(--dim);font-size:11.5px;margin:11px 2px}
.srcs a{color:var(--accent);text-decoration:none}
.srcs a:hover{text-decoration:underline}
.checked{background:var(--raised);border:1px solid var(--border);border-radius:9px;color:var(--muted);display:inline-block;font-size:11px;margin:0 0 11px;padding:5px 10px}

@media(max-width:760px){
  .block-container{padding:.7rem .5rem 2rem}
  .hero{margin:0 .2rem 11px;gap:10px}.hero h1{font-size:23px}.hero p{font-size:11.5px}
  .mark{font-size:19px;height:39px;width:39px}
  .band{border-radius:12px;flex-direction:column;align-items:flex-start;gap:7px;padding:14px 16px}
  .band strong{font-size:32px}.band small{text-align:left}
  .cards,.delivery,.tiles{grid-template-columns:repeat(2,1fr)}
  .sec{margin:20px 0 9px}.sec h2{font-size:17px}
  .t{font-size:12px;min-width:640px}
  .t.deals{min-width:720px}
  .t td{padding:8px}.t thead th{padding:9px 8px}
  .t td.item,.t.deals td.nm{min-width:126px}
  .t.deals td.go a{display:inline-block;padding:10px 13px}
  .pc .p{font-size:12.5px}
  .note{padding:12px 13px}
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
        hint = f'<div class="hint">Verified basket comparison: {sgd(BASKET_ANNUAL, 0)}/yr</div>'
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
if view == DATA_CATEGORY:
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

# ----------------------------------------------------- dining out deals ----
elif view == DEALS_CATEGORY:
    st.markdown(
        '<div class="sec"><h2>Current dining deals</h2>'
        "<p>Specific venues, then the programmes and cards that unlock them</p></div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="checked">Checked {DEALS_CHECKED} &middot; dining promos '
        "expire constantly, so re-verify a row before you commit to it</div>",
        unsafe_allow_html=True,
    )

    # Where to actually eat. End dates are evaluated against today, so rows
    # age out on their own instead of quietly going stale.
    def end_state(ends):
        if ends is None:
            return "open", "No end date"
        left = (datetime.strptime(ends, "%d %b %Y").date() - date.today()).days
        if left < 0:
            return "expired", f"Ended {ends}"
        if left <= 14:
            return "soon", f"Ends {ends}" + (" (today)" if left == 0 else f" ({left}d)")
        return "ok", f"Ends {ends}"

    def entry_price(text):
        """Lowest dollar figure in a price string, for numeric sorting."""
        found = re.findall(r"\d+(?:\.\d+)?", text)
        return min(float(n) for n in found) if found else float("inf")

    live = [(r, *end_state(r[6])) for r in DINING_RESTAURANTS]
    expired = [r for r, state, _ in live if state == "expired"]
    live = [(r, state, lbl) for r, state, lbl in live if state != "expired"]
    live.sort(key=lambda x: (entry_price(x[0][4]), x[0][0]))

    st.markdown(
        '<div class="sec"><h2>Where to eat</h2>'
        f"<p>{len(live)} venues with a live 1-for-1, cheapest first</p></div>",
        unsafe_allow_html=True,
    )
    rest = ('<div class="shell"><table class="t deals"><thead><tr>'
            "<th>Restaurant</th><th>What</th><th>Usual</th><th>With 1-for-1</th>"
            "<th>Cards accepted</th><th>Validity</th><th></th></tr></thead><tbody>")
    for row, state, label in live:
        name, venue, what, was, now, cards, _ends = row
        url = "https://www.google.com/search?q=" + quote_plus(f"{name} {venue} 1-for-1 buffet")
        rest += (
            f'<tr><td class="nm">{html.escape(name)}<em>{html.escape(venue)}</em></td>'
            f"<td>{html.escape(what)}</td>"
            f'<td class="was">{html.escape(was)}</td>'
            f'<td class="now">{html.escape(now)}</td>'
            f"<td>{html.escape(cards)}</td>"
            f'<td><span class="ends {state}">{html.escape(label)}</span></td>'
            f'<td class="go"><a href="{url}" target="_blank" rel="noopener">Book &rarr;</a></td></tr>'
        )
    st.markdown(rest + "</tbody></table></div>", unsafe_allow_html=True)
    st.markdown(
        '<div class="note">Prices are <b>++</b> &mdash; add about 19.9% for '
        "service charge and GST. Nearly every deal needs the qualifying card "
        "presented at payment and the promotion named when booking, so confirm "
        "both before you go. "
        + (f"{len(expired)} row(s) hidden as already expired. " if expired else "")
        + "These are hand-entered, not scraped, so treat the validity column as "
        "a prompt to re-check rather than a guarantee.</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="sec"><h2>Programmes and apps</h2>'
        "<p>Subscriptions and free platforms that unlock the deals above</p></div>",
        unsafe_allow_html=True,
    )
    prog = ('<div class="shell"><table class="t deals"><thead><tr>'
            "<th>Programme</th><th>Cost</th><th>What you get</th>"
            "<th>Coverage</th><th>Best for</th><th></th></tr></thead><tbody>")
    for name, cost, deal, coverage, best_for, url in DINING_PROGRAMMES:
        free = " free" if cost == "Free" else ""
        prog += (
            f'<tr><td class="nm">{html.escape(name)}</td>'
            f'<td class="cost{free}">{html.escape(cost)}</td>'
            f"<td>{html.escape(deal)}</td><td>{html.escape(coverage)}</td>"
            f"<td>{html.escape(best_for)}</td>"
            f'<td class="go"><a href="{url}" target="_blank" rel="noopener">Open &rarr;</a></td></tr>'
        )
    st.markdown(prog + "</tbody></table></div>", unsafe_allow_html=True)

    st.markdown(
        '<div class="sec"><h2>Dining cashback cards</h2>'
        "<p>Rebate is capped monthly, so a higher rate is not always more money</p></div>",
        unsafe_allow_html=True,
    )
    cards_tbl = ('<div class="shell"><table class="t deals"><thead><tr>'
                 "<th>Card</th><th>Dining rate</th><th>Min spend / month</th>"
                 "<th>Cashback cap</th><th>Ceiling / year</th><th></th></tr></thead><tbody>")
    for name, rate, min_spend, cap, ceiling in DINING_CARDS:
        url = "https://www.google.com/search?q=" + quote_plus(f"{name} credit card singapore dining")
        cards_tbl += (
            f'<tr><td class="nm">{html.escape(name)}</td>'
            f'<td class="cost">{html.escape(rate)}</td>'
            f"<td>{html.escape(min_spend)}</td><td>{html.escape(cap)}</td>"
            f'<td class="num">{sgd(ceiling, 0)}</td>'
            f'<td class="go"><a href="{url}" target="_blank" rel="noopener">Look up &rarr;</a></td></tr>'
        )
    st.markdown(cards_tbl + "</tbody></table></div>", unsafe_allow_html=True)

    # Reality-check the assumption against what the deals can actually return.
    CARD_RATE, CARD_CAP_MONTH, PER_REDEMPTION = 0.06, 80, 20
    card_value = min(active["spend"] * CARD_RATE, CARD_CAP_MONTH * 12)
    gap = max(0, active["saving"] - card_value)
    per_month = gap / PER_REDEMPTION / 12
    st.markdown(
        f'<div class="note"><b>Does your {active["pct"]}% assumption hold?</b> '
        f'A representative 6% dining card on {sgd(active["spend"], 0)} of dining '
        f"returns about {sgd(card_value, 0)} a year before the monthly cap bites. "
        f'Your assumption implies {sgd(active["saving"], 0)}, leaving {sgd(gap, 0)} '
        f"that has to come from 1-for-1 redemptions &mdash; roughly "
        f"<b>{per_month:.0f} redemptions a month</b> at S${PER_REDEMPTION} saved each. "
        "If that sounds like more eating out than you actually do, the rate is too "
        "high rather than the deals being bad.</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="srcs">Sources: '
        + " &middot; ".join(f'<a href="{u}" target="_blank" rel="noopener">{html.escape(n)}</a>' for n, u in DEALS_SOURCES)
        + "</div>",
        unsafe_allow_html=True,
    )

# ------------------------------------------------- categories without data ----
# Overview deliberately falls through with nothing extra -- it stays a clean
# summary, no detail tables underneath.
elif view != "Overview":
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
