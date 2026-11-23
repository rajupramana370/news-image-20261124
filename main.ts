import { copyFileSync, existsSync, mkdirSync, readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// news-image-20261124: copy the pre-drawn front page (entry.png, drawn by
// draw_news.py from the verified news of Tuesday 24 November 2026) to the
// output directory make.fun asks for. Deterministic: a plain byte copy,
// so repeated runs write identical files. The copy is verified byte for
// byte before success is reported: a truncated or corrupted copy would
// silently ship a broken front page, so any mismatch aborts the run.
const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR;
if (!outDir) {
  throw new Error("MAKEFUN_OUTPUT_DIR is not set");
}
mkdirSync(outDir, { recursive: true });
const source = join(here, "entry.png");
if (!existsSync(source)) {
  throw new Error("entry.png is missing from the repository");
}
const target = join(outDir, "entry.png");
copyFileSync(source, target);
const expected = readFileSync(source);
const written = readFileSync(target);
if (!written.equals(expected)) {
  throw new Error(
    `copied entry.png does not match the source (${written.length} vs ${expected.length} bytes)`,
  );
}
console.log(`entry.png copied and verified (${written.length} bytes)`);
