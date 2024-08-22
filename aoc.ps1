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

function global:run_high { 
    $scriptPath = "$global:aoc_year.$global:aoc_day.solution"
    
    # Start the process in the current window and wait for it to finish
    $process = Start-Process -FilePath "python" -ArgumentList "-m $scriptPath" -NoNewWindow -PassThru -Wait

    # Set the priority (Normal, Idle, BelowNormal, AboveNormal, High, RealTime)
    $process.PriorityClass = "High"
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

function global:process_all {
    param (
        [scriptblock]$command
    )

    # Loop through directories matching 2*
    foreach ($yearDir in Get-ChildItem -Directory -Name -Filter "2*") {
        # Set the global variable aoc_year to the directory name
        $global:aoc_year = $yearDir
        Write-Host "Set global:aoc_year to $global:aoc_year"
        
        # Loop through subdirectories named 1 to 25
        foreach ($day in 1..25) {
            $dayDir = "$yearDir\$day"
            if (Test-Path -Path $dayDir -PathType Container) {
                # Set the global variable aoc_day to the directory number
                $global:aoc_day = $day
                Write-Host "Set global:aoc_day to $global:aoc_day for directory $dayDir"
                & $command
            }
        }
    }
}

function global:run_all {
    global:process_all { run }
}

function global:check_all {
    global:process_all { check }
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