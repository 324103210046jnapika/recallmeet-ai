import { apiRequest } from './client';

export async function getInsights(client) {
  return apiRequest(`/api/insights/${encodeURIComponent(client)}`);
}
