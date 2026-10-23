"""Read a saved scene without changing or saving it. Executed by Blender."""
import argparse
import json
import math
from pathlib import Path
import sys
import bpy

p=argparse.ArgumentParser()
p.add_argument('--scene',required=True);p.add_argument('--report',required=True)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
bpy.ops.wm.open_mainfile(filepath=a.scene,use_scripts=False)
s=bpy.context.scene
errors=[];warnings=[];dependencies={str(Path(a.scene).resolve())}
if not s.camera:errors.append('Scene has no active camera')
if s.frame_start<1 or s.frame_end<s.frame_start:errors.append('Positive inclusive frame range required')
if s.render.fps_base!=1:errors.append('This adapter currently requires integer fps (fps_base=1)')
meshes=[]
for o in s.objects:
    if o.type!='MESH':continue
    if not all(math.isfinite(v) for vertex in o.data.vertices for v in vertex.co):errors.append('Non-finite coordinates: '+o.name)
    row={'name':o.name,'vertices':len(o.data.vertices),'faces':len(o.data.polygons),
         'uv_layers':[u.name for u in o.data.uv_layers],
         'shape_keys':list(o.data.shape_keys.key_blocks.keys()) if o.data.shape_keys else [],
         'materials':[slot.material.name if slot.material else None for slot in o.material_slots]}
    meshes.append(row)
    if not o.data.uv_layers:warnings.append('No UV layer: '+o.name+' (may be intentional for procedural materials)')
    if any(slot.material is None for slot in o.material_slots):warnings.append('Empty material slot: '+o.name)

def dependency(path,owner):
    resolved=Path(path).resolve()
    if not resolved.is_file():errors.append('Missing dependency: '+owner+' -> '+str(resolved))
    else:dependencies.add(str(resolved))

images=[]
for im in bpy.data.images:
    images.append({'name':im.name,'source':im.source,'packed':bool(im.packed_file),'size':list(im.size),
                   'colorspace':im.colorspace_settings.name})
    if im.packed_file or im.source in ('GENERATED','VIEWER'):continue
    if im.source!='FILE':errors.append('Pack/bake or explicitly adapt non-file image source: '+im.name);continue
    if not im.filepath:errors.append('Unpacked image has no path: '+im.name);continue
    dependency(bpy.path.abspath(im.filepath,library=im.library),im.name)
for lib in bpy.data.libraries:dependency(bpy.path.abspath(lib.filepath),'linked library')
materials=[]
for m in bpy.data.materials:
    outputs=[]
    if m.use_nodes:
        for n in m.node_tree.nodes:
            if n.type=='OUTPUT_MATERIAL' and n.is_active_output:
                outputs.extend({'from_node':link.from_node.name,'from_socket':link.from_socket.name}
                               for link in n.inputs['Surface'].links)
    materials.append({'name':m.name,'active_surface_links':outputs})
    if m.use_nodes and not outputs:warnings.append('No active Surface link: '+m.name)
report={'scene':str(Path(a.scene).resolve()),'blender':bpy.app.version_string,'engine':s.render.engine,
        'frames':[s.frame_start,s.frame_end],'fps':s.render.fps,
        'image':[int(s.render.resolution_x*s.render.resolution_percentage/100),int(s.render.resolution_y*s.render.resolution_percentage/100)],
        'camera':s.camera.name if s.camera else None,'meshes':meshes,'images':images,'materials':materials,
        'dependencies':sorted(dependencies),'errors':errors,'warnings':warnings,
        'manual_dependency_review':['Physics and simulation caches','Fonts and media strips','Geometry Nodes external data',
                                    'Driver expressions, add-ons and handlers','Linked libraries may have their own unpacked dependencies'],
        'visual_review':'not_reviewed'}
out=Path(a.report);out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
if errors:raise RuntimeError('Scene inspection failed; see report: '+str(out))
