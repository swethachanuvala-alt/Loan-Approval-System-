"""
Re-train the loan-approval model and refresh the .pkl files in /model.

    python train_model.py

Run this once on your own machine if you want the saved model to be built with
exactly the same library versions you will deploy with.
"""
from utils.ml import (
    MODEL_PATH, SCALER_PATH, evaluate, fit_pipeline, load_dataset, save_artifacts,
)

if __name__ == "__main__":
    df = load_dataset()
    scaler, model = fit_pipeline(df)
    save_artifacts(scaler, model)
    m = evaluate(scaler, model, df)
    print("Saved:", SCALER_PATH.name, "and", MODEL_PATH.name)
    print(f"Accuracy {m['accuracy']:.3f} | Precision {m['precision']:.3f} | "
          f"Recall {m['recall']:.3f} | F1 {m['f1']:.3f} | ROC-AUC {m['roc_auc']:.3f}")
