---
name: Ngân Hàng Đề
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
  on-surface-variant: '#424656'
  inverse-surface: '#213145'
  inverse-on-surface: '#eaf1ff'
  outline: '#727687'
  outline-variant: '#c2c6d8'
  surface-tint: '#0054d6'
  primary: '#0050cb'
  on-primary: '#ffffff'
  primary-container: '#0066ff'
  on-primary-container: '#f8f7ff'
  inverse-primary: '#b3c5ff'
  secondary: '#585f6a'
  on-secondary: '#ffffff'
  secondary-container: '#dce3f0'
  on-secondary-container: '#5e6570'
  tertiary: '#006645'
  on-tertiary: '#ffffff'
  tertiary-container: '#008259'
  on-tertiary-container: '#e1ffec'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#dae1ff'
  primary-fixed-dim: '#b3c5ff'
  on-primary-fixed: '#001849'
  on-primary-fixed-variant: '#003fa4'
  secondary-fixed: '#dce3f0'
  secondary-fixed-dim: '#c0c7d3'
  on-secondary-fixed: '#151c25'
  on-secondary-fixed-variant: '#404751'
  tertiary-fixed: '#6ffbbe'
  tertiary-fixed-dim: '#4edea3'
  on-tertiary-fixed: '#002113'
  on-tertiary-fixed-variant: '#005236'
  background: '#f8f9ff'
  on-background: '#0b1c30'
  surface-variant: '#d3e4fe'
typography:
  display:
    fontFamily: Inter
    fontSize: 48px
    fontWeight: '700'
    lineHeight: '1.2'
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '700'
    lineHeight: '1.3'
    letterSpacing: -0.01em
  headline-lg-mobile:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '700'
    lineHeight: '1.3'
  headline-md:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: '1.4'
  headline-sm:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: '600'
    lineHeight: '1.4'
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.6'
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.6'
  label-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '500'
    lineHeight: '1.4'
    letterSpacing: 0.01em
  label-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: '1.2'
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  unit: 4px
  container-max: 1280px
  gutter: 24px
  margin-mobile: 16px
  margin-desktop: 40px
  stack-sm: 8px
  stack-md: 16px
  stack-lg: 32px
---

## Brand & Style

The design system is engineered for an AI-powered mathematics ecosystem that balances academic rigor with an effortless user experience. The brand personality is **Intelligent, Trustworthy, and Approachable**, blending the precision of a high-tech tool with the friendliness of a personal tutor.

The aesthetic direction is a synthesis of three distinct influences:
- **Apple-inspired Precision:** High-quality finish, subtle gradients, and rhythmic white space.
- **Notion-inspired Utility:** Systematic layout, functional clarity, and a focus on content hierarchy.
- **Duolingo-inspired Engagement:** Friendly geometry and soft, tactile interactions that reduce the "math anxiety" often felt by students.

The resulting style is **Modern Premium Minimalism**, characterized by expansive layouts, high-legibility Vietnamese typography, and a "soft-tech" feel that invites exploration rather than intimidation.

## Colors

The color strategy uses a logic of **Cognitive Clarity**. Primary Blue represents the "AI Intelligence" and trust, while the Secondary Blue acts as a gentle canvas for interactive zones.

- **Primary Blue (#0066FF):** Used for primary actions, progress indicators, and brand-defining moments.
- **Secondary Blue (#EBF2FF):** Applied to large surface areas like active card backgrounds and subtle highlights to keep the UI light.
- **Success Green (#10B981):** A tertiary color reserved specifically for correct answers and completed milestones, providing positive reinforcement.
- **Neutrals:** A palette of soft grays (from #F8FAFC to #1E293B) is used to differentiate content layers and provide a high-contrast environment for mathematical notation.

Avoid pure black (#000000); use deep navy-grays for text to maintain a premium, softer reading experience.

## Typography

The design system utilizes **Inter** for its exceptional legibility in Vietnamese, especially for complex mathematical symbols and scientific notation. 

The typographic hierarchy is intentionally generous. Headlines use tighter letter-spacing and heavier weights to feel "authoritative," while body text uses a line height of 1.6 to ensure that multi-line equations and complex explanations are readable without visual crowding. For mathematical formulas (LaTeX), the system should fall back to a compatible serif or specialized math font, but all UI labeling must remain in Inter.

## Layout & Spacing

The layout follows a **Fluid Grid** model with high-integrity "Safe Zones." 

- **Desktop:** 12-column grid with 24px gutters. Content is centered within a 1280px max-width container to prevent line-lengths from becoming excessive.
- **Mobile:** Single column with 16px side margins. 
- **Rhythm:** A 4px baseline grid governs all spacing. 

Whitespace is used as a functional tool to separate "Problem Statements" from "Solutions." Use large vertical gaps (stack-lg) between distinct learning modules to prevent cognitive overload.

## Elevation & Depth

This design system employs a **Tonal Layering** approach combined with **Ambient Shadows**. Depth is used to signify interactivity and importance.

1.  **Level 0 (Background):** Solid #FFFFFF or #F8FAFC. 
2.  **Level 1 (Cards):** White background with a 1px border in #E2E8F0. This is the standard for lesson cards.
3.  **Level 2 (Interactive Elements):** Cards that respond to hover/touch use a soft, diffused shadow: `0px 10px 25px -5px rgba(0, 102, 255, 0.08)`.
4.  **Level 3 (Modals/Popovers):** Higher elevation with a more pronounced shadow and a subtle backdrop blur (glassmorphism) to keep the user focused on the immediate task.

Depth should feel "physical" but light, as if elements are made of soft matte paper.

## Shapes

The shape language is defined by **High-Radius Geometry**. This reduces the "sharpness" associated with difficult academic subjects.

- **Standard Elements (Inputs, Buttons):** 16px corner radius.
- **Feature Cards (Lesson blocks, Progress panels):** 24px corner radius.
- **Small Elements (Tags, Tooltips):** 8px corner radius.

This generous rounding creates a friendly, "friendly-tech" aesthetic that aligns with the Duolingo influence while maintaining the professional polish of Apple's interface guidelines.

## Components

### Buttons
- **Primary:** Solid #0066FF with white text. 16px radius. Subtle scale-down effect on press (98%).
- **Secondary:** Solid #EBF2FF with #0066FF text. No border.
- **Ghost:** Transparent background with Primary Blue text, used for less critical actions.

### Cards
Cards are the primary container for exam questions. They must feature 24px internal padding. Title text is always Headline-SM. For AI-generated content, use a subtle 1px Primary Blue border to differentiate it from standard content.

### Inputs & Math Fields
Input fields use a 16px radius and a #F1F5F9 background. On focus, the border transitions to Primary Blue with a 3px soft outer glow (Secondary Blue).

### Progress Indicators
Progress bars use a thick 12px height with fully rounded caps. The track is #EBF2FF and the indicator is a gradient of Primary Blue.

### Chips/Tags
Used for "Topic Tags" (e.g., Hình học, Đại số). Small 8px radius, #F1F5F9 background, and Label-SM typography.