from conf import param_names


def augment_properties(properties):
    param_names = {
        "total_area": "Surface totale",
        "plot_area": "Surface du terrain",
        "terrace_area": "Surface de la terrasse",
        "bathrooms": "Salles de bain",
        "bedrooms": "Chambres",
        "rooms": "Pièces",
        "sale_price_base": "Prix de vente",
        "sale_price_per_sqm_base": "Prix de vente par m²",
    }

    properties["sale_price_per_total_area"] = (
        properties["sale_price_base"] / properties["total_area"]
    )
    properties["sale_price_per_plot_area"] = (
        properties["sale_price_base"] / properties["plot_area"]
    )

    properties["sale_price_per_terrace_area"] = (
        properties["sale_price_base"] / properties["terrace_area"]
    )

    properties["sale_price_per_bathrooms"] = (
        properties["sale_price_base"] / properties["bathrooms"]
    )

    properties["sale_price_per_bedrooms"] = (
        properties["sale_price_base"] / properties["bedrooms"]
    )

    properties["sale_price_per_rooms"] = (
        properties["sale_price_base"] / properties["rooms"]
    )

    return properties
