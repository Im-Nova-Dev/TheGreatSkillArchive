# UX Patterns from Charm TUI Showcase

Reference implementations in `/home/nova/charm-tui-showcase/internal/ui/components/`.

## Help System (sidebar.go)
```go
h := help.New()
h.ShowAll = false
h.Styles.ShortKey = styles.HelpKeyStyle
h.Styles.ShortDesc = styles.HelpDescStyle
h.Styles.FullKey = styles.HelpKeyStyle
h.Styles.FullDesc = styles.HelpDescStyle

keys := NavKeyMap{...} // implements ShortHelp()/FullHelp()
m.help.View(m.keys) // renders context-aware help
```

## Progress Bars (progress.go)
```go
// 4 styles demonstrated:
progress.New(progress.WithDefaultGradient())                           // 1. Default
progress.New(progress.WithScaledGradient("#f38ba8", "#a6e3a1"),       // 2. Custom gradient
    progress.WithWidth(40), progress.WithoutPercentage())
progress.New(progress.WithWidth(50))                                   // 3. Default blocks
progress.New(progress.WithWidth(30), progress.WithoutPercentage(),    // 4. No percentage
    progress.WithGradient("#89b4fa", "#cba6f7"))
```

## Spinners (progress.go)
```go
spinners := []spinner.Model{
    spinner.New(spinner.WithSpinner(spinner.Dot)),
    spinner.New(spinner.WithSpinner(spinner.Line)),
    spinner.New(spinner.WithSpinner(spinner.MiniDot)),
    spinner.New(spinner.WithSpinner(spinner.Jump)),
    spinner.New(spinner.WithSpinner(spinner.Pulse)),
    spinner.New(spinner.WithSpinner(spinner.Points)),
    spinner.New(spinner.WithSpinner(spinner.Globe)),
    spinner.New(spinner.WithSpinner(spinner.Moon)),
    spinner.New(spinner.WithSpinner(spinner.Meter)),
    spinner.New(spinner.WithSpinner(spinner.Hamburger)),
}
for i := range spinners {
    spinners[i].Style = styles.InfoStyle
}
```

## Huh Forms (forms.go)
```go
form := huh.NewForm(
    huh.NewGroup(                    // Personal Info
        huh.NewInput().Title("Name").Value(&data.Name).Validate(...),
        huh.NewInput().Title("Email").Value(&data.Email).Validate(emailCheck),
        huh.NewInput().Title("Age").Value(&data.Age).Validate(numericCheck),
    ).Title("Personal Information"),
    huh.NewGroup(                    // Biography
        huh.NewText().Title("Bio").Value(&data.Bio).CharLimit(500).Lines(5),
    ).Title("Biography"),
    huh.NewGroup(                    // Preferences
        huh.NewSelect[string]().Title("Role").Options(...).Value(&data.Role),
        huh.NewMultiSelect[string]().Title("Skills").Options(...).Value(&data.Skills),
        huh.NewSelect[string]().Title("Theme").Options(...).Value(&data.Theme),
    ).Title("Preferences"),
    huh.NewGroup(                    // Notifications
        huh.NewConfirm().Title("Subscribe").Value(&data.Subscribe),
        huh.NewConfirm().Title("Notifications").Value(&data.Notifications),
    ).Title("Notifications"),
    huh.NewGroup(                    // Scheduling
        huh.NewInput().Title("Priority").Value(&data.Priority).Validate(...),
        huh.NewInput().Title("Start Date").Value(&data.StartDate),
    ).Title("Scheduling"),
).WithTheme(huh.ThemeCharm()).WithWidth(60).WithShowHelp(true)
```

## Table + Filters (data_display.go)
```go
t := table.New(
    table.WithColumns([]table.Column{
        {Title: "ID", Width: 4},
        {Title: "Package", Width: 20},
        {Title: "Description", Width: 25},
        {Title: "Rating", Width: 12},
        {Title: "Status", Width: 15},
    }),
    table.WithRows(rows),
    table.WithFocused(true),
    table.WithHeight(15),
)
t.SetStyles(table.Styles{
    Header: styles.TableHeaderStyle,
    Selected: styles.TableRowSelectedStyle,
    Cell: styles.TableRowStyle,
})
```

## Textarea with Preview (text.go)
```go
ta := textarea.New()
ta.Placeholder = "Type here..."
ta.Focus()
ta.CharLimit = 5000
ta.SetWidth(80)
ta.SetHeight(15)
ta.ShowLineNumbers = true
ta.Cursor.Style = styles.SuccessStyle
ta.FocusedStyle.Base = lipgloss.NewStyle().
    Border(lipgloss.RoundedBorder()).
    BorderForeground(lipgloss.Color(styles.Blue)).
    Padding(0, 1).
    Background(lipgloss.Color(styles.Surface0)).
    Foreground(lipgloss.Color(styles.Text))
ta.BlurredStyle.Base = lipgloss.NewStyle().
    Border(lipgloss.RoundedBorder()).
    BorderForeground(lipgloss.Color(styles.Surface1)).
    Padding(0, 1).
    Background(lipgloss.Color(styles.Surface0)).
    Foreground(lipgloss.Color(styles.Text))
```

## Layouts (layouts.go)
```go
// Horizontal join
lipgloss.JoinHorizontal(lipgloss.Top, box1, box2, box3)

// Vertical join
lipgloss.JoinVertical(lipgloss.Left, box1, box2, box3)

// Center placement
lipgloss.Place(width, height, lipgloss.Center, lipgloss.Center, content)

// Corner placement
lipgloss.Place(width, height, lipgloss.Right, lipgloss.Bottom, content)

// Flex-like
lipgloss.JoinHorizontal(lipgloss.Center,
    style1.Width(20).Align(lipgloss.Left).Render("Left"),
    style2.Width(20).Align(lipgloss.Center).Render("Center"),
    style3.Width(20).Align(lipgloss.Right).Render("Right"),
)

// 3x3 Grid
cells := []string{style(i)...}
rows := []string{lipgloss.JoinHorizontal(lipgloss.Top, cells...)...}
grid := lipgloss.JoinVertical(lipgloss.Left, rows...)
```

## Notifications (notifications.go)
```go
// Toast types with auto-dismiss
toastStyle := lipgloss.NewStyle().
    Border(lipgloss.RoundedBorder()).
    BorderForeground(lipgloss.Color(typeColor)).
    Padding(1, 2).
    MarginBottom(1).
    Width(50)

// Status bar
statusStyle := lipgloss.NewStyle().
    Background(lipgloss.Color(styles.Mantle)).
    Foreground(lipgloss.Color(styles.Text)).
    Padding(0, 1).
    Width(m.width - 8).
    Align(lipgloss.Left)

// Dialogs (centered)
dialogStyle := styles.DialogStyle.Render("Content")
lipgloss.Place(width, height, lipgloss.Center, lipgloss.Center, dialogStyle)
```

## Mouse Interaction (mouse.go)
```go
case tea.MouseMsg:
    // Hover tracking
    m.hovers = append(m.hovers, HoverEvent{X: msg.X, Y: msg.Y, Time: timeStr})
    // Button bounds check
    inBounds := msg.X >= btn.X && msg.X < btn.X+btn.W &&
        msg.Y >= btn.Y && msg.Y < btn.Y+btn.H
    // Drag
    if msg.Action == tea.MouseActionPress && msg.Type == tea.MouseLeft {
        btn.Pressed = true
        m.dragging = true
        m.dragStart = &msg
    }
    if msg.Action == tea.MouseActionMotion && m.dragging {
        dx := msg.X - m.dragStart.X
        dy := msg.Y - m.dragStart.Y
        btn.X += dx
        btn.Y += dy
    }
```

## Animation Loop (animation.go)
```go
func (m AnimationModel) Init() tea.Cmd {
    return tea.Tick(time.Millisecond*50, func(t time.Time) tea.Msg {
        return animationTickMsg(t)
    })
}

case animationTickMsg:
    if m.running {
        m.tickCount++
        m.waveOffset += 0.1 * m.speed
        m.colorCycle += 0.02 * m.speed
        m.updatePhysics()
        m.updateParticles()
        cmds = append(cmds, tea.Tick(time.Millisecond*50, func(t time.Time) tea.Msg {
            return animationTickMsg(t)
        }))
    }
```

## Responsive Resize (app.go)
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