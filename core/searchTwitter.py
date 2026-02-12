from colorama import init, Fore
from core.twitterSearchTool import twitterSearchTool

init(autoreset=True)

# UI Icons
F = f"[{Fore.GREEN}+{Fore.RESET}]"
W = f"[{Fore.RED}!{Fore.RESET}]"
Q = f"[{Fore.YELLOW}?{Fore.RESET}]"

def search_twitter():
    user_input = input(f"{Q} Username: ").strip().replace("@", "")
    if not user_input:
        return

    twitool = twitterSearchTool()
    
    try:
        twitool.getInfoProfile(user_input)
    except Exception as e:
        print(f"{W} Erreur lors de la récupération du profil: {e}")
        return

    if not hasattr(twitool, 'id') or not twitool.id:
        print(f"\n{W} Username '@{user_input}' introuvable ou compte suspendu.")
        return

    # Display Header
    print(f"\n[{Fore.CYAN}@{twitool.username}{Fore.RESET}]\n")

    # Define fields to display (Label, Attribute Name, Default)
    fields = [
        ("Nom", "name", "Inconnu"),
        ("Langue", "langue", "N/A"),
        ("Privé", "protected", "No"),
        ("ID", "id", "N/A"),
        ("Abonnés", "followers", "0"),
        ("Abonnements", "friends", "0"),
        ("Tweets", "status", "0"),
        ("Ville", "location", "Non renseigné"),
        ("Naissance", "birth", "Non renseigné"),
        ("URL", "url", "Aucune"),
        ("Création", "create", "Inconnue")
    ]

    for label, attr, default in fields:
        # Use getattr to safely check if the attribute exists on the tool object
        value = getattr(twitool, attr, default)
        
        # Specific formatting for followers/friends
        if attr == "followers":
            friends_val = getattr(twitool, "friends", "0")
            print(f"{F} Abonnés: {value}  |  Abonnements: {friends_val}")
            continue
        if attr == "friends": # Already handled above
            continue
            
        if value:
            print(f"{F} {label}: {value}")

    # Bio display
    bio = getattr(twitool, "description", "Aucune bio.")
    print(f"\n[BIO]: {bio}")

if __name__ == "__main__":
    search_twitter()