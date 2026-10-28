# Trauma Atlas Bones

These are the bone meshes that the [T.R.A.U.M.A](https://github.com/ungamed) wound package bakes into a character's anatomy (its ADR-146, *bones from an anatomy atlas*). They are exported from the [Z-Anatomy](https://github.com/Z-Anatomy/Models-of-human-anatomy) atlas, which derives from [BodyParts3D](https://dbarchive.biosciencedbc.jp/en/bodyparts3d/download.html).

**Licence:** the data is **CC BY-SA 4.0** ([LICENSE](LICENSE)); see [ATTRIBUTION.md](ATTRIBUTION.md) for the credits you must keep. The export script in `tools/` is MIT ([tools/LICENSE](tools/LICENSE)).

## What's here

`atlas_bones.bytes` holds 137 meshes from the atlas's adult male (about 10 MB):

| Group | Meshes | Used for |
|---|---|---|
| Skull | Frontal, parietal, occipital, temporal, sphenoid, ethmoid, vomer, zygomatic, maxilla, nasal, palatine, lacrimal and inferior nasal concha bones, and the mandible | Baked |
| Spine | C1 (atlas), C2 (axis), C3–C7, T1–T12, L1–L5, sacrum, coccyx | Baked |
| Thorax | Ribs 1–12, costal cartilages 1–10, manubrium, body of the sternum, xiphoid process | Baked |
| Shoulder | Scapulae, clavicles | Scapulae baked |
| Pelvis and thigh | Hip bones, femurs | Baked |
| Landmarks | Humeri, all 28 teeth, eyeballs (anterior and posterior segments) | Fitting only |

- **Teeth are landmarks only.** A character brings its own teeth meshes. The atlas teeth tell the fit where the dental arches sit, so the jaw bones land around the character's teeth.
- **Bones and cartilage only.** No soft tissue is included, and nothing from the atlas parts under non-commercial licences (its inner ear and kidney models).

## The file format

The file is little-endian and in metres, in the body frame: x is the body's right, y up, z forward.

```
"ZAB1"                      4 bytes
meshCount                   int32
per mesh:
  nameLength, name          int32, UTF-8 (the Z-Anatomy object name, e.g. "Fifth rib.l"; .l = the body's left)
  vertexCount, vertices     int32, float32 x, y, z each
  triangleCount, triangles  int32, int32 a, b, c each (wound outward)
```

All the meshes are closed, with outward normals.

## Rebuilding it

1. Download `Z-Anatomy.zip` from the Z-Anatomy repository, and extract `Z-Anatomy/Startup.blend`.
2. Run Blender headless, with the file's own scripts disabled:

   ```
   blender -b --disable-autoexec Startup.blend --python tools/export_bones.py -- atlas_bones.bytes
   ```

**This build:**
- Z-Anatomy at commit `6ffffec1d9b17ed3db355903bbd762582cb2328e` (2026-10-27).
- `Z-Anatomy.zip` sha256 begins `e029688545627bd0`.
- Exported with Blender 5.1.1 on 2026-10-28.
- `atlas_bones.bytes` sha256 begins `4bd5243e150df89f`.

## Using it with T.R.A.U.M.A

1. Point the anatomy template's `SkeletonSpec.AtlasLibraryPath` at `atlas_bones.bytes`.
2. Rebake the characters.

The bake warps each bone onto the character's own fitted skeleton and bakes it into the anatomy volume.

**Share-alike reaches the bakes:** a bake made with these bones derives from them, so it falls under CC BY-SA 4.0 too.
