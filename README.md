# Healthcare Data Migration to MongoDB

A scalable, containerized solution for migrating healthcare datasets from CSV to MongoDB with automated data validation, type conversion, and schema enforcement.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Database Schema](#database-schema)
- [Authentication & Security](#authentication--security)
- [Docker Deployment](#docker-deployment)
- [Development](#development)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## Overview

This project provides a complete ETL (Extract, Transform, Load) solution for healthcare data migration. It automatically processes CSV healthcare datasets, performs data validation and type conversion, and loads them into a MongoDB database with proper schema validation and indexing.

The solution is fully containerized using Docker and Docker Compose, ensuring consistent deployment across different environments with separate production and test modes.

## Features

- **Automated Data Migration**: CSV to MongoDB with data type conversion
- **Schema Validation**: JSON Schema validation for MongoDB collections
- **Data Quality**: Comprehensive data validation and error handling
- **Flexible Configuration**: YAML-based field definitions and MongoDB roles
- **Containerized**: Docker and Docker Compose for easy deployment
- **Security**: Role-based access control and authentication
- **Logging**: Detailed logging with configurable levels
- **Development Mode**: Debug and testing capabilities
- **Dual Environment**: Separate production and test configurations

## Architecture

```
├── data/
│   ├── healthcare_dataset.csv    # Source data
│   ├── fields_settings.yml       # Field definitions (configurable)
│   ├── mongodb_roles.yml         # MongoDB roles (configurable)
├── docs/
│   ├── keynotes.md               # notes about project 
│   ├── AWS_keynotes.md           # notes about AWS mongoDB services  
│   ├── migration_healthcare.log  # sample log file
├── importer/
│   ├── __init__.py               # __init__ py file for import abilities
│   ├── Dockerfile                # Container configuration
│   ├── importer.py               # Main application entry point
│   ├── engine.py                 # Core migration engine
│   ├── manager.py                # Field management and validation
│   └── requirements.txt          # Python dependencies
│   └── mongodb_roles.yml         # Database roles configuration (configurable)
├── notebooks/
│   ├── exploratory_analysis.ipynb    # jupyter notebook for data exploration
├── logs/                         # Application logs
├── .template.env                 # Production environment template
├── .template.test.env            # Test environment template
├── launch_mongodb_test.sh        # Test MongoDB container launcher
├── Dockerfile                    # Container configuration
├── docker-compose.yml            # Multi-container setup
└── requirements.txt              # global python dependencies including notebooks need
```

### Core Components

1. **Importer** (`importer/importer.py`): Entry point handling environment configuration
2. **Engine** (`importer/engine.py`): Core ETL logic with MongoDB operations
3. **Manager** (`importer/manager.py`): Field validation, type conversion, and schema management

## Prerequisites

- Docker and Docker Compose
- Python 3.12+ (for local development)
- 4GB+ available RAM
- Network access to MongoDB (port 27017)
- Bash shell (for test scripts)

## Installation

### Production Mode Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd healthcare-data-migration
```

2. Create production environment configuration:
```bash
cp .template.env .env
```

3. Configure your production environment variables in `.env`:
```bash
MONGODBNAME=healthcare
MONGOINITDBROOTUSERNAME=your_username
MONGOINITDBROOTPASSWORD=your_password
MONGOHOST=mongo
MONGOPORT=27017
MONGOVOLUME=mongoproddata
```

4. Start production services:
```bash
docker-compose up -d
```

### Test Mode Setup

1. Create test environment configuration:
```bash
cp .template.test.env .test.env
```

2. Configure your test environment variables in `.test.env`:
```bash
MONGODBNAME=testhc
MONGOINITDBROOTUSERNAME=your_test_username
MONGOINITDBROOTPASSWORD=your_test_password
MONGOHOST=mongo
MONGOPORT=27017
MONGOVOLUME=mongotestdata
MIGRATIONDEBUG=True
DEBUGSTART=0
DEBUGLIMIT=100
DEBUGTRACEONLY=False
```

3. Launch test MongoDB container:
```bash
./launch_mongodb_test.sh
```

### Local Development

1. Install Python dependencies:
```bash
cd importer/
pip install -r requirements.txt
```

2. Run the migration locally:
```bash
cd importer/
python importer.py
```

## Configuration

### Environment Files

The project uses template-based configuration:

- **`.template.env`**: Production environment template
- **`.template.test.env`**: Test environment template

Copy the appropriate template and customize:

```bash
# For production
cp .template.env .env

# For testing  
cp .template.test.env .test.env
```

### Environment Variables

| Variable | Description | Production Default | Test Default | Required |
|----------|-------------|-------------------|--------------|----------|
| `MONGODBNAME` | Database name | healthcare | testhc | ✓ |
| `MONGOINITDBROOTUSERNAME` | MongoDB root username | - | - | ✓ in prod |
| `MONGOINITDBROOTPASSWORD` | MongoDB root password | - | - | ✓ in prod |
| `MONGOHOST` | MongoDB host | mongo | mongo | ✗ |
| `MONGOPORT` | MongoDB port | 27017 | 27017 | ✗ |
| `MONGOVOLUME` | Docker volume name | mongoproddata | mongotestdata | ✓ in prod |
| `MIGRATIONDEBUG` | Enable debug logging | False | True | ✗ |
| `DEBUGSTART` | Start row for debug | 0 | 0 | ✗ |
| `DEBUGLIMIT` | Limit rows for debug | 0 | 100 | ✗ |
| `DEBUGTRACEONLY` | Trace mode only | False | False | ✗ |
| `CLEANDB` | Clean database on start | False | False | ✗ |

### Dynamic Configuration Files

These files can be modified without rebuilding containers:

#### Field Configuration (`data/fields_settings.yml`)

```yaml
_id:
  parent : root
  doc: "care"
  type: "str"

Name:
  parent : care
  doc: "patient"
  type: "str"
  primary: care
  index: true

BloodType:
  parent : care
  doc: "patient"
  type: "str" 
  error_mask : is_blood_tpe
  required: false

Doctor:
  parent : care
  doc: "admission"  
  primary : care 
  type: "str"
  index: true
  replace : null
  
```

**Field Parameters:**
- `parent` : documents collection name, root is master document
- `doc`: Document section (care, patient, admission, billing.)
- `type`: Data type (str, int, float, date)
- `primary`: is part of the primary key of the given doc 
- `index`: Create index on field
- `required`: Required field
- `error_mask`: Validation function
- `replace`: Replacement value for invalid data

#### MongoDB Roles Configuration (`data/mongodb_roles.yml`)

```yaml
readUser:
  role: "read"
  privileges:
    - resource: { db: "healthcare", collection: "care" }
      actions: ["find"]

writeUser:
  role: "readWrite"
  privileges:
    - resource: { db: "healthcare", collection: "care" }
      actions: ["find", "insert", "update", "remove"]
```

## Usage

### Production Deployment

```bash
# Start complete production stack
docker-compose up -d

# Stop all services
docker-compose down

# Start only MongoDB (without migration script)
docker-compose up -d mongo
```

### Test Environment

```bash
# Launch test MongoDB container
./launch_mongodb_test.sh

# Run migration in test mode (local)
cd importer/
python importer.py
```

### Development Mode

```bash
# Navigate to importer directory
cd importer/

# Set debug environment variables
export MIGRATIONDEBUG=True
export DEBUGSTART=0
export DEBUGLIMIT=100
export DEBUGTRACEONLY=True

python importer.py
```

### Configuration Testing

Modify configuration files without rebuilding:

```bash
# Edit field definitions
vim data/fields_settings.yml

# Edit MongoDB roles
vim data/mongodb_roles.yml

# Restart migration to apply changes
docker-compose restart importer
```

## Database Schema

### Collection Structure

The system creates a MongoDB collection with the schema depending on field_settings.yml:

```javascript
{
  $jsonSchema: {
    bsonType: 'object',
    required: [
      'observation',
      '_id',
      'patient',
      'billing',
      'admission'
    ],
    properties: {
      _id: {
        bsonType: 'string'
      },
      patient: {
        bsonType: 'object',
        properties: {
          name: {
            bsonType: 'string'
          },
          age: {
            bsonType: 'int'
          },
          gender: {
            bsonType: 'string'
          },
          bloodType: {
            bsonType: 'string'
          }
        },
        required: [
          'name',
          'age',
          'gender',
          'bloodType'
        ]
      },}
`.........

    }
  }
}
```

### Indexes

Automatically created indexes based on `fields_settings.yml`:
- Primary key (`_id`)
- Fields marked with `INDEX: true`
- Composite indexes for performance optimization

## Authentication & Security

### Database Roles

The system creates role-based access control defined in `data/mongodb_roles.yml`:

```yaml
readUser:
  role: "read"
  privileges:
    - resource: { db: "healthcare", collection: "care" }
      actions: ["find"]

writeUser:
  role: "readWrite"
  privileges:
    - resource: { db: "healthcare", collection: "care" }
      actions: ["find", "insert", "update", "remove"]
```

### Security Features

- **Environment Separation**: Distinct production and test databases
- **Password Protection**: Username/password authentication required
- **Production Safety**: Prevents accidental connection to production in development
- **Input Validation**: Comprehensive data validation before insertion
- **Error Handling**: Secure error logging without exposing sensitive data

## Docker Deployment

### Services

The `docker-compose.yml` defines:

1. **MongoDB Service**:
   - Official MongoDB image
   - Environment-specific persistent volume
   - Port 27017 exposed
   - Authentication enabled

2. **Importer Service**:
   - Custom Python application from `importer/` directory
   - Volume mounts for data and logs
   - Depends on MongoDB service
   - Auto-restart capability

### Volume Management

- **Production**: `mongoproddata` volume
- **Test**: `mongotestdata` volume (via `launch_mongodb_test.sh`)
- **Data**: `./data:/app/data:ro` (read-only)
- **Logs**: `./logs:/app/logs` (read-write)
- **Source**: `./importer:/app` (application code)

### Container Commands

```bash
# Production deployment
docker-compose up -d                 # Start all services
docker-compose up -d mongo          # Start only MongoDB
docker-compose down                  # Stop all services
docker-compose restart importer     # Restart migration service
docker-compose logs -f importer     # View migration logs

# Test environment
./launch_mongodb_test.sh            # Start test MongoDB
```

## Development

### Project Structure

```
importer/
├── importer.py          # Main entry point
├── engine.py           # Migration engine
├── manager.py          # Field management
└── requirements.txt    # Dependencies

data/
├── healthcare_dataset.csv    # Source data
├── fields_settings.yml       # Field configuration (editable)
└── mongodb_roles.yml         # Role configuration (editable)
```

### Local Setup

1. Create development environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

cd importer/
pip install -r requirements.txt
```

2. Use test configuration:
```bash
cp .template.test.env .test.env
# Edit .test.env with test database settings
```

3. Launch test MongoDB:
```bash
./launch_mongodb_test.sh
```

4. Run migration:
```bash
cd importer/
python importer.py
```

### Configuration Workflow

1. **Modify field definitions** in `data/fields_settings.yml`
2. **Update role permissions** in `data/mongodb_roles.yml`
3. **Test changes** without rebuilding containers
4. **Apply production settings** when ready

### Debug Features

- **Row Limiting**: Process subset of data for testing
- **Trace Mode**: Validate without actual database operations  
- **Detailed Logging**: Debug-level logging for troubleshooting
- **Clean Database**: Option to reset database state
- **Environment Isolation**: Separate test and production databases

## Testing

### Test Environment

The test environment provides:

- **Isolated database**: `testhc` (separate from production)
- **Debug logging**: Enabled by default
- **Limited dataset**: Configurable row limits
- **Safe testing**: No impact on production data

### Validation Tests

The system includes automated validation for:

- **Data Types**: Automatic type conversion and validation
- **Age Validation**: Ages between 0-120 years
- **Gender Validation**: Male/Female values only
- **Blood Type Validation**: Valid blood type formats
- **Missing Values**: Proper handling of null/empty values
- **Duplicates**: Detection and handling of duplicate records

### Manual Testing

```bash
# Start test MongoDB
./launch_mongodb_test.sh

# Test with limited dataset
cd importer/
DEBUGSTART=0 DEBUGLIMIT=10 DEBUGTRACEONLY=True python importer.py

# Test data validation
MIGRATIONDEBUG=True python importer.py

# Test clean installation
CLEANDB=True python importer.py
```

### Configuration Testing

```bash
# Modify field settings
vim data/fields_settings.yml

# Test configuration changes
docker-compose restart importer
docker-compose logs -f importer
```

## Troubleshooting

### Common Issues

**Connection Refused**
```bash
# Check container status
docker-compose ps

# Check MongoDB logs
docker-compose logs mongo

# For test environment
docker ps | grep mongo
```

**Authentication Failed**
```bash
# Verify credentials in environment file
cat .env | grep MONGO
# or for test
cat .test.env | grep MONGO

# Check MongoDB logs
docker-compose logs mongo
```

**Wrong Database Mode**
```bash
# Check if connected to wrong database
# Production protection prevents test connections to prod
# Use appropriate environment file and launcher
```

**Configuration Not Applied**
```bash
# Restart importer service to reload config files
docker-compose restart importer

# Check if files are mounted correctly
docker-compose exec importer ls -la /app/data/
```

### Environment-Specific Issues

**Production Mode:**
```bash
docker-compose up -d           # Full stack
docker-compose logs importer  # Check logs
```

**Test Mode:**
```bash
./launch_mongodb_test.sh       # Test database
cd importer/ && python importer.py  # Local execution
```

### Log Files

- **Application logs**: `logs/migration_healthcare.log`
- **MongoDB logs**: `docker-compose logs mongo`  
- **Container logs**: `docker-compose logs importer`
- **Test MongoDB**: `docker logs <container_name>`

### Debug Commands

```bash
# Enable detailed logging
export MIGRATIONDEBUG=True

# Check container connectivity
docker-compose exec importer ping mongo

# Verify environment loading
docker-compose exec importer env | grep MONGO

# Check file permissions
ls -la data/ logs/ importer/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes in the appropriate directory (`importer/` for code)
4. Test with both production and test configurations
5. Update documentation
6. Submit a pull request

### Code Style

- **Directory Structure**: Keep application code in `importer/`
- **Configuration**: Use template-based environment setup
- **Testing**: Use test environment for development
- **Documentation**: Update README for significant changes
- **Follow PEP 8**: Python code style guidelines

### Development Workflow

1. **Setup**: Use `.template.test.env` → `.test.env`
2. **Database**: Launch with `./launch_mongodb_test.sh`
3. **Code**: Modify files in `importer/` directory
4. **Config**: Test with `data/fields_settings.yml` and `data/mongodb_roles.yml`
5. **Production**: Deploy with `docker-compose up -d`

---

## License

This project is developed for educational purposes as part of the OpenClassroom Data Engineer training program.

## Support

For issues and questions:

1. **Check environment**: Verify you're using the correct `.env` or `.test.env`
2. **Check containers**: Use `docker-compose ps` to verify service status
3. **Check logs**: Review `logs/migration_healthcare.log` and container logs
4. **Check configuration**: Verify `data/fields_settings.yml` and `data/mongodb_roles.yml`
5. **Test mode**: Use `./launch_mongodb_test.sh` for safe testing
6. **Create issue**: Include environment details and log excerpts (without sensitive data)