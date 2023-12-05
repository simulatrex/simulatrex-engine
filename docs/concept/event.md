# Event

An event is a key moment in our simulation that we expose our target audience to. Agents will form thoughts and perceptions based on these events. Each event is described using natural language.

## Required Parameters

 Parameter | Description |
-----------|-------------|
 `id` | The unique identifier of the event |
 `type` | The type of the event, chosen by the user |
 `source` | The source of the event |
 `content` | The content of the event |
 `impact` | The impact of the event, a number between 0 and 1 |
 `scheduled_time` | The scheduled time of the event, needs to be related to time_config and in date format |
