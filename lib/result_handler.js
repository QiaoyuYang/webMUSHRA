/**
 * Custom Result Handler for webMUSHRA on GitHub Pages
 * 
 * Since GitHub Pages is static, we need alternative ways to collect results:
 * 1. Download as JSON file (participant emails it to you)
 * 2. Send to Google Forms (automated collection)
 * 3. Send to a custom backend API
 * 
 * SETUP INSTRUCTIONS:
 * 1. Copy this file to your webMUSHRA lib/ directory
 * 2. Include it in index.html after the other scripts
 * 3. Configure your Google Form (see instructions below)
 */

// ============== CONFIGURATION ==============

const RESULT_CONFIG = {
    // Option 1: Google Forms (recommended for GitHub Pages)
    // Set up a Google Form with a single "Long answer" question
    // Get the form URL and field ID from the form's pre-filled link
    googleForms: {
        enabled: true,
        formUrl: "https://docs.google.com/forms/d/e/YOUR_FORM_ID/formResponse",
        fieldId: "entry.YOUR_FIELD_ID"  // e.g., "entry.1234567890"
    },
    
    // Option 2: Custom backend API
    customApi: {
        enabled: false,
        url: "https://your-server.com/api/results",
        method: "POST"
    },
    
    // Option 3: Always allow download as backup
    allowDownload: true,
    
    // Participant ID settings
    requireParticipantId: true,
    generateRandomId: true  // If true, auto-generate; if false, ask user
};

// ============== IMPLEMENTATION ==============

class ResultHandler {
    constructor(config) {
        this.config = config;
        this.participantId = null;
    }
    
    async initialize() {
        if (this.config.requireParticipantId) {
            if (this.config.generateRandomId) {
                this.participantId = this.generateParticipantId();
                console.log(`Participant ID: ${this.participantId}`);
            } else {
                this.participantId = prompt("Please enter your participant ID:");
            }
        }
        return this.participantId;
    }
    
    generateParticipantId() {
        const timestamp = Date.now().toString(36);
        const randomPart = Math.random().toString(36).substring(2, 8);
        return `P_${timestamp}_${randomPart}`.toUpperCase();
    }
    
    async submitResults(results) {
        const payload = {
            participantId: this.participantId,
            timestamp: new Date().toISOString(),
            userAgent: navigator.userAgent,
            results: results
        };
        
        const jsonString = JSON.stringify(payload, null, 2);
        let success = false;
        
        // Try Google Forms
        if (this.config.googleForms.enabled) {
            try {
                success = await this.sendToGoogleForms(jsonString);
                if (success) {
                    alert("✅ Results submitted successfully!\n\nThank you for participating.");
                    return true;
                }
            } catch (error) {
                console.error("Google Forms submission failed:", error);
            }
        }
        
        // Try custom API
        if (this.config.customApi.enabled && !success) {
            try {
                success = await this.sendToApi(payload);
                if (success) {
                    alert("✅ Results submitted successfully!\n\nThank you for participating.");
                    return true;
                }
            } catch (error) {
                console.error("API submission failed:", error);
            }
        }
        
        // Fallback to download
        if (this.config.allowDownload && !success) {
            this.downloadResults(jsonString);
            alert(
                "⚠️ Automatic submission failed.\n\n" +
                "Your results have been downloaded as a JSON file.\n" +
                "Please email this file to the researcher."
            );
            return true;
        }
        
        alert("❌ Failed to submit results. Please contact the researcher.");
        return false;
    }
    
    async sendToGoogleForms(jsonString) {
        const { formUrl, fieldId } = this.config.googleForms;
        
        // Google Forms requires form-urlencoded data
        const formData = new FormData();
        formData.append(fieldId, jsonString);
        
        // Note: Google Forms doesn't return proper CORS headers,
        // so we use no-cors mode (can't read response, but data is sent)
        const response = await fetch(formUrl, {
            method: "POST",
            mode: "no-cors",
            body: formData
        });
        
        // With no-cors, we can't check status, but if no error thrown, assume success
        return true;
    }
    
    async sendToApi(payload) {
        const { url, method } = this.config.customApi;
        
        const response = await fetch(url, {
            method: method,
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        });
        
        return response.ok;
    }
    
    downloadResults(jsonString) {
        const blob = new Blob([jsonString], { type: "application/json" });
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = `mushra_results_${this.participantId}_${Date.now()}.json`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }
}

// ============== INTEGRATION WITH WEBMUSHRA ==============

// Initialize handler when page loads
let resultHandler = new ResultHandler(RESULT_CONFIG);

document.addEventListener("DOMContentLoaded", async () => {
    await resultHandler.initialize();
    
    // Display participant ID
    const idDisplay = document.createElement("div");
    idDisplay.id = "participant-id-display";
    idDisplay.style.cssText = `
        position: fixed;
        top: 10px;
        right: 10px;
        background: #f0f0f0;
        padding: 5px 10px;
        border-radius: 4px;
        font-size: 12px;
        z-index: 1000;
    `;
    idDisplay.textContent = `ID: ${resultHandler.participantId}`;
    document.body.appendChild(idDisplay);
});

// Override the default result submission (if webMUSHRA uses one)
// This hooks into webMUSHRA's finish page
window.submitMUSHRAResults = async function(results) {
    return await resultHandler.submitResults(results);
};

// Export for use in other scripts
window.ResultHandler = ResultHandler;
window.resultHandler = resultHandler;