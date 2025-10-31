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

    The Cloud-Native E-Commerce Application involves several key stakeholders who play different roles in both the development and DevOps processes. Each stakeholder has unique responsibilities, interests, and levels of influence that contribute to the success of the project.

    The end users or customers are the primary stakeholders. They use the e-commerce platform to browse products, make purchases, and manage their orders. Their main interest lies in having a smooth and reliable shopping experience, with fast performance and secure checkout processes. Although they are not directly involved in DevOps operations, they are heavily affected by the system’s reliability, uptime, and deployment quality.

    The project manager oversees the overall planning, coordination, and execution of the project. This person ensures that all teams meet deadlines and that development and deployment progress remain on track. The project manager has a high level of influence and regularly communicates with the DevOps engineers to align deployment schedules and ensure stable releases.

    The infrastructure engineer (Mahmoud Mohamed) is responsible for setting up and automating the cloud infrastructure using tools such as Terraform and Ansible. His main goal is to ensure scalability, consistency, and automation across all environments. This is a core DevOps role, directly contributing to the foundation on which the application runs.

    The Docker engineer (Ahmed Abdalkader) handles containerization and image management. His work ensures that each application component runs in a consistent environment across development, testing, and production. His influence is high because containerization directly affects how smoothly the CI/CD pipeline and deployments operate.

    The Kubernetes engineer (Marwan Hassan) manages the orchestration layer and ensures that containerized applications are efficiently deployed and scaled across clusters. He is responsible for managing deployment manifests, pods, and services, making him a crucial part of the DevOps workflow that guarantees uptime and high availability.

    The CI/CD engineer (Mohamed Magdy) designs and maintains the Jenkins pipeline for automation, testing, and deployment. He integrates version control systems like GitHub with Jenkins to automate build, test, and release processes. His work directly impacts the project’s delivery speed and reliability, giving him strong influence within the DevOps lifecycle.

    Finally, the monitoring engineer (Andrew Osama) is responsible for observability and performance tracking. He sets up Prometheus and Grafana to collect metrics, visualize data, and configure alerting systems. This role ensures that issues are detected early and that the system remains stable and efficient in production.

    Together, these stakeholders ensure that the Cloud-Native E-Commerce Application is built, deployed, and maintained with reliability, scalability, and continuous improvement in mind. Their collaboration represents the essence of DevOps — integrating development, operations, and monitoring into one cohesive workflow.

------------------------------------------------------------------------------------------------------------------------------------------------------

**Database design**
    The backend uses MongoDB with Mongoose to store and manage application
    data.
    The database includes four main collections: User, Product, Order, and
    Payment.
    Relationships between data are handled using Objected references — users
    can place multiple orders, each containing several products, and each order
    links to a payment record.
    The schema design ensures data consistency, scalability, and secure handle
    user authentication and payment information handling of user authentication
    and payment information.
    Overall, this structure supports a complete e-commerce workflow from
    product listing to order fulfillment.

------------------------------------------------------------------------------------------------------------------------------------------------------

**UI/UX**

1. Design Overview
    The user interface (UI) of the Cloud-Native E-Commerce Application follows a
    modern commercial layout inspired by online retail platforms. It focuses on
    clear product presentation, easy navigation, and a smooth checkout
    experience. The structure uses a grid-based layout displaying various product
    categories such as Mobiles, Electronics Furniture, and Fashion. The UI
    emphasizes usability, consistency, and simplicity——Ensuring that users can
    browse, search, and purchase products with minimal effort.

2. Color Palette & Visual Identity
    | Element         | Color                 | Purpose                                                                                    |
    | --------------- | --------------------- | ------------------------------------------------------------------------------------------ |
    | Primary Color   | **Blue (#007BFF)**    | Used in the header, buttons, and links to convey trust and reliability                     |
    | Secondary Color | **Yellow (#FFC107)**  | Used in promotional banners and highlights (e.g., Flipkart Plus section) to grab attention |
    | Background      | **White (#FFFFFF)**   | Provides a clean and minimal look, improving readability                                   |
    | Text Color      | **Black / Dark Gray** | Ensures clarity and contrast against the white background                                  |

3. Layout and Navigation
    • Grid Layout: Products are displayed in a responsive grid system for easy
    visual scanning.
    • Top Navigation Bar: Contains categories, search bars, and cart/login icons.
    • Category Sections: Featured collections with product thumbnails and
    prices.
    • Footer: Includes contact info, policies, and social media links.
    • Product Page: Shows details, reviews, price, and Add to Cart button.
4. User Experience (UX) Flow
    1. Browse Products Explore categories
    2. Product Selection View details, images, and reviews
    3. Add to Cart One-click interaction
    4. Checkout Enter address, payment, and confirm
    5. Order Tracking View delivery status
    5. Responsiveness and Accessibility
The application is fully responsive, adapting to mobile, tablet, and desktop
screens. It uses
clear icons, readable fonts, and strong color contrast for better accessibility.
Optimized for
touch interactions on mobile devices.