#!/usr/bin/env python3
"""
DOM_010101 Copyright Header Injector
Adds copyright headers to all source files for legal protection
"""

from pathlib import Path
from datetime import datetime

COPYRIGHT_TEMPLATES = {
    'python': '''"""
Copyright (c) {year} Domenic Garza (DOM_010101)
Project: Strategic Khaos
Repository: https://github.com/Me10101-01/strategic-khaos

This file is part of Strategic Khaos.

Strategic Khaos is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Strategic Khaos is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with Strategic Khaos. If not, see <https://www.gnu.org/licenses/>.
"""
''',
    'javascript': '''/**
 * Copyright (c) {year} Domenic Garza (DOM_010101)
 * Project: Strategic Khaos
 * Repository: https://github.com/Me10101-01/strategic-khaos
 * 
 * This file is part of Strategic Khaos.
 * 
 * Strategic Khaos is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 */
''',
    'powershell': '''# Copyright (c) {year} Domenic Garza (DOM_010101)
# Project: Strategic Khaos
# Repository: https://github.com/Me10101-01/strategic-khaos
# 
# Licensed under GNU Affero General Public License v3.0
# See: https://www.gnu.org/licenses/agpl-3.0.html
''',
    'bash': '''# Copyright (c) {year} Domenic Garza (DOM_010101)
# Project: Strategic Khaos
# Repository: https://github.com/Me10101-01/strategic-khaos
# 
# Licensed under GNU Affero General Public License v3.0
# See: https://www.gnu.org/licenses/agpl-3.0.html
''',
}

FILE_EXTENSIONS = {
    '.py': 'python',
    '.js': 'javascript',
    '.ts': 'javascript',
    '.ps1': 'powershell',
    '.sh': 'bash',
}

def has_copyright_header(content: str) -> bool:
    """Check if file already has copyright header"""
    return 'Copyright (c)' in content[:500] or 'DOM_010101' in content[:500]

def inject_copyright_headers(root_dir: str = '.', dry_run: bool = True):
    """Add copyright headers to all source files"""
    root = Path(root_dir)
    year = datetime.now().year
    
    stats = {'checked': 0, 'updated': 0, 'skipped': 0}
    
    print(f"🔒 DOM_010101 Copyright Header Injector")
    print(f"📁 Scanning: {root.absolute()}")
    print(f"{'🔍 DRY RUN MODE' if dry_run else '✍️  WRITE MODE'}")
    print("="*60)
    
    # Find all source files
    for ext, lang in FILE_EXTENSIONS.items():
        pattern = f"**/*{ext}"
        files = list(root.glob(pattern))
        
        print(f"\n📝 {lang.upper()} files ({ext}):")
        
        for file_path in files:
            # Skip certain directories
            if any(skip in str(file_path) for skip in ['.git', 'node_modules', '.venv', '__pycache__']):
                continue
            
            stats['checked'] += 1
            
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                if has_copyright_header(content):
                    print(f"   ✅ {file_path.name} (already has header)")
                    stats['skipped'] += 1
                    continue
                
                # Add header
                header = COPYRIGHT_TEMPLATES[lang].format(year=year)
                
                # Handle shebangs
                if content.startswith('#!'):
                    lines = content.split('\n', 1)
                    new_content = lines[0] + '\n' + header + '\n' + (lines[1] if len(lines) > 1 else '')
                else:
                    new_content = header + '\n' + content
                
                if not dry_run:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"   📝 {file_path.name} (header added)")
                else:
                    print(f"   🔍 {file_path.name} (would add header)")
                
                stats['updated'] += 1
                
            except Exception as e:
                print(f"   ❌ {file_path.name} (error: {e})")
    
    print("\n" + "="*60)
    print(f"📊 Summary:")
    print(f"   Checked: {stats['checked']}")
    print(f"   Updated: {stats['updated']}")
    print(f"   Skipped: {stats['skipped']}")
    
    if dry_run:
        print(f"\n💡 Run with --write to actually add headers")

if __name__ == '__main__':
    import sys
    
    dry_run = '--write' not in sys.argv
    inject_copyright_headers(dry_run=dry_run)
