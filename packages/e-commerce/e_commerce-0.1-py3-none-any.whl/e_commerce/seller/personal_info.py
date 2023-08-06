#get information of seller using name
def getName(seller,name):
    try:
        if isinstance(name, str):
            return seller.loc[seller['Name'] == name]
        else: 
            raise TypeError
    except TypeError:
        print("Error: Enter name in string!")
    except:
        print("Error: Enter name in string!")
    finally:
        print("Function end!!")
        

#get information of seller using email
def getEmail(seller,email):
    try:
        if "@" in email:
            return seller.loc[seller['Email'] == email]
        else:
            raise ValueError
    except ValueError as ex:
        print("Error: Invalid email address!")
    except:
        print("Error: Invalid email address!")
    finally:
        print("Function end!!")

#get information of seller using product category
def getCategory(seller,category):
    try:
        
        if isinstance(category, str):
            
            return seller.loc[seller['Product_Category'] == category]
        else: 
            
            raise TypeError
    except TypeError:
        print("Error: category should be valid!")
    except:
        
        print("Error: category should be valid!")
    finally:
        
        print("Function end!!")
    

#get information of seller using country
def getCountry(seller,country):
    
    try:
        if isinstance(country, str):
            return seller.loc[seller['Country'] == country]
        else: 

            raise TypeError
   
    except TypeError:
        print("Error: Invalid country name!")
    except:
        
        print("Error: Invalid country name!")
    finally:
        
        print("Function end!!")
    
    