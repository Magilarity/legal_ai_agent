Param([string]$url = "http://localhost:8501")
$resp = Invoke-WebRequest -Uri $url -UseBasicParsing
if ($resp.StatusCode -ne 200) {
  Write-Error "Smoke test failed: HTTP $($resp.StatusCode)"
  exit 1
}
Write-Host "Smoke test passed: HTTP $($resp.StatusCode)"