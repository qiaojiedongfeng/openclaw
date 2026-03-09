import { createHash } from "node:crypto";
import fs from "node:fs/promises";
import fsSync from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { execSync } from "node:child_process";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT_DIR = path.resolve(__dirname, "..");
const HASH_FILE = path.join(ROOT_DIR, "src/canvas-host/a2ui/.bundle.hash");
const OUTPUT_FILE = path.join(ROOT_DIR, "src/canvas-host/a2ui/a2ui.bundle.js");
const A2UI_RENDERER_DIR = path.join(ROOT_DIR, "vendor/a2ui/renderers/lit");
const A2UI_APP_DIR = path.join(ROOT_DIR, "apps/shared/OpenClawKit/Tools/CanvasA2UI");

if (!fsSync.existsSync(A2UI_RENDERER_DIR) || !fsSync.existsSync(A2UI_APP_DIR)) {
  if (fsSync.existsSync(OUTPUT_FILE)) {
    console.log("A2UI sources missing; keeping prebuilt bundle.");
    process.exit(0);
  }
  console.error(`A2UI sources missing and no prebuilt bundle found at: ${OUTPUT_FILE}`);
  process.exit(1);
}

const inputPaths = [
  path.join(ROOT_DIR, "package.json"),
  path.join(ROOT_DIR, "pnpm-lock.yaml"),
  A2UI_RENDERER_DIR,
  A2UI_APP_DIR,
];

const files = [];

async function walk(entryPath) {
  const st = await fs.stat(entryPath);
  if (st.isDirectory()) {
    const entries = await fs.readdir(entryPath);
    for (const entry of entries) {
      await walk(path.join(entryPath, entry));
    }
    return;
  }
  files.push(entryPath);
}

async function computeHash() {
  for (const input of inputPaths) {
    if (fsSync.existsSync(input)) {
        await walk(input);
    }
  }

  function normalize(p) {
    return p.split(path.sep).join("/");
  }

  files.sort((a, b) => normalize(a).localeCompare(normalize(b)));

  const hash = createHash("sha256");
  for (const filePath of files) {
    const rel = normalize(path.relative(ROOT_DIR, filePath));
    hash.update(rel);
    hash.update("\0");
    hash.update(await fs.readFile(filePath));
    hash.update("\0");
  }

  return hash.digest("hex");
}

async function main() {
  const currentHash = await computeHash();
  if (fsSync.existsSync(HASH_FILE)) {
    const previousHash = await fs.readFile(HASH_FILE, "utf-8");
    if (previousHash.trim() === currentHash && fsSync.existsSync(OUTPUT_FILE)) {
      console.log("A2UI bundle up to date; skipping.");
      return;
    }
  }

  console.log("Building A2UI bundle...");
  
  execSync(`pnpm -s exec tsc -p "${path.join(A2UI_RENDERER_DIR, "tsconfig.json")}"`, { stdio: 'inherit', cwd: ROOT_DIR });
  
  try {
    execSync(`pnpm -s exec rolldown -c "${path.join(A2UI_APP_DIR, "rolldown.config.mjs")}"`, { stdio: 'inherit', cwd: ROOT_DIR });
  } catch(e) {
    execSync(`pnpm -s dlx rolldown -c "${path.join(A2UI_APP_DIR, "rolldown.config.mjs")}"`, { stdio: 'inherit', cwd: ROOT_DIR });
  }

  await fs.writeFile(HASH_FILE, currentHash);
  console.log("A2UI bundle build complete.");
}

main().catch(err => {
  console.error("A2UI bundling failed.");
  console.error(err);
  process.exit(1);
});
