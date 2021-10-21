import json
import requests
from bs4 import BeautifulSoup
import uuid

# Scrapping medicine details from netmeds.com


with open("medicines.json", "r") as file:
        data = json.load(file)
        length = len(data)
        batches = int(length / 1000)
        medicine_details=[]
        for ii in range(0,1):
            with open(f"Medicines/medicine{str(ii)}.json", "w") as file1:
                state = 0
                Medicines = []
                product_name=[]
                price =[]
                sizeandcompany=[]
                salts=[]
                product_urls = []
                pimage_urls=[]
                size=[]
                company=[]
                pcategory=[]
                
                for medicine in data[ii * 11: (ii + 1) * 11]:
                    
                    try:
                        state += 1
                        print(state)
                        name = medicine["medicine_name"]
                        Medicine = medicine
                        name = name.lower().replace(' ', '-').replace('\'', '-').replace("\\", "-").replace(".", "-")
                        if(name[len(name)-2:len(name)-1]=="-"):
                            name= name[:len(name)-2]+name[len(name)-1:]
                            print(name)

                        name = name.replace("%", "")
                        first = name.find("(")
                        last = name.find(")")
                        if first != -1:
                            name = name.replace(name[first: last + 1], "")
                        print(name)
                        product_name.append(name)
                        
                        url = "https://www.netmeds.com/prescriptions/" + name
                        product_urls.append(url)
                        data = requests.get(url)
                        if data.status_code == 200:
                            Data = BeautifulSoup(data.text, "lxml")
                            images = Data.find("figure", {"class": "figure largeimage"})
                            # Taking image urls
                            image_urls = []
                            if images is not None:
                                for image in images:
                                    data = BeautifulSoup(f" <body> f{image} </body>", "lxml")
                                    i = data.find('img', {})
                                    if i is not None:
                                        image_urls.append(i['src'])
                            Medicine["image_urls"] = image_urls
                            # print(image_urls)
                            pimage_urls.append(image_urls)

                            
                            # Finding Out MRP
                            amount = Data.find("span", {"class": "final-price"}).get_text().replace("Best Price*", "").replace("₹","").lstrip()
                            Medicine["MRP"] = amount
                            # print(amount)
                            price.append(amount)

                            # Finding Manufacturer
                            manufacturerData = Data.find("span", {"class": "drug-manu"})
                            manufacturerData = manufacturerData.find("a", {})
                            manufacturer_url = manufacturerData['href']
                            try:
                                manufacturer_name = manufacturerData.get_text()
                            except Exception as e:
                                manufacturer_name = None
                            manufacturer = manufacturer_name
                            Medicine["pcompany"] = manufacturer
                            print(manufacturer)
                            company.append(manufacturer)

                            # Variant
                            try:
                                Variant = Data.find("span", {"class": "drug-varient"}).get_text()
                                Medicine["psize"] = Variant
                            except Exception as e:
                                Variant = None
                                
                            # print(Variant)
                            size.append(Variant)
                            # salt
                            try:
                                Salt = Data.find("div", {"class": "drug-manu"}).get_text().strip()
                                Medicine["psize"] = Salt
                            except Exception as e:
                                Medicine["psize"] = None
                                
                            # print(Salt)
                            salts.append(Salt)


                            category = medicine['category']['category']
                            print(category)
                            pcategory.append(category)

                        for i in range(1):
                
                            d1 = {"site name": "netmeds" ,"id": str(uuid.uuid4()),'pname':product_name[i],'psize':size[i],"pcompany":company[i],'mrp':price[i],'salts' :salts[i] ,"image_url":pimage_urls[i],"product_url" : product_urls[i] ,'category': category[i]}
                            # print(d1)
                            medicine_details.append(d1)
                            # Medicines.append(Medicine)
                            
                    except Exception as e:
                        print(e)
                        pass
                try:
                    
                    print(len(product_name))
                    print(len(price))

                    print(len(company))
                    print(len(pcategory))
                    print(pcategory)
                    print(len(size))
                    print(len(product_urls))
                    print(product_urls)
                    print(len(pimage_urls))
                    print(len(product_urls))

                    for i in range(len(product_name)):
                        
                        d1 = {"site name": "netmeds" ,"id": str(uuid.uuid4()),'pname':product_name[i],'psize':size[i],"pcompany":company[i],'mrp':price[i],'salts' :salts[i] ,"image_url":pimage_urls[i],"product_url" : product_urls[i] ,'category': pcategory[i]}
                            # print(d1)
                        medicine_details.append(d1)
                    # json.dump(Medicines, file1)
                except Exception as e:
                    print(e)
                    pass

with open("medicinedetails.json", "w") as file:
        json.dump(medicine_details, file)

