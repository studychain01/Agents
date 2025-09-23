export async function sendChatMessage(text: string) {
    const apiBase = import.meta.env.VITE_API_BASE || import.meta.env.VITE_API_URL || 'https://35uprpy3px.us-east-2.awsapprunner.com';
    const res = await fetch(`${apiBase}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json'},
        body: JSON.stringify({
            session_id: 'default-session',
            input: text
        }),
    });

    if(!res.ok) throw new Error('Failed to send');
    return res.json();
}

