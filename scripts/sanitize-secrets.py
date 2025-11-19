#!/usr/bin/env python3
"""
DOM_010101 Secrets Sanitizer
Strips sensitive data before pasting to AI agents
"""

import re
import sys
from pathlib import Path

# Patterns that indicate secrets (case-insensitive)
SECRET_PATTERNS = [
    # GitHub tokens (must be first - more specific)
    (r'gh[pso]_[a-zA-Z0-9]{36,}', '[GITHUB_TOKEN_REDACTED]'),
    
    # API Keys & Tokens
    (r'(api[_-]?key|apikey)\s*[=:]\s*([^\s"\']+)', r'\1=[API_KEY_REDACTED]'),
    (r'(token|access[_-]?token)\s*[=:]\s*([^\s"\']+)', r'\1=[TOKEN_REDACTED]'),
    (r'(secret|client[_-]?secret)\s*[=:]\s*([^\s"\']+)', r'\1=[SECRET_REDACTED]'),
    
    # OAuth tokens
    (r'(bearer|oauth)[_-]?token\s*[=:]\s*([^\s"\']+)', r'\1_token=[OAUTH_TOKEN_REDACTED]'),
    
    # Discord webhooks
    (r'https://discord\.com/api/webhooks/[\d]+/[a-zA-Z0-9_\-]+', '[DISCORD_WEBHOOK_REDACTED]'),
    
    # Passwords
    (r'(password|passwd|pwd)\s*[=:]\s*([^\s"\']+)', r'\1=[PASSWORD_REDACTED]'),
    
    # Private keys
    (r'-----BEGIN [A-Z ]+PRIVATE KEY-----[\s\S]+?-----END [A-Z ]+PRIVATE KEY-----', '[PRIVATE_KEY_REDACTED]'),
    
    # AWS keys
    (r'AKIA[0-9A-Z]{16}', '[AWS_ACCESS_KEY_REDACTED]'),
    (r'aws_secret_access_key\s*[=:]\s*([^\s"\']+)', 'aws_secret_access_key=[AWS_SECRET_REDACTED]'),
    
    # Database connection strings
    (r'(postgresql|mysql|mongodb)://[^:]+:[^@]+@[^\s]+', '[DB_CONNECTION_REDACTED]'),
    
    # IP addresses (optional - only private ranges)
    (r'\b10\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', '[PRIVATE_IP_REDACTED]'),
    (r'\b192\.168\.\d{1,3}\.\d{1,3}\b', '[PRIVATE_IP_REDACTED]'),
    (r'\b172\.(1[6-9]|2[0-9]|3[0-1])\.\d{1,3}\.\d{1,3}\b', '[PRIVATE_IP_REDACTED]'),
    
    # Email addresses (optional)
    (r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL_REDACTED]'),
    
    # JWT tokens
    (r'eyJ[a-zA-Z0-9_\-]+\.eyJ[a-zA-Z0-9_\-]+\.[a-zA-Z0-9_\-]+', '[JWT_REDACTED]'),
]


def sanitize_text(text: str) -> str:
    """Remove all sensitive patterns from text"""
    sanitized = text
    
    for pattern, replacement in SECRET_PATTERNS:
        sanitized = re.sub(pattern, replacement, sanitized, flags=re.IGNORECASE | re.MULTILINE)
    
    return sanitized


def sanitize_file(filepath: Path) -> str:
    """Sanitize a file and return clean content"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        return sanitize_text(content)
    except Exception as e:
        return f"[ERROR: Could not read {filepath}: {e}]"


def main():
    if len(sys.argv) < 2:
        print("Usage: python sanitize-secrets.py <file_or_text>")
        print("   or: echo 'text with secrets' | python sanitize-secrets.py -")
        sys.exit(1)
    
    # Set UTF-8 encoding for Windows console output
    if sys.platform == 'win32':
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    
    input_arg = sys.argv[1]
    
    # Read from stdin
    if input_arg == '-':
        text = sys.stdin.read()
        print(sanitize_text(text), end='')
    
    # Read from file
    elif Path(input_arg).exists():
        filepath = Path(input_arg)
        print(sanitize_file(filepath), end='')
    
    # Treat as raw text
    else:
        print(sanitize_text(input_arg), end='')


if __name__ == '__main__':
    main()
