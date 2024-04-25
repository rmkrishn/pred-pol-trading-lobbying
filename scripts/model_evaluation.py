"""Tools for model evaluation."""
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.lines as mlines

from sklearn.model_selection import TimeSeriesSplit

from darts import TimeSeries
from darts.metrics import mse
   
def cross_validate(model, col, plot=True, test_size=4, n_cv=5, metric=mse):
    """Cross-validate a model across a time-series split, and optionally plot
    forecasts.
    
    Args:
      model: Darts-style model to test -- needs to implement model.fit(data)
        and model.predict(n) for forecasting.
      col (pd.Series): Column to fit the model on.
      plot (bool, default True): whether to plot the series and model forecasts
        on validation data.
      test_size (int, default 4): Number of quarters of data to include in each
        validation set.
      n_cv (int, default 5): Number of validation sets to use.
      metric (callable, default mse): Metric used to score, a callable of
        signature (y_true, y_pred). Default is mean squared error.
      
    Returns:
      The score of the model across all validation splits.
    """
    kf = TimeSeriesSplit(n_cv, test_size=test_size)
    score = 0
    
    if plot:
        fig, ax = plt.subplots()
        sns.lineplot(col, ax=ax)
        forecast_line = mlines.Line2D([], [], color="gray", linestyle="dashed")
        true_line = mlines.Line2D([], [], color="gray", linestyle="solid")

    for train_idx, valid_idx in kf.split(col):
        col_train = TimeSeries.from_series(col.iloc[train_idx])
        col_valid = TimeSeries.from_series(col.iloc[valid_idx])

        model.fit(col_train)
        y_pred = model.predict(4)
        score += metric(col_valid, y_pred)

        if plot:
            y_pred.plot(linestyle="dashed", ax=ax)
            
    score = score / kf.get_n_splits()
    
    if plot:
        ax.legend(labels = ["observed", "forecast"], handles=[true_line, forecast_line])
        ax.set_title(col.name + f": score {score:0.3e}")
        
    return score