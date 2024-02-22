# Blender Decentraland Toolkit: Cannon Colliders

This is a Blender plugin for exporting Rigidbodies to JSON as Cannon-compatible colliders. The results are exported to a JSON file that contains the data needed to create Trimesh colliders.

It was written for use with the **Infinity Engine** in Decentraland - see the [Decentrally repository](https://github.com/decentraland-scenes/decentrally) for more information.


### Features

* Export Rigidbodies as cannon colliders

Installation
--
* Download the latest version from the [Releases](/releases) page
* In Blender, go to `Edit > Preferences > Addons > Install`
* Select the .zip file
* Once installed, ensure the plugin is activated (ticked) in the list of Addons

Once installed you can find it in `3D Viewport -> Sidebar -> DCL Toolkit -> Cannon Colliders`

![blender ui panel location](./assets/blender-ui-location.png)


How to use
---
* Place your colliders in a collection
* Give each of your colliders a **Rigidbody** in the Physics tab:
	* Set the type to Passive
	* Under "Collisions" set the Shape. Currently only "Mesh" with source "Base" is supported.
	* Under "Surface Response" set both the "Friction" and "Bounciness"
* In the **DCL Toolkit** sidebar panel, under section **Cannon Colliders**: 
    * Choose your collection in the dropdown 
    * Configure output path (see below)
    * Click the "Export" button



### Settings:

The following options are available in the Cannon Colliders panel: 

#### Export collection

* Choose the collection of colliders you wish to export
* Click the refresh symbol if your collection is not in the dropdown
* All objects in the collection **with a Rigidbody** will be exported - visbility is ignored

#### Output path
* Blender uses `//` for relative paths
* Use `//colliders.json` to output to a file in the current blend file location

#### JSON: minify output
* Significantly reduces JSON export file size
* Disable for dev; enable for production


How does it work
--

The addon peforms roughly the following process when the "Export" button is clicked:

* Loop through all objects in the specified collection
* Check if the object has a Rigibody component
* Create an object representing the object mesh and its Rigidbody properties
* Export all objects to the specified JSON file


Collider JSON
---

> **NOTE:** Positions and indexes are in XYZ order, with Z representing the vertical (up) axis

The addon exports a JSON structure describing the colliders to the output file specified. By default this is `colliders.json`.

It contains the following information:

```js
{
	"name"           : "park",            // Name of the tileset (the collection name)
	"tileset_size"   : [ 7,   6,   2   ], // The total size (in tiles) of the tileset
	"tileset_origin" : [ 0.0, 0.0, 0.0 ], // The origin position of the tileset
	"tile_dimensions": [ 8.0, 8.0, 4.0 ], // The size (in Blender units) of each tile
	"tile_format"    : "GLTF_SEPARATE",   // glTF format, possible values are GLB, GLTF_SEPARATE
	"tile_origin"    : "CENTER",          // Tile origin, possible values are CENTER, TILE_MIN, TILE_MAX
	"tiles"          : [                  // A nested array of tiles 
		[
			[
				{ 
					"index"     : [ 0, 0, 0 ],       // The index of this tile in the tiles array
					"src"       : "tile_0_0_0",      // The gltf filename. File extension derived from tile_format 
					"pos_center": [ 4.0, 4.0, 2.0 ], // The tile center 
					"pos_min"   : [ 0.0, 0.0, 0.0 ], // The minimum bounds of this tile
					"pos_max"   : [ 8.0, 8.0, 4.0 ]  // The maximum bounds of the tile
				}, // ... etc, for each tile
			],
		],
	]
}
```


Known issues, limitations and caveats:
--

1) Does not apply modifiers. Exported mesh data represents the base mesh.
1) Object visibility is ignored - if it's in the collection, it gets exported

ToDo:
--
[ ] Show warning if objects are missing RBs  
[ ] Support shapes properly: box, sphere  
[ ] Add option to apply modifiers  
[ ] Add option to flip tileset.json YZ on export  
[ ] Make all collections objects visible to avoid error with exporter  