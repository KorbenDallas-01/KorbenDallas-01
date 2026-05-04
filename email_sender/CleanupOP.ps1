$nexfolder_path = 'C:\Users\IBE\Desktop\certs\archive'
$certs_path = 'C:\Users\IBE\Desktop\certs\pdfs'

#next folder creation
$last_fn = Get-ChildItem -Path $nexfolder_path -Directory |Sort-Object {[int]($_.name -replace 'A','')} -Descending|
           select name -ExpandProperty name |select -First 1 |ForEach-Object {$_ -replace 'A',''}
New-Item -Path $nexfolder_path -Name "A$([int]$last_fn+1)" -ItemType Directory
$destination = Join-Path -Path $nexfolder_path -ChildPath $("A$([int]$last_fn+1)")

Get-ChildItem -Path $certs_path -File | Move-Item -Destination $destination
Move-Item -Path $(Join-Path -Path 'C:\Users\IBE\Desktop\certs' -ChildPath 'outlist.csv') `
          -Destination $destination
$cvs = "$HOME\Downloads\wysylkaScript - Arkusz3.csv"
$csv_to_move = 'C:\Users\IBE\Desktop\certs\NamesList.csv'
Rename-Item -LiteralPath $cvs -NewName NamesList.csv 
if(Test-Path $csv_to_move){
Move-Item -LiteralPath $csv_to_move -Destination 'C:\Users\IBE\Desktop\certs\temp' -Force}
else{Write-Host "no NAMESLIST in cert folder"}
Move-Item "$HOME\Downloads\NamesList.csv" -Destination 'C:\Users\IBE\Desktop\certs'

$DownloadsPath = "$env:USERPROFILE\Downloads"
$DestinationPath = "$env:USERPROFILE\Desktop\certs\pdfs"

# Find the first matching zip file (including subfolders if needed)
$ZipFile = Get-ChildItem $DownloadsPath -Recurse -Filter "*drive-download*.zip" | Select-Object -First 1

if ($ZipFile) {
    $MovedZipPath = Join-Path $DestinationPath $ZipFile.Name

    # Move the zip file
    Move-Item $ZipFile.FullName $MovedZipPath -Force

    # Extract contents directly into destination folder
    Expand-Archive -Path $MovedZipPath -DestinationPath $DestinationPath -Force

    Write-Host "ZIP moved and extracted successfully."
    Get-ChildItem $DestinationPath -Recurse -Filter "*drive-download*.zip"|Remove-Item

} 
else {
    Write-Host "No matching ZIP file found."
}
python.exe "C:\Users\IBE\Desktop\python_adv\Automation\sort-pdf.py"


#$var = $()
#$var+= -join ([char[]](([char]65..[char]90)+([char]97..[char]122))+(0..cd 9)|Get-Random -Count 13)