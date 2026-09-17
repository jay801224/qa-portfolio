# QA Test Plan – <PRODUCT> Sic Bo Project

## Objective

This QA Test Plan covers multiple React-based projects involving both game features and supporting UI components. These include full game integrations (Baccarat, Jackpot, Micard with card squeeze), multi-table functionality, lobby access, and core UI infrastructure. The objective is to:

- Seamlessly integrate the respective React modules into the platform, ensuring full functionality of game mechanics, video streaming (where applicable), and UI responsiveness
- Deliver consistent, accurate, and smooth experiences across all supported features and platforms
- Ensure backward compatibility and stability for Business As Usual (BAU) features
- Maintain performance, visual consistency, and platform alignment
- Provide support for multi-currency, multi-language, and multi-platform operations

## Testing Schedule

TBC (To Be Confirmed)

## Testing Coverage

### Game Integration / Game Flow Testing

- Validate correct launch and entry into the <PRODUCT> Sic Bo game
- Ensure betting logic, payout, and result evaluation align with Sic Bo game rules
- Verify availability and accuracy of bet types: Big/Small, Odd/Even, Double, Triple, Two Dice Combo, One/Two/Three Dice bets
- Validate payout calculations and odds consistency including multiplier features, per functional spec
- Ensure direct bet features (Undo, x2, Repeat) work as intended, aligned with React BAC behavior
- Confirm bet details panel displays winning bet types and payout multipliers per round, wraps content when too long
- Ensure UI supports heat/cold indicators and trend line views for roadmaps; behavior differs on PC vs MB
- Confirm all 21 supported currencies display correct 6-chip presets (excluding IDR2/VND2)

### Game Access Verification

- Ensure Lobby supports entry to BAC, DT, ROU, SHB games
- Confirm correct routing, parameter passing (e.g. table ID, language), and fallback handling

### Video Streaming Testing

- Validate video resolution, latency, and loading stability
- Ensure audio is synchronized with video and gameplay
- Confirm compatibility across device types and network conditions
- Verify streaming continuity on reconnect or screen resize

### Data Binding & State Management Testing

- Validate rendering of dynamic content based on user actions
- Ensure consistent state updates via context/store/hooks
- Confirm sync between local and global UI states

### Account

- Multi-currency support (e.g., CNY, KRW, MYR, USD; among 21+ supported currencies)
- Single wallet functionality validation
- Transaction processing and record validation

### Cross-Platform Compatibility

- Desktop (PC/Mac)
- Mobile (iOS/Android)
- Different screen resolutions and orientations

### Browser Compatibility Testing

- Chrome
- Microsoft Edge
- Safari
- Other mobile browsers (e.g., Chrome, QQ, UC Browser)

### UI/UX Verification

- Game interface consistency (for game projects)
- Component rendering and interaction (for UI-focused modules)
- UI alignment, colors, spacing, and typography standards
- Multi-language support (11 languages including English, Simplified Chinese, Traditional Chinese, Burmese, Indonesian, Japanese, Khmer, Korean, Portuguese, Thai, Vietnamese)

### Performance & Load Testing

- Animation and transition smoothness (e.g., Micard squeeze, Dialog opening)
- System responsiveness under normal and high concurrency
- Simultaneous UI interaction, game states, or live content rendering

### Back Office Testing (if applicable)

- Validate bet records, game logs, and transaction reporting accuracy
- Confirm record synchronization with back-office tools or admin panels
- Ensure compatibility of reporting data format and filter functions

### Regression Testing

- Ensure BAU features remain stable after each integration
- Ensure Gift and Jackpot modules are not triggered or exposed in <PRODUCT> Sic Bo, as they are not supported
- Ensure platform-level modules (e.g., Notification, Roadmap service) remain unaffected

## Testing Environment

- **QA Environment** for component- and game-level testing
- **UAT Environment** for flow, integration, and animation verification

## Testing Resources

- **QA Team**: Responsible for core functional, regression, and compatibility testing
- **Other Teams**:
  - UI/UX testing (front-end, design consistency)
  - Language testing (non-primary languages)
  - Browser compatibility validation
  - Performance testing
