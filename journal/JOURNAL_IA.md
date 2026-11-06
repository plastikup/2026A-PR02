- **11/02**: De l'IA (Gemini) a été utilisé pour conclure sur le type optimale d'algorithme à adopter pour notre modèle à entrainer. Les lignes générés ci-dessous ont été modifiés puis utilisés:
	```py
	clf = svm.SVC(gamma=0.001)
	clf.fit(data, digits.target)
	joblib.dump(clf, 'trained_model.pkl')
	```
- **11/05** L'IA (CoPilot) a été utilisé pour le déboguage des erreurs de FileNotFoundError dans le fichier scenes.py pour le chemin du fichier dataset.csv. La ligne ci-dessous a été recommandé par IA: 
	Ancient code:
	```py
	source = os.path.dirname(os.path.abspath(__file__))
	```
	Nouvelle code généré par IA:
	```py
	source = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	```