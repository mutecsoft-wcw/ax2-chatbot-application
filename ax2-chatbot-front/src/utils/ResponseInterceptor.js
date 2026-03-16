export const responseInterceptor = (response) => {
    if (typeof response === 'string') {
        const clean = response.replace(/^data:\s*/, '').trim();
        if (!clean || clean === '[DONE]') return null;

        try {
            const parsed = JSON.parse(clean);
            return { 
                text: parsed.text || "", 
                isFinal: false 
            };
        } catch (e) {
            return { text: response, isFinal: false };
        }
    }
    return response;
};