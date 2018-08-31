import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--actual', '-a', default = './input/actual.txt')
parser.add_argument('--predicted', '-p', default = './input/predicted.txt')
parser.add_argument('--window', '-w', default = './input/window.txt')
parser.add_argument('--output', '-o',  default = './output/comparison.txt')
args = parser.parse_args()

actual_file = args.actual
predicted_file = args.predicted
window_file = args.window
output_file = args.output

# Define the window variable based on value contained in window_file
with open(window_file, 'r') as f:
    window = int(f.read())

def make_price_dictionary(price_input_file):
    """
    Make a nested dictionary from an input file which is arranged as the following:
    hour|stock|price
    The first level of the dictionary will contain the hour as the key
    The second level of the dictionary will contain the stock as the key and the price as the value
    """
    price_dict = {}
    with open(price_input_file, 'r') as f:
        for line in f:
            line = line.strip('\n')
            (time, stock, price) = line.split('|')
            time = int(time)
            price = float(price)
            if time in price_dict.keys():
                price_dict[time][stock] = price
            else:
                price_dict[time] = {stock: price}
    return price_dict

def compare_stock_prices(actual, predicted):
    """
    Compares the prices between two nested dictionaries created by the make_price_dictionary funciton
    """
    comparison = {}
    for hour in actual:
        stocks_actual = actual[hour]
        stocks_predicted = predicted[hour]
        comparison[hour] = {x: abs(stocks_actual[x] - stocks_predicted[x]) for x in stocks_actual if x in stocks_predicted}
    return comparison

def calculate_sum_and_length_by_hour(list_of_dictionaries):
    """
    Calculates the sum and length of the prices for each hour
    """
    calculations = {}
    for hour in list_of_dictionaries:
        sumation = abs(sum(list_of_dictionaries[hour].values()))
        length = len(list_of_dictionaries[hour])
        calculations[hour] = [sumation, length]
    return calculations

def calculate_average_error(err_calc, window):
    """
    Calculate the average error of the predicted prices via rolling window
    """
    ave_err = []
    max_hour = max(err_calc)
    beginning_hour = 1
    while (beginning_hour + window - 1) <= max_hour:
        hour_range = range(beginning_hour, (beginning_hour + window))
        sumation = 0
        length = 0
        for hour in hour_range:
            sumation += err_calc[hour][0]
            length += err_calc[hour][1]
        precise_err = sumation/length
        err = "%.2f" % precise_err
        ave_err.append(str(beginning_hour)+'|'+str(beginning_hour+window-1)+'|'+err+'\n')
        beginning_hour += 1
    return ave_err

def write_to_output(average_error):
    """
    Write computed errors of the predicted stock prices to the output file in the format:
    Beginning_Hour|Beginning_Hour+Window|Error
    """
    with open(output_file, 'w') as f:
        for row in average_error:
            f.write(row)

actual_prices = make_price_dictionary(actual_file)
predicted_prices = make_price_dictionary(predicted_file)
price_diff = compare_stock_prices(actual_prices, predicted_prices)
error_calculations = calculate_sum_and_length_by_hour(price_diff)
average_error = calculate_average_error(error_calculations, window)
write_to_output(average_error)