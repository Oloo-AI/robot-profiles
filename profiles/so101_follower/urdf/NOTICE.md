# SO-101 robot description — NOTICE

Source: https://github.com/TheRobotStudio/SO-ARM100 (`Simulation/SO101/`), licensed Apache-2.0
(same license text as this repository's root `LICENSE`; TheRobotStudio's SO-ARM100 is itself
Apache-2.0 licensed, so no separate license file is duplicated here).
Upstream commit: `7629d2ad9853d10fb903093a33ef6114099d97e5`.

Copied here (unmodified re-export) from `Oloo-AI/oloo-studio`
(`packages/oloo/src/oloo/assets/robots/so101/`), which is the source of truth for
the desktop app's built-in copy. This registry entry mirrors it so the profile is
fetchable over a public raw URL — `oloo-studio` itself is a private repository.

`robot.urdf` is verbatim (`so101_new_calib.urdf`), with mesh `filename="assets/…"`
attributes rewritten to `filename="meshes/…"` to match this directory's layout.
No geometry was changed.

Meshes were decimated with quadric edge collapse
(`scripts/prepare_so101_assets.py --ratio 0.4` in `oloo-studio`) and re-exported as
binary STL; geometry is approximate and intended for visualization only, not for
manufacturing or precision simulation.

| mesh | triangles (upstream) | triangles (here) | bytes |
|---|---:|---:|---:|
| base_motor_holder_so101_v1.stl | 37540 | 15016 | 750884 |
| base_so101_v2.stl | 9430 | 3772 | 188684 |
| motor_holder_so101_base_v1.stl | 22586 | 9034 | 451784 |
| motor_holder_so101_wrist_v1.stl | 21042 | 8416 | 420884 |
| moving_jaw_so101_v1.stl | 28270 | 11308 | 565484 |
| rotation_pitch_so101_v1.stl | 17672 | 7068 | 353484 |
| sts3215_03a_no_horn_v1.stl | 17316 | 6926 | 346384 |
| sts3215_03a_v1.stl | 19080 | 7632 | 381684 |
| under_arm_so101_v1.stl | 39516 | 15806 | 790384 |
| upper_arm_so101_v1.stl | 26068 | 10426 | 521384 |
| waveshare_mounting_plate_so101_v2.stl | 1254 | 1254 | 62784 |
| wrist_roll_follower_so101_v1.stl | 28796 | 14120 | 706084 |
| wrist_roll_pitch_so101_v2.stl | 53994 | 21596 | 1079884 |

Total mesh bytes: 6619792

This directory is used by both `profiles/so101_follower/` and `profiles/so101_leader/`
(the leader and follower SO-101 kits share the same physical arm geometry);
`so101_leader/profile.json` points its `kinematics.urdf.url` at these files rather
than duplicating them.
