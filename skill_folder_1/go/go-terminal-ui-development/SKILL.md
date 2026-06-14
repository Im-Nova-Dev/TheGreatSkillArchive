---
name: "go-terminal-ui-development"
description: "Teach terminal UI in Go using the Charm ecosystem: Bubble Tea, Bubbles, Lipgloss, Huh, and related libraries."
tags: ["go", "tui", "bubble-tea", "bubbles", "lipgloss", "huh", "charm"]
related_skills: ["go-cli-ux-and-accessibility", "go-building-clis-for-internal-tools"]
---

# Go Terminal UI Development

Teach terminal UI in Go using the Charm ecosystem: Bubble Tea, Bubbles, Lipgloss, Huh, and related libraries.

## Core Concepts

### The Charm Ecosystem
- **Bubble Tea** (`github.com/charmbracelet/bubbletea`) — Elm-inspired TUI framework. Models implement `Init()`, `Update(msg)`, `View() string`. Commands (`tea.Cmd`) handle async work.
- **Bubbles** (`github.com/charmbracelet/bubbles`) — Pre-built components: `list`, `table`, `viewport`, `progress`, `spinner`, `textarea`, `textinput`, `help`, `key`, `filepicker`, `timer`, `checkbox`, `radio`.
- **Lipgloss** (`github.com/charmbracelet/lipgloss`) — CSS-like styling: colors, borders, padding, margins, flexbox-like layouts via `JoinHorizontal`, `JoinVertical`, `Place`.
- **Huh** (`github.com/charmbracelet/huh`) — Declarative forms: `Input`, `Text`, `Select`, `MultiSelect`, `Confirm`, `Slider`, with built-in validation and themes.
- **Wish** (`github.com/charmbracelet/wish`) — SSH/TUI server for hosting Bubble Tea apps over SSH.
- **Glamour** (`github.com/charmbracelet/glamour`) — Markdown rendering in terminals.
- **Log** (`github.com/charmbracelet/log`) — Structured, pretty logging.

### Architecture Patterns
- **Model-View-Update**: Each page is a `tea.Model`. Compose via map of `PageID -> tea.Model`.
- **Sidebar navigation**: Persistent `SidebarModel` + content area switched by keypress (1-9,0).
- **Shared styles package**: Centralized Catppuccin Mocha colors + Lipgloss styles for consistency.
- **Responsive layout**: `WindowSizeMsg` triggers `SetSize(w, h)` on all pages.
- **Interface for pages**: Use `interface{ Init() tea.Cmd; Update(tea.Msg) (tea.Model, tea.Cmd); View() string; SetSize(int, int) }` for type-safe page registry.

## Procedure

### 1. Initialize Module
```go
module github.com/your-app
go 1.23.0
require (
    github.com/charmbracelet/bubbletea v1.3.6
    github.com/charmbracelet/bubbles v0.21.1
    github.com/charmbracelet/lipgloss v1.1.0
    github.com/charmbracelet/huh v1.0.0
    github.com/charmbracelet/log v1.0.0
)
```
**Note**: Use non-v2 imports (no `/v2` suffix) for current versions as of 2024+.

### 2. Create Styles Package
Define Catppuccin Mocha palette as constants, then build Lipgloss styles for: containers, sidebar, titles, buttons, inputs, lists, tables, progress bars, help, status indicators, code blocks, dialogs, tabs, tree/viewport.

### 3. Build Reusable Components
- `SidebarModel` — navigation with `list`/`viewport`, keybindings via `bubbles/key`, help via `bubbles/help`
- `ComponentShowcaseModel` — gallery using `bubbles/list` + detail `viewport`
- `ProgressModel` — multiple progress bars + 10 spinner styles
- `FormModel` — Huh forms with validation, groups, themes
- `DataDisplayModel` — `bubbles/table` + `textinput` filters
- `TextModel` — `bubbles/textarea` with line numbers, live preview
- `LayoutModel` — `JoinHorizontal`, `JoinVertical`, `Place`, Flex, Grid demos
- `NotificationModel` — toasts (auto-dismiss), status bar, dialogs
- `AnimationModel` — tick-based physics, particles, waves, HSV color cycling
- `MouseModel` — click, drag, hover, canvas drawing

### 4. Wire Main App
```go
p := tea.NewProgram(
    NewAppModel(),
    tea.WithAltScreen(),
    tea.WithMouseCellMotion(),
    tea.WithReportFocus(),
)
```

## Common Pitfalls

### Import Version Mismatch
**Problem**: `github.com/charmbracelet/bubbles/v2` not found (unknown revision)
**Fix**: Use non-v2 imports (`github.com/charmbracelet/bubbles`). The v2 module path was never published.

### Lipgloss API Changes
- `lipgloss.Height(h)` / `lipgloss.MaxHeight(h)` → use `lipgloss.NewStyle().Height(h)` / `.MaxHeight(h)`
- `VerticalAlign` not on `Style` → use `lipgloss.NewStyle().Align(lipgloss.Center)` for horizontal, vertical centering via `Place`
- `lipgloss.Value` type removed → don't use helper functions returning it

### Bubbles Component API
- `progress.WithFill`/`WithEmpty` → use `WithFilledChar`/`WithEmptyChar` (or omit for defaults)
- `progress.ShowPercentage` → use `WithoutPercentage`
- `textarea.LineNumberStyle`, `CursorStyle`, `FocusedStyle`, `BlurStyle` → use `ShowLineNumbers`, `Cursor.Style`, `FocusedStyle.Base`, `BlurredStyle.Base`
- `table.Rows().Len()` → `len(table.Rows())` (returns `[]Row`)
- `huh.ValidateEmail` → custom validation: `func(s string) error { if !strings.Contains(s, "@") { return errors.New("invalid") }; return nil }`
- `huh.NewSlider` → not in v1; use `Input` with numeric validation
- `form.GetStringSlice` → use `GetString` and parse

### Huh Form Update Returns Two Values
```go
updatedForm, formCmd := m.form.Update(msg)
m.form = updatedForm.(*huh.Form)
```

### MouseMsg Time Field
`tea.MouseMsg` has no `Time` field. Use `time.Now()` for timestamps.

### Interface Satisfaction
Page structs with pointer-receiver `SetSize` don't satisfy value-receiver interface. Use `interface{ SetSize(int, int) }` with type assertions, or define `PageModel` interface with pointer receivers consistently.

### ⚠️ Critical: Update() Must Use Pointer Receiver
**Problem**: `func (m Model) Update(msg tea.Msg)` (value receiver) causes the model to be copied on each update. The program runs but `View()` returns "Loading..." forever because `width`/`height` stay 0 on the original struct. The `tea.Program` holds a pointer to your model; value-receiver `Update` modifies a copy.

**Fix**: Always use pointer receiver:
```go
func (m *AppModel) Update(msg tea.Msg) (tea.Model, tea.Cmd) { ... }
```
And pass pointer to `tea.NewProgram`:
```go
model := NewAppModel()
p := tea.NewProgram(&model, ...)  // note the &
```

**Symptoms**: Build succeeds, runs without panics, but terminal shows only "Loading..." (or empty) and never renders the UI. Mouse/key events seem ignored. `WindowSizeMsg` processed but dimensions don't persist.

## References
- Charm docs: https://github.com/charmbracelet/
- Bubble Tea tutorial: https://github.com/charmbracelet/bubbletea#tutorial
- Bubbles component list: https://github.com/charmbracelet/bubbles
- Lipgloss guide: https://github.com/charmbracelet/lipgloss
- Huh forms: https://github.com/charmbracelet/huh
- Catppuccin palette: https://github.com/catppuccin/catppuccin
- Showcase reference implementation: `/home/nova/charm-tui-showcase` (12-page demo app)