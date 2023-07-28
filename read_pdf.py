import PyPDF2
from fetch_word import give_word

def find_nth2(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start

def pdftojson(): #currently extracts pages and divides into arrays based on sentences
    pdffileobj=open('1.pdf','rb')
    pdfreader=PyPDF2.PdfReader(pdffileobj)
    x=len(pdfreader.pages)
    data = ""

    #file1=open("1.txt","a")
    for i in range(0,x):
        pageobj=pdfreader.pages[i]
        text=pageobj.extract_text()    
        data = data+text.replace("\n","")
        
   
    prejson = []
    
    while find_nth2(data, ".", 2) != -1:
        prejson.append(data[find_nth2(data, ".", 1) : find_nth2(data, ".", 2)].replace(".","").split(" "))
        data=data[find_nth2(data, ".", 2):]                                                                


    return prejson

def pdftojson2(file): #currently extracts pages and divides into arrays based on sentences
    #pdffileobj=open(filename,'rb')
    pdfreader=PyPDF2.PdfReader(file)
    x=len(pdfreader.pages)
    data = ""

    #file1=open("1.txt","a")
    for i in range(0,1):#for i in range(0,x): for all pages
        pageobj=pdfreader.pages[i]
        text=pageobj.extract_text()    
        data = data+text.replace("\n","").replace(".","")
        
    print(f"data before split: {data}")
    text = data
    data = data.split(" ")
    data = list(filter(('').__ne__, data))
    print(f"data after split and filter: {data}")
    
    dict = {}
    for word in data:
        print(f"Fetching {word}:",end="")
        if word in dict.keys():
            print(f" unneeded, already found {word} to be f{dict[word]}")
        else:
            try:
                dict[word] = give_word(word)
                print(f" yielded {dict[word]}")
            except:
                print("didn't work")
    
    return text, dict
    for i in data:
        print(f".{i}")
    return data
    prejson = []
    
    while find_nth2(data, ".", 2) != -1:
        prejson.append(data[find_nth2(data, ".", 1) : find_nth2(data, ".", 2)].replace(".","").split(" "))
        data=data[find_nth2(data, ".", 2):]                                                                


    return prejson

if __name__=="__main__":
    print(str(pdftojson()).replace("'",'"'))
    #file1=open("1.txt","a")
    #for i in range(0,x):
    #    pageobj=pdfreader.pages[i]
    #    text=pageobj.extract_text()    
    #    file1.writelines(text)

    #file1=open("1.txt","a")
    #for i in range(0,x):
    #    pageobj=pdfreader.pages[i]
    #    text=pageobj.extract_text()    
    #    file1.writelines(text)
