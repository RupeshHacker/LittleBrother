from core.facebookSearchTool import facebookSearchTool
import webbrowser, colorama
from colorama import init, Fore,  Back,  Style

init()
warning = "["+Fore.RED+"!"+Fore.RESET+"]"
question = "["+Fore.YELLOW+"?"+Fore.RESET+"]"
information = "["+Fore.BLUE+"I"+Fore.RESET+"]"
wait = "["+Fore.MAGENTA+"*"+Fore.RESET+"]"
found = "["+Fore.GREEN+"+"+Fore.RESET+"]"
tiret = "["+Fore.CYAN+"-"+Fore.RESET+"]"

def facebookStalk():
	profile = input(" Facebook username: ")
	if profile.startswith("http"):
		profile = profile.split("/")
		profile = profile[3]

	menuStalk = """

        TAGS              PERSONNES              LIEUX
    ------------        -------------        -------------
    [1] Photos          [4] Famille          [10] Tout
    [2] Videos          [5] Amis             [11] Bars
    [3] Publication     [6] Amis en commun   [12] Restaurants
                        [7] Travail          [13] Magasin
        LIKE            [8] Etude            [14] Exterieur
    ------------        [9] Locaux           [15] Hotels
    [17] Photos                              [16] Theatre
    [18] Videos          COMMENTAIRE
    [19] Publications   -------------          INTERETS     
                        [20] Photos          -------------
        PROFIL                               [29] Pages
    -------------                            [30] Politiques
    [21] Photos                              [31] Religion
    [22] Videos                              [32] Musiques
    [23] Publications                        [33] Films
    [24] Groupes                             [34] Livres
    [25] Futur evenements                    [35] Lieux
    [26] Evenements passes
    [27] Jeux
    [28] Apps

        [b] Back    [c] Clear screen    [e] Exit script
	"""

	dicFbStalk = {
	# <
	# TAGS 
	"1": "https://www.facebook.com/search/%s/photos-of/intersect",
	"2": "https://www.facebook.com/search/%s/videos-of/intersect",
	"3": "https://www.facebook.com/search/%s/stories-tagged/intersect",
	# PERSONNE
	"4": "https://www.facebook.com/search/%s/relatives/intersect",
	"5": "https://www.facebook.com/search/%s/friends/intersect",
	"6": "https://www.facebook.com/search/%s/friends/friends/intersect",
	"7": "https://www.facebook.com/search/%s/employees/intersect/",
	"8": "https://www.facebook.com/search/%s/schools-attended/ever-past/intersect/students/intersect/",
	"9": "https://www.facebook.com/search/%s/current-cities/residents-near/present/intersect",
	# LEUX
	"10": "https://www.facebook.com/search/%s/places-visited/",
	"11": "https://www.facebook.com/search/%s/places-visited/110290705711626/places/intersect/",
	"12": "https://www.facebook.com/search/%s/places-visited/273819889375819/places/intersect/",
	"13": "https://www.facebook.com/search/%s/places-visited/200600219953504/places/intersect/",
	"14": "https://www.facebook.com/search/%s/places-visited/935165616516865/places/intersect/",
	"15": "https://www.facebook.com/search/%s/places-visited/164243073639257/places/intersect/",
	"16": "https://www.facebook.com/search/%s/places-visited/192511100766680/places/intersect/",
	# LIKE
	"17": "https://www.facebook.com/search/%s/photos-liked/intersect",
	"18": "https://www.facebook.com/search/%s/videos-liked/intersect",
	"19": "https://www.facebook.com/search/%s/stories-liked/intersect",
	# COMMENTAIRE
	"20": "https://www.facebook.com/search/%s/photos-commented/intersect",
	# PROFIL
	"21": "https://www.facebook.com/search/%s/photos-by/",
	"22": "https://www.facebook.com/search/%s/videos-by/",
	"23": "https://www.facebook.com/search/%s/stories-by/",
	"24": "https://www.facebook.com/search/%s/groups",
	"25": "https://www.facebook.com/search/%s/events-joined/",
	"26": "https://www.facebook.com/search/%s/events-joined/in-past/date/events/intersect/",
	"27": "https://www.facebook.com/search/%s/apps-used/game/apps/intersect",
	"28": "https://www.facebook.com/search/%s/apps-used/",
	# INTERETS
	"29": "https://www.facebook.com/search/%s/pages-liked/intersect",
	"30": "https://www.facebook.com/search/%s/pages-liked/161431733929266/pages/intersect/",
	"31": "https://www.facebook.com/search/%s/pages-liked/religion/pages/intersect/",
	"32": "https://www.facebook.com/search/%s/pages-liked/musician/pages/intersect/",
	"33": "https://www.facebook.com/search/%s/pages-liked/movie/pages/intersect/",
	"34": "https://www.facebook.com/search/%s/pages-liked/book/pages/intersect/",
	"35": "https://www.facebook.com/search/%s/places-liked/"
	}

	helpMsgFbStalk = """
		back : Revenir au menu principal.
		exit / quit  : Pour quitter le logiciel.
		clear : Efface l'ecran."""

	resultProfile = """
    [Name]  %s
    [work]  %s
    [Loc]   %s
    [ID]    %s"""

	fbtool = facebookSearchTool()

	# 1. Attempt Initial Data Collection
	try:
		fbtool.getInfoProfile(profile)
		# Using .get() style or direct assignment if attributes are guaranteed
		loc = fbtool.address or "Inconnu"
		work = fbtool.job or "Inconnu"
		name = fbtool.name or "Inconnu"
		facebook_id = fbtool.facebookId
	except Exception as e:
		print(f"\n{W} Une erreur est survenue : {e}")
		return

	# 2. ID Validation Step
	if not facebook_id:
		print(f"\n{W} Impossible de récupérer l'ID automatiquement.")
		choice = input(f"{Q} Connaissez-vous l'ID ? [O/N]: ").upper()
		if choice in ("O", "Y"):
			facebook_id = input(f"{S} Entrez l'ID: ").strip()
		else:
			return # Exit stalker if no ID is available

	# 3. Display Results Summary
	# Assuming resultProfile is a pre-defined format string
	print(resultProfile % (name, work, loc, facebook_id))
	print(menuStalk)

	# 4. Interactive Menu Loop
	while True:
		prompt = f"\nLittleBrother({Fore.BLUE}Lookup/facebookStalk{Fore.RESET})$ "
		cmd = input(prompt).strip().lower()

		if cmd == "help":
			print(helpMsgFbStalk)
		elif cmd == "c":
			clear() # Ensure clear() is defined in your core utils
			print(menuStalk)
		elif cmd == "b":
			break # Go back to previous menu
		elif cmd == "e":
			exit()
		elif cmd == "29":
			# Specialized Page Liked check
			print(f"{S} Recherche des pages aimées...")
			pages = fbtool.searchPageLiked(profile)
			if pages:
				for p in pages:
					print(f"[{Fore.GREEN}Liked{Fore.RESET}] {p}")
			else:
				print(f"{W} Aucune page trouvée ou profil privé.")
		else:
			# Handle Numeric Menu Options (Opening Browser)
			if cmd.isdigit():
				target_url_template = dicFbStalk.get(cmd)
				if target_url_template:
					final_url = target_url_template % facebook_id
					print(f"{S} Ouverture de : {final_url}")
					webbrowser.open(final_url)
				else:
					print(f"{W} Option '{cmd}' non reconnue.")