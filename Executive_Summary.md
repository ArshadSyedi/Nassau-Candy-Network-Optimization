# Executive Summary: Nassau Candy Network Planning

**Prepared by:** Arshad Syedi · **Cohort:** September Batch · **Mentor:** Unified Mentor.

## Objective

Review Nassau Candy order performance and create a prototype that helps compare product-to-factory assignments across customer regions.

## What the data says

The supplied file contains 10,194 order lines with product, customer-region, sales, unit, cost, and gross-profit information. It supports descriptive sales and margin analysis. However, its shipment dates imply 904–1,642 days between order and ship (median 1,274 days). These values are not credible shipping lead times, so no predictive lead-time model or model accuracy claim is reported.

## Prototype

The Streamlit dashboard summarizes sales and gross profit, filters by region/ship mode/division, compares the current factory with alternatives, and downloads a ranked geographic candidate shortlist. The scenario uses project-brief factory coordinates, coarse region centers, and disclosed ship-mode speed assumptions. It is an illustrative straight-line-distance proxy, not a delivery forecast. Profit impact remains neutral because freight rates and factory-specific costs/capacities were not supplied.

## Recommendation

Use the candidate list to guide investigation, not to change assignments. First validate the Ship Date field and collect actual shipment routes, freight charges, plant capacity, product eligibility, and service targets. With corrected data, train and evaluate lead-time models on a temporal holdout and optimize factory assignments under real capacity and cost constraints.

**Deliverables:** interactive app, reproducible analysis notebook, and full research report. Update the author and cohort fields above before submission.
