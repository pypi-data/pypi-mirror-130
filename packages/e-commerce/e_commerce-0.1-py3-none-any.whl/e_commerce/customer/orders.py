import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# User defined Exceptions
class BrandNameError(Exception):
    pass
class DataFrameError(Exception):
    pass


def total_purchase(data, value):
    dummy = pd.DataFrame()
    dummy = data[data['Email'] == value]
    total = dummy['Price'].sum()
    new = list(data[data['Email'] == value]['Name'].head(1))
    result = pd.DataFrame({"Name": new, "Total_purchasings": total})
    return result

def sale_by_category(data, value):
    try:
        if value in list(data.Product_Category):
            dummy = pd.DataFrame()
            dummy = data[data['Product_Category'] == value]
            total = dummy['Price'].sum()
            return total
        else:
            raise ValueError
    except ValueError:
        print("Error: Invalid category")
    except:
        print("Please enter valid category")

def sale_by_brand(data, value):
    try:
        if value in list(data.Brand_Name):
            dummy = pd.DataFrame()
            dummy = data[data['Brand_Name'] == value]
            total = dummy['Price'].sum()
            return total
        else:
            raise BrandNameError
    except BrandNameError:
        print("BrandNameError: Brand does not exit in data")

def cust_by_city(data):
    try:
        if 'Address' in data.columns:
            city_count = data.groupby('Address')['Email'].nunique()
            new_df = pd.DataFrame({'City': city_count.index, 'Number_of_Customers': city_count.values})
            return new_df
        else:
            raise DataFrameError
    except DataFrameError:
        print("DataFrameError: Data in not appropriate for this function.")
    except:
        print("Error")