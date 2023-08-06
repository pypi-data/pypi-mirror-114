from sklearn.metrics import mean_squared_error as mse


def rmse(a, b):
    return mse(a, b) ** 0.5


def neg_rmse(a, b):
    return -rmse(a, b)
