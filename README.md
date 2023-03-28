# Python G-Engine and Simulations
Python is too slow for these types of simulations, see the Rust implementation (being worked on)
https://github.com/syn-chromatic/rust-physics-simulation

___
# Setup
No external libraries are required, other than typing-extensions.

```pip install typing-extensions```

___
# Issues and Upcoming changes 
* Issue: Physics is currently broken
* Issue: Lighting is flawed and is only a placeholder
* Issue: Frustum Clipping doesn't work for quad polygons
* Issue: Projection math causes drift when an object is positioned on an axis plane
* Issue: Performance optimization is needed for draw calls
* Issue: Text Writer flickering and disappearance for the Turtle graphical backend
* Change: Implement a Draw Call system
* Change: Implement Backface Culling
* Change: Separate physics from the Body abstraction 

___
### Scene with simple lighting, mesh models loaded from the built-in OBJ file loader.
https://user-images.githubusercontent.com/68112904/228265504-85410196-b1f5-4eb0-b052-797b9d497c06.mp4

___
### Collision Simulation ~150 objects (Particles) *(currently broken)*
https://user-images.githubusercontent.com/68112904/222963578-858a5a60-f47b-41aa-b9cb-ddd21c583262.mp4

___


