import { useState, useEffect } from 'react';

const useChatScroll = (isSurveyActive, isLoaded) => {
    const [isSurveyVisible, setIsSurveyVisible] = useState(true);

    const scrollToSurvey = () => {
        const chatElement = document.querySelector('deep-chat');
        const shadow = chatElement?.shadowRoot;
        const surveyElement = shadow?.getElementById("survey_form") 
                           || shadow?.querySelector(".dynamic-survey-card");

        if (surveyElement) {
            surveyElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
        } else {
            document.getElementById("survey_form")?.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    };

    useEffect(() => {
        if (!isSurveyActive) {
            setIsSurveyVisible(true);
            return;
        }

        const timer = setTimeout(() => {
            const chatElement = document.querySelector('deep-chat');
            const survey = chatElement?.shadowRoot?.getElementById("survey_form") 
                        || chatElement?.shadowRoot?.querySelector(".dynamic-survey-card");

            if (!survey) return;

            const observer = new IntersectionObserver(
                ([entry]) => setIsSurveyVisible(entry.isIntersecting),
                { threshold: 0.1 }
            );

            observer.observe(survey);
            return () => observer.disconnect();
        }, 500);

        return () => clearTimeout(timer);
    }, [isSurveyActive, isLoaded]);

    return { isSurveyVisible, scrollToSurvey };
};

export default useChatScroll;