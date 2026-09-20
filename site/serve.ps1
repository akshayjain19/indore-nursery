# Indore Nursery - local preview server (http://localhost:8080)
$root = $PSScriptRoot
$listener = New-Object System.Net.HttpListener
$listener.Prefixes.Add("http://localhost:8080/")
$listener.Start()
Write-Host "Serving Indore Nursery at http://localhost:8080  (press Ctrl+C or close this window to stop)"
Start-Process "http://localhost:8080/"
$mime = @{".html"="text/html; charset=utf-8"; ".htm"="text/html; charset=utf-8"; ".css"="text/css"; ".js"="text/javascript"; ".jpg"="image/jpeg"; ".jpeg"="image/jpeg"; ".png"="image/png"; ".webp"="image/webp"; ".gif"="image/gif"; ".svg"="image/svg+xml"; ".ico"="image/x-icon"; ".txt"="text/plain; charset=utf-8"; ".xml"="text/xml"}
while ($listener.IsListening) {
  $ctx = $listener.GetContext()
  try {
    $raw = $ctx.Request.Url.AbsolutePath
    if ($raw -eq "/") { $raw = "/index.html" }
    elseif ($raw.EndsWith("/")) { $raw = $raw + "index.html" }
    $cand = @($raw, [Uri]::UnescapeDataString($raw)) | Select-Object -Unique
    $file = $null
    foreach ($c in $cand) {
      $f = Join-Path $root ($cand[0].TrimStart("/") -replace "/", "\")
      $f2 = Join-Path $root ([Uri]::UnescapeDataString($cand[0]).TrimStart("/") -replace "/","\")
      if (Test-Path -LiteralPath $f -PathType Leaf) { $file = $f; break }
      if (Test-Path -LiteralPath $f2 -PathType Leaf) { $file = $f2; break }
    }
    if (-not $file) {
      $ctx.Response.StatusCode = 404
      $msg = [Text.Encoding]::UTF8.GetBytes("<h1>404 - Page not found</h1>")
      $ctx.Response.OutputStream.Write($msg,0,$msg.Length); $ctx.Response.Close(); continue
    }
    $ext = [IO.Path]::GetExtension($file).ToLower()
    if ($mime.ContainsKey($ext)) { $ctx.Response.ContentType = $mime[$ext] }
    $bytes = [IO.File]::ReadAllBytes($file)
    $ctx.Response.ContentLength64 = $bytes.Length
    $ctx.Response.OutputStream.Write($bytes,0,$bytes.Length)
    $ctx.Response.Close()
  } catch { try { $ctx.Response.Close() } catch {} }
}
