import bpy
import os
import time
from mathutils import Euler, Vector
from math import sqrt, atan, acos, pi, asin, atan2
from bpy import context
from bpy.props import *
from math import sin, cos, radians
from mathutils import Vector

#nodearr = []

#cubeobject = bpy.ops.mesh.primitive_uv_sphere_add

cursor = context.scene.cursor_location
scene = bpy.context.scene
objects = {}
array = []
keys = []
isModified = True
delta_frame = 40
scene.frame_set(1)

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

"""class Line():
    _attributes = {} 
    _nodes = []
    _obj = None
    _material =  makeMaterial('Red', (1,0,0), (1,1,1), 1)
    
    def __init__(self, name, Node1, Node2):
        node1 = Node1._obj
        node2 = Node2._obj
        
        bpy.ops.mesh.primitive_cylinder_add()
        ob = bpy.context.object
        ob.data.materials.append(self._material)
        ob.location = list((node1.location[i] + node2.location[i]) / 2 for i in range(3))
        dist = 0
        for i in range(3):
            dist += (node1.location[i] - node2.location[i])**2
        ob.scale = (0.1, 0.1, sqrt(dist)/2)
        vector = Vector((node2.location.x - node1.location.x, node2.location.y - node1.location.y, node2.location.z - node1.location.z))
    
        ob.rotation_mode = 'QUATERNION'
        ob.rotation_quaternion = vector.to_track_quat('Z','Y')

        ob.name = name
        ob.show_name = True
        
        self._obj = ob
        self._nodes = [Node1, Node2]
    
    def remove(self):
        scene.objects.unlink(self._obj)
        bpy.data.objects.remove(self._obj)
        self._attributes = None
        self._nodes = None
        self._obj = None
        self._material = None"""
        
        
    #def link(node1, node2):
     #   Line('line ' + node1._obj.name + ' / ' + node2._obj.name, node1, node2)
        
'''class Node():
    #_attributes = {}
    _obj = None
    #_line = None
    _material = makeMaterial('Blue', (0,0,1), (0.5,0.5,0), 1)
    
    def __init__(self, name, origin):
        bpy.ops.mesh.primitive_uv_sphere_add(location = origin)
        ob = bpy.context.object
        ob.data.materials.append(self._material)
        ob.name = name
        ob.show_name = True
        
        self._obj = ob
    
    def moveTo(self, dest):
        self._obj.location = dest
        
    def remove(self):
        scene.objects.unlink(self._obj)
        bpy.data.objects.remove(self._obj)
        _attributes = None
        _obj = None
        _line = None
        _material = None
            
    def linkTo(self, node):
        if self._line is None:
            _line = Line('line ' + self._obj.name + ' / ' + node._obj.name, self, node)
        else:
            print('Link already exists')
            
    def unlink(self):
        self._link.remove()
        self._link = None'''
        
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
        #print(dir(context))
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
 
initSceneProperties(bpy.context.scene)

def scene_update(context):
    scn = bpy.context.scene
    if bpy.data.objects.is_updated:
        print("One or more objects were updated!")
        
        ob = bpy.context.object
        scn.xCoord = ob.location.x
        scn.yCoord = ob.location.y
        scn.zCoord = ob.location.z
bpy.app.handlers.scene_update_post.append(scene_update)

def frame_controller(context):
    scn = bpy.context.scene
        
    print("Frame Change", scn.frame_current)
    if (scn.frame_current is (delta_frame + 1)):
        bpy.ops.screen.animation_cancel(restore_frame = False)
        
bpy.app.handlers.frame_change_pre.append(frame_controller)

class MenuPanel(bpy.types.Panel):
    bl_label = "Menu panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    
    '''@classmethod
    def poll(cls, context):
        return not bpy.data.objects is None'''
 
    def draw(self, context):
        layout = self.layout
        scn = context.scene
        #layout.prop(scn, "DropDownList")
        layout.label("Coordinates:")
        
        col = layout.column()
        ob = context.object
        
        #col.prop(ob, "location")
        col.prop(scn, "xCoord")
        col.prop(scn, "yCoord")
        col.prop(scn, "zCoord")
        layout.operator("update.button")
        
'''class Menu(bpy.types.Operator) :      
    bl_idname = "visualizer.menu"  
    bl_label = "Menu Panel"  
    bl_options = {"REGISTER", "UNDO"}                                           
    
    print(bpy.data.objects)
    def gen_list():
        if (bpy.context.object == None):
            return [("NULL", "NULL", "It seems data hasn't been received yet")]
        else:
            return [(ob.name, ob.name, ob.type) for ob in bpy.data.objects]
                                         
    DropDownList = bpy.props.EnumProperty(items=gen_list(), name = "Object", description = "Choose object here")                  
                                                                           
    xCoord = FloatProperty(
        name = "X", 
        description = "X coordinate of the object")
    yCoord = FloatProperty(
        name = "Y", 
        description = "Y coordinate of the object")
    zCoord = FloatProperty(
        name = "Z", 
        description = "Z coordinate of the object")
    
    def execute(self, context):
        for ob in bpy.data.objects:
            print(ob)
        print(self.DropDownList)
        #bpy.ops.object.select_all(action='DESELECT')
        if (self.DropDownList != "NULL"):
            obj = bpy.data.objects[self.DropDownList]
            obj.select = True
        
            self.xCoord = obj.location.x
            self.yCoord = obj.location.y
            self.zCoord = obj.location.z        
        #Node().create("node1")

        return {"FINISHED"}
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "DropDownList")
        
        col = layout.column()
        col.label(text="Attributes:")
       
        col.prop(self, "xCoord")
        col.prop(self, "yCoord")
        col.prop(self, "zCoord")
        layout.operator("update.button")'''
        
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
            
        scn = bpy.context.scene
        #current_frame = scn.frame_current
        '''for i in range(delta_frame):
            scn.frame_set(i)'''
    
    def execute(self, context):
        scn = bpy.context.scene
        """win      = bpy.context.window
        scr      = win.screen
        areas3d  = [area for area in scr.areas if area.type == 'VIEW_3D']
        region   = [region for region in areas3d[0].regions if region.type == 'WINDOW']
        
        override = {'window':win,
                    'screen':scr,
                    'area'  :areas3d[0],
                    'region':region[0],
                    'scene' :bpy.context.scene,
                    'edit_object':bpy.context.edit_object,
                    'active_object':bpy.context.active_object,
                    'blend_data':bpy.context.blend_data
                    #'object':bpy.context.object
                    }"""
        
        Node().create("node1")
        Node().get("node1").moveTo((5, 0, 0), delta_frame)
        bpy.ops.screen.animation_play()
        
        return{'FINISHED'}  
    
'''class UpdateMenuInfo(bpy.types.Operator):
    bl_idname = "update.menuinfo"
    bl_label = "Update Menu Info"
    
    def __init__(self):
        print("update operator init")
        scn = context.scene
        self.previous_dropdown = scn["DropDownList"]
    
    def modal(self, context, event):
        scn = context.scene
        current_dropdown = scn["DropDownList"]
        
        print("running modal")
        
        if (current_dropdown != self.previous_dropdown):
            print("previous object: {0}".format(self.previous_dropdown))
            print("current object: {0}".format(current_dropdown))
            bpy.ops.object.select_all(action="DESELECT")
            ob = bpy.data.objects[current_dropdown]
            ob.select = True
            
        if (current_dropdown != "NULL"):
            ob = bpy.data.objects[current_dropdown]
            scn["xCoord"] = ob.location.x
            scn["yCoord"] = ob.location.y
            scn["zCoord"] = ob.location.z
            print("coord props updated")
            
        return {"RUNNING_MODAL"}
    
    def invoke(self, context, event):
        print("INVOKE")
        
        context.window_manager.modal_handler_add(self) # add modal handler!!!
        return {'RUNNING_MODAL'}'''

'''def add_to_menu(self, context) :  
    self.layout.operator("visualizer.menu", icon = "PLUGIN")  '''

def register() :  
    bpy.utils.register_module(__name__)       
    #bpy.types.VIEW3D_PT_tools_object.append(add_to_menu)
    #self.layout.operator("mesh.dropdownexample", icon = "PLUGIN")      

def unregister() :  
    bpy.utils.unregister_module(__name__)   
    #bpy.types.VIEW3D_PT_tools_object.remove(add_to_menu)   
    
    #bpy.ops.mesh.primitive_cylinder_add()
    #ob = bpy.context.object
    #ob.data.materials.append(line_mat)
    #location = tuple(list((node1.location[i] + node2.location[i]) / 2 for i in range(3)))
    #ob.location = location
    #dist = 0
    #for i in range(3):
    #    dist += (node1.location[i] - node2.location[i])**2
    #ob.scale = (0.1, 0.1, sqrt(dist)/2)
    #vector = Vector((node2.location.x - node1.location.x, node2.location.y - node1.location.y, node2.location.z - node1.location.z))
    
    #ob.rotation_mode = 'QUATERNION'
    #ob.rotation_quaternion = vector.to_track_quat('Z','Y')"""

    #ob.name = 'line ' + node1.name + '-' + node2.name
    #ob.show_name = True  
    
def main():
    global objects
    #unregister()
    register()
    #Node().create("node")
    '''line_mat = makeMaterial('Red', (1,0,0), (1,1,1), 1)
    node_mat = makeMaterial('Blue', (0,0,1), (0.5,0.5,0), 1)'''
    '''data = ('node1', 0, ((0.0, 0.0, 0.0), 0))
    Interface().receive(data)
    i = 0.0
    while i < 10.0:
        data = ('node1', 1, ((i, 0.0, 0.0), 0))
        Interface().receive(data)
        time.sleep(0.1)
        i += 1'''
    #Node.get(
    #node1 = Node("node1", cursor)
    #createNode("node1", cursor)
    #node2 = Node("node2", (cursor.x - 5, cursor.y + 4, cursor.z + 3))
    #createNode("node2", (cursor.x - 5, cursor.y + 4, cursor.z + 3))
    #node1.linkTo(node2)
    #drawLine(bpy.data.objects["node1"], bpy.data.objects["node2"])
    
main()
