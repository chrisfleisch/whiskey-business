
import os
import pandas as pd

from transformations import (my_va_transform, my_size_transform, transform_currency,
    my_wc_transform, my_proof_transform)


dir_path = os.path.dirname(os.path.realpath(__file__))
read_dir = os.path.join(dir_path, '..', 'data_source')
save_dir = os.path.join(dir_path, '..', 'data_transformed')


def transform_data():
    # transform va price list
    va_df = pd.read_csv(os.path.join(read_dir, 'va_prices.csv'), skiprows=1)
    va_df.columns = va_df.columns.str.lower()
    va_df = va_df[va_df.description.str.contains('WHISKEY') | va_df.description.str.contains('WHISKY')]

    va_df['alt_brand'] = va_df['brand'].map(lambda x: my_va_transform(x))
    va_df['oz'] = va_df['size'].map(lambda x: my_size_transform(x))
    va_df['alt_price'] = va_df['price'].str.replace('$', '')
    va_df['alt_age'] = va_df['age'].str.replace('YR', '')

    # transform reddit whiskey archive
    w_archive = pd.read_csv(os.path.join(read_dir, 'reddit_archive.csv'),
                        names=['timestamp', 'whisky_name', 'reviewer_username', 'link',
                               'rating', 'style', 'bottle_price', 'review_date'],
                        skiprows=1,
                        parse_dates=['timestamp', 'review_date'])
    w_archive['rating'] = pd.to_numeric(w_archive['rating'], errors='coerce')
    w_archive['timestamp'] = pd.to_datetime(w_archive['timestamp'], errors='coerce')
    w_archive['review_date'] = pd.to_datetime(w_archive['review_date'], errors='coerce')
    w_archive['whisky_name'] = w_archive.whisky_name.str.lower()
    w_archive['style'] = w_archive['style'].str.lower()
    w_archive['alt_brand'] = w_archive['whisky_name'].map(lambda x: my_va_transform(x))
    w_archive['alt_bottle_price'] = w_archive['bottle_price'].map(lambda x: transform_currency(x))

    # transform whiskey critic
    wc_df = pd.read_csv(os.path.join(read_dir, 'metacritic.csv'))
    wc_df.columns = wc_df.columns.str.lower().str.replace(' ', '_')
    wc_df['alt_brand'] = wc_df['whisky'].map(lambda x: my_va_transform(x))
    wc_df['alt_brand'] = wc_df['alt_brand'].map(lambda x: my_wc_transform(x))

    # transform proof66:
    proof_df = pd.read_csv(os.path.join(read_dir, 'proof66.csv'))
    proof_df.columns = proof_df.columns.str.lower().str.replace(' ', '_')
    proof_df['alt_brand'] = proof_df['name'].map(lambda x: my_va_transform(x))
    proof_df['alt_brand'] = proof_df['alt_brand'].map(lambda x: my_proof_transform(x))

    va_df.to_csv(os.path.join(save_dir, 'va_prices.csv'), index=False)
    w_archive.to_csv(os.path.join(save_dir, 'reddit_archive.csv'), index=False)
    wc_df.to_csv(os.path.join(save_dir, 'meta_critic.csv'), index=False)
    proof_df.to_csv(os.path.join(save_dir, 'proof66.csv'), index=False)

if __name__ == '__main__':

    #download_data()
    transform_data()
