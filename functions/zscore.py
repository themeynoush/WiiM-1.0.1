import numpy as np
import pandas as pd
import json
import matplotlib.pyplot as plt
from scipy.stats import norm
import plotly.graph_objs as go

from preprocess import augment_properties
from conf import param_names, weights


def compute_zscore(properties):
    # List of parameters we're interested in

    # Initialize a dictionary to hold our stats
    stats = {}

    # 1. Calculate the mean and standard deviation for each parameter
    # while ignoring zeros (and NaN values which can arise from None in the JSON).
    for param in param_names.keys():
        values = properties[param].replace(
            0, np.nan
        )  # Replace 0s with NaN to ignore them
        stats[param] = {"mean": values.mean(), "std": values.std()}

    # 2. Compute the z-scores for each property
    # We'll add a new column for each z-score
    z_scores = pd.DataFrame()

    for param in param_names.keys():
        mean = stats[param]["mean"]
        std = stats[param]["std"]

        # Ignoring nan values in calculations
        z_scores[param + "_z"] = (properties[param].replace(0, np.nan) - mean) / std

    # Now, z_scores holds a dataframe where each column contains the z-scores for the corresponding parameter.

    # To keep the property IDs with the z-scores, we can join this dataframe with the property IDs.
    properties_with_z_scores = properties.join(z_scores)

    return properties_with_z_scores


def compute_weighted_zscore(properties_with_z_scores):
    # Calculate weighted scores for each property
    properties_with_z_scores["weighted_score"] = 0

    # Calculate the weighted score for each property,
    # ignoring the z-scores that are NaN.
    for column in properties_with_z_scores.columns:
        if column in weights:
            z_score_values = properties_with_z_scores[column]
            # Apply weights only to non-NaN z-score values
            z_score_values = z_score_values.replace(np.nan, 0)
            weighted_scores = z_score_values * weights[column]
            properties_with_z_scores["weighted_score"] += weighted_scores

    return properties_with_z_scores


def plot_zscores(properties_with_z_scores):
    # Helper function to create traces
    def create_traces(df, column, hover_text):
        trace_points = go.Scatter(
            x=df[column],
            y=norm.pdf(df[column]),
            mode="markers",
            marker=dict(color="blue", size=10),
            text=hover_text,  # the hover text
            name="Properties",
            hoverinfo="text",
        )
        return trace_points

    # Construct the Gaussian curve for each z-score parameter
    for column in properties_with_z_scores.columns:
        if "_z" in column:
            hover_text = properties_with_z_scores["property_id"]  # Define hover text
            trace_points = create_traces(properties_with_z_scores, column, hover_text)

            # Create a range of values representing our Gaussian curve
            x_curve = np.linspace(-3, 3, 200)  # Typical z-scores range from -3 to 3
            y_curve = norm.pdf(x_curve)

            trace_curve = go.Scatter(
                x=x_curve,
                y=y_curve,
                mode="lines",
                line=dict(color="red", width=2),
                name="Gaussian Curve",
                hoverinfo="none",  # no hover info
            )

            layout = go.Layout(
                title=f'Gaussian Distribution with Z-Scores of {column.replace("_z", "")}',
                xaxis=dict(title="Z-Scores"),
                yaxis=dict(title="Probability Density"),
                showlegend=False,
            )

            figure = go.Figure(data=[trace_curve, trace_points], layout=layout)

            # Save the figure in html format in plots folder
            figure.write_html(f'plots/{column.replace("_z", "")}.html')


# plot weighted scores as linear curve
def plot_weighted_scores(properties_with_z_scores):
    # clone the dataframe
    properties_with_z_scores = properties_with_z_scores.copy()

    # sort the dataframe by weighted score
    properties_with_z_scores = properties_with_z_scores.sort_values(by="weighted_score")

    def compute_hover_text(df):
        hover_text = []
        for index, row in df.iterrows():
            text = f"Property ID: {row['property_id']}<br>"
            text += f"Z-score: {row['weighted_score']}<br>"
            for param in param_names.keys():
                text += f"{param_names[param]}: {row[param]}<br>"
            hover_text.append(text)
        return hover_text

    def compute_url(df):
        url = []
        for index, row in df.iterrows():
            url.append(row["listings"][0]["listing_url"])
        return url

    # Create a trace for the weighted scores
    trace = go.Scatter(
        x=list(range(len(properties_with_z_scores))),
        y=properties_with_z_scores["weighted_score"],
        text=compute_hover_text(properties_with_z_scores),
        customdata=compute_url(properties_with_z_scores),
        mode="lines+markers",
        marker=dict(color="blue", size=10),
        name="Weighted Scores",
        hoverinfo="text",
    )

    layout = go.Layout(
        title="Weighted Scores",
        xaxis=dict(title="ID"),
        yaxis=dict(title="Weighted Score"),
        showlegend=False,
    )

    figure = go.Figure(data=[trace], layout=layout)

    # Save the figure in html format in plots folder
    figure.write_html(f"plots/weighted_scores.html")


def find_outliers(properties_with_z_scores, n=5):
    # Calculate weighted scores for each property
    properties_with_z_scores = compute_weighted_zscore(properties_with_z_scores)

    # Select properties with the most extreme weighted scores
    outliers = (
        properties_with_z_scores.nlargest(n, "weighted_score")
        if len(properties_with_z_scores) > n
        else properties_with_z_scores
    )

    # Sort the outliers by weighted score
    outliers = outliers.sort_values(by="weighted_score", ascending=False)

    return outliers


if __name__ == "__main__":
    # 0. Load the JSON data
    with open("casafari.json") as f:
        data = json.load(f)

    # 1. Gather all properties into a dataframe called `properties`.
    # This would be where you load your JSON data into the dataframe.
    properties = pd.DataFrame(data["results"])

    # 1.1. Augment the properties dataframe with additional columns
    properties = augment_properties(properties)

    # 2. Compute the z-scores for each property
    properties_with_z_scores = compute_zscore(properties)

    # 3. Compute the weighted scores for each property
    properties_with_z_scores = compute_weighted_zscore(properties_with_z_scores)

    # 4. Plot the z-scores for each parameters
    plot_zscores(properties_with_z_scores)

    # 5. Plot the weighted scores
    plot_weighted_scores(properties_with_z_scores)

    # 6. Find the outliers
    outliers = find_outliers(properties_with_z_scores)

    # 7. Print the outliers
    for index, row in outliers.iterrows():
        print(f"Property ID: {row['property_id']}")
        for param in param_names.keys():
            print(f"{param_names[param]}: {row[param]}")
        print(f"Weighted Score: {row['weighted_score']}")
        print("")
