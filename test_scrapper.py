from scraper import fetch_jobs

def test_fetch_jobs():
    keywords = "website developer, shopify, data analysis, website design, UI/UX"
    jobs = fetch_jobs(keywords)
    for job in jobs:
        print(f"Title: {job['title']}")
        print(f"Link: {job['link']}")
        print(f"Summary: {job['summary']}")
        print("---")

if __name__ == "__main__":
    test_fetch_jobs()
