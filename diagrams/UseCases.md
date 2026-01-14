# Use Case Diagram

```mermaid
usecaseDiagram
    actor Admin
    actor Parent
    actor Educateur
    actor Dietitian

    package "System" {
        usecase "Login" as UC1
        usecase "View Dashboard" as UC2
        usecase "Manage Users" as UC3
        usecase "Manage Groups" as UC4
        usecase "Manage Children" as UC5
        usecase "Manage Invoices" as UC6
        usecase "View Child Progress" as UC7
        usecase "Pay Invoices" as UC8
        usecase "Record Meal Intake" as UC9
        usecase "Create Menu" as UC10
        usecase "Assign Nutrition Plan" as UC11
        usecase "Record Attendance" as UC12
        usecase "Send Messages" as UC13
        usecase "Manage Activities" as UC14
    }

    Admin --> UC1
    Admin --> UC2
    Admin --> UC3
    Admin --> UC4
    Admin --> UC5
    Admin --> UC6
    Admin --> UC13

    Parent --> UC1
    Parent --> UC2
    Parent --> UC7
    Parent --> UC8
    Parent --> UC13

    Educateur --> UC1
    Educateur --> UC2
    Educateur --> UC9
    Educateur --> UC12
    Educateur --> UC13
    Educateur --> UC14

    Dietitian --> UC1
    Dietitian --> UC2
    Dietitian --> UC10
    Dietitian --> UC11
    Dietitian --> UC9
    Dietitian --> UC13
```
