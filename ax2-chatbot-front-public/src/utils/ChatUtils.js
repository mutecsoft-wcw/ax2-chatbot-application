export const analyzeSurveyStatus = (allMessages) => {
    if (allMessages.length < 2) return { hasSurvey: false, isMatched: false };

    const hasSurvey = allMessages.some(msg => (msg.html || "").includes("dynamic-survey-card"));
    let isMatched = false;

    const positiveWords = ["예", "응", "네", "그래", "__START_SURVEY__", "좋아"];

    for (let i = allMessages.length - 1; i >= 1; i--) {
        const currentUserMsg = allMessages[i];
        const prevAiMsg = allMessages[i - 1];

        if (currentUserMsg.role === 'user') {
            const userText = (currentUserMsg.text || "").trim();
            const aiText = (prevAiMsg.html || prevAiMsg.text || "").replace(/<[^>]*>?/gm, '');

            const isUserPositive = positiveWords.some(word => userText.includes(word));
            const isAiAsking = aiText.includes("간단 설문을 진행하시겠습니까?");

            if (isUserPositive && isAiAsking) {
                isMatched = true;
                break;
            }
        }
    }

    return { hasSurvey, isMatched };
};