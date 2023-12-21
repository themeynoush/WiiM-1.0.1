import json
import requests
from dotenv import load_dotenv
import os
from typing import List, Optional, Literal
from pydantic import BaseModel, Field, constr, conlist


load_dotenv()


class CustomLocationBoundary(BaseModel):
    # Add the fields for the custom location boundary object.
    # Example (this needs to be tailored to match the specific requirements):
    # coordinates: List[List[float]]  # Define coordinates for a polygon
    # For a circle (you might define them like this)
    # center: List[float]  # Center of the circle [latitude, longitude]
    # radius: float         # Radius in meters
    pass  # Replace with actual fields


class PropertyCharacteristics(BaseModel):
    # Define the characteristics data model here
    pass  # Replace with actual fields.


class SearchParameters(BaseModel):
    search_operations: List[
        Literal["sale", "sold", "sale_hold", "rent", "rented", "rent_hold"]
    ]
    city: Optional[str] = Field(default=None)
    zip_code: Optional[int] = Field(default=None, ge=1)
    conditions: Optional[
        List[Literal["used", "ruin", "very-good", "new", "other"]]
    ] = Field(default=None)
    property_date_from: Optional[str] = Field(
        default=None, pattern=r"^\d{4}-\d{2}-\d{2}$"
    )
    property_date_to: Optional[str] = Field(
        default=None, pattern=r"^\d{4}-\d{2}-\d{2}$"
    )
    created_date_from: Optional[str] = Field(
        default=None, pattern=r"^\d{4}-\d{2}-\d{2}$"
    )
    created_date_to: Optional[str] = Field(default=None, pattern=r"^\d{4}-\d{2}-\d{2}$")
    updated_date_from: Optional[str] = Field(
        default=None, pattern=r"^\d{4}-\d{2}-\d{2}$"
    )
    updated_date_to: Optional[str] = Field(default=None, pattern=r"^\d{4}-\d{2}-\d{2}$")

    price_from: Optional[int] = Field(default=None, ge=1)
    price_to: Optional[int] = Field(default=None, ge=1)

    price_per_sqm_from: Optional[int] = Field(default=None, ge=1)
    price_per_sqm_to: Optional[int] = Field(default=None, ge=1)

    bedrooms_from: Optional[int] = Field(default=None, ge=0)
    bedrooms_to: Optional[int] = Field(default=None, ge=0)

    bathrooms_from: Optional[int] = Field(default=None, ge=1)
    bathrooms_to: Optional[int] = Field(default=None, ge=1)

    total_area_from: Optional[int] = Field(default=None, ge=1)
    total_area_to: Optional[int] = Field(default=None, ge=1)

    plot_area_from: Optional[int] = Field(default=None, ge=1)
    plot_area_to: Optional[int] = Field(default=None, ge=1)

    construction_year_from: Optional[int] = Field(default=None, ge=1)
    construction_year_to: Optional[int] = Field(default=None, ge=1)

    floor: Optional[Literal["no_floor", "ground", "middle", "top"]] = Field(
        default=None, deprecated=True
    )
    floors: Optional[List[Literal["no_floor", "ground", "middle", "top"]]] = Field(
        default=None
    )

    orientation: Optional[Literal["exterior", "interior"]] = Field(default=None)

    view: Optional[Literal["water", "landscape", "city", "golf", "park"]] = Field(
        default=None, deprecated=True
    )
    views: Optional[
        List[Literal["water", "landscape", "city", "golf", "park"]]
    ] = Field(default=None)

    direction: Optional[Literal["north", "south", "east", "west"]] = Field(
        default=None, deprecated=True
    )
    directions: Optional[List[Literal["north", "south", "east", "west"]]] = Field(
        default=None
    )

    types: Optional[
        List[
            Literal[
                "apartment",
                "studio",
                "duplex",
                "penthouse",
                "country_house",
                "house",
                "palace",
                "townhouse",
                "villa",
                "country_estate",
                "chalet",
                "bungalow",
                "retail",
                "office",
                "industrial",
                "warehouse",
                "hotel",
                "other_commercial",
                "plot",
                "room",
                "parking",
                "garage",
                "other",
                "apartment_building",
                "office_building",
                "mix_use_building",
            ]
        ]
    ] = Field(default=None)

    property_types: Optional[
        List[
            Literal[
                "apartment",
                "studio",
                "duplex",
                "penthouse",
                "country_house",
                "house",
                "palace",
                "townhouse",
                "villa",
                "country_estate",
                "chalet",
                "bungalow",
                "retail",
                "office",
                "industrial",
                "warehouse",
                "hotel",
                "other_commercial",
                "plot",
                "room",
                "parking",
                "garage",
                "other",
                "apartment_building",
                "office_building",
                "mix_use_building",
            ]
        ]
    ] = Field(default=None, deprecated=True)

    private: Optional[bool] = Field(default=None)

    auction: Optional[bool] = Field(default=None)

    bank: Optional[bool] = Field(default=None)

    listing_agents: Optional[List[str]] = Field(default=None)

    with_agencies: Optional[List[str]] = Field(default=None)

    without_agencies: Optional[List[str]] = Field(default=None)

    exclusive: Optional[bool] = Field(default=None)

    ref_numbers: Optional[List[str]] = Field(default=None)

    energy_certificate: Optional[
        Literal["Unknown", "A+", "A", "B", "C", "D", "E", "F", "G", "H"]
    ] = Field(default=None, deprecated=True)

    energy_certificates: Optional[
        List[Literal["Unknown", "A+", "A", "B", "C", "D", "E", "F", "G", "H"]]
    ] = Field(default=None)


CASAFARI_API_BASE_URL = "https://api.casafari.com"
CASAFARI_API_TOKEN = os.getenv("CASAFARI_API_TOKEN")


def fetch_location_ids_from_name_and_zip_code(name, zip_code):
    json_payload = {"name": name}
    if zip_code:
        json_payload["zip_codes"] = [zip_code]

    response = requests.post(
        url=f"{CASAFARI_API_BASE_URL}/v1/references/locations",
        json=json_payload,
        headers={"Authorization": f"Token {CASAFARI_API_TOKEN}"},
    )

    locations = response.json()["locations"]
    location_ids = [location["location_id"] for location in locations]
    print(location_ids)

    return location_ids


def fetch_location_ids_from_name(name):
    response = requests.post(
        url=f"{CASAFARI_API_BASE_URL}/v1/references/locations",
        json={"name": name},
        headers={"Authorization": f"Token {CASAFARI_API_TOKEN}"},
    )

    locations = response.json()["locations"]
    location_ids = [location["location_id"] for location in locations]
    

    return location_ids


def fetch_properties(parameters: SearchParameters):
    location_ids = fetch_location_ids_from_name_and_zip_code(parameters.city, parameters.zip_code)
    # location_ids = fetch_location_ids_from_name(parameters.city)
    data = parameters.model_dump(exclude_none=True)
    data["location_ids"] = location_ids
    print(data)

    def fetch(limit, offset):
        response = requests.post(
            url=f"{CASAFARI_API_BASE_URL}/v1/properties/search",
            params={
                "limit": limit,
                "offset": offset,
                "order_by": "last_update",
                "order": "desc",
            },
            json=data,
            headers={"Authorization": f"Token {CASAFARI_API_TOKEN}"},
        )

        return response.json()

    # fetch n properties, the max limit is 100
    def fetch_n(n):
        results = []
        max_limit = 100  # Max limit per request
        total_fetched = 0

        while total_fetched < n:
            batch_size = min(max_limit, n - total_fetched)
            offset = total_fetched
            response_data = fetch(limit=batch_size, offset=offset)

            if "results" not in response_data:
                # Handle error (response without 'results')
                break

            results.extend(response_data["results"])
            total_fetched += len(response_data["results"])

            # If the last request returned fewer properties than asked, we reached the end
            if len(response_data["results"]) < batch_size:
                break

        return results

    return fetch_n(100)


# if __name__ == "__main__":
#     name = "Nice"
#     price_from = 100_000
#     price_to = 200_000

#     parameters = SearchParameters(
#         search_operations=["sale"],
#         city=name,
#         price_from=price_from,
#         price_to=price_to,
#     )

#     properties = fetch_properties(parameters)
#     print(properties)

if __name__ == "__main__":
    name = "Toulouse"
    price_from = 700_000
    plot_area_from = 2000
    total_area_from = 200

    parameters = SearchParameters(
        search_operations=["sale"],
        city="Toulouse",
        zip_code=31_000,
        price_from=700_000,
        plot_area_from=2000,
        total_area_from=200,
        # created_date_from="2023-06-01",
    )
    # parameters = SearchParameters(
    #     search_operations=["sale"],
    #     city=name,
    #     zip_code=31_000,
    #     price_from=price_from,
    #     plot_area_from=plot_area_from,
    #     total_area_from=total_area_from,
    # )

    properties = fetch_properties(parameters)
    with open("properties.json", "w") as f:
        json.dump(properties, f)
    # print(properties)
