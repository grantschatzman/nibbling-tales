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

### Scene markers (optional)

In Audacity, click where a scene starts and press **Ctrl+B**, then type a short name ("The Balloon") and press Enter. Repeat for each scene; add one at 0:00 for the opening scene. Then **File → Export → Export Labels…** and save it into `audio/` with the same name as the mp3 but ending `.txt` (e.g. `audio/01-pooh-and-some-bees.txt`). The page picks it up automatically: ticks on the progress bar and tap-to-jump scene buttons. A label named just `page` is reserved and ignored.

### Page labels (for "turn the page" mode, coming later)

Open `recording-script.html` (on the site, or locally) and read from it. At every honey bar, press **Ctrl+B** and type `page`, right before the first word of that page. Page 1 needs no label. They go in the same labels file as the scene markers.

The pages are fixed by `tools/build-text.py`: every Shepard drawing starts a page, pages over 250 words are split evenly at paragraph breaks, and a drawing that ends a chapter joins the last page. Don't re-run it with different settings after recording, or the labels won't line up.

To tease the next one, set its `soonText` (e.g. `"Coming Saturday!"`).

The welcome note card is hidden until `welcome.status` is `"ready"` and `audio/00-welcome.mp3` exists.

## Previewing locally

```
npx http-server -p 8765 -c-1
```

then open http://localhost:8765. Don't use `python -m http.server`: it can't serve part of a file, so the audio can't jump and page turns, scene buttons and the progress bar all snap back to the start. `-c-1` turns off caching so edits show up on refresh.

## What the page remembers

Per device, in the browser: which chapters have been heard (filled honey pots), where each story was paused, and which new chapters have already had their bee welcome. Nothing is sent anywhere.

## Credits

*Winnie-the-Pooh* by A. A. Milne (1926); drawings by E. H. Shepard from the 1926 edition, via [Project Gutenberg eBook #67098](https://www.gutenberg.org/ebooks/67098). Both are public domain in the US.
