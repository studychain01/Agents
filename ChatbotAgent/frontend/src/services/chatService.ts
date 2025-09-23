export async function sendChatMessage(text: string) {
    const res = await fetch(`${import.meta.env.VITE_API_BASE}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json'},
        body: JSON.stringify({message: text}),
    });

    if(!res.ok) throw new Error('Failed to send');
    return res.json();
}

