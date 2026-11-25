# M3U Playlist Studio 1.0

A small static M3U/M3U8 playlist organizer with a scheduled catalog refresh.

## Files
- `index.html`: browser UI; imports M3U files and exports selected entries.
- `scanner.py`: downloads and parses configured playlist sources; deduplicates stream URLs.
- `sources.json`: allow-list of public sources you choose to use.
- `catalog.json`: generated catalog consumed by the web app.
- `.github/workflows/daily-update.yml`: runs every day at 03:17 UTC and can be run manually.

## Setup
1. Create a new GitHub repository, for example `m3u-playlist-studio`.
2. Upload all files and folders from this project, preserving `.github/workflows/daily-update.yml`.
3. In GitHub, open Actions and enable workflows if prompted.
4. Run **Daily M3U catalog update** once manually from Actions > workflow > Run workflow.
5. In Netlify, import the repository. Publish directory: `/` (no build command).
6. After the first catalog is generated and deployed, the site displays the catalog. For updates to appear on Netlify, connect the repository to Netlify so commits trigger deploys.

## Notes
- The workflow runs on GitHub-hosted runners; scheduled jobs may be delayed by GitHub.
- GitHub Actions has usage limits; check current plan limits in your account.
- Only add sources you are authorized to access and redistribute. This starter project does not discover arbitrary servers, bypass authentication, or access paid/private streams.
- A stream marked as listed is not guaranteed to be online; this version does not actively probe each stream because probing large catalogs can overload third-party servers. Add a rate-limited checker only for streams you are authorized to test.
