import random

import bpy

#import nodeLib
from .debug import Debug_Tools
from . import cleanup
from . import node_dataLoader

from . import nodeLib

class CreateViz_OT_Operator(bpy.types.Operator):
    bl_idname = "view3d.create_ot_viz"
    bl_label = "Create Viz Operator"
    bl_description = "Creates Visualization of Node data"
    
    
    def execute(self, context):
        # do something
        Debug_Tools.debug_msg("----------------------------------------------------------------")
        Debug_Tools.debug_msg("Create viz STARTED")
        # single script


        Debug_Tools.set_force_off(False)

        """
        step 1: cleanup if true
        """

        if True:
            cleanup.run_cleanup()


            
        """
        step 2: create a new collection 'Node_data_Viz'.
        default parent: Scene Collection or active collection
        """
        # TODO create the main viz collection
        if 'Node_data_Viz' in bpy.data.collections:
            Node_data_Viz_Coll = bpy.data.collections['Node_data_Viz']
        else:
            Node_data_Viz_Coll = bpy.data.collections.new('Node_data_Viz')
        # TODO create new collection
        # Note: if the name already exists blender adds 001
        Node_data_Viz_Coll_new = bpy.data.collections.new('Node_data_Viz.000')

        # TODO link main viz collection to the scene main collection
        if 'Node_data_Viz' not in bpy.context.scene.collection.children:
            bpy.context.scene.collection.children.link(Node_data_Viz_Coll) 
        
        # TODO link the new collection to the main viz collection
        Node_data_Viz_Coll.children.link(Node_data_Viz_Coll_new) 
        # TODO make 'Node_data_Viz.xxx' active collection
        layer_coll = bpy.context.view_layer.layer_collection.children['Node_data_Viz'].children[-1]
        bpy.context.view_layer.active_layer_collection = layer_coll
        """
        step 3: load database to visualize
        Currently nodeLib cannot export database. So create a sample database and load that.
        """
        node_pack_data = node_dataLoader.load_data()

        """
        step 4: create viz
        """
        #createViz(nodepack, visualiser)
        def corner_prescribe():
            bpy.ops.mesh.primitive_cube_add(enter_editmode=True, location=(0,0,0))
            bpy.context.active_object.name = 'corner_piece'
            bpy.ops.mesh.subdivide()
            bpy.ops.mesh.delete(type='ONLY_FACE')
            bpy.ops.object.editmode_toggle()
            bpy.data.objects['corner_piece'].hide_viewport = True
            return bpy.data.objects[-1]
            
        corner_piece = corner_prescribe()
        
        def visualiser1(nodePack: nodeLib.structure.node_structs.NodePack_Struct):
            # TODO center cursor
            bpy.ops.view3d.snap_cursor_to_center()
            # TODO create a empty/box with respective node_ID
            Debug_Tools.debug_msg("creating empty for node {}: {}".format(0, nodePack.pack[0].node_ID))
            bpy.ops.object.empty_add(type='PLAIN_AXES', radius=0.5, align='WORLD', location=(0, 0, 0), rotation=(0, 0, 0))
            bpy.context.active_object.name = 'node.000'
            #bpy.data.objects[-1].name = 'node.000'
            for count, node_ in enumerate(nodePack.pack[1:]):
                Debug_Tools.debug_msg("creating empty for node {}: {}".format(count+1, node_.node_ID))
                curr_node_empty = bpy.context.active_object
                # each node can have 26 neighbors
                # TODO pick a random number btw 1 to 26
                rand_pos = random.randint(0,25)
                Debug_Tools.debug_msg('rand_pos: {}'.format(rand_pos))
                # TODO reposition the corner_piece to the node.xxx location
                # bpy.context.view_layer.objects.active = bpy.data.objects['corner_piece']
                bpy.data.objects['corner_piece'].location = curr_node_empty.location
                # bpy.data.objects['corner_piece'].data.vertices[5].co.copy()
                # TODO get the new location for next node empty
                next_loc = tuple(bpy.data.objects['corner_piece'].data.vertices[rand_pos].co)
                # TODO create the next node empty
                bpy.ops.object.empty_add(type='PLAIN_AXES', radius=0.5, align='WORLD', location=next_loc, rotation=(0, 0, 0))
                bpy.context.active_object.name = 'node.000'
                
        
        visualiser1(node_pack_data)
        
        Debug_Tools.debug_msg("Create viz ENDED")
        Debug_Tools.debug_msg("----------------------------------------------------------------")
        return {'FINISHED'}