- **11/02**: De l'IA (Gemini) a été utilisé pour conclure sur le type optimale d'algorithme à adopter pour notre modèle à entrainer. Les lignes générés ci-dessous ont été modifiés puis utilisés:
	```py
	clf = svm.SVC(gamma=0.001)
	clf.fit(data, digits.target)
	joblib.dump(clf, 'trained_model.pkl')
	```
