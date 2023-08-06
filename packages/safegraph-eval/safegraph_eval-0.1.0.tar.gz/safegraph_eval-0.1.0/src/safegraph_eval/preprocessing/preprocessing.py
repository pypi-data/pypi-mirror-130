import pandas as pd

def q25(x):
    "Returns 25th percentile of a number"
    return x.quantile(0.25)

def q75(x):
    "Returns 75th percentile of a number"
    return x.quantile(0.75)

def label_and_remove_outliers_iqr(
    df_, group_column, column_to_filter, 
    k = 1.5, remove = True, verbose = True,
    brand_whitelist = [], placekey_whitelist = []
):
    """
    Label outliers in Patterns using k*IQR filtering, by group, and optionally remove them. 
    If remove, POIs with values in any month that are determined as outliers are removed.
    Returns a DataFrame.

    Parameters:
        df_ (pandas DataFrame): DataFrame containing SafeGraph Patterns data.
        group_column (str): The SafeGraph column that will be used to group the data (e.g., safegraph_brand_ids). Outliers are determined based in the distribution of values in each group.
        column_to_filter (str): The SafeGraph column on which perform the outlier filtering (e.g., raw_visit_counts).
    Optional Parameters:
        k (float): Value that will be multiplied by the interquartile range to determine outliers. Defaults to 1.5.
        remove (bool): Whether or not to remove the outlier rows from the returned DataFrame. Defaults to True.
        verbose (bool): If True, prints how many POI were removed as outliers. Defaults to True.
        brand_whitelist (list): List of safegraph_brand_ids to omit from the outlier filter. Defaults to an empty list.
        placekey_whitelist (list): List of placekeys to omit from the outlier filter. Defaults to an empty list.
    """

    df = df_.copy()
    
    df_grouped = df.groupby(group_column, as_index = False)[column_to_filter].agg(['min', q25, q75, 'max']).reset_index()
    df_grouped = df_grouped.assign(iqr = df_grouped['q75'] - df_grouped['q25'])
    df_grouped = df_grouped.assign(
        min_range = df_grouped['q25'] - k * df_grouped['iqr'],
        max_range = df_grouped['q75'] + k * df_grouped['iqr'])[[group_column, 'min_range', 'max_range']]
    df = df.merge(df_grouped, on = group_column, how = 'left')
    df = df.assign(
        outlier = (
            (df[group_column].notnull()) & # do not filter POI with a null group_column (e.g., unbranded POI)
            (df[column_to_filter] < df['min_range']) | (df[column_to_filter] > df['max_range'])
        )
    )
    outlier_placekeys = df.loc[df['outlier']]['placekey'].unique()
    
    if remove:
        rows_to_keep = (
            (~df['placekey'].isin(outlier_placekeys)) |
            (df['safegraph_brand_ids'].isin(brand_whitelist)) |
            (df['placekey'].isin(placekey_whitelist))    
        )
        df = df.loc[rows_to_keep]
        
        if verbose:
            print(str(len(df_['placekey'].unique()) - len(df['placekey'].unique())) + ' POI out of ' + str(len(df_['placekey'].unique())) + ' were removed as outliers.\n')
    
        df = df.drop(columns = ['min_range', 'max_range', 'outlier'])
    
    return(df)