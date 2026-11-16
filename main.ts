// "A colossal koi leaping out of a tiny goldfish bowl" — ai-excited-01
// entry v1 (Node 22, standard library only). The artwork is the entry.png
// beside this file: a flat vector-style illustration drawn in code
// (compose.py, included) of one giant white-and-orange koi arcing out of
// a small round fishbowl on a windowsill, water exploding toward the
// viewer, golden-hour sun against a deep teal background. No text in the
// image — the scale contrast (huge fish, tiny bowl) is the whole idea.
// PNG, 1024 by 1024 pixels, 211,227 bytes. The program copies it to
// /output/entry.png. The gate takes a whole PNG or JPEG of at most 1 MiB
// and 1024 by 1024 pixels, and the judge sees exactly the bytes copied.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from 'node:fs';
import { dirname, join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
copyFileSync(
  new URL('./entry.png', import.meta.url),
  join(outDir, 'entry.png'),
);
console.log('wrote', join(outDir, 'entry.png'));
