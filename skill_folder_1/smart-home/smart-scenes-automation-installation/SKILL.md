---
name: smart-scenes-automation-installation
description: Teach creating, naming, and testing lighting scenes and time/trigger/condition-based automations across Hue, HomeKit, Google Home, Alexa, Govee, and SmartThings. Covers golden rules for reliable schedules, fallback behavior, and transition timing.
---

# Smart Scenes & Automation Installation Mastery

## Core concept
A scene is one saved lighting state. An automation is a scene triggered by time, sensor, or device event. 90% of daily smart-home value comes from good automation design, not app control.

## Terminology
  - Scene: snapshot of brightness, CCT, color for a group.
  - Automation: IF <trigger> AND <conditions> THEN <action(s)>.
  - Transition time: fade duration in seconds; prevents jarring brightness jumps.
  - Condition: optional filter so automation only runs when true (e.g., “only if nobody home”).
  - Time trigger: sunrise/sunset with offset, specific clock time.

## Setup flows
### Hue scenes and automations
1. Hue app: Rooms > select room > tap + > Add scene.
2. Name by purpose: “Morning”, “Focus”, “Movie”, “Off”.
3. Automations tab: select “Add automation” > choose trigger (time, sensor, button).
4. Set transition time 1-3s for small changes; 10-30s for wake-up.

### Apple HomeKit scenes
1. Home app: Automation tab > + > Choose Accessory.
2. Set trigger (time of day, sensor).
3. Select scene or set brightness/color inline.
4. Test by tapping scene.

### Alexa / Google Home
1. Alexa app: More > Routines > +.
2. Trigger: Voice, Schedule, Device.
3. Actions: Smart Home > Control lights; set brightness/color temp.
4. Save and test.

### Govee scenes
1. Govee Home: Group > Add Scene > DIY.
2. Save with name; assign to automation trigger.
3. For music/camera sync: enable permissions.

## Golden rules
  Rule 1: Start with scenes first, automations second. Scene failures are visible immediately; automation failures may never be noticed.
  Rule 2: Always include an “Off” scene for every room.
  Rule 3: Use transition times >0s for wake-up scenes.
  Rule 4: Set sensor-triggered automations to re-arm after 30-60s delay. Otherwise one motion event fires every 15 minutes forever.

## Automation patterns worth teaching
  - Goodnight: all lights off + locks engaged + thermostat set.
  - Welcome home: porch light on at 40% when front door unlocks after sunset.
  - Movie time: living room dims to 15%, 2700K, strips go blue accent.
  - Wake-up: bedroom 2700K at 1% → 80% over 15 min from 6:45am weekdays.
  - Night light: hall 2700K at 5%, only if lux < 10 and motion after 11pm.

## Troubleshooting
  Symptom                  | Cause                       | Fix
  -------------------------|-----------------------------|--------------------------------
  Automation fires wrong time | Time zone mismatch on hub   | Set hub time zone in app
  Scene looks different on bulb vs in app | saved color space mismatch | Re-record scene from physical bulb
  Motion triggers too often  | No delay / re-arm window     | Add 60s timeout
  Voice fails but app works | Device name ambiguous       | Rename to “Kitchen Ceiling” not “Hue Color 2”

## Teaching drills
- Drill 1: apprentice writes 3 scenes from verbal requirements in <10 min each.
- Drill 2: break an existing automation; apprentice finds missing condition.
- Drill 3: daylight harvesting exercise; apprentice creates rule that blinds adjust when living room lux exceeds 500.

## Post-install
- [ ] Every room has at least an “On” and “Off” scene.
- [ ] Motion automations include armed timeout.
- [ ] Wake-up transition tested at actual wake hour.
- [ ] Voice labels unambiguous (no “Light 2”).
- [ ] Fallback behavior documented: if Wi-Fi dies, local control via switch/remote still works.
