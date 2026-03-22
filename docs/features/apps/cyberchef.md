# CyberChef App Package

- Status: Current + Planned
- Audience: Operators, app authors, maintainers
- Source of truth: App package specification for `nomad_cyberchef`
- Related modules/features: `M12`, App Dock, Control Room

## Why It Exists

CyberChef provides a browser-based data transformation toolkit for local utility
and analysis tasks.

## Current Package Contract

- Service ID: `nomad_cyberchef`
- Kind: `sibling_app`
- Image: `mpepping/cyberchef:latest`
- Port mapping: `8001 -> 8000`
- No persistent mount required
- Healthcheck: HTTP on port `8000`

## Operator-Visible Behavior

- appears in App Dock with Control Room-oriented utility positioning
- exposes launch URL `http://127.0.0.1:8001`
- supports reinstall and update operations

## Planned Evolution

- richer utility-tool explanations and operational grouping

## Acceptance Criteria

- CyberChef installs and remains operable through App Dock lifecycle actions
