# Nibbling Tales

*Winnie-the-Pooh*, read aloud one chapter at a time.

## Releasing a chapter

1. Compress the recording (a 15-minute WAV goes from ~75 MB to ~7 MB with no audible loss for voice):

   ```
   ffmpeg -i WTP_Ch2.wav -ac 1 -codec:a libmp3lame -b:a 64k audio/02-pooh-gets-stuck.mp3
   ```

   Use the exact filename listed for that chapter in `stories.js`.
2. In `stories.js`, change that chapter's `status: "soon"` to `status: "ready"` and set `minutes`.
3. Commit and push. GitHub Pages updates in a minute or two.

To tease the next one, set its `soonText` (e.g. `"Coming Saturday!"`).

The welcome note card is hidden until `welcome.status` is `"ready"` and `audio/00-welcome.mp3` exists.

## What the page remembers

Per device, in the browser: which chapters have been heard (filled honey pots), where each story was paused, and which new chapters have already had their bee welcome. Nothing is sent anywhere.

## Credits

*Winnie-the-Pooh* by A. A. Milne (1926); drawings by E. H. Shepard from the 1926 edition, via [Project Gutenberg eBook #67098](https://www.gutenberg.org/ebooks/67098). Both are public domain in the US.
