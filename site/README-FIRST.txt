INDORE NURSERY - STATIC WEBSITE (local preview copy)
====================================================

What's inside
- 547 pages: Home, All Plants (241 product pages), 12 category pages,
  304 blog articles, Events & Decor, About, Contact
- Full image library (site/images)
- sitemap.xml + robots.txt
- All links, prices and WhatsApp enquiry buttons work exactly as they will on the live site

HOW TO VIEW IT LOCALLY (Windows)
--------------------------------
1. Extract this zip to any folder (right-click > Extract All).
2. Double-click  Start-Website.bat
   - A PowerShell window opens running a tiny local web server on port 8080.
   - Your browser opens automatically at  http://localhost:8080
3. Browse the site. Clicking around works (plants, categories, blog...).
4. To stop: just close the PowerShell window.

If double-clicking the .bat is blocked:
  - Open PowerShell in this folder and run:
      powershell -ExecutionPolicy Bypass -File .\serve.ps1

NOTES
- This is a preview only - nothing is published online and the old
  indorenursery.com website was not touched.
- Pages are plain HTML + CSS (no database needed), so this exact folder
  can later be uploaded to any static host.
- all_images.txt is the image manifest (flat name -> original URL on the old site).
