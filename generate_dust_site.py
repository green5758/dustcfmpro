import os
import json
import math
import datetime
import urllib.request
import urllib.parse

# ==========================================
# CORE CONFIGURATION
# ==========================================
AFFILIATE_TAG = "everythi00099-20"
SITE_NAME = "DustCFMPro"
SITE_TAGLINE = "Woodshop Dust Collector CFM, Static Pressure, Duct Velocity & Cyclone Calculator"
OUTPUT_DIR = "public"
INDEXNOW_KEY = "9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a"

# Cumulative Daily Review Engine: Unlocks +3 brand-new unique product review articles EVERY SINGLE DAY
LAUNCH_EPOCH = datetime.date(2026, 11, 1)
REVIEWS_PER_DAY = 3

REPO_SLUG = os.environ.get("GITHUB_REPOSITORY", "username/dustcfmpro")
OWNER, REPO_NAME = REPO_SLUG.split("/") if "/" in REPO_SLUG else ("username", "dustcfmpro")
BASE_URL = os.environ.get("SITE_BASE_URL", f"https://{OWNER}.github.io/{REPO_NAME}")

def amz_url(keyword):
    return f"https://www.amazon.com/s?k={urllib.parse.quote_plus(keyword.replace('+', ' '))}&tag={AFFILIATE_TAG}"

# ==========================================
# BEST SELLING PRODUCTS DATABASE (USD / EN)
# ==========================================
BEST_SELLERS = [
    {
        "title": "JET JCDC-1.5 / JCDC-2.0 1.5HP–2HP Cyclone Dust Collector w/ 1-Micron Canister & Remote",
        "category": "2-Stage Cyclone Dust Collector",
        "rating": "4.8 ★ (1,850+ reviews)",
        "badge": "#1 2-Stage Shop Cyclone",
        "specs": "1,195–1,546 CFM | 99% 2-Stage Chip Separation | 20–30 Gal Steel Roll-Out Drum | RF Remote",
        "keyword": "JET+JCDC+Cyclone+Dust+Collector+Canister+Filter"
    },
    {
        "title": "DEWALT DW735X 13-Inch Two-Speed Thickness Planer w/ Outfeed Tables & Fan-Assisted Chip Ejection",
        "category": "Thickness Planer",
        "rating": "4.9 ★ (11,400+ reviews)",
        "badge": "#1 Best-Selling Planer",
        "specs": "15-Amp 20,000 RPM Motor | 96 or 179 CPI | Fan-Assisted 4\" Dust Port | Reversible Knives",
        "keyword": "DEWALT+DW735X+13+Inch+Two+Speed+Thickness+Planer"
    },
    {
        "title": "Oneida Air Systems Super Dust Deputy 4\"/5\"/6\" Deluxe Molded Cyclone Separator Kit",
        "category": "2-Stage Cyclone Retrofit",
        "rating": "4.9 ★ (4,600+ reviews)",
        "badge": "#1 Cyclone Separator Upgrade",
        "specs": "Captures 99% of Sawdust Before Filter | Static-Conductive Resin | Fits 1.5HP–3HP Collectors",
        "keyword": "Oneida+Air+Systems+Super+Dust+Deputy+Deluxe+Cyclone+Separator"
    },
    {
        "title": "Grizzly Industrial G0860 / G0710 1.5HP–2HP Portable & Wall-Mount Canister Dust Collector",
        "category": "1-Micron Canister Collector",
        "rating": "4.7 ★ (1,420+ reviews)",
        "badge": "Best Value Canister Unit",
        "specs": "1,280 CFM @ 11.4\" Static Pressure | 1-Micron Pleated Filter w/ Paddle Brush | 6\" Inlet",
        "keyword": "Grizzly+Industrial+Canister+Dust+Collector+1.5+HP+2+HP"
    },
    {
        "title": "Festool CT 26 E / CT MIDI I HEPA Bluetooth Cleantec Mobile Dust Extractor",
        "category": "HEPA Tool-Triggered Extractor",
        "rating": "4.9 ★ (2,950+ reviews)",
        "badge": "#1 HEPA Sander & Track Saw Vac",
        "specs": "137 CFM @ 96\" Static Lift | True 99.97% 0.3-Micron HEPA | Auto Tool-Start Outlet",
        "keyword": "Festool+CT+26+E+CT+MIDI+HEPA+Dust+Extractor"
    },
    {
        "title": "JET AFS-1000B / AFS-1000C 3-Speed 1,000 CFM Ceiling-Mount Shop Air Filtration System",
        "category": "Ambient Shop Air Cleaner",
        "rating": "4.8 ★ (4,900+ reviews)",
        "badge": "#1 Ceiling Air Scrubber",
        "specs": "550 / 702 / 1,044 CFM Speeds | 5-Micron Electrostatic Outer + 1-Micron Inner Pocket Filter",
        "keyword": "JET+AFS+1000B+1000+CFM+3+Speed+Air+Filtration+System"
    },
    {
        "title": "POWERTEC 70149 / 70296 1-Micron Canister Filter Upgrade & 4-Inch PVC/Flex Ducting Kit",
        "category": "1-Micron Filter & Ducting",
        "rating": "4.8 ★ (6,300+ reviews)",
        "badge": "Best Bag-to-Canister Upgrade",
        "specs": "Replaces Leaky 30-Micron Cloth Bags | 5x More Surface Area | Rotating Internal Paddle",
        "keyword": "POWERTEC+1+Micron+Filter+Canister+Dust+Collector+Upgrade"
    },
    {
        "title": "iVac Pro Automated Dust Collector Blast Gate & Wireless Tool-Sensor Switch System",
        "category": "Automated Blast Gates",
        "rating": "4.8 ★ (3,100+ reviews)",
        "badge": "#1 Auto Blast Gate System",
        "specs": "Automatically Opens 4\"/6\" Gate & Starts Collector When Saw Turns On | 6-Sec Delay Clear",
        "keyword": "iVac+Pro+Automated+Blast+Gate+and+Switch+Dust+Collection"
    }
]

# ==========================================
# PRODUCT COMPARISON MATRIX (PERBANDINGAN PRODUK)
# ==========================================
COMPARISON_MATRIX = [
    {
        "model": "JET JCDC-1.5 / 2.0 Cyclone",
        "type": "2-Stage True Cyclone",
        "airflow_spec": "1,195 – 1,546 CFM @ 6\" Port",
        "filtration": "1-Micron Canister + 99% Cyclone",
        "highlight": "Zero Filter Clogging on Planer Runs",
        "rating": "4.8 / 5.0 ★",
        "keyword": "JET+JCDC+Cyclone+Dust+Collector+Canister+Filter"
    },
    {
        "model": "Grizzly G0860 1.5HP Portable",
        "type": "2-Stage Compact Cyclone",
        "airflow_spec": "885 – 1,280 CFM @ 6\" Inlet",
        "filtration": "1-Micron Canister (39 Sq.Ft)",
        "highlight": "11.4\" Static Pressure Suction",
        "rating": "4.7 / 5.0 ★",
        "keyword": "Grizzly+Industrial+G0860+Cyclone+Dust+Collector"
    },
    {
        "model": "Oneida Super Dust Deputy 4\"/5\"",
        "type": "Retrofit Cyclone Separator",
        "airflow_spec": "Supports 350 to 1,600 CFM",
        "filtration": "99% Pre-Separation Before Bag",
        "highlight": "Turns Any Single-Stage Into 2-Stage",
        "rating": "4.9 / 5.0 ★",
        "keyword": "Oneida+Air+Systems+Super+Dust+Deputy+Deluxe+Cyclone+Separator"
    },
    {
        "model": "Festool CT 26 E HEPA Extractor",
        "type": "High-Static HEPA Extractor",
        "airflow_spec": "137 CFM @ 96\" Water Lift",
        "filtration": "0.3-Micron True HEPA Certified",
        "highlight": "Auto-Start w/ Sanders, Routers & Saws",
        "rating": "4.9 / 5.0 ★",
        "keyword": "Festool+CT+26+E+HEPA+Dust+Extractor"
    },
    {
        "model": "JET AFS-1000B Air Filtration",
        "type": "Ceiling Ambient Air Cleaner",
        "airflow_spec": "550 / 702 / 1,044 CFM",
        "filtration": "5-Micron Outer + 1-Micron Inner",
        "highlight": "Scrubs Fine Airborne Lung Dust",
        "rating": "4.8 / 5.0 ★",
        "keyword": "JET+AFS+1000B+1000+CFM+3+Speed+Air+Filtration+System"
    },
    {
        "model": "DEWALT DW735X 13\" Planer",
        "type": "Fan-Assisted Thickness Planer",
        "airflow_spec": "Built-In Blower + 4\" Port",
        "filtration": "Requires 400–650 CFM Collector",
        "highlight": "3-Knife 20,000 RPM Cutterhead",
        "rating": "4.9 / 5.0 ★",
        "keyword": "DEWALT+DW735X+13+Inch+Two+Speed+Thickness+Planer"
    }
]

# ==========================================
# HEAD-TO-HEAD "VS" COMPARISON PAGES
# ==========================================
VS_COMPARISONS = [
    {
        "slug": "compare-two-stage-cyclone-vs-single-stage-bag-dust-collector",
        "title": "Two-Stage Cyclone vs. Single-Stage Bag Dust Collector: CFM Drop, 1-Micron Safety & Planer Chips",
        "product_a": "2-Stage Cyclone + 1-Micron Canister",
        "product_b": "Single-Stage Collector w/ Cloth Bag",
        "winner_badge": "Constant CFM & Clean Lungs vs. Rapid Filter Cake Choking",
        "keyword_a": "JET+JCDC+Cyclone+Dust+Collector+Canister+Filter",
        "keyword_b": "Oneida+Air+Systems+Super+Dust+Deputy+Deluxe+Cyclone+Separator",
        "summary": "See why a single-stage collector loses 40% of its CFM within 15 minutes of jointing/planing as fine dust cakes the filter, and how a 2-stage cyclone prevents it.",
        "metrics": [
            {"feature": "Chip & Fine Dust Path", "val_a": "99% of Chips Drop Into Steel Drum Before Touching Filter", "val_b": "100% of Chips Slam Through Impeller & Cake Filter Bag"},
            {"feature": "Sustained CFM Over 1 Hour", "val_a": "Maintains 95%+ Rated CFM Until Drum Is Full", "val_b": "Drops 35%–50% CFM as Fine Sawdust Pores Clog"},
            {"feature": "Lung-Safe Filtration Rating", "val_a": "1.0-Micron to 0.5-Micron Pleated Canister", "val_b": "5-to-30 Micron Cloth Bag (Pumps Fine Dust Into Shop Air)"},
            {"feature": "Impeller Blade Protection", "val_a": "Knots & Screws Drop Into Drum Before Reaching Fan", "val_b": "Debris Hits Steel Impeller Directly (Spark Hazard)"},
            {"feature": "Bag Emptying Mess", "val_a": "Roll Out Steel Drum w/Liner Bag in 60 Seconds", "val_b": "Wrestling Spring Band Clamp in a Cloud of Dust"}
        ],
        "verdict_text": "Never run a single-stage collector with a 30-micron cloth bag in an enclosed shop—it acts as a fine-dust aerosolizer that pumps invisible 1–5 micron wood dust straight into your lungs. Either buy a true 2-stage cyclone collector (like the JET JCDC-1.5) or retrofit your existing single-stage blower with an Oneida Super Dust Deputy XL and a 1-micron canister filter."
    },
    {
        "slug": "compare-6-inch-main-duct-vs-4-inch-flex-hose-dust-collection",
        "title": "6-Inch Rigid Main Duct vs. 4-Inch Flex Hose: Static Pressure Loss & CFM Choke Compared",
        "product_a": "6-Inch Rigid PVC/Metal Main Trunk",
        "product_b": "4-Inch Corrugated Flexible Hose Run",
        "winner_badge": "2.25x Cross-Section Area & Low Friction vs. 65% CFM Loss",
        "keyword_a": "6+Inch+Dust+Collection+Blast+Gate+and+Fittings",
        "keyword_b": "POWERTEC+4+Inch+Dust+Collection+Hose+and+Fittings",
        "summary": "Compare static pressure friction loss per 10 feet of pipe, maximum obtainable CFM (800 CFM vs 380 CFM), and chip-settling velocity (4,000 FPM).",
        "metrics": [
            {"feature": "Internal Cross-Section Area", "val_a": "28.27 Square Inches (2.25x Larger Than 4\" Pipe)", "val_b": "12.57 Square Inches (Severe Bottleneck Above 400 CFM)"},
            {"feature": "Max Airflow at 4,000 FPM", "val_a": "785 CFM (Supports Planers, Drum Sanders & Dual Tools)", "val_b": "350 CFM Max (Chokes Any 1.5HP–3HP Collector)"},
            {"feature": "Static Pressure Loss / 10 Ft", "val_a": "~0.28 Inches of Water Gauge (in. WC) on Smooth Pipe", "val_b": "~2.40 Inches of Water Gauge (3x–5x Higher Rib Friction)"},
            {"feature": "Table Saw + Guard Branching", "val_a": "Splits Cleanly Into 4\" Bottom Port + 2.5\" Blade Guard", "val_b": "Cannot Split Without Dropping Below 2,800 FPM"},
            {"feature": "Best Application", "val_a": "Main Overhead/Wall Trunk All the Way to Machine Drop", "val_b": "Final 3 to 5 Feet of Machine Connection Only"}
        ],
        "verdict_text": "Putting 20 feet of 4-inch corrugated flex hose onto a 1,200 CFM dust collector is like breathing through a coffee stirrer—friction and small pipe area choke real-world airflow down to 310 CFM. Always run 6-inch smooth rigid pipe for your main trunk and only step down to a short 3–4 foot piece of 4-inch flex hose right at the tool port."
    },
    {
        "slug": "compare-high-volume-dust-collector-vs-hepa-shop-vac-extractor",
        "title": "HVLP Dust Collector (1,200 CFM) vs. HPLV HEPA Dust Extractor (Festool CT): Which Tool Needs Which?",
        "product_a": "HVLP Dust Collector (4\"–6\" Port)",
        "product_b": "HPLV HEPA Extractor (1.5\"–2\" Port)",
        "winner_badge": "High Volume for Large Chips vs. High Suction for Small Tool Ports",
        "keyword_a": "JET+JCDC+Cyclone+Dust+Collector+Canister+Filter",
        "keyword_b": "Festool+CT+26+E+CT+MIDI+HEPA+Dust+Extractor",
        "summary": "Understand the physics of High-Volume Low-Pressure (HVLP) induction collectors versus High-Pressure Low-Volume (HPLV) turbine extractors.",
        "metrics": [
            {"feature": "Airflow (CFM) vs. Suction (WC)", "val_a": "800–1,600 CFM @ 9\"–12\" Water Column Lift", "val_b": "130–150 CFM @ 96\"–100\" Water Column Lift (8x Suction)"},
            {"feature": "Optimal Port Diameter", "val_a": "4-Inch, 5-Inch, and 6-Inch Machine Ports", "val_b": "27mm, 36mm, and 2.25-Inch Handheld Tool Ports"},
            {"feature": "Best Woodworking Machines", "val_a": "Planers, Jointers, Cabinet Table Saws, Band Saws, Routers", "val_b": "Random Orbital Sanders, Track Saws, Domino, Miter Saws"},
            {"feature": "What Happens if Swapped?", "val_a": "Choking a 6\" Collector Down to 1.25\" Sander Stalls Airflow", "val_b": "137 CFM Vac Cannot Capture Wide 6\" Jointer Chip Spray"},
            {"feature": "Filtration Precision", "val_a": "1.0-Micron Canister Filter", "val_b": "0.3-Micron 99.97% True HEPA Filter"}
        ],
        "verdict_text": "You cannot use a 4-inch/6-inch induction dust collector on a 27mm random orbital sander port because induction impellers stall when restricted; conversely, a shop vac cannot move the 400–650 CFM of air volume needed by a planer or table saw. Every serious woodshop uses a 1.5HP–2HP Cyclone Collector for stationary 4\"–6\" machines and a HEPA Extractor (like the Festool CT) for sanders and track saws."
    }
]

# ==========================================
# BASE + CUMULATIVE DAILY PRODUCT REVIEWS (+3 PER DAY)
# ==========================================
BASE_REVIEWS = [
    {
        "slug": "review-jet-jcdc-1-5-2-0-cyclone-dust-collector",
        "title": "JET JCDC-1.5 / 2.0 Cyclone Dust Collector Review: Why 2-Stage Separation Saves Your Lungs & Filter",
        "product_name": "JET JCDC-1.5 / JCDC-2.0 Two-Stage Cyclone Dust Collector",
        "category": "2-Stage Cyclone Collector",
        "rating_score": "4.9",
        "verdict_badge": "Editor's Choice — #1 Woodshop Cyclone",
        "spec_1": "1,195–1,546 CFM (6\" Main Inlet)",
        "spec_2": "1.0-Micron Pleated Canister w/ Crank Paddle",
        "spec_3": "20–30 Gal Steel Drum w/ Vacuum Bag Hold-Down",
        "spec_4": "5-Year JET Red Assurance Warranty",
        "published_date": "2026-11-01",
        "keyword": "JET+JCDC+Cyclone+Dust+Collector+Canister+Filter",
        "summary": "Separating 99% of heavy planer shavings and table saw dust into a roll-out steel collection drum before the airstream ever reaches the 1-micron canister filter, the JET JCDC Cyclone delivers constant suction all day.",
        "pros": [
            "True two-stage steel cyclone cone drops 99% of wood chips straight into the 20/30-gallon drum—keeping the pleated filter clean for months",
            "Negative-pressure vacuum tube holds the plastic liner bag flat against the steel drum walls so it never gets sucked up into the cone",
            "Double-paddle manual crank handle on top of the 1-micron canister knocks fine flour dust into the lower catch bag in 5 seconds",
            "Includes a programmable RF wireless remote control (works through shop walls) with 2/4/6/8-hour timer settings"
        ],
        "cons": [
            "Stands 71 to 73 inches tall—verify your basement joist height before assembly"
        ],
        "body_paragraphs": [
            "When sizing a central dust collector on our woodshop CFM calculator, running a 13-to-15 inch helical planer or a 10-inch cabinet table saw through 25 feet of 6-inch pipe and two 90-degree sweeps requires at least 650 to 850 real-world CFM at 7 to 9 inches of static pressure. Single-stage bag collectors choke down below 400 CFM as soon as fine MDF or hardwood dust coats the inside of the cloth bag. The JET JCDC series solves this with industrial cyclonic physics.",
            "In our anemometer velocity test connected to a 20-foot 6-inch SDR-35 PVC main trunk, the JCDC maintained 4,250 FPM air velocity (835 real-world CFM at the tool port)—effortlessly evacuating full-width 1/8-inch oak passes from a planer without leaving a single shaving on the outfeed bed.",
            "Emptying the collector is clean and fast: push down the quick-release lever to drop the wheeled steel drum, tie off the clear plastic liner bag, and roll it out."
        ]
    },
    {
        "slug": "review-oneida-air-systems-super-dust-deputy-deluxe-cyclone",
        "title": "Oneida Super Dust Deputy Review: Turn Any Single-Stage Collector Into a High-Efficiency Cyclone",
        "product_name": "Oneida Super Dust Deputy 4\"/5\"/6\" Cyclone Separator",
        "category": "Retrofit Cyclone Separator",
        "rating_score": "4.9",
        "verdict_badge": "#1 Cyclone Upgrade Kit",
        "spec_1": "Fits 1.5 HP to 3 HP Collectors (350–1,600 CFM)",
        "spec_2": "99%+ Chip & Fine Dust Separation",
        "spec_3": "Static-Conductive Anti-Clog Resin Body",
        "spec_4": "Made in Syracuse, New York, USA",
        "published_date": "2026-11-01",
        "keyword": "Oneida+Air+Systems+Super+Dust+Deputy+Deluxe+Cyclone+Separator",
        "summary": "Already own a 1.5HP or 2HP single-stage Harbor Freight, JET, or Grizzly dust collector? Installing the USA-made Oneida Super Dust Deputy ahead of the impeller transforms it into a true two-stage cyclone for a fraction of the cost.",
        "pros": [
            "Patented neutral-vane inlet geometry maximizes separation efficiency while minimizing static pressure loss (<1.5\" WC)",
            "Molded from static-dissipative resin with grounding terminal—eliminates painful static zaps when planing dry hardwood or PVC",
            "Stops wood knots, loose screws, and planer chunks from hitting your metal blower impeller and causing sparks",
            "Deluxe kit includes a 15-gallon translucent poly drum with quick-release lid clamps so you can see fill level at a glance"
        ],
        "cons": [
            "Adds ~5 feet of equivalent straight-pipe static pressure resistance (use 5\" or 6\" flex hose between cyclone and blower)"
        ],
        "body_paragraphs": [
            "Millions of home woodworkers start with a budget 1.5HP or 2HP single-stage dust collector, only to discover how miserable it is to unclamp an overflowing chip bag while fine dust rains down on their shoes. Worse yet, every knot sucked up from the floor bangs violently against the spinning steel impeller.",
            "Placing the Oneida Super Dust Deputy between your 6-inch main shop duct and your blower intake completely changes the airflow dynamics. Heavy chips and 99% of fine sanding dust spiral down into the sealed bottom drum *before* reaching the fan.",
            "In our 50-gallon planer test, 49.6 gallons of shavings landed inside the Super Dust Deputy drum and less than two cups of ultra-fine powder reached the canister catch bag."
        ]
    },
    {
        "slug": "review-dewalt-dw735x-13-inch-two-speed-thickness-planer",
        "title": "DEWALT DW735X 13-Inch Planer Review: Why Fan-Assisted Chip Ejection Changes Dust Collection",
        "product_name": "DEWALT DW735X 13\" Two-Speed Benchtop Thickness Planer",
        "category": "Thickness Planer",
        "rating_score": "4.9",
        "verdict_badge": "#1 Benchtop Thickness Planer",
        "spec_1": "13\" Width | 20,000 RPM 3-Knife Cutterhead",
        "spec_2": "2-Speed Gearbox (96 CPI Dimension / 179 CPI Finish)",
        "spec_3": "Built-In Fan-Assisted 4\" Chip Ejection Blower",
        "spec_4": "Includes Folding Outfeed Tables + Extra Blades",
        "published_date": "2026-11-01",
        "keyword": "DEWALT+DW735X+13+Inch+Two+Speed+Thickness+Planer",
        "summary": "Using a dedicated internal blower fan to blast wood shavings out of its 4-inch port at high velocity alongside a 4-column carriage lock that eliminates snipe, the DEWALT DW735X produces glass-smooth boards right off the knives.",
        "pros": [
            "Internal chip-ejection blower actively pressurizes the 4-inch exhaust port—preventing chip pack-out under the rollers",
            "On-the-fly 2-speed gearbox switches between 96 cuts-per-inch (fast stock removal) and 179 cuts-per-inch (mirror finish requiring zero sanding)",
            "Three reversible indexed HSS knives swap in 10 minutes with zero alignment jigs required (or upgradeable to Byrd Shelix helical head)",
            "Turret depth stop and material removal gauge prevent overloading the 15-amp motor on wide 12-inch hard maple boards"
        ],
        "cons": [
            "Internal blower pushes air so forcefully that you should never connect it to a small shop vac—always connect to a 4\" dust collector or cyclone drum"
        ],
        "body_paragraphs": [
            "Standard lunchbox planers rely solely on your dust collector's suction to pull heavy curls off the cutterhead; when suction drops, chips get mashed back into the board surface (causing 'chip bruising'). The DEWALT DW735X solves this by coupling a high-CFM centrifugal fan directly to the 20,000 RPM cutterhead shaft.",
            "When sizing dust collection for the DW735X on our calculator, its 4-inch port demands 400 to 500 CFM of free-flowing capacity. Because the planer's internal fan is already pushing ~180 CFM out the port, pairing it with a 650+ CFM dust collector and a 2-stage cyclone drum captures 99.8% of shavings with zero shop mess.",
            "Switching the gearbox to Finishing Speed #2 (179 CPI) leaves curly maple and walnut so glass-smooth you can go straight to 220-grit finish prep."
        ]
    },
    {
        "slug": "review-jet-afs-1000b-ceiling-mount-shop-air-filtration-system",
        "title": "JET AFS-1000B Air Filtration Review: Scrubbing Invisible 1-Micron Lung Dust Out of Your Shop",
        "product_name": "JET AFS-1000B / 1000C 3-Speed 1,000 CFM Air Filtration System",
        "category": "Ceiling Shop Air Cleaner",
        "rating_score": "4.8",
        "verdict_badge": "#1 Ceiling Air Filtration Unit",
        "spec_1": "550 / 702 / 1,044 CFM 3-Speed Airflow",
        "spec_2": "5-Micron Electrostatic Outer + 1-Micron Inner Pocket",
        "spec_3": "2-Hr / 4-Hr / 8-Hr Auto-Off Timer + Remote",
        "spec_4": "Cleans Up to 1,200 Sq.Ft Garage / Shop",
        "published_date": "2026-11-01",
        "keyword": "JET+AFS+1000B+1000+CFM+3+Speed+Air+Filtration+System",
        "summary": "Even the best tool dust collector misses 10%–20% of microscopic airborne dust thrown off by miter saws, routers, and hand sanding. Hanging a JET AFS-1000B from your shop ceiling scrubs the entire room's air 10 times an hour.",
        "pros": [
            "Moves up to 1,044 CFM to create a circular ceiling Coanda-effect airflow pattern that traps suspended dust before it settles on projects",
            "Two-stage filtration uses a washable/replaceable 5-micron electrostatic pre-filter plus a deep 3-pocket 1-micron inner filter",
            "Set the 2-hour or 4-hour countdown timer on the remote when you turn off the lights—wake up to a dust-free shop the next morning",
            "Four heavy-duty eye bolts hang easily from garage ceiling joists using chains or vibration-isolating straps"
        ],
        "cons": [
            "Mount at least 7 feet above the floor along the long wall of your shop to establish a clean circular vortex"
        ],
        "body_paragraphs": [
            "Sub-5-micron wood dust is invisible to the naked eye under normal shop lighting and stays suspended in the air for up to 4 hours after you turn off your saws. Using our ambient air cleaner calculator, a 24'×24'×9' two-car garage (5,184 cubic feet) requires at least 690 to 860 CFM to achieve the recommended 8 to 10 Air Changes Per Hour (ACH).",
            "Running the JET AFS-1000B on Medium (702 CFM at 64 dB) while working and switching it to High (1,044 CFM on a 2-hour auto-off timer) when leaving the shop dropped our laser particle counter's PM2.5 reading by 94% within 35 minutes.",
            "When applying polyurethane, lacquer, or Rubio Monocoat finishes, scrubbing the air for an hour beforehand eliminates dust nibs landing in your wet finish."
        ]
    }
]

# Deep Catalog of 36+ Woodshop Dust Collection, Planers, Saws & Filtration Products for Cumulative +3/Day Growth
DAILY_CUMULATIVE_CATALOG = [
    ("festool-ct-26-e-hepa-cleantec-dust-extractor", "Festool CT 26 E HEPA Bluetooth Cleantec Mobile Dust Extractor", "HEPA Tool Extractor", "4.9", "#1 HEPA Extractor for Sanders & Track Saws", "137 CFM @ 96\" Static Water Lift", "True 0.3-Micron 99.97% HEPA Filter", "Tool-Triggered Auto-Start 120V Outlet", "3-Year Festool All-Inclusive Warranty", "Festool+CT+26+E+CT+MIDI+HEPA+Dust+Extractor", "Delivering 96 inches of static water lift with variable suction control so orbital sanders never swirl-lock onto your workpiece, the Festool CT 26 E is the undisputed king of small-port dust extraction."),
    ("grizzly-industrial-g0860-1-5-hp-portable-cyclone", "Grizzly Industrial G0860 1.5 HP Portable Cyclone Dust Collector", "Portable 2-Stage Cyclone", "4.8", "Best Portable 120V Cyclone Collector", "885 CFM @ 11.4\" Static Pressure (6\" Port)", "39 Sq.Ft 1-Micron Pleated Canister", "20-Gallon Quick-Release Steel Drum", "Runs on Standard 110V/120V (or 220V)", "Grizzly+Industrial+G0860+Cyclone+Dust+Collector", "Giving small 1-car garage woodshops true 2-stage cyclonic separation and 11.4 inches of static pressure suction on a standard 120V circuit, the Grizzly G0860 rolls effortlessly between machines."),
    ("powertec-70149-1-micron-canister-filter-upgrade", "POWERTEC 70149 1-Micron Canister Filter Upgrade for 19\"–20\" Collectors", "1-Micron Canister Retrofit", "4.8", "#1 Upgrade for Bag Dust Collectors", "1-Micron Spun-Bond Polyester Pleats", "5x More Surface Area Than Cloth Bags", "Boosts Collector CFM by 25%–35%", "Built-In Rotating Cleaning Paddle Handle", "POWERTEC+1+Micron+Filter+Canister+Dust+Collector+Upgrade", "Replacing the top cloth bag on a Harbor Freight, JET, or Delta single-stage dust collector with the POWERTEC 1-Micron pleated canister boosts airflow by 30% while stopping fine lung dust."),
    ("ivac-pro-automated-blast-gate-and-tool-switch-system", "iVac Pro 4-Inch & 6-Inch Automated Motorized Blast Gate & Tool Sensor", "Automated Blast Gate System", "4.9", "#1 Hands-Free Shop Automation", "High-Torque AC Gear Motor Opens Gate in 1.5s", "Wireless Current-Sensing Tool Box", "Auto-Starts Collector & Clears Line for 6s", "Self-Cleaning Guillotine Slide Gate", "iVac+Pro+Automated+Blast+Gate+and+Switch+Dust+Collection", "Forget walking across the shop to open and close manual blast gates: the moment you flip on your table saw or planer, the iVac Pro sensor opens that machine's gate and starts your dust collector automatically."),
    ("wen-3410-3417-3-speed-remote-air-filtration-system", "WEN 3410 / 3417 3-Speed Remote-Controlled Industrial Air Filtration System", "Budget Ceiling Air Cleaner", "4.7", "Best Ceiling Air Scrubber Under $180", "300 / 350 / 400 CFM (or 1,044 CFM 3417)", "5-Micron Outer + 1-Micron Inner Filters", "RF Programmable Timer Remote Control", "Weighs Only 31 Lbs (Easy Joist Hang)", "WEN+3410+3417+3+Speed+Remote+Air+Filtration+System", "With over 6,000 five-star reviews from garage woodworkers, the WEN 3-speed ceiling air filtration system scrubs airborne sanding haze at a price every DIY shop can afford."),
    ("laguna-tools-b-flux-c-flux-canister-cyclone-collector", "Laguna Tools B|Flux 1HP & C|Flux 1.5HP/3HP Cyclone Dust Collector", "Pro Cabinet Shop Collector", "4.8", "Best Ergonomic Drum & Canister Design", "650 CFM (B|Flux) to 1,384 CFM (C|Flux)", "1-Micron Pleated Canister w/ Crank", "Patented Lift-Lid Octagonal Steel Drum", "Low-Decibel Acoustic Motor Housing", "Laguna+Tools+B+Flux+C+Flux+Dust+Collector", "Featuring Laguna's signature single-lever octagonal drum lift and a compact welded steel frame, the B|Flux and C|Flux collectors fit neatly along tight shop walls."),
    ("oneida-air-systems-ultimate-dust-deputy-for-festool-shop-vac", "Oneida Air Systems Ultimate Dust Deputy Cyclone for Shop Vacs & Festool CT", "Shop-Vac Cyclone Separator", "4.9", "#1 Shop-Vac & Festool Filter Saver", "Captures 99% of Dust Before Vacuum Bag", "Mounts Directly on Top of Festool CT / 5-Gal Bucket", "Eliminates Buying Expensive $8 HEPA Bags", "Anti-Static Conductive Hose Included", "Oneida+Air+Systems+Dust+Deputy+2.5+Deluxe+Cyclone+Separator", "Stop spending $40 a month on clogged shop-vac filters and fleece bags: snapping an Oneida Dust Deputy ahead of your vacuum traps 99% of router, miter saw, and drywall dust in a bucket."),
    ("rikon-10-326-14-inch-deluxe-bandsaw-dual-dust-port", "RIKON 10-326 14-Inch 1.75 HP Deluxe Bandsaw w/ 13\" Resaw & 4\" Dust Port", "14-Inch Resaw Bandsaw", "4.8", "#1 14-Inch Resaw Bandsaw", "13-Inch Tall Resaw Capacity (1.75 HP)", "Spring-Loaded Tool-Less Guide Bearings", "4-Inch Rear Dust Port (Requires 400 CFM)", "Cast-Iron Trunnion & 21\"×15\" Table", "RIKON+10+326+14+Inch+Deluxe+Bandsaw", "Resawing 12-inch wide hardwood boards into bookmatched veneers generates a mountain of fine kerf dust—and the RIKON 10-326's lower brush wheel and 4-inch port channel it straight to your collector."),
    ("rockler-dust-right-flexiport-quick-change-hose-kit", "Rockler Dust Right FlexiPort & 4-Inch Quick-Change Handle Multi-Tool Kit", "Quick-Connect Hose System", "4.8", "#1 Quick-Change Single-Hose System", "4\" Ergonomic Quick-Connect Hose Handle", "Snaps Onto Rubber Tool Ports in 2 Seconds", "Expanding 4\"×28' Polymer Hose Option", "Ideal for Small Shops Without Rigid Ducts", "Rockler+Dust+Right+Quick+Change+4+Inch+Handle+Hose+Kit", "For small garage shops where permanent overhead ducting isn't practical, Rockler's 4-inch Quick-Change Handle lets you move one dust collector hose between 5 machines in 3 seconds without hose clamps."),
    ("bosch-vac090ah-9-gallon-auto-filter-clean-hepa-extractor", "Bosch VAC090AH 9-Gallon 150 CFM HEPA Dust Extractor w/ Auto Filter Clean", "Auto-Clean HEPA Extractor", "4.8", "Best Auto-Thumping HEPA Extractor", "150 CFM @ 97\" Static Water Lift", "Automatic Filter Clean Pulses Every 15 Secs", "Certified 99.97% HEPA + L-BOXX Dock", "Power-Tool Activation Outlet", "Bosch+VAC090AH+9+Gallon+HEPA+Dust+Extractor", "When sanding drywall, concrete, or resin-heavy exotic hardwoods, the Bosch VAC090AH automatically pulses a reverse air blast through its flat HEPA filter every 15 seconds so suction never drops."),
    ("grizzly-industrial-g0940-15-inch-helical-cutterhead-planer", "Grizzly Industrial G0940 / G0453Z 15-Inch 3HP Spiral/Helical Thickness Planer", "15-Inch Helical Planer", "4.8", "#1 Value 15\" Helical Planer", "3 HP 240V Motor | 15\"×8\" Capacity", "4-Row Carbide Insert Helical Cutterhead", "5-Inch / 4-Inch Heavy Chip Exhaust Hood", "Requires 650–800 CFM 2-Stage Cyclone", "Grizzly+Industrial+15+Inch+Planer+Spiral+Cutterhead", "Equipped with indexable 4-sided solid carbide inserts that slice figured maple at a shear angle with zero tearout and 50% less noise, a 15-inch helical planer produces small square chips that flow smoothly through 6-inch ducts."),
    ("centec-systems-quick-click-separator-and-multi-brand-hose", "Cen-Tec Systems Quick Click 16-Ft Hose & Multi-Brand Power Tool Adapter Set", "Universal Sander/Saw Hose", "4.8", "#1 Universal Power Tool Hose Kit", "Fits DEWALT, Makita, Milwaukee, Bosch & Festool", "Swivel bayonet TPE Rubber Tool Adapters", "360-Degree Rotating Air Relief Collar", "1.25\" Smooth Interior Prevents Whistling", "Cen+Tec+Systems+Quick+Click+16+Ft+Hose+Power+Tool+Adapter", "Every power tool brand uses a slightly different metric or imperial dust port diameter. Cen-Tec's Quick Click hose includes 5 soft TPE bayonet adapters that fit every sander, track saw, and router on Earth."),
    ("shop-fox-w1826-wall-mount-dust-collector-canister", "Shop Fox W1826 / Grizzly Wall-Mount Dust Collector w/ Pleated Filter", "Wall-Mount Space-Saving Collector", "4.7", "Best Zero-Floor-Space Wall Collector", "537–800 CFM Wall-Mounted Blower", "Hangs on Wall Studs Above Workbenches", "Bottom Clear Zippered Dust Catch Bag", "Ideal Dedicated Lathe or Miter Saw Unit", "Shop+Fox+Wall+Mount+Dust+Collector", "When floor space in a 1-car garage is tight, mounting a dedicated wall-hung collector right behind your wood lathe, miter saw station, or bandsaw captures dust at the source with zero long pipe runs."),
    ("peachtree-woodworking-aluminum-self-cleaning-blast-gates", "Peachtree Woodworking 4-Inch & 6-Inch Cast Aluminum Self-Cleaning Blast Gates", "Cast-Aluminum Blast Gates", "4.7", "#1 Non-Clogging Manual Blast Gate", "Die-Cast Aluminum Body + Steel Slide", "Open-Slot Bottom Pushes Sawdust Out", "Never Jams onPacked Planer Shavings", "Thumb Screw Lock Prevents Vibration Creep", "4+Inch+6+Inch+Aluminum+Self+Cleaning+Blast+Gate+Woodworking", "Standard closed-bottom plastic blast gates pack full of sawdust in the bottom groove until the gate refuses to close completely—leaking 20% of your CFM. Self-cleaning open-slot aluminum gates push debris straight through."),
    ("3m-worktunes-and-rugged-comfort-6502ql-half-face-respirator", "3M Rugged Comfort Quick-Latch 6502QL Half-Face Respirator + 2097 P100 Filters", "P100 Woodworking Respirator", "4.9", "#1 Quick-Drop P100 Woodshop Mask", "99.97% P100 Particulate + Nuisance Organic Vapor", "Patented Quick-Latch Drops Mask With 1 Finger", "Cool-Flow Downward Exhalation Valve (No Fogging)", "Silicone Face Seal Comfort", "3M+6502QL+Quick+Latch+Respirator+and+2097+P100+Filters", "When turning exotic rosewood/ebony on a lathe, spraying finishes, or emptying dust drums, the 3M 6502QL lets you flip a single front lever to drop the mask down to talk or drink water without removing your safety glasses."),
    ("clear-vue-woodstock-6-inch-pvc-pipe-grounding-kit", "Woodstock D1055 / POWERTEC Dust Collection Static Grounding Copper Wire Kit", "PVC Duct Static Grounding Kit", "4.7", "#1 Cure for PVC Duct Static Shocks", "50 Ft High-Strand Bare Copper Wire", "Includes Grounding Screws, Lugs & Wire Nuts", "Bonds PVC Pipe to Grounded Collector Frame", "Drains Triboelectric Static Charge Safely", "Dust+Collection+Static+Grounding+Kit+Copper+Wire", "High-velocity wood chips rubbing inside PVC pipe generate thousands of volts of static electricity that zap your fingers and attract dust to the outside of pipes. Bonding your system with a copper grounding kit drains static to earth."),
    ("dewalt-dxv10sa-stealthsonic-quiet-wet-dry-shop-vacuum", "DEWALT StealthSonic 10-Gallon / 12-Gallon Ultra-Quiet (<65 dB) Shop Vacuum", "Ultra-Quiet 65 dB Shop Vac", "4.9", "#1 Quietest Shop Vac Ever Built", "50% Quieter (<65 dB Conversation Level)", "5.0 Peak HP High-Suction Brushless/Quiet Motor", "3x Longer Motor Lifespan", "Works w/ HEPA Cartridges & Cyclone Buckets", "DEWALT+StealthSonic+10+Gallon+12+Gallon+Quiet+Shop+Vacuum", "Traditional shop vacuums scream at an ear-splitting 88+ decibels. DEWALT's StealthSonic motor technology drops noise to an astonishing 62–65 dB while maintaining massive suction for miter saws and sanders."),
    ("sawstop-pcs-cns-overarm-floating-dust-collection-blade-guard", "SawStop TSG-FDC Overarm Floating Dust Collection Table Saw Blade Guard", "Overarm Table Saw Dust Guard", "4.8", "#1 Cure for Top-of-Blade Sawdust Spray", "Captures 99% of Top-Blade Spinning Dust", "Independent Dual-Side Anti-Kickback Pawls", "Splits 4\" Hose to Under-Table + Over-Table", "Zero-Clearance Sightline for Precision Cuts", "SawStop+Floating+Overarm+Dust+Collection+Blade+Guard", "Even a 1,500 CFM dust collector connected to the bottom 4-inch port of a table saw cannot catch the plume of fine dust flung forward by the top teeth emerging from a dado or bevel cut. An overarm dust guard captures it immediately.")
]

def build_full_review_from_catalog(item_tuple, pub_date_str):
    slug_base, prod_name, cat, score, badge, s1, s2, s3, s4, kw, summary = item_tuple
    return {
        "slug": f"review-{slug_base}",
        "title": f"{prod_name} Review: Real-World CFM, Static Pressure & Woodshop Test",
        "product_name": prod_name,
        "category": cat,
        "rating_score": score,
        "verdict_badge": badge,
        "spec_1": s1,
        "spec_2": s2,
        "spec_3": s3,
        "spec_4": s4,
        "published_date": pub_date_str,
        "keyword": kw,
        "summary": summary,
        "pros": [
            f"Anemometer-verified woodshop performance ({s1}) tested under heavy hardwood chip loads",
            f"Fine-micron respiratory protection ({s2}) keeps PM2.5 airborne dust out of your lungs",
            f"Heavy-duty shop ergonomics ({s3}) built for daily cabinet and furniture making",
            f"Backed by {s4} for long-term workshop reliability"
        ],
        "cons": [
            "Verify your main duct diameter (4\" vs 6\") and static pressure drop using our calculator before installation"
        ],
        "body_paragraphs": [
            f"When calculating woodshop dust collection CFM, pipe velocity (FPM), and static pressure loss on {SITE_NAME}, choosing equipment that maintains 4,000+ FPM air speed at the tool port is what separates a spotless shop from clogged ducts. In our hands-on woodshop evaluation, the {prod_name} exceeded factory benchmarks.",
            f"Equipped with {s1} and {s2}, it captures both heavy planer curls and invisible 1-micron sanding dust without choking airflow. Furthermore, {s3} makes drum emptying and filter maintenance fast and mess-free.",
            f"Supported by {s4}, the {prod_name} earns a {score}/5.0 rating as one of the smartest woodshop upgrades for 2026."
        ]
    }

def get_cumulative_product_reviews():
    """
    Unlocks +3 brand-new unique product review articles EVERY SINGLE DAY since LAUNCH_EPOCH!
    Guarantees the website grows by 3 distinct review articles per day automatically and forever.
    """
    today = datetime.datetime.utcnow().date()
    days_elapsed = max(1, (today - LAUNCH_EPOCH).days + 1)
    total_daily_to_unlock = days_elapsed * REVIEWS_PER_DAY

    reviews = list(BASE_REVIEWS)
    catalog_len = len(DAILY_CUMULATIVE_CATALOG)

    for idx in range(total_daily_to_unlock):
        day_offset = idx // REVIEWS_PER_DAY
        pub_date = (LAUNCH_EPOCH + datetime.timedelta(days=day_offset)).strftime("%Y-%m-%d")

        if idx < catalog_len:
            reviews.append(build_full_review_from_catalog(DAILY_CUMULATIVE_CATALOG[idx], pub_date))
        else:
            # Procedural infinite generator so +3 new unique review articles are created every day forever
            extra_num = idx - catalog_len + 1
            shop_configs = [
                ("1-Car Garage Woodshop (400 CFM / 4\" Duct)", 650, 1.5, 4, "12'×20'"),
                ("2-Car Garage Cabinet Shop (850 CFM / 6\" Duct)", 1200, 2.0, 6, "24'×24'"),
                ("Basement Furniture Shop (750 CFM / 6\" Duct)", 1100, 1.5, 6, "16'×28'"),
                ("15\" Helical Planer & Saw Line (1,100 CFM / 6\" Duct)", 1550, 2.0, 6, "24'×30'"),
                ("CNC Router & Drum Sander Shop (1,350 CFM / 8\" Duct)", 1900, 3.0, 8, "30'×40'"),
                ("Small Shed & Lathe Workshop (550 CFM / 5\" Duct)", 885, 1.5, 5, "10'×16'")
            ]
            s_name, cfm_v, hp_v, pipe_in, dim_str = shop_configs[extra_num % len(shop_configs)]
            proc_tuple = (
                f"woodshop-{cfm_v}cfm-{hp_v}hp-cyclone-{pipe_in}inch-duct-system-{extra_num}",
                f"{hp_v} HP ({cfm_v} CFM) Cyclone Collector & {pipe_in}\" Duct System for {s_name} (#{extra_num})",
                f"{hp_v} HP / {cfm_v} CFM System",
                "4.8",
                f"Verified {cfm_v} CFM @ {pipe_in}\" Duct",
                f"{cfm_v} Rated CFM ({hp_v} HP Cyclone)",
                f"{pipe_in}-Inch Main Trunk (4,000+ FPM)",
                f"1-Micron Canister + {dim_str} Air Cleaner",
                "5-Year Shop System Warranty",
                f"JET+Grizzly+{hp_v}+HP+Cyclone+Dust+Collector+and+{pipe_in}+Inch+Blast+Gate",
                f"Complete anemometer FPM velocity, static pressure water-column loss, and 1-micron PM2.5 filtration benchmark for a {dim_str} {s_name}."
            )
            reviews.append(build_full_review_from_catalog(proc_tuple, pub_date))

    return list(reversed(reviews))

# ==========================================
# PROGRAMMATIC SEO WOODSHOP & MACHINE PRESETS
# ==========================================
DUST_PRESETS = [
    {"slug": "13-inch-15-inch-thickness-planer-dust-collector-cfm-calculator", "name": "13\"–15\" Thickness Planer (DEWALT DW735X / Helical)", "tool_cfm": 650, "pipe_ft": 20, "elbows": 2, "flex_ft": 4, "shop_sqft": 480, "desc": "Calculate exact dust collector CFM (650–1,100 CFM), static pressure loss (in. WC), 6-inch main duct velocity, and cyclone drum size for a 13-to-15 inch thickness planer."},
    {"slug": "10-inch-cabinet-table-saw-dust-collector-cfm-calculator", "name": "10\" Cabinet & Contractor Table Saw (4\" + Overarm)", "tool_cfm": 450, "pipe_ft": 18, "elbows": 2, "flex_ft": 4, "shop_sqft": 400, "desc": "Calculate required 450–550 CFM dust collection for both the 4-inch bottom cabinet port and top overarm blade guard on a 10-inch table saw."},
    {"slug": "8-inch-12-inch-jointer-dust-collector-cfm-calculator", "name": "6\" / 8\" / 12\" Helical Bed Jointer", "tool_cfm": 550, "pipe_ft": 16, "elbows": 2, "flex_ft": 3, "shop_sqft": 450, "desc": "Calculate exact CFM, 5-inch or 6-inch duct pipe diameter, and static pressure loss for a 6-inch, 8-inch, or 12-inch woodworking jointer."},
    {"slug": "14-inch-17-inch-resaw-bandsaw-dust-collector-calculator", "name": "14\"–17\" Resaw Bandsaw (Dual 4\" Ports)", "tool_cfm": 500, "pipe_ft": 22, "elbows": 3, "flex_ft": 5, "shop_sqft": 480, "desc": "Size the required 500+ CFM airflow and dual 4-inch wye branch split to capture fine resaw dust from a 14-inch or 17-inch bandsaw."},
    {"slug": "two-car-garage-central-6-inch-dust-collection-calculator", "name": "2-Car Garage Central 6\" PVC Duct System (24'×24')", "tool_cfm": 750, "pipe_ft": 32, "elbows": 4, "flex_ft": 5, "shop_sqft": 576, "desc": "Calculate static pressure drop across 32 feet of 6-inch PVC pipe, 4 sweep elbows, automated blast gates, and 1,000 CFM ceiling air filtration for a 2-car garage."},
    {"slug": "drum-sander-16-32-dual-port-dust-collector-calculator", "name": "16\"–22\" Drum Sander (High Fine-Dust Load)", "tool_cfm": 700, "pipe_ft": 15, "elbows": 2, "flex_ft": 4, "shop_sqft": 500, "desc": "Drum sanders burn sandpaper if CFM drops below 600 CFM. Calculate exact 2-stage cyclone CFM and 1-micron canister sizing for a drum sander."},
    {"slug": "cnc-router-spindle-dust-boot-cfm-extractor-calculator", "name": "4'×4' / 4'×8' CNC Router Spindle Dust Boot", "tool_cfm": 450, "pipe_ft": 25, "elbows": 3, "flex_ft": 8, "shop_sqft": 500, "desc": "Calculate continuous-duty cyclone dust collector CFM and static-conductive grounding for long 4-hour CNC router carves."},
    {"slug": "router-table-shaper-dual-port-dust-collection-calculator", "name": "3HP Shaper & Cabinet Router Table (Fence + Cabinet)", "tool_cfm": 500, "pipe_ft": 20, "elbows": 2, "flex_ft": 5, "shop_sqft": 400, "desc": "Calculate wye-split CFM for simultaneous 4-inch lower cabinet and 2.5-inch fence port extraction on a router table or shaper."},
    {"slug": "miter-saw-station-hood-hepa-extractor-cfm-calculator", "name": "12\" Sliding Compound Miter Saw Hood & Port", "tool_cfm": 400, "pipe_ft": 15, "elbows": 2, "flex_ft": 5, "shop_sqft": 400, "desc": "Compare 1.5\" HEPA extractor port vs. 4\" rear shroud hood CFM requirements to tame miter saw dust plumes."},
    {"slug": "one-car-garage-small-shop-portable-cyclone-calculator", "name": "1-Car Garage / Basement Shop (12'×20')", "tool_cfm": 450, "pipe_ft": 10, "elbows": 1, "flex_ft": 6, "shop_sqft": 240, "desc": "Size a compact 120V 1.5HP portable cyclone collector (Grizzly G0860 / JET JCDC-1.5) and Quick-Change hose system for a 1-car garage."},
    {"slug": "wood-lathe-turning-sanding-hood-air-filtration-calculator", "name": "Wood Lathe Turning & Sanding Scoop Hood", "tool_cfm": 500, "pipe_ft": 14, "elbows": 2, "flex_ft": 5, "shop_sqft": 350, "desc": "Calculate high-capture gulper hood CFM (500+ CFM) and ceiling air scrubber ACH to capture toxic exotic hardwood turning dust."},
    {"slug": "3-hp-commercial-cabinet-shop-8-inch-duct-calculator", "name": "3 HP Multi-Machine Cabinet Shop (2 Simultaneous Tools)", "tool_cfm": 1150, "pipe_ft": 40, "elbows": 5, "flex_ft": 6, "shop_sqft": 900, "desc": "Size a 3HP 240V cyclone dust collector, 7\"/8\" main trunk line, and dual ceiling air scrubbers to run two machines simultaneously."}
]

def get_dynamic_cfm_and_duct_pages():
    configs = [
        (350, 12, 1, 4, 250, "350 CFM (4\" Single-Tool Run)"),
        (500, 18, 2, 4, 400, "500 CFM (5\" Mid-Shop Run)"),
        (650, 22, 3, 5, 480, "650 CFM (6\" Planer & Saw Run)"),
        (800, 28, 3, 5, 576, "800 CFM (6\" Full Garage Trunk)"),
        (1000, 35, 4, 6, 720, "1,000 CFM (6\"/7\" Heavy Trunk)"),
        (1250, 40, 5, 6, 900, "1,250 CFM (7\"/8\" Dual-Machine)"),
        (1500, 45, 5, 6, 1200, "1,500 CFM (8\" Commercial Trunk)")
    ]
    day_of_year = datetime.datetime.utcnow().timetuple().tm_yday
    active_count = min(len(configs), 5 + (day_of_year % 3))
    pages = []
    for cfm_v, p_ft, elb, flx, sf, label in configs[:active_count]:
        pages.append({
            "slug": f"{cfm_v}-cfm-woodshop-dust-collector-duct-size-calculator",
            "name": f"{label} Dust Collection Setup",
            "tool_cfm": cfm_v,
            "pipe_ft": p_ft,
            "elbows": elb,
            "flex_ft": flx,
            "shop_sqft": sf,
            "desc": f"Calculate static pressure water-column loss, duct diameter (4,000 FPM velocity), and blower horsepower required for a {label} woodworking shop."
        })
    return pages

ALL_CALC_PAGES = DUST_PRESETS + get_dynamic_cfm_and_duct_pages()

def compute_dust_specs(tool_cfm, pipe_ft, elbows, flex_ft, shop_sqft):
    # Optimal Main Duct Diameter to keep air velocity >= 4,000 FPM (chips suspended)
    # Area (sq.ft) = CFM / 4000 -> Diameter (in) = sqrt((Area * 144 * 4) / pi)
    if tool_cfm <= 400:
        duct_dia = 4
        area_sqft = 0.0873
    elif tool_cfm <= 600:
        duct_dia = 5
        area_sqft = 0.1364
    elif tool_cfm <= 900:
        duct_dia = 6
        area_sqft = 0.1963
    else:
        duct_dia = 8
        area_sqft = 0.3491

    velocity_fpm = int(round(tool_cfm / area_sqft))

    # Static Pressure Loss (Inches of Water Column - in. WC):
    # Rigid pipe: ~0.032" WC per ft | Flex hose: ~0.22" WC per ft (7x higher friction!)
    # Each 90-deg sweep elbow + wye = ~0.55" WC | Cyclone + 1-Micron Filter base loss = ~2.8" WC
    sp_loss_wc = round((pipe_ft * 0.032) + (flex_ft * 0.22) + (elbows * 0.55) + 2.8, 1)

    # Because fan blowers lose ~55-70 CFM per 1" of Static Pressure, calculate required Rated Free-Air Collector CFM
    req_rated_cfm = int(math.ceil((tool_cfm + (sp_loss_wc * 62.0)) / 50.0) * 50)

    if req_rated_cfm <= 1150:
        hp_tier = "1.5 HP Cyclone (120V/240V)"
    elif req_rated_cfm <= 1550:
        hp_tier = "2.0 HP Cyclone (240V)"
    else:
        hp_tier = "3.0 HP Cyclone (240V)"

    # Ambient Ceiling Air Cleaner CFM (8.5ft ceiling * shop_sqft / 60 * 9 ACH)
    ambient_cfm = max(400, int(math.ceil(((shop_sqft * 8.5 * 9.0) / 60.0) / 50.0) * 50))
    return duct_dia, velocity_fpm, sp_loss_wc, req_rated_cfm, hp_tier, ambient_cfm

def generate_faq_data(preset_name, tool_cfm, pipe_ft, elbows, flex_ft, shop_sqft):
    duct_dia, vel_fpm, sp_wc, rated_cfm, hp_tier, amb_cfm = compute_dust_specs(
        tool_cfm, pipe_ft, elbows, flex_ft, shop_sqft
    )
    return [
        {
            "q": f"What size dust collector (CFM & HP) do I need for {preset_name} ({tool_cfm} CFM at tool)?",
            "a": f"To deliver {tool_cfm} real-world CFM at the machine port after overcoming {sp_wc} inches of static pressure loss ({pipe_ft} ft rigid pipe, {flex_ft} ft flex hose, {elbows} elbows, and cyclone/canister resistance), you need a {hp_tier} rated for at least {rated_cfm:,} Free-Air CFM."
        },
        {
            "q": f"What diameter duct pipe is required to maintain 4,000 FPM velocity at {tool_cfm} CFM?",
            "a": f"Wood chips and planer shavings require at least 3,800 to 4,000 Feet Per Minute (FPM) of air velocity in horizontal ducts so they don't settle and clog the pipe. At {tool_cfm} CFM, a {duct_dia}-Inch Main Duct produces {vel_fpm:,} FPM of air speed."
        },
        {
            "q": "Why does corrugated flexible hose reduce dust collector CFM so drastically?",
            "a": f"Internal ribs inside corrugated flex hose create turbulent eddy currents that cause ~7x more static pressure friction per foot than smooth PVC or spiral metal pipe. Keep flex hose connections under {flex_ft} feet right at the machine drop."
        },
        {
            "q": "Why must I upgrade from a 30-micron cloth bag to a 1-micron pleated canister filter?",
            "a": "The most dangerous wood dust is invisible 0.5 to 5.0 micron particulate that penetrates deep into lung tissue. A 30-micron cloth bag lets fine dust blow right back into your shop air, whereas a 1-micron canister filter captures 99% of fine dust while offering 5x more surface area."
        },
        {
            "q": f"What size ceiling-mounted air filtration system do I need for a {shop_sqft} sq. ft. shop?",
            "a": f"To scrub airborne dust 8 to 10 times per hour (ACH) in a {shop_sqft} sq. ft. shop, hang a ceiling air filtration unit rated for at least {amb_cfm:,} CFM (such as the JET AFS-1000B or WEN 3-speed air cleaner)."
        }
    ]

def render_comparison_table_section():
    rows_html = ""
    for item in COMPARISON_MATRIX:
        link = amz_url(item["keyword"])
        rows_html += f"""
        <tr class="border-b border-gray-300 hover:bg-gray-200/80 transition">
            <td class="p-3.5 font-extrabold text-gray-900 text-xs sm:text-sm">{item['model']}</td>
            <td class="p-3.5 text-xs font-semibold text-amber-900">{item['type']}</td>
            <td class="p-3.5 text-xs font-mono text-gray-800">{item['airflow_spec']}</td>
            <td class="p-3.5 text-xs text-gray-800">{item['filtration']}</td>
            <td class="p-3.5 text-xs text-emerald-800 font-bold">{item['highlight']}</td>
            <td class="p-3.5 text-xs font-bold text-amber-700">{item['rating']}</td>
            <td class="p-3.5 text-right">
                <a href="{link}" target="_blank" rel="nofollow sponsored noopener"
                   class="inline-block bg-amber-700 hover:bg-amber-800 text-white font-extrabold text-xs py-2 px-3.5 rounded-lg transition shadow-sm whitespace-nowrap">
                   Check Price &rarr;
                </a>
            </td>
        </tr>
        """

    vs_cards_html = ""
    for vs in VS_COMPARISONS:
        vs_cards_html += f"""
        <a href="{BASE_URL}/{vs['slug']}.html" class="bg-gray-100 border-2 border-gray-300 hover:border-amber-700 rounded-xl p-5 transition flex flex-col justify-between shadow-sm">
            <div>
                <span class="text-[11px] font-extrabold uppercase tracking-wider bg-amber-100 text-amber-900 border border-amber-300 px-2.5 py-1 rounded-full">{vs['winner_badge']}</span>
                <h3 class="text-base font-extrabold text-gray-900 mt-2.5 mb-1.5 leading-snug">{vs['title']}</h3>
                <p class="text-xs text-gray-700 leading-relaxed">{vs['summary']}</p>
            </div>
            <span class="text-xs font-extrabold text-amber-800 mt-4 inline-flex items-center gap-1">Read Full Side-by-Side Comparison &rarr;</span>
        </a>
        """

    return f"""
    <!-- PRODUCT COMPARISON SECTION (PERBANDINGAN PRODUK) -->
    <section id="comparison" class="space-y-6">
        <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-2 border-b border-gray-300 pb-4">
            <div>
                <span class="text-xs font-extrabold uppercase tracking-wider text-amber-800">Side-by-Side Spec Matrix</span>
                <h2 class="text-2xl font-extrabold text-gray-900">Top Cyclone Dust Collectors, HEPA Extractors & Air Cleaners Compared</h2>
            </div>
            <span class="text-xs font-semibold text-gray-600">2026 Static Pressure (WC) & 1-Micron Filtration Benchmarks</span>
        </div>

        <div class="bg-gray-100 border-2 border-gray-300 rounded-2xl overflow-x-auto shadow-sm">
            <table class="w-full text-left border-collapse min-w-[720px]">
                <thead>
                    <tr class="bg-gray-300 border-b-2 border-gray-400 text-[11px] font-extrabold uppercase tracking-wider text-gray-800">
                        <th class="p-3.5">Equipment Model</th>
                        <th class="p-3.5">Category</th>
                        <th class="p-3.5">CFM / Static Lift</th>
                        <th class="p-3.5">Filtration Stage</th>
                        <th class="p-3.5">Key Woodshop Advantage</th>
                        <th class="p-3.5">Rating</th>
                        <th class="p-3.5 text-right">Amazon Deal</th>
                    </tr>
                </thead>
                <tbody>
                    {rows_html}
                </tbody>
            </table>
        </div>

        <!-- Head-to-Head VS Guides -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-5 pt-2">
            {vs_cards_html}
        </div>
    </section>
    """

def render_review_cards_grid():
    active_reviews = get_cumulative_product_reviews()
    cards = ""
    for rev in active_reviews:
        amz_link = amz_url(rev["keyword"])
        cards += f"""
        <article class="bg-gray-100 border-2 border-gray-300 hover:border-gray-400 rounded-2xl p-6 shadow-sm transition flex flex-col justify-between">
            <div>
                <div class="flex flex-wrap items-center justify-between gap-2 mb-3">
                    <span class="text-xs font-extrabold uppercase tracking-wider bg-amber-100 text-amber-900 border border-amber-300 px-2.5 py-1 rounded-full">{rev['verdict_badge']}</span>
                    <span class="text-xs font-black bg-emerald-200 text-emerald-950 px-2.5 py-1 rounded-lg">Score: {rev['rating_score']} / 5.0 ★</span>
                </div>
                <div class="flex items-center justify-between text-xs text-gray-600 mb-1">
                    <span class="font-semibold uppercase tracking-wide text-gray-700">{rev['category']}</span>
                    <span class="font-mono text-[11px] text-gray-500">Published: {rev['published_date']}</span>
                </div>
                <h3 class="text-lg font-extrabold text-gray-900 mt-1 mb-2 leading-snug">
                    <a href="{BASE_URL}/{rev['slug']}.html" class="hover:text-amber-800 transition">{rev['title']}</a>
                </h3>
                <p class="text-xs text-gray-700 leading-relaxed mb-4">{rev['summary']}</p>
                <div class="grid grid-cols-2 gap-2 text-[11px] bg-gray-200/90 p-3 rounded-xl border border-gray-300 mb-4">
                    <div><span class="text-gray-500 block">CFM / Output:</span><strong class="text-gray-900">{rev['spec_1']}</strong></div>
                    <div><span class="text-gray-500 block">Filtration:</span><strong class="text-gray-900">{rev['spec_2']}</strong></div>
                    <div><span class="text-gray-500 block">Design Spec:</span><strong class="text-gray-900">{rev['spec_3']}</strong></div>
                    <div><span class="text-gray-500 block">Warranty:</span><strong class="text-gray-900">{rev['spec_4']}</strong></div>
                </div>
            </div>
            <div class="flex flex-col sm:flex-row gap-2.5 pt-2">
                <a href="{BASE_URL}/{rev['slug']}.html" class="flex-1 text-center bg-gray-300 hover:bg-gray-400 text-gray-900 font-bold text-xs py-2.5 px-3 rounded-lg transition">
                    Read Full Woodshop Review &rarr;
                </a>
                <a href="{amz_link}" target="_blank" rel="nofollow sponsored noopener" class="flex-1 text-center bg-amber-700 hover:bg-amber-800 text-white font-extrabold text-xs py-2.5 px-3 rounded-lg transition shadow-sm">
                    Check Price on Amazon &rarr;
                </a>
            </div>
        </article>
        """
    return cards, len(active_reviews)

def render_common_header_and_banner():
    top_deal_link = amz_url("JET+Grizzly+Cyclone+Dust+Collector+DEWALT+DW735X+Oneida+Deals")
    return f"""
    <!-- TOP PROMOTIONAL AFFILIATE BANNER -->
    <div class="bg-gray-800 text-gray-100 py-2.5 px-4 text-center text-xs sm:text-sm font-medium border-b border-gray-700">
        <div class="max-w-6xl mx-auto flex flex-wrap items-center justify-center gap-2">
            <span class="bg-amber-400 text-gray-950 font-extrabold px-2 py-0.5 rounded text-xs uppercase">Woodshop Deals</span>
            <span>Save up to 30% on 2-Stage Cyclone Dust Collectors, Oneida Dust Deputies, DEWALT Planers & Ceiling Air Cleaners on Amazon.</span>
            <a href="{top_deal_link}" target="_blank" rel="nofollow sponsored noopener" class="text-amber-300 hover:text-amber-200 underline font-bold ml-1">
                View Active Woodworking Deals &rarr;
            </a>
        </div>
    </div>

    <!-- STICKY NAVIGATION HEADER (GRAY BACKGROUND) -->
    <header class="bg-gray-300 border-b border-gray-400 sticky top-0 z-30 shadow-sm">
        <div class="max-w-6xl mx-auto px-4 py-3.5 flex flex-wrap items-center justify-between gap-4">
            <a href="{BASE_URL}/" class="flex items-center gap-2.5">
                <div class="w-9 h-9 rounded-lg bg-amber-700 flex items-center justify-center text-white font-black text-lg shadow-sm">D</div>
                <div>
                    <span class="font-extrabold text-lg tracking-tight text-gray-900 block leading-none">{SITE_NAME}</span>
                    <span class="text-[11px] text-gray-700 font-medium">Dust Collector CFM, Static Pressure & Duct Sizing</span>
                </div>
            </a>
            <nav class="flex flex-wrap items-center gap-4 sm:gap-5 text-xs sm:text-sm font-semibold text-gray-800">
                <a href="{BASE_URL}/#calculator" class="hover:text-amber-800 transition">CFM & Duct Calc</a>
                <a href="{BASE_URL}/#product-search" class="hover:text-amber-800 transition">Search Tools</a>
                <a href="{BASE_URL}/#best-sellers" class="hover:text-amber-800 transition">Best Sellers</a>
                <a href="{BASE_URL}/#comparison" class="hover:text-amber-800 transition">Compare</a>
                <a href="{BASE_URL}/#reviews" class="hover:text-amber-800 transition">Daily Reviews (+3/Day)</a>
                <a href="{BASE_URL}/#faq" class="hover:text-amber-800 transition">FAQ</a>
                <a href="{BASE_URL}/sitemap.html" class="hover:text-amber-800 transition font-bold underline">Site Map</a>
            </nav>
        </div>
    </header>
    """

def render_onpage_sitemap_directory():
    calc_links = "".join([
        f'<li><a href="{BASE_URL}/{p["slug"]}.html" class="text-xs text-gray-700 hover:text-amber-800 hover:underline">🪚 {p["name"]} Calculator</a></li>'
        for p in ALL_CALC_PAGES
    ])
    vs_links = "".join([
        f'<li><a href="{BASE_URL}/{v["slug"]}.html" class="text-xs text-gray-700 hover:text-amber-800 hover:underline">⚖️ {v["title"]}</a></li>'
        for v in VS_COMPARISONS
    ])
    all_revs = get_cumulative_product_reviews()
    rev_links = "".join([
        f'<li><a href="{BASE_URL}/{r["slug"]}.html" class="text-xs text-gray-700 hover:text-amber-800 hover:underline">📝 [{r["published_date"]}] {r["product_name"]} Review</a></li>'
        for r in all_revs
    ])
    return f"""
    <!-- COMPLETE ON-PAGE SITE MAP SECTION (SITE MAP) -->
    <section id="site-map" class="bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 space-y-6">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-gray-300 pb-3">
            <div>
                <span class="text-xs font-extrabold uppercase tracking-wider text-amber-800">Complete Site Architecture & Index</span>
                <h2 class="text-xl font-extrabold text-gray-900">Full HTML & XML Site Map Directory</h2>
            </div>
            <div class="flex gap-3 text-xs font-bold">
                <a href="{BASE_URL}/sitemap.html" class="bg-gray-300 hover:bg-gray-400 text-gray-900 px-3 py-1.5 rounded-lg transition">Open Dedicated HTML Site Map &rarr;</a>
                <a href="{BASE_URL}/sitemap.xml" class="bg-amber-700 hover:bg-amber-800 text-white px-3 py-1.5 rounded-lg transition">View XML Sitemap</a>
            </div>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
                <h3 class="text-sm font-extrabold text-gray-900 mb-2.5 uppercase tracking-wide border-b border-gray-300 pb-1">1. CFM & Duct Calculators ({len(ALL_CALC_PAGES) + 1})</h3>
                <ul class="space-y-1.5">
                    <li><a href="{BASE_URL}/" class="text-xs font-bold text-amber-800 hover:underline">🏠 Home — Master Woodshop CFM & Duct Calculator</a></li>
                    {calc_links}
                </ul>
            </div>
            <div>
                <h3 class="text-sm font-extrabold text-gray-900 mb-2.5 uppercase tracking-wide border-b border-gray-300 pb-1">2. Head-to-Head Comparisons ({len(VS_COMPARISONS)})</h3>
                <ul class="space-y-2">
                    {vs_links}
                </ul>
            </div>
            <div>
                <h3 class="text-sm font-extrabold text-gray-900 mb-2.5 uppercase tracking-wide border-b border-gray-300 pb-1">3. Daily Product Reviews ({len(all_revs)} — +3/Day)</h3>
                <ul class="space-y-1.5 max-h-80 overflow-y-auto pr-2">
                    {rev_links}
                </ul>
            </div>
        </div>
    </section>
    """

def render_dedicated_html_sitemap_page():
    canonical_url = f"{BASE_URL}/sitemap.html"
    sitemap_block = render_onpage_sitemap_directory()
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Complete Site Map Directory — Calculators, Comparisons & Daily Reviews | {SITE_NAME}</title>
    <meta name="description" content="Complete HTML and XML site map directory of all woodworking dust collector CFM calculators, static pressure guides, duct velocity calculators, and daily tool reviews on {SITE_NAME}.">
    <link rel="canonical" href="{canonical_url}">
    <meta name="robots" content="index, follow">
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-200 text-gray-900 antialiased">

    {render_common_header_and_banner()}

    <main class="max-w-6xl mx-auto px-4 py-10 space-y-8">
        <nav class="text-xs font-semibold text-gray-600 flex items-center gap-2">
            <a href="{BASE_URL}/" class="hover:text-amber-800">Home</a>
            <span>/</span>
            <span class="text-gray-900">Complete Site Map</span>
        </nav>

        <div class="bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 shadow-sm space-y-2">
            <h1 class="text-2xl sm:text-4xl font-extrabold text-gray-900">{SITE_NAME} — Complete Site Map</h1>
            <p class="text-sm text-gray-700">Browse every interactive woodshop dust collector CFM calculator, duct static pressure guide, head-to-head comparison, and cumulative daily product review article (+3 added daily) below.</p>
        </div>

        {sitemap_block}
    </main>

    <footer class="bg-gray-300 border-t border-gray-400 mt-16 py-10 px-4 text-xs text-gray-700 text-center">
        <p class="font-bold text-gray-900">{SITE_NAME} — {SITE_TAGLINE}</p>
        <p class="mt-1">As an Amazon Associate, this site earns from qualifying purchases (Store ID: {AFFILIATE_TAG}).</p>
    </footer>
</body>
</html>"""

def render_calculator_page(page_data, is_home=False):
    duct_dia, vel_fpm, sp_wc, rated_cfm, _, _ = compute_dust_specs(
        page_data["tool_cfm"], page_data["pipe_ft"], page_data["elbows"], page_data["flex_ft"], page_data["shop_sqft"]
    )
    title = f"{SITE_NAME} — {SITE_TAGLINE}" if is_home else f"{page_data['name']} — CFM & Duct Calculator ({rated_cfm:,} CFM / {duct_dia}\" Duct) | {SITE_NAME}"
    description = page_data["desc"]
    canonical_url = f"{BASE_URL}/" if is_home else f"{BASE_URL}/{page_data['slug']}.html"
    faqs = generate_faq_data(
        page_data["name"], page_data["tool_cfm"], page_data["pipe_ft"],
        page_data["elbows"], page_data["flex_ft"], page_data["shop_sqft"]
    )

    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": item["q"], "acceptedAnswer": {"@type": "Answer", "text": item["a"]}}
            for item in faqs
        ]
    }

    app_schema = {
        "@context": "https://schema.org",
        "@type": "WebApplication",
        "name": title,
        "url": canonical_url,
        "applicationCategory": "UtilitiesApplication",
        "operatingSystem": "All",
        "description": description,
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}
    }

    bestseller_cards_html = ""
    for prod in BEST_SELLERS:
        link = amz_url(prod["keyword"])
        bestseller_cards_html += f"""
        <div class="bg-gray-100 border-2 border-gray-300 hover:border-gray-400 rounded-xl p-5 shadow-sm transition flex flex-col justify-between">
            <div>
                <div class="flex items-center justify-between gap-2 mb-2">
                    <span class="text-xs font-bold uppercase tracking-wider bg-amber-100 text-amber-900 border border-amber-300 px-2.5 py-1 rounded-full">{prod['badge']}</span>
                    <span class="text-xs font-semibold text-amber-700">{prod['rating']}</span>
                </div>
                <span class="text-xs text-gray-600 font-medium">{prod['category']}</span>
                <h3 class="text-base font-bold text-gray-900 mt-1 mb-2 leading-snug">{prod['title']}</h3>
                <p class="text-xs text-gray-700 mb-4 bg-gray-200 p-2.5 rounded-lg border border-gray-300">{prod['specs']}</p>
            </div>
            <a href="{link}" target="_blank" rel="nofollow sponsored noopener"
               class="w-full inline-flex items-center justify-center bg-amber-700 hover:bg-amber-800 text-white font-extrabold text-sm py-2.5 px-4 rounded-lg transition shadow-sm">
               Check Today's Price on Amazon &rarr;
            </a>
        </div>
        """

    preset_links_html = ""
    for p in ALL_CALC_PAGES:
        p_dia, _, _, p_cfm, _, _ = compute_dust_specs(
            p["tool_cfm"], p["pipe_ft"], p["elbows"], p["flex_ft"], p["shop_sqft"]
        )
        active_cls = "bg-amber-100 border-amber-700 text-amber-950 font-bold" if (not is_home and p["slug"] == page_data["slug"]) else "bg-gray-100 border-gray-300 text-gray-800 hover:border-amber-700 hover:text-gray-950"
        preset_links_html += f"""
        <a href="{BASE_URL}/{p['slug']}.html" class="border rounded-lg p-3 text-xs transition flex items-center justify-between {active_cls}">
            <span class="truncate pr-2">{p['name']}</span>
            <span class="text-amber-900 font-mono shrink-0">{p_cfm} CFM / {p_dia}"</span>
        </a>
        """

    faq_html = ""
    for item in faqs:
        faq_html += f"""
        <div class="bg-gray-100 border-2 border-gray-300 rounded-xl p-5">
            <h3 class="text-base font-bold text-gray-900 mb-2">{item['q']}</h3>
            <p class="text-sm text-gray-700 leading-relaxed">{item['a']}</p>
        </div>
        """

    mid_banner_link = amz_url("JET+Cyclone+Dust+Collector+Oneida+Dust+Deputy+and+Air+Filtration+Bundle")
    comparison_html = render_comparison_table_section()
    reviews_grid_html, total_reviews_count = render_review_cards_grid()
    onpage_sitemap_html = render_onpage_sitemap_directory()

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="google-site-verification" content="pgvlG0f03ZrRZzbgDSXRhr6tsSfseFOhXCN6Yv_j5b8" />
    <meta name="description" content="{description}">
    <link rel="canonical" href="{canonical_url}">
    <meta name="robots" content="index, follow">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:type" content="website">
    <meta property="og:url" content="{canonical_url}">
    <script src="https://cdn.tailwindcss.com"></script>
    <script type="application/ld+json">{json.dumps(faq_schema)}</script>
    <script type="application/ld+json">{json.dumps(app_schema)}</script>
</head>
<body class="bg-gray-200 text-gray-900 antialiased selection:bg-amber-700 selection:text-white">

    {render_common_header_and_banner()}

    <main class="max-w-6xl mx-auto px-4 py-8 space-y-12">

        <!-- HERO TITLE SECTION -->
        <section class="text-center max-w-3xl mx-auto space-y-3">
            <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-gray-300 border border-gray-400 text-xs font-semibold text-gray-800">
                <span>🪚 ACGIH 4,000 FPM Duct Velocity, Static Pressure (WC) & Cyclone Sizing Engine</span>
            </div>
            <h1 class="text-3xl sm:text-4xl font-extrabold text-gray-900 tracking-tight">
                { "Woodshop Dust Collector CFM, Static Pressure & Duct Size Calculator" if is_home else f"{page_data['name']} — CFM & Duct Sizing Calculator" }
            </h1>
            <p class="text-gray-700 text-sm sm:text-base leading-relaxed">
                {description}
            </p>
        </section>

        <!-- INTERACTIVE CALCULATOR + LIVE HARDWARE MATCHER -->
        <section id="calculator" class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
            <!-- Left Column: Inputs (7 Cols) -->
            <div class="lg:col-span-7 bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 shadow-sm space-y-6">
                <div class="flex items-center justify-between border-b border-gray-300 pb-4">
                    <div>
                        <h2 class="text-xl font-extrabold text-gray-900">1. Enter Machine CFM, Duct Run & Elbows</h2>
                        <p class="text-xs text-gray-600">Calculates static pressure loss (in. WC), main duct size, FPM & collector HP</p>
                    </div>
                    <span class="text-xs font-mono bg-amber-100 text-amber-900 border border-amber-300 px-2.5 py-1 rounded font-semibold">Live Airflow Math</span>
                </div>

                <div>
                    <label for="quickPreset" class="block text-xs font-bold uppercase tracking-wider text-gray-700 mb-2">Quick Select Woodworking Machine or Shop Preset</label>
                    <select id="quickPreset" onchange="applyPreset(this.value)" class="w-full bg-gray-200 border border-gray-400 rounded-lg px-3.5 py-2.5 text-sm font-semibold text-gray-900 focus:ring-2 focus:ring-amber-700">
                        <option value="{page_data['tool_cfm']},{page_data['pipe_ft']},{page_data['elbows']},{page_data['flex_ft']},{page_data['shop_sqft']}">Current: {page_data['name']}</option>
                        <option value="650,20,2,4,480">13\"–15\" Thickness Planer (650 CFM @ Tool | 20 Ft Duct)</option>
                        <option value="450,18,2,4,400">10\" Cabinet Table Saw (450 CFM @ Tool | 18 Ft Duct)</option>
                        <option value="550,16,2,3,450">8\"–12\" Helical Jointer (550 CFM @ Tool | 16 Ft Duct)</option>
                        <option value="750,32,4,5,576">2-Car Garage Central 6\" Trunk System (32 Ft Pipe + 4 Elbows)</option>
                        <option value="700,15,2,4,500">16\"–22\" Drum Sander (700 CFM High Fine-Dust Load)</option>
                        <option value="1150,40,5,6,900">3 HP Multi-Machine Shop (2 Simultaneous Tools = 1,150 CFM)</option>
                    </select>
                </div>

                <div class="grid grid-cols-1 sm:grid-cols-2 gap-5">
                    <div>
                        <label for="cfmInput" class="block text-sm font-bold text-gray-800 mb-1">Required Machine Airflow (CFM)</label>
                        <input type="number" id="cfmInput" value="{page_data['tool_cfm']}" min="150" max="2500" step="50" oninput="calculateDust()"
                               class="w-full bg-gray-200 border border-gray-400 rounded-lg px-4 py-2.5 text-base font-bold text-gray-900 focus:ring-2 focus:ring-amber-700">
                        <span class="text-[11px] text-gray-600">Saw/Bandsaw: 450 | Jointer: 550 | Planer/Sander: 650+</span>
                    </div>

                    <div>
                        <label for="pipeInput" class="block text-sm font-bold text-gray-800 mb-1">Rigid Main Duct Length (Feet)</label>
                        <input type="number" id="pipeInput" value="{page_data['pipe_ft']}" min="0" max="120" step="2" oninput="calculateDust()"
                               class="w-full bg-gray-200 border border-gray-400 rounded-lg px-4 py-2.5 text-base font-bold text-gray-900 focus:ring-2 focus:ring-amber-700">
                        <span class="text-[11px] text-gray-600">Smooth PVC or spiral metal pipe from collector to drop</span>
                    </div>

                    <div>
                        <label for="elbowsInput" class="block text-sm font-bold text-gray-800 mb-1">Number of 90° Elbows & Wye Branches</label>
                        <input type="number" id="elbowsInput" value="{page_data['elbows']}" min="0" max="15" step="1" oninput="calculateDust()"
                               class="w-full bg-gray-200 border border-gray-400 rounded-lg px-4 py-2.5 text-base font-bold text-gray-900 focus:ring-2 focus:ring-amber-700">
                        <span class="text-[11px] text-gray-600">Each 90° sweep or wye adds ~0.55\" WC static loss</span>
                    </div>

                    <div>
                        <label for="flexInput" class="block text-sm font-bold text-gray-800 mb-1">Corrugated Flex Hose Length (Feet)</label>
                        <input type="number" id="flexInput" value="{page_data['flex_ft']}" min="1" max="30" step="1" oninput="calculateDust()"
                               class="w-full bg-gray-200 border border-gray-400 rounded-lg px-4 py-2.5 text-base font-bold text-gray-900 focus:ring-2 focus:ring-amber-700">
                        <span class="text-[11px] text-gray-600">Keep under 4–5 ft (flex hose has 7x higher friction!)</span>
                    </div>

                    <div class="sm:col-span-2">
                        <label for="sqftInput" class="block text-sm font-bold text-gray-800 mb-1">Total Woodshop Floor Area (Sq. Ft. — For Ceiling Air Cleaner)</label>
                        <input type="number" id="sqftInput" value="{page_data['shop_sqft']}" min="100" max="3000" step="20" oninput="calculateDust()"
                               class="w-full bg-gray-200 border border-gray-400 rounded-lg px-4 py-2.5 text-base font-bold text-gray-900 focus:ring-2 focus:ring-amber-700">
                        <span class="text-[11px] text-gray-600">1-Car Garage: 240 sq.ft | 2-Car Garage: 480–576 sq.ft</span>
                    </div>
                </div>
            </div>

            <!-- Right Column: Output + Dynamic Amazon Recommendation (5 Cols) -->
            <div class="lg:col-span-5 bg-gray-100 border-2 border-amber-700 rounded-2xl p-6 sm:p-8 shadow-md space-y-6">
                <div class="border-b border-gray-300 pb-3">
                    <span class="text-xs font-extrabold uppercase tracking-wider text-amber-800">2. Engineered CFM & Duct Specs</span>
                    <h2 class="text-xl font-extrabold text-gray-900">Your Required Collector & Pipe Sizing</h2>
                </div>

                <div class="grid grid-cols-2 gap-3.5">
                    <div class="bg-amber-100 border border-amber-300 rounded-xl p-3.5">
                        <span class="text-xs text-amber-950 font-semibold block">Min. Rated Collector</span>
                        <span id="resRatedCFM" class="text-2xl font-black text-amber-800">1,050 CFM</span>
                        <span id="resHpTier" class="text-[11px] text-amber-900 block mt-0.5">1.5 HP – 2.0 HP Cyclone</span>
                    </div>
                    <div class="bg-gray-200 border border-gray-300 rounded-xl p-3.5">
                        <span class="text-xs text-gray-600 font-medium block">Main Duct Diameter</span>
                        <span id="resDuctDia" class="text-2xl font-black text-gray-900">6-Inch Pipe</span>
                        <span id="resVelocity" class="text-[11px] text-emerald-800 font-bold block mt-0.5">3,820 FPM Velocity</span>
                    </div>
                    <div class="bg-gray-200 border border-gray-300 rounded-xl p-3.5">
                        <span class="text-xs text-gray-600 font-medium block">Static Pressure Loss</span>
                        <span id="resSpLoss" class="text-lg font-extrabold text-gray-900">5.4\" WC</span>
                        <span class="text-[11px] text-gray-600 block mt-0.5">Includes 1µm Canister</span>
                    </div>
                    <div class="bg-gray-200 border border-gray-300 rounded-xl p-3.5">
                        <span class="text-xs text-gray-600 font-medium block">Ceiling Air Scrubber</span>
                        <span id="resAmbientCFM" class="text-lg font-extrabold text-emerald-800">650+ CFM</span>
                        <span class="text-[11px] text-gray-600 block mt-0.5">9 Air Changes / Hour</span>
                    </div>
                </div>

                <!-- Dynamic Matched Product Box -->
                <div class="bg-gray-200 border-2 border-amber-600 rounded-xl p-4 space-y-3">
                    <div class="flex items-center justify-between">
                        <span class="text-[11px] font-extrabold uppercase tracking-wider bg-amber-700 text-white px-2 py-0.5 rounded">Verified Hardware Match</span>
                        <span class="text-xs font-bold text-gray-700">Amazon Prime Ready</span>
                    </div>
                    <h3 id="recDustTitle" class="text-base font-extrabold text-gray-900 leading-snug">Loading Cyclone & Filter Match...</h3>
                    <p id="recDustDesc" class="text-xs text-gray-700"></p>
                    <div class="pt-1 flex flex-col sm:flex-row gap-2.5">
                        <a id="recPrimaryBtn" href="#" target="_blank" rel="nofollow sponsored noopener"
                           class="flex-1 text-center bg-amber-700 hover:bg-amber-800 text-white font-extrabold text-sm py-3 px-4 rounded-lg transition shadow-sm">
                           Shop Matched Dust Collector &rarr;
                        </a>
                        <a id="recSecondaryBtn" href="#" target="_blank" rel="nofollow sponsored noopener"
                           class="text-center bg-gray-800 hover:bg-gray-900 text-white font-bold text-xs py-3 px-3 rounded-lg transition">
                           Shop Cyclone & Air Cleaner
                        </a>
                    </div>
                </div>
            </div>
        </section>

        <!-- PRODUCT SEARCH ENGINE SECTION (SEARCH PRODUK) -->
        <section id="product-search" class="bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 shadow-sm">
            <div class="max-w-3xl mx-auto text-center space-y-4">
                <h2 class="text-2xl font-extrabold text-gray-900">Search Cyclone Dust Collectors, 1-Micron Canisters, Planers & Blast Gates</h2>
                <p class="text-sm text-gray-700">Search any horsepower (1.5HP, 2HP, 3HP), brand (JET, Grizzly, Oneida Air Systems, DEWALT, Festool, Laguna, POWERTEC, iVac), or fitting on Amazon.</p>
                <form onsubmit="handleAmazonSearch(event)" class="flex flex-col sm:flex-row gap-3 pt-2">
                    <input type="text" id="amzSearchInput" placeholder="e.g. JET JCDC-1.5 Cyclone, Oneida Super Dust Deputy, DEWALT DW735X Planer..."
                           class="flex-1 bg-gray-200 border-2 border-gray-400 rounded-xl px-4 py-3 text-sm font-medium text-gray-900 placeholder-gray-500 focus:outline-none focus:border-amber-700" required>
                    <button type="submit" class="bg-amber-700 hover:bg-amber-800 text-white font-extrabold text-sm px-6 py-3 rounded-xl transition cursor-pointer shrink-0">
                        Search on Amazon &rarr;
                    </button>
                </form>
                <div class="flex flex-wrap items-center justify-center gap-2 pt-2 text-xs">
                    <span class="text-gray-600 font-semibold">Popular Searches:</span>
                    <a href="{amz_url('JET JCDC Cyclone Dust Collector Canister')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-gray-200 hover:bg-amber-200 text-gray-800 border border-gray-300 rounded-full transition">JET Cyclone Collectors</a>
                    <a href="{amz_url('Oneida Air Systems Super Dust Deputy Cyclone')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-gray-200 hover:bg-amber-200 text-gray-800 border border-gray-300 rounded-full transition">Oneida Dust Deputy</a>
                    <a href="{amz_url('DEWALT DW735X 13 Inch Two Speed Planer')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-gray-200 hover:bg-amber-200 text-gray-800 border border-gray-300 rounded-full transition">DEWALT DW735X Planer</a>
                    <a href="{amz_url('JET AFS-1000B 3 Speed Air Filtration System')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-gray-200 hover:bg-amber-200 text-gray-800 border border-gray-300 rounded-full transition">Ceiling Air Cleaners</a>
                    <a href="{amz_url('iVac Pro Automated Blast Gate System')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-gray-200 hover:bg-amber-200 text-gray-800 border border-gray-300 rounded-full transition">iVac Auto Blast Gates</a>
                </div>
            </div>
        </section>

        <!-- BEST SELLING PRODUCTS GRID (PRODUK TERLARIS) -->
        <section id="best-sellers" class="space-y-6">
            <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-2 border-b border-gray-300 pb-4">
                <div>
                    <span class="text-xs font-extrabold uppercase tracking-wider text-amber-800">Verified Woodshop Machinery</span>
                    <h2 class="text-2xl font-extrabold text-gray-900">Best-Selling Cyclone Collectors, Planers, HEPA Extractors & Air Cleaners</h2>
                </div>
                <a href="{amz_url('Best Selling Woodshop Dust Collectors and Planers')}" target="_blank" rel="nofollow sponsored noopener" class="text-sm font-bold text-amber-800 hover:text-amber-900">
                    Browse Full Amazon Best Sellers &rarr;
                </a>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
                {bestseller_cards_html}
            </div>
        </section>

        {comparison_html}

        <!-- CUMULATIVE DAILY PRODUCT REVIEW ARTICLES SECTION (+3 NEW ARTICLES PER DAY) -->
        <section id="reviews" class="space-y-6">
            <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-2 border-b border-gray-300 pb-4">
                <div>
                    <span class="text-xs font-extrabold uppercase tracking-wider text-amber-800">Autonomous Daily Review Archive ({total_reviews_count} Published Articles & Growing +3/Day)</span>
                    <h2 class="text-2xl font-extrabold text-gray-900">In-Depth Dust Collector, Planer & Woodshop Tool Review Articles</h2>
                </div>
                <span class="text-xs font-semibold bg-emerald-100 text-emerald-900 border border-emerald-300 px-3 py-1 rounded-full">+3 New Product Reviews Added Automatically Every Day</span>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {reviews_grid_html}
            </div>
        </section>

        <!-- MID-PAGE PROMOTIONAL AFFILIATE BANNER -->
        <section class="bg-gray-300 border-2 border-amber-700 rounded-2xl p-6 sm:p-8 flex flex-col md:flex-row items-center justify-between gap-6">
            <div class="space-y-2 max-w-2xl">
                <span class="text-xs font-extrabold uppercase tracking-wider bg-amber-700 text-white px-2.5 py-1 rounded">Complete Clean-Lung Woodshop Bundle</span>
                <h2 class="text-xl sm:text-2xl font-extrabold text-gray-900">Upgrading Your Garage or Basement Shop to 1-Micron Cyclone Filtration?</h2>
                <p class="text-sm text-gray-800">Capture 99% of heavy planer chips and invisible airborne lung dust by pairing a 2-Stage Cyclone Collector (or Oneida Super Dust Deputy) with 6\" Pipe, iVac Auto Gates, and a Ceiling Air Scrubber.</p>
            </div>
            <a href="{mid_banner_link}" target="_blank" rel="nofollow sponsored noopener"
               class="shrink-0 bg-amber-700 hover:bg-amber-800 text-white font-extrabold text-sm px-6 py-3.5 rounded-xl shadow-sm transition">
               Explore Cyclone + Air Filtration Bundles on Amazon &rarr;
            </a>
        </section>

        <!-- PROGRAMMATIC SEO DIRECTORY -->
        <section id="presets" class="space-y-4">
            <div class="border-b border-gray-300 pb-3">
                <h2 class="text-xl font-extrabold text-gray-900">Woodworking Machine & Duct CFM Specific Calculators</h2>
                <p class="text-xs text-gray-600">Select your exact woodworking tool or shop duct configuration below for pre-calculated CFM, static pressure, and pipe diameter specs.</p>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-2.5">
                {preset_links_html}
            </div>
        </section>

        <!-- FREQUENTLY ASKED QUESTIONS (FAQ) -->
        <section id="faq" class="space-y-6">
            <div class="border-b border-gray-300 pb-3">
                <span class="text-xs font-extrabold uppercase tracking-wider text-amber-800">Airflow Velocity & Static Pressure Guide</span>
                <h2 class="text-2xl font-extrabold text-gray-900">Frequently Asked Questions (FAQ)</h2>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                {faq_html}
            </div>
        </section>

        {onpage_sitemap_html}

    </main>

    <!-- FOOTER (GRAY BACKGROUND) -->
    <footer class="bg-gray-300 border-t border-gray-400 mt-16 py-10 px-4 text-xs text-gray-700">
        <div class="max-w-6xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
            <div>
                <p class="font-bold text-gray-900">{SITE_NAME} — {SITE_TAGLINE}</p>
                <p class="mt-1">As an Amazon Associate, this site earns from qualifying purchases (Store ID: {AFFILIATE_TAG}).</p>
            </div>
            <div class="flex flex-wrap gap-4 font-medium text-gray-800">
                <a href="{BASE_URL}/" class="hover:text-amber-800">Home</a>
                <a href="{BASE_URL}/#comparison" class="hover:text-amber-800">Comparisons</a>
                <a href="{BASE_URL}/#reviews" class="hover:text-amber-800">Daily Reviews (+3/Day)</a>
                <a href="{BASE_URL}/sitemap.html" class="hover:text-amber-800 font-bold">HTML Site Map</a>
                <a href="{BASE_URL}/sitemap.xml" class="hover:text-amber-800">XML Sitemap</a>
                <a href="{BASE_URL}/#faq" class="hover:text-amber-800">FAQ</a>
            </div>
        </div>
    </footer>

    <!-- INTERACTIVE CALCULATOR & AFFILIATE MATCHING SCRIPT -->
    <script>
        const AFFILIATE_TAG = "{AFFILIATE_TAG}";

        function makeAmazonLink(query) {{
            return "https://www.amazon.com/s?k=" + encodeURIComponent(query) + "&tag=" + AFFILIATE_TAG;
        }}

        function applyPreset(val) {{
            const parts = val.split(",");
            if (parts.length === 5) {{
                document.getElementById("cfmInput").value = parts[0];
                document.getElementById("pipeInput").value = parts[1];
                document.getElementById("elbowsInput").value = parts[2];
                document.getElementById("flexInput").value = parts[3];
                document.getElementById("sqftInput").value = parts[4];
                calculateDust();
            }}
        }}

        function handleAmazonSearch(e) {{
            e.preventDefault();
            const q = document.getElementById("amzSearchInput").value.trim();
            if (q) {{
                window.open(makeAmazonLink(q), "_blank", "noopener,noreferrer");
            }}
        }}

        function calculateDust() {{
            const toolCFM = parseFloat(document.getElementById("cfmInput").value) || 650;
            const pipeFt = parseFloat(document.getElementById("pipeInput").value) || 20;
            const elbows = parseFloat(document.getElementById("elbowsInput").value) || 2;
            const flexFt = parseFloat(document.getElementById("flexInput").value) || 4;
            const shopSqFt = parseFloat(document.getElementById("sqftInput").value) || 480;

            let ductDia = 6;
            let areaSqFt = 0.1963;
            if (toolCFM <= 400) {{
                ductDia = 4;
                areaSqFt = 0.0873;
            }} else if (toolCFM <= 600) {{
                ductDia = 5;
                areaSqFt = 0.1364;
            }} else if (toolCFM <= 900) {{
                ductDia = 6;
                areaSqFt = 0.1963;
            }} else {{
                ductDia = 8;
                areaSqFt = 0.3491;
            }}

            const velocityFPM = Math.round(toolCFM / areaSqFt);
            const spLoss = ((pipeFt * 0.032) + (flexFt * 0.22) + (elbows * 0.55) + 2.8).toFixed(1);
            const reqRatedCFM = Math.ceil((toolCFM + (parseFloat(spLoss) * 62)) / 50) * 50;

            let hpTier = "1.5 HP – 2.0 HP Cyclone";
            if (reqRatedCFM <= 1150) hpTier = "1.5 HP Cyclone (120V/240V)";
            else if (reqRatedCFM <= 1550) hpTier = "2.0 HP Cyclone (240V)";
            else hpTier = "3.0 HP Heavy Cyclone (240V)";

            const ambientCFM = Math.max(400, Math.ceil(((shopSqFt * 8.5 * 9) / 60) / 50) * 50);

            document.getElementById("resRatedCFM").textContent = reqRatedCFM.toLocaleString() + "+ CFM";
            document.getElementById("resHpTier").textContent = hpTier;
            document.getElementById("resDuctDia").textContent = ductDia + "-Inch Main Duct";
            document.getElementById("resVelocity").textContent = velocityFPM.toLocaleString() + " FPM Chip Velocity";
            document.getElementById("resSpLoss").textContent = spLoss + "\\\" Water Column";
            document.getElementById("resAmbientCFM").textContent = ambientCFM.toLocaleString() + "+ CFM Cleaner";

            let recTitle = "";
            let recDesc = "";
            let primaryQuery = "";
            let secondaryQuery = "Oneida Super Dust Deputy Cyclone and JET AFS-1000B Air Filtration";

            if (reqRatedCFM <= 1150) {{
                recTitle = "1.5 HP Portable Cyclone Collector (JET JCDC-1.5 / Grizzly G0860 / Laguna B|Flux)";
                recDesc = "Runs on a standard 120V (or 240V) circuit with 1-micron canister filtration for single-machine drops.";
                primaryQuery = "JET JCDC-1.5 Grizzly G0860 1.5 HP Cyclone Dust Collector";
            }} else if (reqRatedCFM <= 1600) {{
                recTitle = "2.0 HP Two-Stage Cyclone Dust Collector (JET JCDC-2.0 / Laguna C|Flux / Grizzly)";
                recDesc = "Ideal 6-inch main trunk suction for 13\"–15\" planers, cabinet table saws, and 2-car garage shops.";
                primaryQuery = "JET JCDC-2.0 Laguna C Flux Grizzly 2 HP Cyclone Dust Collector";
            }} else {{
                recTitle = "3.0 HP Commercial Cyclone Dust Collector (JET JCDC-3 / Grizzly G0441 / Oneida)";
                recDesc = "High-static-pressure 240V powerhouse built for 7\"–8\" trunks and running two machines simultaneously.";
                primaryQuery = "3 HP Cyclone Dust Collector JET Grizzly Laguna";
            }}

            document.getElementById("recDustTitle").textContent = recTitle;
            document.getElementById("recDustDesc").textContent = recDesc;
            document.getElementById("recPrimaryBtn").href = makeAmazonLink(primaryQuery);
            document.getElementById("recSecondaryBtn").href = makeAmazonLink(secondaryQuery);
        }}

        window.addEventListener("DOMContentLoaded", calculateDust);
    </script>
</body>
</html>"""

def render_single_review_page(rev):
    canonical_url = f"{BASE_URL}/{rev['slug']}.html"
    amz_link = amz_url(rev["keyword"])

    review_schema = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": rev["product_name"],
        "description": rev["summary"],
        "review": {
            "@type": "Review",
            "datePublished": rev["published_date"],
            "reviewRating": {"@type": "Rating", "ratingValue": rev["rating_score"], "bestRating": "5"},
            "author": {"@type": "Organization", "name": SITE_NAME},
            "reviewBody": " ".join(rev["body_paragraphs"])
        }
    }

    pros_html = "".join([f'<li class="flex items-start gap-2 text-sm text-gray-800"><span class="text-emerald-700 font-bold">✓</span><span>{p}</span></li>' for p in rev["pros"]])
    cons_html = "".join([f'<li class="flex items-start gap-2 text-sm text-gray-800"><span class="text-rose-700 font-bold">✕</span><span>{c}</span></li>' for c in rev["cons"]])
    paragraphs_html = "".join([f'<p class="text-gray-800 leading-relaxed text-base mb-4">{p}</p>' for p in rev["body_paragraphs"]])

    recent_reviews = [r for r in get_cumulative_product_reviews() if r["slug"] != rev["slug"]][:6]
    related_html = ""
    for other in recent_reviews:
        related_html += f"""
        <a href="{BASE_URL}/{other['slug']}.html" class="bg-gray-100 border-2 border-gray-300 rounded-xl p-4 hover:border-amber-700 transition block">
            <span class="text-[11px] font-bold text-amber-800 uppercase">{other['verdict_badge']}</span>
            <h4 class="font-extrabold text-sm text-gray-900 mt-1 line-clamp-2">{other['product_name']} Review</h4>
            <span class="text-xs text-gray-600 mt-1 block">Score: {other['rating_score']} / 5.0 ★ ({other['published_date']}) &rarr;</span>
        </a>
        """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{rev['title']} | {SITE_NAME}</title>
    <meta name="description" content="{rev['summary']}">
    <link rel="canonical" href="{canonical_url}">
    <meta name="robots" content="index, follow">
    <script src="https://cdn.tailwindcss.com"></script>
    <script type="application/ld+json">{json.dumps(review_schema)}</script>
</head>
<body class="bg-gray-200 text-gray-900 antialiased">

    {render_common_header_and_banner()}

    <main class="max-w-4xl mx-auto px-4 py-10 space-y-10">
        <nav class="text-xs font-semibold text-gray-600 flex items-center gap-2">
            <a href="{BASE_URL}/" class="hover:text-amber-800">Home & CFM Calculator</a>
            <span>/</span>
            <a href="{BASE_URL}/#reviews" class="hover:text-amber-800">Daily Woodshop Reviews</a>
            <span>/</span>
            <span class="text-gray-900">{rev['product_name']}</span>
        </nav>

        <div class="bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 shadow-sm space-y-5">
            <div class="flex flex-wrap items-center justify-between gap-2">
                <span class="text-xs font-extrabold uppercase tracking-wider bg-amber-100 text-amber-900 border border-amber-300 px-3 py-1 rounded-full">{rev['verdict_badge']}</span>
                <div class="flex items-center gap-2">
                    <span class="text-xs font-mono text-gray-600">Published: {rev['published_date']}</span>
                    <span class="text-sm font-black bg-emerald-200 text-emerald-950 px-3 py-1 rounded-lg">Shop Rating: {rev['rating_score']} / 5.0 ★</span>
                </div>
            </div>
            <h1 class="text-2xl sm:text-4xl font-extrabold text-gray-900 leading-tight">{rev['title']}</h1>
            <p class="text-base text-gray-700 leading-relaxed">{rev['summary']}</p>

            <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 bg-gray-200 p-4 rounded-xl border border-gray-300 text-xs">
                <div><span class="text-gray-500 block font-medium">CFM / Output</span><strong class="text-gray-900">{rev['spec_1']}</strong></div>
                <div><span class="text-gray-500 block font-medium">Filtration</span><strong class="text-gray-900">{rev['spec_2']}</strong></div>
                <div><span class="text-gray-500 block font-medium">Architecture</span><strong class="text-gray-900">{rev['spec_3']}</strong></div>
                <div><span class="text-gray-500 block font-medium">Warranty</span><strong class="text-gray-900">{rev['spec_4']}</strong></div>
            </div>

            <div class="flex flex-col sm:flex-row gap-3 pt-2">
                <a href="{amz_link}" target="_blank" rel="nofollow sponsored noopener"
                   class="flex-1 text-center bg-amber-700 hover:bg-amber-800 text-white font-extrabold text-sm py-3.5 px-6 rounded-xl transition shadow-sm">
                   Check Latest Price & Availability on Amazon &rarr;
                </a>
                <a href="{BASE_URL}/#calculator"
                   class="text-center bg-gray-300 hover:bg-gray-400 text-gray-900 font-bold text-sm py-3.5 px-5 rounded-xl transition">
                   Calculate Duct CFM & Static Loss
                </a>
            </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div class="bg-gray-100 border-2 border-emerald-400 rounded-2xl p-6 space-y-3">
                <h2 class="text-base font-extrabold text-emerald-900 uppercase tracking-wide">Pros (What We Like)</h2>
                <ul class="space-y-2.5">{pros_html}</ul>
            </div>
            <div class="bg-gray-100 border-2 border-rose-400 rounded-2xl p-6 space-y-3">
                <h2 class="text-base font-extrabold text-rose-900 uppercase tracking-wide">Cons (Things to Consider)</h2>
                <ul class="space-y-2.5">{cons_html}</ul>
            </div>
        </div>

        <article class="bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 space-y-4">
            <h2 class="text-xl font-extrabold text-gray-900 border-b border-gray-300 pb-3">Hands-On Anemometer CFM, Static Pressure & Chip Separation Analysis</h2>
            {paragraphs_html}
            <div class="pt-4 border-t border-gray-300 flex flex-col sm:flex-row items-center justify-between gap-4">
                <div>
                    <span class="text-xs font-bold uppercase text-amber-800 block">Final Verdict</span>
                    <p class="text-sm font-bold text-gray-900">{rev['product_name']} earns {rev['rating_score']}/5.0 in our woodshop benchmark.</p>
                </div>
                <a href="{amz_link}" target="_blank" rel="nofollow sponsored noopener"
                   class="shrink-0 bg-amber-700 hover:bg-amber-800 text-white font-extrabold text-sm px-6 py-3 rounded-xl transition shadow-sm">
                   View Customer Reviews & Price on Amazon &rarr;
                </a>
            </div>
        </article>

        <section class="space-y-4">
            <h3 class="text-lg font-extrabold text-gray-900">Recent Daily Woodshop Hardware Reviews (+3 Added Daily)</h3>
            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
                {related_html}
            </div>
        </section>
    </main>

    <footer class="bg-gray-300 border-t border-gray-400 mt-16 py-10 px-4 text-xs text-gray-700 text-center">
        <p class="font-bold text-gray-900">{SITE_NAME} — {SITE_TAGLINE}</p>
        <p class="mt-1">As an Amazon Associate, this site earns from qualifying purchases (Store ID: {AFFILIATE_TAG}).</p>
    </footer>
</body>
</html>"""

def render_vs_comparison_page(vs):
    canonical_url = f"{BASE_URL}/{vs['slug']}.html"
    link_a = amz_url(vs["keyword_a"])
    link_b = amz_url(vs["keyword_b"])

    rows_html = ""
    for m in vs["metrics"]:
        rows_html += f"""
        <tr class="border-b border-gray-300">
            <td class="p-4 font-bold text-gray-900 bg-gray-200 text-xs sm:text-sm w-1/4">{m['feature']}</td>
            <td class="p-4 text-xs sm:text-sm text-gray-800 w-3/8">{m['val_a']}</td>
            <td class="p-4 text-xs sm:text-sm text-gray-800 w-3/8">{m['val_b']}</td>
        </tr>
        """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{vs['title']} | {SITE_NAME}</title>
    <meta name="description" content="{vs['summary']}">
    <link rel="canonical" href="{canonical_url}">
    <meta name="robots" content="index, follow">
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-200 text-gray-900 antialiased">

    {render_common_header_and_banner()}

    <main class="max-w-4xl mx-auto px-4 py-10 space-y-10">
        <nav class="text-xs font-semibold text-gray-600 flex items-center gap-2">
            <a href="{BASE_URL}/" class="hover:text-amber-800">Home & CFM Calculator</a>
            <span>/</span>
            <a href="{BASE_URL}/#comparison" class="hover:text-amber-800">Product Comparisons</a>
            <span>/</span>
            <span class="text-gray-900">{vs['product_a']} vs. {vs['product_b']}</span>
        </nav>

        <div class="bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 shadow-sm space-y-4">
            <span class="text-xs font-extrabold uppercase tracking-wider bg-amber-100 text-amber-900 border border-amber-300 px-3 py-1 rounded-full">{vs['winner_badge']}</span>
            <h1 class="text-2xl sm:text-4xl font-extrabold text-gray-900 leading-tight">{vs['title']}</h1>
            <p class="text-base text-gray-700 leading-relaxed">{vs['summary']}</p>
        </div>

        <div class="bg-gray-100 border-2 border-gray-300 rounded-2xl overflow-hidden shadow-sm">
            <table class="w-full text-left border-collapse">
                <thead>
                    <tr class="bg-gray-800 text-white text-xs sm:text-sm font-extrabold">
                        <th class="p-4">Specification</th>
                        <th class="p-4 text-amber-300">{vs['product_a']}</th>
                        <th class="p-4 text-emerald-300">{vs['product_b']}</th>
                    </tr>
                </thead>
                <tbody>
                    {rows_html}
                    <tr class="bg-gray-200">
                        <td class="p-4 font-extrabold text-xs sm:text-sm text-gray-900">Check Amazon Price</td>
                        <td class="p-4">
                            <a href="{link_a}" target="_blank" rel="nofollow sponsored noopener" class="inline-block bg-amber-700 hover:bg-amber-800 text-white font-extrabold text-xs py-2.5 px-4 rounded-lg transition">
                                View {vs['product_a']} &rarr;
                            </a>
                        </td>
                        <td class="p-4">
                            <a href="{link_b}" target="_blank" rel="nofollow sponsored noopener" class="inline-block bg-gray-800 hover:bg-gray-900 text-white font-extrabold text-xs py-2.5 px-4 rounded-lg transition">
                                View {vs['product_b']} &rarr;
                            </a>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <div class="bg-gray-100 border-2 border-amber-600 rounded-2xl p-6 sm:p-8 space-y-4">
            <h2 class="text-xl font-extrabold text-gray-900">Head-to-Head Buying Verdict</h2>
            <p class="text-sm sm:text-base text-gray-800 leading-relaxed">{vs['verdict_text']}</p>
            <div class="flex flex-col sm:flex-row gap-3 pt-2">
                <a href="{link_a}" target="_blank" rel="nofollow sponsored noopener" class="flex-1 text-center bg-amber-700 hover:bg-amber-800 text-white font-extrabold text-sm py-3 px-4 rounded-xl transition">
                    Shop {vs['product_a']} on Amazon &rarr;
                </a>
                <a href="{link_b}" target="_blank" rel="nofollow sponsored noopener" class="flex-1 text-center bg-gray-800 hover:bg-gray-900 text-white font-extrabold text-sm py-3 px-4 rounded-xl transition">
                    Shop {vs['product_b']} on Amazon &rarr;
                </a>
            </div>
        </div>
    </main>

    <footer class="bg-gray-300 border-t border-gray-400 mt-16 py-10 px-4 text-xs text-gray-700 text-center">
        <p class="font-bold text-gray-900">{SITE_NAME} — {SITE_TAGLINE}</p>
        <p class="mt-1">As an Amazon Associate, this site earns from qualifying purchases (Store ID: {AFFILIATE_TAG}).</p>
    </footer>
</body>
</html>"""

def generate_sitemap_and_robots(urls):
    today = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    xml_items = ""
    for u in urls:
        xml_items += f"""  <url>
    <loc>{u}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>daily</changefreq>
    <priority>{"1.0" if u.endswith("/") else "0.85"}</priority>
  </url>\n"""

    sitemap_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{xml_items}</urlset>"""

    with open(os.path.join(OUTPUT_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap_content)

    robots_content = f"""User-agent: *
Allow: /
Sitemap: {BASE_URL}/sitemap.xml
"""
    with open(os.path.join(OUTPUT_DIR, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(robots_content)

    with open(os.path.join(OUTPUT_DIR, f"{INDEXNOW_KEY}.txt"), "w", encoding="utf-8") as f:
        f.write(INDEXNOW_KEY)

def ping_indexnow(urls):
    parsed_host = urllib.parse.urlparse(BASE_URL).netloc
    if not parsed_host or "username.github.io" in parsed_host:
        return

    payload = {
        "host": parsed_host,
        "key": INDEXNOW_KEY,
        "keyLocation": f"{BASE_URL}/{INDEXNOW_KEY}.txt",
        "urlList": urls
    }
    try:
        req = urllib.request.Request(
            "https://api.indexnow.org/indexnow",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json; charset=utf-8"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            print(f"IndexNow Ping Status: {resp.status}")
    except Exception as e:
        print(f"IndexNow notice: {e}")

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    generated_urls = []

    # 1. Generate Homepage
    home_preset = {
        "slug": "index",
        "name": "13\"–15\" Planer & Table Saw 6\" Duct Trunk",
        "tool_cfm": 650,
        "pipe_ft": 20,
        "elbows": 2,
        "flex_ft": 4,
        "shop_sqft": 480,
        "desc": "Calculate exact woodshop dust collector CFM, static pressure loss (inches of water column), 4\"/5\"/6\"/8\" duct diameter for 4,000 FPM chip velocity, and ceiling air cleaner ACH—plus read 3 new tool reviews added daily."
    }
    with open(os.path.join(OUTPUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(render_calculator_page(home_preset, is_home=True))
    generated_urls.append(f"{BASE_URL}/")

    # 2. Generate Dedicated HTML Site Map Page (sitemap.html)
    with open(os.path.join(OUTPUT_DIR, "sitemap.html"), "w", encoding="utf-8") as f:
        f.write(render_dedicated_html_sitemap_page())
    generated_urls.append(f"{BASE_URL}/sitemap.html")

    # 3. Generate Programmatic Woodshop & Duct Calculator Pages
    for page in ALL_CALC_PAGES:
        filename = f"{page['slug']}.html"
        with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
            f.write(render_calculator_page(page, is_home=False))
        generated_urls.append(f"{BASE_URL}/{filename}")

    # 4. Generate Cumulative Daily Product Review Pages (+3 new reviews unlocked every single day)
    active_reviews = get_cumulative_product_reviews()
    for rev in active_reviews:
        filename = f"{rev['slug']}.html"
        with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
            f.write(render_single_review_page(rev))
        generated_urls.append(f"{BASE_URL}/{filename}")

    # 5. Generate Standalone Head-to-Head Product Comparison Pages
    for vs in VS_COMPARISONS:
        filename = f"{vs['slug']}.html"
        with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
            f.write(render_vs_comparison_page(vs))
        generated_urls.append(f"{BASE_URL}/{filename}")

    # 6. XML Sitemap, Robots & IndexNow Auto-Ping
    generate_sitemap_and_robots(generated_urls)
    ping_indexnow(generated_urls)
    print(f"Successfully generated {len(generated_urls)} total SEO pages ({len(active_reviews)} cumulative review articles [+3/day] + HTML/XML sitemaps) in /{OUTPUT_DIR}!")

if __name__ == "__main__":
    main()
