import timeit

def build_shift_table(pattern):
  """Створити таблицю зсувів для алгоритму Боєра-Мура."""
  table = {}
  length = len(pattern)
  # Для кожного символу в підрядку встановлюємо зсув рівний довжині підрядка
  for index, char in enumerate(pattern[:-1]):
    table[char] = length - index - 1
  # Якщо символу немає в таблиці, зсув буде дорівнювати довжині підрядка
  table.setdefault(pattern[-1], length)
  return table

def boyer_moore(text, pattern):
  # Створюємо таблицю зсувів для патерну (підрядка)
  shift_table = build_shift_table(pattern)
  i = 0 # Ініціалізуємо початковий індекс для основного тексту

  # Проходимо по основному тексту, порівнюючи з підрядком
  while i <= len(text) - len(pattern):
    j = len(pattern) - 1 # Починаємо з кінця підрядка

    # Порівнюємо символи від кінця підрядка до його початку
    while j >= 0 and text[i + j] == pattern[j]:
      j -= 1 # Зсуваємось до початку підрядка

    # Якщо весь підрядок збігається, повертаємо його позицію в тексті
    if j < 0:
      return i # Підрядок знайдено

    # Зсуваємо індекс i на основі таблиці зсувів
    # Це дозволяє "перестрибувати" над неспівпадаючими частинами тексту
    i += shift_table.get(text[i + len(pattern) - 1], len(pattern))

  # Якщо підрядок не знайдено, повертаємо -1
  return -1


def compute_lps(pattern):
    lps = [0] * len(pattern)
    length = 0
    i = 1

    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    return lps

def kmp(main_string, pattern):
    M = len(pattern)
    N = len(main_string)

    lps = compute_lps(pattern)

    i = j = 0

    while i < N:
        if pattern[j] == main_string[i]:
            i += 1
            j += 1
        elif j != 0:
            j = lps[j - 1]
        else:
            i += 1

        if j == M:
            return i - j

    return -1  # якщо підрядок не знайдено

def rabin_karp(text, pattern, d=256, q=101):
    n = len(text)
    m = len(pattern)
    h = pow(d, m - 1) % q
    p = 0
    t = 0
    result = []
    for i in range(m):
        p = (d * p + ord(pattern[i])) % q
        t = (d * t + ord(text[i])) % q

    for i in range(n - m + 1):
        if p == t:
            if text[i:i + m] == pattern:
                result.append(i)
        if i < n - m:
            t = (d * (t - ord(text[i]) * h) + ord(text[i + m])) % q
            if t < 0:
                t += q
    return result

def measure_time(func, text, pattern, number=100):
  timer = timeit.Timer(lambda: func(text, pattern))
  time = timer.timeit(number=number)
  return time

# Завантаження текстів
with open("стаття 1.txt", "r", encoding="utf-8") as f:
  text1 = f.read()
with open("стаття 2.txt", "r", encoding="utf-8") as f:
  text2 = f.read()

# Підрядки для пошуку
patterns = {
    "стаття 1": {
        "існуючий": "рекомендаційної системи",
        "вигаданий": "нейронні мережі"
    },
    "стаття 2": {
        "існуючий": "структури даних",
        "вигаданий": "машинне навчання"
    }
}

# Вимірювання часу виконання
results = {}
for text_name, text in [("стаття 1", text1), ("стаття 2", text2)]:
    results[text_name] = {}
    for pattern_type, pattern in patterns[text_name].items():
        results[text_name][pattern_type] = {
            "Боєра-Мура": measure_time(boyer_moore, text, pattern),
            "Кнута-Морріса-Пратта": measure_time(kmp, text, pattern),
            "Рабіна-Карпа": measure_time(rabin_karp, text, pattern)
        }
print(results)
