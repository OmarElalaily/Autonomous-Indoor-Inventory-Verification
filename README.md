# Autonomous Indoor Inventory Verification

A ROS 2 (Jazzy) project for autonomous indoor inventory verification. The robot navigates through predefined waypoints using Nav2 (AMCL) and performs shelf-level auditing using OpenCV ArUco marker detection. Results are logged to a CSV report for compliance / mismatch tracking.

## Key Features
- ROS 2 Jazzy + Nav2 waypoint navigation (AMCL localization)
- Autonomous patrol between waypoints for repeatable audits
- OpenCV ArUco detection for shelf / bay / product identification
- CSV reporting for audit results (found / missing / mismatched IDs)
- Modular bringup structure (PiBot + camera)

## Project Structure (work in progress)
- `src/pibot_bringup/` : robot bringup, navigation launch, parameters, maps
- `src/camera_bringup/` : camera bringup and perception/auditing nodes
- `docs/` : project report (PDF) and documentation assets

## Quick Start (placeholder)
> This repository is being migrated from container-based development to a clean ROS 2 workspace layout.
1. Clone the repository
2. Build with `colcon build`
3. Launch bringup + navigation + camera nodes (see `launch/` folders)

## Documentation
- See `docs/Autonomous_Indoor_Inventory_Verification.pdf`

## License
MIT
