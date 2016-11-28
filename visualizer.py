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
scn = bpy.context.scene
lines = None
delta_frame = 40
previous_object = ''
first_frame = 0
adr = 'localhost'
port = 9000
bpy.data.scenes["Scene"].frame_start = 0
bpy.data.scenes["Scene"].frame_end = 300000
scn.frame_set(0)
previous_frame = None

os.system('clear')

def close_sock(sock):
    sock.shutdown(0)
    sock.close()

def connect(host):
    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
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

class Line():
    material =  makeMaterial('Red', (1,0,0), (1,1,1), 1)

    #def get_by_name(self, name):
    def get(self, name):
        try:
            self.ob =  bpy.data.objects[name]
        except:
            print("Object" + name + "not found")
        finally:
            return self

    def link(self, node1, node2, name = None):
        global delta_frame
        
        scn = bpy.context.scene
        
        if name is None:
            name = node1 + "+" + node2
        node1 = bpy.data.objects[node1]
        node2 = bpy.data.objects[node2]
        if node1 is None or node2 is None:
            return
        bpy.ops.mesh.primitive_cylinder_add()
        ob = bpy.context.object
        ob.data.materials.append(self.material)
        ob.location = tuple([(node1.location[i] + node2.location[i]) / 2 for i in range(3)])
        print("line location: {0}".format(ob.location))
        dist = 0
        for i in range(3):
            dist += (node1.location[i] - node2.location[i])**2
        ob.scale = (0.1, 0.1, sqrt(dist)/2)
        vector = Vector((node2.location.x - node1.location.x, node2.location.y - node1.location.y, node2.location.z - node1.location.z))
    
        ob.rotation_mode = 'QUATERNION'
        ob.rotation_quaternion = vector.to_track_quat('Z','Y')

        ob.name = name
        ob.show_name = True

    def follow(self, node1, node2):
        global lines, delta_frame
        if self.ob is None:
            return
        scn = bpy.context.scene
        
        self.ob.select = True
        first_frame = scn.frame_current
        scn.frame_set(first_frame + delta_frame)
        node1_loc = bpy.data.objects[node1].location
        print("final node1 loc: {0}".format(node1_loc))
        node2_loc = bpy.data.objects[node2].location
        print("final node2 loc: {0}".format(node2_loc))

        new_loc = tuple([(node1_loc[i] + node2_loc[i])/2 for i in range(3)])
        
        dist = 0
        for i in range(3):
            dist += (node1_loc[i] - node2_loc[i])**2
        new_scale = (0.1, 0.1, sqrt(dist)/2)

        vector = Vector([(node2_loc[i] - node1_loc[i]) for i in range(3)])

        scn.frame_set(first_frame)
        self.ob.keyframe_insert(data_path = 'location', frame = scn.frame_current)
        self.ob.keyframe_insert(data_path = 'scale', frame = scn.frame_current)
        self.ob.keyframe_insert(data_path = 'rotation_quaternion', frame = scn.frame_current)

        delta_path = tuple([new_loc[i] - self.ob.location[i] for i in range(3)])
        
        print('Line' + self.ob.name)
        print('delta_path = {0}'.format(delta_path))
        print('new_scale = {0}'.format(new_scale))
        print('vector = {0}'.format(vector))
        bpy.ops.transform.translate(value = delta_path)
        self.ob.scale = new_scale
        self.ob.rotation_quaternion = vector.to_track_quat('Z','Y')
        self.ob.keyframe_insert(data_path = 'location', frame = scn.frame_current + delta_frame)
        self.ob.keyframe_insert(data_path = 'scale', frame = scn.frame_current + delta_frame)
        self.ob.keyframe_insert(data_path = 'rotation_quaternion', frame = scn.frame_current + delta_frame)

        scn.frame_set(first_frame)

    def remove(self):
        scene.objects.unlink(self.ob)
        bpy.data.objects.remove(self.ob)        
        
class Node():
    material = makeMaterial('Blue', (0,0,1), (0.5,0.5,0), 1)    
        
    def get(self, name):
        try:
            self.ob = bpy.data.objects[name]
        except:
            print("Node: Object " + name + " is not found")
        finally:
            return self
            
    def create(self, name, origin = (0, 0, 0)):
        try:
            bpy.data.objects[name]
        except:
            bpy.ops.mesh.primitive_uv_sphere_add(location = origin)
            ob = bpy.context.object
            ob.data.materials.append(self.material)
            ob.name = name
            ob.show_name = True
            bpy.ops.object.mode_set(mode = "OBJECT")
        else:
            return

    def moveTo(self, pos):
        print(self.ob)
        global delta_frame, first_frame
        scn = bpy.context.scene
        if not self.ob:
            return None
        for ob in bpy.data.objects:
            ob.select = False
        scn.frame_set(first_frame)
        self.ob.select = True
        self.ob.keyframe_insert(data_path = 'location', frame = scn.frame_current)
        delta_path = tuple([pos[i] - self.ob.location[i] for i in range(3)])
        print('delta_path = {0}'.format(delta_path))
        bpy.ops.transform.translate(value = delta_path)
        self.ob.keyframe_insert(data_path = 'location', frame = scn.frame_current + delta_frame)
        self.ob.select = False
        scn.frame_set(first_frame)

        
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

    bpy.types.Scene.eval = bpy.props.StringProperty(name = "Eval")
    
initSceneProperties(bpy.context.scene)

def scene_update(context):
    global previous_object
    scn = bpy.context.scene
    #if bpy.data.objects.is_updated:        
    for ob in bpy.data.objects:
        if ob.select:
            scn.xCoord = ob.location.x
            scn.yCoord = ob.location.y
            scn.zCoord = ob.location.z
            break
        scn.xCoord = 0
        scn.yCoord = 0
        scn.zCoord = 0
    

    if (previous_object != scn.current_object):
        for ob in bpy.data.objects:
            ob.select = False
        if (scn.current_object != ''):
            bpy.data.objects[scn.current_object].select = True
        previous_object = scn.current_object
     
bpy.app.handlers.scene_update_post.append(scene_update)

def frame_controller(context):
    global previous_frame
    scn = bpy.context.scene
        
    #print("Frame Change", scn.frame_current)
    if (scn.frame_current % (delta_frame) == 0) and (scn.frame_current != previous_frame):
        previous_frame = scn.frame_current
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
        
        layout.prop_search(scn, "current_object", scn, "objects")
        layout.label("Coordinates:")
        
        col = layout.column()
        ob = context.object
        
        col.prop(scn, "xCoord")
        col.prop(scn, "yCoord")
        col.prop(scn, "zCoord")
        col.prop(scn, "eval")
        layout.operator("update.button")
        
class UpdateButton(bpy.types.Operator):
    bl_idname = "update.button"
    bl_label = "Update"

    list = None
    
    def getList(self):
        global adr, port
        scn = bpy.context.scene

        sock = socket.socket()
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            sock.connect((adr, port))
        except:
            self.report({'ERROR'}, "Cannot connect to %s using port %d" % (adr, port))
            return 1

        #time.sleep(10)

        #sock.send(scn.eval.encode())
        if (scn.eval == ''):
            sock.send(str('None').encode())
        else:
            sock.send(scn.eval.encode())

        size = sock.recv(1024)

        size = int(size.decode())
        print("Pickled data size: %d" % size)
        #receive list
        pickled_list = sock.recv(size) #вот это работает
        #pickled_list = b'' #если передавать этим способом, то куда то деваются ровно 37 байт
        #print(size)
        #print(pickled_list)
        #while len(pickled_list) < size:
        #    data = sock.recv(size - len(pickled_list))
        #    if not data:
        #        self.report({'ERROR'}, "Socket closed %d bytes into a %d-byte message" % (len(pickled_list), size))
        #        return 1
        #    pickled_list += data
        #    print(pickled_list)
        #    print(len(pickled_list))
        self.list = pickle.loads(pickled_list)
        print("Unpickled data: {0}".format(self.list))
        sock.shutdown(0)
        sock.close()
        return 0

    def createObjects(self):
        for item in self.list.items():
            #node, location, linked_node, line_name = item
            node, location = item
            Node().create(node)
            #Line().link(node, linked_node, line_name)
        
    def updateObjects(self):
        global first_frame, delta_frame
        scn = bpy.context.scene
        
        #moving nodes and lines, if exist
        #names = self.list.keys()
        for item in self.list.items():
            #node, location, linked_node, line_name = item
            node, location = item
            Node().get(node).moveTo(location)
            #Line().get(line_name).follow(node1, node2)
        first_frame += delta_frame



    '''@classmethod
    def poll(cls, context):
        global sock

        if not sock:
            print("No connection to server")
        return sock'''
    
    def execute(self, context):        
        #Node().create("node1")
        #Node().get("node1").moveTo((5, 0, 0), delta_frame)
        if (self.getList()):
            return {'FINISHED'}
        self.createObjects()
        self.updateObjects()
        bpy.ops.screen.animation_play()
        
        return{'FINISHED'}  

def register() :  
    bpy.utils.register_module(__name__)            

def unregister() :  
    bpy.utils.unregister_module(__name__)     
    
def main():
    global sock

    #Node().create("node1")
    #Node().create("node2")
    #Line().link("node1", "node2")
    #Node().get("node1").moveTo((5,0,0))
    #Line().get("node1+node2").follow("node1", "node2")
    #scn.frame_set(scn.frame_current + delta_frame)
    #Node().get("node1").moveTo((0,5,0))
    #Line().get("node1+node2").follow("node1", "node2")
    #scn.frame_set(scn.frame_current + delta_frame)
    #Node().get("node1").moveTo((0,0,5))
    #Line().get("node1+node2").follow("node1", "node2")
    
    register()
    
main()

