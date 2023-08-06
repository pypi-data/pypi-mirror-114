from time import sleep
import numpy as np
from typing import Callable, Dict, Tuple

import pandas as pd
import nevergrad as ng
from multiprocess import Pool


def find_best_params(
        calc_strategy: Callable,
        df: pd.DataFrame,
        param_ranges: Dict[str, list]
) -> Tuple[float, Dict[str, float]]:
    params = {}
    for param_name in param_ranges:
        params[param_name] = ng.p.TransitionChoice(param_ranges[param_name])
    parametrization = ng.p.Instrumentation(
        df=ng.p.TransitionChoice([df]),
        **params
    )
    optimizer = ng.optimizers.NGOpt(parametrization=parametrization, budget=100)
    recommendation = optimizer.minimize(calc_strategy)
    best_params = recommendation.kwargs
    del best_params['df']
    best_profit = calc_strategy(df, **best_params)
    return -best_profit, best_params


def forward_test(
        calc_strategy: Callable,
        df: pd.DataFrame,
        param_ranges: Dict[str, list],
        window_train_days: int,
        window_test_days: int
) -> pd.DataFrame:
    train_window = window_train_days * 24 * 60
    test_window = window_test_days * 24 * 60

    epochs = int((len(df) - train_window) / test_window)

    epoch_train_ts = {}
    tasks = {}

    with Pool(processes=12) as pool:
        for epoch in range(epochs):
            epoch_start_learn = epoch * test_window
            epoch_end_learn = epoch_start_learn + train_window
            train_df = df[epoch_start_learn:epoch_end_learn].reset_index()
            tasks[epoch] = pool.apply_async(find_best_params, (
                calc_strategy,
                train_df.copy(),
                param_ranges
            ))
            epoch_train_ts[epoch] = [train_df['close_time'][0], train_df['close_time'][len(train_df) - 1]]
        df_result = pd.DataFrame(columns=['epoch', 'coef_eff',
                                          'train_profit', 'train_rel_profit',
                                          'test_profit'] + \
                                         list(param_ranges.keys()) + \
                                         ['ts_train_start', 'ts_train_end',
                                          'ts_test_start', 'ts_test_end']
                                 )
        total_epochs = len(tasks)
        while len(tasks):
            print("\r ", end="")
            print(f' leave epochs: {len(tasks)}/{total_epochs}'.ljust(40), end="")
            for epoch, task in tasks.copy().items():
                if task.ready():
                    epoch_start_test = epoch * test_window + train_window
                    epoch_end_test = epoch_start_test + test_window
                    test_df = df[epoch_start_test:epoch_end_test].reset_index()
                    train_profit, best_params = task.get()
                    test_profit = -calc_strategy(test_df, **best_params)
                    train_rel_profit = train_profit * window_test_days / window_train_days
                    del tasks[epoch]
                    df_result = df_result.append({
                        'epoch': epoch,
                        'train_profit': train_profit,
                        'train_rel_profit': train_rel_profit,
                        'test_profit': test_profit,
                        'coef_eff': calc_efficiency(train_rel_profit, test_profit),
                        **best_params,
                        'ts_train_start': epoch_train_ts[epoch][0],
                        'ts_train_end': epoch_train_ts[epoch][1],
                        'ts_test_start': test_df['close_time'][0],
                        'ts_test_end': test_df['close_time'][len(test_df) - 1]
                    }, ignore_index=True)
            sleep(1)
    print("\r ", end="")
    print(f' leave epochs: {len(tasks)}/{total_epochs}'.ljust(40))
    df_result = df_result.sort_values('epoch').reset_index()
    return df_result


def calc_efficiency(train_profit: float, test_profit: float) -> float:
    if train_profit <= 0:
        return np.nan
    return round((test_profit / train_profit) * 100, 2)
