import { apiRequest } from './client';

export async function getClients() {
  return apiRequest('/api/clients');
}

export async function getClient(client) {
  return apiRequest(`/api/clients/${encodeURIComponent(client)}`);
}
