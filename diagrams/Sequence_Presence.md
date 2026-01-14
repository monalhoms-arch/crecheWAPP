# Sequence Diagram: Daily Presence Recording

```mermaid
sequenceDiagram
    participant E as Educateur
    participant B as Browser
    participant PC as Presence Controller
    participant DB as MongoDB
    
    E->>B: Navigate to /presences
    B->>PC: GET /presences?date=today
    PC->>DB: Find all children (filtered by role)
    DB-->>PC: Children list
    PC->>DB: Find presences for date
    DB-->>PC: Presences list
    PC->>PC: Merge children + presences (Register View)
    PC->>PC: Calculate stats (present/absent/late)
    PC-->>B: Render presences.html with register + stats
    B-->>E: Display daily register
    
    E->>B: Select child, status, times
    E->>B: Click "Valider"
    B->>PC: POST /presences/add
    PC->>PC: Validate date <= today
    PC->>DB: Upsert presence record
    DB-->>PC: Success
    PC-->>B: Redirect to /presences?date=X
    B-->>E: Show updated register with stats
