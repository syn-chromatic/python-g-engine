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
* Issue: Lighting simple is flawed and is only a placeholder
* Issue: Frustum Clipping doesn't work for quad polygons
* Issue: Projection math causes drift when an object is positioned on an axis plane
* Issue: Performance optimization is needed for draw calls
* Issue: Text Writer flickering and disappearance
* Change: Implement a Draw Call system
* Change: Implement Backface Culling
* Change: Separate physics from the Body abstraction 

___

### Gravity Simulation ~30 objects (Cubes and Particles, No Collision)
https://user-images.githubusercontent.com/68112904/221572327-ffb9d2fb-e025-46a3-b639-8ac5723b0159.mp4

___

### Collision Simulation ~150 objects (Particles)
https://user-images.githubusercontent.com/68112904/222963578-858a5a60-f47b-41aa-b9cb-ddd21c583262.mp4

___

### Camera Projection and Mouse Controls
https://user-images.githubusercontent.com/68112904/224444553-2adc66f0-874c-4fcf-be2b-799e9468d499.mp4


