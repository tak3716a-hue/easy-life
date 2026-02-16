# CLAUDE.md

## Project Overview

**Easy Life** ("사랑이 넘치는 가족") is a Korean-language family portal web application built with vanilla HTML, CSS, and JavaScript. It provides family-oriented tools and information pages including a lotto number generator, CME futures trading dashboard, financial knowledge links, a contact form, and placeholder pages for family content.

No build step, no frameworks, no npm dependencies. All pages are static HTML served directly.

## Repository Structure

```
/
├── index.html                      # Main landing page with category navigation
├── main.js                         # Shared JS utilities (dark mode, basic lotto)
├── style.css                       # Legacy stylesheet (mostly unused by current pages)
├── blueprint.md                    # Original project blueprint
├── pages/                          # All sub-pages
│   ├── lotto.html                  # Premium lotto number generator (full)
│   ├── trading-dashboard.html      # CME futures trading dashboard (full)
│   ├── finance.html                # Financial knowledge & tool links (full)
│   ├── contact.html                # Formspree-powered contact form (full)
│   ├── family-intro.html           # Family introduction (placeholder)
│   ├── album.html                  # Photo album (placeholder)
│   ├── recipe.html                 # Cooking recipes (placeholder)
│   ├── schedule.html               # Family schedule (placeholder)
│   └── notice.html                 # Announcements (placeholder)
├── .idx/
│   ├── dev.nix                     # Nix dev environment (Node 20, Python 3)
│   └── mcp.json                    # Firebase MCP server config
└── .vscode/
    └── settings.json               # VS Code / IDX settings
```

## Technology Stack

- **Languages:** HTML5, CSS3, JavaScript (ES6+)
- **Frameworks:** None (vanilla web stack)
- **Fonts:** Google Fonts — Orbitron (display), Noto Sans KR (body/Korean)
- **Form backend:** Formspree (`https://formspree.io/f/xqelbzgg`)
- **Dev server:** Python 3 `http.server` (configured in `.idx/dev.nix`)
- **Runtime:** Node.js 20 and Python 3 available in dev environment

## Development Workflow

### Running Locally

```bash
python3 -m http.server 8080 --bind 0.0.0.0
```

Then open `http://localhost:8080` in a browser. No build or install step required.

### No Build System

This is a purely static site. There is:
- No `package.json` or npm dependencies
- No bundler (webpack, vite, etc.)
- No transpilation or compilation step
- No test framework or test files
- No linter or formatter configured

### Git Workflow

- **Main branch:** `master`
- Pages are deployed as static files — changes take effect immediately upon serving
- Commit history follows a pattern of feature-based commits (e.g., "Add CME futures trading dashboard")

## Architecture & Key Patterns

### Page Structure

Each page is **self-contained** — all CSS and JavaScript are inline within the HTML file. There are no shared CSS or JS imports between pages (except `main.js` which is only used by `index.html` and the legacy flow).

Navigation is file-based: `index.html` links to `pages/*.html`, and each sub-page has a back button ("← 홈으로") linking to `../index.html`.

### CSS Design System

All pages use a consistent set of CSS custom properties:

```css
:root {
  --primary: #FFD700;        /* Gold — accent */
  --secondary: #1a1a2e;      /* Dark navy — background */
  --accent: #16213e;         /* Darker navy */
  --highlight: #0f3460;      /* Navy accent */
  --success: #00ff88;        /* Bright green */
  --family: #ff6b9d;         /* Pink — family section */
  --life: #4ecdc4;           /* Cyan — lifestyle section */
  --etc: #a29bfe;            /* Purple — misc section */
  --glow: rgba(255, 215, 0, 0.3); /* Gold glow */
}
```

Visual effects include glassmorphism (`backdrop-filter: blur`), gradient text, CSS animations (`fadeInDown`, `fadeInUp`, `slideIn`, `ballPop`, `gradientShift`), and hover transforms with `0.3s ease` transitions.

### Naming Conventions

| Element | Convention | Examples |
|---------|-----------|----------|
| CSS classes | kebab-case | `.back-btn`, `.card-grid`, `.main-panel` |
| HTML IDs | camelCase | `#setCount`, `#algorithm`, `#darkModeToggle` |
| JS functions | camelCase | `generateNumbers()`, `ensureOddEvenBalance()` |
| JS variables | camelCase | `totalGenerated`, `numberFrequency` |

### State Management

Client-side state is stored in `localStorage` with JSON serialization. Key patterns:
- `totalGenerated` / `todayGenerated` — lotto generation statistics
- `numberFrequency` — frequency map of generated numbers
- `lastDate` — daily reset tracking via date comparison

### Responsive Design

Pages use mobile-first CSS with grid layouts:
```css
grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
```
Media queries target tablets at `max-width: 768px`.

## Conventions for AI Assistants

### When Adding New Pages

1. Create a new HTML file in `pages/`
2. Include all CSS and JS inline within the file (self-contained pattern)
3. Use the same CSS custom properties for consistent theming
4. Add a back button linking to `../index.html` at the top
5. Add a navigation card for the new page in `index.html` under the appropriate category section ("우리가족 모여라", "슬기로운 생활", or "기타")
6. Follow the existing visual style: dark background, glassmorphism cards, gold accents

### When Modifying Existing Pages

- Each page's styles/scripts are inline — edit the specific HTML file directly
- Do not extract inline styles/scripts into external files unless explicitly requested
- Preserve the Korean-language interface
- Maintain responsive behavior and animation patterns

### External Services

- **Formspree** is used for the contact form — do not change the endpoint without user consent
- **Google Fonts** are loaded via CDN — Orbitron and Noto Sans KR must remain available
- **Firebase** is configured in `.idx/mcp.json` but not actively used in current code

### Things to Avoid

- Do not introduce npm dependencies or a build system unless explicitly requested
- Do not add English-only UI text — the interface is Korean-first
- Do not remove placeholder pages — they represent planned features
- Do not modify `.idx/` configuration without explicit request
