import pandas as pd
from dateutil.relativedelta import relativedelta
from sklearn.decomposition import PCA, FastICA

from spoef.utils import (
    prepare_data_yearly,
    prepare_data_quarterly,
)
from spoef.feature_generation import compute_list_featuretypes


def create_global_transformer_PCA():
    global transformer 
    transformer = PCA(n_components=2)
    
    
def create_global_transformer_ICA():
    global transformer 
    transformer = FastICA(n_components=2)


def feature_creation_yearly_transformed(
    data,
    grouper,
    combine_fill_method,
    list_featuretypes=["B"],
    observation_length=1,
    fourier_n_largest_frequencies=30,
    wavelet_depth=6,
    mother_wavelet="db2",
):
    features = (
        data.groupby(grouper)
        .apply(
            compute_features_yearly_transformed,
            combine_fill_method=combine_fill_method,
            list_featuretypes=list_featuretypes,
            observation_length=observation_length,
            fourier_n_largest_frequencies=fourier_n_largest_frequencies,
            wavelet_depth=wavelet_depth,
            mother_wavelet=mother_wavelet,
        )
        .reset_index(level=1, drop=True)
    )
    return features


def compute_features_yearly_transformed(
    data,
    combine_fill_method,
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


def feature_creation_quarterly_transformed(
    data,
    grouper,
    combine_fill_method,
    list_featuretypes=["B"],
    observation_length=4,
    fourier_n_largest_frequencies=10,
    wavelet_depth=4,
    mother_wavelet="db2",
):

    features = (
        data.groupby(grouper)
        .apply(
            compute_features_quarterly_transformed,
            combine_fill_method=combine_fill_method,
            list_featuretypes=list_featuretypes,
            observation_length=observation_length,
            fourier_n_largest_frequencies=fourier_n_largest_frequencies,
            wavelet_depth=wavelet_depth,
            mother_wavelet=mother_wavelet,
        )
        .reset_index(level=1, drop=True)
    )
    return features


def compute_features_quarterly_transformed(
    data,
    combine_fill_method,
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

    # create features per month
    features = pd.DataFrame()
    for quarter in range(0, observation_length):
        data_quarter = prepared_data[
            (prepared_data.iloc[:, 0] >= start_date + relativedelta(months=3*quarter))
            & (prepared_data.iloc[:, 0] < start_date + relativedelta(months=3*quarter + 3))
        ]
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
