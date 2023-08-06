def get_by_email(data, value):
    try:
        if "@" in value:
            return data.loc[data['Email'] == value]
        else:
            raise ValueError
    except ValueError:
        print("Error: Invalid email address!")
    except:
        print("Error: Invalid email address!")

def get_by_address(data, value):
    try:
        if isinstance(value, str):
            return data.loc[data['Address'] == value]
        else:
            raise TypeError
    except TypeError:
        print("Error: Input is not a string!")
    except:
        print("Error: City name is invalid")
    finally:
        print("Function end!")
        
def get_by_Product_Category(data, value):
    try:
        if isinstance(value, str):
            return data.loc[data['Product_Category'] == value]
        else:
            raise TypeError
    except TypeError:
        print("Error: Invalid category name!")
    except:
        print("Error: Invalid category name!")
    finally:
        print("Function end!")