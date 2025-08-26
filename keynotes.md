# Projet 5

---

# **Synthèse scientifique du projet**

## Contexte et objectifs

Le projet s’articule autour de la migration d’un dataset médical fourni par un client de l’entreprise DataSoluTech, spécialisée dans la gestion et l’analyse de données pour l’optimisation opérationnelle et la prise de décision. Confronté à des problèmes de scalabilité, le client requiert une solution **Big Data** moderne, permettant une gestion robuste, évolutive et performante de ses données médicales.

La mission confiée consiste à:

- **Migrer les données** d’un format CSV vers une base **MongoDB**, tirant profit des atouts du NoSQL pour la performance et la scalabilité horizontale.
- **Automatiser** et documenter le processus de migration via un script, géré comme un projet logiciel moderne (utilisation de GitHub, README détaillé, fichier requirements.txt, etc.).
- **Conteneuriser** l’ensemble de l’application (MongoDB et scripts de migration) avec **Docker** afin d’assurer portabilité, reproductibilité et scalabilité.
- **Explorer le déploiement Cloud** sur AWS, en documentant les solutions Amazon S3, Amazon RDS pour MongoDB, Amazon DocumentDB, Amazon ECS.
- **Livrer une documentation scientifique et technique complète** et une présentation structurée présentant le contexte, la démarche, les choix réalisés et les résultats obtenus.

## Enjeux techniques

- Compréhension et maîtrise des bases de données **NoSQL**, et plus particulièrement de MongoDB : modélisation des documents, collections, manipulation CRUD, gestion des types, indexation.
- Maîtrise du workflow **Docker/Docker Compose** : création de conteneurs, orchestration, gestion de volumes de données.
- Validation et qualité des données (tests d’intégrité, gestion des erreurs, automatisation des processus de test).
- Sensibilisation aux **pratiques DevOps** (versioning, documentation, automatisation).
- Découverte des architectures Cloud AWS pertinentes pour MongoDB, illustrant les avantages du cloud pour la gestion scalable et sécurisée des données.

# Plan d’action proposé

## 1. Prise de connaissance et cadrage

- Lire consciencieusement le cahier des charges et les ressources pédagogiques fournies.
- Prendre note des livrables attendus et des critères d’évaluation (techniques et de soutenance).
- Analyser en détail le dataset à migrer (structure, types, qualité).

## 2. Maîtrise des fondamentaux techniques

- Approfondir le fonctionnement de MongoDB, ses concepts clés (documents, collections, index, schéma).
- Réviser les bases de Docker (conteneurs, images, Dockerfile, docker-compose).
- Prendre en main l’environnement de développement (installation locale de MongoDB, Docker, Git).

## 3. Développement de la migration de données

- Définir le schéma MongoDB adéquat pour les données.
- Rédiger le script de migration du CSV vers MongoDB :
    - Test de qualité des données (duplications, valeurs manquantes, cohérence des types).
    - Automatisation des tests avant/après migration.
- Produire la documentation associée (README, explanations sur le schéma, gestion des rôles utilisateurs et authentification).

## 4. Conteneurisation et orchestration

- Conteneuriser MongoDB et le script de migration par Docker/Docker Compose.
- Gérer les volumes nécessaires pour le stockage des données sources et du serveur MongoDB.
- Valider la portabilité de l’ensemble (tests de déploiement dans différents environnements).

## 5. Exploration cloud AWS

- Étudier la documentation, relever les possibilités d’hébergement MongoDB sur AWS (Amazon S3, RDS, DocumentDB, ECS).
- Documenter les avantages, la tarification et la mise en œuvre pour le client.

## 6. Production et formalisation des livrables

- Rédiger toute la documentation nécessaire et un journal de bord des étapes et choix.
- Élaborer la présentation (support PPT) synthétisant le contexte, la démarche, la solution technique et les justifications de choix.
- Préparer la démonstration pour la soutenance.

## 7. Validation et itération

- Auto-évaluation à partir de la grille donnée.
- Demander un retour/avis du mentor, puis ajuster et finaliser les livrables.

Ce plan garantit une progression structurée et exhaustive, compatible avec les attentes professionnelles et académiques du projet.CopiesWebduProjet.pdf

# Présentation des différents types de NoSQL

[https://openclassrooms.com/fr/courses/8587446-utilisez-les-bases-de-donnees-nosql/8637550-choisissez-votre-base-de-donnees-nosql](https://openclassrooms.com/fr/courses/8587446-utilisez-les-bases-de-donnees-nosql/8637550-choisissez-votre-base-de-donnees-nosql)

Les bases de données NoSQL ("Not Only SQL") regroupent une diversité de technologies alternatives au modèle relationnel classique. Elles sont optimisées pour la gestion de grands volumes de données, généralement non structurées ou semi-structurées, et s’adaptent particulièrement aux besoins de scalabilité et de flexibilité des architectures modernes, notamment dans les environnements Big Data et Cloud.[microsoft+2](https://azure.microsoft.com/fr-fr/resources/cloud-computing-dictionary/what-is-nosql-database)

On distingue quatre grands types de bases NoSQL, chacune adaptée à des besoins spécifiques :[datascientest+4](https://datascientest.com/nosql-tout-savoir)

## 1. **Bases clé-valeur (Key-Value Stores)**

- **Principe** : les données sont stockées sous forme de paires clé/valeur. Chaque clé unique permet d’accéder facilement à sa valeur associée, qui peut être n'importe quel type de donnée (texte, nombre, objet binaire, etc.).
- **Exemples** : Redis, Amazon DynamoDB, Riak.
- **Spécificités** :
    - Extrêmement performantes pour des accès simples, rapides et massifs.
    - Modèle très simple, ne nécessitant pas de schéma prédéfini.
    - Faible granularité des requêtes (pas de jointures ou requêtes complexes).
- **Cas d’utilisation** :
    - Gestion de sessions utilisateurs et caches.
    - Stockage des profils, logs, ou toute donnée par nature peu structurée.
    - Applications nécessitant de la haute disponibilité et des temps de réponse faibles.[mongodb+2](https://www.mongodb.com/fr-fr/resources/basics/databases/nosql-explained)

## 2. **Bases orientées colonnes (Column-Family Stores)**

- **Principe** : extension des bases relationnelles ; chaque colonne peut être traitée indépendamment et les données d’une même colonne sont stockées ensemble, facilitant l'accès massif à certains champs.
- **Exemples** : Apache Cassandra, HBase, Google BigTable.
- **Spécificités** :
    - Optimisées pour le stockage et la consultation de larges volumes de données réparties sur plusieurs serveurs.
    - Très adaptées à des traitements analytiques et aux charges de type "Big Data" (exemple : systèmes OLAP).
- **Cas d’utilisation** :
    - Applications analytiques et de reporting où l’on manipule des milliers/millions d’enregistrements sur quelques colonnes.
    - Stockage de grandes historiques, de données de capteurs ou de logs.[data-bird+2](https://www.data-bird.co/blog/nosql)

## 3. **Bases orientées documents (Document Stores)**

- **Principe** : stockent les données sous forme de documents (ex. JSON, BSON), qui regroupent des données structurées, imbriquées, et variables en champs.
- **Exemples** : MongoDB, CouchDB, Couchbase.
- **Spécificités** :
    - Modèle flexible, proche des structures de données manipulées par les développeurs.
    - Supporte des requêtes riches sur le contenu des documents, avec indexation avancée.
    - Favorise la modularité et l’évolutivité du schéma.[mongodb](https://www.mongodb.com/fr-fr/resources/basics/databases/nosql-explained)
- **Cas d’utilisation** :
    - Applications web, CMS, catalogues produits, gestion de contenus ou profils utilisateurs.
    - Cas où les structures de données évoluent fréquemment ou sont hétérogènes.[microsoft+3](https://azure.microsoft.com/fr-fr/resources/cloud-computing-dictionary/what-is-nosql-database)

## 4. **Bases orientées graphes (Graph Databases)**

- **Principe** : conçues pour gérer et interroger des données organisées en graphes (nœuds, arêtes, propriétés).
- **Exemples** : Neo4j, JanusGraph, Amazon Neptune.
- **Spécificités** :
    - Excellentes pour modéliser des réseaux complexes (relations, parcours, dépendances).
    - Optimisent le stockage et la requête de relations multiples et évolutives entre entités.
- **Cas d’utilisation** :
    - Recommandations (amis, produits), moteurs sociaux, cartographie de relations, détection de fraudes.
    - Recherche de plus courts chemins ou calculs de proximité au sein de réseaux.[astera+2](https://www.astera.com/fr/knowledge-center/sql-vs-nosql/)

---

## Table Récapitulative des types NoSQL

| Type | Exemple(s) | Spécificités principales | Cas d'utilisation privilégiés |
| --- | --- | --- | --- |
| Clé-Valeur | Redis, DynamoDB | Simplicité, rapidité, schéma abs. | Cache, session, IoT, logs |
| Orienté Colonnes | Cassandra, HBase | Scalabilité, requêtes analytiques massives | Big Data, reporting, séries temporelles |
| Orienté Document | MongoDB, CouchDB | Souplesse du schéma, requêtes riches, évolutif | Applications web, contenus, catalogues |
| Orienté Graphe | Neo4j, Amazon Neptune | Modélisation de réseaux, requêtes relationnelles | Réseaux sociaux, recommandations, fraude |

---

## Spécificités générales des bases NoSQL

- **Schéma flexible** : pas de contrainte forte de structure, adaptation facile à l’évolution du modèle de données.
- **Scalabilité horizontale** : gestion des volumes par distribution automatique des données (sharding).
- **Performance** : optimisées pour les opérations massives, le temps réel, ou la tolérance aux pannes.
- **Inconvénients** : absence du modèle ACID strict de la majorité des SGBDR, jeunes technologies, écosystèmes parfois moins matures pour certains usages industriels.[cloud.google+2](https://cloud.google.com/discover/what-is-nosql?hl=fr)

---

## Conclusion

Le choix du type de base NoSQL dépend toujours du **cas d’usage réel** et de la nature des données à gérer. Les bases NoSQL offrent polyvalence, performance et scalabilité, mais nécessitent une analyse approfondie pour choisir la technologie la mieux adaptée à la problématique rencontrée.[datascientest+3](https://datascientest.com/nosql-tout-savoir)

1. [https://azure.microsoft.com/fr-fr/resources/cloud-computing-dictionary/what-is-nosql-database](https://azure.microsoft.com/fr-fr/resources/cloud-computing-dictionary/what-is-nosql-database)
2. [https://datascientest.com/nosql-tout-savoir](https://datascientest.com/nosql-tout-savoir)
3. [https://cloud.google.com/discover/what-is-nosql?hl=fr](https://cloud.google.com/discover/what-is-nosql?hl=fr)
4. [https://www.oracle.com/fr/database/nosql/what-is-nosql/](https://www.oracle.com/fr/database/nosql/what-is-nosql/)
5. [https://www.mongodb.com/fr-fr/resources/basics/databases/nosql-explained](https://www.mongodb.com/fr-fr/resources/basics/databases/nosql-explained)
6. [https://www.data-bird.co/blog/nosql](https://www.data-bird.co/blog/nosql)
7. [https://www.astera.com/fr/knowledge-center/sql-vs-nosql/](https://www.astera.com/fr/knowledge-center/sql-vs-nosql/)
8. [https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_dba37358-f03b-40a8-8d10-3c05b359efe6/b4cac9e2-3222-44e6-a768-4d94148ae0c5/CopiesWebduProjet.pdf](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_dba37358-f03b-40a8-8d10-3c05b359efe6/b4cac9e2-3222-44e6-a768-4d94148ae0c5/CopiesWebduProjet.pdf)
9. [https://fr.wikipedia.org/wiki/NoSQL](https://fr.wikipedia.org/wiki/NoSQL)
10. [https://www.intersystems.com/fr/--archived--ressources/les-bases-de-donnees-nosql-expliquees-avantages-types-et-cas-dutilisation/](https://www.intersystems.com/fr/--archived--ressources/les-bases-de-donnees-nosql-expliquees-avantages-types-et-cas-dutilisation/)
11. [https://blent.ai/blog/a/nosql-definitions-exemples](https://blent.ai/blog/a/nosql-definitions-exemples)
12. [https://www.jedha.co/formation-analyse-donnee/base-donnees-nosql](https://www.jedha.co/formation-analyse-donnee/base-donnees-nosql)
13. [https://cours.ebsi.umontreal.ca/sci6005/co/sgbd_modele_nosql.html](https://cours.ebsi.umontreal.ca/sci6005/co/sgbd_modele_nosql.html)
14. [https://www.nexa.fr/post/nosql-tout-comprendre-sur-cette-database-non-relationnelle](https://www.nexa.fr/post/nosql-tout-comprendre-sur-cette-database-non-relationnelle)
- Synthèse scientifique du projet
    
    ## Contexte et objectifs
    
    Le projet s’articule autour de la migration d’un dataset médical fourni par un client de l’entreprise DataSoluTech, spécialisée dans la gestion et l’analyse de données pour l’optimisation opérationnelle et la prise de décision. Confronté à des problèmes de scalabilité, le client requiert une solution **Big Data** moderne, permettant une gestion robuste, évolutive et performante de ses données médicales.
    
    La mission confiée consiste à:
    
    - **Migrer les données** d’un format CSV vers une base **MongoDB**, tirant profit des atouts du NoSQL pour la performance et la scalabilité horizontale.
    - **Automatiser** et documenter le processus de migration via un script, géré comme un projet logiciel moderne (utilisation de GitHub, README détaillé, fichier requirements.txt, etc.).
    - **Conteneuriser** l’ensemble de l’application (MongoDB et scripts de migration) avec **Docker** afin d’assurer portabilité, reproductibilité et scalabilité.
    - **Explorer le déploiement Cloud** sur AWS, en documentant les solutions Amazon S3, Amazon RDS pour MongoDB, Amazon DocumentDB, Amazon ECS.
    - **Livrer une documentation scientifique et technique complète** et une présentation structurée présentant le contexte, la démarche, les choix réalisés et les résultats obtenus.
    
    ## Enjeux techniques
    
    - Compréhension et maîtrise des bases de données **NoSQL**, et plus particulièrement de MongoDB : modélisation des documents, collections, manipulation CRUD, gestion des types, indexation.
    - Maîtrise du workflow **Docker/Docker Compose** : création de conteneurs, orchestration, gestion de volumes de données.
    - Validation et qualité des données (tests d’intégrité, gestion des erreurs, automatisation des processus de test).
    - Sensibilisation aux **pratiques DevOps** (versioning, documentation, automatisation).
    - Découverte des architectures Cloud AWS pertinentes pour MongoDB, illustrant les avantages du cloud pour la gestion scalable et sécurisée des données.
    
    ## Plan d’action proposé
    
    ## 1. Prise de connaissance et cadrage
    
    - Lire consciencieusement le cahier des charges et les ressources pédagogiques fournies.
    - Prendre note des livrables attendus et des critères d’évaluation (techniques et de soutenance).
    - Analyser en détail le dataset à migrer (structure, types, qualité).
    
    ## 2. Maîtrise des fondamentaux techniques
    
    - Approfondir le fonctionnement de MongoDB, ses concepts clés (documents, collections, index, schéma).
    - Réviser les bases de Docker (conteneurs, images, Dockerfile, docker-compose).
    - Prendre en main l’environnement de développement (installation locale de MongoDB, Docker, Git).
    
    ## 3. Développement de la migration de données
    
    - Définir le schéma MongoDB adéquat pour les données.
    - Rédiger le script de migration du CSV vers MongoDB :
        - Test de qualité des données (duplications, valeurs manquantes, cohérence des types).
        - Automatisation des tests avant/après migration.
    - Produire la documentation associée (README, explanations sur le schéma, gestion des rôles utilisateurs et authentification).
    
    ## 4. Conteneurisation et orchestration
    
    - Conteneuriser MongoDB et le script de migration par Docker/Docker Compose.
    - Gérer les volumes nécessaires pour le stockage des données sources et du serveur MongoDB.
    - Valider la portabilité de l’ensemble (tests de déploiement dans différents environnements).
    
    ## 5. Exploration cloud AWS
    
    - Étudier la documentation, relever les possibilités d’hébergement MongoDB sur AWS (Amazon S3, RDS, DocumentDB, ECS).
    - Documenter les avantages, la tarification et la mise en œuvre pour le client.
    
    ## 6. Production et formalisation des livrables
    
    - Rédiger toute la documentation nécessaire et un journal de bord des étapes et choix.
    - Élaborer la présentation (support PPT) synthétisant le contexte, la démarche, la solution technique et les justifications de choix.
    - Préparer la démonstration pour la soutenance.
    
    ## 7. Validation et itération
    
    - Auto-évaluation à partir de la grille donnée.
    - Demander un retour/avis du mentor, puis ajuster et finaliser les livrables.
    
    Ce plan garantit une progression structurée et exhaustive, compatible avec les attentes professionnelles et académiques du projet.CopiesWebduProjet.pdf
    
    1. [https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_dba37358-f03b-40a8-8d10-3c05b359efe6/b4cac9e2-3222-44e6-a768-4d94148ae0c5/CopiesWebduProjet.pdf](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_dba37358-f03b-40a8-8d10-3c05b359efe6/b4cac9e2-3222-44e6-a768-4d94148ae0c5/CopiesWebduProjet.pdf)

# Choix de MongoDB

L’examen du dataset « healthcare_dataset.csv » révèle une structure composée d’enregistrements patient comprenant de nombreuses colonnes hétérogènes : informations démographiques, médicales, administratives et financières. Chaque enregistrement regroupe l’ensemble des informations pour un patient ou une admission : identifiants, pathologies, dates, traitements, résultats de tests, etc.healthcare_dataset.csv

Cette organisation répond à des caractéristiques typiques :

- **Données semi-structurées** : chaque ligne correspond à un « document » contenant des attributs variés, parfois absents ou optionnels suivant le patient.
- **Structure évolutive possible** : certains champs peuvent être ajoutés/supprimés selon l’évolution des besoins, des pratiques médicales ou réglementaires.
- **Niveau de granularité : Document** : chaque entrée représente une entité unifiée, manipulable indépendamment (enregistrement patient/admission).

Compte tenu de ces éléments :

- **Le type de NoSQL à privilégier est la base orientée documents (Document Store)**, comme MongoDB.
    - **Justification scientifique** : Ce modèle permet de stocker chaque dossier patient sous forme d’un document unique (par exemple, en JSON), d’intégrer facilement des champs additionnels ou optionnels, de répondre à des exigences de scalabilité horizontale, de requêter efficacement via indexation avancée, et de supporter des évolutions fréquentes du schéma sans migration complexe.CopiesWebduProjet.pdf+1
    - **Avantages concrets** : Les requêtes typiques (filtrage multicritère, agrégation, recherche par champs) sont nativement supportées. L’approche documentaire permet une gestion et un accès direct aux dossiers patients, tout en s’adaptant aux exigences réglementaires (traçabilité, modularité).

En synthèse, **MongoDB** ou toute base de type Document Store est la technologie NoSQL la mieux adaptée pour la migration de ce dataset, car elle conjugue évolutivité, souplesse d’intégration et performance pour des données de santé structurées par dossier.CopiesWebduProjet.pdf+1

1. [https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_dba37358-f03b-40a8-8d10-3c05b359efe6/d2e47c32-8cfa-44e8-a66a-1b34b7cd9dc2/healthcare_dataset.csv](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_dba37358-f03b-40a8-8d10-3c05b359efe6/d2e47c32-8cfa-44e8-a66a-1b34b7cd9dc2/healthcare_dataset.csv)
2. [https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_dba37358-f03b-40a8-8d10-3c05b359efe6/af21f2ce-4541-4187-9e0f-d2913083c511/CopiesWebduProjet.pdf](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_dba37358-f03b-40a8-8d10-3c05b359efe6/af21f2ce-4541-4187-9e0f-d2913083c511/CopiesWebduProjet.pdf)

# La scalabilité MongoDB

## Analyse scientifique  :

## La scalabilité MongoDB : principes et avantages techniques

## **Scalabilité horizontale native**

MongoDB est conçu dès l'origine pour la **scalabilité horizontale** (scale-out), contrairement aux bases SQL traditionnelles qui privilégient la scalabilité verticale (scale-up).[welovedevs+2](https://welovedevs.com/fr/articles/mongo-shard/)

**Mécanisme fondamental** :

- Au lieu d'augmenter la puissance d'un seul serveur (CPU, RAM, stockage), MongoDB distribue automatiquement les données sur plusieurs serveurs appelés **shards**[mongodb+1](https://www.mongodb.com/docs/manual/core/sharding-scaling-strategies/)
- Chaque shard peut être ajouté dynamiquement au cluster sans interruption de service[mongodb+1](https://www.mongodb.com/blog/post/top-4-reasons-to-use-mongodb-8-0-fr)
- Cette approche permet théoriquement une **évolutivité quasi-illimitée** en ajoutant simplement de nouveaux nœuds[stph.scenari-community+1](https://stph.scenari-community.org/contribs/nos/Mongo2/co/activiteapprentissage_3.html)

## **Architecture de sharding avancée**

**Composants clés du sharding MongoDB** :

1. **Shards** : serveurs contenant des partitions des données[programmevitam+1](https://www.programmevitam.fr/ressources/Doc1.10.0/html/archi/archi-exploit-infra/services/mongodb.html)
2. **Config Servers** : stockent les métadonnées de distribution[easyteam+1](https://easyteam.fr/actualites/deployer-une-architecture-mongodb-en-sharding/)
3. **Routeurs (mongos)** : dirigent les requêtes vers les shards appropriés[programmevitam](https://www.programmevitam.fr/ressources/Doc1.10.0/html/archi/archi-exploit-infra/services/mongodb.html)

**Avantages techniques** :

- **Distribution automatique** : MongoDB répartit les données équitablement selon la clé de sharding choisie[welovedevs+1](https://welovedevs.com/fr/articles/mongo-shard/)
- **Parallélisation des requêtes** : chaque shard traite simultanément une portion de la requête[astera](https://www.astera.com/fr/type/blog/mongodb-vs-sql-server/)
- **Performance linéaire** : l'ajout de shards améliore proportionnellement les performances[mongodb](https://www.mongodb.com/blog/post/top-4-reasons-to-use-mongodb-8-0-fr)

## **Haute disponibilité par réplication**

MongoDB intègre un système de **Replica Sets** pour garantir la continuité de service:[octo+2](https://blog.octo.com/exemple-dinfrastructure-mongobd-haute-disponibilite-en-lecture)

**Mécanismes** :

- **Réplication synchrone** : les données sont automatiquement copiées sur plusieurs nœuds[mongoteam.gitbooks+1](https://mongoteam.gitbooks.io/introduction-a-mongodb/01-presentation/replication.html)
- **Élection automatique** : en cas de panne du nœud primaire, un secondaire prend le relais sans intervention[octo+1](https://blog.octo.com/exemple-dinfrastructure-mongobd-haute-disponibilite-en-lecture)
- **Réplication continue** : depuis MongoDB 4.4, les changements sont propagés en temps réel[kinsta](https://kinsta.com/fr/blog/ensemble-repliques-mongodb/)

## **Performances optimisées**

**Avantages structurels** :

- **Stockage en mémoire** : MongoDB peut conserver jusqu'à 10 Go en mémoire pour des accès ultra-rapides[astera](https://www.astera.com/fr/type/blog/mongodb-vs-sql-server/)
- **Modèle dénormalisé** : les données liées sont stockées ensemble, évitant les jointures coûteuses[aws.amazon+1](https://aws.amazon.com/fr/compare/the-difference-between-mongodb-vs-mysql/)
- **Index adaptatifs** : création d'index optimisés pour les requêtes NoSQL[blogdunumerique](https://blogdunumerique.com/les-avantages-et-les-inconvenients-des-bases-de-donnees-nosql-mongodb-vs-cassandra-vs-couchbase/)

**Gains de performance mesurés** :

- MongoDB 8.0 offre des performances **30% supérieures** aux versions précédentes[mongodb](https://www.mongodb.com/blog/post/top-4-reasons-to-use-mongodb-8-0-fr)
- Débit d'écriture amélioré de **56%** pour les opérations en masse[mongodb](https://www.mongodb.com/blog/post/top-4-reasons-to-use-mongodb-8-0-fr)
- Opérations sur séries temporelles **200% plus rapides**[mongodb](https://www.mongodb.com/blog/post/top-4-reasons-to-use-mongodb-8-0-fr)

## **Comparaison scalabilité SQL vs NoSQL**

| Critère | SQL (Relationnel) | NoSQL (MongoDB) |
| --- | --- | --- |
| **Type de scalabilité** | Verticale principalement[wildcodeschool+1](https://www.wildcodeschool.com/blog/sql-vs-nosql-quelles-diff%C3%A9rences) | Horizontale native[wildcodeschool+1](https://www.wildcodeschool.com/blog/sql-vs-nosql-quelles-diff%C3%A9rences) |
| **Ajout de capacité** | Mise à niveau matériel coûteuse[welovedevs+1](https://welovedevs.com/fr/articles/mongo-shard/) | Ajout de serveurs standard[coursera+1](https://www.coursera.org/fr-FR/articles/nosql-vs-sql) |
| **Distribution des données** | Complexe, nécessite sharding manuel[reddit](https://www.reddit.com/r/Database/comments/nma3si/sql_and_nosql_scalability/) | Automatique et transparente[welovedevs+1](https://welovedevs.com/fr/articles/mongo-shard/) |
| **Tolérance aux pannes** | Point de défaillance unique[datastax](https://www.datastax.com/fr/blog/sql-vs-nosql-pros-cons) | Réplication distribuée[datastax+1](https://www.datastax.com/fr/blog/sql-vs-nosql-pros-cons) |
| **Coût d'évolution** | Exponentiel avec la taille[welovedevs+1](https://welovedevs.com/fr/articles/mongo-shard/) | Linéaire par ajout de nœuds[datastax+1](https://www.datastax.com/fr/blog/sql-vs-nosql-pros-cons) |

## **Cas d'usage optimaux pour la scalabilité MongoDB**

**Scénarios privilégiés** :

- **Big Data** : volumes de données massifs et croissance rapide[coursera+2](https://www.coursera.org/fr-FR/articles/nosql-vs-sql)
- **Applications temps réel** : forte charge simultanée (IoT, réseaux sociaux)[wildcodeschool+1](https://www.wildcodeschool.com/blog/sql-vs-nosql-quelles-diff%C3%A9rences)
- **Architecture cloud** : déploiement distribué multi-régions[datastax+1](https://www.datastax.com/fr/blog/sql-vs-nosql-pros-cons)
- **Données semi-structurées** : flexibilité du schéma pour évolution rapide[wildcodeschool+1](https://www.wildcodeschool.com/blog/sql-vs-nosql-quelles-diff%C3%A9rences)

## **Limitations à considérer**

**Trade-offs de la scalabilité horizontale** :

- **Complexité operationnelle** : gestion d'un cluster distribué[ibm+1](https://www.ibm.com/fr-fr/think/topics/nosql-databases)
- **Cohérence éventuelle** : abandon partiel des propriétés ACID strictes[reddit+1](https://www.reddit.com/r/Database/comments/nma3si/sql_and_nosql_scalability/)
- **Coût en ressources** : réplication et distribution consomment de la bande passante[astera](https://www.astera.com/fr/type/blog/mongodb-vs-sql-server/)

---

## Synthèse scientifique

MongoDB apporte une **scalabilité supérieure** grâce à son architecture distribuée native qui permet :

1. **Évolutivité élastique** : ajout transparent de capacité sans interruption
2. **Performance linéaire** : amélioration proportionnelle avec l'ajout de ressources
3. **Résilience élevée** : tolérance aux pannes par redondance automatique
4. **Économies d'échelle** : coût d'infrastructure optimisé vs scalabilité verticale

Cette approche architecturale fait de MongoDB une solution particulièrement adaptée aux environnements nécessitant une **croissance rapide et imprévisible des données**.[edata-warehouse+3](https://www.edata-warehouse.com/mongodb-vs-sql/)

1. [https://welovedevs.com/fr/articles/mongo-shard/](https://welovedevs.com/fr/articles/mongo-shard/)
2. [https://www.mongodb.com/docs/manual/core/sharding-scaling-strategies/](https://www.mongodb.com/docs/manual/core/sharding-scaling-strategies/)
3. [https://easyteam.fr/actualites/deployer-une-architecture-mongodb-en-sharding/](https://easyteam.fr/actualites/deployer-une-architecture-mongodb-en-sharding/)
4. [https://www.mongodb.com/blog/post/top-4-reasons-to-use-mongodb-8-0-fr](https://www.mongodb.com/blog/post/top-4-reasons-to-use-mongodb-8-0-fr)
5. [https://stph.scenari-community.org/contribs/nos/Mongo2/co/activiteapprentissage_3.html](https://stph.scenari-community.org/contribs/nos/Mongo2/co/activiteapprentissage_3.html)
6. [https://odeven.fr/les-secrets-de-la-scalabilite-3-les-performances-et-loptimisation/](https://odeven.fr/les-secrets-de-la-scalabilite-3-les-performances-et-loptimisation/)
7. [https://www.programmevitam.fr/ressources/Doc1.10.0/html/archi/archi-exploit-infra/services/mongodb.html](https://www.programmevitam.fr/ressources/Doc1.10.0/html/archi/archi-exploit-infra/services/mongodb.html)
8. [https://www.astera.com/fr/type/blog/mongodb-vs-sql-server/](https://www.astera.com/fr/type/blog/mongodb-vs-sql-server/)
9. [https://blog.octo.com/exemple-dinfrastructure-mongobd-haute-disponibilite-en-lecture](https://blog.octo.com/exemple-dinfrastructure-mongobd-haute-disponibilite-en-lecture)
10. [https://mongoteam.gitbooks.io/introduction-a-mongodb/01-presentation/replication.html](https://mongoteam.gitbooks.io/introduction-a-mongodb/01-presentation/replication.html)
11. [https://kinsta.com/fr/blog/ensemble-repliques-mongodb/](https://kinsta.com/fr/blog/ensemble-repliques-mongodb/)
12. [https://learn.microsoft.com/fr-fr/azure/cosmos-db/mongodb/vcore/high-availability](https://learn.microsoft.com/fr-fr/azure/cosmos-db/mongodb/vcore/high-availability)
13. [https://aws.amazon.com/fr/compare/the-difference-between-mongodb-vs-mysql/](https://aws.amazon.com/fr/compare/the-difference-between-mongodb-vs-mysql/)
14. [https://blogdunumerique.com/les-avantages-et-les-inconvenients-des-bases-de-donnees-nosql-mongodb-vs-cassandra-vs-couchbase/](https://blogdunumerique.com/les-avantages-et-les-inconvenients-des-bases-de-donnees-nosql-mongodb-vs-cassandra-vs-couchbase/)
15. [https://www.wildcodeschool.com/blog/sql-vs-nosql-quelles-diff%C3%A9rences](https://www.wildcodeschool.com/blog/sql-vs-nosql-quelles-diff%C3%A9rences)
16. [https://www.coursera.org/fr-FR/articles/nosql-vs-sql](https://www.coursera.org/fr-FR/articles/nosql-vs-sql)
17. [https://www.datastax.com/fr/blog/sql-vs-nosql-pros-cons](https://www.datastax.com/fr/blog/sql-vs-nosql-pros-cons)
18. [https://www.reddit.com/r/Database/comments/nma3si/sql_and_nosql_scalability/](https://www.reddit.com/r/Database/comments/nma3si/sql_and_nosql_scalability/)
19. [https://www.reddit.com/r/Database/comments/1cc4zdr/what_advantages_do_nosql_databases_have_over/?tl=fr](https://www.reddit.com/r/Database/comments/1cc4zdr/what_advantages_do_nosql_databases_have_over/?tl=fr)
20. [https://www.edata-warehouse.com/mongodb-vs-sql/](https://www.edata-warehouse.com/mongodb-vs-sql/)
21. [https://www.industrie-numerique.com/nosql-en-2024-panorama-des-bases-de-donnees/](https://www.industrie-numerique.com/nosql-en-2024-panorama-des-bases-de-donnees/)
22. [https://www.ibm.com/fr-fr/think/topics/nosql-databases](https://www.ibm.com/fr-fr/think/topics/nosql-databases)
23. [https://fr.slideshare.net/slideshow/scalabilit-de-mongodb/41766032](https://fr.slideshare.net/slideshow/scalabilit-de-mongodb/41766032)
24. [https://www.mongodb.com/fr-fr/resources/compare/mongodb-mysql](https://www.mongodb.com/fr-fr/resources/compare/mongodb-mysql)
25. [https://www.ionos.fr/digitalguide/serveur/know-how/mongodb-vs-sql/](https://www.ionos.fr/digitalguide/serveur/know-how/mongodb-vs-sql/)
26. [https://blog.logto.io/fr/postgresql-vs-mongodb](https://blog.logto.io/fr/postgresql-vs-mongodb)

## Dans le projet

La mise en place de **routeurs (mongos)** et de **shards** dans MongoDB est une fonctionnalité clé pour assurer la scalabilité horizontale sur des volumes de données très importants ou des charges d’accès très élevées.

---

## Évaluation selon le contexte du projet

## 1. Besoins de scalabilité du projet actuel

- Le projet porte sur un dataset médical dont la taille reste **modérée à moyenne** et vise une première migration et démonstration fonctionnelle.
- Les consignes mettent l’accent sur la maîtrise locale, conteneurisation Docker et exploitation directe de MongoDB.
- L’usage d’un cluster sharded avec routeurs complexifie la gestion, la configuration et la maintenance.
- La scalabilité classique d’un replica set MongoDB (réplication pour haute disponibilité) est généralement suffisante pour ce niveau de volume et de charge.

## 2. Quand envisager routeurs et shards ?

- Quand les données dépassent la capacité d’un seul serveur (taille > plusieurs TB).
- Quand la charge d’écriture et de lecture ne peut plus être assurée par un seul nœud.
- Pour une distribution géographique des données sur plusieurs datacenters.
- Pour des environnements de production à très grande échelle et haute performance.

## 3. Recommandation pour ce projet

- Installer un **Replica Set** MongoDB pour garantir la haute disponibilité et la résilience (facultatif mais recommandé).
- Rester sur un **déploiement simple avec un seul serveur MongoDB**, conteneurisé via Docker, dans un premier temps.
- Ne pas mettre en place de sharding ni routeurs (mongos) à ce stade, car cela ajoute une complexité significative non justifiée par le volume ni par les besoins exprimés.

---

## Conclusion

Pour ce projet, la mise en place de **routeurs et shards n’est pas nécessaire**, à moins d’une croissance future très importante et imprévisible des données.

Dans la phase actuelle, privilégier la simplicité, la robustesse et la portabilité de l’architecture MongoDB locale (voire Replica Set pour haute disponibilité), puis envisager un cluster sharded ultérieurement en fonction de l’évolution des besoins.[mongodb+2](https://www.mongodb.com/docs/manual/core/sharding-scaling-strategies/)

1. [https://www.mongodb.com/docs/manual/core/sharding-scaling-strategies/](https://www.mongodb.com/docs/manual/core/sharding-scaling-strategies/)
2. [https://stph.scenari-community.org/contribs/nos/Mongo2/co/activiteapprentissage_3.html](https://stph.scenari-community.org/contribs/nos/Mongo2/co/activiteapprentissage_3.html)
3. [https://easyteam.fr/actualites/deployer-une-architecture-mongodb-en-sharding/](https://easyteam.fr/actualites/deployer-une-architecture-mongodb-en-sharding/)

# Déroulé script ETL

Voici le **déroulement concret détaillé** de la migration du dataset healthcare CSV vers MongoDB :

## Déroulement concret pour le traitement du dataset

## **Étape 1 : Analyse structurelle du dataset**

Le dataset contient **15 colonnes** réparties en 4 catégories logiques :

- **Identification Patient** (4 colonnes) : Name, Age, Gender, Blood Type
- **Données Médicales** (3 colonnes) : Medical Condition, Medication, Test Results
- **Données Administratives** (6 colonnes) : Date of Admission, Discharge Date, Doctor, Hospital, Room Number, Admission Type
- **Données Financières** (2 colonnes) : Insurance Provider, Billing Amount

**Problèmes identifiés à traiter** :

1. Capitalisation incohérente dans les noms (ex: "emIly CObb")
2. Formats de dates à standardiser
3. Précision excessive des montants (ex: 47333.98046509043210)
4. Variations de casse dans les champs texte

## **Étape 2 : Script de nettoyage des données**

Création d'une fonction `clean_healthcare_data()` pour :

- Normaliser la capitalisation (`.str.title()`)
- Convertir les dates avec `pd.to_datetime()`
- Arrondir les montants à 2 décimales
- Standardiser les types sanguins en majuscules
- Convertir les types numériques (Age, Room Number)

## **Étape 3 : Modélisation orientée document**

**Transformation de la structure tabulaire** en **documents JSON imbriqués** :

- Regroupement logique des champs en sous-documents (`patient_info`, `medical_info`, `admission_info`, `billing_info`)
- Ajout de métadonnées (`created_at`, `source`) pour traçabilité
- Structure flexible permettant l'évolution du schéma

## **Étape 4 : Transformation ligne par ligne**

Script `transform_to_mongodb_documents()` qui :

- Itère sur chaque ligne du DataFrame nettoyé
- Crée un dictionnaire Python structuré pour chaque patient
- Convertit les types appropriés (int, float, datetime)
- Génère une liste de documents prêts pour MongoDB

## **Étape 5 : Insertion batch dans MongoDB**

Utilisation de `pymongo` pour :

- Établir la connexion (`MongoClient`)
- Insérer en batch avec `insert_many()` pour optimiser les performances
- Gérer les erreurs et vérifier le nombre d'insertions
- Fermer proprement la connexion

## **Étape 6 : Optimisation par indexation**

Création d'index sur les champs fréquemment interrogés :

- `patient_info.name` (recherche par nom)
- `medical_info.condition` (filtrage par pathologie)
- `admission_info.admission_date` (requêtes temporelles)
- `admission_info.doctor` (recherche par médecin)
- `billing_info.insurance_provider` (filtrage par assurance)

## **Étape 7 : Validation et tests**

Scripts de validation pour vérifier :

- Le nombre de documents insérés
- La cohérence des données (âges, montants, dates)
- Le bon fonctionnement des requêtes
- Les performances avec les index

**Fichier de référence complet** disponible dans le document généré

migration-healthcare-mongodb.md

Fichier généré

avec tous les scripts Python détaillés et les commandes d'exécution.

Cette méthodologie garantit une **migration robuste, traçable et optimisée** pour un environnement de production, avec gestion d'erreurs et validation systématique à chaque étape.

1. [https://ppl-ai-code-interpreter-files.s3.amazonaws.com/web/direct-files/1766fe915c7dfc7737a36ab350ed640b/3fe43e27-0fc5-49ff-851f-eec9ae540c20/78be95db.md](https://ppl-ai-code-interpreter-files.s3.amazonaws.com/web/direct-files/1766fe915c7dfc7737a36ab350ed640b/3fe43e27-0fc5-49ff-851f-eec9ae540c20/78be95db.md)

# Différence entre docker et machine virtuelle

La différence entre un conteneur Docker et une machine virtuelle (VM) réside principalement dans leur architecture, niveau d'isolation et usage des ressources.

## Architecture et isolation

- Une **machine virtuelle** émule complètement un matériel physique avec son propre système d'exploitation invité (guest OS) fonctionnant au-dessus d'un hyperviseur, ce qui lui confère une isolation forte et la possibilité de faire tourner des systèmes d'exploitation différents de la machine hôte.[aws.amazon+1](https://aws.amazon.com/compare/the-difference-between-docker-vm/)
- Un **conteneur Docker** partage le noyau du système d'exploitation hôte, virtualisant uniquement l'espace utilisateur et les dépendances nécessaires à l'application. Il ne contient pas d'OS complet, ce qui le rend plus léger mais offre une isolation moins complète que la VM.[learn.microsoft+1](https://learn.microsoft.com/en-nz/answers/questions/2109219/how-is-docker-different-from-a-virtual-machine)

## Performance et ressources

- Les VMs nécessitent des ressources préallouées (CPU, mémoire) et un démarrage plus long, car elles lancent un OS complet.
- Les conteneurs Docker sont rapides à démarrer, consomment moins de ressources car ils partagent le noyau avec l'hôte et utilisent les ressources à la demande, ce qui améliore l'efficacité et la densité d'exécution sur une même machine physique.[qa+1](https://www.qa.com/resources/blog/docker-vs-virtual-machines-differences-you-should-know/)

## Sécurité

- Les VMs bénéficient d'une isolation forte grâce à leur OS invité complet, ce qui limite les risques de compromission entre systèmes.
- Les conteneurs, partageant le noyau, peuvent être plus vulnérables à des failles du noyau mais disposent aussi de mécanismes avancés d'isolation comme les namespaces et cgroups pour sécuriser les processus.[aws.amazon+1](https://aws.amazon.com/compare/the-difference-between-docker-vm/)

## Portabilité et cas d'usage

- Les VMs sont utiles pour exécuter plusieurs OS ou environnements isolés sur une même machine physique, souvent dans des contextes nécessitant une forte isolation ou des systèmes différents.
- Docker est adapté à la portabilité des applications dans des environnements homogènes, notamment pour le développement, le test et le déploiement rapide d'applications conteneurisées, et convient particulièrement aux architectures microservices.[qa+1](https://www.qa.com/resources/blog/docker-vs-virtual-machines-differences-you-should-know/)

En résumé, Docker offre une virtualisation légère et rapide au niveau du système d'exploitation pour exécuter des applications isolées, tandis que les machines virtuelles offrent une virtualisation complète d'un matériel et système d'exploitation, au prix d'une consommation de ressources plus élevée et d'une latence au démarrage plus importante.

Références principales :

- AWS comparaison Docker vs VM (2025)[aws.amazon](https://aws.amazon.com/compare/the-difference-between-docker-vm/)
- QA.com comparatif Docker vs VM (2025)[qa](https://www.qa.com/resources/blog/docker-vs-virtual-machines-differences-you-should-know/)
- Microsoft Q&A sur différences architecturales (2024)[learn.microsoft](https://learn.microsoft.com/en-nz/answers/questions/2109219/how-is-docker-different-from-a-virtual-machine)
1. [https://aws.amazon.com/compare/the-difference-between-docker-vm/](https://aws.amazon.com/compare/the-difference-between-docker-vm/)
2. [https://www.qa.com/resources/blog/docker-vs-virtual-machines-differences-you-should-know/](https://www.qa.com/resources/blog/docker-vs-virtual-machines-differences-you-should-know/)
3. [https://learn.microsoft.com/en-nz/answers/questions/2109219/how-is-docker-different-from-a-virtual-machine](https://learn.microsoft.com/en-nz/answers/questions/2109219/how-is-docker-different-from-a-virtual-machine)
4. [https://aws.amazon.com/fr/compare/the-difference-between-docker-vm/](https://aws.amazon.com/fr/compare/the-difference-between-docker-vm/)
5. [https://www.atlassian.com/microservices/cloud-computing/containers-vs-vms](https://www.atlassian.com/microservices/cloud-computing/containers-vs-vms)
6. [https://www.geeksforgeeks.org/devops/difference-between-docker-and-virtualization/](https://www.geeksforgeeks.org/devops/difference-between-docker-and-virtualization/)
7. [https://www.reddit.com/r/learnprogramming/comments/vh2kgn/can_someone_eli5_what_docker_is_and_how_it/](https://www.reddit.com/r/learnprogramming/comments/vh2kgn/can_someone_eli5_what_docker_is_and_how_it/)
8. [https://www.youtube.com/watch?v=a1M_thDTqmU](https://www.youtube.com/watch?v=a1M_thDTqmU)