import by_questions, by_attributes


def film_reco():
    while True:
        print("Voulez-vous :")
        print("1. Rechercher via des questions ?")
        print("2. Rechercher via des attributs ?")
        print("3. Quitter")
        resp = input("Votre choix : ")
        while resp not in ("1", "2", "3"):
            print("Entrée invalide. Choisissez entre '1', '2' et '3'")
            resp = input("Votre choix : ")
        if resp == "1":
            by_questions.display_best()
        elif resp == "2":
            by_attributes.by_attributes()
        else :
            break
        
        
film_reco()