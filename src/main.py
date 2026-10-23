def bootstrap():
	gray_bg, cyan, reset = '\x1b[100m', '\x1b[96m', '\x1b[0m'

	print(f'{gray_bg}PR02A26 - Modèle de prédiction - Par Jialun Cao et Junyi Zhang{reset}')
	print(f'{cyan}Que souhaitez-vous faire?{reset}')
	print(f"{cyan}(1){reset} Entrainer l'IA;")
	print(f"{cyan}(2){reset} Ouvrir l'interface utilisateur;")

	option = input(f'{cyan}Entrez le numéro, ou rien mettre pour 2: {reset}')

	if option == '1': print('got 1')
	elif option == '2' or option == '': print('got 2')

	print('exiting')


if __name__ == "__main__":
    bootstrap()
