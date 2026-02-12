import os
import time
from datetime import date
from colorama import init, Fore
from terminaltables import SingleTable

# Local imports
from core.watcher import watcher
from core.instagramSearchTool import instagramSearchTool
from core.facebookSearchTool import facebookSearchTool
from core.twitterSearchTool import twitterSearchTool
from core.Profiler import Profiler
from core.RegexTool import RegexTool

init(autoreset=True)

# UI Icons
W, Q, F, S = f"[{Fore.RED}!{Fore.RESET}]", f"[{Fore.YELLOW}?{Fore.RESET}]", f"[{Fore.GREEN}+{Fore.RESET}]", f"[{Fore.MAGENTA}*{Fore.RESET}]"

def profiler_func(profile=None, path=''):
    if not profile:
        print(f"\n{W} Profile not found")
        return

    profile_name = profile['name']
    profile_id = profile['id']
    filename = profile['file']
    
    print(f"\n{F} Profil sélectionné: {profile_name} ({profile_id})\n")

    pr = Profiler()
    data_profile = pr.read_profile(filename, path=path) or {}
    
    # Standardized extraction of URLs
    urls = data_profile.get('URL', {})
    url_twitter = urls.get('Twitter')
    url_facebook = urls.get('Facebook')
    url_instagram = urls.get('Instagram')

    current_data = {}
    news_items = []

    # 1. Fetch Fresh Social Data
    if url_twitter:
        twit = twitterSearchTool()
        twit.getInfoProfile(url_twitter)
        current_data['TWITTER'] = {
            'id': twit.id, 'name': twit.name, 'username': twit.username,
            'location': twit.location, 'urlFound': twit.url, 'description': twit.description, 'urlAccount': url_twitter
        }

    if url_facebook:
        fb = facebookSearchTool()
        fb.getInfoProfile(url_facebook)
        current_data['FACEBOOK'] = {
            'id': fb.facebookId, 'name': fb.name, 'location': fb.address,
            'job': fb.job, 'username': fb.username, 'affiliations': fb.affiliations, 'urlAccount': url_facebook
        }

    if url_instagram:
        insta = instagramSearchTool()
        insta.getInfo(url_instagram)
        current_data['INSTAGRAM'] = {
            'id': insta.id, 'name': insta.name, 'username': insta.username,
            'location': insta.adresse, 'description': insta.biography,
            'email': insta.email, 'phone': insta.phone, 'urlAccount': url_instagram
        }

    # 2. Automated Update & News Detection
    for platform, new_info in current_data.items():
        if platform in data_profile:
            for key, val in new_info.items():
                if data_profile[platform].get(key) != val:
                    news_items.append(f"{platform} {key}: {val}")
        data_profile[platform] = new_info

    # 3. Save Updated Profile
    if current_data:
        pr.write_profile(filename, path, data_profile)

    # 4. Regex Analysis (Emails/Phones)
    found_emails, found_phones = set(), set()
    # Add known insta data
    if current_data.get('INSTAGRAM', {}).get('email'): found_emails.add(current_data['INSTAGRAM']['email'])
    
    # Extract from biographies
    for platform in ['TWITTER', 'INSTAGRAM']:
        bio = current_data.get(platform, {}).get('description', '')
        if bio:
            rx = RegexTool(bio)
            found_emails.update(rx.Email().email if hasattr(rx.Email(), 'email') else [])
            # ... repeat for phones if RegexTool supports it

    # 5. Build Global Info String
    t_info = current_data.get('TWITTER', {})
    f_info = current_data.get('FACEBOOK', {})
    i_info = current_data.get('INSTAGRAM', {})

    summary = f"""
    Date: {date.today()}
    Profil ID: {profile_id} | Nom: {profile_name}
    --------------------------------------------------
    Téléphone: {", ".join(found_phones) or 'N/A'}
    Emails:    {", ".join(found_emails) or 'N/A'}
    Loc:       Insta: {i_info.get('location')} | Twit: {t_info.get('location')} | FB: {f_info.get('location')}
    Job:       {f_info.get('job', 'N/A')}
    Pseudos:   FB: {f_info.get('username')} | Twit: {t_info.get('username')} | Insta: {i_info.get('username')}
    --------------------------------------------------
    Facebook:  ({f_info.get('id')}) - {url_facebook}
    Twitter:   ({t_info.get('id')}) - {url_twitter}
    Instagram: ({i_info.get('id')}) - {url_instagram}
    """

    # 6. Activity Watcher (Last Posts)
    watch_results = []
    w = watcher()
    if url_instagram: 
        w.instagramWatcher(url_instagram)
        watch_results.append(w.medias)
    if url_twitter: 
        w.twitterWatcher(url_twitter)
        watch_results.append(w.tweet)

    if watch_results:
        timeline = pr.time_sort(watch_results, reverse=True)
        table_data = [('Date', 'Domain', 'Content/URL', 'Loc')]
        for ts, d in timeline.items():
            content = d.get('tweet', d.get('urlMedia', 'N/A'))
            table_data.append((time.ctime(ts), d['domain'], content[:40], d.get('location', 'None')))
        
        print(SingleTable(table_data, " Last Activity ").table)

    print(summary)
    if news_items:
        print(f"{F} Nouveautés détectées:\n" + "\n".join(news_items))

    # 7. Export Logic
    export_name = filename.replace(".prfl", ".txt")
    if input(f"\n{Q} Exporter vers {export_name} ? [O/n]: ").lower() in ('', 'o', 'y'):
        if pr.export_text(export_name, path, summary):
            print(f"{F} Export réussi: {os.path.join(path, export_name)}")