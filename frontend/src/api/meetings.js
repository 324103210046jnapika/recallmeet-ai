import { apiRequest } from './client';

export async function getMeetings(client = null) {
  const query = client ? `?client=${encodeURIComponent(client)}` : '';
  return apiRequest(`/api/meetings${query}`);
}

export async function getMeeting(id) {
  return apiRequest(`/api/meetings/${encodeURIComponent(id)}`);
}

export async function createMeeting(data) {
  return apiRequest('/api/meetings', {
    method: 'POST',
    body: JSON.stringify(data),
  });
}

export async function prepareMeeting({ client, upcoming_context, user_question, memory_enabled = true }) {
  return apiRequest('/api/meetings/prepare', {
    method: 'POST',
    body: JSON.stringify({
      client,
      upcoming_context,
      user_question,
      memory_enabled,
    }),
  });
}

export async function seedMeetings() {
  return apiRequest('/api/meetings/seed', {
    method: 'POST',
  });
}

export async function getHealth() {
  return apiRequest('/api/health');
}
