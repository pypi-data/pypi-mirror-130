import pandas as pd

class Seller:
    def __init__(self, seller):
        self.seller=seller
    #Function returning country with maximum supplied products
    def max_seller(self):
        maximum_quantity=self.seller['Quantity'].max()
        max_country=self.seller.loc[self.seller['Quantity'] == maximum_quantity]
        country_max=max_country['Country']
        print("Maximum Quantities are supplied by: ")
        c_max=pd.DataFrame({'Country':country_max.values})
        return c_max

    #Function returning total quantity by each country
    def total_quant(self):
        quant=self.seller.groupby('Country').Quantity.sum()
        quant_df=pd.DataFrame({'Country':quant.index, 'Total Quantity':quant.values})
        return quant_df


class Graph(Seller):
    def __init__(self,seller):
        Seller.__init__(self,seller)
    # Function showing total price and quantity per country using inheritance from Seller class   
    def analysis(self):
        data=Seller.total_quant(self)
        price=self.seller.groupby('Country').Product_Price.sum()
        price_df=pd.DataFrame({'Country':price.index,'Total Price':price.values})
        
        final=data.merge(price_df, how='inner', on='Country')
        return final
    