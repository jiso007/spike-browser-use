module.exports = {
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended-type-checked',
    'plugin:@typescript-eslint/strict-type-checked',
    'plugin:import/recommended',
    'plugin:import/typescript',
    'plugin:unicorn/recommended',
    'plugin:react-hooks/recommended',
    'plugin:jsx-a11y/strict'
  ],
  plugins: ['@typescript-eslint', 'deprecation'],
  parser: '@typescript-eslint/parser', // Specify the ESLint parser for TypeScript
  parserOptions: {
    project: './tsconfig.json', // Specify the path to your tsconfig.json for type-aware rules
  },
  rules: {
    '@typescript-eslint/no-unused-vars': ['error', { ignoreRestSiblings: true }],
    '@typescript-eslint/consistent-type-definitions': ['error', 'type'],
    '@typescript-eslint/no-misused-promises': 'error',
    '@typescript-eslint/no-floating-promises': 'error',
    'deprecation/deprecation': 'warn',
    'unicorn/prefer-node-protocol': 'off',
    'import/consistent-type-specifier-style': ['error', 'prefer-top-level']
    // Add other rules as needed
  },
  settings: {
    'import/resolver': { // Configure import resolver for TypeScript
      typescript: true,
      node: true,
    },
    react: { // Configure React version for eslint-plugin-react
      version: 'detect', // Automatically detect the React version
    },
  },
  ignorePatterns: ['dist/', 'node_modules/'] // Ignore build and dependency folders
}; 