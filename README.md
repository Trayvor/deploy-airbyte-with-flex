# Airbyte deploy using flox enivorment
## Introdution
That config installs airbyte as kind and adds 3 connectors (Google search, Google Analytics and Posthog). You can add more connectors in python script with [Official Airbyte API documentation](https://reference.airbyte.com/reference/getting-started).
## How to use
### Prerequirements:
1. Flox installed on your system
2. Docker engine running. If you use WSL2 on Windows - turn on your distributive support in Docker Desktop preferences.
### Step-by-step:
1. (If you use Gooogle connectors): Create project in Google Console, create new project, turn on required APIs (Search, Analytics), create and downlaod your SERVICE(!!!) account credentials.
2. Copy your credentials into project folder. File name: service_account_info.json
3. (If you use posthog): Register Posthog and get your free api key
4. Open flox configuration (type `flox edit` in project folder)
5. Change your posthog api key and google SERVICE(!!!) account mail in `[vars]` part
6. Save changes and activate your eviroment with `flox activate` command
