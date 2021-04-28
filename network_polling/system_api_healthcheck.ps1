# Powershell Script for simple polling.

# If the execution policy prevents this script from running,
# please use the following command to temporarily disable the 
# Restricted policy for only this user :
# Set-ExecutionPolicy -ExecutionPolicy Undefined -Scope CurrentUser
# When complete, undo this by seting the default :
# Set-ExecutionPolicy -ExecutionPolicy Restricted -Scope CurrentUser

# Set DNS so that the cache always expires immediately
[System.Net.ServicePointManager]::DnsRefreshTimeout = 0


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

    Start-Sleep 10;
}