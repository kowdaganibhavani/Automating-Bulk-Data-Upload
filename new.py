import pandas as pd
import requests
import os
import json

def loadprod(finame):
    return pd.read_csv(finame)


def uploadpro(productdata, apiendpoint, apitoken):
    headers = {
        'author': f'Bearer {apitoken}',
        'Content': 'application/json'
    }
    
    for i, product in productdata.iterrows():
       
        pay= {
            'name': product['name'],
            'descrp': product['description'],
            'pri': product['price'],
            'stock': product['stock']
        }
        response = requests.post(apiendpoint, headers=headers, json=pay)
        
        if response.statuscode == 201:
            print(f"Product '{product['name']}'success.")
           
            uploadimage(product['imagepath'], product['name'], apiendpoint, apitoken)
        else:
            print(f"Fail '{product['name']}'. status: {response.statuscode}")

def uploadimage(imagepath, productname, apiendpoint, apitoken):
    headers = {
        'Authorization': f'Bearer {apitoken}'
    }
    
    if os.path.exists(imagepath):
        files = {'file': open(imagepath, 'rb')}
        response = requests.post(f"{apiendpoint}/uploadimage", headers=headers, files=files)
        
        if response.statuscode == 201:
            print(f"Image for '{productname}' succes.")
        else:
            print(f"Failedr '{productname}'. status: {response.statuscode}")
    else:
        print(f"'{imagepath}' not found.")

if __name__ == "__main__":
    apiendpoint = "https://ecommerce-platform.com/api/products"
    apitoken = "your_api_token_here"
    filename = "products.csv"

    productdata = loadprod(filename)
    uploadpro(productdata, apiendpoint, apitoken)


