import bpy, math, os, sys
from mathutils import Vector
from pathlib import Path

argv = sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else []
out_dir = Path(argv[0]); frames = int(argv[1]); out_dir.mkdir(parents=True, exist_ok=True)
bpy.ops.object.select_all(action="SELECT"); bpy.ops.object.delete(use_global=False)
scene=bpy.context.scene
# Use CPU Cycles for reliable headless rendering on GitHub-hosted Linux runners.
# Eevee depends on a working graphics context, which may be unavailable in CI.
scene.render.engine = "CYCLES"
scene.cycles.device = "CPU"
scene.cycles.samples = 8
scene.cycles.use_denoising = True
scene.render.resolution_x=540; scene.render.resolution_y=960; scene.render.resolution_percentage=100
scene.render.fps=12; scene.frame_end=frames
scene.render.image_settings.file_format="PNG"; scene.render.film_transparent=False
scene.world.color=(0.12,0.18,0.28)
scene.view_settings.view_transform="AgX"
def mat(name,color,rough=0.55,metal=0):
 m=bpy.data.materials.new(name); m.diffuse_color=(*color,1); m.use_nodes=True
 p=m.node_tree.nodes.get("Principled BSDF"); p.inputs["Base Color"].default_value=(*color,1); p.inputs["Roughness"].default_value=rough; p.inputs["Metallic"].default_value=metal
 return m
green=mat("Dino - bright jade",(0.12,0.62,0.31)); belly=mat("Warm mint belly",(0.65,0.85,0.46)); dark=mat("Deep green",(0.035,0.22,0.12)); cream=mat("Eye whites",(1,.97,.82)); black=mat("Pupils",(.012,.025,.035),.2); orange=mat("Golden spikes",(1,.48,.07)); pink=mat("Cheeks",(1,.28,.35)); ground=mat("Soft meadow",(0.12,.42,.23)); sky=mat("Backdrop",(0.2,.55,.78))
def uv(name,loc,scale,ma):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=24,ring_count=16,location=loc); o=bpy.context.object; o.name=name; o.scale=scale; o.data.materials.append(ma); bpy.ops.object.shade_smooth(); return o
def cone(name,loc,radius,depth,ma,rot=(0,0,0)):
 bpy.ops.mesh.primitive_cone_add(vertices=24,radius1=radius,radius2=0,depth=depth,location=loc,rotation=rot); o=bpy.context.object; o.name=name; o.data.materials.append(ma); return o
# soft studio stage and rolling backdrop
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,0)); bpy.context.object.name="Meadow floor"; bpy.context.object.data.materials.append(ground)
bpy.ops.mesh.primitive_uv_sphere_add(segments=32,ring_count=16,radius=1,location=(0,4,2)); back=bpy.context.object; back.name="Sky backdrop"; back.scale=(18,.3,12); back.data.materials.append(sky)
# rounded stylized 3D baby dinosaur
body=uv("Dino body",(0,0,1.45),(1.0,.67,1.12),green)
belly_obj=uv("Dino tummy",(0,-.57,1.25),(.62,.17,.78),belly)
neck=uv("Dino neck",(.48,-.02,2.15),(.48,.48,.78),green)
head=uv("Dino head",(.56,-.04,2.83),(.78,.63,.65),green)
snout=uv("Dino muzzle",(.88,-.46,2.65),(.48,.34,.29),belly)
for side in [-1,1]:
 uv("Eye white",(0.89+side*.22,-.57,3.02),(.18,.09,.22),cream)
 uv("Eye pupil",(0.93+side*.22,-.655,3.02),(.075,.045,.12),black)
 uv("Rosy cheek",(1.12+side*.1,-.66,2.67),(.12,.045,.08),pink)
# mouth curve in front
cu=bpy.data.curves.new("Happy smile","CURVE"); cu.dimensions="3D"; cu.bevel_depth=.025; cu.bevel_resolution=3
sp=cu.splines.new("POLY"); sp.points.add(12)
for i,p in enumerate(sp.points):
 x=.75+i*.035; z=2.54-.09*math.sin(i/12*math.pi); p.co=(x,-.77,z,1)
mouth=bpy.data.objects.new("Smile",cu); scene.collection.objects.link(mouth); cu.materials.append(dark)
# tail, little legs and arms, back spikes
tail=uv("Bouncy tail",(-1.0,.12,1.7),(.85,.28,.28),green)
tail.rotation_euler[1]=-.3
legs=[]
for x in [-.48,.48]:
 leg=uv("Little leg",(x,-.02,.48),(.28,.34,.52),green); foot=uv("Rounded foot",(x,-.22,.18),(.38,.48,.19),dark); legs.append(leg)
arms=[]
for x in [-.72,.75]:
 arm=uv("Waving arm",(x,-.02,1.75),(.23,.25,.62),green); arm.rotation_euler[1]=(-.65 if x<0 else .65); arms.append(arm)
for i in range(5):
 cone("Cute back spike",(-.75+i*.34,.05,2.2+(.12 if i%2 else 0)),.22,.5,orange,(0,math.pi/2,0))
# scene props: colorful blocks + plant + book stack around dino
red=mat("Coral block",(.95,.2,.18)); yellow=mat("Sunshine",(1,.68,.08)); blue=mat("Ocean blue",(.12,.42,.9)); pot=mat("Terracotta",(.62,.23,.12)); leaf=mat("Leaf",(.08,.5,.18)); paper=mat("Book pages",(.95,.85,.62))
def cube(name,loc,scale,ma,bevel=.12):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc); o=bpy.context.object; o.name=name; o.dimensions=scale; bpy.ops.object.transform_apply(location=False,rotation=False,scale=True); o.data.materials.append(ma)
 mod=o.modifiers.new("Soft rounded edges","BEVEL"); mod.width=bevel; mod.segments=3; o.modifiers.new("Weighted corner normals","WEIGHTED_NORMAL"); return o
props=[]
for i,(x,z,ma) in enumerate([(-2.0,.35,red),(-1.45,.35,yellow),(-1.72,.9,blue)]):
 props.append(cube("Toy building block",(x,-.25,z),( .48,.42,.48),ma))
cube("Flower pot",(2,-.1,.38),(.65,.6,.65),pot)
stem=cube("Plant stem",(2,-.1,1.05),(.09,.09,.85),leaf,.04)
uv("Plant leaf",(1.72,-.12,1.22),(.38,.15,.18),leaf).rotation_euler[1]=-.5
uv("Plant leaf",(2.27,-.12,1.35),(.38,.15,.18),leaf).rotation_euler[1]=.5
# camera and soft studio lighting
bpy.ops.object.camera_add(location=(5.7,-11,5.3)); cam=bpy.context.object; direction=Vector((0,0,1.75))-cam.location; cam.rotation_euler=direction.to_track_quat("-Z","Y").to_euler(); cam.data.type="ORTHO"; cam.data.ortho_scale=7.2; scene.camera=cam
def area(loc,power,size):
 bpy.ops.object.light_add(type="AREA",location=loc); l=bpy.context.object; l.data.energy=power; l.data.shape="DISK"; l.data.size=size; l.rotation_euler=(Vector((0,0,1.4))-l.location).to_track_quat("-Z","Y").to_euler()
area(( -4,-6,8),950,6); area((5,-3,6),650,5); area((0,4,7),850,4)
# subtle animated breathing, bouncing, tail swish and arm wave
for frame in range(1,frames+1):
 scene.frame_set(frame); t=frame/12
 body.location.z=1.45+.08*math.sin(t*5); head.location.z=2.83+.10*math.sin(t*5+.3); neck.location.z=2.15+.06*math.sin(t*5+.2)
 belly_obj.location.z=1.25+.08*math.sin(t*5)
 tail.rotation_euler[1]=-.3+.22*math.sin(t*3)
 arms[1].rotation_euler[1]=.65+.45*math.sin(t*5)
 arms[0].rotation_euler[1]=-.65+.12*math.sin(t*4)
 for o in [body,head,neck,belly_obj,tail,*arms]: o.keyframe_insert(data_path="location" if o in [body,head,neck,belly_obj] else "rotation_euler",frame=frame)
# interpolate smooth movement
if scene.animation_data and scene.animation_data.action:
 for fc in scene.animation_data.action.fcurves:
  for kp in fc.keyframe_points: kp.interpolation="BEZIER"
scene.render.filepath=str(out_dir/"frame_")
for frame in range(1,frames+1):
 scene.frame_set(frame); scene.render.filepath=str(out_dir/f"frame_{frame-1:05d}.png"); bpy.ops.render.render(write_still=True)
