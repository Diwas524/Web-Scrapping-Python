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
    w=str(a)+"\n"
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
                w=w+(string+"\n")
                if count==3:
                    w=w+"<script async src=\"https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-2532272560785706\"crossorigin=\"anonymous\"></script><!-- free post 1 --> <ins class=\"adsbygoogle\" style=\"display:block\" data-ad-client=\"ca-pub-2532272560785706\" data-ad-slot=\"9861387772\" data-ad-format=\"auto\" data-full-width-responsive=\"true\"></ins><script>(adsbygoogle = window.adsbygoogle || []).push({});</script>"+" \n"
                if count==8:
                    w=w+"<script async src=\"https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-2532272560785706\" crossorigin=\"anonymous\"></script> <ins class=\"adsbygoogle\" style=\"display:block\" data-ad-format=\"fluid\" data-ad-layout-key=\"-fb+5w+4e-db+86\" data-ad-client=\"ca-pub-2532272560785706\" data-ad-slot=\"8682029862\"></ins> <script> (adsbygoogle = window.adsbygoogle || []).push({}); </script>"+" \n"
                if count==13:
                    w=w+"<script async src=\"https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-2532272560785706\" crossorigin=\"anonymous\"></script> <ins class=\"adsbygoogle\" style=\"display:block; text-align:center;\" data-ad-layout=\"in-article\" data-ad-format=\"fluid\" data-ad-client=\"ca-pub-2532272560785706\" data-ad-slot=\"3912918919\"></ins> <script> (adsbygoogle = window.adsbygoogle || []).push({}); </script>"+" \n"
                if count==17:
                    w=w+"<script async src=\"https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-2532272560785706\" crossorigin=\"anonymous\"></script> <!-- before enroll now --> <ins class=\"adsbygoogle\" style=\"display:block\" data-ad-client=\"ca-pub-2532272560785706\" data-ad-slot=\"7147594527\" data-ad-format=\"auto\" data-full-width-responsive=\"true\"></ins> <script> (adsbygoogle = window.adsbygoogle || []).push({}); </script>" + " \n"
                    
    w=w + "\n" + "<a href="+aa+" target=\"_blank\"><button style=\"background-color: #008CBA;\">GET COUPON CODE</button></a>"
    #print(aa)
    user = 'admin'
    pythonapp = 'pwTY KpuG 8BJp oLh5 JbNq ZzbT'
    url = 'https://allcoursefree.com/wp-json/wp/v2'
    credentials = user + ':' + pythonapp

    token = base64.b64encode(credentials.encode())

    headers = {'Authorization': 'Basic ' + token.decode('utf-8')}
    post = {
            'title': title,
       
            'status': 'publish',
            'content': w,
       
        
            'format': 'standard'
            }
    r = requests.post(url + '/posts', headers=headers, json=post)
    bb='Your post is published on ' + json.loads(r.content)['link']
    return render_template('shortenurl.html',short=bb, short1=aa)
