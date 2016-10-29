import bpy
import os
import time
from mathutils import Euler, Vector
from math import sqrt, atan, acos, pi, asin, atan2
from bpy import context
from bpy.props import *
from math import sin, cos, radians
from mathutils import Vector

cursor = context.scene.cursor_location
scene = bpy.context.scene
objects = {}
array = []
keys = []
isModified = True
delta_frame = 40
scene.frame_set(1)
previous_object = None

os.system('clear')

def makeMaterial(name, diffuse, specular, alpha):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = diffuse
    mat.diffuse_shader = 'LAMBERT' 
    mat.diffuse_intensity = 1.0 
    mat.specular_color = specular
    mat.specular_shader = 'COOKTORR'
    mat.specular_intensity = 0.5
    mat.alpha = alpha
    mat.ambient = 1
    return mat
        
class Node():
    material = makeMaterial('Blue', (0,0,1), (0.5,0.5,0), 1)    
        
    def get(self, name):
        try:
            self.ob = bpy.data.objects[name]
            
        except:
            print("Node: Object " + name + " is not found")
        finally:
            return self
            
    def create(self, name, override = None, origin = cursor):
        if override is not None:
            bpy.ops.mesh.primitive_uv_sphere_add(override, location = origin)
        else:
            bpy.ops.mesh.primitive_uv_sphere_add(location = origin)
        ob = bpy.context.object
        ob.data.materials.append(self.material)
        ob.name = name
        ob.show_name = True
        bpy.ops.object.mode_set(mode = "OBJECT")
        
    def moveTo(self, pos, delta_frame):
        print(self.ob)
        self.ob.select = True
        self.ob.keyframe_insert(data_path = 'location', frame = scene.frame_current)
        delta_path = tuple([pos[i] - self.ob.location[i] for i in range(3)])
        print('delta_path = {0}'.format(delta_path))
        bpy.ops.transform.translate(value = delta_path)
        self.ob.keyframe_insert(data_path = 'location', frame = scene.frame_current + delta_frame)
        self.ob.select = False
        bpy.context.scene.frame_set(1)
        
    def remove(self):
        context.scene.objects.unlink(self.ob)
        bpy.data.objects.remove(self.ob)
        
def gen_list():
        if (len(bpy.data.objects) is not 0):
            return [(ob.name, ob.name, ob.type) for ob in bpy.data.objects]
        else:
            return [("None", "None", "It seems data hasn't been received yet")]
        
def initSceneProperties(scn):
 
    bpy.types.Scene.xCoord = FloatProperty(
        name = "X", 
        description = "X coordinate of the object")
    scn["xCoord"] = 0.0
    
    bpy.types.Scene.yCoord = FloatProperty(
        name = "Y", 
        description = "Y coordinate of the object")
    scn["yCoord"] = 0.0
        
    bpy.types.Scene.zCoord = FloatProperty(
        name = "Z", 
        description = "Z coordinate of the object")
    scn["zCoord"] = 0.0
    
    bpy.types.Scene.current_object = bpy.props.StringProperty(name = "Object")
    
initSceneProperties(bpy.context.scene)

def scene_update(context):
    global previous_object
    scn = bpy.context.scene
    if bpy.data.objects.is_updated:
        print("One or more objects were updated!")
        
        ob = bpy.context.object
        scn.xCoord = ob.location.x
        scn.yCoord = ob.location.y
        scn.zCoord = ob.location.z
    
    if ((previous_object != scn.current_object) and (bpy.data.objects[scn.current_object] != None)):
        for ob in bpy.data.objects:
            ob.select = False
        bpy.data.objects[scn.current_object].select = True
        previous_object = scn.current_object
     
bpy.app.handlers.scene_update_post.append(scene_update)

def frame_controller(context):
    scn = bpy.context.scene
        
    print("Frame Change", scn.frame_current)
    if (scn.frame_current is (delta_frame + 1)):
        bpy.ops.screen.animation_cancel(restore_frame = False)
        
bpy.app.handlers.frame_change_pre.append(frame_controller)

class OBJECT_PT_MenuPanel(bpy.types.Panel):
    bl_label = "Menu panel"
    bl_idname = "OBJECT_PT_MenuPanel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"

    def draw(self, context):
        layout = self.layout
        scn = context.scene
        
        layout.prop_search(scene, "current_object", scene, "objects")
        layout.label("Coordinates:")
        
        col = layout.column()
        ob = context.object
        
        col.prop(scn, "xCoord")
        col.prop(scn, "yCoord")
        col.prop(scn, "zCoord")
        layout.operator("update.button")
        
class UpdateButton(bpy.types.Operator):
    bl_idname = "update.button"
    bl_label = "Update"
    
    def getList(self, list):
        self.names = list.keys()
        for name in names:
            Node().create(name)
        
    def updateObjects(self):
        scn = bpy.context.scene
        
        for name in names:
            Node().get(name).moveTo(list[name], delta_frame)
    
    def execute(self, context):        
        Node().create("node1")
        Node().get("node1").moveTo((5, 0, 0), delta_frame)
        bpy.ops.screen.animation_play()
        
        return{'FINISHED'}  

def add_to_menu(self, context) :  
    self.layout.operator("dropdown.list", icon = "PLUGIN")  

def register() :  
    bpy.utils.register_module(__name__)            

def unregister() :  
    bpy.utils.unregister_module(__name__)     
    
def main():
    global objects
    
    register()
    
main()
