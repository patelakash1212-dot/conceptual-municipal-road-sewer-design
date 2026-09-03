# Municipal Road and Sewer Design Portfolio

![Civil 3D](https://img.shields.io/badge/Autodesk-Civil%203D-2878B5?style=for-the-badge)
![Project](https://img.shields.io/badge/Project-Conceptual-21A6A1?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Not%20for%20Construction-E55A5A?style=for-the-badge)

An anonymized Civil 3D portfolio demonstrating a coordinated municipal road and sewer model carried from public terrain information through plan/profile sheet production.

> **Conceptual Portfolio Project - Not for Construction.** This repository demonstrates software and drawing-production skills. It is not an issued design, permit submission, tender package, record drawing or construction document.

[![Municipal Road and Sewer Design Portfolio cover](assets/portfolio-cover.png)](docs/Municipal_Road_and_Sewer_Design_Portfolio.pdf)

<div align="center">

**Click the cover to open the complete portfolio.**

</div>

## Portfolio

[View the complete portfolio PDF](docs/Municipal_Road_and_Sewer_Design_Portfolio.pdf)

The portfolio presents the project brief, design-basis and verification matrix, controlled model-to-sheet workflow, municipal authorization workflow, four drawing exhibits, and an explicit senior-review boundary.

## Project at a Glance

| Design component | Demonstrated work |
|---|---|
| Existing conditions | Existing-ground surface assembled from publicly available mapping and LiDAR-derived terrain information |
| Road | Alignment, profile, corridor modelling and intersection lane-width coordination |
| Storm sewer | Pipes, maintenance structures, plan/profile display, labels and profile bands |
| Sanitary sewer | Pipes, maintenance structures, plan/profile display, labels and profile bands |
| Drawing production | View frames, match lines, plan/profile sheets, colour plotting and sheet-set publication |
| Quality review | Network/profile consistency, structure placement, slopes, inverts, cover targets and drawing readability |

## Drawing Sample

![Plan and profile drawing sample](assets/plan-profile-sample.png)

## Model and Production Workflow

1. Organize GIS and LiDAR-derived source information and state its limitations.
2. Develop the existing-ground surface, alignments and reference profiles.
3. Model the road corridor, intersection geometry, lane transitions and grading intent.
4. Coordinate storm and sanitary pipes and structures in plan and profile.
5. Assemble production drawings using data shortcuts, XREFs, profile bands, view frames and match lines.
6. Publish the colour sheet set and complete model, annotation and PDF checks.

## Conceptual Design Basis

The model was developed using the following project controls, interpreted from applicable local municipal infrastructure requirements:

| Design element | Criterion applied in the conceptual model |
|---|---|
| Storm sewer cover | Minimum target of 1.5 m; current exported results include exceptions that require correction and re-verification |
| Sanitary sewer cover | Minimum target of 2.5 m; independent network-export verification remains pending |
| Road profile | Grades and vertical transitions checked against applicable municipal geometric requirements |
| Lane drainage | Typical 2.0% crossfall from crown toward gutter where applicable |
| Horizontal coordination | Lane widths, intersection tie-ins and corridor-region transitions coordinated by station |
| Pipe-network coordination | Diameters, slopes, inverts, structure depths, cover and crossings reviewed in plan and profile |
| Drawing coordination | Plan/profile agreement, labels, bands, match lines and colour plotting reviewed |

These are portfolio design controls, not claims of completed compliance. The storm network must be rebuilt and its cover exceptions resolved; the sanitary network still requires an equivalent independent cover report. A real project also requires current survey, utility records, geotechnical information, hydrology and hydraulic calculations, downstream-capacity confirmation, constructability review and licensed engineering oversight.

## Municipal Delivery and CLI-ECA Workflow

1. **Confirm project scope and asset ownership.** Identify existing and proposed works, who owns and operates them, whether proposed works will be transferred to the municipal owner, and whether the activity is maintenance, repair, a lateral connection or an alteration.
2. **Obtain the owner's current environmental approval and requirements.** Confirm whether the work affects a municipal sewage collection system, stormwater management system or privately owned works. Establish prescribed-person status and request pre-consultation where needed.
3. **Determine the authorization route.** Schedule D contains the conditions for future pre-authorized alterations. If the proposed alteration satisfies every applicable condition, complete the pre-authorized process and required records. If it is not pre-authorized, the approval holder or an authorized party must obtain a Schedule C amendment before undertaking the alteration.
4. **Prepare the design-stage submission.** Assemble the design brief, stamped drawings when required, design sheets, calculations, supporting reports, criteria-exception list, inspection/testing plan and applicable alteration records. Typical records include SS1/SS2 for sewage collection works and SW1/SW2/SW3 for stormwater works, depending on scope.
5. **Complete detailed design and QA/QC.** Coordinate road geometry, survey, existing utilities, geotechnical constraints, hydrology/hydraulics, receiving-system capacity, pipe cover and clearances, constructability, quantities, specifications and independent checking.
6. **Screen parallel approvals.** Confirm applicable planning and Environmental Assessment Act obligations, conservation authority and source-protection requirements, road and utility permits, heritage/archaeology, property/easements, traffic staging, erosion and sediment control, and stakeholder consultation.
7. **Construction and closeout.** Maintain inspection and testing records; complete CCTV, mandrel, leakage or other testing as applicable; resolve deficiencies; prepare as-built information and O&M documentation; complete post-construction verification; and submit required owner or Director notifications.

The CLI-ECA pathway does not itself prove that downstream capacity exists, that all other permits are satisfied, or that the work is ready for construction.

### Regulatory Source Basis

The delivery workflow is based on current Ontario Ministry of the Environment, Conservation and Parks material:

- [Municipal Consolidated Linear Infrastructure Environmental Compliance Approvals](https://www.ontario.ca/page/municipal-consolidated-linear-infrastructure-environmental-compliance-approvals)
- [Supporting documentation and technical requirements for an ECA](https://www.ontario.ca/document/guide-applying-environmental-compliance-approval-0/supporting-documentation-and-technical)
- [Ontario Central Forms Repository - MECP CLI-ECA records](https://forms.mgcs.gov.on.ca/en/dataset/?_organization_limit=0&organization=ministry-of-environment-conservation-and-parks&q=CLA-1-F)

The municipality's current CLI-ECA, project-specific conditions and latest forms must always be checked before using this workflow on a real project.

## Verification Status

| Status | Scope |
|---|---|
| Demonstrated | Civil 3D object organization, road and intersection coordination, pipe-network plan/profile display, annotation, bands, XREFs, view frames, match lines and colour sheet publication |
| Requires further checking | Pipe connectivity, all cover values, crossings, hydraulic capacity, downstream reserve capacity, design exceptions and drawing-sheet defect review |
| Not represented as complete | Survey verification, utility locates, geotechnical design, quantities, specifications, approvals, licensed engineering review, construction inspection and as-built closeout |

## Data and Engineering Limitations

Existing conditions were interpreted from public GIS and LiDAR-derived terrain information. Utility locations, elevations, materials and capacities require survey, records review, subsurface investigation, field verification and engineering review before real-world use.

The drawings have not been independently checked, approved, sealed, tendered or constructed. File existence and successful Civil 3D regeneration do not establish technical compliance or design suitability.

## Repository Structure

```text
.
|-- README.md
|-- PROJECT_NOTES.md
|-- docs/
|   `-- Municipal_Road_and_Sewer_Design_Portfolio.pdf
`-- assets/
    |-- portfolio-cover.png
    `-- plan-profile-sample.png
```

## Software

- Autodesk Civil 3D
- AutoCAD sheet sets and external references

## Author Note

This project is intentionally anonymized. The public repository excludes original survey data, GIS source files, proprietary references, editable production drawings and any real street name.
