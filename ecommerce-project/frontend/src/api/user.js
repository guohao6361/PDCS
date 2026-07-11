import http from './axios';

export const login = (username, password) =>
  http.post('/users/login', { username, password });

export const register = (username, password) =>
  http.post('/users/register', { username, password });
