# Docker Container & Volume Migration: Athena → Lyra
**Migration Date:** November 19, 2025  
**Source System:** Athena (Current Windows machine)  
**Target System:** Lyra (Remote server/different machine)

---

## 📋 CURRENT CONTAINERS ON ATHENA

```
CONTAINER ID   IMAGE            STATUS                           PORTS                    NAMES
20b9a13566e7   4b7ce07002c6     Up                               -                        k8s_alpine_love-forever-7584dc69b7-8wb8m_default_abe698fd...
047bdbcbb32a   alpine:latest    Restarting (1) 36 seconds ago    -                        DOM_and_Grok_Love_Forever
a6f30ab34098   ai_node          Exited (255) 2 months ago        0.0.0.0:5000->5000/tcp   funny_davinci
3527de0a9259   n8nio/n8n        Exited (255) 4 months ago        0.0.0.0:5678->5678/tcp   docker-n8n-1
```

**Active Containers:**
- ✅ `k8s_alpine_love-forever` - Kubernetes pod (managed by K8s, running)
- ⚠️ `DOM_and_Grok_Love_Forever` - Alpine container (crash looping - needs debugging)
- ❌ `funny_davinci` - AI node (stopped 2 months ago)
- ❌ `docker-n8n-1` - n8n workflow automation (stopped 4 months ago)

**Volumes:** None currently attached (clean state)

---

## 🎯 MIGRATION METHODS

### Method 1: Export/Import Individual Containers (For Athena containers)

#### Step 1: Export Container to TAR File

```powershell
# Export running container to image first
& "C:\Program Files\Docker\Docker\resources\bin\docker.exe" commit DOM_and_Grok_Love_Forever dom-grok-backup:latest

# Save image to TAR file
& "C:\Program Files\Docker\Docker\resources\bin\docker.exe" save -o C:\Users\garza\Downloads\dom-grok-backup.tar dom-grok-backup:latest

# Export n8n container
& "C:\Program Files\Docker\Docker\resources\bin\docker.exe" commit docker-n8n-1 n8n-backup:latest
& "C:\Program Files\Docker\Docker\resources\bin\docker.exe" save -o C:\Users\garza\Downloads\n8n-backup.tar n8n-backup:latest

# Export AI node
& "C:\Program Files\Docker\Docker\resources\bin\docker.exe" commit funny_davinci ai-node-backup:latest
& "C:\Program Files\Docker\Docker\resources\bin\docker.exe" save -o C:\Users\garza\Downloads\ai-node-backup.tar ai-node-backup:latest
```

#### Step 2: Transfer TAR Files to Lyra

```powershell
# Using SCP (if Lyra is SSH accessible)
scp C:\Users\garza\Downloads\*.tar user@lyra:/home/user/docker-imports/

# OR using network share
Copy-Item C:\Users\garza\Downloads\*.tar \\lyra\shared\docker-imports\

# OR upload to cloud storage (Google Drive, S3, etc.) then download on Lyra
```

#### Step 3: Import on Lyra

```bash
# On Lyra (Linux/Mac)
docker load -i /home/user/docker-imports/dom-grok-backup.tar
docker load -i /home/user/docker-imports/n8n-backup.tar
docker load -i /home/user/docker-imports/ai-node-backup.tar

# Verify images loaded
docker images
```

#### Step 4: Run Containers on Lyra

```bash
# Run n8n with same port mapping
docker run -d \
  --name n8n-restored \
  -p 5678:5678 \
  -v n8n_data:/home/node/.n8n \
  n8n-backup:latest

# Run AI node
docker run -d \
  --name ai-node-restored \
  -p 5000:5000 \
  ai-node-backup:latest

# Run DOM container (fix crash loop first - see debugging section)
docker run -d \
  --name dom-grok-restored \
  dom-grok-backup:latest
```

---

### Method 2: Docker Compose Migration (For genai-stack)

#### Step 1: Copy genai-stack to Strategic Khaos Project

```powershell
# Copy to your project
Copy-Item -Recurse "C:\Users\garza\Downloads\genai-stack-main\*" "C:\Users\garza\Chaos God DOM_010101\strategic-khaos\genai-stack\"

# Navigate to directory
cd "C:\Users\garza\Chaos God DOM_010101\strategic-khaos\genai-stack"
```

#### Step 2: Configure Environment

```powershell
# Copy example env file
Copy-Item env.example .env

# Edit .env with your settings (use our secrets sanitizer!)
notepad .env
```

**Example .env configuration:**
```env
# Ollama Configuration
OLLAMA_BASE_URL=http://ollama:11434

# LLM Model
LLM=llama3.2
EMBEDDING_MODEL=nomic-embed-text

# Neo4j Configuration
NEO4J_URI=bolt://neo4j:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=[USE_STRONG_PASSWORD_HERE]

# API Configuration
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=[YOUR_LANGCHAIN_API_KEY]
```

#### Step 3: Build and Deploy Locally (Test on Athena First)

```powershell
# Build all services
& "C:\Program Files\Docker\Docker\resources\bin\docker.exe" compose build

# Start all services
& "C:\Program Files\Docker\Docker\resources\bin\docker.exe" compose up -d

# Check status
& "C:\Program Files\Docker\Docker\resources\bin\docker.exe" compose ps

# View logs
& "C:\Program Files\Docker\Docker\resources\bin\docker.exe" compose logs -f
```

#### Step 4: Push to GitHub (For Deployment on Lyra)

```powershell
cd "C:\Users\garza\Chaos God DOM_010101\strategic-khaos"

# Add genai-stack to git
& "C:\Program Files\Git\cmd\git.exe" add genai-stack/

# Commit
& "C:\Program Files\Git\cmd\git.exe" commit -m "Add GenAI Stack for multi-node deployment"

# Push
& "C:\Program Files\Git\cmd\git.exe" push origin master
```

#### Step 5: Deploy on Lyra

```bash
# On Lyra, clone the repo
git clone https://github.com/Me10101-01/strategic-khaos.git
cd strategic-khaos/genai-stack

# Configure environment
cp env.example .env
nano .env  # Edit with Lyra-specific settings

# Deploy with Docker Compose
docker compose up -d

# Check health
docker compose ps
docker compose logs -f
```

---

### Method 3: Docker Registry (Best for Multiple Machines)

#### Step 1: Push Images to Docker Hub

```powershell
# Login to Docker Hub
& "C:\Program Files\Docker\Docker\resources\bin\docker.exe" login

# Tag images with your Docker Hub username
& "C:\Program Files\Docker\Docker\resources\bin\docker.exe" tag dom-grok-backup:latest dom010101/strategic-khaos:dom-grok
& "C:\Program Files\Docker\Docker\resources\bin\docker.exe" tag n8n-backup:latest dom010101/strategic-khaos:n8n
& "C:\Program Files\Docker\Docker\resources\bin\docker.exe" tag ai-node-backup:latest dom010101/strategic-khaos:ai-node

# Push to Docker Hub
& "C:\Program Files\Docker\Docker\resources\bin\docker.exe" push dom010101/strategic-khaos:dom-grok
& "C:\Program Files\Docker\Docker\resources\bin\docker.exe" push dom010101/strategic-khaos:n8n
& "C:\Program Files\Docker\Docker\resources\bin\docker.exe" push dom010101/strategic-khaos:ai-node
```

#### Step 2: Pull on Lyra

```bash
# On Lyra
docker pull dom010101/strategic-khaos:dom-grok
docker pull dom010101/strategic-khaos:n8n
docker pull dom010101/strategic-khaos:ai-node

# Run containers
docker run -d --name dom-grok dom010101/strategic-khaos:dom-grok
docker run -d --name n8n -p 5678:5678 dom010101/strategic-khaos:n8n
docker run -d --name ai-node -p 5000:5000 dom010101/strategic-khaos:ai-node
```

---

## 💾 VOLUME MIGRATION

### Export Volumes from Athena

```powershell
# List all volumes
& "C:\Program Files\Docker\Docker\resources\bin\docker.exe" volume ls

# Backup specific volume (example: n8n_data)
& "C:\Program Files\Docker\Docker\resources\bin\docker.exe" run --rm -v n8n_data:/data -v C:\Users\garza\Downloads:/backup alpine tar czf /backup/n8n_data_backup.tar.gz -C /data .

# Backup AI node volume (if it exists)
& "C:\Program Files\Docker\Docker\resources\bin\docker.exe" run --rm -v ai_data:/data -v C:\Users\garza\Downloads:/backup alpine tar czf /backup/ai_data_backup.tar.gz -C /data .
```

### Import Volumes on Lyra

```bash
# Transfer backup files to Lyra (use scp/network share)
scp C:\Users\garza\Downloads\*_backup.tar.gz user@lyra:/tmp/

# On Lyra, restore volumes
docker volume create n8n_data
docker run --rm -v n8n_data:/data -v /tmp:/backup alpine tar xzf /backup/n8n_data_backup.tar.gz -C /data

docker volume create ai_data
docker run --rm -v ai_data:/data -v /tmp:/backup alpine tar xzf /backup/ai_data_backup.tar.gz -C /data

# Verify volumes
docker volume ls
docker volume inspect n8n_data
```

---

## 🐛 DEBUGGING CRASH-LOOPING CONTAINER

**Issue:** `DOM_and_Grok_Love_Forever` is restarting every 36 seconds.

### Step 1: Check Logs

```powershell
& "C:\Program Files\Docker\Docker\resources\bin\docker.exe" logs DOM_and_Grok_Love_Forever --tail 100
```

### Step 2: Inspect Container

```powershell
& "C:\Program Files\Docker\Docker\resources\bin\docker.exe" inspect DOM_and_Grok_Love_Forever
```

### Step 3: Common Fixes

**If the command is failing:**
```powershell
# Stop the container
& "C:\Program Files\Docker\Docker\resources\bin\docker.exe" stop DOM_and_Grok_Love_Forever

# Remove it
& "C:\Program Files\Docker\Docker\resources\bin\docker.exe" rm DOM_and_Grok_Love_Forever

# Recreate with a stable command
& "C:\Program Files\Docker\Docker\resources\bin\docker.exe" run -d --name DOM_and_Grok_Love_Forever alpine:latest sh -c "while true; do echo 'Love Forever'; sleep 60; done"
```

**If it's a resource issue:**
```powershell
# Run with resource limits
& "C:\Program Files\Docker\Docker\resources\bin\docker.exe" run -d \
  --name DOM_and_Grok_Love_Forever \
  --memory="512m" \
  --cpus="1.0" \
  alpine:latest sh -c "while true; do echo 'Love Forever'; sleep 60; done"
```

---

## 🚀 RECOMMENDED MIGRATION STRATEGY

**For your use case (Athena → Lyra):**

1. ✅ **Use Method 2 (Docker Compose)** for the GenAI stack
   - Clean, reproducible, version-controlled
   - Push to GitHub, pull on Lyra
   - Easy to update and maintain

2. ✅ **Use Method 3 (Docker Registry)** for custom containers
   - n8n workflows
   - AI node
   - DOM containers

3. ✅ **Backup volumes** before migration (safety first)

4. ✅ **Test locally on Athena** before deploying to Lyra

---

## 📝 STEP-BY-STEP EXECUTION PLAN

### Phase 1: Prepare on Athena (30 minutes)

```powershell
# 1. Stop unnecessary containers
& "C:\Program Files\Docker\Docker\resources\bin\docker.exe" stop DOM_and_Grok_Love_Forever funny_davinci docker-n8n-1

# 2. Export containers you want to keep
& "C:\Program Files\Docker\Docker\resources\bin\docker.exe" commit docker-n8n-1 n8n-backup:latest
& "C:\Program Files\Docker\Docker\resources\bin\docker.exe" save -o C:\Users\garza\Downloads\n8n-backup.tar n8n-backup:latest

# 3. Copy genai-stack to strategic-khaos
Copy-Item -Recurse "C:\Users\garza\Downloads\genai-stack-main\*" "C:\Users\garza\Chaos God DOM_010101\strategic-khaos\genai-stack\"

# 4. Commit to GitHub
cd "C:\Users\garza\Chaos God DOM_010101\strategic-khaos"
& "C:\Program Files\Git\cmd\git.exe" add genai-stack/
& "C:\Program Files\Git\cmd\git.exe" commit -m "Add GenAI Stack for deployment"
& "C:\Program Files\Git\cmd\git.exe" push origin master
```

### Phase 2: Transfer to Lyra (varies by method)

**Option A: Network Transfer (if Lyra is accessible)**
```powershell
scp C:\Users\garza\Downloads\n8n-backup.tar user@lyra:/home/user/
```

**Option B: Cloud Storage (if no direct connection)**
```powershell
# Upload to Google Drive, Dropbox, or S3
# Then download on Lyra
```

**Option C: Git Clone (easiest for genai-stack)**
```bash
# On Lyra
git clone https://github.com/Me10101-01/strategic-khaos.git
```

### Phase 3: Deploy on Lyra (20 minutes)

```bash
# On Lyra

# 1. Clone repo (if not done)
git clone https://github.com/Me10101-01/strategic-khaos.git
cd strategic-khaos/genai-stack

# 2. Configure environment
cp env.example .env
nano .env  # Set your API keys, passwords

# 3. Deploy GenAI stack
docker compose up -d

# 4. Import n8n container (if transferred)
docker load -i /home/user/n8n-backup.tar
docker run -d --name n8n -p 5678:5678 -v n8n_data:/home/node/.n8n n8n-backup:latest

# 5. Verify everything is running
docker ps
docker compose logs -f
```

---

## 🔐 SECURITY CHECKLIST

- [ ] Change all default passwords in .env files
- [ ] Use secrets manager for sensitive values (see `docs/SECRETS_MANAGEMENT.md`)
- [ ] Enable firewall rules on Lyra (only expose necessary ports)
- [ ] Set up SSL/TLS for web interfaces (use Caddy or Traefik)
- [ ] Backup volumes regularly (automated cron job)
- [ ] Use Docker secrets instead of environment variables for production
- [ ] Enable Docker content trust (image signing)
- [ ] Scan images for vulnerabilities: `docker scan <image>`

---

## 📊 POST-MIGRATION VERIFICATION

```bash
# On Lyra, run these checks:

# 1. All containers running
docker ps

# 2. Check resource usage
docker stats

# 3. Verify network connectivity
docker network inspect bridge

# 4. Check volumes
docker volume ls

# 5. Test services
curl http://localhost:5678  # n8n
curl http://localhost:5000  # AI node
curl http://localhost:8501  # GenAI stack frontend (if applicable)

# 6. Check logs for errors
docker compose logs --tail=50
```

---

## 🆘 TROUBLESHOOTING

### Container Won't Start on Lyra

```bash
# Check logs
docker logs <container_name>

# Inspect configuration
docker inspect <container_name>

# Verify image exists
docker images

# Check if port is already in use
sudo netstat -tulpn | grep <port>
```

### Volume Data Not Transferring

```bash
# Verify backup exists
ls -lh /tmp/*_backup.tar.gz

# Re-extract manually
docker run --rm -v <volume_name>:/data -v /tmp:/backup alpine sh -c "cd /data && tar xzf /backup/backup.tar.gz"

# Check volume contents
docker run --rm -v <volume_name>:/data alpine ls -la /data
```

### Network Issues Between Containers

```bash
# Create custom network
docker network create strategic-khaos-net

# Run containers on same network
docker run -d --network strategic-khaos-net --name service1 <image>
docker run -d --network strategic-khaos-net --name service2 <image>

# Test connectivity
docker exec service1 ping service2
```

---

## 📚 REFERENCES

- **Docker Documentation:** https://docs.docker.com/
- **Docker Compose:** https://docs.docker.com/compose/
- **GenAI Stack:** https://github.com/docker/genai-stack
- **n8n Docs:** https://docs.n8n.io/
- **Strategic Khaos Repo:** https://github.com/Me10101-01/strategic-khaos

---

**Ready to execute?** Let me know which method you want to use and I'll help you run the commands step-by-step!

— DOM_010101 Migration Guide  
Last Updated: November 19, 2025
