```mermaid
graph LR
    subgraph "Gesamtsystem"
        subgraph "Backend-Server"
            A[Backend &#40;Python/Django/Flask&#41;] -- RESTful API --> B
            A --> C[Datenbank &#40;MariaDB&#41;]
            A --> D[Dokumentation &#40;Sphinx&#41;]
        end

        subgraph "Clients"
            B[Webanwendung &#40;React/Angular/Vue.js&#41;]
            subgraph "Mobile Apps (Cross-Plattform)"
                E[React Native / Flutter]
            end
            
            B --> F((API-Anfragen))
            E --> F
        end
        
        subgraph "Versionskontrolle & Dokumentation"
            G[GitHub &#40;Git&#41;]
            G --> H[Markdown Dokumentation]
            G --> A  
            G --> B
            G --> E
            G --> D

        end
        F -.-> A
    end

    style A fill:#ccf,stroke:#333,stroke-width:2px
    style B fill:#fcf,stroke:#333,stroke-width:2px
    style C fill:#cff,stroke:#333,stroke-width:2px
    style D fill:#ffc,stroke:#333,stroke-width:2px
    style E fill:#fcc,stroke:#333,stroke-width:2px
    style F fill:#eee,stroke:#333,stroke-width:1px,stroke-dasharray: 5 5
    style G fill:#eee,stroke:#333,stroke-width:2px
    style H fill:#ccf,stroke:#333,stroke-width:1px
