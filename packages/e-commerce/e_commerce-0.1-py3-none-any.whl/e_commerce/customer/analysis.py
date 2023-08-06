import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from .orders import sale_by_category

def category_analysis(data, c_list):
    n = len(c_list)
    total = [None]*n
    for i in range(n):
        total[i] = sale_by_category(data, c_list[i])
    fig = plt.figure()
    plt.bar(np.array(c_list), np.array(total), color = 'red')
    plt.title("Total sale of different categories")
    plt.xlabel("Category")
    plt.ylabel("Total sale ($)")
    plt.show()
    return (np.array(c_list), np.array(total))

def brand_analysis(data):
    dummy = data.groupby('Brand_Name').Price.sum()
    new_df = pd.DataFrame({'Brand_Name': dummy.index, 'Total_sales': dummy.values})
    fig = plt.figure()
    plt.bar(new_df["Brand_Name"], new_df["Total_sales"], color = 'green')
    plt.title("Total sale of different Brands")
    plt.xlabel("Barnd Name")
    plt.ylabel("Total sale ($)")
    plt.show()
    return (new_df["Brand_Name"], new_df["Total_sales"])

class rank_cal:
    def __init__(self, data):
        self.data = data
    def avg_rating(self, value):
        rating = self.data[self.data['Brand_Name'] == value][['Rating']].mean()
        return rating[0]

class rank_analysis(rank_cal):
    def __init__(self, data):
        rank_cal.__init__(self, data)
    def ranking(self):
        brands = self.data['Brand_Name'].unique()
        n = len(brands)
        rank = [None]*n
        for i in range(n):
            rank[i] = rank_cal.avg_rating(self, brands[i])
        fig = plt.figure()
        plt.bar(brands, rank)
        plt.title("Ranking of Brands")
        plt.xlabel("Barnd Name")
        plt.ylabel("Rank")
        plt.show()
        return (brands, rank)
        
        