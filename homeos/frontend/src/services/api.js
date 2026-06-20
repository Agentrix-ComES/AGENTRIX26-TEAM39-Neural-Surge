// api.js

export async function generatePlan({ budget, familySize, inventory }) {
  const response = await fetch('/api/plan/generate', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      budget: parseFloat(budget),
      family_size: parseInt(familySize, 10),
      inventory: inventory,
    }),
  });
  
  if (!response.ok) {
    const err = await response.json();
    throw new Error(err.detail || 'Failed to generate plan.');
  }
  
  return response.json();
}

export async function getTrace() {
  const response = await fetch('/api/plan/trace');
  if (!response.ok) {
    throw new Error('Failed to fetch agent trace.');
  }
  return response.json();
}

export async function getDayDetail(id) {
  const response = await fetch(`/api/plan/day/${id}`);
  if (!response.ok) {
    const err = await response.json();
    throw new Error(err.detail || `Failed to fetch details for day ${id}.`);
  }
  return response.json();
}
