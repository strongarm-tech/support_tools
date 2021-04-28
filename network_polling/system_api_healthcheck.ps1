# Powershell Script for simple polling of network endpoints.

# Instructions:
#
# If the execution policy prevents this script from running,
# please use the following command to temporarily disable the 
# Restricted policy for only this user :
# Set-ExecutionPolicy -ExecutionPolicy Undefined -Scope CurrentUser
# When complete, undo this by seting the default :
# Set-ExecutionPolicy -ExecutionPolicy Restricted -Scope CurrentUser
#
#  if the script fails to run, Review the Local Poliy Editor to enable
#  Computer Configuration -> Policies -> Administrative Templates -> Windows Components -> Windows PowerShell -> "Turn on Script Execution" = Disabled
# Confirm the setting by starting PowerShell and running Get-ExecutionPolicy , the result should be "Unrestricted"
#
# Running this script :  powershell .\system_api_healthcheck.ps1 > log.txt
#
# Press Ctrl+C to stop script.
#
# Review log.txt with an editor when collection complete.
#
# Set DNS so that the cache always expires immediately
[System.Net.ServicePointManager]::DnsRefreshTimeout = 0

# Google Public Nameservers
$publicDNSServer = @('8.8.8.8','8.8.4.4')

function testPing {

    ipconfig /flushdns

    $webResponse = $null;
    $timestamp = Get-Date -Format o;
    Write-Output ($timestamp + ": Start Request to StrongArm Tech HTTPS ping");

    try {
        $webResponse = ( Invoke-WebRequest 'https://dock.strongarmtech.com/prod/ping' -Headers @{"Cache-Control"="no-cache"} -DisableKeepAlive -TimeoutSec 60 -UseBasicParsing -Verbose );
        # This will only execute if the Invoke-WebRequest is successful.
        $StatusCode = $webResponse.StatusCode
        $webResponse.Headers | Where-Object {$_.Keys -eq 'State'}
    }
    catch {
        $StatusCode = $_.Exception.Response.StatusCode.value__;
    }
    $timestampPrev = $timestamp;
    $timestamp = Get-Date -Format o;
    $webResponse.InputFields 
    Write-Output ($timestamp + ": HTTP Response Code:'" + $StatusCode + "' Response:'" + $webResponse +"' RequestTime:'" + (New-TimeSpan -End $timestamp -Start $timestampPrev ) +"'" );
    Write-Output ($timestamp + ': RAWCONTENT:' + ( $webResponse | Select-Object -Expand RawContent) );

    $timestamp = Get-Date -Format o;
    Write-Output ($timestamp + ": Request completed");

}


function test204 {

    ipconfig /flushdns

    $webResponse = $null;
    $timestamp = Get-Date -Format o;
    Write-Output ($timestamp + ": Start Request to StrongArm Tech generate_204 request");

    try {
        $webResponse = ( Invoke-WebRequest 'https://dock.strongarmtech.com/prod/generate-204' -Headers @{"Cache-Control"="no-cache"} -DisableKeepAlive -TimeoutSec 60 -UseBasicParsing -Verbose );
        # This will only execute if the Invoke-WebRequest is successful.
        $StatusCode = $webResponse.StatusCode
        $webResponse.Headers | Where-Object {$_.Keys -eq 'State'}
    }
    catch {
        $StatusCode = $_.Exception.Response.StatusCode.value__;
    }
    $timestampPrev = $timestamp;
    $timestamp = Get-Date -Format o;
    $webResponse.InputFields 
    Write-Output ($timestamp + ": HTTP Response Code:'" + $StatusCode + "' Response:'" + $webResponse +"' RequestTime:'" + (New-TimeSpan -End $timestamp -Start $timestampPrev ) +"'" );
    Write-Output ($timestamp + ': RAWCONTENT:' + ( $webResponse | Select-Object -Expand RawContent) );

    $timestamp = Get-Date -Format o;
    Write-Output ($timestamp + ": Request completed");

}

while( 1 )
{
    testPing;
    test204;
    $timestamp = Get-Date -Format o;
    Write-Output ($timestamp + ": Flushing local DNS Cache")
    ipconfig /flushdns
    $timestamp = Get-Date -Format o;
    Write-Output ($timestamp + ": Resolving dock.strongarmtech.com with DHCP provided nameserver")
    Resolve-DnsName dock.strongarmtech.com

    Write-Output ($timestamp + ": Flushing local DNS Cache")
    ipconfig /flushdns
    $timestamp = Get-Date -Format o;
    Write-Output ($timestamp + ": Resolving dock.strongarmtech.com with Alternate nameserver, 8.8.8.8")
    Resolve-DnsName dock.strongarmtech.com -Server $publicDNSServer

    Start-Sleep 10;
}