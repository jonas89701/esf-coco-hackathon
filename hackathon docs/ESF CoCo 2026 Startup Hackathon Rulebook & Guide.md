# Startup Hackathon Rulebook

## **1\. Code of Conduct**

This handbook outlines technical, ethical, procedural, and governance regulations for the ESF CoCo 2026 Startup Hackathon. All participants are required to strictly adhere to these guidelines throughout the two-week development phase and the final presentation showcase. By competing in this hackathon, you hereby agree to the following conditions.

### **1.1 General Code of Conduct**

* **Fair Play & Respect:** Participants must maintain professional conduct toward fellow competitors, mentors, and judges. Harassment, discrimination, or unsportsmanlike behavior will result in immediate disqualification.  
* **Academic & Intellectual Integrity:** Plagiarism, misrepresentation of pre-existing work, or intentional falsification of prototype functionality is strictly prohibited.  
* **Compliance:** Failure to comply with any section of this handbook may lead to point deductions or forfeiture of competition eligibility at the organizers' discretion.

## **2\. Team Composition & Eligibility Rules**

### **2.1 Division Structure**

The competition is segregated into two primary divisions: **Novice Division** and **Advanced Division**. Teams must register under the appropriate tier based on their prior programming experience and project complexity goals.

#### **2.2 Team Formation & Year Group Division Mapping**

* **Team Size:** Teams must consist of designated student team members. Solo submissions or multi-student collaborations must be registered prior to the hackathon begins.  
* **Participant Eligibility:** All team members must be enrolled students within the eligible grades. **Individual Work Contribution:** All project assets, including software source code, user interfaces, database designs, and documentation, must be exclusively authored by registered team members.  
* **Division Allocation by Year Group:** Division placement is determined by the highest year group represented within your team:

| Year Group | Division Placement Rules |
| :---- | :---- |
| **Years 7 – 10** | Default placement is the **Novice Division**. Teams in this age band may optionally choose to enter the **Senior (Advanced) Division** if they wish to tackle higher-complexity prompts. |
| **Years 11 – 13** | **Mandatory Senior Division**. Any team featuring at least one student from Year 11, 12, or 13 will be automatically placed in the Senior Division. |

### **2.3 Mentorship & External Assistance Regulations**

* **Permissible Guidance:** External assistance from teachers, industry mentors, or internet forums is strictly restricted to conceptual advisory, troubleshooting assistance, and high-level architecture feedback.  
* **Prohibited Direct Intervention:** Mentors, parents, teachers, or non-team members are strictly forbidden from writing code, drawing user interfaces, preparing presentation slides, or directly creating any project assets.

## **3\. Technical Development & Code Governance**

### **3.1 Hackathon Development Window**

* **Strict Start Time:** All ideation, architectural design, UI prototyping, and code development must occur exclusively within the official two-week hackathon period.  
* **Prohibition of Pre-Existing Codebases:** Projects built upon existing commercial software, pre-packaged app templates, or prior personal repositories created before the hackathon start date are strictly barred from submission.

### **3.2 Permissible Software Libraries, APIs, and Frameworks**

To support rapid development and modern software engineering practices, third-party libraries and APIs are permitted under the following regulations:

* **Open-Source Frameworks:** Teams may utilize open-source libraries, packages, and frameworks (e.g., React, Vue, Flutter, PyTorch, Express, Tailwind CSS, standard language runtime libraries).  
* **Public APIs:** Integration of third-party public Application Programming Interfaces (APIs)—such as weather services, mapping tools, public dataset endpoints, or cloud services—is fully allowed.  
* **Attribution Requirement:** Every external dependency, library, framework, or API utilized must be explicitly cited in the project's documentation and code repository (e.g., within a package.json, requirements.txt, or README.md file).

### 

### **3.3 Artificial Intelligence (AI) Usage Policy**

The integration of Generative AI tools (including LLMs, code completion assistants, generative design platforms, and synthetic dataset generators) is permitted under a strict governance framework:

| Category | Permissible Usage | Prohibited Usage   |
| :---- | :---- | :---- |
| **Code Generation** | Generating snippets, debugging specific functions, refactoring modules, or exploring architectural patterns. | Submitting unedited, boiler-plate AI codebases without substantial custom integration, adaptation, or manual authoring. |
| **Asset Creation** | Using AI for initial icon inspiration, texture generation, or asset placeholders that are integrated into custom designs. | Submitting complete UI layouts, application designs, or vector graphic sets generated entirely by AI without manual modification. |
| **Documentation & Disclosures** | Drafting functional specs or refining written explanations. | Failing to disclose specific AI tools used and their exact role in project asset creation. |

### **3.4 Mandatory AI Disclosure Declaration**

Every submission must include an **AI Disclosure Statement** attached to the source repository. The disclosure must detail:

1\. AI Tools Utilised (e.g., GitHub Copilot, ChatGPT, Midjourney)  
2\. Scope of Application (e.g., "Used Copilot for unit testing logic", "Used ChatGPT to create synthetic data")  
3\. Team Modification Narrative (Detailed summary of how AI outputs were modified, integrated, or refactored by the team)

### **3.5 Hardware Integration Policy**

Participants are permitted to build or incorporate physical hardware components (such as microcontrollers, sensors, bespoke 3D-printed enclosures, or robotic interfaces) into their submissions, provided the following regulations are strictly observed:

* **Software-Centric Focus:** Hardware elements must strictly serve to complement and enhance the software application, not replace it. The core of the evaluation remains on software functionality, code logic, and digital user experience. Projects relying solely on off-the-shelf physical assemblies without substantial custom software development may receive significant point deductions under Technical Complexity.  
* **Permissible Model Remixing:** Teams are permitted to utilise, modify, or remix open-source 3D models or CAD assets found online (e.g. Printables, Thingiverse, GrabCAD, Onshape Public Domain). However, significant custom modifications must be made during the competition window to tailor the physical design to the team's specific project architecture.  
* **Mandatory Technical Verification & Attribution:** Teams incorporating custom or remixed physical builds must produce and provide complete design documentation in their public repository for authenticity verification. This includes:  
  * Wiring schematics and circuit diagrams.  
  * Source files and print formats (e.g. STL, STEP, or Onshape/Fusion 360 share links) for all custom or modified components.  
  * Direct links and licence citations for any third-party models used as a base.  
  * Clear documentation highlighting the specific modifications or remixes engineered by the team.  
  * Source code for any embedded firmware or microcontroller scripts (e.g. Arduino, ESP32, Raspberry Pi).  
* **Originality & Intellectual Property:** Submitting unmodified, unmodified third-party CAD models and presenting them as original work is strictly treated as plagiarism. All custom mechanical designs, firmware, and model modifications must be authored by registered team members during the official two-week development window.

## **4\. Submission Deliverables & Repository Governance**

### **4.1 Mandatory Deliverables**

Teams must submit the following items prior to the official competition submission deadline:

1. **Source Code Access:** Public repository link (e.g., GitHub, GitLab, or shared google drive folder) containing all runnable source files, configuration scripts, and asset folders. Version control software like GitHub or GitLab is preferred as we can see changes made to verify authenticity and originality. For those who choose to integrate hardware, provide documentation and designs via Google Drive. **Novice division using Scratch may simply upload the.sb3 to Google Drive and share.**  
2. **Repository Documentation (README.md):** Comprehensive setup instructions, dependency lists, build commands, and the AI Disclosure Statement.  
3. **Recorded Presentation Pitch:** A 2-minute video recording of the team's project presentation and live prototype demonstration. May be edited in whatever manner the team chooses, so long as it conveys the message.

### **4.2 Technical Prototype / MVP Guidelines**

* **Minimum Viable Product (MVP):** Submissions must demonstrate functional execution. Static wireframes, slide-only proposals, or non-functional mockups do not qualify as technical prototypes.  
* **Executability:** Instructions to build, compile, or host the application locally or via web preview must be fully verified and working.

## **5\. Presentation, Pitch, and Final Adjudication Rules**

### **5.1 Presentation Specifications**

* **Duration Limit:** Pitch recordings must strictly adhere to the **2-minute time limit**. Content exceeding 2 minutes will not be evaluated by the judging panel.

* **Mandatory Presentation Elements:**  
  1. Problem statement and user context definition.  
  2. Selected Challenge Prompt and alignment overview.  
  3. Live or recorded functional prototype walk-through.  
  4. Technical architecture, technology stack, and AI tool disclosure review.

### **5.2 Judging Finality & Governance**

* **Scoring Integrity:** All submissions will be independently evaluated by designated judges using an evaluation rubric which will be sent separately.  
* **Binding Authority:** Final scoring decisions, prize awards, and potential disqualification rulings made by the judging panel and organizing committee are final, binding, and non-appealable.

### **5.3 Live Finalist Showcase & Final Adjudication**

Following the initial judging phase, the **top 3 shortlisted teams from each division** will be invited to participate in a final presentation to determine the final overall standings:

* **Event Details:** Sunday, 4th October 2026, South Island School  
* **Format & Presentation:** Shortlisted teams will showcase their project to the panel of judges and answer follow-up technical questions.  
* **Online Participation Option:** While in-person attendance is encouraged, any shortlisted team unable to attend on-site on Sunday, 4th October 2026 may participate remotely via an online video link.  
* **Notification & Award Distribution:** Teams selected for the final showcase will receive an email notification detailing exact timings, presentation requirements, and access links. For teams attending remotely or unable to collect prizes on the day, physical awards and certificates will be sent directly to their school.

