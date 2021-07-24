bl_info = {
    'name': 'Vertex Weights to UV Map',
    "author": "Shankar Sivarajan", # Mostly Alessandro Zomparelli.
    "version": (0, 0, 1),
    'blender': (2, 93, 0),
    'description': 'Convert vertex weights to UV map coordinates',
    'category': 'Mesh',
}


import bpy
import  numpy as np

# Functions copied from the ``Tissue'' addon.

def get_attribute_numpy(elements_list, attribute='select', mult=1):
    '''
    Generate a numpy array getting attribute from a list of element using
    the foreach_get() function.
    '''
    n_elements = len(elements_list)
    values = [0]*n_elements*mult
    elements_list.foreach_get(attribute, values)
    values = np.array(values)
    if mult > 1: values = values.reshape((n_elements,mult))
    return values

def bmesh_get_weight_numpy(group_index, layer, verts):
    weight = np.zeros(len(verts))
    for i, v in enumerate(verts):
        dvert = v[layer]
        if group_index in dvert:
            weight[i] = dvert[group_index]
            #dvert[group_index] = 0.5
    return weight


class Vertex_Weights_to_UV(bpy.types.Operator):
    bl_idname = 'object.vert_weights_to_uv'
    bl_label = 'Vertex Weights to UV'
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        ob = context.active_object
        me = ob.data
        
        active_group = bpy.context.object.vertex_groups.active.name
        
        weight = []
        for v in me.vertices:
            try:
                weight.append(ob.vertex_groups[active_group].weight(v.index))
            except:
                weight.append(0)
        
        weight = np.array(weight)        
        
        uv_layer_name = active_group
        
        if uv_layer_name in me.uv_layers.keys():
            uv_layer = me.uv_layers[uv_layer_name]
        else:
            uv_layer = me.uv_layers.new(name=uv_layer_name)
            
        loops_size = get_attribute_numpy(me.polygons, attribute='loop_total', mult=1)
        n_data = np.sum(loops_size)
        v_id = np.ones(n_data)
        me.polygons.foreach_get('vertices',v_id)
        v_id = v_id.astype(int)
        
        uv_x = weight[v_id,None]
        uv_y = weight[v_id,None]
        
        uv = np.concatenate((uv_x,uv_y),axis=1).flatten()
        
        uv_layer.data.foreach_set('uv',uv)
        me.uv_layers.update()

        return {'FINISHED'}


class WeightsToUV_Menu(bpy.types.Menu):
    bl_label = 'Vertex Weights to UV'
    bl_idname = 'OBJECT_MT_vert_weights_to_uv'

    def draw(self, context):
        self.layout.operator(Vertex_Weights_to_UV.bl_idname)


def menu_func(self, context):
    self.layout.menu(WeightsToUV_Menu.bl_idname)


def register():
    bpy.utils.register_class(WeightsToUV_Menu)
    bpy.utils.register_class(Vertex_Weights_to_UV)
    bpy.types.VIEW3D_MT_object.append(menu_func)


def unregister():
    bpy.utils.unregister_class(WeightsToUV_Menu)

    bpy.utils.unregister_class(Vertex_Weights_to_UV)
    bpy.types.VIEW3D_MT_object.remove(menu_func)


if __name__ == "__main__":
  register()