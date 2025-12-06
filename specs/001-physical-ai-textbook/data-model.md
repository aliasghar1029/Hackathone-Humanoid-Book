# Data Model: Physical AI & Humanoid Robotics Textbook

**Feature Branch**: `001-physical-ai-textbook`
**Date**: 2025-12-05
**Spec**: specs/001-physical-ai-textbook/spec.md
**Plan**: specs/001-physical-ai-textbook/plan.md

## Entities

### Textbook
Represents the overall textbook content and its high-level structure.

-   **`title`** (String): The main title of the textbook.
-   **`focus`** (String): The primary focus or theme of the textbook.
-   **`quarter_overview`** (String): A descriptive paragraph summarizing the course.
-   **`why_physical_ai_matters`** (String): A paragraph explaining the importance of physical AI.
-   **`learning_outcomes`** (List of Strings): A list of educational objectives for the course.
-   **`weekly_breakdown`** (List of Strings): A list detailing the topics covered each week.
-   **`assessments`** (List of Strings): A list of methods used to evaluate student learning.
-   **`modules`** (List of Module objects): A collection of the core instructional modules.
-   **`hardware_requirements`** (List of HardwareRequirement objects): A collection of hardware specifications.

### Module
Represents an individual instructional module within the textbook.

-   **`number`** (Integer): The sequential number of the module (e.g., 1, 2, 3).
-   **`title`** (String): The full title of the module.
-   **`bullets`** (List of Strings): A list of key topics or learning points within the module.
-   **`is_capstone`** (Boolean): Indicates if the module contains a capstone project (e.g., Module 4).

### HardwareRequirement
Represents a specific hardware requirement section, including its descriptive table.

-   **`type`** (String): A descriptive title for the hardware requirement category (e.g., "Digital Twin Workstation").
-   **`table_data`** (List of Dictionary/Map): Structured representation of the Markdown table, where each item in the list is a row, and each dictionary/map represents column headers and their values.
    -   *Example for Digital Twin Workstation Table Row:*
        ```yaml
        - Component: GPU
          Minimum Specification: RTX 4070 Ti+
          Recommended Specification: RTX 4090
        ```

## Relationships

-   **Textbook** `has many` **Module**
-   **Textbook** `has many` **HardwareRequirement**

## Data Flow (Conceptual)

1.  **PDF Ingestion**: The initial 9-page PDF content is processed.
2.  **Markdown Conversion**: The PDF content is converted into structured Markdown files, aligning with the `Module` and `Textbook` entities.
3.  **Docusaurus Rendering**: Docusaurus consumes the Markdown files and associated assets, rendering them into a static HTML website.
4.  **RAG Chatbot (Future)**: A future RAG chatbot will ingest the structured Markdown and metadata (potentially via Docusaurus's search index or custom API) for question-answering capabilities.
