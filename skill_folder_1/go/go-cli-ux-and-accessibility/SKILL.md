---
name: "go-cli-ux-and-accessibility"
description: "Teach CLI/TUI UX in Go: help text, completion, progress bars, color support, interactive prompts, terminal width handling, keyboard navigation, and accessibility."
tags: ["go", "cli", "tui", "ux", "accessibility", "bubbles", "lipgloss", "huh"]
related_skills: ["go-terminal-ui-development", "go-building-clis-for-internal-tools"]
---

# Go CLI/TUI UX and Accessibility

Teach CLI/TUI UX in Go using the Charm ecosystem: help text, completion, progress bars, color support, interactive prompts, terminal width handling, keyboard navigation, and accessibility.

## Core Concepts

### Help Systems
- **bubbles/help** — Context-aware keybinding display. `help.Model` with `ShortHelp()`/`FullHelp()` on keymaps. Styles via `Styles.ShortKey`, `ShortDesc`, `FullKey`, `FullDesc`.
- **Pattern**: Embed `help.Model` in each page/model. Show/hide with `?` key. Auto-generates from `KeyMap` bindings.

### Progress Indicators
- **bubbles/progress** — `progress.Model` with `SetPercent(float64)`, `View() string`. Styles: `WithDefaultGradient()`, `WithScaledGradient()`, `WithWidth()`, `WithoutPercentage()`, `WithFilledChar()`, `WithEmptyChar()`, `WithGradient()`.
- **bubbles/spinner** — 10+ built-in: `Dot`, `Line`, `MiniDot`, `Jump`, `Pulse`, `Points`, `Globe`, `Moon`, `Meter`, `Hamburger`. `spinner.New(spinner.WithSpinner(spinner.Dot))`. Style with `.Style = lipgloss.NewStyle().Foreground(color)`.

### Color & Styling (Lipgloss)
- **Palette**: Define as constants (Catppuccin, Dracula, Nord, etc.). Use `lipgloss.Color("#hex")`.
- **Styles**: Compose with `NewStyle().Foreground().Background().Bold().Padding().Margin().Border().BorderForeground().Width().Height().Align()`.
- **Layout**: `JoinHorizontal(position, ...)`, `JoinVertical(position, ...)`, `Place(width, height, hPos, vPos, content)`.
- **Responsive**: `WindowSizeMsg` → recalculate widths, call `SetSize()` on components.

### Interactive Prompts (Huh)
- **Huh forms**: `huh.NewForm(groups...).WithTheme(huh.ThemeCharm()).WithWidth(60).WithShowHelp(true)`
- **Field types**: `Input`, `Text` (multi-line), `Select`, `MultiSelect`, `Confirm`, `Input` (numeric with validation)
- **Validation**: `Validate(func(s string) error)` on each field. Return `nil` for valid.
- **Groups**: `huh.NewGroup(fields...).Title("Section")` — organizes with visual separation.
- **Value binding**: Pass pointer to string/int/bool/slice. Form mutates directly.

### Keyboard Navigation
- **bubbles/key** — `key.NewBinding(key.WithKeys("up", "k"), key.WithHelp("↑/k", "move up"))`
- **KeyMap methods**: `ShortHelp() []key.Binding`, `FullHelp() [][]key.Binding` for help display.
- **Matching**: `key.Matches(msg, binding)` handles multiple keys per action.
- **Vim + Arrow**: Always bind both (`"up", "k"`).

### Terminal Width Handling
- **WindowSizeMsg**: `tea.WindowSizeMsg{Width, Height}` sent on resize.
- **Pattern**: Each component implements `SetSize(w, h)`. App distributes space (sidebar fixed, content flexible).
- **Viewport**: `viewport.Model` with `Width`, `Height`, `KeyMap = viewport.DefaultKeyMap()`.

### Accessibility
- **High contrast**: Catppuccin Mocha meets WCAG AA for text/background.
- **Focus indicators**: Bold, color change, border highlight on focused elements.
- **Keyboard-only**: All functionality reachable via keyboard (no mouse required).
- **Screen reader friendly**: Semantic structure, descriptive help text.
- **Reduced motion**: Respect `prefers-reduced-motion` — disable spinners/animations via flag.

## Procedure

### 1. Define Color Palette + Base Styles
```go
const (
    Base = "#1e1e2e"
    Text = "#cdd6f4"
    Blue = "#89b4fa"
    Green = "#a6e3a1"
    // ...
)

var (
    ContainerStyle = lipgloss.NewStyle().Background(lipgloss.Color(Base)).Foreground(lipgloss.Color(Text)).Padding(1, 2)
    ButtonStyle = lipgloss.NewStyle().Background(lipgloss.Color(Blue)).Foreground(lipgloss.Color(Crust)).Padding(0, 2).Bold(true).Border(lipgloss.RoundedBorder()).BorderForeground(lipgloss.Color(Blue))
    // ...
)
```

### 2. Build KeyMap with Help
```go
type KeyMap struct {
    Up key.Binding
    Down key.Binding
    Quit key.Binding
}

func DefaultKeyMap() KeyMap {
    return KeyMap{
        Up: key.NewBinding(key.WithKeys("up", "k"), key.WithHelp("↑/k", "move up")),
        Down: key.NewBinding(key.WithKeys("down", "j"), key.WithHelp("↓/j", "move down")),
        Quit: key.NewBinding(key.WithKeys("q", "ctrl+c"), key.WithHelp("q", "quit")),
    }
}
func (k KeyMap) ShortHelp() []key.Binding { return []key.Binding{k.Up, k.Down, k.Quit} }
func (k KeyMap) FullHelp() [][]key.Binding { return [][]key.Binding{{k.Up, k.Down}, {k.Quit}} }
```

### 3. Wire Help Model
```go
h := help.New()
h.ShowAll = false
h.Styles.ShortKey = styles.HelpKeyStyle
h.Styles.ShortDesc = styles.HelpDescStyle
// In View(): if m.showHelp { h.View(m.keys) }
```

### 4. Progress + Spinner
```go
bar := progress.New(progress.WithDefaultGradient())
spinner := spinner.New(spinner.WithSpinner(spinner.Dot))
spinner.Style = styles.InfoStyle
// Update: bar.SetPercent(p), spinner.Update(msg)
// View: bar.View(), spinner.View()
```

### 5. Huh Form with Validation
```go
form := huh.NewForm(
    huh.NewGroup(
        huh.NewInput().Title("Email").Value(&email).Validate(func(s string) error {
            if !strings.Contains(s, "@") { return errors.New("invalid email") }
            return nil
        }),
    ).Title("Contact"),
).WithTheme(huh.ThemeCharm()).WithWidth(60).WithShowHelp(true)
```

### 6. Handle Resize
```go
func (m *Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    switch msg := msg.(type) {
    case tea.WindowSizeMsg:
        m.width, m.height = msg.Width, msg.Height
        m.viewport.Width = msg.Width - 4
        m.viewport.Height = msg.Height - 4
    }
    return m, nil
}
```

## Common Pitfalls

### Help Not Showing
- Forgot `h.Styles.ShortKey/ShortDesc/FullKey/FullDesc` — defaults are invisible.
- `h.ShowAll = false` for short help, toggle to `true` for full.

### Progress Bar Not Animating
- Forgot to tick: `tea.Tick(interval, func(t time.Time) tea.Msg { return tickMsg(t) })`
- Forgot `SetPercent()` in tick handler.

### Huh Form Value Not Updating
- Pass pointer: `Value(&data.Field)` not `Value(data.Field)`.
- Form `Update` returns `(tea.Model, tea.Cmd)` — must type assert: `updatedForm, cmd := m.form.Update(msg); m.form = updatedForm.(*huh.Form)`.

### Colors Missing in Output
- Terminal doesn't support true color — check `TERM` env, use `lipgloss.DefaultRenderer()`.
- `NO_COLOR` env var set — lipgloss respects it.

### Keyboard Navigation Broken
- Missing `key.Matches()` — don't compare `msg.String()` directly for multi-key bindings.
- Forgot vim keys (`"k"` for up, `"j"` for down).

### Resize Causes Panic
- Component `SetSize` called before initialized — check `if m.viewport != nil`.
- Negative width/height — clamp: `max(0, msg.Width - sidebarWidth)`.

## References
- Bubbles help: https://github.com/charmbracelet/bubbles/tree/master/help
- Bubbles progress: https://github.com/charmbracelet/bubbles/tree/master/progress
- Bubbles spinner: https://github.com/charmbracelet/bubbles/tree/master/spinner
- Bubbles key: https://github.com/charmbracelet/bubbles/tree/master/key
- Huh forms: https://github.com/charmbracelet/huh
- Lipgloss: https://github.com/charmbracelet/lipgloss
- Catppuccin: https://github.com/catppuccin/catppuccin
- WCAG contrast: https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html
- Showcase reference: `/home/nova/charm-tui-showcase` (components: sidebar, forms, progress, notifications, layouts)