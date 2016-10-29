#context overriding:
win      = bpy.context.window
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
            }

#menu via operator:
class Menu(bpy.types.Operator) :      
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
        bpy.ops.object.select_all(action='DESELECT')
        if (self.DropDownList != "NULL"):
            obj = bpy.data.objects[self.DropDownList]
            obj.select = True
        
            self.xCoord = obj.location.x
            self.yCoord = obj.location.y
            self.zCoord = obj.location.z        

        return {"FINISHED"}
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "DropDownList")
        
        col = layout.column()
        col.label(text="Attributes:")
       
        col.prop(self, "xCoord")
        col.prop(self, "yCoord")
        col.prop(self, "zCoord")
        layout.operator("update.button")

#line class:
class Line():
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
        self._material = None
        
        
    def link(node1, node2):
        Line('line ' + node1._obj.name + ' / ' + node2._obj.name, node1, node2)

