# AKM12 — versions officielles

Ce dépôt publie les **versions officielles** des logiciels AKM12 (Advanced Knowledge & Maintenance).
Il ne contient pas de code source : uniquement les fichiers à télécharger, attachés à chaque
[Release](https://github.com/akm12-dev/releases/releases).

Catalogue, fiches et documentation : **https://akm12.com/logiciels**

| Logiciel | Dernière version | Système |
|---|---|---|
| Canon Scan Setup | [1.1.0](https://github.com/akm12-dev/releases/releases/tag/canon-scan-setup-v1.1.0) | Windows, macOS |
| Toshiba & Lexmark Scan Setup | [1.1.0](https://github.com/akm12-dev/releases/releases/tag/toshiba-lexmark-scan-setup-v1.1.0) | Windows |
| EdenDisk | [2.0.1](https://github.com/akm12-dev/releases/releases/tag/edendisk-v2.0.1) | Windows |
| SAV Service Tool | [2.0.1](https://github.com/akm12-dev/releases/releases/tag/sav-service-tool-v2.0.1) | Windows |
| EyeControl | [0.1.0](https://github.com/akm12-dev/releases/releases/tag/eyecontrol-v0.1.0) | Windows, Linux |

Les logiciels sont gratuits et ne demandent aucune inscription.

## Vérifier un fichier téléchargé

Chaque version est accompagnée d'un fichier `SHA256SUMS-…txt` et de l'empreinte affichée sur la fiche akm12.com.

```powershell
Get-FileHash .\CanonScanSetup-1.1.0-windows.exe -Algorithm SHA256
```

Sur Mac (Terminal) :

```bash
shasum -a 256 ~/Downloads/CanonScanSetup-1.1.0-macos.dmg
```

L'empreinte obtenue doit être identique à celle publiée. Sinon, supprimez le fichier et téléchargez-le de nouveau
depuis ce dépôt ou depuis akm12.com.

## Avertissement Windows SmartScreen

Les exécutables ne sont pas encore signés numériquement. Au premier lancement, Windows peut afficher
« Windows a protégé votre ordinateur » : vérifiez l'empreinte SHA-256, puis cliquez sur
**Informations complémentaires › Exécuter quand même**. Ne désactivez pas votre antivirus.

## Signaler un problème

Ouvrez une [Issue](https://github.com/akm12-dev/releases/issues) en précisant le logiciel, sa version,
votre version de Windows et le message d'erreur exact. N'envoyez jamais de mot de passe ni de fichier `config.json`.

## Licence

Logiciels gratuits. Tous droits réservés : la redistribution des fichiers est soumise à l'autorisation d'AKM12.
