import csv


def to_int_or_float(string):
    try:
        number = float(string)
        if number.is_integer():
            return int(number)
        return number
    except ValueError:
        return None


def normalize():
    lines = open('apartmentComplexData.txt').read().splitlines()
    with open('normalized.csv', 'w', newline='') as file:
        writer = csv.writer(file)

        for line in lines:
            split = line.split(',')
            writer.writerow([to_int_or_float(split[2]), to_int_or_float(split[3]), to_int_or_float(split[4]),
                             to_int_or_float(split[5]), to_int_or_float(split[6]), to_int_or_float(split[8])])
