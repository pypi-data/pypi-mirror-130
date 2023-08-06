#This module is basically for the graphical representation of the data 
import matplotlib.pyplot as plt


class QuantityInvalid(Exception):
  
   pass

class priceInvalid(Exception):
  
   pass

#Bar graph displaying quantity with respect to the product category
def showQuantity(seller):
    
    try:
        if 'Quantity' in seller.columns:
            quantity=seller['Quantity']
            category=seller['Product_Category']
    
            fig = plt.figure()
            plt.bar(category,quantity)
    
            plt.title('Quantities in each category')
            plt.xlabel('Category')
            plt.ylabel('Quantity')
            plt.show()
            return category

        else:
            raise QuantityInvalid
    except QuantityInvalid:
        print("QuantityInvalid: Invalid Quantity column")

    
    
    
    
    
#Bar graph displaying price with respect to the product 
def showPrice(seller):
    
    try:
        if 'Product_Price' in seller.columns:
            price=seller['Product_Price']
            p_name=seller['Product_Name']
    
            fig = plt.figure()
            plt.bar(p_name,price, color=['orange','green','red','blue'])
    
    
            plt.title('Prices of the Products')
            plt.xlabel('Products')
            plt.ylabel('Price')
            plt.show()
            return price

        else:
            raise priceInvalid
    except priceInvalid:
        print("priceInvalid: Invalid Price column")
    
    
    
    
    
    
#Scatter plot displaying product category with respect to the company name
def showCategory(seller):
    category=seller['Product_Category']
    name=seller['Name']
    
    fig = plt.figure()
    plt.scatter(name,category)
    
    
    plt.title('Different company category')
    plt.xlabel('Company name')
    plt.ylabel('Category')
    plt.show()
    return name