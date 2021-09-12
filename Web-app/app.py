from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import re
import json
import base64

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/shortenurl')
def shortenurl():
    doc=request.args['shortcode']
        # url of the website
    #doc = input("Enter URL: ")
 
    # getting response object
    res = requests.get(doc)
 
    # Initialize the object with the document
    soup = BeautifulSoup(res.content, "html.parser")
    #time.sleep(2)
    #Title Text 
    title = soup.title.text
    title=(str(title).replace("[100% Discount]", ""))


    #Featured Image Link
    q=(soup.find_all("img")[1]) # 0th is site logo & 1st is featured image
    ss = re.findall('data-src=(.+)height=', str(q))
    a=(str(ss).replace("['", "")).replace("']", "")
    a= "<img src="+a+" alt="+title+">"


    #Free Course Redirection link
    urls=(soup.find_all("a"))
    #urls=(soup.find_all("Get this Deal </a>"))  #we need 68th link
    for items in urls:
        check= str(items)
        if "re_track_btn" in check:
            ur=check
            break
    ssu = re.findall('href=(.+)target=', str(ur))
    aa=(str(ssu).replace("['", "")).replace("']", "")
        
    
    # Get the whole body tag
    tag = soup.body
    import re as regex
    c=0
    count=0
    w=str(a)+"<br>"
    #Print each string recursively
    for string in tag.strings:
        #End of text extraction from body
        if "Report Expiry" in string:
            c=300
        if c==300:
            break
        
        #start of text extraction from body
        if "Description" in string:
            c=c+1
        if c==2:#we get 2 Description, start scrapping from 2nd description
            count=count + 1
            if string.rstrip():
                w=w+("<p>"+string+"<p>")
                            
    w=w + "\n" + "<a href="+aa+" target=\"_blank\"><button style=\"background-color: #008CBA;\">GET COUPON CODE</button></a>"
    #print(aa)
    user = '#'
    pythonapp = '#'
    url = '#'
    credentials = user + ':' + pythonapp

    token = base64.b64encode(credentials.encode())
    #aa="token"
    headers = {'Authorization': 'Basic ' + token.decode('utf-8')}
    post = {
            'title': title,
       
            'status': 'publish',
            'content': w,
       
        
            'format': 'standard'
            }
    r=requests.post(url + '/posts', headers=headers, json=post)   #503 error 
    return render_template('shortenurl.html', short1=aa)
