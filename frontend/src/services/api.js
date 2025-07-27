// Localhost for development
const API_BASE_URL = 'http://localhost:5001';

/**
 * API service for handling all backend requests
 * This service provides a generic fetch wrapper with error handling,
 * debugging, and specific methods for interacting with the backend API.
 * It includes methods for getting team configuration, saving requirements,
 * generating code, and performing health checks.
 */
class ApiService {
    /**
     * Constructor initializes the base URL for the API
     */
    constructor() {
        this.baseUrl = API_BASE_URL;
    }

    /**
     * Generic fetch wrapper with error handling and debugging
     */
    async request(endpoint, options = {}) {
        const url = `${this.baseUrl}${endpoint}`;
                
        try {
            const response = await fetch(url, {
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers,
                },
                ...options,
            });

            console.log(`📡 API Response: ${response.status} ${response.statusText}`);

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            const data = await response.json();
            console.log(`✅ API Success:`, data);
            return data;
        } catch (error) {
            console.error(`❌ API Error for ${endpoint}:`, error);
            throw error;
        }
    }

    /**
     * Get team configuration
     */
    async getTeamConfig() {
        return await this.request('/team-config');
    }

    /**
     * Save requirements
     */
    async saveRequirements(requirements) {
        return await this.request('/requirements', {
            method: 'POST',
            body: JSON.stringify({ requirements }),
        });
    }

    /**
     * Generate code
     */
    async generateCode(requirements) {
        return await this.request('/generate', {
            method: 'POST',
            body: JSON.stringify({ requirements }),
        });
    }

    /**
     * Health check
     */
    async healthCheck() {
        return await this.request('/health');
    }
}

// Export a singleton instance
export const apiService = new ApiService();

// Export individual methods for convenience with proper binding
export const getTeamConfig = () => apiService.getTeamConfig();
export const saveRequirements = (requirements) => apiService.saveRequirements(requirements);
export const generateCode = (requirements) => apiService.generateCode(requirements);
export const healthCheck = () => apiService.healthCheck();
