from zscore import (
    compute_zscore,
    compute_weighted_zscore,
    plot_zscores,
    plot_weighted_scores,
    find_outliers,
    param_names,
)
from casafari import fetch_properties, SearchParameters
from preprocess import augment_properties

import pandas as pd
from time import sleep
import json
from tqdm.auto import tqdm


def fetch_properties_anomaly(parameters: SearchParameters, n=5):
    properties = fetch_properties(parameters)

    # 1. Gather all properties into a dataframe called `properties`.
    properties = pd.DataFrame(properties)

    # 1.1. Augment the properties dataframe with additional columns
    properties = augment_properties(properties)

    # 2. Compute the z-scores for each property
    properties_with_z_scores = compute_zscore(properties)

    # 3. Compute the weighted scores for each property
    properties_with_z_scores = compute_weighted_zscore(properties_with_z_scores)

    # 4. Find the outliers
    outliers = find_outliers(properties_with_z_scores, n=n)

    return outliers.to_dict("records")


if __name__ == "__main__":
    pbar = tqdm(total=3, bar_format="{l_bar}{bar:20}{r_bar}{bar:-20b}")
    # 0. Fetch properties from Casafari API
    pbar.set_description("Fetching properties from Casafari API")
    parameters = SearchParameters(
        search_operations=["sale"],
        city="Toulouse",
        zip_code=31_000,
        price_from=700_000,
        plot_area_from=2000,
        total_area_from=200,
        # created_date_from="2023-06-01",
    )
    properties = fetch_properties(parameters)
    with open("casafari2.json", "w") as f:
        json.dump(properties, f)
    pbar.update(1)

    # 1. Gather all properties into a dataframe called `properties`.
    properties = pd.DataFrame(properties)

    # 1.1. Augment the properties dataframe with additional columns
    properties = augment_properties(properties)

    # 2. Compute the z-scores for each property
    pbar.set_description("Computing z-scores")
    properties_with_z_scores = compute_zscore(properties)
    # sleep(2)
    pbar.update(1)

    # 3. Compute the weighted scores for each property
    pbar.set_description("Computing weighted scores")
    properties_with_z_scores = compute_weighted_zscore(properties_with_z_scores)
    # sleep(2)
    pbar.update(1)

    # 4. Plot the z-scores for each parameters
    plot_zscores(properties_with_z_scores)

    # 5. Plot the weighted scores
    plot_weighted_scores(properties_with_z_scores)

    # 3. Find the outliers
    pbar.set_description("Finding outliers")
    outliers = find_outliers(properties_with_z_scores)
    # sleep(2)
    pbar.update(1)

    # 4. Print the outliers
    for index, row in outliers.iterrows():
        print(f"Property ID: {row['property_id']}")
        # print first listing url and first thumbnail url
        listings = row["listings"]
        if len(listings) > 0:
            print(f"Listing URL: {listings[0]['listing_url']}")
            print(f"Thumbnail URL: {listings[0]['thumbnails'][0]}")
        for param in param_names.keys():
            print(f"{param_names[param]}: {row[param]}")
        print(f"Weighted Score: {row['weighted_score']}")
        print("")
