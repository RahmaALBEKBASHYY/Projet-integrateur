La traduction française est ci-dessous. 👇

**Readme - Integrative Project - Trivial Pursuit Game**

This Readme is intended to provide instructions and essential information about the Trivial Pursuit game project developed as part of the Integrative Project with a team of 10 people. This document focuses on the server-side of the project, particularly emphasizing the method of communication between virtual machines (VMs) and the outside world.

---

### Project Description

The project involves developing an online version of the Trivial Pursuit game. The server-side aspects of the game are hosted on virtual machines (VMs) with a private network addressing (192.168.x.y). These VMs are not directly accessible from the Internet and require the use of a bastion to access them.

### Communication with VMs

To access the web servers hosted on the VMs, we use a bastion as an access point. Here's how to access the web servers of the VMs:

1. Access the bastion via SSH using the provided public IP address.
2. Use the bastion as a reverse proxy to access the web servers hosted on the VMs.
3. To access a web server on a VM, use the following URL: `https://bastion_ip/vm_name/` (note the use of HTTPS and forward slashes).
4. The first time you access this URL, your browser may display a security alert. In Firefox, you can bypass this by clicking "Advanced" and then "Accept the Risk and Continue".

### Choice of Server Software

We need to choose server software to handle user HTTP requests. Two popular options are Apache and NGINX. Here's a quick comparison:

- **Apache**:
  - Process-based architecture.
  - Many available add-on modules.
  - Handles both static and dynamic content.
  - High security with configuration tricks for attack management.

- **NGINX**:
  - Event-based architecture.
  - High performance for static content.
  - Handles dynamic content within the server.
  - Enhanced security with finer code base.

### Git Directory Structure

- **/docs**: This folder contains all project-related documentation.
- **/src**: Contains the source code of the web server, separated by VM if necessary.
- **README.md**: This file you are currently reading, providing essential information about the project.

### How to Contribute

If you wish to contribute to the project, please follow these steps:

1. Fork the project from GitHub.
2. Clone your fork locally on your machine.
3. Create a branch for your feature (`git checkout -b feature/feature-name`).
4. Make your changes.
5. Add and commit your changes (`git add . && git commit -m "Description of the modification"`).
6. Push your changes to your fork on GitHub (`git push origin feature/feature-name`).
7. Create a Pull Request on the original repository.

### Notes

- Ensure adherence to coding standards defined by the team.
- Any significant changes must be discussed with the team before implementation.

---

This Readme provides an overview of the project, instructions for contribution, and information about communication with VMs and the choice of server software. For more detailed information, please refer to the documentation in the `/docs` folder.

---
**Readme - Projet Intégrateur - Jeu Trivial Pursuit**

Ce Readme est destiné à fournir des instructions et des informations essentielles sur le projet de jeu Trivial Pursuit réalisé dans le cadre du Projet Intégrateur avec une équipe de 10 personnes. Ce document se concentre sur le côté serveur du projet, en mettant particulièrement l'accent sur la méthode de communication entre les machines virtuelles (VM) et le monde extérieur.

---

### Description du Projet

Le projet consiste à développer une version du jeu Trivial Pursuit en ligne. Les aspects serveur du jeu sont hébergés sur des machines virtuelles (VM) qui ont un adressage réseau privé (192.168.x.y). Ces VM ne sont pas directement accessibles depuis l'Internet et nécessitent l'utilisation d'un bastion pour y accéder.

### Communication avec les VM

Pour accéder aux serveurs web hébergés sur les VM, nous utilisons un bastion comme point d'accès. Voici comment accéder aux serveurs web des VM :

1. Accéder au bastion via SSH avec l'adresse IP publique fournie.
2. Utiliser le bastion comme reverse proxy pour accéder aux serveurs web hébergés sur les VM.
3. Pour accéder à un serveur web sur une VM, utilisez l'URL suivante : `https://IP_du_bastion/nom_de_la_vm/` (notez l'utilisation de HTTPS et des barres obliques).
4. La première fois que vous accédez à cette URL, votre navigateur pourrait afficher une alerte de sécurité. Dans Firefox, vous pouvez passer outre en cliquant sur "Avancés", puis "Accepter le risque et poursuivre".

### Choix du Logiciel Serveur

Nous devons choisir un logiciel serveur pour gérer les requêtes HTTP des utilisateurs. Deux options populaires sont Apache et NGINX. Voici une comparaison rapide :

- **Apache** :
  - Architecture basée sur les processus.
  - Nombreux modules complémentaires disponibles.
  - Traite à la fois le contenu statique et dynamique.
  - Grande sécurité avec des astuces de configuration pour la gestion des attaques.

- **NGINX** :
  - Architecture basée sur les évènements.
  - Performances élevées pour le contenu statique.
  - Traite le contenu dynamique au sein du serveur.
  - Sécurité renforcée grâce à un code de base plus fin.

### Structure du Répertoire Git

- **/docs** : Ce dossier contient toute la documentation relative au projet.
- **/src** : Contient le code source du serveur web, séparé par VM si nécessaire.
- **README.md** : Ce fichier que vous êtes en train de lire, fournissant des informations essentielles sur le projet.

### Comment Contribuer

Si vous souhaitez contribuer au projet, veuillez suivre ces étapes :

1. Fork le projet depuis GitHub.
2. Clonez votre fork localement sur votre machine.
3. Créez une branche pour votre fonctionnalité (`git checkout -b feature/nom-de-la-fonctionnalité`).
4. Faites vos modifications.
5. Ajoutez et commitez vos modifications (`git add . && git commit -m "Description de la modification"`).
6. Poussez vos modifications vers votre fork sur GitHub (`git push origin feature/nom-de-la-fonctionnalité`).
7. Créez une Pull Request sur le dépôt d'origine.

### Remarques

- Assurez-vous de respecter les normes de codage définies par l'équipe.
- Toute modification importante doit être discutée avec l'équipe avant d'être implémentée.

---

Ce Readme fournit une vue d'ensemble du projet, des instructions pour contribuer, et des informations sur la communication avec les VM et le choix du logiciel serveur. Pour des informations plus détaillées, veuillez consulter la documentation dans le dossier `/docs`.
