
# Notion Service Hub

This is a demo for integrating with the Notion API, which provides an API layer for interacting with Notion's REST API.

## Prerequisites

- Python 3.12
- Docker (optional, for running with Docker)
- Google Cloud CLI (optional, for deployments)

## Setup

### Set Environment Variables

Create a `.env` file in the root directory of the project and set the following environment variables:

```env
NOTION_BASE_URL=https://api.notion.com/v1
NOTION_API_KEY=notion_api_key

APP_BASE_PATH=/api/v1
APP_API_KEY=app_api_key
LOGGING_LEVEL=debug
```

Replace `notion_api_key` and `secure_api_key_for_notion_service_hub` with your actual Notion API key and API key for the service hub.

## Running the Application

### Run with Python

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   python run.py
   ```

### Run with Docker (Optional)

1. Build the Docker image:
   ```bash
   docker build . -t notion-service-hub
   ```

2. Run the Docker container:
   ```bash
   docker run notion-service-hub:latest
   ```

## Sample Request

To make a request to the Notion Service Hub, you can use the following details:

- **Authorization**:
`X-API-key`: `app_api_key`

```shell
curl --location '{host}/api/v1/databases' \
--header 'X-API-Key: f6473d3e-7074-4769-b69f-32c98827b28c'
```

## Running Unit Tests

To run unit tests, use `pytest`:

```bash
pytest tests
```

## Deployment

To deploy the application, use the provided `cloudrun_deploy.sh` script:

```bash
./cloudrun_deploy.sh
```

This script will deploy the service to Google Cloud Run.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
