import sys
from pathlib import Path

import pytest

FOLDER = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(FOLDER))


def _require_model_deps():
    for mod in ("xgboost", "shap", "sklearn", "joblib", "anthropic", "dotenv"):
        pytest.importorskip(mod, reason=f"{mod} not installed (model dependencies needed)")


@pytest.fixture(scope="session")
def eval_set():
    """Fresh eval set built into memory (never reads or writes qualification_eval/eval_set.json)."""
    _require_model_deps()
    import build_eval_set

    return build_eval_set.build()
