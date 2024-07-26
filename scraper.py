import requests
from bs4 import BeautifulSoup

def fetch_jobs(keywords):
    search_url = "https://www.upwork.com/nx/jobs/search/?q=" + "+".join(keywords.split(','))
    response = requests.get(search_url)
    
    if response.status_code != 200:
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    jobs = []
    for job_elem in soup.find_all('div', class_='up-card-section'):
        title_elem = job_elem.find('h4', class_='up-card-title')
        link_elem = job_elem.find('a', class_='up-card-link')
        summary_elem = job_elem.find('span', class_='up-card-description')
        
        if None in (title_elem, link_elem, summary_elem):
            continue
        
        jobs.append({
            'title': title_elem.text.strip(),
            'link': "https://www.upwork.com" + link_elem['href'],
            'summary': summary_elem.text.strip()
        })
    
    return jobs
