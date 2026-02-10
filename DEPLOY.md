# Deployment Guide

## 1. Push to GitHub

**Prerequisite**: Create a new empty repository on GitHub (e.g., `sky-culture-lite`).

```bash
cd "d:\Sky Cultures\sky_culture_engine"

# Initialize Git
git init
git add .
git commit -m "Initial commit of Sky Culture Lite"

# Link to GitHub (Replace URL with your actual repo URL)
git remote add origin https://github.com/YOUR_USERNAME/sky-culture-lite.git
git branch -M main
git push -u origin main
```

## 2. Push to Docker Hub

**Prerequisite**: Create a Docker Hub account and a repository (e.g., `sky-culture-lite`).

```bash
# Login to Docker Hub
docker login

# Tag your local image (Replace YOUR_DOCKER_USER)
docker tag sky-culture-lite:latest YOUR_DOCKER_USER/sky-culture-lite:latest

# Push the image
docker push YOUR_DOCKER_USER/sky-culture-lite:latest
```

## Notes

- **`data/de421.bsp`**: This file is ignored by Git (`.gitignore`) to keep the repo light (~17MB avoided).
- **Docker Build**: The Dockerfile automatically creates the `data/` directory. On the *first run* inside the container, it will download `de421.bsp` if it's missing.
- **Running from Docker Hub**:
  ```bash
  docker run -i --rm YOUR_DOCKER_USER/sky-culture-lite
  ```
