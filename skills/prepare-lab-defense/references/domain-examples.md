# Domain prompts and synthetic examples

These small examples are original teaching fixtures, not copied student work or universal assignment requirements. Their file names and symbols refer only to the examples below. Replace them with verified locators from the student's actual lab. Load only the relevant section.

## Numerical computation

Possible topics: task data, algorithm choice, one iteration by hand, matrix decomposition, stopping criterion and safeguard, convergence assumptions, reconstruction/residual, approximation error, or comparison across step sizes. Use only those relevant to the assigned method.

Synthetic fixed-point task: solve x = 0.5*x + 1 from x0 = 0, with tolerance 0.01.

```python
# iteration.py — synthetic example


def solve(tol=0.01, limit=100):
    x = 0.0
    q = 0.5
    for k in range(1, limit + 1):
        previous = x
        x = 0.5 * previous + 1.0
        bound = q / (1.0 - q) * abs(x - previous)
        if bound <= tol:
            return x, k, bound
    raise RuntimeError("Accuracy not reached")
```

`solve` applies the iteration, computes the a posteriori bound for the contraction q = 0.5, and distinguishes reaching tolerance from exhausting the safeguard. The contraction maps the real line into itself and has the unique fixed point 2. After k iterations, x_k = 2 - 2^(1-k). At k = 8, x = 1.9921875 and the error and bound both equal 0.0078125. Substitution residual is 0.00390625 in magnitude; it is a different quantity from the solution error.

Beginner opening: “The program is looking for a number that stays the same after we halve it and add one. We start at zero; the inputs also set the desired accuracy and the maximum number of steps. The result is an approximate number, a step count, and an error bound. Let's first see one step: half of zero plus one is one.” Offer: “If we repeat that rule with one, what do we get?” Do not ask the novice to explain contraction or the loop before teaching them.

If the student says “I don't know,” work through half of one plus one = 1.5, perhaps as 0.5 + 1 on a number line. Offer the smaller supported step “Half of two is one; now add one.” After that, gradually ask them to do a whole step. Introduce x_k as the current approximation and map the update to `solve`'s `previous` and `x` only after the rule is clear. Teach the bound and its assumptions in later fragments, not in this opening.

If a learner says “a small change always means a small error,” correct that claim: the displayed bound depends on contraction and q < 1. If contraction has not been explained, first show how halving shrinks the distance between two inputs, then introduce q. Offer a counterexample when needed rather than testing an unexplained condition. A map x → x + 0.001 changes little at every step and has no fixed point; the given bound cannot be applied with q = 1.

Mock question: “Locate the accuracy check and explain why the loop limit cannot replace it.” Keep the worked answer hidden until debrief. Delayed question: “For contraction factor 0.9, what multiplies the step difference in this bound?” Expected factor: 9; no need to solve a new full lab.

## Computer graphics

Select among pipeline stages and methods, CPU/shader interfaces, GPU resource lifetime or synchronization, coordinate spaces, geometry and normals, texture sampling, visual interpretation, demonstration controls, and implementation limits. Do not require Vulkan concepts from a software rasterizer or lighting from an unlit assignment.

Synthetic column-vector transform, with CPU and shader interfaces already matched:

```cpp
// scene.cpp — synthetic pseudocode, not a graphics API declaration
model = translate(1, 0, 0) * scale(2, 2, 2);
uploadObjectUniform(model);
bindObjectUniform();
drawMesh();
```

```glsl
// mesh.vert — synthetic shader fragment
vec4 world = object.model * vec4(position, 1.0);
gl_Position = scene.projection * scene.view * world;
```

The local point (1, 0, 0) becomes (3, 0, 0) in world coordinates; reversing the two CPU factors yields (4, 0, 0). `uploadObjectUniform` sends model data; the binding makes it accessible to the draw; the vertex shader uses it before view and projection. A real explanation must inspect the actual layout/binding and upload code rather than infer compatibility from this pseudocode. Clip coordinates precede perspective division and viewport mapping. Both orthographic and perspective projections can use matrices; their visible depth-size behavior differs.

Beginner opening: “This lab draws a model at a chosen size and position. The inputs include its points and the transformation settings; the expected output is an image showing it there. For now, take just one point: its x coordinate is 1. Enlarging by two changes it to 2; moving it one unit to the right changes it to 3.” Offer: “What x coordinate would we get if we moved that enlarged point one more unit right?” Do not ask for matrix multiplication or pipeline terminology before explaining them.

If the student says “I don't know,” show positions 2, 3, and 4 on a line and demonstrate one move. Offer a supported move from 3 with the same rule, then later a new starting point with less help. Introduce model coordinates, the column-vector convention, and the model matrix only as needed in later fragments. Map the operations to `scene.cpp` and then `mesh.vert`; in a real lab, inspect the actual CPU upload and shader data use. Ask for a prediction before a later demo once the relevant operation has been explained. Do not require a novice to identify unfamiliar shader code before this mapping.

For a lighting assignment, a synthetic cube with shared averaged vertex normals can show smooth lighting across planar faces. Its silhouette remains angular; shading has not turned it into a sphere. For sharp edges, inspect whether face corners have distinct vertex records/normals. Under an invertible nonuniform model transform, normals generally require the inverse transpose of its linear part, with normalization for lighting. Ask about the coordinate space used for the light and normal before declaring a shader defective.

Mock question: “Predict the visual difference after changing the projection, then show the code that causes it.” Delayed question: “If the image looks rounded but the silhouette is still a cube, what data would you inspect first, and why?” A screenshot alone cannot establish which implementation path ran or that all assignment requirements pass.
