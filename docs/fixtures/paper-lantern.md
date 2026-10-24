# Paper Lantern

`LV_PaperLantern` is the map entry in the Nightglass fixture. The room has two
light sources in the sketch: a desk lamp and a paper shade near the window.
The map name comes from the latter.

## Things the prefix checker won't catch

- Two different materials with names that both start with `M_`.
- A texture using the wrong colour space.
- A mesh with a missing collision setup.
- An empty level with a perfectly valid `LV_` prefix.

That last case is why the sample includes a map: a clean naming report says
very little about whether a scene is usable.

There is no `.uproject`, packaged level or download attached to this fixture.
The checked-in JSON is the complete example. You don't need to find a build
to run it.
