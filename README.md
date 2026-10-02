# 💜 LoanLens — Loan Approval Predictor

A multipage Streamlit web app for the loan-approval Logistic Regression model built in `notebook/GGST_7.ipynb`.

**Pages:** Home · Check Eligibility · Insights · Model Lab · About

## Project structure

```
loan-approval-app/
├── app.py                  # entry point + top navigation
├── views/                  # one file per page
│   ├── home.py
│   ├── eligibility.py      # prediction form, gauge, explanations, what-ifs
│   ├── insights.py         # interactive data dashboard
│   ├── model_lab.py        # metrics, ROC, confusion matrix, model comparison
│   └── about.py
├── utils/
│   ├── ml.py               # model loading / training / prediction helpers
│   ├── loaders.py          # cached data + model loaders
│   ├── theme.py            # purple design system (CSS, palette, Plotly style)
│   └── art.py              # SVG illustrations (bank, coins, house, shield...)
├── model/
│   ├── logistic_regression_model.pkl
│   └── scaler.pkl
├── data/loan_prediction_dataset.csv
├── notebook/GGST_7.ipynb
├── train_model.py          # re-creates the .pkl files from the CSV
├── requirements.txt
└── .streamlit/config.toml  # purple theme
```

## Run it locally (Windows CMD / VS Code terminal)

```bash
cd loan-approval-app
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

(macOS/Linux: activate with `source venv/bin/activate`.)

The app opens at http://localhost:8501

## Use your own trained model files (recommended)

The `.pkl` files in `model/` were re-created from your notebook's pipeline. To use the exact files from *your* notebook,
copy your own `scaler.pkl` and `logistic_regression_model.pkl` into the `model/` folder (replace the two files).

Or run `python train_model.py` to rebuild both files with the library versions installed on your machine.

If a `.pkl` file is missing or was saved with an incompatible scikit-learn version, the app automatically re-trains
the model from the CSV, so it will not crash.

## Push to GitHub

```bash
git init
git add .
git commit -m "LoanLens: loan approval predictor"
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo>.git
git push -u origin main
```

## Deploy on Streamlit Community Cloud

1. Go to https://share.streamlit.io and sign in with GitHub.
2. Click **Create app** → choose your repository and the `main` branch.
3. Set **Main file path** to `app.py`.
4. Click **Deploy**. The first build takes a few minutes while it installs `requirements.txt`.

## Notes

- Inputs are limited to the ranges found in the training data (age 20–69, income 4,000–100,000, credit score 300–850, 0–4 dependents).
- Illustrations are inline SVGs, so there are no image files to upload. To use real photos, put them in an `assets/` folder and show them with `st.image("assets/photo.jpg")`.
- For learning and demonstration only — not financial advice.
