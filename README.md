# Kanban clone Frontend - TICKETEER

## Project Overview
The TICKETEER is a task management tool built with Angular. It allows users to create, update, delete, and manage tasks in various stages of completion, such as "To Do," "In Progress," "Done," and "Urgent." The frontend communicates with a backend service (DJANGO/ https://github.com/benjaminBennewitz/kanban_backend) to persist data and ensure that users can effectively track their work.

## Why This Project is Useful
Managing tasks effectively is crucial for productivity. The TICKETEER Frontend provides a visual way to organize tasks, prioritize work, and ensure deadlines are met. It simplifies task management by providing a clear interface and robust functionality for handling various task states.

## Installation Guide
Follow these steps to set up the Kanban Frontend on your local machine:

### Prerequisites
- [Node.js](https://nodejs.org/) (version 12 or later)
- [Angular CLI](https://angular.io/cli) (version 17 or later)
- [Git](https://git-scm.com/)

## Installation and Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/benjaminBennewitz/kanban-frontend.git
    ```
2. Change to the project directory:
    ```bash
    cd kanban-frontend
    ```
3. Install dependencies:
    ```bash
    npm install
    ```
4. Start the development server:
    ```bash
    ng serve
    ```
5. Open your browser and navigate to `http://localhost:4200/`. The app will automatically reload if you change any of the source files.

### Configuration
Ensure the backend API URL is correctly set in your environment configuration files. Modify the environment files (`src/environments/environment.ts` and `src/environments/environment.prod.ts`) as needed to match your backend API settings.

### Building for Production
To build the project for production, run:
```bash
ng build --prod

## How Users Can Get Involved
Users can contribute to the project in several ways:
1. **Report Issues**: If you encounter any bugs or have suggestions for improvements, please report them via the [GitHub Issues](https://github.com/benjaminBennewitz/kanban-frontend/issues) page.
2. **Submit Pull Requests**: If you want to contribute code, fork the repository, make your changes, and submit a pull request. Make sure to follow the [contribution guidelines](CONTRIBUTING.md).

## Getting Help
If you have questions or run into problems, you can:
- Open an issue on GitHub
- Contact us via email: support@example.com

## Project Maintainers and Contributors
The TICKETEER Frontend project is managed by the following individuals:
- **[Your Name](https://github.com/benjaminBennewitz)** - Lead Developer


## License

This project is licensed under the MIT License
