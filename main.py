import pandas as pd
import matplotlib.pyplot as plt

# Veri setini okumak için bir fonksiyon.
def read_data_set(file_name):
    columns = {}

    with open(file_name, 'r') as file:
        for line in file:
            data = list(map(float, line.strip().split(',')))
            for i, value in enumerate(data):
                if i not in columns:
                    columns[i] = []
                columns[i].append(float(value))

    return columns

# Dosyayı okur ve sütunları ayırır
file_name = "Veri_Seti.txt"
columns = read_data_set(file_name)

# Her bir sütunu ekrana yazdır.
for column_number, column_data in columns.items():
    print(f"Column {column_number + 1}:", column_data)
    print("\n")

# Pandas kütüphanesi ile veri setini yükler
data_set = pd.read_csv("Veri_Seti.txt", header=None)

# Her bir sutun icin kutu cizimi yapar
for column in data_set.columns:
    plt.figure(figsize=(6, 4))
    plt.boxplot(data_set[column])
    plt.title(f"Sütun {column + 1} Kutu Cizimi")
    plt.xlabel("Sütun Degerleri")
    plt.ylabel("Degerler")
    plt.show()

# Veri setinin uzunluğunu hesaplayan fonksiyon
def calculate_length(series):
    length = 0
    for _ in series:
        length += 1
    return length

# Aykırı değerleri tespit eden fonksiyon
def find_outliers(series):
    # Veri setinin uzunluğunu hesaplar
    length = calculate_length(series)

    # Veriyi sırala
    sorted_series = []
    for value in series:
        # Sıralı bir şekilde eklemek için uygun konumu bulur
        inserted = False
        for i in range(len(sorted_series)):
            if value < sorted_series[i]:
                sorted_series.insert(i, value)
                inserted = True
                break
        if not inserted:
            sorted_series.append(value)

    # Çeyrekler aralığını IQR hesaplar
    q1_index = length // 4
    q3_index = 3 * length // 4
    q1 = sorted_series[q1_index]
    q3 = sorted_series[q3_index]
    iqr = q3 - q1

    # Alt ve üst sınırları belirler
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    outliers = []
    # Aykırı değerleri tespit eder
    for value in series:
        if value < lower_bound or value > upper_bound:
            outliers.append(value)

    return outliers

# aykırı değerleri depolamak için bir sözlük
outliers = {}

# Her bir sütun için aykırı değerleri bulur
for column in data_set.columns:
    outliers[column] = find_outliers(data_set[column])

# Her bir sütun için aykırı değerleri yazdır.
for column, outlier in outliers.items():
    print(f"Aykırı Değerler for Column {column + 1}:\n{outlier}\n")

# sütunlardaki aykırı değerleri kaldırır
for column, outlier_values in outliers.items():
    for value in outlier_values:
        data_set = data_set[data_set[column] != value]

# aykırı değerleri çıkardıktan sonra sütunların kutu grafiği çizer
for column in data_set.columns:
    plt.figure(figsize=(6, 4))
    plt.boxplot(data_set[column])
    plt.title(f" Aykiri Sütun {column + 1} Kutu Cizimi")
    plt.xlabel("Sütun Degerleri")
    plt.ylabel("Degerler")
    plt.show()

# merkezi eğilim ölçüleri

# Serinin aritmetik ortalamasını hesaplar.
def calculate_mean(series):
    total = 0
    count = 0

    # Serideki tüm değerleri toplar ve sayar
    for value in series:
        total += value
        count += 1

    # Toplamı eleman sayısına bölerek ortalama değeri hesaplar
    mean = total / count
    return mean

# Serinin medyanını hesaplar.
def calculate_median(series):
    # Dizi uzunluğunu hesaplar
    length = 0
    for _ in series:
        length += 1

    # Diziyi sıralar
    for i in range(length):
        for j in range(0, length - i - 1):
            if series[j] > series[j + 1]:
                series[j], series[j + 1] = series[j + 1], series[j]

    # Medyanı hesaplar
    if length % 2 != 0:
        median = series[length // 2]
    else:
        median = (series[length // 2 - 1] + series[length // 2]) / 2
    return median

# Serinin modunu hesaplar.
def calculate_mode(series):
    max_count = 0
    mode = None

    for value in series:
        count = 0
        for other_value in series:
            if other_value == value:
                count += 1
        if count > max_count:
            max_count = count
            mode = value

    return mode

# merkezi dağılım ölçüleri
# Serinin değişim aralığını hesaplar hesaplar
def calculate_range(series):
    max_value = series[0]
    min_value = series[0]

    for value in series:
        if value > max_value:
            max_value = value
        if value < min_value:
            min_value = value

    range_value = max_value - min_value
    return range_value

# Serinin ortalama mutlak sapmasını hesaplar
def calculate_mean_absolute_deviation(series):
    total = 0
    count = 0

    # Toplamı ve eleman sayısını hesaplar
    for value in series:
        total += value
        count += 1

    # Ortalama değeri hesaplar
    mean = total / count

    deviation_sum = 0

    # Mutlak sapmaların toplamını hesaplar
    for value in series:
        deviation_sum += (value - mean) if value >= mean else (mean - value)

    # Ortalama mutlak sapmayı hesaplar
    mean_absolute_deviation = deviation_sum / count
    return mean_absolute_deviation


# Serinin varyansını hesaplar
def calculate_variance(series):
    total = 0
    count = 0

    # Toplamı ve eleman sayısını hesaplar
    for value in series:
        total += value
        count += 1

    # Ortalama değeri hesaplar
    mean = total / count

    # Karelerin toplamını hesaplar
    squared_sum = 0
    for value in series:
        squared_sum += (value - mean) ** 2

    # Varyansı hesaplar
    variance = squared_sum / count
    return variance

# Serinin standart sapmasını hesaplar
def calculate_standard_deviation(series):
    total = 0
    count = 0

    # Toplamı ve eleman sayısını hesaplar
    for value in series:
        total += value
        count += 1

    # Ortalama değeri hesaplar
    mean = total / count

    # Karelerin toplamını hesaplar
    squared_sum = 0
    for value in series:
        squared_sum += (value - mean) ** 2

    # Varyansı hesaplar
    variance = squared_sum / count

    # Standart sapmayı hesaplar
    standard_deviation = variance ** 0.5
    return standard_deviation

# Serinin değişim katsayısını hesaplar.
def calculate_coefficient_of_variation(series):
    total = 0
    count = 0

    # Toplamı ve eleman sayısını hesaplar
    for value in series:
        total += value
        count += 1

    # Ortalama değeri hesaplar
    mean = total / count

    # Karelerin toplamını hesaplar
    squared_sum = 0
    for value in series:
        squared_sum += (value - mean) ** 2

    # Varyansı hesaplar
    variance = squared_sum / count

    # Standart sapmayı hesaplar
    standard_deviation = (variance ** 0.5)

    # Değişim katsayısını hesaplar
    coefficient_of_variation = (standard_deviation / mean) * 100
    return coefficient_of_variation

# Serinin çeyrekler arası açıklığını hesaplar
def calculate_interquartile_range(series):
    # Veri setini sıralar
    series_sorted = sorted(series)

    # Veri setinin uzunluğunu hesaplar
    n = len(series_sorted)

    # Q1 ve Q3 indislerini belirler
    q1_index = n // 4
    q3_index = 3 * n // 4

    # Q1 ve Q3 değerlerini bulur
    q1 = series_sorted[q1_index]
    q3 = series_sorted[q3_index]

    # Çeyrekler arası açıklığı hesaplar
    interquartile_range = q3 - q1
    return interquartile_range

# Sonuçları saklamak için bir sözlük oluşturur
results = {}

# Her bir sütun için ölçümleri hesaplar
for column_number, column_data in columns.items():
    results[f"Column {column_number + 1}"] = {}
    results[f"Column {column_number + 1}"]["Ortalama"] = calculate_mean(column_data)
    results[f"Column {column_number + 1}"]["Medyan"] = calculate_median(column_data)
    results[f"Column {column_number + 1}"]["Mod"] = calculate_mode(column_data)
    results[f"Column {column_number + 1}"]["Değişim Aralığı"] = calculate_range(column_data)
    results[f"Column {column_number + 1}"]["Ortalama Mutlak Sapma"] = calculate_mean_absolute_deviation(column_data)
    results[f"Column {column_number + 1}"]["Varyans"] = calculate_variance(column_data)
    results[f"Column {column_number + 1}"]["Standart Sapma"] = calculate_standard_deviation(column_data)
    results[f"Column {column_number + 1}"]["Değişim Katsayısı"] = calculate_coefficient_of_variation(column_data)
    results[f"Column {column_number + 1}"]["Çeyrekler Arası Açıklık"] = calculate_interquartile_range(column_data)

# Sonuçları ekranda gösterir
for column, measurements in results.items():
    print(column)
    for measurement, value in measurements.items():
        print(f"{measurement}: {value}")
    print()

# Sonuçları dosyaya yazdırır
with open("sonuc.txt", "w") as file:
    for column, measurements in results.items():
        file.write(column + ":\n")
        for measurement, value in measurements.items():
            file.write(f"{measurement}: {value}\n")
        file.write("\n")