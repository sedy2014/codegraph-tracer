"""Small AdaBoost classifier using decision stumps. Demo project for /cg-trace and /cg-ask."""
import numpy as np


def best_stump(X, y, w):
    """Find the feature, threshold and sign with the lowest weighted error."""
    best = {"error": np.inf}
    for feature in range(X.shape[1]):
        for threshold in np.unique(X[:, feature]):
            for sign in (1, -1):
                pred = stump_predict(X, feature, threshold, sign)
                error = w[pred != y].sum()
                if error < best["error"]:
                    best = {"error": error, "feature": feature,
                            "threshold": threshold, "sign": sign}
    return best


def stump_predict(X, feature, threshold, sign):
    """Predict +1 or -1 by comparing one feature to a threshold."""
    return np.where(sign * (X[:, feature] - threshold) >= 0, 1, -1)


def fit(X, y, n_rounds=10):
    """Train AdaBoost: repeatedly pick a stump, then reweight misclassified samples."""
    w = np.full(len(y), 1 / len(y))
    model = []
    for _ in range(n_rounds):
        stump = best_stump(X, y, w)
        err = max(stump["error"], 1e-10)
        alpha = 0.5 * np.log((1 - err) / err)
        pred = stump_predict(X, stump["feature"], stump["threshold"], stump["sign"])
        w = w * np.exp(-alpha * y * pred)
        w /= w.sum()
        model.append((alpha, stump))
    return model


def predict(model, X):
    """Combine all stumps by a weighted vote."""
    score = np.zeros(len(X))
    for alpha, s in model:
        score += alpha * stump_predict(X, s["feature"], s["threshold"], s["sign"])
    return np.where(score >= 0, 1, -1)


def main():
    rng = np.random.default_rng(0)
    X = rng.normal(size=(200, 2))
    y = np.where(X[:, 0] + X[:, 1] ** 2 > 0.5, 1, -1)
    model = fit(X, y, n_rounds=15)
    acc = (predict(model, X) == y).mean()
    print(f"training accuracy: {acc:.2%}")


if __name__ == "__main__":
    main()
