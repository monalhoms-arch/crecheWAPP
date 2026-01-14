# Deployment Diagram

```mermaid
graph TD
    UserClient[User Device (Browser)]
    
    subgraph DockerHost [Docker Host Server]
        subgraph DockerNetwork [Bridge Network]
            
            subgraph FlaskContainer [Container: creche_flask]
                Flask[Flask App (Gunicorn/Werkzeug)]
                Port5000[Port 5000]
            end
            
            subgraph MongoContainer [Container: creche_mongo]
                MongoDb[(MongoDB 7.0)]
                Port27017[Port 27017]
                VolData[Volume: mongo_data]
            end
            
        end
    end

    UserClient -- HTTP:5000 --> Port5000
    Port5000 --> Flask
    Flask -- "mongodb://mongo:27017" --> Port27017
    Port27017 --> MongoDb
    MongoDb -- Read/Write --> VolData

    style FlaskContainer fill:#e1f5fe,stroke:#01579b
    style MongoContainer fill:#e8f5e9,stroke:#2e7d32
```
