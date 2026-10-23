"""Blender native Beauty adapter for the fixed CG Workbench dependency."""
import argparse
import os
from pathlib import Path
import shutil
import subprocess
import sys
from cgworkbench.core import Project, Protected, Stopped, WorkbenchError, read_json, run, write_json
from cgworkbench.media import encode

HERE=Path(__file__).resolve().parent

def main():
    p=argparse.ArgumentParser()
    p.add_argument('action',choices=['init','run','encode'])
    p.add_argument('--work',type=Path,required=True)
    p.add_argument('--blender',default='blender');p.add_argument('--scene',type=Path)
    p.add_argument('--ffmpeg',default='ffmpeg');p.add_argument('--ffprobe',default='ffprobe')
    p.add_argument('--reserve-gib',type=float,default=2)
    p.add_argument('--budget-gib',type=float,default=1)
    p.add_argument('--timeout-seconds',type=float,default=600)
    p.add_argument('--max-new-frames',type=int)
    a=p.parse_args();work=a.work.resolve();work.mkdir(parents=True,exist_ok=True)
    config=work/'render.local.json'
    if a.action=='init':
        if not a.scene or not a.scene.resolve().is_file():raise WorkbenchError('Pass a saved .blend via --scene')
        blender=shutil.which(a.blender)
        if not blender:raise WorkbenchError('Blender executable not found')
        if a.reserve_gib<=0 or a.budget_gib<0:raise WorkbenchError('Invalid capacity budget')
        if shutil.disk_usage(work).free < (a.reserve_gib+a.budget_gib)*1024**3:raise Protected('Insufficient startup capacity')
        temp=work/'temp';temp.mkdir(exist_ok=True)
        env=os.environ.copy();env.update({k:str(temp) for k in ('TEMP','TMP','TMPDIR')})
        with (work/'inspection.log').open('wb') as log:
            result=subprocess.run([blender,'--background','--factory-startup','--disable-autoexec','--python-exit-code','1',
                                   '--python',str(HERE/'inspect_scene.py'),'--','--scene',str(a.scene.resolve()),
                                   '--report',str(work/'inspection.json')],env=env,stdout=log,stderr=subprocess.STDOUT,
                                  timeout=180,check=False)
        if result.returncode:raise WorkbenchError('Inspection failed; read inspection.json and inspection.log')
        r=read_json(work/'inspection.json')
        if r['errors']:raise WorkbenchError(str(r['errors']))
        c={'schema_version':1,'name':a.scene.stem,'inputs':r['dependencies']+[str(HERE/'render_frame.py')],
           'command':[blender,'--background','--factory-startup','--disable-autoexec','--python-exit-code','1',
                      '--python',str(HERE/'render_frame.py'),'--','--scene',str(a.scene.resolve()),
                      '--frame','{frame}','--output','{output}','--temp','{temp}'],
           'output':str(work/'render'),'frames':r['frames'],'image':r['image'],'fps':r['fps'],
           'timeout_seconds':a.timeout_seconds,'poll_seconds':1,
           'storage':{'reserve_bytes':int(a.reserve_gib*1024**3),'job_budget_bytes':int(a.budget_gib*1024**3)}}
        write_json(config,c)
        print('Initialized:',config)
        print('Read inspection warnings and manual dependency review before a full render.')
    elif a.action=='run':print(run(Project(config),max_new_frames=a.max_new_frames))
    else:print(encode(Project(config),a.ffmpeg,a.ffprobe)['output'])

if __name__=='__main__':
    try:main()
    except (Exception,KeyboardInterrupt) as e:
        print(f'{type(e).__name__}: {e}',file=sys.stderr)
        raise SystemExit(2 if isinstance(e,Protected) else 3 if isinstance(e,(Stopped,KeyboardInterrupt)) else 1)
