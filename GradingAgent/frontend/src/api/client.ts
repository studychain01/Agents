// Backend API URL
const BACKEND_URL = 'https://ukp7a2u6pw.us-east-1.awsapprunner.com';
const BASE_URL = import.meta.env.VITE_API_URL?.replace(/\/$/, '') ?? BACKEND_URL;

async function json<T>(res: Response): Promise<T> {
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`HTTP ${res.status}: ${text}`);
  }
  return res.json();
}

export async function gradeEssay(essay: string) {
  const url = `${BASE_URL}/grade-essay`;
  console.log('Making request to:', url);
  console.log('Request body:', { essay });
  
  try {
    const res = await fetch(url, {
      method: 'POST',
      headers: { 
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
      body: JSON.stringify({ essay }),
    });
    
    console.log('Response status:', res.status);
    console.log('Response headers:', Object.fromEntries(res.headers.entries()));
    
    return json(res);
  } catch (error) {
    console.error('Fetch error:', error);
    throw new Error(`Network error: ${error instanceof Error ? error.message : 'Unknown error'}`);
  }
}
