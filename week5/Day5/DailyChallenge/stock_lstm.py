"""
Stock Price Prediction with LSTM using PyTorch
Daily Challenge Solution
"""

import os
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import r2_score
import joblib
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────
# 1. CONFIGURATION
# ─────────────────────────────────────────────
SEQUENCE_LENGTH = 60      # number of past days used to predict next day
BATCH_SIZE      = 64
EPOCHS          = 30
LEARNING_RATE   = 1e-3
HIDDEN_SIZE     = 128
NUM_LAYERS      = 2
DROPOUT         = 0.2
TEST_SIZE       = 0.1
VAL_SIZE        = 0.1

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {DEVICE}")


# ─────────────────────────────────────────────
# 2. LOAD & PREPROCESS DATA
# ─────────────────────────────────────────────
def load_and_preprocess(csv_path: str) -> tuple[np.ndarray, np.ndarray, MinMaxScaler]:
    """
    Load a single stock CSV, engineer features, and normalise.

    Returns
    -------
    X : np.ndarray, shape (n_samples, SEQUENCE_LENGTH, n_features)
    y : np.ndarray, shape (n_samples,)
    scaler : fitted MinMaxScaler (for the target column)
    """
    df = pd.read_csv(csv_path, parse_dates=["Date"])
    df.sort_values("Date", inplace=True)
    df.reset_index(drop=True, inplace=True)

    # Drop columns that leak the future or carry no signal
    drop_cols = [c for c in ["Date", "OpenInt", "Adj Close"] if c in df.columns]
    df.drop(columns=drop_cols, inplace=True)

    # Basic feature engineering
    df["Return"]    = df["Close"].pct_change()
    df["MA7"]       = df["Close"].rolling(7).mean()
    df["MA21"]      = df["Close"].rolling(21).mean()
    df["Volatility"]= df["Return"].rolling(7).std()

    # Target: next day's Close
    df["Target"] = df["Close"].shift(-1)
    df.dropna(inplace=True)

    feature_cols = [c for c in df.columns if c != "Target"]
    target_col   = "Target"

    # Fit one scaler on features, another on the target
    feat_scaler   = MinMaxScaler()
    target_scaler = MinMaxScaler()

    features_scaled = feat_scaler.fit_transform(df[feature_cols].values)
    target_scaled   = target_scaler.fit_transform(df[[target_col]].values).flatten()

    # Build sliding-window sequences
    X, y = [], []
    for i in range(SEQUENCE_LENGTH, len(df)):
        X.append(features_scaled[i - SEQUENCE_LENGTH : i])
        y.append(target_scaled[i])

    return np.array(X, dtype=np.float32), np.array(y, dtype=np.float32), target_scaler


# ─────────────────────────────────────────────
# 3. PYTORCH DATASET
# ─────────────────────────────────────────────
class StockDataset(Dataset):
    def __init__(self, X: np.ndarray, y: np.ndarray):
        self.X = torch.tensor(X)
        self.y = torch.tensor(y)

    def __len__(self):
        return len(self.y)

    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]


def make_loaders(X, y):
    n        = len(y)
    n_test   = max(1, int(n * TEST_SIZE))
    n_val    = max(1, int(n * VAL_SIZE))
    n_train  = n - n_val - n_test

    X_train, y_train = X[:n_train],           y[:n_train]
    X_val,   y_val   = X[n_train:n_train+n_val], y[n_train:n_train+n_val]
    X_test,  y_test  = X[n_train+n_val:],     y[n_train+n_val:]

    train_loader = DataLoader(StockDataset(X_train, y_train),
                              batch_size=BATCH_SIZE, shuffle=True,  drop_last=True)
    val_loader   = DataLoader(StockDataset(X_val,   y_val),
                              batch_size=BATCH_SIZE, shuffle=False, drop_last=False)
    test_loader  = DataLoader(StockDataset(X_test,  y_test),
                              batch_size=BATCH_SIZE, shuffle=False, drop_last=False)

    print(f"Dataset splits → train: {len(y_train):,}  val: {len(y_val):,}  test: {len(y_test):,}")
    return train_loader, val_loader, test_loader, y_test


# ─────────────────────────────────────────────
# 4. LSTM MODEL
# ─────────────────────────────────────────────
class LSTMPredictor(nn.Module):
    """
    Multi-layer LSTM followed by a fully-connected head.
    """
    def __init__(self, input_size: int, hidden_size: int = HIDDEN_SIZE,
                 num_layers: int = NUM_LAYERS, dropout: float = DROPOUT):
        super().__init__()
        self.lstm = nn.LSTM(
            input_size  = input_size,
            hidden_size = hidden_size,
            num_layers  = num_layers,
            batch_first = True,
            dropout     = dropout if num_layers > 1 else 0.0
        )
        self.dropout = nn.Dropout(dropout)
        self.fc      = nn.Linear(hidden_size, 1)

    def forward(self, x):
        # x: (batch, seq_len, features)
        out, _ = self.lstm(x)          # (batch, seq_len, hidden)
        out     = out[:, -1, :]        # take the last time-step
        out     = self.dropout(out)
        return self.fc(out).squeeze(-1)


# ─────────────────────────────────────────────
# 5. TRAINING
# ─────────────────────────────────────────────
def train_epoch(model, loader, optimizer, criterion):
    model.train()
    total_loss = 0.0
    for X_batch, y_batch in loader:
        X_batch, y_batch = X_batch.to(DEVICE), y_batch.to(DEVICE)
        optimizer.zero_grad()
        preds = model(X_batch)
        loss  = criterion(preds, y_batch)
        loss.backward()
        nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        optimizer.step()
        total_loss += loss.item() * len(y_batch)
    return total_loss / len(loader.dataset)


@torch.no_grad()
def evaluate(model, loader, criterion):
    model.eval()
    total_loss = 0.0
    for X_batch, y_batch in loader:
        X_batch, y_batch = X_batch.to(DEVICE), y_batch.to(DEVICE)
        preds      = model(X_batch)
        total_loss += criterion(preds, y_batch).item() * len(y_batch)
    return total_loss / len(loader.dataset)


def train(model, train_loader, val_loader):
    optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE, weight_decay=1e-5)
    criterion = nn.MSELoss()
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
        optimizer, patience=3, factor=0.5
    )

    best_val_loss = float("inf")
    best_state    = None

    print(f"\n{'Epoch':>6} │ {'Train MSE':>10} │ {'Val MSE':>10}")
    print("─" * 34)

    for epoch in range(1, EPOCHS + 1):
        train_loss = train_epoch(model, train_loader, optimizer, criterion)
        val_loss   = evaluate(model, val_loader,   criterion)
        scheduler.step(val_loss)

        if val_loss < best_val_loss:
            best_val_loss = val_loss
            best_state    = {k: v.cpu().clone() for k, v in model.state_dict().items()}

        if epoch % 5 == 0 or epoch == 1:
            print(f"{epoch:>6} │ {train_loss:>10.6f} │ {val_loss:>10.6f}")

    # Restore best weights
    model.load_state_dict(best_state)
    print(f"\nBest validation MSE: {best_val_loss:.6f}")
    return model


# ─────────────────────────────────────────────
# 6. EVALUATION
# ─────────────────────────────────────────────
@torch.no_grad()
def get_predictions(model, loader):
    model.eval()
    all_preds = []
    for X_batch, _ in loader:
        preds = model(X_batch.to(DEVICE)).cpu().numpy()
        all_preds.append(preds)
    return np.concatenate(all_preds)


def evaluate_r2(model, test_loader, y_test_scaled, scaler):
    preds_scaled = get_predictions(model, test_loader)

    # Inverse-transform both arrays to actual price space
    preds_actual = scaler.inverse_transform(preds_scaled.reshape(-1, 1)).flatten()
    true_actual  = scaler.inverse_transform(y_test_scaled.reshape(-1, 1)).flatten()

    r2 = r2_score(true_actual, preds_actual)
    mse = np.mean((preds_actual - true_actual) ** 2)
    rmse = np.sqrt(mse)
    print(f"\n{'─'*40}")
    print(f"  Test R²   : {r2:.4f}")
    print(f"  Test RMSE : {rmse:.4f}")
    print(f"{'─'*40}")
    return r2


# ─────────────────────────────────────────────
# 7. SAVE ARTEFACTS
# ─────────────────────────────────────────────
def save_artefacts(model, scaler, model_path="lstm_model.pt", scaler_path="scaler.pkl"):
    torch.save(model.state_dict(), model_path)
    joblib.dump(scaler, scaler_path)
    print(f"\nModel saved  → {model_path}")
    print(f"Scaler saved → {scaler_path}")


# ─────────────────────────────────────────────
# 8. MAIN
# ─────────────────────────────────────────────
def main(csv_path: str = None):
    # ── If no CSV is provided, generate synthetic data for demo ──────────────
    if csv_path is None or not os.path.exists(csv_path):
        print("No dataset found – generating synthetic stock data for demonstration.\n")
        rng = np.random.default_rng(42)
        n   = 2000
        dates = pd.date_range("2017-01-01", periods=n, freq="B")
        price = 100 + np.cumsum(rng.normal(0, 1, n))
        df    = pd.DataFrame({
            "Date"  : dates,
            "Open"  : price * (1 + rng.uniform(-0.005, 0.005, n)),
            "High"  : price * (1 + rng.uniform(0,      0.01,  n)),
            "Low"   : price * (1 - rng.uniform(0,      0.01,  n)),
            "Close" : price,
            "Volume": rng.integers(1_000_000, 10_000_000, n),
        })
        tmp = "/tmp/synthetic_stock.csv"
        df.to_csv(tmp, index=False)
        csv_path = tmp

    # ── Pipeline ─────────────────────────────────────────────────────────────
    print("Loading & preprocessing data …")
    X, y, target_scaler = load_and_preprocess(csv_path)
    print(f"Sequences shape: X={X.shape}  y={y.shape}")

    train_loader, val_loader, test_loader, y_test = make_loaders(X, y)

    input_size = X.shape[2]
    model = LSTMPredictor(input_size=input_size).to(DEVICE)
    total_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"\nModel: {model.__class__.__name__}  |  trainable params: {total_params:,}")

    model = train(model, train_loader, val_loader)

    r2 = evaluate_r2(model, test_loader, y_test, target_scaler)

    save_artefacts(model, target_scaler)

    return r2


if __name__ == "__main__":
    import sys
    csv_file = sys.argv[1] if len(sys.argv) > 1 else None
    main(csv_file)
