---
name: Performance Intelligence System
colors:
  surface: '#f8f9ff'
  surface-dim: '#cbdbf5'
  surface-bright: '#f8f9ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#eff4ff'
  surface-container: '#e5eeff'
  surface-container-high: '#dce9ff'
  surface-container-highest: '#d3e4fe'
  on-surface: '#0b1c30'
  on-surface-variant: '#434655'
  inverse-surface: '#213145'
  inverse-on-surface: '#eaf1ff'
  outline: '#737686'
  outline-variant: '#c3c6d7'
  surface-tint: '#0053db'
  primary: '#004ac6'
  on-primary: '#ffffff'
  primary-container: '#2563eb'
  on-primary-container: '#eeefff'
  inverse-primary: '#b4c5ff'
  secondary: '#712ae2'
  on-secondary: '#ffffff'
  secondary-container: '#8a4cfc'
  on-secondary-container: '#fffbff'
  tertiary: '#006242'
  on-tertiary: '#ffffff'
  tertiary-container: '#007d55'
  on-tertiary-container: '#bdffdb'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#dbe1ff'
  primary-fixed-dim: '#b4c5ff'
  on-primary-fixed: '#00174b'
  on-primary-fixed-variant: '#003ea8'
  secondary-fixed: '#eaddff'
  secondary-fixed-dim: '#d2bbff'
  on-secondary-fixed: '#25005a'
  on-secondary-fixed-variant: '#5a00c6'
  tertiary-fixed: '#6ffbbe'
  tertiary-fixed-dim: '#4edea3'
  on-tertiary-fixed: '#002113'
  on-tertiary-fixed-variant: '#005236'
  background: '#f8f9ff'
  on-background: '#0b1c30'
  surface-variant: '#d3e4fe'
typography:
  display-lg:
    fontFamily: Inter
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
    letterSpacing: -0.01em
  headline-lg-mobile:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  title-md:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  label-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
    letterSpacing: 0.05em
  mono-data:
    fontFamily: JetBrains Mono
    fontSize: 14px
    fontWeight: '500'
    lineHeight: 20px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 8px
  container-padding: 24px
  gutter: 16px
  viz-gap: 32px
  stack-sm: 4px
  stack-md: 12px
---

## Brand & Style

The design system focuses on a high-performance SaaS aesthetic tailored for educational growth tracking and data-driven insights. The brand personality is **analytical, encouraging, and sophisticated**, designed to transform complex academic data into actionable progress narratives.

The design style is **Corporate Modern with subtle Glassmorphism**, utilizing high-clarity interfaces that prioritize information density without sacrificing breathing room. It leverages a "Clean Precision" approach: using light-weight borders, strategic whitespace, and a layered surface architecture to guide the user's eye through intricate performance metrics and heatmap distributions.

## Colors

The palette is engineered for data visualization and growth tracking. 

- **Primary (Blue):** Used for core navigation, primary actions, and "Standard" performance metrics.
- **Secondary (Purple):** Reserved for "Aspiration" metrics, specialized growth insights, and trend lines.
- **Tertiary (Green):** Indicates "Mastery" and positive growth velocity.
- **Heatmap Scales:** A 7-step monochromatic progression from Slate-50 to Sky-800 provides clear density mapping for student activity and question difficulty distributions.
- **Neutral:** A sophisticated Slate-based grayscale ensures that UI chrome remains unobtrusive, allowing colorful data points to remain the focal point.

## Typography

This design system utilizes **Inter** for its exceptional legibility in data-heavy environments. 

- **Numerical Data:** For tabular data and growth percentages, use `mono-data` (JetBrains Mono) to ensure vertical alignment of digits.
- **Hierarchy:** Use tight letter-spacing on larger headlines to maintain a premium, "tucked" look. 
- **Labels:** All caps are reserved for small labels (category headers in sidebars or axis titles) to provide a distinct visual anchor.
- **Scalability:** Display sizes should downscale by roughly 25% on mobile devices to prevent excessive wrapping in data dashboards.

## Layout & Spacing

The layout follows a **12-column fluid grid** for desktop, collapsing to a single column on mobile. 

- **Rhythm:** An 8px base unit (the "soft grid") governs all padding and margins. 
- **Dashboard Layout:** Data visualizations (Radar charts, Heatmaps) should be housed in containers with at least `viz-gap` (32px) of separation to prevent visual cognitive load.
- **Density:** Use `stack-sm` for related text elements (title + subtitle) and `stack-md` for separating distinct logical blocks within a card.

## Elevation & Depth

Visual hierarchy is achieved through **Tonal Layering** and **Subtle Outlines**. 

- **Level 0 (Background):** A soft neutral (Slate-50) creates a canvas.
- **Level 1 (Cards):** Pure white background with a 1px border (#E2E8F0). No shadow is used here to maintain a crisp, flat SaaS look.
- **Level 2 (Active States/Modals):** Use a 12% opacity shadow with a 16px blur, tinted with the Primary color (#2563EB) to create a sense of "lift" without looking heavy.
- **Glassmorphism:** For overlays or sidebar navigation on scroll, apply a `blur(12px)` with a semi-transparent white fill (`rgba(255,255,255,0.8)`).

## Shapes

The design system adheres to a consistent **8px (0.5rem)** radius for standard UI elements.

- **Standard Elements:** Buttons, Input fields, and Cards use the 8px radius.
- **Large Components:** Hero sections or large dashboard containers use `rounded-lg` (16px).
- **Interactive Triggers:** Smaller elements like Tooltips or Tags use `rounded-sm` (4px) to maintain sharpness at small scales.
- **Radar Charts:** Data points within charts should be rendered as 6px circular nodes.

## Components

### Data Visualization
- **Radar Charts:** Grid lines should be Slate-200 with a 0.5px stroke. The "Area" fill should use Primary or Secondary colors at 15% opacity with a 2px solid stroke.
- **Heatmaps:** Cells must have a 2px white gap between them. Use the `heatmap_intensity` scale. Tooltips on hover must show the exact value and date.
- **Growth Indicators:** Use "Pill" shapes with an icon (arrow up/down) + percentage. Positive growth uses Tertiary (Green), negative uses a muted Red-500.

### Input & Controls
- **Input Fields:** 8px rounded corners, Slate-300 border. On focus, the border transitions to Primary Blue with a 3px soft outer glow.
- **Buttons:** Primary buttons are solid Blue. Secondary buttons are ghost-style (Slate-600 text, no fill) with an 8px radius.

### Feedback & Progress
- **Progress Bars:** Dual-tone bars. The background track is Slate-100. The active track uses a gradient from Primary to Secondary to indicate "High Velocity" growth.
- **Chips:** Small, 4px rounded labels used for tagging question categories (e.g., "Math", "Difficult").