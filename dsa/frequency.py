# Hardcoding the actual trips and corresponding hours obtained from curling get_trips_per_hour
trips_per_hour_data = [
    {"hour": 0 , "total_trips": 67441},
    {"hour": 1 , "total_trips": 51736},
    {"hour": 2 , "total_trips": 38159},
    {"hour": 3 , "total_trips": 27615},
    {"hour": 4 , "total_trips": 21139},
    {"hour": 5 , "total_trips": 25977},
    {"hour": 6 , "total_trips": 59238},
    {"hour": 7 , "total_trips": 98276},
    {"hour": 8 , "total_trips": 120452},
    {"hour": 9 , "total_trips": 118696},
    {"hour": 10 , "total_trips": 117534},
    {"hour": 11 , "total_trips": 122747},
    {"hour": 12 , "total_trips": 131422},
    {"hour": 13 , "total_trips": 132953},
    {"hour": 14 , "total_trips": 142505},
    {"hour": 15 , "total_trips": 149747},
    {"hour": 16 , "total_trips": 138352},
    {"hour": 17 , "total_trips": 153606},
    {"hour": 18 , "total_trips": 167358},
    {"hour": 19 , "total_trips": 153991},
    {"hour": 20 , "total_trips": 136558},
    {"hour": 21 , "total_trips": 131037},
    {"hour": 22 , "total_trips": 115397},
    {"hour": 23 , "total_trips": 78064}
]

# This function will analyze the top 5 rush hours
def get_top_rush_hours(data, top_n=5):

    trips_copy = data.copy()
    top_hours = []

    """

    Pseudo Code:
        function get_top_rush_hours(data, top_n):
            trips_copy = copy of data
            top_hour = empty list

            for i = 1 to top_n:
                max_idx = 0
                for j = 1 to length(trips_copy)-1:
                    if trips_copy[j].total_trips > trips_copy[max_idx].total_trips:
                        max_idx = j --> Manually finding the maximum element on each iteration
                
                append trips_copy[max_idx] to top_hours
                remove trips_copy[max_idx] from trips_copy --> Adjusting top_n times on each iteration,
                                                               if the latest value is larger than previous, it becomes
                                                               the new max and climbs up in the top_n times ranking
                                            
            return top_hours


    Time complexity analysis:

    n --> list size
    k --> top elements
    1. Outer loop: runs top_n times which indicates linear time complexity O(k)
    2. Inner loop:  Scans remaining items to find the max also exhibiting linear time complexity O(n)
    3. Removing elements from the list with pop: Also displays linear time complexity O(n)
    4. Worst Case Scenario: Linear time complexity --> o(k *n) // Maximum possible work done
    5. Conclusion: Linear time complexity displays worst case scenario since every element is scanned on each loop iteration

    
    """

    for _ in range(top_n):
        # Locating the index for max total_trips
        max_idx = 0
        for i in range(1, len(trips_copy)):
            if trips_copy[i]["total_trips"] > trips_copy[max_idx]["total_trips"]:
                max_idx = i
        # Pop adds the max elements to the top_hours list
        top_hours.append(trips_copy.pop(max_idx))

    return top_hours

if __name__ == "__main__":
    top_5_hours = get_top_rush_hours(trips_per_hour_data, top_n=5)

    print("Top 5 rush hours (with DSA integration):") 
    for h in top_5_hours:
        print(f"Hour {h['hour']}: {h['total_trips']} trips")  