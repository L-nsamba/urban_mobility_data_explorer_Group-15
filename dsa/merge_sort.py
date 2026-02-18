"""
merge_sort.py

Time Complexity: O(n log n)
Space Complexity: O(n)
Stable yes
Sorting Order: Descending by default
"""

from typing import List, Dict, Any
from flask import Blueprint, jsonify
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

# Merge sort implementation
def merge_sort(arr: List[Dict[str, Any]], key: str, descending: bool = True) -> List[Dict[str, Any]]:
    """
    Sorts a list of dictionaries based on a specified key using the merge sort.

    parameters:
    arr (List[Dict[str, Any]]): The list of dictionaries to be sorted.
    key (str): The key in the dictionary to sort by.
    descending (bool): Whether to sort in descending order. Default is True.

    Returns:
    List[Dict[str, Any]]: The sorted list of dictionaries.
    """

    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2

    left_half = merge_sort(arr[:mid], key, descending)
    right_half = merge_sort(arr[mid:], key, descending)

    return merge(left_half, right_half, key, descending)

def merge(left: List[Dict[str, Any]], right: List[Dict[str, Any]], key: str, descending: bool) -> List[Dict[str, Any]]:
    """
    Merges two sorted lists of dictionaries into a single sorted list.
    parameters:
    left (List[Dict[str, Any]]): The left sorted sublist.
    right (List[Dict[str, Any]]): The right sorted sublist.
    key: str -key to sort by
    descending: bool - whether to sort in descending order

    Returns:
    List[Dict[str, Any]]: merged sorted list
    
    """

    result = []
    left_index = 0
    right_index = 0

    while left_index < len(left) and right_index < len(right):
        # Handle missing keys
        left_val = left[left_index].get(key, None)
        right_val = right[right_index].get(key, None)

        try:
            if (left_val >= right_val and descending) or (left_val <= right_val and not descending):
                result.append(left[left_index])
                left_index += 1
            else:
                result.append(right[right_index])
                right_index += 1
        except TypeError:
            # If values are not comparable, treat them as equal
            result.append(left[left_index])
            left_index += 1

    result.extend(left[left_index:])
    result.extend(right[right_index:])

    return result

# Flask Endpoint

load_dotenv()

engine = create_engine(
    f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}",
    connect_args={"ssl": {"ssl_ca": os.getenv('DB_CA')}}
)

top5_blueprint = Blueprint('top5', __name__)

@top5_blueprint.route("/top5_busiest_boroughs", methods=["GET"])
def top5_busiest_boroughs() -> Any:
    """
    Results the top 5 busiest boroughs based on total distance traveled.

    steps:
    1. Aggregate total distance per borough from the trips table.
    2. Convert the result to a list of dictionaries.
    3. Sort the list using merge sort in descending order.
    4. Return the top 5 results as JSON.

    Returns:
        JSON response with keys:
            - 'borough': str
            - 'total_distance': float

    """

    query = text("""
        SELECT z.borough AS borough, ROUND(SUM(t.trip_distance), 2) AS total_distance
        FROM trips t
        JOIN zones z ON t.PULocationID = z.LocationID
        GROUP BY z.borough
    """)

    with engine.connect() as conn:
        result = conn.execute(query)
        
        borough_totals: List[Dict[str, Any]] = [
            {"borough": row.borough, "total_distance": float(row.total_distance)} for row in result
        ]
    
    sorted_boroughs = merge_sort(
        borough_totals,
        key="total_distance",
        descending=True
    )

    #Take top 5
    top5 = sorted_boroughs[:5]

    return jsonify({"top_5_busiest_boroughs": top5})

if __name__ == "__main__":
    sample_data = [
        {"borough": "Manhattan", "total_distance": 500000},
        {"borough": "Brooklyn", "total_distance": 300000},
        {"borough": "Queens", "total_distance": 225000},
        {"borough": "Bronx", "total_distance": 20000},
        {"borough": "Staten Island", "total_distance": 10000}
    ]

    print("Top 5 boroughs sorted by total_distance(descending):")
    print(merge_sort(sample_data, key="total_distance", descending=True))
