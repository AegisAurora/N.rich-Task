import sys
import time
import pandas as pd

def normalize_trend_score(change, pos_scale, neg_scale):
    if change > 0:
        return 50 + (50 * (change / pos_scale))
    elif change < 0:
        return 50 - (50 * (abs(change) / neg_scale))
    else:
        return 50

def process_data(input_file, output_file):
    """
    Process the data in input_file path and output the processed data to output_file path.
    The script can be optimized for efficiency if needed, by using polars instead of pandas for example.

    Parameters:
    - input_file: path to input file
    - output_file: path to output file
    """
    start_time = time.time()   
    print(f"Starting data processing for file {input_file}",flush=True)
    df = pd.read_csv(input_file)
    print(f"Data loaded successfully from {input_file}.",flush=True)

    # asserts
    print("Performing data integrity checks...",flush=True)
    assert df.groupby('topic_id')['category_id'].nunique().max() == 1, "Each topic_id should map to only one category_id"
    assert df.groupby('company_id')['industry_id'].nunique().max() == 1, "Each company_id should map to only one industry_id"
    assert not df['interest_level'].isnull().any(), "There should be no missing values in 'interest_level' column"
    assert not df['week'].isnull().any(), "There should be no missing values in 'week' column"
    assert pd.api.types.is_numeric_dtype(df['interest_level']), "'interest_level' must be a numeric type"
    assert df['interest_level'].between(0, 100).all(), "Interest levels should be between 0 and 100"
    print("Data integrity checks passed.",flush=True)
    # script
    print("Starting data processing",flush=True)
    df["original_indicator"] = True
    # pairs from the original dataset
    unique_pairs = df[['company_id', 'topic_id']].drop_duplicates()
    all_weeks = pd.DataFrame({
        'week': range(df['week'].min(), df['week'].max() + 1)
    })
    # cross join with a key
    unique_pairs['key'] = 1
    all_weeks['key'] = 1
    all_combinations = pd.merge(unique_pairs, all_weeks, on='key').drop('key', axis=1)

    df_full = pd.merge(all_combinations, df, on=['company_id', 'topic_id', 'week'], how='left')
    df_full['original_indicator'] = ~df_full['interest_level'].isna()
    # replace NaNs in 'interest_level' with 0
    df_full['interest_level'] = df_full['interest_level'].fillna(0)

    df_full['weekly_change'] = df_full.groupby(['company_id', 'topic_id'])['interest_level'].diff()


    df_full['smoothed_change'] = df_full.groupby(['company_id', 'topic_id'])['weekly_change'].transform(lambda x: x.ewm(halflife=2).mean())

    pos_scale = df_full['smoothed_change'][df_full['smoothed_change'] > 0].max()
    neg_scale = df_full['smoothed_change'][df_full['smoothed_change'] < 0].abs().max()

    #exclude non-original data points
    df_full = df_full[df_full["original_indicator"]]
    # apply normalization to calculate the trend scores
    df_full['trend_score'] = df_full['smoothed_change'].apply(normalize_trend_score, args=(pos_scale, neg_scale))
    df_full = df_full[['company_id', 'topic_id', 'category_id','industry_id', 'week', 'interest_level', 'trend_score']]
    df_full.to_csv(output_file, index=False)
    end_time = time.time()
    print(f"Script completed in {end_time - start_time:.2f} seconds",flush=True)


if __name__ == '__main__':
    input_file_path = sys.argv[1]
    output_file_path = sys.argv[2]
    print(f"Script started with input file {input_file_path} and output file {output_file_path}.",flush=True)
    process_data(input_file_path, output_file_path)
