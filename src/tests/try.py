from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

import requests
from bs4 import BeautifulSoup as bs

data = defaultdict(list)

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:57.0) Gecko/20100101 Firefox/57.0'}

def get_data(data, headers, page=1):

    # Get start time
    start_time = datetime.now()
    url = f'https://www.jobstreet.co.id/en/job-search/job-vacancy/{page}/?src=20&srcr=2000&ojs=6'
    r = requests.get(url, headers=headers)

    # If the requests is fine, proceed
    if r.ok:
        jobs = bs(r.content,'lxml').find('div',{'id':'job_listing_panel'})
        data['title'].extend([i.text.strip() for i in jobs.find_all('div',{'class':'position-title header-text'})])
        data['company'].extend([i.text.strip() for i in jobs.find_all('h3',{'class':'company-name'})])
        data['location'].extend([i['title'] for i in jobs.find_all('li',{'class':'job-location'})] )
        data['desc'].extend([i.text.strip() for i in jobs.find_all('ul',{'class':'list-unstyled hidden-xs '})])
    else:
        print('connection issues')
    print(f'Page: {page} | Time taken {datetime.now()-start_time}')
    return data
    

def multi_get_data(data,headers,start_page=1,end_page=20,workers=20):
    start_time = datetime.now()
    # Execute our get_data in multiple threads each having a different page number
    with ThreadPoolExecutor(max_workers=workers) as executor:
        [executor.submit(get_data, data=data,headers=headers,page=i) for i in range(start_page,end_page+1)]
    
    print(f'Page {start_page}-{end_page} | Time take {datetime.now() -     start_time}')
    return data


# Test page 10-15
k = multi_get_data(data,headers,start_page=10,end_page=15)