# System Architecture

```mermaid
graph TD
    subgraph Client
        Browser[Web Browser]
    end

    subgraph "Flask Application"
        App[app.py (Entry Point)]
        
        subgraph Controllers[Blueprints / Controllers]
            AuthBP[Auth Controller]
            ParentsBP[Parents Controller]
            EnfantsBP[Enfants Controller]
            EducateursBP[Educateurs Controller]
            DietitiansBP[Dietitians Controller]
            GroupsBP[Groups Controller]
            NutritionBP[Nutrition Controller]
            CommunicationBP[Communication Controller]
            ActivitiesBP[Activities Controller]
            FinanceBP[Payment/Invoice Controller]
        end

        subgraph Models[Data Models]
            UserM[User]
            ParentM[Parent]
            EnfantM[Enfant]
            EducateurM[Educateur]
            DietitianM[Dietitian]
            GroupM[Group]
            NutritionM[Nutrition/Meal]
            CommunicationM[Communication]
            InvoiceM[Invoice]
        end

        subgraph Views[Templates (Jinja2)]
            BaseT[base.html]
            AuthT[auth/*.html]
            DashboardT[index.html]
            ParentsT[parents/*.html]
            EnfantsT[enfants/*.html]
            NutritionT[nutrition/*.html]
            EtcT[...other templates]
        end
    end

    subgraph Database
        MongoDB[(MongoDB)]
    end

    Browser -- HTTP Requests --> App
    App -- Route Dispatch --> Controllers

    AuthBP --> UserM
    ParentsBP --> ParentM
    EnfantsBP --> EnfantM
    EducateursBP --> EducateurM
    DietitiansBP --> DietitianM
    GroupsBP --> GroupM
    NutritionBP --> NutritionM
    CommunicationBP --> CommunicationM
    FinanceBP --> InvoiceM

    Controllers -- Render --> Views
    Controllers -- Read/Write --> Models
    Models -- PyMongo --> MongoDB

    style Browser fill:#f9f,stroke:#333,stroke-width:2px
    style MongoDB fill:#ff9,stroke:#333,stroke-width:2px
    style App fill:#99f,stroke:#333,stroke-width:2px
```
