# Services AWS pour MongoDB : Documentation Complète pour Déploiement Cloud

## Introduction : Contexte du Passage au Cloud

Le passage vers l'infrastructure cloud représente une transformation majeure pour les organisations gérant des bases de données MongoDB. Cette transition s'inscrit dans une stratégie de modernisation visant à améliorer la scalabilité horizontale, réduire les coûts opérationnels et augmenter la disponibilité des systèmes de gestion de données médicales.

### Avantages Fondamentaux du Cloud AWS

**Scalabilité et Élasticité** : AWS permet une mise à l'échelle automatique des ressources en fonction de la demande, offrant une capacité de stockage virtuellement illimitée avec S3  et une architecture élastique capable de gérer des exaoctets de données sans nécessiter d'investissements matériels préalables.[1][2]

**Durabilité et Disponibilité** : L'infrastructure AWS garantit une durabilité de 99,999999999% (11 neufs) pour le stockage S3 avec réplication automatique sur au moins 3 zones de disponibilité , assurant une continuité de service critique pour les données médicales sensibles.[1]

**Modèle Économique Optimisé** : L'approche "pay-as-you-go" permet de réduire considérablement les coûts d'infrastructure, particulièrement pour les entreprises avec des charges de travail variables. Les tarifs S3 débutent à environ 3 cents par Go avec des réductions progressives selon le volume stocké.[3]

## Méthode de Création d'un Compte AWS

### Processus d'Inscription Standard

La création d'un compte AWS suit une procédure en 6 étapes rigoureusement encadrées  :[4]

**Étape 1 : Informations de Compte**
- Saisie d'une adresse e-mail qui servira d'identifiant utilisateur racine
- Définition d'un nom de compte AWS personnalisé
- Vérification par code de confirmation envoyé par e-mail
- Création d'un mot de passe sécurisé pour l'utilisateur racine

**Étape 2 : Coordonnées**
- Sélection du type de compte (Personnel/Professionnel)
- Saisie des informations de contact complètes
- Acceptation du Contrat Client AWS (conditions légales obligatoires)

**Étape 3 : Mode de Paiement**
- Ajout d'une carte bancaire valide pour la facturation
- Débit de vérification de 1 EUR pour validation[5]
- Configuration optionnelle d'une adresse de facturation différente

**Étape 4 : Vérification d'Identité**
- Validation par appel téléphonique ou SMS
- Saisie d'un code PIN de vérification
- Résolution d'un CAPTCHA de sécurité[6]

**Étape 5 : Choix de Formule Support**
- Sélection d'un plan de support (gratuit recommandé pour débuter)
- Options payantes disponibles pour support technique avancé

**Étape 6 : Activation**
- Processus d'activation automatique (généralement sous quelques minutes)
- Délai maximal d'activation : 24 heures

### Accès aux Services et Console

Une fois le compte activé, l'accès s'effectue via console.aws.amazon.com  avec les identifiants créés. La console AWS Management Console propose une interface centralisée pour gérer l'ensemble des services cloud disponibles.[7]

## Tarification AWS : Modèles et Calculateur

### Structure Tarifaire AWS Free Tier 2025

AWS propose depuis 2025 une offre gratuite révisée  comprenant :[8]

**Nouveau Plan Gratuit :**
- **200 USD de crédits** utilisables sur 6 mois (extension par rapport aux anciens 12 mois)
- **Fermeture automatique** des comptes gratuits après expiration
- **Période de grâce de 90 jours** pour migration vers plan payant
- **Services interdits** en plan gratuit pour éviter la consommation rapide des crédits

**Limitations du Free Tier  :**[9]
- EC2 limité aux instances micro (t2.micro)
- Pas d'accès aux instances réservées
- Amazon EKS non disponible
- Pas de support pour le cryptominage
- Route 53 avec facturation des zones hébergées

**Services Toujours Gratuits :**
- 1 million de requêtes/mois AWS Lambda
- 25 GB de stockage DynamoDB
- 50 GB de stockage Glacier
- 1 million d'appels/mois API Gateway

### Calculateur de Prix AWS

Le calculateur officiel AWS Pricing Calculator  permet d'estimer précisément les coûts d'infrastructure avant déploiement. Cet outil intègre l'ensemble des services AWS et leurs modèles tarifaires spécifiques.[10]

## Amazon RDS et MongoDB : Limitations Fondamentales

### Incompatibilité Structurelle

Amazon RDS (Relational Database Service) **ne supporte pas MongoDB** car il s'agit exclusivement d'un service de bases de données relationnelles. Cette limitation architecturale fondamentale nécessite l'utilisation d'alternatives spécifiquement conçues pour les bases de données NoSQL.[11]

**Pourquoi MongoDB n'est pas dans RDS :**
- RDS signifie "Relational Database Service" - exclusivement relationnel
- MongoDB est une base de données documentaire NoSQL non-relationnelle  
- Architecture incompatible avec le modèle relationnel d'RDS
- AWS privilégie DynamoDB comme solution NoSQL native

### Alternatives Disponibles

**MongoDB Atlas** : Service Database-as-a-Service (DBaaS) officiel MongoDB hébergé sur AWS , offrant :[12]
- Compatibilité 100% avec MongoDB
- Intégration AWS IAM
- Optimisation coûts via instances réservées
- Sauvegardes automatisées et monitoring avancé

**Amazon DocumentDB** : Alternative AWS native avec compatibilité partielle MongoDB , présentant des limitations significatives de compatibilité API.[13]

## Amazon DocumentDB : Analyse Détaillée

### Caractéristiques Techniques

Amazon DocumentDB constitue une base de données de documents JSON entièrement gérée, émulant les APIs MongoDB 4.0 et 5.0. Le service utilise un moteur de stockage propriétaire basé sur Aurora, distinct du serveur MongoDB officiel.[13]

**Architecture Technique :**
- Moteur non basé sur le code MongoDB original[14]
- Émulation API MongoDB sur backend Aurora
- Support partiel des fonctionnalités MongoDB 4.0/5.0
- Stockage découplé du calcul pour scalabilité indépendante

**Limitations Critiques de Compatibilité  :**[14]
- Échec à plus de 66% des tests de compatibilité API MongoDB
- Nécessité de modifications code pour migration applications
- Fonctionnalités MongoDB avancées non supportées
- Pas de support sharding horizontal complet

### Modèle Tarifaire DocumentDB

DocumentDB propose deux configurations de stockage   :[15][16]

**Configuration Standard (pay-per-use I/O) :**
- **4 dimensions de facturation** :
  1. Instances à la demande (par seconde, minimum 10 minutes)
  2. E/S base de données (par million d'opérations)
  3. Stockage base de données (par GB/mois)
  4. Stockage sauvegarde (par GB/mois excédentaire)
- **Recommandée** si coûts I/O < 25% du budget cluster

**Configuration I/O-Optimized :**
- **3 dimensions de facturation** (I/O incluses)
- **Coûts prévisibles** sans facturation I/O
- **Recommandée** si coûts I/O > 25% du budget cluster

**Exemple Tarifaire Concret  :**[15]
Configuration : Cluster db.r5.large x2 instances, 50 GB données, 200M I/O/mois (US East)
- Instances : 404,42 USD/mois (0,277 USD/h × 730h × 2)
- Stockage : 5,00 USD/mois (0,10 USD/GB × 50 GB)
- I/O : 40,00 USD/mois (0,20 USD/million × 200M)
- **Total : 449,42 USD/mois**

### Comparaison Coûts DocumentDB vs MongoDB Atlas

Une analyse comparative  pour un cluster 16 vCPUs, 300 GB stockage multi-AZ révèle :[17]
- **DocumentDB I/O-Optimized** : 3 603,60 USD/mois
- **MongoDB Atlas** : 2 844,00 USD/mois
- **Différence** : DocumentDB 26,7% plus coûteux

## Déploiement MongoDB sur Amazon ECS

### Architecture ECS avec MongoDB

Amazon ECS (Elastic Container Service) permet l'orchestration complète de conteneurs MongoDB avec intégration native Fargate. Cette approche offre une flexibilité maximale tout en conservant un contrôle granulaire sur l'infrastructure.[18]

**Configuration Type Multi-Conteneurs  :**[18]

**Conteneur MongoDB :**
- Image : mongo (Docker Hub officiel)
- Port mapping : 27017 (port standard MongoDB)
- Variables d'environnement :
  ```yaml
  MONGO_INITDB_ROOT_USERNAME: admin_user
  MONGO_INITDB_ROOT_PASSWORD: secure_password
  ```

**Conteneur Application :**
- Image : Application personnalisée
- Port mapping : 3000 (ou selon besoins)
- Variables d'environnement connexion MongoDB
- Health checks configurés

### Persistance des Données avec EFS

**Configuration Volume EFS  :**[18]
- Création volume EFS dédié "mongo-db"
- Montage dans conteneur MongoDB : `/data/db`
- Groupes de sécurité autorisant NFS (port 2049)
- Réplication multi-AZ automatique

**Sécurité Réseau :**
- Déploiement en sous-réseaux privés
- Groupes de sécurité restrictifs ECS ↔ EFS uniquement
- Pas d'accès Internet direct aux conteneurs de données

### Intégration Docker Compose sur ECS

AWS supporte le déploiement Docker Compose directement sur ECS , simplifiant considérablement le processus :[19]

**Workflow Déploiement :**
1. **Conteneurisation locale** avec Docker Desktop
2. **Publication images** sur Amazon ECR (Elastic Container Registry)
3. **Configuration docker-compose.yaml** avec références ECR
4. **Déploiement automatisé** via Docker Compose CLI

**Avantages Approche :**
- Développement local → Production cloud transparent
- Gestion dépendances inter-services automatisée
- Scaling et monitoring intégrés
- Intégration native Load Balancer (ALB)

## Configuration Sauvegardes et Surveillance

### Sauvegardes MongoDB sur AWS

**Stratégie Multi-Niveaux :**

**Snapshots EFS  :**[20]
- Sauvegardes automatiques quotidiennes des volumes de données
- Rétention configurable (1-35 jours)
- Restauration point-in-time avec résolution à la seconde
- Chiffrement automatique des snapshots

**Sauvegardes S3 :**
- Export périodique des collections MongoDB vers S3
- Classes de stockage optimisées (Standard → IA → Glacier)
- Lifecycle policies automatisées pour archivage long terme
- Cross-region replication pour disaster recovery

### Surveillance avec CloudWatch

**Métriques Système  :**[21]
- CPU, mémoire, I/O disque des conteneurs ECS
- Métriques réseau et latence inter-services
- Utilisation stockage EFS et S3

**Métriques MongoDB Personnalisées  :**[22]
- Connexions actives et pool de connexions
- Temps de réponse requêtes et operations/seconde
- Réplication lag et status replica set
- Utilisation indexes et cache hit ratio

**Configuration Alertes  :**[23]
```json
{
  "AlarmName": "MongoDB-HighConnections",
  "MetricName": "ConnectionsActive",
  "Threshold": 1000,
  "ComparisonOperator": "GreaterThanThreshold",
  "AlarmActions": ["arn:aws:sns:region:account:topic"]
}
```

### Logs et Monitoring Avancé

**Centralisation Logs CloudWatch  :**[24]
- Configuration awslogs driver pour conteneurs ECS
- Streaming logs MongoDB vers CloudWatch Logs
- Requêtes CloudWatch Insights pour analyse patterns
- Intégration alertes basées sur logs d'erreurs

**Profiling et Optimisation  :**[21]
- Activation profiler MongoDB pour requêtes lentes
- Analyse détaillée via CloudWatch Insights
- Recommandations d'optimisation automatisées
- Monitoring performance indexes

## Architecture Cloud Recommandée

### Conception Multi-AZ Haute Disponibilité

**Topologie Réseau  :**[25]
- VPC dédié avec sous-réseaux privés multi-AZ
- Application Load Balancer (ALB) pour distribution trafic
- NAT Gateways pour accès Internet sortant sécurisé
- VPC Endpoints pour services AWS (S3, ECR, CloudWatch)

**Services Complémentaires  :**[25]
- **Amazon Route 53** : DNS et health checks
- **AWS CloudFront** : CDN et mise en cache edge
- **AWS WAF** : Filtering trafic malveillant
- **AWS Shield** : Protection DDoS automatique

### Stratégie de Migration Progressive

**Phase 1 : Assessment et Planning**
- Évaluation données existantes et patterns d'usage
- Dimensionnement infrastructure cible
- Plan de migration avec downtime minimal

**Phase 2 : Infrastructure Setup**
- Provisioning VPC, ECS cluster, EFS volumes
- Configuration monitoring et alertes
- Tests de charge et validation performances

**Phase 3 : Migration Données**
- Synchronisation initiale via AWS DMS[26]
- Cutover progressif par application/service
- Validation intégrité données post-migration

**Phase 4 : Optimisation Post-Migration**
- Fine-tuning paramètres performance
- Ajustement politiques de sauvegarde
- Formation équipes opérationnelles

## Recommandations Stratégiques

### Choix d'Architecture Optimal

Pour un client nécessitant une migration MongoDB avec exigences de compatibilité maximale, la recommandation est :

**Architecture Hybride :**
- **MongoDB Atlas** pour workloads critiques nécessitant compatibilité 100%
- **Amazon DocumentDB** pour nouvelles applications acceptant limitations
- **Auto-hébergé sur ECS** pour contrôle maximal et personnalisation

### Considérations Coûts vs Fonctionnalités

**Matrice Décisionnelle :**

| Solution | Compatibilité | Gestion | Coût | Flexibilité |
|----------|---------------|---------|------|-------------|
| MongoDB Atlas | 100% | Entièrement gérée | $$$ | Moyenne |
| Amazon DocumentDB | 66% | Entièrement gérée | $$$$ | Faible |
| Auto-hébergé ECS | 100% | Auto-gérée | $$ | Maximale |

### Feuille de Route Implémentation

**Immédiat (0-3 mois) :**
- Création compte AWS et setup environnement
- POC migration subset données sur ECS
- Formation équipes AWS et MongoDB

**Court terme (3-6 mois) :**
- Migration applications non-critiques
- Mise en place monitoring et alertes
- Optimisation coûts et performances

**Moyen terme (6-12 mois) :**
- Migration complète workloads production
- Disaster recovery testing
- Certification équipes et processus

Cette approche méthodique garantit une transition réussie vers une infrastructure cloud scalable, sécurisée et optimisée pour les besoins spécifiques de gestion de données médicales.

***

**Sources :**

 CopiesWebduProjet.pdf - Document projet P5 OpenClassrooms[27]
 https://www.mongodb.com/resources/compare/documentdb-vs-mongodb - Comparing Amazon DocumentDB And MongoDB[14]
 https://www.reddit.com/r/aws/comments/frnazr/mongodb_on_rds/ - MongoDb sur RDS : r/aws[11]
 https://aws.amazon.com/fr/s3/ - Stockage d'objets dans le cloud – Amazon S3[1]
 https://docs.aws.amazon.com/fr_fr/documentdb/latest/developerguide/compatibility.html - Compatibilité d'Amazon DocumentDB avec MongoDB[13]
 https://notes.kodekloud.com/docs/Amazon-Elastic-Container-Service-AWS-ECS/Deploying-a-new-application-from-scratch/Demo-Creating-multi-container-application - Demo Creating multi container application[18]
 https://www.lemagit.fr/actualites/450416968/AWS-cree-un-pont-direct-depuis-MongoDB-vers-DynamoDB - AWS crée un pont direct depuis MongoDB vers DynamoDB[26]
 https://aws.amazon.com/documentdb/pricing/ - Amazon DocumentDB (with MongoDB compatibility) pricing[15]
 https://aws.amazon.com/blogs/database/deploy-a-containerized-application-with-amazon-ecs-and-connect-to-amazon-documentdb-securely/ - Deploy a containerized application with Amazon ECS[28]
 https://www.vantage.sh/blog/documentdb-vs-mongodb-price-comparison - MongoDB Atlas vs Amazon DocumentDB: Cost Considerations[17]
 https://aws.amazon.com/blogs/apn/accelerate-application-modernization-with-amazon-ecs-aws-fargate-and-mongodb-atlas/ - Accelerate Application Modernization with Amazon ECS[19]
 https://aws.amazon.com/fr/documentdb/pricing/ - Tarification Amazon DocumentDB – Amazon Web Services[16]
 https://www.mongodb.com/fr-fr/products/platform/atlas-cloud-providers/aws - Comment Exécuter MongoDB Atlas Sur Le Cloud AWS[12]
 https://aws.amazon.com/fr/resources/create-account/ - Comment créer un compte AWS[4]
 https://nouslesdevs.com/serveur/creer-un-compte-aws/ - Créer un compte AWS[5]
 https://fr.linkedin.com/learning/preparer-la-certification-aws-cloud-practitioner-les-bases-23118376/creer-son-compte-aws-et-gerer-ses-couts - Créer son compte AWS et gérer ses coûts[7]
 https://www.marches-publics.info/kiosque/inscription.pdf - AWS Entreprises - Inscription[6]
 https://calculator.aws - AWS Pricing Calculator[10]
 https://stackoverflow.com/questions/58092007/send-mongodb-logs-to-aws-cloudwatch - Send Mongodb logs to AWS Cloudwatch[24]
 https://www.influxdata.com/integrations/cloudwatch-mongodb/ - Amazon CloudWatch and MongoDB Integration[22]
 https://docs.aws.amazon.com/fr_fr/documentdb/latest/developerguide/logging-and-monitoring.html - Journalisation et surveillance dans Amazon DocumentDB[21]
 https://dev.to/imsushant12/aws-monitoring-and-logging-cloudwatch-and-cloudtrail-explained-4165 - AWS Monitoring and Logging: CloudWatch and CloudTrail[23]
 https://docs.aws.amazon.com/fr_fr/documentdb/latest/developerguide/backup_restore.html - Sauvegarde et restauration dans Amazon DocumentDB[20]
 https://docs.aws.amazon.com/fr_fr/whitepapers/latest/web-application-hosting-best-practices/an-aws-cloud-architecture-for-web-hosting.html - Une architecture de cloud AWS pour l'hébergement web[25]
 https://rotek.fr/aws-free-tier-nouveaux-plans-gratuits-payants-amazon/ - AWS Free Tier 2025 : tout savoir sur les nouveaux plans[8]
 https://cloudmounter.net/fr/amazon-s3-vs-google-cloud-storage/ - Différences entre Google Cloud Storage et Amazon S3[3]
 https://cloudavocado.com/blog/aws-free-tier-an-overview-of-capabilities-and-limitations/ - AWS Free Tier: an overview of capabilities and limitations[9]
 https://www.hivenet.com/fr/post/best-cloud-storage-example-understanding-how-it-works - Exemples de stockage dans le cloud : Google Drive, AWS[2]

[1](https://aws.amazon.com/fr/s3/)
[2](https://www.hivenet.com/fr/post/best-cloud-storage-example-understanding-how-it-works)
[3](https://cloudmounter.net/fr/amazon-s3-vs-google-cloud-storage/)
[4](https://aws.amazon.com/fr/resources/create-account/)
[5](https://nouslesdevs.com/serveur/creer-un-compte-aws/)
[6](https://www.marches-publics.info/kiosque/inscription.pdf)
[7](https://fr.linkedin.com/learning/preparer-la-certification-aws-cloud-practitioner-les-bases-23118376/creer-son-compte-aws-et-gerer-ses-couts)
[8](https://rotek.fr/aws-free-tier-nouveaux-plans-gratuits-payants-amazon/)
[9](https://cloudavocado.com/blog/aws-free-tier-an-overview-of-capabilities-and-limitations/)
[10](https://calculator.aws)
[11](https://www.reddit.com/r/aws/comments/frnazr/mongodb_on_rds/)
[12](https://www.mongodb.com/fr-fr/products/platform/atlas-cloud-providers/aws)
[13](https://docs.aws.amazon.com/fr_fr/documentdb/latest/developerguide/compatibility.html)
[14](https://www.mongodb.com/resources/compare/documentdb-vs-mongodb)
[15](https://aws.amazon.com/documentdb/pricing/)
[16](https://aws.amazon.com/fr/documentdb/pricing/)
[17](https://www.vantage.sh/blog/documentdb-vs-mongodb-price-comparison)
[18](https://notes.kodekloud.com/docs/Amazon-Elastic-Container-Service-AWS-ECS/Deploying-a-new-application-from-scratch/Demo-Creating-multi-container-application)
[19](https://aws.amazon.com/blogs/apn/accelerate-application-modernization-with-amazon-ecs-aws-fargate-and-mongodb-atlas/)
[20](https://docs.aws.amazon.com/fr_fr/documentdb/latest/developerguide/backup_restore.html)
[21](https://docs.aws.amazon.com/fr_fr/documentdb/latest/developerguide/logging-and-monitoring.html)
[22](https://www.influxdata.com/integrations/cloudwatch-mongodb/)
[23](https://dev.to/imsushant12/aws-monitoring-and-logging-cloudwatch-and-cloudtrail-explained-4165)
[24](https://stackoverflow.com/questions/58092007/send-mongodb-logs-to-aws-cloudwatch)
[25](https://docs.aws.amazon.com/fr_fr/whitepapers/latest/web-application-hosting-best-practices/an-aws-cloud-architecture-for-web-hosting.html)
[26](https://www.lemagit.fr/actualites/450416968/AWS-cree-un-pont-direct-depuis-MongoDB-vers-DynamoDB)
[27](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_dba37358-f03b-40a8-8d10-3c05b359efe6/af21f2ce-4541-4187-9e0f-d2913083c511/CopiesWebduProjet.pdf)
[28](https://aws.amazon.com/blogs/database/deploy-a-containerized-application-with-amazon-ecs-and-connect-to-amazon-documentdb-securely/)
[29](https://www.sprinkledata.com/blogs/mongodb-vs-documentdb-a-comprehensive-comparison-for-choosing-the-right-nosql-database)
[30](https://www.amazonaws.cn/en/documentdb/pricing/)
[31](https://n2ws.com/blog/aws-cloud/amazon-documentdb)
[32](https://www.mongodb.com/products/platform/atlas-cloud-providers/aws/pricing)
[33](https://docs.aws.amazon.com/documentdb/latest/developerguide/functional-differences.html)
[34](https://www.youtube.com/watch?v=H4QZg73nKFc)
[35](https://docs.aws.amazon.com/fr_fr/documentdb/latest/developerguide/functional-differences.html)
[36](https://docs.aws.amazon.com/fr_fr/accounts/latest/reference/manage-acct-creating.html)
[37](https://www.mongodb.com/pricing)
[38](https://www.geeksforgeeks.org/dbms/difference-between-mongodb-and-amazon-documentdb/)
[39](https://learn.microsoft.com/fr-fr/entra/permissions-management/onboard-aws)
[40](https://cloudchipr.com/blog/mongodb-pricing)
[41](https://severalnines.com/blog/mysql-cloud-pros-and-cons-amazon-rds/)
[42](https://supervision-clever.fr/supervision-aws-amazon-cloudwatch-logiciel-alertes-notifications/)
[43](https://www.youtube.com/watch?v=7QmbmHsz0x8)
[44](https://www.reddit.com/r/aws/comments/aecfrf/aws_announces_amazon_documentdb_with_mongodb/)
[45](https://dev.to/gbenga700/deploying-a-dockerized-web-application-with-aws-ecs-and-fargate-29bb)
[46](https://docs.aws.amazon.com/fr_fr/documentdb/latest/developerguide/limits.html)
[47](https://stackoverflow.com/questions/49579796/connect-to-mongodb-in-separate-docker-container-aws-ecs)
[48](https://www.netapp.com/blog/aws-cvo-blg-mongodb-on-aws-managed-service-vs-self-managed/)
[49](https://dev.to/aws-builders/complete-guide-deploying-production-ready-mongodb-replica-set-on-aws-1ph)
[50](https://web.pysae.com/blog/infrastructure-mongodb-et-amazon-cloud-pourquoi-ce-choix-et-quest-ce-que-cela-implique)
[51](https://onecompiler.com/posts/3smjka7gd/mongodb-atlas-free-tier-limitations)
[52](https://cloud.google.com/storage/docs/aws-simple-migration?hl=fr)
[53](https://www.redhat.com/fr/topics/cloud-computing/what-is-cloud-architecture)
[54](https://miro.com/fr/diagramme/architecture-cloud-aws/)
[55](https://dev.to/briansuarezsantiago/how-to-create-a-free-aws-account-and-understand-the-free-tier-a-beginners-guide-1dhl)
[56](https://www.orsys.fr/orsys-lemag/architectures-serverless-par-ou-commencer/)
[57](https://flexa.cloud/fr/services-de-stockage-aws-et-leurs-avantages/)
[58](https://www.mongodb.com/docs/atlas/reference/free-shared-limitations/)
[59](https://aws.amazon.com/fr/architecture/)
[60](https://aws.amazon.com/fr/cloud-data-migration/)
[61](https://www.globalknowledge.com/fr-fr/formation/amazon_web_services/cloud_computing/gk4502)
[62](https://movebot.io/fr/blog/aws-s3-migrations)
[63](https://docs.aws.amazon.com/fr_fr/awsaccountbilling/latest/aboutv2/tracking-free-tier-usage.html)

# MongoDB Atlas est généralement recommandé comme choix de service pour les projets nécessitant une base MongoDB sur AWS.

## Raisons principales pour préconiser MongoDB Atlas

- **Service managé complet** : Atlas gère automatiquement la disponibilité, la scalabilité, les mises à jour, la sécurité, les backups, ainsi que la conformité aux normes. Cela réduit fortement la charge opérationnelle.
- **Compatibilité totale** : Atlas utilise le moteur MongoDB natif, assurant la prise en charge de toutes les fonctionnalités avancées, nouveaux formats de données, transactions distribuées, et extensions propriétaires sans limite.
- **Support dédié** : En choisissant Atlas, les équipes bénéficient d’un support spécialisé MongoDB, facilitant la résolution rapide des incidents et l’optimisation des performances.
- **Intégration AWS native** : Atlas est disponible sur la marketplace AWS, ce qui permet une intégration poussée avec IAM, VPC, CloudWatch, et autres outils AWS.
- **Sécurité et conformité** : Certifications fréquentes, chiffrement robuste et contrôle d’accès granulaire simplifient le respect des réglementations dans les domaines sensibles comme la santé.
- **Coûts plus élevés mais plus prévisibles** : Les coûts sont plus élevés qu’en auto-hébergement ECS, mais le service inclut la majorité des tâches d’administration critiques automatiquement.

## Inconvénients de l’auto-hébergement ECS

- **Exigences élevées en compétences techniques** : Il faut une équipe expérimentée capable de gérer la configuration, la maintenance, l’optimisation et la sécurité MongoDB, tout en maîtrisant l’écosystème AWS.
- **Charge opérationnelle accrue** : Les mises à jour, sauvegardes, surveillance, gestion des incidents et scalabilité manuelle doivent être gérées en interne.
- **Risques accrus** : Mauvaise configuration ou manque d’attention dans la maintenance peut entraîner des interruptions, pertes de données ou slowdowns.

En conclusion, MongoDB Atlas est recommandé lorsque la priorité est une solution robuste, supérieure techniquement et opérationnellement, même avec un budget plus important. L’auto-hébergement ECS convient mieux à des environnements maîtrisés avec des équipes compétentes et recherchant des coûts maîtrisés avec plus de flexibilité.

Cette analyse correspond à la recommandation stratégique présentée dans le projet, privilégiant la qualité de service et la sécurité des données médicales en production.

# Sharding
La différence entre **"Sharding = Oui"** et **"Sharding = Hash Shard"** réside dans la manière dont la distribution des données est gérée au sein du cluster.

## Sharding = Oui (MongoDB natif ou Atlas)
- Le sharding natif de MongoDB est un partitionnement horizontal avancé où les données sont divisées en fragments (shards) répartis sur plusieurs serveurs.
- Le partitionnement peut se faire par différentes clés de sharding, et MongoDB supporte plusieurs stratégies de sharding : 
  - **Range Sharding** (données réparties par plages de valeurs)
  - **Hash Sharding** (données réparties par hachage de la clé)
  - Sharding complexe pouvant répartir la charge de façon très précise.
- Cela permet une **scalabilité horizontale étendue** avec équilibrage fin de la charge et haute disponibilité.
- Supporte aussi des configurations de sharding dynamiques avec migration automatique des chunks.
- Offre une scalabilité et performance optimales pour charges de travail variées.

## Hash Shard (Amazon DocumentDB)
- Le sharding dans DocumentDB est une **implémentation simplifiée**, souvent limitée au sharding par hachage fixe (hash shard).
- Les données sont distribuées selon le hash de la clé de partition, ce qui garantit une distribution relativement uniforme.
- Cette approche est moins flexible, ne supporte pas toutes les stratégies de partitionnement avancées de MongoDB.
- Le sharding automatique de DocumentDB est plus simplifié, avec moins d’options et de capacités de migration/chunk management dynamique.
- Peut entraîner des **"hot partitions"** où certaines shards reçoivent plus de charge.
- En résumé, moins puissant et flexible que le sharding natif MongoDB.

## En résumé
- Le **sharding natif MongoDB** est plus complet, configurable et performant.
- Le **hash sharding DocumentDB** est une version simplifiée avec moins de contrôle, conçue pour une scalabilité de base mais avec des limites.

Cette distinction explique pourquoi DocumentDB est mieux adapté pour des workloads moins exigeants en scalabilité fine alors que le sharding natif MongoDB reste la référence pour des déploiements distribués à grande échelle.