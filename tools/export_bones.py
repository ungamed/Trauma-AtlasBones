# Exports Z-Anatomy bone meshes (bones and cartilage only, no teeth) for ADR-146.
# Output: little-endian binary. Coordinates converted to the canonical body frame
# (right, up, forward) in metres: Blender X is the body's left, Z up, -Y the front.
import bpy, struct, sys

out = sys.argv[sys.argv.index('--') + 1]

SIDED = [
    'Parietal bone', 'Temporal bone', 'Zygomatic bone', 'Maxilla', 'Nasal bone', 'Palatine bone', 'Lacrimal bone',
    'Inferior nasal concha bone', 'Hip bone', 'Scapula', 'Femur', 'Clavicle',
    'First rib', 'Second rib', 'Third rib', 'Fourth rib', 'Fifth rib', 'Sixth rib', 'Seventh rib', 'Eighth rib',
    'Ninth rib', 'Tenth rib', 'Eleventh rib', 'Twelfth rib',
]
CARTILAGE = ['first', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh', 'eighth', 'ninth', 'tenth']
SINGLE = [
    'Frontal bone', 'Occipital bone', 'Sphenoid bone', 'Ethmoid bone', 'Vomer', 'Mandible',
    'Atlas (C1)', 'Axis (C2)', 'Sacrum', 'Coccyx',
    'Manubrium of sternum', 'Body of sternum', 'Xiphoid process',
] + [f'Vertebra C{i}' for i in range(3, 8)] + [f'Vertebra T{i}' for i in range(1, 13)] + [f'Vertebra L{i}' for i in range(1, 6)]

names = list(SINGLE)
for n in SIDED:
    names += [n + '.l', n + '.r']
# Landmark-only meshes (not baked): humeral heads, teeth, eyeballs.
for n in ['Humerus', 'Anterior segment of eyeball', 'Posterior segment of eyeball'] + [
        f'{jaw} {t}' for jaw in ('Upper', 'Lower') for t in ('medial incisor', 'lateral incisor', 'canine', 'first premolar',
                                                           'second premolar', 'first molar tooth', 'second molar tooth')]:
    names += [n + '.l', n + '.r']
for c in CARTILAGE:
    names += [f'Costal cartilage of {c} rib.l', f'Costal cartilage of {c} rib.r']

depsgraph = bpy.context.evaluated_depsgraph_get()
missing = []
with open(out, 'wb') as f:
    f.write(b'ZAB1')
    present = [n for n in names if n in bpy.data.objects]
    missing = [n for n in names if n not in bpy.data.objects]
    f.write(struct.pack('<i', len(present)))
    for name in present:
        obj = bpy.data.objects[name]
        ev = obj.evaluated_get(depsgraph)
        mesh = ev.to_mesh()
        mesh.calc_loop_triangles()
        m = obj.matrix_world
        flip = m.determinant() < 0
        verts = []
        for v in mesh.vertices:
            w = m @ v.co
            verts.append((-w.x, w.z, -w.y))
        tris = []
        for t in mesh.loop_triangles:
            a, b, c = t.vertices
            # The axis swap (x -> -x, y -> z, z -> -y) has determinant -1: flip once for it, once more for a mirrored object.
            tris.append((a, b, c) if flip else (a, c, b))
        encoded = name.encode('utf-8')
        f.write(struct.pack('<i', len(encoded)))
        f.write(encoded)
        f.write(struct.pack('<i', len(verts)))
        for v in verts:
            f.write(struct.pack('<3f', *v))
        f.write(struct.pack('<i', len(tris)))
        for t in tris:
            f.write(struct.pack('<3i', *t))
        ev.to_mesh_clear()
print('EXPORTED', len(present), 'MISSING', missing)
