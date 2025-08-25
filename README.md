# README - Medical Data Migration to MongoDB with Docker and AWS

## 1. Project Context

This project is conducted for DataSoluTech to migrate a medical dataset (CSV format) to a **MongoDB** database in order to provide a scalable and efficient solution for a client facing challenges in data management and exploitation. 
All components of the application are containerized using **Docker**, and an exploration of deployment on **AWS** Cloud is also included.[1]

## 2. Objectives

- Migrate medical data from CSV to MongoDB
- Automate the migration process with a Python script
- Containerize all components using Docker/Docker Compose
- Deliver comprehensive technical documentation and a client presentation
- Investigate AWS cloud solutions compatible with MongoDB[1]

## 3. Technical Prerequisites

- Operating system compatible with Docker (Linux, Windows, Mac)
- Docker & Docker Compose installed
- Python (recommended version: 3.9+)
- MongoDB (local instance or Docker container)
- Git for version control[1]

## 4. Project File Structure

- `migration_script.py`: Python script for importing CSV data into MongoDB
- `requirements.txt`: List of Python dependencies
- `docker-compose.yml`: Container orchestration file
- `README.md`: This documentation file
- `docs/`: Documentation and technical diagrams directory
- `notebooks/`: (Optional) Exploratory analysis or Jupyter notebooks
- `data/`: Source CSV files to be migrated[1]

## 5. Migration Workflow

1. Dataset analysis and preparation
2. Definition of the appropriate MongoDB schema
3. Execution of the migration script with quality controls
4. Integrity tests before and after migration
5. Containerization of the entire environment with Docker Compose[1]

## 6. Usage Instructions

### Installation

```bash
# Clone the project repository
git clone 
cd 

# Create and activate Python virtual environment
python -m venv venv
source venv/bin/activate   # On Windows: .\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Deployment with Docker

```bash
# Launch containers and execute the migration
docker-compose up --build
```

### Configuration

- Connection parameters for MongoDB are set in the `.env` file (to be created)
- User roles and access control are managed in `docs/authentication.md` (coming soon)[1]

## 7. Key Considerations

- Check data integrity and quality before migration
- Provide thorough documentation for all stages and technical decisions
- Use GitHub for version control and development traceability
- Follow security best practices for MongoDB and Docker[1]

## 8. Additional Resources

- MongoDB Documentation: https://docs.mongodb.com/
- Docker Documentation: https://docs.docker.com/
- AWS MongoDB Solutions: https://aws.amazon.com/documentdb/

