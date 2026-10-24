# Nightglass

`nightglass` is the workspace label in the sample inventory. Think of a small
desk scene: a desk, a lamp, a shared material and a room-tone loop. The JSON is
a hand-written fixture, so you can try the audit without downloading a project.

## Expected findings

| Asset | Result |
| --- | --- |
| `SM_Desk` | Pass |
| `DeskLamp` | Missing `SM_` |
| `M_Desk` | Pass |
| `desk_basecolor` | Missing `T_` |
| `LV_PaperLantern` | Pass |
| `RoomTone` | Skip: no `SoundWave` rule |

The audit should report two findings and return exit status `1`. The lowercase
texture name is intentional; leave it in the fixture so the example has
something useful to report.

The workspace label isn't read by either script. It's just a way to tell this
sample apart from another project's export.

The level entry has its own [scene note](paper-lantern.md).
