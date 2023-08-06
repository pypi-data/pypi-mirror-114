import numpy as np
import pandas as pd


class Model:
    def __init__(self, models, do_ranking: bool):
        self.models = models
        self.do_ranking = do_ranking

    def predict(self, data):
        y_hat = np.zeros(data.shape[0])
        for model in self.models:
            pred = model.predict_proba(data)[:, 1]

            if self.do_ranking:
                pred = pd.Series(pred).rank()

            pred = pred / len(self.models)

            y_hat += pred
        return y_hat
