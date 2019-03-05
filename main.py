from processing.series import TimeSeries
from data.MOCK.mock import Mock
from processing.features import feature_functions, weighted_average_based_history_function

if __name__ == '__main__':
    mock = Mock().create_graphs(3)
    ts = TimeSeries(mock)
    ts.set_feature_functions(feature_functions)
    ts.set_history_function(weighted_average_based_history_function)
    ts.learn_features()
    ts.create_time_series()
