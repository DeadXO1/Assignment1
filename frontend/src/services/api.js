/**
 * API client for communicating with the backend.
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

/**
 * Fetch events from the API
 * @param {Object} params - Query parameters
 * @param {string} params.search - Search term
 * @param {string} params.date_from - Start date (YYYY-MM-DD)
 * @param {string} params.date_to - End date (YYYY-MM-DD)
 * @param {string} params.source - Filter by source
 * @param {number} params.page - Page number
 * @param {number} params.page_size - Items per page
 * @returns {Promise<Object>} Response data
 */
export async function fetchEvents(params = {}) {
  const queryParams = new URLSearchParams();
  
  if (params.search) queryParams.append('search', params.search);
  if (params.date_from) queryParams.append('date_from', params.date_from);
  if (params.date_to) queryParams.append('date_to', params.date_to);
  if (params.source) queryParams.append('source', params.source);
  if (params.page) queryParams.append('page', params.page);
  if (params.page_size) queryParams.append('page_size', params.page_size);
  
  const url = `${API_BASE_URL}/api/events?${queryParams.toString()}`;
  
  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error('Error fetching events:', error);
    throw error;
  }
}

/**
 * Fetch a single event by ID
 * @param {number} eventId - Event ID
 * @returns {Promise<Object>} Event data
 */
export async function fetchEvent(eventId) {
  const url = `${API_BASE_URL}/api/events/${eventId}`;
  
  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error('Error fetching event:', error);
    throw error;
  }
}

/**
 * Submit email capture
 * @param {Object} emailData - Email data
 * @param {string} emailData.email - Email address
 * @param {number} emailData.event_id - Event ID
 * @param {boolean} emailData.opt_in - Opt-in consent
 * @returns {Promise<Object>} Response data
 */
export async function submitEmail(emailData) {
  const url = `${API_BASE_URL}/api/emails`;
  
  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(emailData),
    });
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || `HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error submitting email:', error);
    throw error;
  }
}

