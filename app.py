import streamlit as st
import schedule
import time
import threading
import webbrowser
from scraper import fetch_jobs
from plyer import notification

st.title("Upwork Job Notifier")

keywords = st.text_input("Enter keywords (comma separated)", "")
refresh_rate = st.number_input("Enter refresh rate (minutes)", min_value=1, value=5)

if st.button("Start Notifier"):
    if keywords:
        keywords_list = [kw.strip() for kw in keywords.split(',')]
        seen_jobs = set()
        
        def job_notifier():
            st.write("Checking for new jobs...")
            all_jobs = fetch_jobs(keywords)
            st.write(f"Found {len(all_jobs)} jobs.")
            
            new_jobs = [job for job in all_jobs if job['link'] not in seen_jobs]
            for job in new_jobs:
                seen_jobs.add(job['link'])
            
            if new_jobs:
                for job in new_jobs:
                    st.write(f"**{job['title']}**")
                    st.write(job['summary'])
                    if st.button(f"Apply for {job['title']}", key=job['link']):
                        webbrowser.open_new_tab(job['link'])
                    
                    # Send desktop notification
                    notification.notify(
                        title=f"New Upwork Job: {job['title']}",
                        message=job['summary'],
                        app_name='Upwork Job Notifier',
                        timeout=10
                    )
            else:
                st.write("No new jobs found.")
        
        def run_continuously():
            while True:
                schedule.run_pending()
                time.sleep(1)
        
        schedule.every(refresh_rate).minutes.do(job_notifier)
        
        st.write("Notifier is running...")
        
        # Run the schedule in a separate thread to prevent blocking Streamlit
        threading.Thread(target=run_continuously).start()
    else:
        st.write("Please enter at least one keyword.")
