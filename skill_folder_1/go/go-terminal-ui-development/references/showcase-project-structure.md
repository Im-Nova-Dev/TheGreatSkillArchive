# Charm TUI Showcase Project Structure

Reference implementation at `/home/nova/charm-tui-showcase` — 12-page demo app demonstrating all major Charm libraries.

## Directory Layout
```
charm-tui-showcase/
├── cmd/main.go                    # Entry point
├── go.mod                         # Dependencies (v1.3.6 tea, v0.21.1 bubbles, v1.1.0 lipgloss, v1.0.0 huh)
├── internal/ui/
│   ├── app.go                     # Main app with 12 pages, sidebar nav
│   ├── styles/styles.go           # Catppuccin Mocha theme + all Lipgloss styles
│   ├── pages/
│   │   ├── dashboard.go           # Overview: stats cards, quick actions, system info, activity
│   │   ├── settings.go            # 3 tabs: Appearance, Behavior, Advanced
│   │   └── placeholder.go         # Generic "coming soon" page
│   └── components/
│       ├── sidebar.go             # Navigation: 12 items, keybindings, help, mouse click
│       ├── component_showcase.go  # Bubbles gallery (list + detail viewport)
│       ├── forms.go               # Huh form: Input, Text, Select, MultiSelect, Confirm
│       ├── data_display.go        # Table + 4 TextInputs (search, filter, query, regex)
│       ├── progress.go            # 4 Progress styles + 10 Spinner types
│       ├── text.go                # Textarea (line numbers) + live preview + code view
│       ├── layouts.go             # JoinH/V, Place, Flexbox, 3x3 Grid
│       ├── notifications.go       # Toasts, status bar, Confirm/Input/Custom dialogs
│       ├── animation.go           # Bouncing ball, particles, sine wave, HSV color cycle
│       └── mouse.go               # Draggable buttons, drawing canvas, click/hover log
```

## Key Implementation Patterns

### Page Registry (app.go)
```go
pages := map[PageID]interface{}{
    PageDashboard:     pages.NewDashboardModel(),
    PageComponents:    components.NewComponentShowcaseModel(),
    PageForms:         components.NewFormModel(),
    PageData:          components.NewDataDisplayModel(),
    PageProgress:      components.NewProgressModel(),
    PageText:          components.NewTextModel(),
    PageLayouts:       components.NewLayoutModel(),
    PageStyling:       pages.NewPlaceholderModel(...),
    PageNotifications: components.NewNotificationModel(),
    PageAnimation:     components.NewAnimationModel(),
    PageMouse:         components.NewMouseModel(),
    PageSettings:      pages.NewSettingsModel(),
}
```
Update uses type assertions: `page.(interface{ Update(tea.Msg) (tea.Model, tea.Cmd) })`

### Styles Package (styles/styles.go)
- **Palette**: All Catppuccin Mocha colors as `const` strings
- **Style vars**: `var ( ContainerStyle, SidebarStyle, TitleStyle, ... )`
- **Helpers**: `Width(w)`, `MaxWidth(w)`

### Responsive Resize
```go
func (m *AppModel) handleResize(width, height int) {
    sidebarWidth := 32
    contentWidth := width - sidebarWidth - 2
    m.sidebar.SetSize(sidebarWidth, height)
    for _, page := range m.pages {
        if s, ok := page.(interface{ SetSize(int, int) }); ok {
            s.SetSize(contentWidth, height)
        }
    }
}
```

### Sidebar Navigation
- `NavKeyMap` with `bubbles/key` bindings (Up/Down/Enter/Quit/Help/PageUp/PageDown)
- `bubbles/help` for context-aware help (short/full)
- Mouse click support: calculates item from Y position
- `SetSelected(i)` called from app when page changes via number keys

## Running the Showcase
```bash
cd /home/nova/charm-tui-showcase
go build -o charm-tui ./cmd/main.go
./charm-tui   # requires real TTY
```

## Navigation Keys
| Key | Action |
|-----|--------|
| 1-9,0 | Switch pages |
| ↑/↓/k/j | Navigate sidebar |
| PgUp/PgDown | Page sidebar |
| ? | Toggle help in sidebar |
| q/Ctrl+C | Quit |
| Page-specific | See each page's help |

## Dependencies (go.mod)
```
require (
    github.com/charmbracelet/bubbletea v1.3.6
    github.com/charmbracelet/bubbles v0.21.1
    github.com/charmbracelet/lipgloss v1.1.0
    github.com/charmbracelet/huh v1.0.0
    github.com/charmbracelet/log v1.0.0
)
```