

from db_access import store_data, get_data

if __name__ == "__main__":
    key = "1"
    value = "Piyush Kuhikar"

    store_data(key, value)
    retrieved_value = get_data(key)
    print(f"Retrieved value: {retrieved_value}")
