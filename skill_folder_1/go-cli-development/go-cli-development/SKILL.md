---
name: go-cli-development
description: Teach Go CLI development including flag parsing, Cobra/urfave CLI frameworks, terminal UX, configuration, and distribution.
tags:
  - golang
  - cli
  - terminal
---

# Go CLI Development

## Purpose
Teach Go CLI development for building elegant command-line tools. Use this skill when building CLIs, teaching cobra/urfave, or improving terminal UX.

## Core Principles
- Subcommands should be discoverable
- Help text is documentation
- Exit codes mean something
- Config files supplement flags, not duplicate them
- Human-readable and machine-readable output modes

## Stdlib CLI
- `flag` package for simple arguments
- `os.Args` for raw access
- `fmt` and `io` for output formatting
- `os.Exit` for exit codes

## Framework Comparison
- `spf13/cobra`: batteries included, subcommands, completion
- `urfave/cli`: simpler API, less boilerplate
- Use stdlib when command surface is minimal

## Cobra Basics
```go
var rootCmd = &cobra.Command{
    Use:   "myapp",
    Short: "Brief description",
    Long:  `Longer description here`,
}
```

## Flags and Arguments
- Persistent flags (inherited by subcommands)
- Local flags
- Positional args with `Args`

## Terminal UX
- Colored output with `fatih/color` or ANSI codes
- Progress bars with `cheggaaa/pb`
- Interactive prompts with `AlecAivazis/survey`
- Tables with `olekukonko/tablewriter`

## Configuration
- Viper for config files, env vars, and flags
- `viper.BindPFlags` integration with Cobra
- Support JSON, YAML, TOML, ENV

## Testing CLIs
- Capture stdout/stderr
- Test flag defaults and overrides
- Test subcommand execution paths

## Common Mistakes
- Not setting exit codes properly
- Duplicating help text
- Global mutable state for CLI config
- Making CLI output hard to parse
- Missing bash/zsh/fish completion

## Teaching Sequence
1. Stdlib flag parsing simple app
2. Cobra basic command structure
3. Add subcommands and flags
4. Add configuration support
5. Add terminal UX improvements
6. Add shell completion
7. Package and distribute with Goreleaser