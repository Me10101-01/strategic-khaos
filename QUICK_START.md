# 🚀 Quick Start - DOM_010101 Secrets Management

## Load the function (do this once per PowerShell session)

```powershell
cd "C:\Users\garza\Chaos God DOM_010101\strategic-khaos"
. .\scripts\ai-safe-paste.ps1
```

## Usage Examples

### Sanitize whatever's in your clipboard:
```powershell
ai-paste -Clipboard
```

### Sanitize a specific file:
```powershell
ai-paste -FilePath ".env.vault"
```

### Test it:
```powershell
# Copy this sensitive data
"GitHub token: ghp_1234567890abcdefghijklmnopqrstuvwxyz123456
API Key: sk-test123456
password=SuperSecret2024
Discord webhook: https://discord.com/api/webhooks/123456/abcdef" | Set-Clipboard

# Sanitize it
ai-paste -Clipboard

# Now paste (Ctrl+V) - all secrets redacted!
```

## What Gets Redacted

✅ GitHub tokens (ghp_, gho_, ghs_)  
✅ API keys  
✅ Passwords  
✅ Discord webhooks  
✅ AWS credentials  
✅ Private keys (PEM, SSH)  
✅ JWT tokens  
✅ Database connection strings  
✅ Private IP addresses  
✅ Email addresses

## Pro Tips

**Add to your PowerShell profile** (auto-load on every session):
```powershell
notepad $PROFILE
```

Add this line:
```powershell
. "C:\Users\garza\Chaos God DOM_010101\strategic-khaos\scripts\ai-safe-paste.ps1"
```

**Before pasting ANYTHING to AI:**
1. Ctrl+C (copy)
2. Run `ai-paste -Clipboard`
3. Ctrl+V (paste) - now safe!

**Your secrets stay secret. The AI gets context.** 🔐🧠
