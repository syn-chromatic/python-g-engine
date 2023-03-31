# Python G-Engine and Simulations
Python is too slow for these types of simulations, see the Rust implementation (being worked on)
https://github.com/syn-chromatic/rust-physics-simulation

___
# Setup
```
pip install typing-extensions
pip install pygame
```

___
# Issues and Upcoming changes 
* Issue: Physics is currently broken
* Issue: Frustum Clipping doesn't work for quad polygons
* Issue: Projection math causes drift when an object is positioned on an axis plane
* Issue: Performance optimization is needed for draw calls
* Issue: Text Writer flickering and disappearance for the Turtle graphical backend
* Issue: ZBuffer needs improvement
* ~~Change: Implement a Draw Call system~~
* ~~Change: Implement a Z-Buffer~~
* ~~Change: Implement Backface Culling~~
* Change: Separate physics from the Body abstraction 


___
### Same scene from below, but with Backface Culling, performance improves.
https://user-images.githubusercontent.com/68112904/228908793-249e8fb0-3466-40ea-9998-a8acfccbf5af.mp4

___
### Scene with simple PBR lighting, mesh models loaded from the built-in OBJ file loader.
https://user-images.githubusercontent.com/68112904/228430947-58a5b0d0-a3e1-4d1a-9a93-9393def56874.mp4

___
### Collision Simulation ~150 objects (Particles) *(currently broken)*
https://user-images.githubusercontent.com/68112904/222963578-858a5a60-f47b-41aa-b9cb-ddd21c583262.mp4

___


