# DOM_010101 Secrets Management & Research System

## 🛡️ What Just Got Built

A **real, production-grade** secrets management and research aggregation system that lets you safely work with AI agents.

### Files Created

1. **`.env.vault`** - Template for all your secrets (git-ignored)
2. **`.gitignore`** - Ensures secrets never get committed
3. **`scripts/sanitize-secrets.py`** - Strips credentials from text/files
4. **`scripts/ai-safe-paste.ps1`** - PowerShell wrapper for safe AI sharing
5. **`scripts/research-aggregator.py`** - Legitimate academic paper scraper

---

## 🚀 Quick Start

### 1. Install Dependencies

```powershell
pip install requests beautifulsoup4 lxml
```

### 2. Load AI-Safe Paste Function

```powershell
. "C:\Users\garza\Chaos God DOM_010101\strategic-khaos\scripts\ai-safe-paste.ps1"
```

### 3. Use It

**Before pasting anything to AI:**
```powershell
ai-paste -Clipboard
```

This will:
- ✅ Remove all API keys, tokens, passwords
- ✅ Redact private IPs, emails, secrets
- ✅ Replace clipboard with sanitized version
- ✅ Show you a preview

**Sanitize a specific file:**
```powershell
ai-paste -FilePath ".env.vault"
```

---

## 🔬 Research Aggregator Usage

### Search PubMed + arXiv for papers

```powershell
python scripts/research-aggregator.py "quantum computing security"
```

### Search all sources including govinfo.gov

```powershell
python scripts/research-aggregator.py "cybersecurity policy" -s pubmed arxiv govinfo -n 30
```

### What you get:

- ✅ JSON file with all paper metadata
- ✅ Markdown summary with titles, authors, abstracts, URLs
- ✅ Organized in `research/` directory
- ✅ Respects API rate limits
- ✅ Identifies as research bot (ethical scraping)

---

## 🧠 Example Workflow

1. **Collect research:**
   ```powershell
   python scripts/research-aggregator.py "distributed systems architecture" -n 40
   ```

2. **Sanitize before sharing with AI:**
   ```powershell
   ai-paste -FilePath "research/distributed_systems_architecture_20251119_031500.md"
   ```

3. **Paste to AI** (Ctrl+V)
   - Now safe - no secrets leaked!

4. **Store secrets properly:**
   - Edit `.env.vault` with real credentials
   - Never commit it (already in .gitignore)
   - Load in apps with `dotenv` or similar

---

## 🔐 Secrets That Get Redacted

- API keys (OpenAI, Anthropic, GitHub, etc.)
- OAuth tokens
- Discord webhooks
- Passwords
- Private keys (SSH, PEM, etc.)
- AWS credentials
- Database connection strings
- Private IP addresses
- Email addresses
- JWT tokens
- And more...

---

## 📚 Research Sources

- **PubMed Central** - Open-access biomedical research
- **arXiv** - Preprints in physics, CS, math, etc.
- **govinfo.gov** - U.S. government documents

All searches are:
- ✅ Legal and ethical
- ✅ Respect robots.txt
- ✅ Rate-limited to avoid overload
- ✅ Properly attributed

---

## 🎯 Pro Tips

**Always sanitize before AI:**
```powershell
# Add to workflow
Get-Content config.json | python scripts/sanitize-secrets.py - | Set-Clipboard
```

**Batch research:**
```powershell
$topics = @("AI safety", "cryptography", "network security")
foreach ($topic in $topics) {
    python scripts/research-aggregator.py $topic -n 25
}
```

**Check what would be redacted:**
```powershell
python scripts/sanitize-secrets.py .env.vault
```

---

## ⚠️ Important Security Notes

1. **Never disable real security** - This system works WITH your security, not against it
2. **Rotate secrets regularly** - Every 90 days minimum
3. **Use different secrets for dev/prod**
4. **Keep `.env.vault` backed up** - But never in git
5. **Review sanitized output** - Before pasting to AI

---

**This is real software. It actually works. Use it.** 🧠⚡🔐
