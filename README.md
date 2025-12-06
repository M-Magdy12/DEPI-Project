**Project planning**
    • Week 1: (OCT 18 – 24 OCT) Build Docker images & push to Docker Hub
    • Week 2: (OCT 25 – 31 OCT) Creating K8S cluster
    • Week 3: (NOV 1 – 7 NOV) Create infrastructure using Terraform &
    Ansible
    • Week 4: (NOV 8 – 14 NOV) Set up Jenkins CI/CD pipeline and
    deployment
    • Week 5: (NOV 15 – 21 NOV) Implement monitoring using Prometheus &
    Grafana
    • Week 6: (NOV 22 – 28 NOV) Final testing, documentation, and
    presentation

------------------------------------------------------------------------------------------------------------------------------------------------------
 
**Stakeholder Analysis**

    The Simple e-commerce web app with DevOps tools involves several key stakeholders who play different roles in both the development and DevOps processes. Each stakeholder has unique responsibilities, interests, and levels of influence that contribute to the success         of the project.

    The end users or customers are the primary stakeholders. They use the e-commerce platform to browse products, make purchases, and manage their orders. Their main interest lies in having a smooth and reliable shopping experience, with fast performance and secure checkout processes. Although they are not directly involved in DevOps operations, they are heavily affected by the system’s reliability, uptime, and deployment quality.

    The project manager oversees the overall planning, coordination, and execution of the project. This person ensures that all teams meet deadlines and that development and deployment progress remain on track. The project manager has a high level of influence and regularly communicates with the DevOps engineers to align deployment schedules and ensure stable releases.

------------------------------------------------------------------------------------------------------------------------------------------------------

**Database design**
   Relational Database (SQLite)
   The database is SQLite, a lightweight relational DB system.
   Tables are connected with foreign keys, meaning you are using a structured relational model.
   SQL queries are used for retrieving and updating data.
   Data is stored in a file called ecommerce.db

------------------------------------------------------------------------------------------------------------------------------------------------------

**UI/UX**

User Journey Overview
    Landing on Homepage → User sees available
    products immediately
    Browse Products → Prices, stock info, and order
    controls visible at a glance
    Place an Order → Simple quantity input + instant
    feedback
    Check Orders List → Users track their order history
    and status in one place
Usability & User Experience Focus
    Minimal clicks to perform key actions (order
    creation, browsing)
    Responsive design for mobile and desktop
    Simple layout designed for non-technical users
-----------------------------------------------------------------------------------------------------------------------------
Enhancement we are supposed to do
using Terraform to manage infrastructure as code (IaC), allowing us to automate the creation and management of cloud resources in a repeatable and consistent we will push it separately in commit called " Enhancement "   