import urllib.request,json
from urllib.parse import quote  

def find_nth(haystack, needle, n): #a helper function
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start

def give_definition(name):

    link="https://en.wiktionary.org/w/index.php?search="+quote(name)
    my_request = urllib.request.urlopen(link)
    data = my_request.read()
    #info = json.loads(data)
    #return data
    text=data.decode('utf-8')
    #return text
    if text.find("<p>We could not find the above page on our servers.</p>") != -1: #no such or similar entry
        return "No translation found for " + name 
    good_site = text.find(">Contents</h2>") #finds whether the correct site was found, silly.
    if good_site == -1: #-1 means correct website wasn't found
        if text.find("mw-search-results-container") != -1: #presumably works
            index=find_nth(text,"mw-search-results-container",1) #finds whether there are similar results
            text=text[index:]
            index=find_nth(text,'href="',1) + 6 #
            text=text[index:]
            #return text[index:index+50]
            end_index=find_nth(text,'"',1)
            #return str(index) + " " + str(end_index)
            link=text[:end_index]
            # this creates a link in the form of /wiki/ruoanlaitto
            link="https://en.wiktionary.org"+link
            #return "linkki " + link
            my_request = urllib.request.urlopen(link)
            data = my_request.read()
            #info = json.loads(data)
            #text=info.decode('utf-8')
            #return data
            text=data.decode('utf-8')
        else:
            if(find_nth(text,"There were no results matching the query",1)!=-1):
                return "There were no results matching the query"
            #indexWordType = find_nth(text,name+"</strong>",1) #finds if the word comes from a conjugation/declension
            #indexWordType = indexWordType - 100 #Before the conjugated word comes the type of word
            #if text.find("Noun") != -1:         #Setting the word type
            #    wordType = "Noun"
            #elif text.find("Verb") != -1:
            #    wordType = "Verb"
            #elif text.find("Numeral") != -1:
            #    wordType = "Numeral"
            #elif text.find("Adverb") != -1:
            #    wordType = "Adverb"
            
            index=find_nth(text,"form-of-definition-link",1) #find the link to the original form of a word
            text=text[index:]
            index=find_nth(text,'href="',1) + 6 #
            text=text[index:]
            end_index=find_nth(text,'"',1)
            link=text[:end_index]       # this creates a link in the form of /wiki/ruoanlaitto
            link="https://en.wiktionary.org"+link
            my_request = urllib.request.urlopen(link)
            data = my_request.read()
            text=data.decode('utf-8') #imperfect type for some finnish words.

    
    #index=find_nth(text,"Finnish",4) #Here and below: finding the definition
    index=find_nth(text,'<h2><span class="mw-headline" id="Finnish">Finnish',1)+4
    text=text[index:]
    #print(text + "->text")
    #index=find_nth(text,wordType,1) #wordType is needed because below it is the correct definition of a word
    #text=text[index:]
    #index=find_nth(text,"<ol>",1)
    end_index=min(find_nth(text,"<h2>",1)+4,find_nth(text,'<h2>Navigation menu</h2>',1))
    text=text[:end_index]
    
    text2=text.replace('"',"'")
    if len(text2) == 0:
        return "No translation found for " + name
    if text2 ==  ">":
        return "The case of >"
    return text2


#
#
#
#
#


def give_word(name):

    link="https://en.wiktionary.org/w/index.php?search="+quote(name)
    my_request = urllib.request.urlopen(link)
    data = my_request.read()
    #info = json.loads(data)
    #return data
    text=data.decode('utf-8')
    #return text
    if text.find("<p>We could not find the above page on our servers.</p>") != -1: #no such or similar entry
        return "No translation found for " + name 
    good_site = text.find(">Contents</h2>") #finds whether the correct site was found, silly.
    if good_site == -1: #-1 means correct website wasn't found
        if text.find("mw-search-results-container") != -1: #presumably works
            index=find_nth(text,"mw-search-results-container",1) #finds whether there are similar results
            text=text[index:]
            index=find_nth(text,'href="',1) + 6 #
            text=text[index:]
            #return text[index:index+50]
            end_index=find_nth(text,'"',1)
            #return str(index) + " " + str(end_index)
            link=text[:end_index]
            # this creates a link in the form of /wiki/ruoanlaitto
            word=link[find_nth(link,"/",1)+1:]
            return word
            #link="https://en.wiktionary.org"+link
            #return "linkki " + link
            #my_request = urllib.request.urlopen(link)
            #data = my_request.read()
            #info = json.loads(data)
            #text=info.decode('utf-8')
            #return data
            #text=data.decode('utf-8')
        else:
            if(find_nth(text,"There were no results matching the query",1)!=-1):
                return "There were no results matching the query"
            #indexWordType = find_nth(text,name+"</strong>",1) #finds if the word comes from a conjugation/declension
            #indexWordType = indexWordType - 100 #Before the conjugated word comes the type of word
            #if text.find("Noun") != -1:         #Setting the word type
            #    wordType = "Noun"
            #elif text.find("Verb") != -1:
            #    wordType = "Verb"
            #elif text.find("Numeral") != -1:
            #    wordType = "Numeral"
            #elif text.find("Adverb") != -1:
            #    wordType = "Adverb"
            
            index=find_nth(text,"form-of-definition-link",1) #find the link to the original form of a word
            text=text[index:]
            index=find_nth(text,'href="',1) + 6 #
            text=text[index:]
            end_index=find_nth(text,'"',1)
            link=text[:end_index]       # this creates a link in the form of /wiki/ruoanlaitto
            link = text[:find_nth(link, "#", 1)]
            word=link[find_nth(link,"/",2)+1:]
            return word
            #link="https://en.wiktionary.org"+link
            #my_request = urllib.request.urlopen(link)
            #data = my_request.read()
            #text=data.decode('utf-8') #imperfect type for some finnish words.

    
    #lazy
    #index=find_nth(text,"form-of-definition-link",1) #find the link to the original form of a word
    
    #index=find_nth(text,"Finnish",4) #Here and below: finding the definition
    index=find_nth(text,'<h2><span class="mw-headline" id="Finnish">Finnish',1)+4
    text=text[index:]
    #print(text + "->text")
    #index=find_nth(text,wordType,1) #wordType is needed because below it is the correct definition of a word
    #text=text[index:]
    #index=find_nth(text,"<ol>",1)
    end_index=min(find_nth(text,"<h2>",1)+4,find_nth(text,'<h2>Navigation menu</h2>',1))
    text=text[:end_index]
    #if(find_nth(text, ""))
    text2=text.replace('"',"'")
    text = text[find_nth(text, "form-of-definition-link",1):]
    text = text[find_nth(text, 'title="',1)+7:]
    text = text[:find_nth(text, '"',1)]
    return text
    
    text2=text.replace('"',"'")
    if len(text2) == 0:
        return "No translation found for " + name
    if text2 ==  ">":
        return "The case of >"
    return text2




def give_word2(name):
    name = urllib.parse.unquote(name)
    name = name.lower()
    link="https://en.wiktionary.org/w/index.php?search="+quote(name)
    my_request = urllib.request.urlopen(link)
    data = my_request.read()
    #info = json.loads(data)
    #return data
    text=data.decode('utf-8')
    #return text
    if text.find("<p>We could not find the above page on our servers.</p>") != -1: #no such or similar entry
        return "No translation found for " + name 
    good_site = text.find(">Contents</h2>") #finds whether the correct site was found, silly.
    
    if text.find("mw-search-results-container") != -1: #presumably works
        index=find_nth(text,"mw-search-results-container",1) #finds whether there are similar results
        text=text[index:]
        index=find_nth(text,'href="',1) + 6 #
        text=text[index:]
        #return text[index:index+50]
        end_index=find_nth(text,'"',1)
        #return str(index) + " " + str(end_index)
        link=text[:end_index]
        # this creates a link in the form of /wiki/ruoanlaitto
        link="https://en.wiktionary.org"+link
        #return "linkki " + link
        my_request = urllib.request.urlopen(link)
        data = my_request.read()
        #info = json.loads(data)
        #text=info.decode('utf-8')
        #return data
        text=data.decode('utf-8')
    else:
        if(find_nth(text,"There were no results matching the query",1)!=-1):
            return "There were no results matching the query"
        #indexWordType = find_nth(text,name+"</strong>",1) #finds if the word comes from a conjugation/declension
        #indexWordType = indexWordType - 100 #Before the conjugated word comes the type of word
        #if text.find("Noun") != -1:         #Setting the word type
        #    wordType = "Noun"
        #elif text.find("Verb") != -1:
        #    wordType = "Verb"
        #elif text.find("Numeral") != -1:
        #    wordType = "Numeral"
        #elif text.find("Adverb") != -1:
        #    wordType = "Adverb"
        #new
        index=find_nth(text,'<h2><span class="mw-headline" id="Finnish">Finnish',1)+4
        text=text[index:]
        end_index=min(find_nth(text,"<h2>",1)+4,find_nth(text,'<h2>Navigation menu</h2>',1))
        text=text[:end_index]

        index=find_nth(text,"form-of-definition-link",1) #find the link to the original form of a word
        if(index != -1):
            text=text[index:]
            index=find_nth(text,'href="',1) + 6 #
            text=text[index:]
            end_index=find_nth(text,'"',1)
            link=text[:end_index]       # this creates a link in the form of /wiki/ruoanlaitto
            link="https://en.wiktionary.org"+link
            print(f"link: {link}")
            try: 
                my_request = urllib.request.urlopen(link)
                data = my_request.read()
                text=data.decode('utf-8') #imperfect type for some finnish words.
            except:
                pass
            

    index=find_nth(text,'<h2><span class="mw-headline" id="Finnish">Finnish',1)+4
    text=text[index:]
    end_index=min(find_nth(text,"<h2>",1)+4,find_nth(text,'<h2>Navigation menu</h2>',1))
    text=text[:end_index]
    #new

    index = find_nth(text, '<strong class="Latn headword" lang="fi">',0)+40
    text = text[index:]
    end_index = find_nth(text, '<',1)
    text= text[:end_index]
    #print(f"index {index}")
    return text
    print(text)
    text = text[index:]
    
    print(text)

    text2=text.replace('"',"'")
    if len(text2) == 0:
        return "No translation found for " + name
    if text2 ==  ">":
        return "The case of > i.e. index -1 i.e. not found"
    return text2



if __name__=="__main__":   #test script #mennä doesn't work
    #print(urllib.parse.unquote("lehteä"))
    print(give_word2("lehteä"))
    print(give_word2(urllib.parse.unquote("Viikonloppuisin")))
    
