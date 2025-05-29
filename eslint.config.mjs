import pluginJs from "@eslint/js";
import eslintPluginImport from "eslint-plugin-import";
import eslintPluginUnicorn from "eslint-plugin-unicorn";
import eslintPluginDeprecation from "eslint-plugin-deprecation";
import eslintPluginReactHooks from "eslint-plugin-react-hooks";
import eslintPluginJsxA11y from "eslint-plugin-jsx-a11y";

// Correct import pattern for the @typescript-eslint/eslint-plugin CommonJS module
import tseslintPlugin from "@typescript-eslint/eslint-plugin";
import globals from "globals"; // Import the globals package again for easier access to predefined environments

export default [
  // Ignore patterns for the entire configuration
  {
    ignores: ['dist/', 'node_modules/', '.eslintrc.cjs', 'eslint.config.mjs', 'babel.config.js', 'playwright.config.ts'] // Also ignore playwright config for now
  },
  // General configuration for all relevant code files (JS, JSX, TS, TSX)
  {
    files: ['**/*.{js,jsx,ts,tsx,cjs,mjs}'], // Apply to common code file extensions
    rules: {
      ...pluginJs.configs.recommended.rules, // Basic ESLint recommended rules
      // Add other non-type-aware rules here that apply generally
      'unicorn/prefer-node-protocol': 'off',
      // Disable no-undef and no-unused-vars globally and enable them in environment-specific overrides
      'no-undef': 'off',
      'no-unused-vars': 'off',
    },
    plugins: {
       // Include plugins with rules that don't require type info by default
       import: eslintPluginImport,
       unicorn: eslintPluginUnicorn,
       'react-hooks': eslintPluginReactHooks,
       'jsx-a11y': eslintPluginJsxA11y,
       deprecation: eslintPluginDeprecation, // Include deprecation here, but apply type-aware part below
    },
    settings: { // General settings (can be overridden)
      react: { // Configure React version for eslint-plugin-react
        version: 'detect', // Automatically detect the React version
      },
      'import/resolver': { // Configure import resolver for TypeScript and Node
        typescript: true,
        node: true,
      },
    },
    languageOptions: { // Basic language options without specific parser/project
      // Globals defined here will be merged with environment-specific globals in overrides
      globals: { // Manually define common globals that are consistently named
        globalThis: 'readonly',
        console: 'readonly',
        process: 'readonly',
        module: 'readonly',
        require: 'readonly',
        __dirname: 'readonly',
        __filename: 'readonly',
      }
    },
  },
  // Configuration specifically for TypeScript files (including type-aware rules)
  {
    files: ['**/*.ts', '**/*.tsx'], // Apply only to TypeScript files
    // Correctly register the @typescript-eslint plugin
    plugins: { '@typescript-eslint': tseslintPlugin },
    // Include and configure type-aware rules
    rules: {
      ...tseslintPlugin.configs.recommended.rules,
      ...tseslintPlugin.configs['recommended-type-checked'].rules,
      ...tseslintPlugin.configs['strict-type-checked'].rules,
      // Add custom rules or overrides for TS files
      // Re-enable type-aware no-unused-vars
      '@typescript-eslint/no-unused-vars': ['error', { ignoreRestSiblings: true }],
      '@typescript-eslint/consistent-type-definitions': ['error', 'type'],
      '@typescript-eslint/no-misused-promises': 'error',
      '@typescript-eslint/no-floating-promises': 'error',
      // The deprecation rule is type-aware, so include it here as well
      'deprecation/deprecation': 'warn',
    },
    languageOptions: {
      // Specify the TypeScript parser and project options
      parser: tseslintPlugin.parser,
      parserOptions: {
        project: './tsconfig.json', // Specify the path to your tsconfig.json for type-aware rules
      },
      // Note: Globals for TS files will be inherited from the general config and environment overrides
    },
  },
  // Environment-specific overrides
  // Browser environment (for DOM manipulation code)
  {
    files: ['browser_use/dom/**/*.js', 'browser_use/dom/**/*.ts'], // Adjust glob pattern as needed
    languageOptions: {
      globals: { // Sanitize and add browser globals + performance
        ...Object.fromEntries(
          Object.entries(globals.browser).map(([key, value]) => [key.trim(), value])
        ),
        'performance': 'readonly',
      },
    },
    rules: {
      // Re-enable no-undef and no-unused-vars for this specific environment
      'no-undef': 'error',
      'no-unused-vars': ['error', { argsIgnorePattern: '^_' }], // Allow unused vars starting with _
    },
  },
  // Chrome Extension environments (background, content, popup)
  {
    files: ['browser_use_ext/extension/**/*.js', 'browser_use_ext/extension/**/*.ts'], // Adjust glob pattern as needed
    languageOptions: {
      globals: { // Sanitize and add browser globals + chrome, WebSocket, setTimeout
        ...Object.fromEntries(
          Object.entries(globals.browser).map(([key, value]) => [key.trim(), value])
        ),
        'chrome': 'readonly',
        'WebSocket': 'readonly',
        'setTimeout': 'readonly',
      },
    },
    rules: {
      // Re-enable no-undef and no-unused-vars for this specific environment
      'no-undef': 'error',
      'no-unused-vars': ['error', { argsIgnorePattern: '^_' }], // Allow unused vars starting with _
    },
  },
   // Jest test files
  {
    files: ['**/*.test.js', '**/*.test.ts', '**/*.test.jsx', '**/*.test.tsx'], // Jest test file pattern
    languageOptions: {
      globals: { // Sanitize and add Jest globals + global, setTimeout, WebSocket
        ...Object.fromEntries(
          Object.entries(globals.jest).map(([key, value]) => [key.trim(), value])
        ),
        'global': 'readonly',
        'setTimeout': 'readonly',
        'WebSocket': 'readonly',
      },
    },
    rules: {
      // Re-enable no-undef and no-unused-vars for this specific environment
      'no-undef': 'error',
      'no-unused-vars': ['error', { argsIgnorePattern: '^_' }], // Allow unused vars starting with _
      // Add Jest specific rules if needed, e.g., from eslint-plugin-jest
      'no-func-assign': 'warn', // Temporarily reduce severity for known issues
    },
  },
  // Add more environment overrides as needed (e.g., Node.js specific files)
  // Example: Node.js files (if any outside of build scripts)
  // {
  //   files: ['src/server/**/*.js', 'src/server/**/*.ts'],
  //   languageOptions: {
  //     globals: { ...globals.node },
  //   },
  //   rules: { 'no-undef': 'error', 'no-unused-vars': ['error', { argsIgnorePattern: '^_' }] },
  // },
]; 