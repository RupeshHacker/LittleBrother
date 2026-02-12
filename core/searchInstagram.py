import os
from colorama import init, Fore
from core.instagramSearchTool import instagramSearchTool
from core.shortCutUrl import shortCutUrl

init(autoreset=True)

# UI Icons using f-strings for speed
W = f"[{Fore.RED}!{Fore.RESET}]"
Q = f"[{Fore.YELLOW}?{Fore.RESET}]"
F = f"[{Fore.GREEN}+{Fore.RESET}]"
S = f"[{Fore.MAGENTA}*{Fore.RESET}]"

def search_instagram():
    user = input(f"{Q} Username: ").strip()
    if not user: return

    insta = instagramSearchTool()
    insta.get_info(user)

    if not insta.name:
        print(f"\n{W} Username '{user}' not found.")
        return

    # Display Header
    print(f"\n[{Fore.CYAN}{insta.username}{Fore.RESET}]\n")
    
    # Using a dictionary to loop through standard fields cleanly
    fields = [
        ("Name", insta.name),
        ("ID", insta.id),
        ("Protected", "Yes" if insta.private else "No"),
        ("Abonnés", f"{insta.followers}  |  Abonnements: {insta.friends}"),
        ("Publication", insta.medias),
        ("Bio", insta.biography),
        ("Pictures", shortCutUrl(insta.profi_pic_hd))
    ]

    for label, value in fields:
        if value:
            print(f"{F} {label}: {value}")

    # Display Conditional Fields
    extra_fields = {
        "Url": insta.url,
        "Email": insta.email,
        "Telephone": insta.phone,
        "Lieux": insta.adresse
    }

    for label, value in extra_fields.items():
        if value:
            print(f"{F} {label}: {value}")

    # Media Downloader Logic
    if not insta.private:
        print(f"\n{Q} Voulez vous télécharger les 12 dernières photos postées ?")
        choix = input(" [o/N]: ").strip().upper()

        if choix == "O":
            path_default = os.getcwd()
            print(f"\n{Q} Où voulez-vous enregistrer les photos ?")
            print(f"{Fore.YELLOW} Default path: {path_default}{Fore.RESET}")
            
            save_path = input(" Path: ").strip() or path_default

            # Ensure directory exists (Important for Linux/Kali)
            if not os.path.exists(save_path):
                try:
                    os.makedirs(save_path)
                except Exception as e:
                    print(f"{W} Erreur lors de la création du dossier: {e}")
                    return

            print(f"\n{S} Téléchargement des photos de '{user}'...\n")
            
            # Use the method from your optimized search tool
            picture_info = insta.get_pictures_info(user)

            for i, info in picture_info.items():
                media_url = info['display']
                filename = f"{user}_{i}.jpg"
                
                try:
                    insta.downloadPictures(media_url, save_path, filename)
                    # Clean print formatting
                    meta = f"[{info['info'][:30]}...]" if info['info'] else ""
                    loc = f"@{info['localisation']}" if info['localisation'] else ""
                    print(f"({i}) {info['type_media']} {info['date']} {meta} {loc} téléchargé.")
                except Exception as e:
                    print(f"{W} Erreur téléchargement {i}: {e}")

            print(f"\n{F} Téléchargement fini.")

if __name__ == "__main__":
    search_instagram()