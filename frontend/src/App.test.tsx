import { render, screen } from '@testing-library/react';
import App from './App';

// Mock fetch for testing in jsdom environment
beforeAll(() => {
  global.fetch = jest.fn(() =>
    Promise.resolve({
      json: () => Promise.resolve([]),
    } as unknown as Response)
  );
});

afterAll(() => {
  jest.restoreAllMocks();
});

test('renders App component without crashing', () => {
  render(<App />);
  // Check for key elements that should exist
  expect(document.body).toBeTruthy();
});

test('renders navigation', () => {
  render(<App />);
  expect(screen.getByText(/echo/i)).toBeInTheDocument();
});

test('renders initial state message', () => {
  render(<App />);
  expect(screen.getByText(/no transcription yet/i)).toBeInTheDocument();
});