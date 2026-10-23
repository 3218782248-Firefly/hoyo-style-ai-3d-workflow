"""Render the saved scene with its actual camera, renderer and display settings."""
import argparse
import sys
import bpy
p=argparse.ArgumentParser()
p.add_argument('--scene',required=True);p.add_argument('--frame',type=int,required=True)
p.add_argument('--output',required=True);p.add_argument('--temp',required=True)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
bpy.ops.wm.open_mainfile(filepath=a.scene,use_scripts=False)
bpy.context.preferences.filepaths.temporary_directory=a.temp
s=bpy.context.scene
# Export Beauty directly; compositor/file-output pipelines need their own adapter.
s.render.use_compositing=False
s.render.image_settings.file_format='PNG';s.render.filepath=a.output
s.frame_set(a.frame)
bpy.ops.render.render(write_still=True)
