import { apiRequest } from './client';

export async function recallMemory(client, query, bankId = null) {
  return apiRequest('/api/memory/recall', {
    method: 'POST',
    body: JSON.stringify({
      client,
      query,
      bank_id: bankId,
    }),
  });
}
