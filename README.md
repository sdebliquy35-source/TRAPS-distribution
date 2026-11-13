# Téléchargements TRAPS

> [!IMPORTANT]
> **Jugement 0.70 : erreur de certificat pendant « Installer et redémarrer » ?**
>
> Installez cette mise à jour une fois depuis votre navigateur :
>
> **[Télécharger Jugement 0.74 pour Windows](https://github.com/sdebliquy35-source/TRAPS-distribution/releases/download/jugement-74/Jugement_TRAPS_0.74_Windows_x64.exe)**
>
> 1. Téléchargez le fichier dans votre navigateur.
> 2. Dans Jugement, choisissez **Arrêter Jugement et quitter**. Fermer seulement la fenêtre ne suffit pas.
> 3. Lancez le fichier téléchargé, **sans désinstaller Jugement ni effacer ses données**.
>
> La 0.73 corrige la gestion des certificats pour les prochaines mises à jour. La 0.70 déjà installée ne peut pas réparer elle-même son téléchargement défaillant. La même procédure s’applique aux autres anciennes versions présentant cette erreur.

**TRAPS 2.0 pour Android** et **Jugement_TRAPS pour Windows 10/11 64 bits**.

Les téléchargements sont publics et ne nécessitent pas de compte GitHub. Les dépôts de sources restent privés. Les logiciels restent soumis à leur licence propriétaire ; un téléchargement public ne constitue pas une autorisation de redistribution ou de modification.

➡ [Télécharger une version publiée](https://github.com/sdebliquy35-source/TRAPS-distribution/releases)

## Versions disponibles

- **[Jugement TRAPS 0.74 — Windows 10/11 64 bits](https://github.com/sdebliquy35-source/TRAPS-distribution/releases/download/jugement-74/Jugement_TRAPS_0.74_Windows_x64.exe)**
- **[TRAPS 2.0 — APK110 Android](https://github.com/sdebliquy35-source/TRAPS-distribution/releases/download/traps-110/TRAPS_2.0_APK110.apk)**

Jugement 0.74 inclut les contrôles des révisions et effacements, la correction de sélection des chronos après restauration et l’ordre des départs dans les fiches/tableaux. APK110 reste la version Android actuelle ; les correctifs 0.74 ne nécessitent pas de changement sur les téléphones.

## Guides illustrés

- [Guide TRAPS 2.0 pour Android (13 pages)](guides/Guide_TRAPS_2.0.pdf)
- [Guide Jugement TRAPS - Serveur et Juge Arbitre (14 pages)](guides/Guide_Jugement_TRAPS.pdf)

Les guides sont mis à jour à ces mêmes liens. Référence actuelle des guides : APK110 et Jugement 0.74. Les captures utilisent une course fictive.

## Installation et mises à jour

Jugement contient Python et son visualiseur. Installer puis choisir **Serveur Jugement** ou **Poste Juge Arbitre** au premier lancement. Le rôle peut ensuite être changé dans **Poste et connexion**. Le JA s’associe au Serveur avec le code à six chiffres existant.

Les mises à jour sont recherchées au démarrage et signalées dans les applications. Aucune recherche périodique pendant la course ; un contrôle manuel reste possible. Aucune installation automatique pendant une course. Les données de course ne sont pas publiées ici et restent conservées sur les appareils.

Les **10 dernières versions publiées de chaque application** sont conservées dans Releases. Les anciennes versions ne sont pas réinstallées automatiquement. La suppression d’un ancien téléchargement ne supprime jamais les données des utilisateurs.

Premières versions distribuées : **APK107** et **Jugement 0.68**. Télécharger le fichier `.apk` pour Android ou `.exe` pour Windows ; les liens « Source code » générés par GitHub contiennent uniquement le contenu de ce dépôt de distribution.

Pour une installation existante de Jugement : arrêter l’ancien serveur, garder une sauvegarde de son dossier de données, puis choisir **Utiliser une installation existante** et son fichier `jugement.sqlite3` au premier lancement. Les données restent dans leur dossier. Une installation neuve stocke ses données dans le profil Windows.

L’installateur demande les droits administrateur et configure la réception sur le réseau local. À partir de Jugement 0.70, **Installer et redémarrer** télécharge, vérifie, arrête proprement puis relance le programme, après confirmation de l’opérateur. Aucun téléchargement du paquet ni installation sans cet accord. Pour installer 0.70 depuis une version antérieure, utiliser une dernière fois **Arrêter Jugement et quitter** puis lancer l’installateur téléchargé. Fermer seulement le visualiseur laisse la réception fonctionner en arrière-plan. Les demandes de sécurité Windows peuvent rester nécessaires.

Validation de Jugement 0.70 : 676 tests réussis sur Windows, contrôle du programme autonome, de son rendu Qt et de l’assistant séparé. Le premier essai opérationnel du visualiseur, de l’impression et des fenêtres sur plusieurs écrans reste à réaliser sur les PC de course. L’installateur n’a pas de certificat commercial de signature Windows.
