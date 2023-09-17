$python_command = (Get-Command python.exe -ErrorAction SilentlyContinue).Source

if ($python_command -eq $null) {
    Write-Host "Error: The Python interpreter 'python.exe' is not found in your PATH."
    exit 1
}

if (-not (Test-Path $python_command)) {
    Write-Host "Error: The specified Python executable path '$python_command' does not exist."
    exit 1
}

if (-not (Test-Path .venv)) {
    Write-Host "Creating a new virtual environment..."
    python -m venv .venv
    .\.venv\Scripts\Activate
} else {
    Write-Host "Using existing virtual environment."
}

$python_in_venv = ".\.venv\Scripts\python"

if ($setup_venv -eq "yes") {
    if (-not (Test-Path (Get-Command virtualenv -ErrorAction SilentlyContinue))) {
        Write-Host "Error: virtualenv is not installed. Please install it and rerun this script."
        exit 1
    }

    python -m venv .venv
    .\.venv\Scripts\Activate
}

# Now, use the Python interpreter within the virtual environment for subsequent commands.
$python_in_venv = ".\.venv\Scripts\python"

# For example:
& $python_in_venv -m pip install -r requirements.txt

$secret_key = (python manage.py shell -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
@"
SECRET_KEY=$secret_key
DEBUG=False
ALLOWED_HOSTS=*.ku.th,localhost,127.0.0.1,::1
TIME_ZONE=Asia/Bangkok
EMAIL_HOST_PASSWORD=ineedmorebullets
"@ | Set-Content -Path .env

$text = @"
Django is now running in insecure mode for the static files gathering reason.
You can stop the server and run it again
"@
$boxWidth = ($text | Measure-Object -Property Length -Maximum).Maximum + 4
$topBorder = '+' + ('-' * ($boxWidth - 2)) + '+'
$sideBorder = '| ' + $text + (' ' * ($boxWidth - $text.Length - 4)) + ' |'
$bottomBorder = '+' + ('-' * ($boxWidth - 2)) + '+'

Write-Host $topBorder
Write-Host $sideBorder
Write-Host $bottomBorder


python manage.py migrate
python manage.py loaddata data/users.json
python manage.py loaddata data/polls.json
python manage.py loaddata data/vote.json
python manage.py runserver --insecure