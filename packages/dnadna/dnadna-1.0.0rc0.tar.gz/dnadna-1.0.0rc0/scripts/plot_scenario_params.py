#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import argparse
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt

def plot_scenario_params(scenario_params_path, to_pdf=True):
    scenario_params = pd.read_csv(args.scenario_params_path)
    size_time_keys = [k for k in scenario_params.keys() if (k[-5:] == '_size' and k != 'sample_size') or k[-5:] == '_time']
    if to_pdf:
        for k in size_time_keys:
            plt.hist(scenario_params.loc[:, k])
            plt.title(k)
            plt.savefig(f'plot_{k}.pdf')
            plt.close()
    else:
        for k in size_time_keys:
            plt.hist(scenario_params.loc[:, k])
            plt.title(k)
            plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--scenario_params_path", default="", type=str)
    parser.add_argument("--to_pdf", default=True, type=bool)
    args = parser.parse_args()
    plot_scenario_params(args.scenario_params_path, args.to_pdf)
