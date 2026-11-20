# Image generation: full investigation and why it stopped on iOS

Read this before changing any image code. It records five failed approaches so
they are not repeated, and the owner decision that closed the investigation.

## Goal

Device-local, offline-first still-image generation in the static/phone app:
NanoDiffuser, WebGPU/float16, sizes 1:1 / 4:5 / 9:16 / 16:9 plus model choice,
copy/download controls, attach to chat. No bridge endpoint, cloud key or API
call. Owner/static only; hidden on guest and host.

## Model facts

- `utkucoban/NanoDiffuser`, pinned revision
  `14cff72356365c3586ee38a2237332525889b69c`, ~382 MB total.
- Manifest: 512×512, latent `[1,4,64,64]`, 77 prompt tokens, one step.
  `text_encoder_q4.onnx(.data)` ~63 MB, `unet_mixed_q4q8.onnx` 56 MB +
  `.data` ~257 MB, `vae_decoder_fp16.onnx` 29 KB + `.data` 2.3 MB.
- No smaller ready-to-run browser export was found. `recoilme/sdxs-micro`
  contains only Python and safetensors (no ONNX/WebGPU files);
  `kishanhk/sdxs-unet-u8` is a single 330 MB int8 U-Net, larger than the one
  already in use. Converting a model would be a large, uncertain project.

## Build-by-build

| Build | Change | Result |
|---|---|---|
| `2026-11-20d/e` | Introduced NanoDiffuser; reload fix | Worked in harness; iPhone flashed white and killed the tab |
| `2026-11-20f/g/h` | Chat-model release, blank-image fix, unfiltered model, reload defer | No change to the flash |
| `2026-11-20i/j` | Labelled stages + error log + diagnostics; streamed model files from cache one pair at a time | Diagnostics showed **no errors** — iOS was killing the tab before any `catch` could run |
| `2026-11-20k` | `imageCheckpoint()` before every stage and cache file read | Physical iPhone checkpoint: **`unet run`** |
| `2026-11-20l` | All-CPU engine (`wasm`) as a fallback, iPhone default | Physical iPhone screenshot: `text encoder load: Can't create a session. ERROR_CODE: 9, ERROR_MESSAGE: Could not find an implementation for GatherBlockQuantized(1) node ... Gather_Q4` |
| `2026-11-20m` | Hybrid: WebGPU encoder + CPU U-Net/decoder, iPhone default | Diagnostics: `Engine: hybrid`, last checkpoint **`unet run`**, no new error |
| `2026-11-21a` | **Graceful unsupported message on iOS** | Current build; awaits physical iPhone confirmation |

## Why the memory work could not fix it

The checkpoint proved the session loads and the fail is inside `unet.run()`.
Memory refactors (`j`) changed peak memory from ~695 MB to ~313 MB but did not
move the failure. A killed tab cannot run a `catch`, which is why the error log
stayed empty and a checkpoint was needed at all.

## Local verification of the two engines

Using the real pinned model in a local browser harness:

- WebGPU: the U-Net computes on desktop but kills the iPhone tab at `unet run`.
- CPU/WASM: the encoder cannot be created (`GatherBlockQuantized` unsupported),
  but the U-Net ran successfully in ~10 s and the FP16 decoder in ~5 s with the
  same float16 tensors, `numThreads=1`. So the app configuration was correct —
  the device, not the code, was the limit.

## Conclusion

The two engines fail at opposite ends on this iPhone:

| Engine | Encoder | U-Net | Decoder |
|---|---|---|---|
| WebGPU | works | **kills tab** | fine |
| CPU/WASM | **unsupported op** | works (on Mac) | works (on Mac) |
| Hybrid | works (WebGPU) | **kills tab** (WASM) | works |

The U-Net compute itself exceeds the device. No provider selection or memory
tweak avoids it, and no smaller drop-in model exists. The owner chose the
graceful message over further speculation.

## Current implementation

`imageUnsupported()` returns true for iPhone/iPad. `openImageModal()` then
renders "Images aren't available on iPhone" with a Close button only — no
prompt, size, engine or Generate controls. `startImageGeneration()` and
`loadImageRuntime()` both guard before any work, so no 382 MB download or U-Net
run is attempted. Desktop WebGPU generation is unchanged. The command palette
and model menu show the unsupported status on iOS.

Diagnostic identifiers if this area is revisited: `imageCheckpoint`,
`oracle.image.checkpoint`, `oracle.image.errors`, `copyImageDiagnostics`,
`imageStage`, `imageFile`, `imageSession`, `imageProvider`, `imageEngine`,
`setImageEngine`, `IMG_SMALL`, `IMG_MODEL_REV`, `IMG_CACHE`, `imageBusy`,
`updateBusy()`.
