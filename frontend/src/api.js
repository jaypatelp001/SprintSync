/**
 * SprintSync API Client — handles all HTTP requests to the backend.
 */

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';

class ApiClient {
  constructor() {
    this.token = localStorage.getItem('sprintsync_token');
  }

  setToken(token) {
    this.token = token;
    if (token) {
      localStorage.setItem('sprintsync_token', token);
    } else {
      localStorage.removeItem('sprintsync_token');
    }
  }

  async request(path, options = {}) {
    const headers = {
      'Content-Type': 'application/json',
      ...options.headers,
    };

    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }

    const response = await fetch(`${API_BASE}${path}`, {
      ...options,
      headers,
    });

    if (response.status === 401) {
      this.setToken(null);
      window.location.href = '/';
      throw new Error('Session expired');
    }

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Request failed' }));
      throw new Error(error.detail || `HTTP ${response.status}`);
    }

    if (response.status === 204) return null;
    return response.json();
  }

  // Auth
  login(username, password) {
    return this.request('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ username, password }),
    });
  }

  register(username, email, password) {
    return this.request('/auth/register', {
      method: 'POST',
      body: JSON.stringify({ username, email, password }),
    });
  }

  getMe() {
    return this.request('/auth/me');
  }

  // Tasks
  listTasks(params = {}) {
    const query = new URLSearchParams();
    if (params.status) query.set('status', params.status);
    if (params.assignee_id) query.set('assignee_id', params.assignee_id);
    const qs = query.toString();
    return this.request(`/tasks/${qs ? '?' + qs : ''}`);
  }

  getTask(id) {
    return this.request(`/tasks/${id}`);
  }

  createTask(data) {
    return this.request('/tasks/', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  updateTask(id, data) {
    return this.request(`/tasks/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  updateTaskStatus(id, status) {
    return this.request(`/tasks/${id}/status`, {
      method: 'PATCH',
      body: JSON.stringify({ status }),
    });
  }

  deleteTask(id) {
    return this.request(`/tasks/${id}`, { method: 'DELETE' });
  }

  logTime(id, minutes) {
    return this.request(`/tasks/${id}/log-time`, {
      method: 'POST',
      body: JSON.stringify({ minutes }),
    });
  }

  // AI
  aiSuggest(type, title = null) {
    const body = { type };
    if (title) body.title = title;
    return this.request('/ai/suggest', {
      method: 'POST',
      body: JSON.stringify(body),
    });
  }

  // Stats
  topUsers() {
    return this.request('/stats/top-users');
  }

  metrics() {
    return this.request('/metrics');
  }
}

export const api = new ApiClient();
