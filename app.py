import html
import re
from datetime import date, datetime
from urllib.parse import quote_plus
import streamlit as st

st.set_page_config(page_title="Price Basket Kaki", page_icon="🧺", layout="wide")

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
    ("Dining out", 15000, 15, "Restaurants, hawker, delivery. The deal finder makes this actionable; the saving rate remains your estimate."),
    ("Travel", 15000, 8, "Large and lumpy. Use the planner below to model only the habits you can realistically sustain."),
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
UOB_VI_PERKS = (
    ("Miles", "1.4 mpd local · 2.4 mpd overseas", "No miles-conversion fee. Selected transaction categories are excluded."),
    ("Renewal", "25,000 miles + up to 15,000 bonus", "25,000 after paying the annual fee; another 15,000 after S$100,000 qualifying annual spend."),
    ("Airport", "12 lounge passes per membership year", "DragonPass access at 1,400+ lounges; passes can be shared with accompanying guests."),
    ("Insurance", "Up to US$1m travel accident cover", "Charge the full travel fare to the card; also includes specified inconvenience and purchase-protection cover."),
    ("Hotels", "IHG 20% off · Agoda stay 3 pay 2", "Participating properties and booking windows only; Agoda discount is capped at US$150 per transaction."),
    ("Dining", "Up to 30% off restaurants", "Plus up to 25% off participating airport restaurants through DragonPass."),
    ("Concierge", "24/7 Visa Infinite concierge", "Dining, travel and lifestyle assistance: 1800 253 2288 or +65 6253 2288 overseas."),
    ("Golf", "Complimentary weekday green fees", "Participating regional courses; advance booking and individual course terms apply."),
    ("Assistance", "Home, vehicle, travel and medical help", "Home assistance up to S$100 per visit, twice yearly; separate limits and terms apply."),
    ("Fee", "S$654 yearly · non-waivable", "First supplementary card is free for life; later supplementary cards are chargeable."),
)
UOB_VI_DINING = (
    ("Mosella", "Pan Pacific Orchard", "20% off à la carte menu", "30 Dec 2026"),
    ("Portman's Bar", "PARKROYAL COLLECTION Marina Bay", "20% off à la carte menu", "30 Dec 2026"),
    ("Peppermint", "PARKROYAL COLLECTION Marina Bay", "20% off à la carte menu", "30 Dec 2026"),
    ("Skyline Bar", "PARKROYAL COLLECTION Marina Bay", "20% off à la carte menu", "30 Dec 2026"),
    ("Ginger", "PARKROYAL on Beach Road", "20% off à la carte menu", "30 Dec 2026"),
    ("Club 5", "PARKROYAL on Beach Road", "20% off à la carte menu", "30 Dec 2026"),
    ("Lime", "PARKROYAL COLLECTION Pickering", "20% off à la carte menu", "30 Dec 2026"),
    ("Pete's Place", "Grand Hyatt Singapore", "15% off food bill", "30 Dec 2026"),
    ("10|Scotts", "Grand Hyatt Singapore", "15% off afternoon tea or food/bites menu", "30 Dec 2026"),
    ("Hai Tien Lo", "Pan Pacific Singapore", "15% off à la carte menu", "30 Dec 2026"),
    ("Edge", "Pan Pacific Singapore", "15% off à la carte menu", "30 Dec 2026"),
    ("Keyaki", "Pan Pacific Singapore", "15% off à la carte menu", "30 Dec 2026"),
    ("Peach Blossoms", "PARKROYAL COLLECTION Marina Bay", "15% off à la carte menu", "30 Dec 2026"),
    ("Li Bai Cantonese Restaurant", "Sheraton Towers Singapore", "15% off total bill", "30 Dec 2026"),
    ("The Dining Room", "Sheraton Towers Singapore", "25% off total bill", "30 Dec 2026"),
    ("Lobby Bar", "Sheraton Towers Singapore", "25% off total bill", "30 Dec 2026"),
    ("Nobu Singapore", "Four Seasons Hotel Singapore", "Complimentary welcome drink per person", "See UOB terms"),
    ("Capasso", "Telok Ayer", "15% off à la carte food + aperitif", "31 Dec 2026"),
    ("NOX – Dine in the Dark", "Club Street", "Cocktail per diner or Prosecco with 4 prix fixe menus", "30 Dec 2026"),
    ("Sapoto", "Amoy Street", "Complimentary 300ml house-pour carafe", "31 Dec 2027"),
    ("Sushi Yujo", "Amoy Street", "Complimentary 300ml house-pour carafe", "31 Dec 2027"),
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

# Travel savings are modelled as controllable levers rather than volatile
# promo codes. The user can switch on only the habits they would genuinely use.
# label, saving rate applied to annual travel spend, short explanation
TRAVEL_LEVERS = (
    ("Flexible dates", 4.0, "Compare a 3-day window and avoid peak departure times."),
    ("Fare alerts", 2.0, "Track first, then book when the route drops below its normal range."),
    ("No-FX-fee payment", 1.5, "Avoid the common card markup on overseas spend."),
    ("Book direct after comparing", 1.0, "Use aggregators to compare, then check the airline or hotel directly."),
    ("Right-size baggage", 1.5, "Price the whole trip, including bags and seats, before choosing the fare."),
)
TRAVEL_DEALS_CHECKED = "29 Aug 2026"
SCHOOL_HOLIDAY_WINDOWS = {
    "March": ("14–22 Mar 2026", "MOE Term 1 school holiday", "14 Mar 2026", "22 Mar 2026"),
    "June": ("30 May–28 Jun 2026", "MOE Term 2 school holiday", "30 May 2026", "28 Jun 2026"),
    "September": ("4–13 Sep 2026", "Teachers' Day + MOE Term 3 break", "4 Sep 2026", "13 Sep 2026"),
    "December": ("21 Nov–31 Dec 2026", "MOE Term 4 school holiday", "21 Nov 2026", "31 Dec 2026"),
}
# group, destination, indicative return fare, trip length, why it works,
# source URL. Sale fares are indicative and may not
# be available on the suggested family dates.
TRIP_IDEAS = (
    ("Australia & NZ", "Perth", "From S$548", "8 nights", "Easy first Australia trip; beaches, wildlife and a compact city.", "https://www.singaporeair.com/en_UK/sg/plan-travel/local-promotions/offers/"),
    ("Australia & NZ", "Sydney", "From S$588", "9 nights", "Harbour sights plus Blue Mountains; spring weather suits family days out.", "https://www.singaporeair.com/en_UK/sg/plan-travel/local-promotions/offers/"),
    ("Australia & NZ", "Melbourne", "From S$688", "9 nights", "City, wildlife and a Great Ocean Road add-on without changing hotels often.", "https://www.singaporeair.com/en_UK/sg/plan-travel/local-promotions/offers/"),
    ("Australia & NZ", "Auckland + Rotorua", "From S$1,288", "9 nights", "A good North Island loop with geothermal parks and short driving days.", "https://www.singaporeair.com/en_UK/sg/plan-travel/local-promotions/offers/"),
    ("Japan", "Osaka + Kyoto", "From S$808", "9 nights", "One base or a simple two-city split; late November often catches autumn colour.", "https://www.singaporeair.com/en_UK/sg/plan-travel/local-promotions/offers/"),
    ("Japan", "Tokyo", "From S$1,008", "9 nights", "Big family variety; year-end dates are cooler and generally more comfortable.", "https://www.singaporeair.com/en_UK/sg/plan-travel/local-promotions/offers/"),
    ("Japan", "Hokkaido", "Check live fare", "8 nights", "Choose September for outdoors or December for an early snow-focused trip.", "https://www.flyscoot.com/flights/en/flights-from-singapore"),
    ("Regional", "Penang", "From S$159", "4 nights", "Short, food-led break with little planning overhead.", "https://www.flyscoot.com/flights/en/flights-from-singapore"),
    ("Regional", "Bangkok", "From S$213", "4 nights", "Simple city break with family hotels, food and indoor options.", "https://www.flyscoot.com/flights/en/flights-from-singapore"),
    ("Regional", "Bali", "From S$298", "6 nights", "Works best with one resort base; September is typically the stronger window.", "https://www.singaporeair.com/en_UK/sg/plan-travel/local-promotions/offers/"),
    ("Regional", "Hanoi", "From S$328", "6 nights", "Pair the city with Ninh Binh for a compact culture-and-nature trip.", "https://www.singaporeair.com/en_UK/sg/plan-travel/local-promotions/offers/"),
)
TRIP_DATES = {
    "Perth": ("14–22 Mar", "6–14 Jun", "4–12 Sep", "21–29 Nov"),
    "Sydney": ("14–22 Mar", "6–14 Jun", "4–13 Sep", "28 Nov–6 Dec"),
    "Melbourne": ("14–22 Mar", "6–14 Jun", "4–13 Sep", "5–13 Dec"),
    "Auckland + Rotorua": ("14–22 Mar", "6–14 Jun", "4–13 Sep", "27 Nov–6 Dec"),
    "Osaka + Kyoto": ("14–22 Mar", "6–14 Jun", "4–13 Sep", "21–29 Nov"),
    "Tokyo": ("14–22 Mar", "6–14 Jun", "4–13 Sep", "28 Nov–6 Dec"),
    "Hokkaido": ("14–22 Mar", "6–14 Jun", "4–12 Sep", "12–20 Dec"),
    "Penang": ("14–18 Mar", "6–10 Jun", "5–9 Sep", "21–25 Nov"),
    "Bangkok": ("14–18 Mar", "6–10 Jun", "5–9 Sep", "21–25 Nov"),
    "Bali": ("14–20 Mar", "6–12 Jun", "4–10 Sep", "21–27 Nov"),
    "Hanoi": ("14–20 Mar", "6–12 Jun", "4–10 Sep", "28 Nov–4 Dec"),
}
# destination: hotel, area, family fit, official page
HOTEL_IDEAS = {
    "Perth": ("Holiday Inn Perth City Centre", "Perth CBD", "King + two singles in a separate family sleeping area; kids stay and eat free terms apply.", "https://perth.holidayinn.com/stay/family-room/"),
    "Sydney": ("Sofitel Sydney Wentworth", "Sydney CBD", "Connecting rooms, children’s welcome kit and free breakfast for under-12s.", "https://sofitel.accor.com/en/hotels/3665/Family.html"),
    "Melbourne": ("Quay West Suites Melbourne", "Southbank", "Apartment-style stay with extra living space and a kitchen for longer family trips.", "https://all.accor.com/a/en/experiences/melbourne-family-hotels.html"),
    "Auckland + Rotorua": ("The Sebel Quay West Auckland", "Auckland CBD", "One- to three-bedroom apartments near the harbour; two-bedroom units sleep up to five.", "https://all.accor.com/hotel/8802/index.en.shtml"),
    "Osaka + Kyoto": ("MIMARU Osaka Namba Station", "Namba", "Family apartments with kitchens; two-bedroom options keep longer stays manageable.", "https://mimaruhotels.com/en/"),
    "Tokyo": ("MIMARU Tokyo Station East", "Hatchobori", "One- and two-bedroom family apartments, including bunk-bed layouts and kitchens.", "https://mimaruhotels.com/en/hotel/tokyo-station-east/"),
    "Hokkaido": ("Hotel Keihan Sapporo", "Sapporo Station", "Connecting rooms sleep four to six with five or six separate beds.", "https://sapporo.hotelkeihan.co.jp/rooms/connecting-room-non-smoking/"),
    "Penang": ("Sunway Hotel Georgetown", "George Town", "Family room with one king and one single; accommodates two adults and two young children.", "https://www.sunwayhotels.com/sunway-georgetown/rooms-suites/family-room"),
    "Bangkok": ("Courtyard by Marriott Bangkok", "Ratchaprasong", "Family room for four with two double beds, a bathtub and connecting-room options.", "https://www.marriott.com/en-us/hotels/bkkcy-courtyard-bangkok/rooms/premium-rooms/"),
    "Bali": ("Courtyard Bali Nusa Dua Resort", "Nusa Dua", "Resort rooms and spacious suites around a lagoon pool, suited to a one-base family holiday.", "https://www.marriott.com/en-us/hotels/dpscy-courtyard-bali-nusa-dua-resort/rooms/"),
    "Hanoi": ("Hanoi Harmonia Hotel", "Old Quarter", "Family room with two king beds for up to four adults and one child.", "https://hanoiharmoniahotel.com/rooms-rates/family-room"),
}

# Home-screen offers, verified against the linked publisher pages. Keep this
# intentionally small: it is a useful editorial shortlist, not a deal dump.
# category, eyebrow, title, offer, detail, valid-through, url, source
FLASH_DEALS_CHECKED = "29 Aug 2026"
FLASH_DEALS = (
    ("Groceries", "FairPrice weekly", "Australian strawberries", "S$4.95 · save S$3", "250 g pack; available while stocks last.", "2 Sep 2026", "https://www.fairprice.com.sg/tag/weekly-deals", "FairPrice"),
    ("Groceries", "FairPrice weekly", "Shine Muscat grapes", "S$2.45 · save S$1.50", "500 g pack; available while stocks last.", "2 Sep 2026", "https://www.fairprice.com.sg/tag/weekly-deals", "FairPrice"),
    ("Dining out", "Eatigo lunch", "50% off selected lunches", "Up to 50% off", "Live time slots include Crossroads Buffet, J65 and Food Capital.", None, "https://eatigo.com/en/regions/27/themes/15505", "Eatigo"),
    ("Dining out", "Chope exclusive", "Gaia Ristorante", "20% off total bill", "Book and dine through Chope; à la carte only, exclusions apply.", "31 Aug 2026", "https://www.chope.co/singapore-restaurants/pages/testwebview", "Chope"),
    ("Travel", "KrisFlyer", "Spontaneous Escapes", "30% off Saver awards", "Selected Singapore Airlines flights for travel in September.", "31 Aug 2026", "https://www.singaporeair.com/en_UK/sg/plan-travel/promotions/global/kf/kf-promo/kfescapes/", "Singapore Airlines"),
    ("Travel", "Singapore Airlines", "Regional fares from Singapore", "Kuala Lumpur from S$158", "Economy return fare; selected travel periods and blackout dates apply.", "10 Sep 2026", "https://www.singaporeair.com/en_UK/sg/plan-travel/local-promotions/offers/", "Singapore Airlines"),
)


def sgd(value, dp=2):
    return f"S${value:,.{dp}f}"


st.session_state.setdefault("appearance", "Dark")
appearance = st.session_state["appearance"]


st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap');

/* Dark palette. Every colour is a token so the theme can be retuned in one
   place; .streamlit/config.toml carries the matching widget chrome. */
:root{
  /* Deep blue-charcoal keeps dense comparison data calm and legible. */
  --bg:#090d14; --surface:#111824; --raised:#182231; --border:#263448;
  --text:#f5f7fb; --muted:#aeb9ca; --dim:#7f8da3;
  /* Coral adds warmth without turning the entire interface brown. */
  --accent:#ffad7a; --accent-deep:#f18455; --accent-dim:#8e4d32;
  --soft:rgba(255,173,122,.13); --softer:rgba(255,173,122,.07);
  /* Mint is reserved for one meaning only: money saved / cheapest option. */
  --good:#72dfb0; --good-deep:#40b987; --good-dim:#286e56;
  --good-soft:rgba(114,223,176,.13); --good-softer:rgba(114,223,176,.07);
  --shadow:0 18px 50px rgba(0,0,0,.34);
  --app-bg:radial-gradient(circle at 78% -10%,#182438 0,transparent 35%),var(--bg);
  --band-a:#172335;--band-b:#101824;--band-border:#30415a;
  --pick-top:#172232;--flash-a:#172231;--flash-b:#101720;--flash-hover:#405671;
  --miles-a:#17283a;--miles-b:#111824;--miles-border:#31526a;--mark-text:#12151c;
  color-scheme:dark;
}
.stApp{background:var(--app-bg);color:var(--text)}
html,body,[class*=css]{font-family:'DM Sans',system-ui,sans-serif}
.block-container{max-width:1400px;padding:1.8rem 2.2rem 4rem}
#MainMenu,footer,header{visibility:hidden}
::selection{background:var(--accent-dim);color:#fff}

.hero{align-items:center;display:flex;gap:13px;margin-bottom:15px}
.mark{align-items:center;background:linear-gradient(135deg,var(--accent),var(--accent-deep));border-radius:14px;box-shadow:0 8px 24px rgba(241,132,85,.25);color:var(--mark-text);display:flex;font-size:23px;height:46px;justify-content:center;width:46px}
.hero h1{color:var(--text);font-size:30px;letter-spacing:-.9px;margin:0}
.hero p{color:var(--muted);font-size:13px;margin:4px 0 0}

/* category nav pills */
div[data-testid="stPills"]{margin:5px 0 10px}
div[data-testid="stPills"] button,div[data-testid="stSegmentedControl"] button,div[data-testid="stButtonGroup"] button{background:var(--surface)!important;border:1px solid var(--border)!important;border-radius:999px!important;color:var(--text)!important;font-size:13.5px!important;font-weight:600!important;padding:7px 17px!important}
div[data-testid="stPills"] button[aria-selected="true"],div[data-testid="stPills"] button[aria-pressed="true"],div[data-testid="stSegmentedControl"] button[aria-pressed="true"],div[data-testid="stButtonGroup"] button[data-selected="true"]{background:var(--accent)!important;border-color:var(--accent)!important;color:var(--mark-text)!important}
div[data-testid="stButtonGroup"] button p{color:inherit!important}
button[kind="secondary"]{background:var(--surface)!important;border-color:var(--border)!important;color:var(--text)!important}
div[data-baseweb="select"]>div,div[data-baseweb="input"]>div{background:var(--surface)!important;border-color:var(--border)!important;color:var(--text)!important}
div[data-baseweb="select"] *,div[data-baseweb="input"] input{color:var(--text)!important}
div[data-baseweb="popover"] ul{background:var(--surface)!important;color:var(--text)!important}
div[data-testid="stWidgetLabel"] p{color:var(--muted)!important}

.band{background:linear-gradient(135deg,var(--band-a),var(--band-b));border:1px solid var(--band-border);border-radius:18px;display:flex;align-items:flex-end;justify-content:space-between;gap:16px;margin:8px 0 16px;padding:22px 24px;position:relative;overflow:hidden;box-shadow:var(--shadow)}
.band::after{background:radial-gradient(circle at 88% 12%,rgba(240,168,105,.22),transparent 62%);content:'';inset:0;position:absolute}
.band>*{position:relative;z-index:1}
.band span{color:var(--accent);display:block;font-size:11px;font-weight:700;letter-spacing:.09em;text-transform:uppercase}
.band strong{color:var(--text);display:block;font-size:40px;letter-spacing:-1.6px;line-height:1.04;margin-top:5px}
.band small{color:var(--muted);font-size:11.5px;line-height:1.55;text-align:right}
.band small b{color:var(--text)}

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
.t thead th{background:var(--raised);border-bottom:1px solid var(--border);color:var(--muted);font-size:11px;font-weight:700;letter-spacing:.07em;padding:11px 10px;position:sticky;text-align:right;text-transform:uppercase;top:31px;z-index:3}
.t thead tr.superhead th{background:var(--surface);border-bottom:1px solid var(--border);color:var(--dim);font-size:9px;height:31px;letter-spacing:.11em;padding:7px 10px;text-align:center;top:0;z-index:5}
.t thead tr.superhead th:first-child{text-align:left}
.t thead th.itemh{left:0;text-align:left;z-index:4}
.t thead tr.superhead th.itemh{z-index:7}
.t thead th.store-ss{box-shadow:inset 0 3px 0 var(--good);color:var(--good)}
.t thead th.store-cs{box-shadow:inset 0 3px 0 #d98ad8;color:#d98ad8}
.t thead th.store-fp{box-shadow:inset 0 3px 0 #6db7ff;color:#6db7ff}
.t thead th.store-rm{box-shadow:inset 0 3px 0 var(--accent);color:var(--accent)}
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
.picks{display:grid;gap:12px;grid-template-columns:repeat(3,1fr);margin:12px 0 20px}
.pick{background:linear-gradient(180deg,var(--pick-top),var(--surface));border:1px solid var(--border);border-radius:14px;padding:16px}
.pick span{color:var(--accent);font-size:10.5px;font-weight:700;letter-spacing:.08em;text-transform:uppercase}
.pick strong{color:var(--text);display:block;font-size:16px;margin:7px 0 5px}
.pick p{color:var(--muted);font-size:11.5px;line-height:1.5;margin:0}
.travel-result{background:linear-gradient(135deg,var(--good-soft),var(--surface));border:1px solid var(--good-dim);border-radius:15px;margin:14px 0;padding:18px 20px}
.travel-result span{color:var(--muted);font-size:11px;text-transform:uppercase;letter-spacing:.08em}
.travel-result strong{color:var(--good);display:block;font-size:30px;letter-spacing:-1px;margin-top:4px}
.travel-result small{color:var(--muted)}
.deal-head{align-items:flex-end;display:flex;justify-content:space-between;gap:20px;margin:12px 0 14px}
.deal-head h2{color:var(--text);font-size:25px;letter-spacing:-.7px;margin:0}
.deal-head p{color:var(--muted);font-size:12px;line-height:1.5;margin:5px 0 0}
.deal-head small{color:var(--dim);font-size:10.5px;white-space:nowrap}
.tag{background:var(--soft);border-radius:999px;color:var(--accent);display:inline-block;font-size:9px;font-weight:700;letter-spacing:.06em;padding:4px 7px;text-transform:uppercase;white-space:nowrap}
.home-note{color:var(--dim);font-size:10.5px;line-height:1.6;margin:5px 1px}
.card-alert{background:var(--soft);border:1px solid var(--accent-dim);border-radius:11px;color:var(--muted);font-size:11px;line-height:1.55;margin:10px 0 14px;padding:11px 13px}
.card-alert b{color:var(--text)}
.miles-strip{align-items:center;background:linear-gradient(135deg,var(--miles-a),var(--miles-b));border:1px solid var(--miles-border);border-radius:15px;display:flex;gap:18px;justify-content:space-between;margin:13px 0 18px;padding:17px 19px}
.miles-strip span{color:var(--accent);font-size:10px;font-weight:700;letter-spacing:.07em;text-transform:uppercase}
.miles-strip strong{color:var(--text);display:block;font-size:17px;margin:4px 0}
.miles-strip small{color:var(--muted);font-size:10.5px}
.miles-strip a{background:var(--soft);border:1px solid var(--accent-dim);border-radius:8px;color:var(--accent);font-size:11px;font-weight:700;padding:8px 11px;text-decoration:none;white-space:nowrap}

@media(max-width:760px){
  .block-container{padding:.7rem .5rem 2rem}
  .hero{margin:0 .2rem 11px;gap:10px}.hero h1{font-size:23px}.hero p{font-size:11.5px}
  .mark{font-size:19px;height:39px;width:39px}
  .band{border-radius:12px;flex-direction:column;align-items:flex-start;gap:7px;padding:14px 16px}
  .band strong{font-size:32px}.band small{text-align:left}
  .delivery,.tiles{grid-template-columns:repeat(2,1fr)}
  .picks{grid-template-columns:1fr}
  .miles-strip{align-items:flex-start;flex-direction:column}
  .deal-head{align-items:flex-start;flex-direction:column;gap:5px}.deal-head h2{font-size:21px}
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
""", unsafe_allow_html=True)

if appearance == "Light":
    st.markdown("""
    <style>
    :root{
      --bg:#f5f3ee;--surface:#ffffff;--raised:#eeeae2;--border:#d9d3c8;
      --text:#1e2937;--muted:#5f6b78;--dim:#7b8490;
      --accent:#d85f32;--accent-deep:#bd4720;--accent-dim:#e9a083;
      --soft:rgba(216,95,50,.10);--softer:rgba(216,95,50,.05);
      --good:#187a58;--good-deep:#116143;--good-dim:#98cbb9;
      --good-soft:rgba(24,122,88,.10);--good-softer:rgba(24,122,88,.05);
      --shadow:0 16px 42px rgba(52,43,32,.10);
      --app-bg:radial-gradient(circle at 78% -10%,#fff1e6 0,transparent 34%),var(--bg);
      --band-a:#fff9f3;--band-b:#f3eee7;--band-border:#ddd3c5;
      --pick-top:#fffaf4;--flash-a:#fffdf9;--flash-b:#f7f3ed;--flash-hover:#c9b9a8;
      --miles-a:#f3fbf7;--miles-b:#ffffff;--miles-border:#b7d8ca;--mark-text:#ffffff;
      color-scheme:light;
    }
    .t thead th.savh{background:#e8f4ee}.pc.best .u{color:#357b62}
    </style>
    """, unsafe_allow_html=True)

brand_col, theme_col = st.columns([5, 1.25], vertical_alignment="center")
with brand_col:
    st.markdown(
        '<div class="hero"><div class="mark">&#129530;</div><div>'
        '<h1>Price Basket Kaki</h1><p>Your Singapore kaki for better prices, makan deals and family trips.</p>'
        '</div></div>',
        unsafe_allow_html=True,
    )
with theme_col:
    if hasattr(st, "segmented_control"):
        st.segmented_control("Appearance", ("Light", "Dark"), key="appearance", label_visibility="collapsed")
    else:
        st.radio("Appearance", ("Light", "Dark"), key="appearance", horizontal=True, label_visibility="collapsed")

# --------------------------------------------------- state + category nav ----
# Canonical values live under v_* keys so they survive a category switch even
# though the input widgets are only rendered for the category being viewed.
for index, (_, default_spend, default_pct, _note) in enumerate(SAVINGS_CATEGORIES):
    st.session_state.setdefault(f"v_spend_{index}", default_spend)
    st.session_state.setdefault(f"v_pct_{index}", default_pct)

VIEW_LABELS = {
    "🔥 Deals": "Overview",
    "🧺 Groceries": "Groceries",
    "🍜 Dining out": "Dining out",
    "✈️ Travel": "Travel",
}
VIEWS = tuple(VIEW_LABELS)
if hasattr(st, "pills"):
    view_label = st.pills("Category", VIEWS, default="🔥 Deals", label_visibility="collapsed")
else:  # streamlit < 1.40 fallback
    view_label = st.radio("Category", VIEWS, horizontal=True, label_visibility="collapsed")
view = VIEW_LABELS.get(view_label or "🔥 Deals", "Overview")


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


rows = category_rows()
total_saving = sum(r["saving"] for r in rows)

# ------------------------------------------------------------- overview ----
if view == "Overview":
    st.markdown(
        f'<div class="deal-head"><div><h2>Worth a look right now</h2>'
        '<p>A short list of live offers across groceries, dining and travel.</p></div>'
        f'<small>Checked {FLASH_DEALS_CHECKED}</small></div>',
        unsafe_allow_html=True,
    )
    deals_table = ('<div class="shell"><table class="t deals"><thead><tr>'
                   '<th>Category</th><th>Deal</th><th>Offer</th><th>Details</th>'
                   '<th>Validity</th><th>Source</th></tr></thead><tbody>')
    for category, eyebrow, title, offer, detail, valid, url, source in FLASH_DEALS:
        validity = f"Ends {valid}" if valid else "Live availability"
        deals_table += (
            f'<tr><td><span class="tag">{html.escape(category)}</span></td>'
            f'<td class="nm">{html.escape(title)}<em>{html.escape(eyebrow)}</em></td>'
            f'<td class="now">{html.escape(offer)}</td><td>{html.escape(detail)}</td>'
            f'<td><span class="ends ok">{html.escape(validity)}</span></td>'
            f'<td class="go"><a href="{url}" target="_blank" rel="noopener">'
            f'{html.escape(source)} &rarr;</a></td></tr>'
        )
    st.markdown(
        deals_table + '</tbody></table></div>'
        '<div class="home-note">Offers can sell out or change without notice. '
        'Open the original source to confirm price, availability and terms before buying.</div>',
        unsafe_allow_html=True,
    )

# ------------------------------------------------------ category detail ----
else:
    active = next(r for r in rows if r["name"] == view)
    index = active["index"]
    share = (active["saving"] / total_saving * 100) if total_saving else 0
    if view == "Travel":
        st.markdown(
            '<div class="band"><div><span>Family travel planner</span>'
            '<strong>Mar · Jun · Sep · Dec</strong></div>'
            '<small>Four MOE school-holiday planning blocks<br>'
            '<b>Flights + family hotels</b> kept together</small></div>',
            unsafe_allow_html=True,
        )
    else:
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

        head = ('<div class="shell"><table class="t"><thead>'
                '<tr class="superhead"><th class="itemh">Product</th>'
                '<th colspan="4">Compare supermarket prices</th><th>Potential saving</th></tr>'
                '<tr><th class="itemh">Item <em>pack size</em></th>')
        for key, label, _ in STORES:
            caption = "you pay now" if key == "rm" else "price &middot; per unit"
            head += f'<th class="store-{key}">{html.escape(label)}<em>{caption}</em></th>'
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
    dining_section = st.segmented_control(
        "Dining section", ("Deals by price", "My UOB Visa Infinite"),
        default="Deals by price", label_visibility="collapsed", key="dining_section",
    ) if hasattr(st, "segmented_control") else st.radio(
        "Dining section", ("Deals by price", "My UOB Visa Infinite"),
        horizontal=True, label_visibility="collapsed", key="dining_section",
    )
    if dining_section == "My UOB Visa Infinite":
        st.markdown(
            '<div class="card-alert"><b>Card assumed:</b> UOB Visa Infinite Metal Card. '
            'The Privilege Banking Visa Infinite card is a different product; tell me if that is the card you hold.</div>',
            unsafe_allow_html=True,
        )
        perks_html = ('<div class="shell"><table class="t deals"><thead><tr>'
                      '<th>Benefit</th><th>What you get</th><th>Important detail</th>'
                      '</tr></thead><tbody>')
        for label, value, detail in UOB_VI_PERKS:
            perks_html += (
                f'<tr><td class="nm">{html.escape(label)}</td>'
                f'<td class="now">{html.escape(value)}</td><td>{html.escape(detail)}</td></tr>'
            )
        st.markdown(perks_html + '</tbody></table></div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="sec"><h2>Published dining privileges</h2>'
            '<p>Use the card to pay and quote the offer when reserving</p></div>',
            unsafe_allow_html=True,
        )
        uob_table = ('<div class="shell"><table class="t deals"><thead><tr>'
                     '<th>Restaurant</th><th>Location</th><th>Benefit</th><th>Valid until</th><th></th>'
                     '</tr></thead><tbody>')
        uob_url = "https://www.uob.com.sg/personal/cards/privilege/visa-infinite-metal-card.page"
        for venue, location, benefit, validity in UOB_VI_DINING:
            uob_table += (
                f'<tr><td class="nm">{html.escape(venue)}</td>'
                f'<td>{html.escape(location)}</td><td class="now">{html.escape(benefit)}</td>'
                f'<td>{html.escape(validity)}</td>'
                f'<td class="go"><a href="{uob_url}" target="_blank" rel="noopener">UOB terms &rarr;</a></td></tr>'
            )
        st.markdown(uob_table + '</tbody></table></div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="note"><b>Worth remembering:</b> the S$654 annual fee is non-waivable. '
            'The card returns 25,000 renewal miles after the fee is paid, with another 15,000 miles '
            'after S$100,000 qualifying annual spend. Airport lounge access changed to 12 passes per '
            'membership year from 1 June 2026.</div>',
            unsafe_allow_html=True,
        )
        st.stop()

    st.markdown(
        '<div class="picks">'
        '<div class="pick"><span>Best free option</span><strong>Eatigo</strong>'
        '<p>Start here if your schedule is flexible: 10&ndash;50% off without paying for a membership.</p></div>'
        '<div class="pick"><span>Best for regular dining</span><strong>Burpple Beyond</strong>'
        '<p>Worth considering when you can naturally use 1-for-1 offers at least a few times a year.</p></div>'
        '<div class="pick"><span>Best stack</span><strong>Chope + dining card</strong>'
        '<p>Use the free booking layer, then pay with a card whose cap and minimum spend fit your actual habits.</p></div>'
        '</div>',
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

    def highest_price(text):
        """Highest dollar figure shown, used for descending deal order."""
        found = re.findall(r"\d+(?:\.\d+)?", text)
        return max(float(n) for n in found) if found else float("-inf")

    live = [(r, *end_state(r[6])) for r in DINING_RESTAURANTS]
    expired = [r for r, state, _ in live if state == "expired"]
    live = [(r, state, lbl) for r, state, lbl in live if state != "expired"]
    live.sort(key=lambda x: (highest_price(x[0][4]), x[0][0]), reverse=True)
    price_band = st.segmented_control(
        "Price per person before ++", ("All prices", "Under S$35", "S$35–49", "S$50+"),
        default="All prices", label_visibility="collapsed", key="dining_price_band",
    ) if hasattr(st, "segmented_control") else st.radio(
        "Price per person before ++", ("All prices", "Under S$35", "S$35–49", "S$50+"),
        horizontal=True, label_visibility="collapsed", key="dining_price_band",
    )
    if price_band == "Under S$35":
        live = [x for x in live if entry_price(x[0][4]) < 35]
    elif price_band == "S$35–49":
        live = [x for x in live if 35 <= entry_price(x[0][4]) < 50]
    elif price_band == "S$50+":
        live = [x for x in live if entry_price(x[0][4]) >= 50]

    st.markdown(
        '<div class="sec"><h2>Where to eat</h2>'
        f"<p>{len(live)} matching venues · highest listed deal price first</p></div>",
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

# -------------------------------------------------------- travel planner ----
elif view == "Travel":
    st.markdown(
        '<div class="sec"><h2>School-holiday trip finder</h2>'
        '<p>Pick the holiday first, then a part of the world</p></div>',
        unsafe_allow_html=True,
    )

    if st.session_state.get("travel_holiday") not in SCHOOL_HOLIDAY_WINDOWS:
        st.session_state["travel_holiday"] = "September"
    holiday_period = st.segmented_control(
        "Holiday block", tuple(SCHOOL_HOLIDAY_WINDOWS),
        label_visibility="collapsed", key="travel_holiday",
    ) if hasattr(st, "segmented_control") else st.radio(
        "Holiday block", tuple(SCHOOL_HOLIDAY_WINDOWS), horizontal=True,
        label_visibility="collapsed", key="travel_holiday",
    )
    holiday_period = holiday_period or "September"
    travel_group = st.selectbox(
        "Where to", ("All destinations", "Australia & NZ", "Japan", "Regional"),
        key="travel_group",
    )
    holiday_dates, holiday_note, _holiday_start, _holiday_end = SCHOOL_HOLIDAY_WINDOWS[holiday_period]
    date_index = tuple(SCHOOL_HOLIDAY_WINDOWS).index(holiday_period)
    st.markdown(
        f'<div class="miles-strip"><div><span>Official MOE window</span>'
        f'<strong>{html.escape(holiday_dates)}</strong>'
        f'<small>{html.escape(holiday_note)} · Suggested trips below leave a buffer before school restarts.</small></div>'
        '<a href="https://www.moe.gov.sg/calendar" target="_blank" rel="noopener">MOE calendar &rarr;</a></div>',
        unsafe_allow_html=True,
    )

    matching_fares = [
        idea for idea in TRIP_IDEAS
        if travel_group == "All destinations" or idea[0] == travel_group
    ]
    fares_html = ('<div class="shell"><table class="t deals"><thead><tr>'
                  '<th>Region</th><th>Destination & dates</th><th>Return fare</th>'
                  '<th>Family hotel</th><th>Why it works</th><th>Book</th>'
                  '</tr></thead><tbody>')
    for group, destination, price, nights, why, url in matching_fares:
        suggested_dates = TRIP_DATES[destination][date_index]
        hotel_name, hotel_area, hotel_fit, hotel_url = HOTEL_IDEAS[destination]
        fares_html += (
            f'<tr><td><span class="tag">{html.escape(group)}</span></td>'
            f'<td class="nm">{html.escape(destination)}'
            f'<em>{html.escape(suggested_dates)} · {html.escape(nights)}</em></td>'
            f'<td class="now">{html.escape(price)}</td>'
            f'<td class="nm">{html.escape(hotel_name)}<em>{html.escape(hotel_area)} · '
            f'{html.escape(hotel_fit)}</em></td><td>{html.escape(why)}</td>'
            f'<td class="go"><a href="{url}" target="_blank" rel="noopener">Flight &rarr;</a><br>'
            f'<a href="{hotel_url}" target="_blank" rel="noopener">Hotel &rarr;</a></td></tr>'
        )
    st.markdown(fares_html + '</tbody></table></div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="miles-strip"><div><span>Best use of miles this month</span>'
        '<strong>30% off KrisFlyer Saver awards</strong>'
        '<small>Examples from Singapore: Kuala Lumpur or Penang from 5,600 miles; '
        'Bangkok or Phuket from 9,100 miles one-way. Book by 31 Aug for September travel.</small></div>'
        '<a href="https://www.singaporeair.com/en_UK/sg/plan-travel/promotions/global/kf/kf-promo/kfescapes/" '
        'target="_blank" rel="noopener">View award list &rarr;</a></div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="note"><b>Fare check:</b> Prices were checked {TRAVEL_DEALS_CHECKED}. '
        'The dates are family-friendly suggestions inside the MOE holiday, not a guarantee that the headline fare '
        'is available on those exact days. Hotel picks link to official room pages; confirm occupancy for your '
        'children’s ages before paying. Compare the final total including bags, seats, meals and local taxes.</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="sec"><h2>Travel savings planner</h2>'
        '<p>Build a realistic annual target from habits you would actually use</p></div>',
        unsafe_allow_html=True,
    )

    trip_col, timing_col = st.columns([1, 1])
    with trip_col:
        trips = st.number_input("Trips per year", 1, 20, 3, 1)
    with timing_col:
        style = st.selectbox("Typical travel style", ("Value-conscious", "Comfort", "Premium"))

    st.markdown(
        '<div class="shell"><table class="t deals"><thead><tr>'
        '<th>Priority</th><th>Action</th><th>Why</th></tr></thead><tbody>'
        '<tr><td><span class="tag">Do first</span></td><td class="nm">Compare total trip cost</td>'
        '<td>Include baggage, seats, transport, taxes and FX fees. The cheapest headline fare often is not cheapest.</td></tr>'
        '<tr><td><span class="tag">Highest leverage</span></td><td class="nm">Move the dates</td>'
        '<td>A small date shift usually beats points optimisation. Search a window before choosing exact leave dates.</td></tr>'
        '<tr><td><span class="tag">Avoid</span></td><td class="nm">Blind loyalty</td>'
        '<td>Points are useful only after price, schedule and cancellation terms are competitive.</td></tr>'
        '</tbody></table></div>', unsafe_allow_html=True,
    )

    st.markdown('<div class="sec"><h2>Your savings levers</h2><p>Select only the changes you can sustain</p></div>', unsafe_allow_html=True)
    chosen_rate = 0.0
    for lever_index, (label, rate, explanation) in enumerate(TRAVEL_LEVERS):
        enabled = st.checkbox(
            f"{label} · about {rate:g}%",
            value=lever_index in (0, 1, 2),
            help=explanation,
            key=f"travel_lever_{lever_index}",
        )
        if enabled:
            chosen_rate += rate

    style_factor = {"Value-conscious": 1.0, "Comfort": 0.85, "Premium": 0.7}[style]
    modelled_rate = min(chosen_rate * style_factor, 15)
    modelled_saving = active["spend"] * modelled_rate / 100
    per_trip = modelled_saving / trips
    st.markdown(
        f'<div class="travel-result"><span>Modelled annual opportunity</span>'
        f'<strong>{sgd(modelled_saving, 0)}</strong>'
        f'<small>{modelled_rate:.1f}% of travel spend &middot; about {sgd(per_trip, 0)} per trip</small></div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="note"><b>Reality check:</b> your headline assumption is '
        f'{active["pct"]}% ({sgd(active["saving"], 0)} per year). The habits selected above model '
        f'{modelled_rate:.1f}% ({sgd(modelled_saving, 0)}). Use the lower figure for planning; '
        'it is better to capture a modest target consistently than count sale prices you would not actually book.</div>',
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
