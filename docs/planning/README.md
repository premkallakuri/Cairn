# Atlas Haven Planning

- Status: Current + Planned
- Audience: Product owners, maintainers, release planners
- Source of truth: Planning and control layer for rewrite progress after the documentation system was established
- Related modules/features: `M00-M14`, PRD, feature specs, module notes, rebuild roadmap

This folder is the planning and coordination layer for the Atlas Haven rewrite.
It sits between the product-definition docs and the engineering delivery notes.
Use it to answer three questions:

- what is already complete in the rewrite
- what the next implementation wave should build
- in what order the near-term roadmap should be executed

## Planning Documents

- [`completed-features.md`](./completed-features.md): canonical inventory of what is complete through `M14`
- [`e2e-verification-and-gaps.md`](./e2e-verification-and-gaps.md): latest E2E verification run, API probes, and requirement gap summary
- [`roadmap-next-wave.md`](./roadmap-next-wave.md): near-term roadmap after `M12`
- [`next-wave-sequencing.md`](./next-wave-sequencing.md): recommended execution order and completion gates for the next wave

## Related Core References

- Product contract: [`../prd/atlas-haven-prd.md`](../prd/atlas-haven-prd.md)
- Release framing: [`../prd/release-phasing.md`](../prd/release-phasing.md)
- Feature definitions: [`../features/README.md`](../features/README.md)
- Delivery evidence: [`../modules/`](../modules/)
- Long-horizon rebuild source material: root repo `docs/rebuild/`

## How To Use This Folder

- Start with `completed-features.md` when you need to know the current shipped shape.
- Use `roadmap-next-wave.md` when choosing the next feature outcome to build.
- Use `next-wave-sequencing.md` when converting roadmap intent into an implementation order and test plan.

This folder is rewrite-scoped. It does not replace the broader rebuild master
plan in the root repo; it summarizes only the immediately relevant next wave for
Atlas Haven.
