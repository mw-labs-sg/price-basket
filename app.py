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
    ("Breakfast", "Salmon", "Smoked or sliced", "100 g equivalent", 1, 4.90, "kg", .1, 4.50, 3.95, 7.95),
    ("Beverages", "100PLUS", "Active", "12 x 300 ml", 1, 9.47, "L", 3.6, 8.95, 9.47, 9.95),
    ("Fruits", "Apples", "Any brand", "650 g equivalent", 1, 3.67, "kg", .65, 4.26, 2.80, 3.94),
    ("Fruits", "Oranges", "Any brand", "800 g equivalent", 1, 5.76, "kg", .8, 6.32, 3.95, 7.95),
]

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap');
:root{color-scheme:light}.stApp{background:#f6f8fb;color:#17202a}html,body,[class*=css]{font-family:'DM Sans',system-ui,sans-serif}.block-container{max-width:1750px;padding:1.8rem 2rem 3rem}#MainMenu,footer,header{visibility:hidden}
.hero{align-items:center;display:flex;gap:10px;margin-bottom:9px}.mark{align-items:center;background:linear-gradient(135deg,#27835d,#185f43);border-radius:10px;color:white;display:flex;font-size:20px;height:40px;justify-content:center;width:40px}.hero h1{font-size:27px;letter-spacing:-1px;margin:0}.hero p{color:#718078;font-size:11px;margin:2px 0 0}.summary{align-items:center;background:linear-gradient(135deg,#176b49,#27835d);border-radius:10px;color:white;display:flex;justify-content:space-between;margin:8px 0;padding:8px 12px}.summary span{font-size:9px;font-weight:700;letter-spacing:.07em;opacity:.82;text-transform:uppercase}.summary strong{display:block;font-size:21px}.summary small{font-size:9px;opacity:.8;text-align:right}.shell{background:white;border:1px solid #e4eae6;border-radius:11px;box-shadow:0 6px 20px rgba(22,50,37,.05);overflow:auto}.t{border-collapse:collapse;min-width:1250px;width:100%;font-size:10.5px}.t th{background:#f5f8f6;border-bottom:1px solid #dfe7e2;color:#526059;padding:5px 6px;text-align:left}.t th.store{background:white;color:#203128;font-size:10.5px;text-align:center}.t th.sub{font-size:8.5px;text-align:right;text-transform:uppercase}.t th:last-child{background:#eaf3ed;color:#246244}.t td{border-bottom:1px solid #edf1ee;padding:5px 6px;vertical-align:middle}.t td:last-child{background:#f1f7f3}.t tr:last-child td{border-bottom:0}.delivery-row td{background:#f8faf9;color:#53635a}.delivery-row.last td{border-bottom:2px solid #d8e4dd}.delivery-fee{text-align:center;font-size:9px;white-space:nowrap}.delivery-fee b{color:#203128}.category-start td{border-top:2px solid #d8e4dd}.cat{color:#27835d;font-size:8.5px;font-weight:700;text-transform:uppercase;width:68px}.item{font-weight:600;min-width:145px;white-space:nowrap}.num{text-align:right;white-space:nowrap}.saving{color:#176b49;font-weight:700}.price-link{color:inherit;font-size:9px;margin-left:2px;text-decoration:none}.price-link:hover{text-decoration:underline}.best{font-weight:700}.best.rm{background:#e8f0fa;color:#275b91}.best.ss{background:#e8f7ef;color:#126b48}.best.fp{background:#fff0dc;color:#a45112}.best.cs{background:#fde8e8;color:#a83838}.missing{color:#aab2ae}.note{color:#75817b;font-size:10px;margin:8px 2px}.badge{background:#eef3f0;border-radius:9px;color:#56645d;font-size:9px;padding:2px 6px;white-space:nowrap}.swipe-note{display:none}
@media(max-width:700px){
  .block-container{padding:.65rem .35rem 1.5rem}.hero{margin:0 .2rem 6px}.hero h1{font-size:22px}.hero p{font-size:9px}.mark{height:34px;width:34px;font-size:17px}
  .summary{border-radius:8px;margin:6px 0;padding:7px 9px}.summary strong{font-size:18px}.summary small{font-size:8px;max-width:130px}
  [data-testid="stHorizontalBlock"]{gap:.4rem}.shell{border-radius:8px;-webkit-overflow-scrolling:touch;overscroll-behavior-x:contain}.t{font-size:8.5px;min-width:940px}.t th,.t td{padding:4px}
  .cat{line-height:1.2;width:58px}.item{min-width:100px}.delivery-fee{font-size:8px}.note{font-size:8px}.swipe-note{color:#718078;display:block;font-size:8px;margin:4px 2px;text-align:right}
}
</style>
<div class="hero"><div class="mark">🛒</div><div><h1>Price Basket</h1><p>Your actual shopping list, organized for like-for-like supermarket matching.</p></div></div>
""", unsafe_allow_html=True)

CATEGORY_NAMES = ("Breakfast", "Fruits", "Vegetables", "Meat, Poultry, Seafood & Frozen", "Rice, Noodles & Pasta", "Beverages")
filter_category, filter_item = st.columns([1, 1.25])
with filter_category:
    selected_category = st.selectbox("Category", ("All categories", *CATEGORY_NAMES))
available_items = [row[1] for row in ITEMS if selected_category == "All categories" or row[0] == selected_category]
with filter_item:
    selected_item = st.selectbox("Item", ("All items", *available_items))

display_items = [
    row for row in ITEMS
    if (selected_category == "All categories" or row[0] == selected_category)
    and (selected_item == "All items" or row[1] == selected_item)
]
matched = sum(1 for row in display_items if len([p for p in (row[5], *row[8:11]) if p is not None]) >= 2)
st.markdown(f'<span class="badge">{len(display_items)} products</span> &nbsp; <span class="badge">{matched} price comparisons ready</span>', unsafe_allow_html=True)

total_savings = sum(
    max(0, row[5] - row[8]) * 52
    for row in display_items
    if row[5] is not None and row[8] is not None
)
st.markdown(f'<div class="summary"><div><span>SHENG SIONG savings per year</span><strong>S${total_savings:,.2f}</strong></div><small>Compared with RedMart<br>one purchase per item each week</small></div>', unsafe_allow_html=True)
head = '<div class="shell"><table class="t"><thead><tr><th rowspan="2">Category</th><th rowspan="2">Item</th>'
for store in ("SHENG SIONG", "COLD STORAGE", "NTUC FAIRPRICE", "REDMART"):
    head += f'<th class="store" colspan="2">{store}</th>'
head += '<th rowspan="2">SHENG SIONG<br>savings / year</th></tr><tr>' + '<th class="sub">Price</th><th class="sub">Per kg / L</th>' * 4 + '</tr></thead><tbody>'

body = '''<tr class="delivery-row"><td class="cat" rowspan="2">DELIVERY</td><td class="item">Delivery fee</td>
<td class="delivery-fee" colspan="2"><b>S$6</b></td><td class="delivery-fee" colspan="2"><b>S$6.99</b></td>
<td class="delivery-fee" colspan="2"><b>S$5 + S$3.99 service</b></td><td class="delivery-fee" colspan="2"><b>From S$3.99</b></td><td>—</td></tr>
<tr class="delivery-row last"><td class="item">Free delivery from</td>
<td class="delivery-fee" colspan="2">S$100</td><td class="delivery-fee" colspan="2">S$80</td>
<td class="delivery-fee" colspan="2">S$59</td><td class="delivery-fee" colspan="2">S$60 · 6-hour slot</td><td>—</td></tr>'''
last_category = None
category_counts = {}
for row in display_items:
    category_counts[row[0]] = category_counts.get(row[0], 0) + 1
CATEGORY_ORDER = {name: index for index, name in enumerate(CATEGORY_NAMES)}
ITEM_ORDER = {name: index for index, name in enumerate(("Fresh Milk", "Eggs", "Loaf Bread", "Ham", "Butter", "Salmon", "Apples", "Oranges", "Bananas", "Blackberries", "Strawberries", "Broccoli", "Cabbage", "Baby Corn", "Corn", "Garlic", "Brown Shimeji Mushrooms", "Carrots", "Green Beans", "Green Chillies", "Radish", "Kai Lan", "Gourd", "Onions", "Potatoes", "Xiao Bai Cai", "Chicken", "Pork", "Beef", "Fish", "Prawns", "Rice", "Indomie", "100PLUS"))}
for category, item, brand, pack, _qty, paid, unit, amount, *store_prices in sorted(display_items, key=lambda row: (CATEGORY_ORDER.get(row[0], 99), ITEM_ORDER.get(row[1], 99), row[1])):
    prices = [paid, *store_prices]
    available = [p for p in prices if p is not None]
    lowest = min(available) if len(available) >= 2 else None
    annual = max(0, paid - store_prices[0]) * 52 if paid is not None and store_prices[0] is not None else None
    row_class = "category-start" if last_category is not None and category != last_category else ""
    category_cell = ""
    if category != last_category:
        category_cell = f'<td class="cat" rowspan="{category_counts[category]}">{html.escape(category)}</td>'
    body += f'<tr class="{row_class}">{category_cell}<td class="item" title="{html.escape(pack)}">{html.escape(item)}</td>'
    price_map = {"rm": prices[0], "ss": prices[1], "fp": prices[2], "cs": prices[3]}
    winner = next(
        (store for store in ("ss", "cs", "fp", "rm") if lowest is not None and price_map[store] == lowest),
        None,
    )
    search = quote_plus(f"{brand} {item} {pack}")
    links = {
        "ss": "https://www.foodpanda.sg/shop/cvhb/sheng-siong-supermarket-hougang-hg",
        "cs": f"https://coldstorage.com.sg/search?q={search}",
        "fp": f"https://www.fairprice.com.sg/search?query={search}",
        "rm": f"https://www.lazada.sg/catalog/?q={search}",
    }
    for store_class in ("ss", "cs", "fp", "rm"):
        price = price_map[store_class]
        if price is None:
            body += f'<td class="num missing">— <a class="price-link" href="{links[store_class]}" target="_blank">↗</a></td><td class="num missing">—</td>'
        else:
            css = f" best {store_class}" if store_class == winner else ""
            label = "each" if unit == "item" else unit
            body += f'<td class="num{css}">S${price:.2f}<a class="price-link" href="{links[store_class]}" target="_blank">↗</a></td><td class="num{css}">S${price/amount:.2f}/{label}</td>'
    savings_text = "—" if annual is None or annual == 0 else f"S${annual:,.2f}"
    savings_class = "num saving" if annual is not None and annual > 0 else "num"
    body += f'<td class="{savings_class}">{savings_text}</td></tr>'
    last_category = category

st.markdown('<div class="swipe-note">Swipe left or right to compare stores →</div>' + head + body + '</tbody></table></div><div class="note">RedMart prices are transcribed from your order screenshots. When the identical product is unavailable, the closest practical category substitute is normalized to the RedMart quantity (for example eggs per egg or produce per kg). A dash means no defensible comparison has been verified yet.</div>', unsafe_allow_html=True)
