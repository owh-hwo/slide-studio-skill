<#
  slide-studio installer for Claude Code (Windows PowerShell 5.1+ / PowerShell 7)

    .\install.ps1                 install for this user   (%USERPROFILE%\.claude\skills\slide-studio)
    .\install.ps1 -Project        install into this project (.\.claude\skills\slide-studio)
    .\install.ps1 -NoDeps         skip the Python package install
    .\install.ps1 -Uninstall      remove the installed skill

  One-liner (no clone needed):
    irm https://raw.githubusercontent.com/owh-hwo/slide-studio-skill/main/install.ps1 | iex

  An existing install is moved to slide-studio.bak-<timestamp>, never deleted.
#>
param([switch]$Project, [switch]$NoDeps, [switch]$Uninstall)
$ErrorActionPreference = 'Stop'

$RepoUrl = if ($env:SLIDE_STUDIO_REPO) { $env:SLIDE_STUDIO_REPO } else { 'https://github.com/owh-hwo/slide-studio-skill.git' }
$ZipUrl = 'https://github.com/owh-hwo/slide-studio-skill/archive/refs/heads/main.zip'
$Name = 'slide-studio'
$SkillsDir = if ($env:CLAUDE_SKILLS_DIR) { $env:CLAUDE_SKILLS_DIR } else { Join-Path $HOME '.claude\skills' }
if ($Project) { $SkillsDir = Join-Path (Get-Location) '.claude\skills' }
$Dest = Join-Path $SkillsDir $Name

function Say($m) { Write-Host "==> $m" -ForegroundColor Green }
function Warn($m) { Write-Host "!! $m" -ForegroundColor Yellow }

if ($Uninstall) {
  if (Test-Path $Dest) { Remove-Item -Recurse -Force $Dest; Say "removed $Dest" } else { Warn "nothing at $Dest" }
  return
}

# 1. source: this clone, or download the repo
$Tmp = $null
$Here = if ($PSScriptRoot) { $PSScriptRoot } else { $null }
if ($Here -and (Test-Path (Join-Path $Here "$Name\SKILL.md"))) {
  $Src = Join-Path $Here $Name
} else {
  $Tmp = Join-Path ([IO.Path]::GetTempPath()) ("slide-studio-" + [guid]::NewGuid())
  New-Item -ItemType Directory -Force $Tmp | Out-Null
  if (Get-Command git -ErrorAction SilentlyContinue) {
    Say "downloading $RepoUrl"
    git clone --quiet --depth 1 $RepoUrl (Join-Path $Tmp 'repo')
    $Src = Join-Path $Tmp "repo\$Name"
  } else {
    Say "downloading $ZipUrl"
    $zip = Join-Path $Tmp 'repo.zip'
    Invoke-WebRequest -UseBasicParsing $ZipUrl -OutFile $zip
    Expand-Archive $zip -DestinationPath $Tmp
    $Src = Join-Path $Tmp "slide-studio-skill-main\$Name"
  }
}

try {
  # 2. copy (back up any existing install)
  New-Item -ItemType Directory -Force $SkillsDir | Out-Null
  if (Test-Path $Dest) {
    $bak = "$Dest.bak-" + (Get-Date -Format 'yyyyMMdd-HHmmss')
    Move-Item $Dest $bak
    Warn "existing install moved to $bak"
  }
  Copy-Item -Recurse $Src $Dest
  Get-ChildItem $Dest -Recurse -Directory -Filter '__pycache__' | Remove-Item -Recurse -Force
  Say "installed to $Dest"
} finally {
  if ($Tmp) { Remove-Item -Recurse -Force $Tmp -ErrorAction SilentlyContinue }
}

# 3. python + packages
$Py = $null
foreach ($c in @('python', 'py', 'python3')) {
  if (Get-Command $c -ErrorAction SilentlyContinue) {
    & $c -c "import sys; sys.exit(sys.version_info < (3, 8))" 2>$null
    if ($LASTEXITCODE -eq 0) { $Py = $c; break }
  }
}
if (-not $Py) {
  Warn 'Python 3.8+ not found: install it, then run: pip install python-pptx pillow pypdf pypdfium2'
} elseif (-not $NoDeps) {
  Say 'installing Python packages (python-pptx, pillow, pypdf, pypdfium2)'
  & $Py -m pip install --quiet python-pptx pillow pypdf pypdfium2
  if ($LASTEXITCODE -ne 0) { Warn "pip failed: run it yourself: $Py -m pip install python-pptx pillow pypdf pypdfium2" }
}

# 4. Chrome (used headless for checks, rendering and PPTX export)
if ($Py) {
  $scripts = Join-Path $Dest 'scripts'
  $ch = & $Py -c "import sys; sys.path.insert(0, r'$scripts'); import chrome; print(chrome.CHROME)" 2>$null
  if ($LASTEXITCODE -eq 0) { Say "Chrome found: $ch" } else { Warn 'Chrome / Edge not found. Install Google Chrome, or set $env:CHROME to its path' }
}

Write-Host ''
Write-Host 'Done. Restart Claude Code (or start a new session), then ask for slides, e.g.'
Write-Host '  "make a project status deck for the steering committee"   or   /slide-studio'
Write-Host "Theme previews: $Dest\assets\previews\index.html"
