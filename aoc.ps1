################################################
#  
# Powershell functions to simplify command line
#
################################################
param(
    [Parameter(Mandatory=$true)]
    [string]$year,
    
    [Parameter(Mandatory=$true)]
    [string]$day
)

# Create global variables to store day and year
$global:aoc_year = $year
$global:aoc_day = $day

# execute solution.py
function global:run { 
    python -m "$global:aoc_year.$global:aoc_day.solution" 
}

# check solution.py
function global:check { 
    pylint "$global:aoc_year/$global:aoc_day/solution.py" 
}

# show files
function global:show {
    ls $global:aoc_year/$global:aoc_day/
}

# clean up
function global:clean {
    $files = @(
        "$global:aoc_year\$global:aoc_day\*.txt",
        "$global:aoc_year\$global:aoc_day\script.py",
        "$global:aoc_year\$global:aoc_day\test.py",
        "$global:aoc_year\$global:aoc_day\stole.py"
    )

    foreach ($file in $files) {
        if (Test-Path $file) {
            Remove-Item $file -Force
            Write-Host "Removed: $file"
        } else {
            Write-Host "File not found: $file"
        }
    }
}

# push changes to github
function global:push {
    clean 
    git commit -a -m "$global:aoc_year $global:aoc_day"
    git push
}
Write-Host "Functions 'run' and 'check' have been defined for year $global:aoc_year, day $global:aoc_day."
Write-Host "Use 'run' to execute the solution,'check' to run pylint and 'push' to update github."
Write-Host "The variables 'aoc_year' and 'aoc_day' are now available globally."


$reminderFile = ".reminder"

if (Test-Path $reminderFile) {
    Get-Content $reminderFile
    $configFile = ".\.aoc.cfg.json"

    if (Test-Path $configFile) {
        $config = Get-Content $configFile | ConvertFrom-Json
        
        if ($config.editor) {
            Write-Host "Opening editor: $($config.editor)"
            Start-Process $config.editor $reminderFile
        } else {
            Write-Host "Editor path not found in the configuration file."
        }
    } else {
        Write-Host "Configuration file '$configFile' not found."
    }
} else {
    Write-Host "The file '$reminderFile' does not exist in the current directory."
}

show