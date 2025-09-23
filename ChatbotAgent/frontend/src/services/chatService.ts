export async function sendChatMessage(text: string) {
    const apiBase = import.meta.env.VITE_API_BASE || import.meta.env.VITE_API_URL || 'http://localhost:8000';
    const res = await fetch(`${apiBase}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json'},
        body: JSON.stringify({message: text}),
    });

    if(!res.ok) throw new Error('Failed to send');
    return res.json();
}

