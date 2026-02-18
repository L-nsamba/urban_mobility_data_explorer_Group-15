"""
merge_sort.py

Time Complexity: O(n log n)
Space Complexity: O(n)
Sorting Order: Descending by default
"""

from typing import List, Dict, Any

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

if __name__ == "__main__":
    # Actual values from the dataset manually hardcoded
    distance_per_day_borough = [
        {"borough": "null", "date": "2019-01-01","total_distance": 255.34},
        {"borough": "Bronx", "date": "2019-01-01","total_distance": 255.34},
        {"borough": "Brooklyn", "date": "2019-01-01","total_distance": 19059.11},
        {"borough": "EWR", "date": "2019-01-01","total_distance": 41.28},
        {"borough": "Manhattan", "date": "2019-01-01","total_distance": 441704.33},
        {"borough": "Queens", "date": "2019-01-01","total_distance": 183997.31},
        {"borough": "Staten Island", "date": "2019-01-01","total_distance":  166.69},
        {"borough": "Unknown", "date": "2019-01-01","total_distance": 8908.72}
    ]

    print("Top 5 boroughs sorted by total_distance(descending):")
    print(merge_sort(distance_per_day_borough, key="total_distance", descending=True))
