/**
 * Frontend execution agent controller for the Lemonade-Router-Builder
 */
document.addEventListener('DOMContentLoaded', () => {
    const routerForm = document.getElementById('routerForm');
    const temperatureInput = document.getElementById('temperature');
    const tempValueDisplay = document.getElementById('tempValue');
    const promptInput = document.getElementById('prompt');
    const logConsole = document.getElementById('logConsole');
    const submitBtn = document.getElementById('submitBtn');

    // Dynamically update visual value trackers
    temperatureInput.addEventListener('input', (e) => {
        tempValueDisplay.textContent = e.target.value;
    });

    // Handle intent routing dispatch form submits
    routerForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const userPrompt = promptInput.value.trim();
        if (!userPrompt) {
            appendLog('[Warning] Target routing intent cannot be empty.', 'orange');
            return;
        }

        const configurationPayload = {
            prompt: userPrompt,
            temperature: parseFloat(temperatureInput.value),
            model: "Qwen3-Coder-30B-A3B-Instruct"
        };

        // Reset UI state for processing feedback
        submitBtn.disabled = true;
        submitBtn.textContent = "Routing Intent...";
        appendLog(`\n[Dispatch] Sending payload to core router framework using Qwen3 MoE configurations...`);

        try {
            // Adjust the backend URL path to match your local app gateway implementation (e.g., FastAPI / Flask)
            const response = await fetch('/api/route-intent', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(configurationPayload)
            });

            if (!response.ok) {
                throw new Error(`Server returned unhealthy code response status: ${response.status}`);
            }

            const data = await response.json();
            
            // Format log messages according to structural outputs parsed from the backend route tool registry
            appendLog(`[Success] Intent process finalized successfully.`);
            appendLog(`${data.result}`);

        } catch (error) {
            appendLog(`[Error] Fallback execution route broken: ${error.message}`, '#ef4444');
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = "Dispatch Intent Route";
        }
    });

    /**
     * Utility tool helper to log out timestamps and status markers directly into the UI panel
     */
    function appendLog(message, color = null) {
        const timestamp = new Date().toLocaleTimeString();
        const stylizedMessage = color 
            ? `<span style="color: ${color}">${message}</span>`
            : message;
            
        logConsole.innerHTML += `\n[${timestamp}] ${stylizedMessage}`;
        logConsole.scrollTop = logConsole.scrollHeight; // Autoscroll to bottom tracking logs
    }
});
