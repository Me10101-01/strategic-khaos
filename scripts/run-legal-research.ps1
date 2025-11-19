# DOM_010101 Legal Research Runner
# Run this to collect 100+ legal sources for IP protection

$pythonCmd = "C:\Users\garza\Miniconda3\python.exe"
$scriptPath = "C:\Users\garza\Chaos God DOM_010101\strategic-khaos\scripts\legal-research-aggregator.py"

Write-Host "🧠⚖️  DOM_010101 LEGAL RESEARCH AGGREGATOR" -ForegroundColor Cyan
Write-Host "="*60 -ForegroundColor Gray
Write-Host ""
Write-Host "This will collect 100+ legal sources on:" -ForegroundColor Yellow
Write-Host "  ✓ Open source IP protection" -ForegroundColor Green
Write-Host "  ✓ Trademark/copyright enforcement cases WON" -ForegroundColor Green
Write-Host "  ✓ Defamation law precedents" -ForegroundColor Green
Write-Host "  ✓ DAO/LLC structure case law" -ForegroundColor Green
Write-Host "  ✓ License violation remedies" -ForegroundColor Green
Write-Host "  ✓ Anti-SLAPP protections" -ForegroundColor Green
Write-Host "  ✓ Trade secret protection" -ForegroundColor Green
Write-Host ""
Write-Host "Sources: Google Scholar, Justia, govinfo.gov, Cornell LII, SSRN" -ForegroundColor Cyan
Write-Host "Estimated time: ~15-20 minutes (rate-limited for ethics)" -ForegroundColor Gray
Write-Host ""
Write-Host "="*60 -ForegroundColor Gray
Write-Host ""

$response = Read-Host "Start research? (y/n)"

if ($response -eq 'y' -or $response -eq 'Y') {
    Write-Host "`nStarting legal research..." -ForegroundColor Green
    & $pythonCmd $scriptPath
    
    Write-Host "`n✅ Research complete! Check research/legal/ directory" -ForegroundColor Green
} else {
    Write-Host "Cancelled." -ForegroundColor Yellow
}
