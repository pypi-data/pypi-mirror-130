from datetime import time
import os
import stat
import getpass
import numpy as np
import pandas as pd
import importlib
from pathlib import Path

from tfcaidm.common import timedate
from tfcaidm.data.jclient import JClient
from tfcaidm.metrics.custom import registry

import tfcaidm.metrics.funcs.acc as acc
import tfcaidm.metrics.funcs.dice as dice
import tfcaidm.metrics.funcs.distance as distance


# TODO: need to ensure use is not submitting code that has been trained on all of the data
# TODO: make sure user cannot just write to a file (user submits a single file that later populates dataframe), file is not writeable
# TODO figure out private attr results
# USAGE: user types benchmark -d "dataset name" -c "client path" -m "model path" -i "information on their model" and run will be submitted
# Alternatively I keep it in the library but more susceptible to security issues.

desc = (
    "Any information you would like to share about your model or how you trained it :)"
)


class Score:
    def __init__(self, client_path):
        self.client_path = client_path

    @property
    def metrics(self):
        metrics = registry.custom_metric()
        return metrics[self.client_path["SOME FIELD TO TELL ME WHAT METRIC TO USE"]]


class Benchmark:
    """
    Example:

    # --- Get some benchmark related information.
    Benchmark.help(optional_path)

    # --- View the leaderboard!
    Benchmark.view_leaderboard(optional_path)

    # --- Instantiate a benchmark object
    benchmark = Benchmark(client_path=(...))

    # --- Run model evaluation...
    benchmark.run(model)

    # --- If you are happy with your score, submit it!
    benchmark.submit()

    # --- View the new updated leaderboard!
    Benchmark.view_leaderboard(optional_path)
    """

    def __init__(self, client_path, desc=desc):
        self.client_path = client_path
        # self.client = JClient(client_path)

        self.desc = desc
        self._results = []
        self._storage = "BENCHMARK PATH"

    @property
    def results(self):
        return self._results

    @property
    def score(self):
        return self._score

    @property
    def storage(self):
        return self._storage

    def check(self, y_true, y_pred):

        ytk = y_true.keys()
        ypk = y_pred.keys()
        yts = [v.shape for v in y_true.values()]
        yps = [v.shape for v in y_pred.values()]

        assert (
            ytk == ypk
        ), f"ERROR! Expecting output_name={ytk} but getting pred_name={ypk}"
        assert (
            yts == yps
        ), f"ERROR! Expecting output_shape={yts} but getting pred_shape={yps}"

    def infer(self, model, xs, **kwargs):
        """To set the correct outputs during model inference.
        For expected inputs and outputs, use `Benchmark.help()`.

        NOTE: This method (only this method) can be modified (overloaded).

        Args:
            model (tf model): A trained tensorflow model
            xs (dict): The inputs ingested by the model

        Returns:
            dict : The outputs of the model
        """

        return model(xs)

    def run(self, model, **kwargs):
        importlib.reload(registry)
        importlib.reload(acc)
        importlib.reload(dice)
        importlib.reload(distance)

        _, gen_data = self.client.create_generators(test=True)

        results = []

        for xs, ys in gen_data:
            if ys:
                xs = {**xs, **ys}

            pred = self.infer(model, xs, **kwargs)
            self.check(ys, pred)

            result = self._score(ys, pred)
            results.append(result)

        self._results = float(np.array(results).mean())

        return self._results

    def _score(self):
        return Score(self.client_path).metrics

    def submit(self):

        # --- Submit scores
        assert (
            type(self._results) == float
        ), f"ERROR! Model results must be of type float!"

        schema = {
            "User": getpass.getuser(),
            "Dataset": self.client,
            "Task": self.client,
            "Model": self.client,
            "# Params": self.client,
            "Description": self.desc,
            "Metrics": self.client,
            "Score": self._results,
            "Date": timedate.get_mdy(),
        }

        schema = {k: [v] for k, v in schema.items()}

        pd.DataFrame(schema).to_csv(self._storage)
        os.chmod(self._storage, stat.S_IREAD | stat.S_IRGRP | stat.S_IROTH)

        print("- congratulations your run has been submitted!")

    @staticmethod
    def view_leaderboard(client_path):

        leaderboad = []

        # --- Specific leaderboard
        if client_path is not None:
            leaderboad += [pd.read_csv(client_path, index=False)]

        # --- All leaderboard
        else:
            TODO_path = os.listdir()  # TODO
            leaderboad += [pd.read_csv(TODO_path, index=False)]

        print(leaderboad)

        return pd.read_csv(leaderboad)

    @staticmethod
    def help(client_path=None):

        # TODO: Ask peter where benchmark related code can reside, should be some external file following a specific format.

        schema = {
            "Dataset": [],
            "Client": [],
            "Description": [],
            "Annotation": [],
            "Additional Information": [],
            "# Training Samples": [],
            "# Validation Samples": [],
        }

        information = []

        # --- Specific benchmark information
        if client_path is not None:
            information += [pd.read_csv(client_path, index=False)]

        # --- All benchmark information
        else:
            TODO_path = os.listdir()  # TODO
            information += [pd.read_csv(TODO_path, index=False)]

        print(information)

        return pd.DataFrame(information)


def get_csvs(path=None):

    # --- Single csv dataframe
    if path is not None:
        return [pd.read_csv(path, index=False)]

    # --- Multi csv dataframe
    else:
        TODO_path = os.listdir()  # TODO
        return [pd.read_csv(TODO_path, index=False)]
