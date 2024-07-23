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

# push changes to github
function global:push { 
    git commit -a -m "$global:aoc_year $global:aoc_day"
    git push
}
Write-Host "Functions 'run' and 'check' have been defined for year $global:aoc_year, day $global:aoc_day."
Write-Host "Use 'run' to execute the solution,'check' to run pylint and 'push' to update github."
Write-Host "The variables 'aoc_year' and 'aoc_day' are now available globally."