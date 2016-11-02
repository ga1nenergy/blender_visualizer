import bpy
import os
import time
import socket
import pickle
import sys
from mathutils import Euler, Vector
from math import sqrt, atan, acos, pi, asin, atan2
from bpy import context
from bpy.props import *
from math import sin, cos, radians
from mathutils import Vector

cursor = context.scene.cursor_location
scene = bpy.context.scene
delta_frame = 40
previous_object = None
sock = None
port = 7777

os.system('clear')

def close_sock(sock):
    sock.shutdown(0)
    sock.close()

def connect(host):
    sock = socket.socket()
    try:
        sock.connect((host, port))
    except:
        print("Error: {0}".format(sys.exc_info()[0]))
        close_sock(sock)
    return sock

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
        scn = bpy.context.scene
        scn.frame_set(1)
        self.ob.select = True
        self.ob.keyframe_insert(data_path = 'location', frame = scene.frame_current)
        delta_path = tuple([pos[i] - self.ob.location[i] for i in range(3)])
        print('delta_path = {0}'.format(delta_path))
        bpy.ops.transform.translate(value = delta_path)
        self.ob.keyframe_insert(data_path = 'location', frame = scene.frame_current + delta_frame)
        self.ob.select = False
        scn.frame_set(1)
        
    def remove(self):
        context.scene.objects.unlink(self.ob)
        bpy.data.objects.remove(self.ob)
        
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
    
    '''if ((previous_object != scn.current_object)):
        for ob in bpy.data.objects:
            ob.select = False
        bpy.data.objects[scn.current_object].select = True
        previous_object = scn.current_object'''
     
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

    list = None
    
    def getList(self):
        global sock

        print(sock)

        if sock is None:
            print("came here")
            sock = connect('localhost')
        #sock = connect('localhost')

        print(sock)

        command = "send_list"
        print("Sent command: " + command)
        command = command.encode()
        sock.send(command)
        #receive pickled data size
        size = sock.recv(2)
        size = size.decode()
        print("Pickled data size: " + size)
        #receive list
        pickled_list = sock.recv(int(size))
        self.list = pickle.loads(pickled_list)
        print("Unpickled data: {0}".format(self.list))

        names = self.list.keys()
        for name in names:
            Node().create(name)
        
    def updateObjects(self):
        scn = bpy.context.scene
        
        names = self.list.keys()
        for name in names:
            Node().get(name).moveTo(self.list[name], delta_frame)

    '''@classmethod
    def poll(cls, context):
        global sock

        if not sock:
            print("No connection to server")
        return sock'''
    
    def execute(self, context):        
        #Node().create("node1")
        #Node().get("node1").moveTo((5, 0, 0), delta_frame)
        self.getList()
        self.updateObjects()
        bpy.ops.screen.animation_play()
        
        return{'FINISHED'}  

def register() :  
    bpy.utils.register_module(__name__)            

def unregister() :  
    bpy.utils.unregister_module(__name__)     
    
def main():
    global sock
    
    register()
    
main()

