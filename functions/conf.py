# params names in french
param_names = {
    "total_area": "Surface totale",
    "plot_area": "Surface du terrain",
    "terrace_area": "Surface de la terrasse",
    "bathrooms": "Salles de bain",
    "bedrooms": "Chambres",
    "rooms": "Pièces",
    "sale_price_base": "Prix de vente",
    "sale_price_per_total_area": "Prix de vente par m² de surface",
    "sale_price_per_plot_area": "Prix de vente par m² de terrain",
    "sale_price_per_terrace_area": "Prix de vente par m² de terrasse",
    "sale_price_per_bathrooms": "Prix de vente par salle de bain",
    "sale_price_per_bedrooms": "Prix de vente par chambre",
    "sale_price_per_rooms": "Prix de vente par pièce",
}

# weights for each parameter
weights = {
    "total_area_z": 1.5,  # Higher is better
    "plot_area_z": 1.0,  # Higher is better
    "terrace_area_z": 1.0,  # Higher is better
    "bathrooms_z": 0.5,  # Higher is better
    "bedrooms_z": 0.5,  # Higher is better
    "rooms_z": 0.5,  # Higher is better
    "sale_price_base_z": -1.5,  # Lower is better
    "sale_price_per_sqm_base_z": -1.0,  # Lower is better
    "sale_price_per_total_area_z": -1.0,  # Lower is better
    "sale_price_per_plot_area_z": -1.0,  # Lower is better
    "sale_price_per_terrace_area_z": -1.0,  # Lower is better
    "sale_price_per_bathrooms_z": -0.5,  # Lower is better
    "sale_price_per_bedrooms_z": -0.5,  # Lower is better
    "sale_price_per_rooms_z": -0.5,  # Lower is better
}
