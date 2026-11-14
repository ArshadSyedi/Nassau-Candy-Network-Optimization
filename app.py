"""Nassau Candy factory relocation and shipping scenario dashboard."""
from pathlib import Path
import math

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Nassau Candy | Network Planner", page_icon="🍬", layout="wide")

DATA_PATH = Path(__file__).with_name("Nassau Candy Distributor.csv")
FACTORIES = {
    "Lot's O' Nuts": (32.881893, -111.768036),
    "Wicked Choccy's": (32.076176, -81.088371),
    "Sugar Shack": (48.11914, -96.18115),
    "Secret Factory": (41.446333, -90.565487),
    "The Other Factory": (35.1175, -89.971107),
}
PRODUCT_FACTORY = {
    "Wonka Bar - Nutty Crunch Surprise": "Lot's O' Nuts",
    "Wonka Bar - Fudge Mallows": "Lot's O' Nuts",
    "Wonka Bar - Scrumdiddlyumptious": "Lot's O' Nuts",
    "Wonka Bar - Milk Chocolate": "Wicked Choccy's",
    "Wonka Bar - Triple Dazzle Caramel": "Wicked Choccy's",
    "Laffy Taffy": "Sugar Shack", "SweeTARTS": "Sugar Shack", "Nerds": "Sugar Shack",
    "Fun Dip": "Sugar Shack", "Fizzy Lifting Drinks": "Sugar Shack",
    "Everlasting Gobstopper": "Secret Factory", "Lickable Wallpaper": "Secret Factory",
    "Hair Toffee": "The Other Factory", "Kazookles": "The Other Factory",
    "Wonka Gum": "Secret Factory",
}
# Regional centers are illustrative proxies, not customer geocodes.
REGION_CENTER = {
    "Pacific": (38.0, -120.0), "Interior": (39.0, -100.0),
    "Atlantic": (39.0, -76.0), "Gulf": (30.0, -90.0),
}
SHIP_SPEED = {"Same Day": 900, "First Class": 650, "Second Class": 450, "Standard Class": 300}

@st.cache_data
def load_data():
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Place the CSV beside app.py: {DATA_PATH.name}")
    d = pd.read_csv(DATA_PATH, dtype={"Postal Code": str})
    d.columns = d.columns.str.strip()
    for c in d.select_dtypes(include="object"):
        d[c] = d[c].str.strip()
    d["Order Date"] = pd.to_datetime(d["Order Date"], format="%d-%m-%Y", errors="coerce")
    d["Ship Date"] = pd.to_datetime(d["Ship Date"], format="%d-%m-%Y", errors="coerce")
    d["Product Name"] = d["Product Name"].str.replace(r"\s*-\s*", " - ", regex=True)
    d["Lead Time (days)"] = (d["Ship Date"] - d["Order Date"]).dt.days
    return d

def haversine(a, b):
    r = 3958.8
    lat1, lon1, lat2, lon2 = map(math.radians, [a[0], a[1], b[0], b[1]])
    h = math.sin((lat2-lat1)/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin((lon2-lon1)/2)**2
    return 2*r*math.asin(math.sqrt(h))

try:
    df = load_data()
except Exception as exc:
    st.error(str(exc)); st.stop()

st.title("🍬 Nassau Candy | Factory & Shipping Network Planner")
st.caption("Decision-support prototype · Historical ship dates are flagged as unreliable; scenario transit figures are distance-based estimates.")

with st.sidebar:
    st.header("Explore the data")
    regions = st.multiselect("Customer region", sorted(df["Region"].dropna().unique()), default=sorted(df["Region"].dropna().unique()))
    modes = st.multiselect("Ship mode", sorted(df["Ship Mode"].dropna().unique()), default=sorted(df["Ship Mode"].dropna().unique()))
    divisions = st.multiselect("Product division", sorted(df["Division"].dropna().unique()), default=sorted(df["Division"].dropna().unique()))
    st.divider()
    st.caption("Optimization priority")
    speed_weight = st.slider("Speed vs. profit focus", 0, 100, 70, help="Scenario ranking weights distance-based transit estimate. Profit remains unchanged because no freight charge or factory capacity data was supplied.")

view = df[df["Region"].isin(regions) & df["Ship Mode"].isin(modes) & df["Division"].isin(divisions)].copy()
if view.empty:
    st.warning("No orders match these filters."); st.stop()

sales = view["Sales"].sum(); profit = view["Gross Profit"].sum()
k1,k2,k3,k4 = st.columns(4)
k1.metric("Filtered sales", f"${sales:,.0f}")
k2.metric("Gross profit", f"${profit:,.0f}")
k3.metric("Gross margin", f"{profit/sales*100:.1f}%" if sales else "—")
k4.metric("Orders", f"{view['Order ID'].nunique():,}")

with st.expander("Data quality and interpretation", expanded=True):
    lead = view["Lead Time (days)"].dropna()
    st.warning(f"The provided Ship Date values imply {lead.median():,.0f} median days from order to ship (range {lead.min():,}–{lead.max():,}). Treat this field as corrupted until confirmed. The app does not train or display a predictive ML model from these dates.")
    st.info("Scenario transit estimates use straight-line distance from the supplied factory coordinates to broad region-center proxies, divided by an illustrative speed assumption for each ship mode. They are relative comparisons, not delivery forecasts. Factory capacity, freight cost, road routes, and service-level data were not supplied.")

tab1,tab2,tab3,tab4 = st.tabs(["Executive overview", "Scenario simulator", "Recommendations", "Data & method"])
with tab1:
    left,right = st.columns(2)
    monthly = view.dropna(subset=["Order Date"]).assign(Month=lambda x:x["Order Date"].dt.to_period("M").astype(str)).groupby("Month",as_index=False).agg(Sales=("Sales","sum"), Profit=("Gross Profit","sum"))
    left.plotly_chart(px.line(monthly,x="Month",y=["Sales","Profit"],title="Monthly sales and gross profit"),use_container_width=True)
    by_region = view.groupby("Region",as_index=False).agg(Sales=("Sales","sum"),Profit=("Gross Profit","sum"),Units=("Units","sum"))
    right.plotly_chart(px.bar(by_region,x="Region",y="Sales",color="Profit",title="Sales by customer region",color_continuous_scale="Teal"),use_container_width=True)
    prod = view.groupby(["Product Name","Division"],as_index=False).agg(Sales=("Sales","sum"),Profit=("Gross Profit","sum"),Units=("Units","sum")).sort_values("Sales",ascending=True)
    st.plotly_chart(px.bar(prod,x="Sales",y="Product Name",color="Division",orientation="h",title="Product sales"),use_container_width=True)
    st.caption("Profit impact stability is not estimated: the dataset has manufacturing cost but no shipping cost, production capacity, or factory-specific cost differences.")

with tab2:
    st.subheader("Compare factory assignments for a product")
    product = st.selectbox("Product", sorted(view["Product Name"].unique()))
    product_rows = view[view["Product Name"] == product]
    region = st.selectbox("Destination region", sorted(product_rows["Region"].unique()))
    mode = st.selectbox("Ship mode", sorted(product_rows["Ship Mode"].unique()))
    current = PRODUCT_FACTORY.get(product)
    center = REGION_CENTER.get(region)
    if not current or not center:
        st.error("This product or region has no mapping in the project brief.")
    else:
        options=[]
        for factory,coord in FACTORIES.items():
            miles=haversine(coord,center)
            est=miles/SHIP_SPEED[mode]*24
            options.append({"Factory":factory,"Estimated distance (mi)":miles,"Illustrative transit (hours)":est,"Current assignment":factory==current})
        sim=pd.DataFrame(options).sort_values("Illustrative transit (hours)")
        baseline=float(sim.loc[sim.Factory==current,"Illustrative transit (hours)"].iloc[0])
        sim["Relative time improvement (%)"]=(baseline-sim["Illustrative transit (hours)"])/baseline*100
        sim["Priority score"]=(speed_weight/100)*sim["Relative time improvement (%)"] + (1-speed_weight/100)*0
        st.caption(f"Current assignment: **{current}** · scenario priority puts {speed_weight}% weight on relative distance proxy. Profit impact is held neutral because comparable factory and freight costs are unavailable.")
        st.plotly_chart(px.bar(sim,x="Factory",y="Illustrative transit (hours)",color="Current assignment",title=f"Illustrative transit by factory · {region} · {mode}",color_discrete_map={True:"#6c757d",False:"#20a486"}),use_container_width=True)
        st.dataframe(sim.round(1),hide_index=True,use_container_width=True)
        best=sim.iloc[0]
        if best.Factory != current:
            st.success(f"Distance-only candidate: **{best.Factory}** ({best['Relative time improvement (%)']:.1f}% lower proxy time than the current assignment). Validate capacity, real freight rates, and service levels before changing production.")
        else:
            st.success("Current factory is already the closest option under this illustrative distance proxy.")

with tab3:
    st.subheader("Ranked product reassignment candidates")
    rank=[]
    for product in sorted(view["Product Name"].unique()):
        current=PRODUCT_FACTORY.get(product)
        if not current: continue
        p=view[view["Product Name"]==product]
        for region in sorted(p["Region"].unique()):
            center=REGION_CENTER.get(region)
            if not center: continue
            cur_dist=haversine(FACTORIES[current],center)
            nearest,dist=min(((f,haversine(c,center)) for f,c in FACTORIES.items()),key=lambda z:z[1])
            if nearest != current:
                rank.append({"Product":product,"Region":region,"Current factory":current,"Closest factory":nearest,"Orders":p[p.Region==region]["Order ID"].nunique(),"Distance proxy reduction (mi)":cur_dist-dist,"Sales":p[p.Region==region]["Sales"].sum(),"Gross profit":p[p.Region==region]["Gross Profit"].sum()})
    rec=pd.DataFrame(rank)
    if rec.empty: st.info("No alternate factory candidates for the current filters.")
    else:
        rec=rec.sort_values(["Distance proxy reduction (mi)","Orders"],ascending=False)
        st.dataframe(rec.head(20).round(1),hide_index=True,use_container_width=True)
        st.caption("Ranking is based on distance proxy and observed order volume. It does not account for capacity, freight pricing, factory suitability, or real delivery performance; treat as shortlist for investigation.")
        st.download_button("Download candidate shortlist (CSV)",rec.to_csv(index=False).encode("utf-8"),"nassau_reassignment_candidates.csv","text/csv")

with tab4:
    st.subheader("Dataset profile")
    st.write(f"{len(df):,} rows · {df.shape[1]} source columns · {df['Order ID'].nunique():,} unique orders · {df['Product Name'].nunique()} products · {df['Region'].nunique()} customer regions")
    st.write("Source columns: Row ID, Order ID, Order Date, Ship Date, Ship Mode, Customer ID, Country/Region, City, State/Province, Postal Code, Division, Region, Product ID, Product Name, Sales, Units, Gross Profit, Cost.")
    st.write("Cleaning: trim text, parse dd-mm-yyyy dates, normalize product-name hyphen spacing, preserve postal codes as text. No rows are removed by default.")
    st.write("Project brief factory mappings and coordinates are embedded in this app. The regional center coordinates are explicitly illustrative. Haversine measures straight-line miles.")
    st.write("No predictive estimator is fitted because the target Ship Date is inconsistent with Order Date. RMSE/MAE/R² therefore are not reported. Replacing the heuristic with a validated predictive model requires corrected shipment records and route/freight/capacity data.")
    st.download_button("Download filtered rows (CSV)",view.to_csv(index=False).encode("utf-8"),"nassau_filtered_orders.csv","text/csv")
    st.dataframe(view.head(100),use_container_width=True)
