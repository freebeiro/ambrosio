module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'jsdom',
  transform: {
    '^.+\\.tsx?$': 'ts-jest',
    '^.+\\.jsx?$': 'babel-jest'
  },
  moduleFileExtensions: ['ts', 'tsx', 'js', 'jsx', 'json', 'node'],
  testMatch: ['**/tests/**/*.test.[jt]s?(x)'],
  setupFilesAfterEnv: ['./jest.setup.cjs'],
  globals: {
    'ts-jest': {
      tsconfig: 'tsconfig.json',
      useESM: false
    }
  },
  forceExit: true,
  detectOpenHandles: true
};
