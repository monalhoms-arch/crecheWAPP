# Presence Activity Diagram

```mermaid
graph TD
    Start([Start]) --> Login[Educateur Logs In]
    Login --> SelectMenu[Select 'Pr&eacute;sences' Menu]
    SelectMenu --> ViewList[View Daily List]
    ViewList --> Check{Date Selected?}
    
    Check -- No --> DefaultDate[Use Today's Date]
    Check -- Yes --> LoadDate[Load Selected Date]
    
    DefaultDate --> FetchChildren[Fetch Children in Group]
    LoadDate --> FetchChildren
    
    FetchChildren --> DisplayList[Display Children List]
    
    DisplayList --> SelectChild[Select Child & Status]
    SelectChild --> Submit[Click 'Save/Update']
    
    Submit -- POST --> Controller[Presence Controller]
    Controller --> Validate[Validate Input]
    
    Validate -- Invalid --> Error[Flash Error]
    Error --> DisplayList
    
    Validate -- Valid --> UpsertDB[Update Database (Upsert)]
    UpsertDB --> Success[Flash Success]
    Success --> DisplayList
    
    DisplayList --> End([End])
```
