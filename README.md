# Nassau Candy Network Optimization Project

This project package contains a Streamlit decision-support dashboard, an analysis notebook, and written research/management summaries.

## Run locally (Windows)

1. Install Python 3.10 or newer from python.org and enable **Add Python to PATH**.
2. Open PowerShell in this folder.
3. Create and activate an environment:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install -r requirements.txt
   ```

4. Start the app:

   ```powershell
   streamlit run app.py
   ```

The browser opens the dashboard. Keep the CSV beside `app.py`.

## Notebook

Open `Nassau_Candy_Analysis.ipynb` in Jupyter or Google Colab. For Colab, upload the accompanying CSV when prompted or put both files in the same working folder. Run all cells from top to bottom.

## Main finding and limitation

The supplied dataset has 10,194 rows and no blank values in its source fields. Its Ship Date values imply 904–1,642 elapsed days after Order Date (median 1,274), so they are not suitable for a shipping lead-time model. The dashboard reports this issue and uses disclosed, illustrative straight-line distance proxies for scenario comparison. It does not present the proxy as a prediction. The project brief's factory/product mappings are included. Capacity, real routes, freight rates, and factory-specific cost data are absent, so recommendations are candidates to validate rather than operational instructions.

## Submission checklist

- Submit this project folder (or ZIP it) with the CSV, notebook, app, and written report.
- Include screenshots of the app's overview and scenario tabs if your portal requests evidence.
- Add your name, cohort, and mentor details to the executive summary before submission.
- Do not describe the distance proxy as a validated ML model. Mention the Ship Date issue in the report and presentation.
