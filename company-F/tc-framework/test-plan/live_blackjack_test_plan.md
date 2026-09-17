QA Test Plan – <PRODUCT> (Live Blackjack 21)

Objective:
This QA Test Plan covers the React-based <PRODUCT> (Live Blackjack 21) game integration. The objective is to:
Seamlessly integrate the <PRODUCT> module into the platform, ensuring full functionality of game mechanics, video streaming, and UI responsiveness
Deliver consistent, accurate, and smooth experiences across all supported features and platforms
Ensure backward compatibility and stability for Business As Usual (BAU) features
Maintain performance, visual consistency, and platform alignment
Provide support for multi-currency, multi-language, and multi-platform operations

Source Spec:
Axure: https://example.internal (<PRODUCT>, 39 pages, 7 chapters)

Testing Schedule:
TBC (To Be Confirmed)

Testing Coverage:

Game Integration / Game Flow Testing
- Validate correct launch and entry into the <PRODUCT> game from Lobby
- Ensure betting logic, payout, and result evaluation align with Blackjack rules (Game Rules / Settle Flow / Suffering Flow per Axure §1.2)
- Verify Main Bet behavior: Blackjack 3:2 (incl. 6-card Charlie), Win 1:1, Insurance 2:1
- Verify Side Bet availability and payout: HOT3, 21+3, Perfect Pairs, Bust Bonus, Cash Out
- Validate RTP per spec: Main <per spec> / HOT3 <per spec> / 21+3 <per spec> / Perfect Pairs <per spec> / Bust Bonus <per spec> / Cash Out <per spec>
- Validate table limit enforcement: <per spec> per Axure spec
- Ensure player decision actions work correctly: Hit, Stand, Double Down, Split, Surrender, Insurance
- Confirm direct bet features (Undo, x2, Repeat) behavior aligned with React BAC pattern
- Confirm bet details panel displays winning bet types and payout multipliers per round
- Ensure UI supports roadmap and trend views per Axure §3.2 (簡易路紙) / §3.3 (歷史紀錄); behavior differs on PC vs MB
- Confirm all 21 supported currencies display correct 6-chip presets (excluding IDR2/VND2)

Game Access Verification
- Ensure Lobby supports entry to BJ alongside existing BAC/DT/ROU/SHB games
- Confirm correct routing, parameter passing (e.g. table ID, language), and fallback handling
- Validate table card behavior on Lobby per Axure §2.1.2 (桌卡)

Video Streaming Testing
- Validate video resolution, latency, and loading stability
- Ensure audio sync with video and gameplay (dealing, reveal, settle audio cues)
- Confirm compatibility across device types and network conditions
- Verify streaming continuity on reconnect or screen resize

Data Binding & State Management Testing
- Validate rendering of dynamic content based on user actions (bet placement, decision, side bet activation)
- Ensure consistent state updates via context/store/hooks across betting → dealing → settle → payout phases
- Confirm sync between local and global UI states (chip stack, balance, side bet status)

Account
- Multi-currency support (CNY, KRW, MYR, USD; among 21+ supported currencies)
- Single wallet functionality validation
- Transaction processing and record validation (main bet + each side bet recorded separately)

Cross-Platform Compatibility
- Desktop (PC/Mac)
- Mobile (iOS/Android)
- Different screen resolutions and orientations (per Axure §2.2.1 尺寸版面規則)

Browser Compatibility Testing
- Chrome
- Microsoft Edge
- Safari
- Other mobile browsers (e.g., Chrome, QQ, UC Browser)

UI/UX Verification
- Game interface consistency (Core UI per Axure §2.1.1)
- Component rendering and interaction (chip placement, side bet zones, decision buttons)
- UI alignment, colors, spacing, and typography standards
- Multi-language support (11 languages including English, Simplified Chinese, Traditional Chinese, Burmese, Indonesian, Japanese, Khmer, Korean, Portuguese, Thai, Vietnamese)

Performance & Load Testing
- Animation and transition smoothness (card dealing, chip placement, dialog opening)
- System responsiveness under normal and high concurrency
- Simultaneous UI interaction, game states, or live content rendering

Back Office Testing
- Validate bet records, game logs, and transaction reporting accuracy
- Confirm record synchronization with back-office tools per Axure §4.1 (後台) / §4.3 (operational tool)
- Ensure dealer-end operations align with Axure §4.2 (荷官端)
- Ensure compatibility of reporting data format and filter functions

Admin Console Operations
- Agent → Common Pankou Table-Limit Setting: after modification, frontend table display reflects the new limit immediately
- Agent → Common Pankou Table-Limit Setting: chip presets and bet min/max enforcement on frontend follow the updated values
- Member → Bet Records: every frontend bet (main bet + each side bet) generates a corresponding record in admin with matching amount, bet type, and timestamp
- Admin config changes propagate without requiring game restart or table reopen (live sync)

Dealer ⇄ Frontend ⇄ Admin Result Consistency
- Dealer Tool manual deal: dealer-side card values = player-frontend displayed cards = admin-side settlement record
- Dealer Tool auto deal: auto-deal logic outcome consistent across all three views
- Post-settlement payout amount, bet record, and member balance aligned across all three views
- Abnormal scenarios (disconnect / reconnect / void round) maintain consistent state across all three views

Regression Testing
- Ensure BAU features remain stable after <PRODUCT> integration
- Ensure Gift and Jackpot modules are not triggered or exposed in <PRODUCT>, as they are not supported
- Ensure platform-level modules (e.g., Notification, Roadmap service) remain unaffected
- Verify arbitrage and risk-control defenses per Axure §6.1 (套利與模型與風控防禦報告)

Testing Environment:
QA Environment for component- and game-level testing
UAT Environment for flow, integration, and animation verification

Testing Resources:
QA Team: Responsible for core functional, regression, and compatibility testing
Other Teams:
UI/UX testing (front-end, design consistency)
Language testing (non-primary languages)
Browser compatibility validation
Performance testing
