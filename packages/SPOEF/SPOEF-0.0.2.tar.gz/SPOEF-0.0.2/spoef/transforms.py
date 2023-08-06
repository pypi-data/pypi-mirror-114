import pandas as pd
from dateutil.relativedelta import relativedelta
from sklearn.decomposition import PCA, FastICA

from spoef.utils import (
    prepare_data_yearly,
    prepare_data_quarterly,
)
from spoef.feature_generation import compute_list_featuretypes


def create_transformer_PCA():
    transformer = PCA(n_components=2)
    return transformer
    
    
def create_transformer_ICA():
    transformer = FastICA(n_components=2)
    return transformer


def feature_generation_transformed(
    data,
    grouper,
    combine_fill_method,
    time_window,
    transformer_type,
    list_featuretypes=["Basic"],
    observation_length=1,
    fourier_n_largest_frequencies=10,
    wavelet_depth=4,
    mother_wavelet="db2",
):
    """
    This function splits the data per identifier and performs the feature
    generation.

    list_featuretypes:
        "Basic" - min, max, mean, kurt ,skew, std, sum.
        "FourierComplete" - all frequencies amplitudes and phases.
        "FourierNLargest" - n largest frequencies and their values.
        "WaveletComplete" - all approximation and details coefficients at each depth.
        "WaveletBasic" - takes "Basic" (min, max, etc) at each depth.

    Args:
        data (pd.DataFrame()) : data from one identifier for which to make features.
        combine_fill_method (str) : 'balance' or 'transaction'.
        observation_length (int) : number of recent time windows you want for the analysis.
        normalize (bool) : normalize data in time window
        list_featuretypes (list) : list of feature types to be computed.
        fourier_n_largest_frequencies (int) : amount of fourier features.
        wavelet_depth (int) : level of depth up to which the wavelet is computed.
            possible values: 3 is the max, depends on len(data)
        mother_wavelet (str) : type of wavelet used for the analysis.
            possible values: "db2", "db4", "haar", see pywt.wavelist(kind="discrete")
    Returns:
        features (pd.DataFrame()) : df with row of features for each identifier.

    """
    if time_window == 'quarter':
        features = (
            data.groupby(grouper)
            .apply(
                compute_features_quarterly_transformed,
                combine_fill_method=combine_fill_method,
                transformer_type=transformer_type,
                list_featuretypes=list_featuretypes,
                observation_length=observation_length,
                fourier_n_largest_frequencies=fourier_n_largest_frequencies,
                wavelet_depth=wavelet_depth,
                mother_wavelet=mother_wavelet,
            )
            .reset_index(level=1, drop=True)
        )
    elif time_window == 'year':
        features = (
            data.groupby(grouper)
            .apply(
                compute_features_yearly_transformed,
                combine_fill_method=combine_fill_method,
                transformer_type=transformer_type,
                list_featuretypes=list_featuretypes,
                observation_length=observation_length,
                fourier_n_largest_frequencies=fourier_n_largest_frequencies,
                wavelet_depth=wavelet_depth,
                mother_wavelet=mother_wavelet,
            )
            .reset_index(level=1, drop=True)
        )
    else:
        raise ValueError('Please enter one of ["quarter", "year"]')
    
    # Check if NaNs are generated
    na_list = []
    na_list.append(features.isna().sum().sum())
    if sum(na_list) != 0:
        raise ValueError("There are NaNs generated in the following columns:", na_list)
    
    return features


def compute_features_yearly_transformed(
    data,
    combine_fill_method,
    transformer_type,
    list_featuretypes,
    observation_length,
    fourier_n_largest_frequencies,
    wavelet_depth,
    mother_wavelet,
):

    # drop identifier column
    data = data.drop(data.columns[0], axis=1)

    # select only relevant period and fill the empty date
    trans_data = prepare_data_yearly(data[["date", "transaction"]], "transaction", observation_length)
    bal_data = prepare_data_yearly(data[["date", "balance"]], "balance", observation_length)
    prepared_data = trans_data.merge(bal_data, on="date")

    start_date = prepared_data.iloc[0, 0]

    # create features per year
    features = pd.DataFrame()
    for year in range(0, observation_length):
        data_year = prepared_data[
            (prepared_data.iloc[:, 0] >= start_date + relativedelta(years=year))
            & (prepared_data.iloc[:, 0] < start_date + relativedelta(years=year + 1))
        ]
        if transformer_type == 'PCA':
            transformer = create_transformer_PCA()
        elif transformer_type == 'ICA':
            transformer = create_transformer_ICA()  
        else:
            raise ValueError('Please enter one of ["PCA", "ICA"] for the transformer_type')
        data_transformed = pd.DataFrame(transformer.fit_transform(data_year.iloc[:,[1,2]]))
        for i in range(2):
            data_used = data_transformed.iloc[:,i]
            transformed_features = compute_list_featuretypes(
                data_used,
                list_featuretypes,
                fourier_n_largest_frequencies,
                wavelet_depth,
                mother_wavelet,
            )
            # name columns
            transformed_features.columns = [
                f"{i} Y_"
                + str(year + 1)
                + "/"
                + str(observation_length)
                + " "
                + col
                for col in transformed_features.columns
            ]
            features = pd.concat([features, transformed_features], axis=1)
    return features


def compute_features_quarterly_transformed(
    data,
    combine_fill_method,
    transformer_type,
    list_featuretypes,
    observation_length,
    fourier_n_largest_frequencies,
    wavelet_depth,
    mother_wavelet,
):
    # drop identifier column
    data = data.drop(data.columns[0], axis=1)

    # select only relevant period and fill the empty date
    trans_data = prepare_data_quarterly(data[["date", "transaction"]], "transaction", observation_length)
    bal_data = prepare_data_quarterly(data[["date", "balance"]], "balance", observation_length)
    prepared_data = trans_data.merge(bal_data, on="date")
    
    start_date = trans_data.iloc[0, 0]

    # create features per quarter
    features = pd.DataFrame()
    for quarter in range(0, observation_length):
        data_quarter = prepared_data[
            (prepared_data.iloc[:, 0] >= start_date + relativedelta(months=3*quarter))
            & (prepared_data.iloc[:, 0] < start_date + relativedelta(months=3*quarter + 3))
        ]
        if transformer_type == 'PCA':
            transformer = create_transformer_PCA()
        elif transformer_type == 'ICA':
            transformer = create_transformer_ICA()  
        else:
            raise ValueError('Please enter one of ["PCA", "ICA"] for the transformer_type')
        data_transformed = pd.DataFrame(transformer.fit_transform(data_quarter.iloc[:,[1,2]]))
        for i in range(2):
            data_used = data_transformed.iloc[:,i]
            transformed_features = compute_list_featuretypes(
                data_used,
                list_featuretypes,
                fourier_n_largest_frequencies,
                wavelet_depth,
                mother_wavelet,
            )
            # name columns
            transformed_features.columns = [
                f"{i+1} Q_"
                + str(quarter + 1)
                + "/"
                + str(observation_length)
                + " "
                + col
                for col in transformed_features.columns
            ]
            features = pd.concat([features,transformed_features], axis=1)
    return features
