def binary_search(arr, x):
    low = 0
    high = len(arr) - 1
    count = 0
    upper_bound = None
    while low <= high:
        count += 1
        mid = (low + high) // 2
        if arr[mid] == x:
            return (count, arr[mid])
        elif arr[mid] < x:
            low = mid + 1
        else:
            high = mid - 1
            upper_bound = arr[mid]
    if upper_bound is None:
        return (count, None)
    else:
        return (count, upper_bound)

# Тестуємо функцію
arr = [1.2, 2.3, 3.4, 4.5, 5.6, 6.7, 7.8, 8.9]

# Тест 1
x = 5.6
result = binary_search(arr, x)
print(f"Для x = {x}: {result}")  # Виведе: Для x = 5.6: (3, 5.6)

# Тест 2
x = 5.0
result = binary_search(arr, x)
print(f"Для x = {x}: {result}")  # Виведе: Для x = 5.0: (3, 5.6)

# Тест 3
x = 9.0
result = binary_search(arr, x)
print(f"Для x = {x}: {result}")  # Виведе: Для x = 9.0: (4, None)