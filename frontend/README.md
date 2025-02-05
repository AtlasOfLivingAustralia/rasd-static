# frontend

This project is built using [Vue 3](https://vuejs.org/) and [Vite](https://vitejs.dev/)

## Frontend Requirements

- Node.js V18+ (with `npm`).

## Frontend Tools

- axios: For API calls
- bulma: CSS framework
- oruga: UI library
- luxon: date/time library
- pinia: state management
- validator: form validation
- vitest: unit testing
- eslint: linting
- prettier: code formatting

## Project setup for local development

```shell
cd frontend
```

```shell
npm install
```

### Compiles and hot-reloads for development

```shell
npm start
```

Server at: http://localhost:5173/

### Environment variables and Modes
Environment variables are defined in a `.env` file or `.env.[mode]` files.  
You can specify which environment/mode to use with the `--mode` switch. 

Example: start your frontend with the production env variables.
```shell
npm start -- --mode production
```
See https://vitejs.dev/guide/env-and-mode.html for details.




### Compiles and minifies for production
The build and deployment are handled by the CI/CD. You should never build and deploy manually.  
That said you can run a build for testing.

```shell
npm run build
```

The build result will be in the `dist/` directory.

### Run your unit tests

This project uses Vitest for unit testing. https://vitest.dev/
While there are no tests currently written for the front-end of the project, you can run the following command to see if the tests pass after writing your own tests:

```shell
npm run test
```

### Lint with ESLint and code formatting with Prettier

ESLint
```shell
npm run lint
```

Prettier code check
```shell
npm run prettier-check
```

Prettier code format
```shell
npm run prettier-write
```

#### CI/CD quality assurance check 
The CI/CD will run the frontend lint and prettier at every commit.


### VSCode note:

make sure that you have inherit terminal env enabled if debug fails to load: ![alt text](https://gitlab.gaiaresources.com.au/devs/bdr-parta/uploads/2d11e5a5d55df6264365b740bac78c77/Screen_Shot_2022-03-25_at_1.34.05_pm.png)

### Recommended IDE Setup

[VSCode](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur) + [TypeScript Vue Plugin (Volar)](https://marketplace.visualstudio.com/items?itemName=Vue.vscode-typescript-vue-plugin).

