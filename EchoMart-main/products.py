import pandas as pd
import pickle
def pickler(name,obj):
    file = open(name+".pickle","wb")
    pickle.dump(obj=obj,file=file)
    file.close()

def depickle(fname):
    file = open(fname+".pickle","rb")
    pickle_obj = pickle.load(file)
    file.close()
    return pickle_obj

def getData():
    df = pd.read_csv('Book2.csv',header=0)
    print(df)
    print(df.columns)
    total_tags = list(df['Tag1'])
    total_tags += list(df['Tag2'])
    total_tags += list(df['Tag3'])
    total_tags += list(df['Tag4'])
    total_tags += list(df['Tag5'])
    total_tags = list(set([i.lower() for i in total_tags]))
    pickler('total_tags',total_tags)

    
    #print(total_tags)
def getNewData():
    file = open("D:\\Downloaded Files\\newproducts.csv","r")
    rows = file.readlines()
    rows = rows[1:]
    tag_set = set()
    for row in rows:
        tmp = row.split(',')
        tmp.pop(0)
        for word in tmp:
            ok = [i.lower() for i in word.split()]
            for tag in ok:
                tag_set.add(tag)
    new_tags = list(tag_set)
    #print(new_tags)
    file.close()
    obj = depickle("total_tags")
    obj+=new_tags
    obj = list(set(obj))
    pickler('total_tags2',obj=obj)
    print(obj)

def getDict():
    df = pd.read_csv('Book2.csv',header=0)
    #print(df.head())

    # Convert the DataFrame to a dictionary
    result_dict = df.groupby('Product').apply(lambda x: x.drop('Product', axis=1).values[0].tolist()).to_dict()
    for key in result_dict:
        tmp = []
        for i in result_dict[key]:
            tmp+=i.split()
        result_dict[key] = tmp.copy()

    pfile = open("formattedproducts.csv","r")
    prows = pfile.readlines()
    #print(len(prows))
    prows.pop(0)
    pfile.close()
    prod_dict = {}
    for row in prows:
        tmp = row.split(',')
        tmp[-1] = tmp[-1][:-1]
        pname = tmp.pop(0)
        prod_dict[pname] = tmp
    result_dict.update(prod_dict)
    #print(len(result_dict))

    return result_dict

#print(getDict())


def ProductMatch(tags):
    prod_catalog = getDict()
    match = []
    for prod in prod_catalog:
        ptags = {i.lower() for i in prod_catalog[prod]}
        if ptags.intersection(tags)==tags:
            match.append(prod)
    return match



class Shopper:
    def __init__(self,user_name,email,phone_num,address):
        self.user_name = user_name
        self.email = email
        self.phone_num = phone_num
        self.address = address
    def store(self):
        file = open("Profile\\"+self.user_name+".pickle","wb")
        pickle.dump(obj=self,file=file)
        file.close()

#print(ProductMatch({'shirt','cotton'}))

print(depickle('total_tags'))
