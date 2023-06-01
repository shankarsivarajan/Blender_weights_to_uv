# Vertex Weights to UV Map

Convert vertex weights to UV coordinates, for use in shaders. The [Tissue](https://github.com/alessandro-zomparelli/tissue) addon includes this function for the reaction–diffusion weights.

## Instructions

- Select the vertex group you wish to convert to UV map.
- Select the object in `Object` mode, and click on `Object > Vertex Weights to UV > Active Vertex Group`(or `All Vertex Groups`).
- This should create a new UV map with the same name as the selected vertex group.
- The weights in the vertex group are now available in the Shader editor through the "UV Map" node.
