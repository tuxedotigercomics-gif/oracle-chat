# Phone model research — November 2026

Question: can a real language model run reliably on any phone, and which one?

## Bottom line

Yes, but the **runtime matters more than the model**. The phone build now uses
**wllama** (llama.cpp compiled to WebAssembly) with two small GGUF models.
Transformers.js — which the previous build used — was the problem.

## Why Transformers.js kept killing the iPhone tab

- [transformers.js issue #1242](https://github.com/huggingface/transformers.js/issues/1242):
  v3 caused runaway memory on iOS/iPadOS. Multiple users confirmed crashes in
  Safari and Chrome. A WebKit fix landed in iOS 18.4, but reports continued on
  iOS 26, where downgrading to `@xenova/transformers@2.15.1` was the workaround.
- [Nearform's Oct 2026 runtime comparison](https://nearform.com/digital-community/web-ai-runtimes-five-ways-to-run-a-language-model-in-the-browser/)
  tested five browser runtimes on an iPhone 15 Pro in both Safari and Chrome
  for iOS:

  | Runtime | Result on iPhone |
  | --- | --- |
  | WebLLM | Runs |
  | **wllama** | **Runs** |
  | Transformers.js | Answers, then iOS kills the tab |
  | LiteRT-LM.js | Tab dies during load |
  | Chrome Prompt API | Unavailable |

- iOS caps memory per browser tab and every iOS browser uses WebKit, so
  Safari and Chrome hit the same limit. There is no catchable error — the tab
  just dies. That is exactly the "preparing device → back to home / blank"
  behaviour reported.

## Models that fit

GGUF files are downloaded from Hugging Face once, then cached on the device
by wllama. Sizes checked against the HF API:

| Model | Runtime | Download | Use |
| --- | --- | --- | --- |
| `SmolLM2-135M-Instruct-Q4_K_M` | wllama | ~105 MB | default, fits low-end phones |
| `LFM2.5-350M-Q4_K_M` | wllama | ~229 MB | better answers, still under the ~400 MB iPhone ceiling |
| `Qwen2.5-0.5B-Instruct-Q4_K_M` | wllama | ~491 MB | too large for older iPhones |
| `SmolLM2-360M q4f16` | WebLLM | ~376 MB VRAM | alternative, but requires WebGPU |

Old build: SmolLM2-135M ONNX q4 = 182 MB / q4f16 = 118 MB, on the runtime
that kills iOS tabs.

## Honest quality caveat

Small models are small. Nearform found SmolLM2-135M often produced nonsense
and LFM2.5-350M gave plausible-but-wrong answers on a knowledge question.
The 135M default is chosen for **reliability and universal fit**, not depth.
For demanding questions, use a larger model on a laptop/desktop (the Mac
bridge build) where memory is not constrained.

## Why the models are not bundled into the site

Cloudflare Pages limits a single static asset to **25 MiB**. Even the 105 MB
model cannot be uploaded as a site file. Hugging Face serves the GGUF files,
and the service worker / wllama cache them on the phone after first download.
There is no host-Mac dependency.

## Service worker note

`sw.js` passes HTTP `Range` requests through without caching: a cached partial
`206` response would corrupt a later wllama load. Cache version bumped to `v3`
so stale ONNX files are discarded.
