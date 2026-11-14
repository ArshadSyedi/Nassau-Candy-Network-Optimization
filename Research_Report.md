# Factory Reallocation & Shipping Optimization Recommendation System

**Organization:** Nassau Candy Distributor. 
**Prepared:** 13 November 2026.  
**Prepared by:** Arshad Syedi.  
**Program / mentor:** Batch September and Unfied mentor.
## Executive summary

This project reviews 10,194 order-line records and builds a decision-support prototype for factory assignment analysis. The source has 18 fields covering order dates, ship mode, customer geography, product, sales, units, gross profit, and cost. No source field is blank in the supplied file. Sales and profit summaries can support descriptive business analysis.

The file's Ship Date field is not operationally credible: dates are between 904 and 1,642 days after Order Date, with a median interval of 1,274 days. Therefore, this work does not train a lead-time model or claim actual delivery-time improvements. The accompanying Streamlit app compares factories using straight-line distance from the project-brief factory coordinates to broad, illustrative region centers. This heuristic is a screening tool, not a shipping forecast.

The most defensible recommendation is to treat the ranked product-region assignments as candidates for validation. Before any factory move, obtain corrected ship timestamps, route-level costs and distances, plant capacity, factory-product eligibility, and service-level targets. Those data are prerequisites for testing a true multi-objective optimization and supervised prediction system.

## Business problem

Static product-to-factory assignments may create avoidable transportation distance and uneven service. Leadership needs to compare alternate assignments and understand tradeoffs in shipping performance, profit, risk, and feasibility. The available file contains order and financial measures, while the project brief supplies product-factory mappings and five factory coordinates.

## Project questions

1. How do sales, units, gross profit, and margin vary by product, region, and ship mode?
2. Does the supplied shipment-date field support lead-time modeling?
3. Which alternate factory is geographically closest to a broad customer-region proxy for each current product assignment?
4. What additional data is needed to convert a geographic shortlist into an implementable recommendation?

## Data and preparation

The CSV contains 10,194 rows and 18 columns. Text is trimmed, dates are parsed using day-month-year format, postal codes are retained as text, and product-name hyphen spacing is normalized. Derived measures include order month, gross margin, and the raw order-to-ship interval for data-quality review. No observations are silently removed.

The project brief provides the following current product-to-factory mapping:

| Current factory | Products |
|---|---|
| Lot's O' Nuts | Wonka Bar - Nutty Crunch Surprise; Wonka Bar - Fudge Mallows; Wonka Bar - Scrumdiddlyumptious |
| Wicked Choccy's | Wonka Bar - Milk Chocolate; Wonka Bar - Triple Dazzle Caramel |
| Sugar Shack | Laffy Taffy; SweeTARTS; Nerds; Fun Dip; Fizzy Lifting Drinks |
| Secret Factory | Everlasting Gobstopper; Lickable Wallpaper; Wonka Gum |
| The Other Factory | Hair Toffee; Kazookles |

## Methods

### Descriptive analytics

Aggregate unique orders, units, sales, gross profit, and profit margin by division, region, ship mode, country, state, and product. Monthly sales/profit trends are shown in the notebook and dashboard.

### Shipping-data validation

Compute `(Ship Date - Order Date)` only to inspect data plausibility. The resulting 904–1,642 day range (median 1,274 days) makes it unsuitable as a real transit target. Predictive models and RMSE, MAE, and R² are intentionally withheld; fabricated model scores would give false confidence.

### Factory scenario proxy

The app applies the Haversine formula to the five factory coordinates and broad region-center coordinates, then divides straight-line miles by an explicitly assumed speed for each ship mode. It reports relative distance/time proxy comparisons and holds profit neutral. Region centers, speeds, and proxy travel times are assumptions; they are not sourced delivery observations. The candidate shortlist also shows observed order count, sales, and gross profit as context, not as causal effects.

## Findings and limitations

- The supplied data is useful for historical sales and gross-profit reporting.
- The Ship Date values are inconsistent with ordinary parcel lead times and require correction or owner confirmation.
- Customer regions are categorical; a single broad center does not represent the true location mix within the region.
- Straight-line miles differ from actual truck routes, network constraints, and carrier pricing.
- The data has no factory capacity, production eligibility, lane cost, inventory, or service-level fields.
- Gross profit is available at order level, but no factory-specific production cost or shipping expense exists. Profit impact from relocation cannot be estimated credibly.
- Correlation or clustering cannot establish that reassignment causes better service or profitability.

## Recommendations

1. Ask the data owner to correct or explain Ship Date and verify date formats and time zones.
2. Use the dashboard's top distance-reduction candidates as a shortlist for operational review only.
3. Add plant capacity, SKU capability, actual customer coordinates, lane-level distances, freight rates, and shipment service targets.
4. Once dates are fixed, compare regression baselines and tree-based models using a temporal holdout; report RMSE, MAE, and R² with uncertainty and segment-level error checks.
5. Formulate assignment optimization with explicit capacity, product eligibility, service-level, and budget constraints. Compare speed-versus-cost scenarios and test stability before execution.

## Deliverables

- `Nassau_Candy_Analysis.ipynb`: reproducible EDA, cleaning, validation, and scenario shortlist.
- `app.py`: interactive Streamlit dashboard with filters, charts, factory scenario simulator, and CSV downloads.
- `Nassau Candy Distributor.csv`: supplied source data.
- `Executive_Summary.md`: concise stakeholder brief.

## Conclusion

The prototype makes sales patterns and geographical assignment scenarios easier to inspect while keeping the limitations visible. It is a useful first decision-support artifact, but the current file cannot substantiate shipment-time predictions or profit-optimized factory relocation. Correct shipment data and operational cost/capacity inputs are the next steps toward a validated recommendation system.
